#!/usr/bin/env python3
"""Proactive Activation Eval: Does the model decide to use MCP tools on its own?

For each activation fixture, sends a realistic user scenario to Claude with
MCP tool definitions available (via the tools parameter) but NO instruction
to use them. Grades whether the model proactively invokes the right tool.

Metrics:
  - Activation rate: did it call any shudaizi tool?
  - Selection accuracy: did it call the right tool with the right task_type?
  - Quality: did the output contain expected patterns? (keyword matching)

Two conditions:
  A) Tools available, no instruction → measures proactive activation
  B) No tools available → baseline output quality

Usage:
    python tests/run_activation_eval.py                  # default: 5 trials, sonnet
    python tests/run_activation_eval.py --trials 10
    python tests/run_activation_eval.py --model claude-sonnet-4-20250514
    python tests/run_activation_eval.py --fixture activation_code_review_async

Requires: ANTHROPIC_API_KEY environment variable (or .env file).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import anthropic

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Auto-load .env if present
_env_file = PROJECT_ROOT / ".env"
if _env_file.exists():
    import os
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

FIXTURES_DIR = Path(__file__).parent / "eval_fixtures"

# ── MCP tool schemas for the Anthropic SDK ───────────────────────
# Only the 3 read tools. Uses input_schema (snake_case) per SDK convention.

TASK_TYPES = [
    "architecture_review", "code_review", "security_audit", "test_strategy",
    "bug_fix", "feature_design", "api_design", "data_viz_review",
    "product_doc", "presentation", "devops", "ai_ml_design",
    "refactoring", "observability", "ux_review", "agent_design",
]
TASK_ENUM_DESC = ", ".join(TASK_TYPES)

SDK_TOOLS = [
    {
        "name": "get_task_checklist",
        "description": (
            "Get a curated checklist for a software engineering task. "
            "Returns actionable items drawn from 33 books and 21 Anthropic articles, each citing its source. "
            "Use this as your primary review/design companion."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "task_type": {
                    "type": "string",
                    "description": f"Task type. Available: {TASK_ENUM_DESC}",
                },
                "focus": {
                    "type": "string",
                    "description": "Optional: narrow to specific sub-topics (comma-separated). Example: 'security,scalability'",
                    "default": "",
                },
                "detail_level": {
                    "type": "string",
                    "enum": ["brief", "standard", "detailed"],
                    "description": "brief = items only (~1-3K tokens), standard = items + questions (~3-6K), detailed = everything (~5-10K)",
                    "default": "standard",
                },
            },
            "required": ["task_type"],
        },
    },
    {
        "name": "get_book_knowledge",
        "description": (
            "Retrieve knowledge from a specific book or Anthropic article. "
            "Returns the requested section for deep-dive context. "
            "Use when you need deeper understanding of a principle cited in a checklist (e.g., [01] → book 01)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "book_id": {
                    "type": "string",
                    "description": "Book ID ('01'-'33') or article ID ('a01'-'a21'). Use list_available_knowledge to discover IDs.",
                },
                "section": {
                    "type": "string",
                    "enum": ["key_ideas", "patterns", "tradeoffs", "pitfalls", "framings", "applicability", "full"],
                    "description": "Which section to return. 'full' returns entire file (use sparingly).",
                    "default": "key_ideas",
                },
            },
            "required": ["book_id"],
        },
    },
    {
        "name": "list_available_knowledge",
        "description": (
            "List all available knowledge in the system: task checklists, books, and articles. "
            "Use this to discover what's available before requesting specifics."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["all", "tasks", "books", "articles"],
                    "description": "What to list.",
                    "default": "all",
                },
            },
        },
    },
]


# ── Data structures ──────────────────────────────────────────────


@dataclass
class ToolCallResult:
    tool_name: str
    tool_input: dict
    matched_expected: bool
    matched_acceptable: bool


@dataclass
class TrialResult:
    fixture_name: str
    trial_num: int
    activated: bool          # any shudaizi tool called?
    selection_correct: bool  # right tool + right task_type?
    quality_passed: bool     # output keywords matched?
    tool_calls: list[ToolCallResult]
    matched_keywords: list[str]
    response_text: str
    latency_ms: int


@dataclass
class FixtureResult:
    fixture_name: str
    trials: list[TrialResult] = field(default_factory=list)
    activation_rate: float = 0.0
    selection_rate: float = 0.0
    quality_rate: float = 0.0

    def compute_metrics(self):
        if not self.trials:
            return
        n = len(self.trials)
        self.activation_rate = sum(1 for t in self.trials if t.activated) / n
        self.selection_rate = sum(1 for t in self.trials if t.selection_correct) / n
        self.quality_rate = sum(1 for t in self.trials if t.quality_passed) / n


# ── Fixture loading ──────────────────────────────────────────────


def discover_fixtures(filter_name: str | None = None) -> list[tuple[str, Path]]:
    """Find activation fixtures (eval_mode == 'activation')."""
    fixtures = []
    for d in sorted(FIXTURES_DIR.iterdir()):
        if not d.is_dir():
            continue
        gt_path = d / "ground_truth.json"
        if not gt_path.exists():
            continue
        gt = json.loads(gt_path.read_text())
        if gt.get("eval_mode") != "activation":
            continue
        if filter_name and d.name != filter_name:
            continue
        fixtures.append((d.name, d))
    return fixtures


def load_fixture(fixture_dir: Path) -> tuple[dict, str]:
    """Load ground_truth.json and prompt.md from a fixture directory."""
    ground_truth = json.loads((fixture_dir / "ground_truth.json").read_text())
    prompt_text = (fixture_dir / "prompt.md").read_text()
    return ground_truth, prompt_text


# ── Grading ──────────────────────────────────────────────────────


def grade_tool_calls(
    response,
    expected_tool_calls: list[dict],
) -> tuple[bool, bool, list[ToolCallResult]]:
    """Grade tool_use blocks in the response.

    Returns: (activated, selection_correct, tool_call_results)
    """
    # Extract tool_use blocks
    tool_use_blocks = [
        block for block in response.content
        if block.type == "tool_use"
    ]

    shudaizi_tools = {"get_task_checklist", "get_book_knowledge", "list_available_knowledge"}
    relevant_calls = [b for b in tool_use_blocks if b.name in shudaizi_tools]

    activated = len(relevant_calls) > 0

    results = []
    selection_correct = False

    for call in relevant_calls:
        matched_expected = False
        matched_acceptable = False

        for expected in expected_tool_calls:
            if call.name != expected["tool_name"]:
                continue

            # Check exact match on expected_args
            expected_args = expected.get("expected_args", {})
            if all(call.input.get(k) == v for k, v in expected_args.items()):
                matched_expected = True
                selection_correct = True
                break

            # Check acceptable alternatives
            for alt in expected.get("acceptable_args", []):
                if all(call.input.get(k) == v for k, v in alt.items()):
                    matched_acceptable = True
                    selection_correct = True
                    break

        results.append(ToolCallResult(
            tool_name=call.name,
            tool_input=dict(call.input) if hasattr(call.input, 'items') else call.input,
            matched_expected=matched_expected,
            matched_acceptable=matched_acceptable,
        ))

    return activated, selection_correct, results


def grade_quality(
    response,
    expected_findings: list[dict],
) -> tuple[bool, list[str]]:
    """Grade text content in the response for expected keywords."""
    # Collect all text from text blocks
    text_parts = [
        block.text for block in response.content
        if block.type == "text"
    ]
    response_text = "\n".join(text_parts).lower()

    all_matched = []
    all_passed = True

    for finding in expected_findings:
        keywords = finding.get("keywords", [])
        matched = []
        for kw in keywords:
            # Support regex patterns in keywords (e.g., "mock.*stripe")
            try:
                if re.search(kw.lower(), response_text):
                    matched.append(kw)
            except re.error:
                # Fall back to simple substring match
                if kw.lower() in response_text:
                    matched.append(kw)

        all_matched.extend(matched)
        if not matched:
            all_passed = False

    return all_passed, all_matched


# ── LLM interaction ──────────────────────────────────────────────

PROMPT_TEMPLATE = """\
You are a senior software engineer. Complete the following task.

{prompt_text}"""

PROMPT_TEMPLATE_NO_TOOLS = """\
You are a senior software engineer. Complete the following task.

{prompt_text}"""


async def run_trial(
    client: anthropic.AsyncAnthropic,
    model: str,
    ground_truth: dict,
    prompt_text: str,
    trial_num: int,
    use_tools: bool,
) -> TrialResult:
    """Run a single activation eval trial."""
    prompt = PROMPT_TEMPLATE.format(prompt_text=prompt_text)

    kwargs = {
        "model": model,
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
    }
    if use_tools:
        kwargs["tools"] = SDK_TOOLS

    start = time.monotonic()
    response = await client.messages.create(**kwargs)
    latency_ms = int((time.monotonic() - start) * 1000)

    # Grade tool calls
    if use_tools:
        activated, selection_correct, tool_call_results = grade_tool_calls(
            response, ground_truth.get("expected_tool_calls", [])
        )
    else:
        activated = False
        selection_correct = False
        tool_call_results = []

    # Grade output quality
    quality_passed, matched_keywords = grade_quality(
        response, ground_truth.get("expected_findings", [])
    )

    # Collect response text for debugging
    text_parts = [b.text for b in response.content if b.type == "text"]
    response_text = "\n".join(text_parts)

    return TrialResult(
        fixture_name="",
        trial_num=trial_num,
        activated=activated,
        selection_correct=selection_correct,
        quality_passed=quality_passed,
        tool_calls=tool_call_results,
        matched_keywords=matched_keywords,
        response_text=response_text,
        latency_ms=latency_ms,
    )


# ── Main eval loop ───────────────────────────────────────────────


async def run_eval(
    model: str,
    num_trials: int,
    filter_fixture: str | None,
    use_tools: bool,
) -> list[FixtureResult]:
    """Run activation eval across all fixtures."""
    client = anthropic.AsyncAnthropic()
    fixtures = discover_fixtures(filter_fixture)

    if not fixtures:
        print(f"No activation fixtures found{f' matching {filter_fixture}' if filter_fixture else ''}.")
        return []

    async def run_fixture(fixture_name: str, fixture_dir: Path) -> FixtureResult:
        gt, prompt_text = load_fixture(fixture_dir)

        trial_coros = [
            run_trial(client, model, gt, prompt_text, i, use_tools)
            for i in range(1, num_trials + 1)
        ]
        trials = await asyncio.gather(*trial_coros)

        result = FixtureResult(fixture_name=fixture_name)
        for trial in trials:
            trial.fixture_name = fixture_name
            result.trials.append(trial)

            # Print per-trial status
            mode = "TOOLS" if use_tools else "BASE"
            tool_info = ""
            if use_tools:
                if trial.activated:
                    calls = ", ".join(
                        f"{tc.tool_name}({tc.tool_input.get('task_type', '?')})"
                        for tc in trial.tool_calls
                    )
                    sel = "EXACT" if any(tc.matched_expected for tc in trial.tool_calls) \
                        else "ALT" if any(tc.matched_acceptable for tc in trial.tool_calls) \
                        else "WRONG"
                    tool_info = f" → {calls} [{sel}]"
                else:
                    tool_info = " → no tool called"

            if use_tools:
                # With tools, quality is not meaningful (model stops at tool_use)
                print(f"  [{mode}] {fixture_name} trial {trial.trial_num}/{num_trials} "
                      f"({trial.latency_ms}ms){tool_info}")
            else:
                quality = "Q:OK" if trial.quality_passed else "Q:MISS"
                print(f"  [{mode}] {fixture_name} trial {trial.trial_num}/{num_trials} "
                      f"({trial.latency_ms}ms) {quality}")

        result.compute_metrics()
        return result

    fixture_coros = [run_fixture(name, fdir) for name, fdir in fixtures]
    results = await asyncio.gather(*fixture_coros)
    await client.close()
    return list(results)


def print_summary(results: list[FixtureResult], use_tools: bool):
    """Print a summary table."""
    mode = "WITH TOOLS (proactive)" if use_tools else "WITHOUT TOOLS (baseline)"
    k = len(results[0].trials) if results else 0

    print(f"\n{'=' * 78}")
    print(f"  {mode} — k={k}")
    print(f"{'=' * 78}")

    if use_tools:
        # With tools: model stops at tool_use, so quality is N/A — show activation metrics only
        print(f"{'Fixture':<40} {'Activated':>10} {'Selection':>10} {'Most Common':>20}")
        print(f"{'-' * 40} {'-' * 10} {'-' * 10} {'-' * 20}")
        for r in results:
            # Find most common task_type called
            type_counts: dict[str, int] = {}
            for t in r.trials:
                for tc in t.tool_calls:
                    tt = tc.tool_input.get("task_type", "?")
                    type_counts[tt] = type_counts.get(tt, 0) + 1
            most_common = max(type_counts, key=type_counts.get) if type_counts else "—"
            print(f"{r.fixture_name:<40} {r.activation_rate:>9.0%} {r.selection_rate:>9.0%} {most_common:>20}")
        n = len(results)
        avg_act = sum(r.activation_rate for r in results) / n
        avg_sel = sum(r.selection_rate for r in results) / n
        print(f"{'-' * 40} {'-' * 10} {'-' * 10} {'-' * 20}")
        print(f"{'AVERAGE':<40} {avg_act:>9.0%} {avg_sel:>9.0%}")
    else:
        print(f"{'Fixture':<40} {'Quality':>10} {'Trials':>10}")
        print(f"{'-' * 40} {'-' * 10} {'-' * 10}")
        for r in results:
            passed = sum(1 for t in r.trials if t.quality_passed)
            print(f"{r.fixture_name:<40} {r.quality_rate:>9.0%} {passed}/{len(r.trials):>8}")
        n = len(results)
        avg_q = sum(r.quality_rate for r in results) / n
        print(f"{'-' * 40} {'-' * 10} {'-' * 10}")
        print(f"{'AVERAGE':<40} {avg_q:>9.0%}")

    print()


def print_comparison(with_results: list[FixtureResult], without_results: list[FixtureResult]):
    """Print a comparison table showing activation behavior.

    Note: Quality comparison between tools/no-tools is not meaningful because
    the model stops at tool_use (waiting for tool results) when tools are
    available. Instead we show: activation rate, selection accuracy, and
    baseline quality (what the model produces without any tools).
    """
    print(f"\n{'=' * 78}")
    print(f"  RESULTS SUMMARY")
    print(f"{'=' * 78}")
    print(f"{'Fixture':<40} {'Activated':>10} {'Selection':>10} {'Base Q':>10}")
    print(f"{'-' * 40} {'-' * 10} {'-' * 10} {'-' * 10}")

    for w, wo in zip(with_results, without_results):
        print(f"{w.fixture_name:<40} {w.activation_rate:>9.0%} {w.selection_rate:>9.0%} "
              f"{wo.quality_rate:>9.0%}")

    n = len(with_results)
    avg_act = sum(r.activation_rate for r in with_results) / n
    avg_sel = sum(r.selection_rate for r in with_results) / n
    avg_qwo = sum(r.quality_rate for r in without_results) / n
    print(f"{'-' * 40} {'-' * 10} {'-' * 10} {'-' * 10}")
    print(f"{'AVERAGE':<40} {avg_act:>9.0%} {avg_sel:>9.0%} {avg_qwo:>9.0%}")
    print()
    print("  Activated = model called any shudaizi tool")
    print("  Selection = called the expected task_type (exact or acceptable)")
    print("  Base Q    = baseline quality without tools (keyword match)")
    print()


async def async_main():
    parser = argparse.ArgumentParser(description="Run proactive activation eval")
    parser.add_argument("--trials", type=int, default=5, help="Number of trials per fixture (default: 5)")
    parser.add_argument("--model", default="claude-sonnet-4-20250514", help="Model ID")
    parser.add_argument("--fixture", default=None, help="Run only this fixture")
    args = parser.parse_args()

    print(f"\nModel: {args.model} | Trials: {args.trials}")
    print(f"Fixtures: {args.fixture or 'all activation fixtures'}\n")

    # Condition A: Tools available
    print("--- Condition A: Tools available (no instruction) ---\n")
    with_results = await run_eval(args.model, args.trials, args.fixture, use_tools=True)
    print_summary(with_results, use_tools=True)

    # Condition B: No tools (baseline)
    print("--- Condition B: No tools (baseline) ---\n")
    without_results = await run_eval(args.model, args.trials, args.fixture, use_tools=False)
    print_summary(without_results, use_tools=False)

    # Comparison
    if with_results and without_results:
        print_comparison(with_results, without_results)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
