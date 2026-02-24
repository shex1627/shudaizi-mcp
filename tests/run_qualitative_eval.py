#!/usr/bin/env python3
"""Qualitative Eval with LLM-as-Judge: Does knowledge improve output quality?

For each qualitative fixture, runs a full conversation loop:
  A) With tools: model calls tools → gets checklist content → completes task
  B) Without tools: model completes task directly

Then an LLM judge grades both outputs on per-criterion rubrics. Comparing
scores tells us whether the knowledge system measurably improves quality.

Metrics:
  - Per-criterion scores: PASS (1.0) / PARTIAL (0.5) / FAIL (0.0)
  - Total quality score: average across criteria
  - Delta: with_tools - without_tools (positive = tools helped)

Usage:
    python tests/run_qualitative_eval.py
    python tests/run_qualitative_eval.py --trials 3 --model claude-sonnet-4-20250514
    python tests/run_qualitative_eval.py --fixture qualitative_data_viz --trials 1
    python tests/run_qualitative_eval.py --judge-model claude-sonnet-4-20250514

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

# Add MCP server source to path for BookLoader import
sys.path.insert(0, str(PROJECT_ROOT / "mcp_server" / "src"))
from shudaizi_mcp.book_loader import BookLoader  # noqa: E402

FIXTURES_DIR = Path(__file__).parent / "eval_fixtures"

# ── MCP tool schemas for the Anthropic SDK ───────────────────────
# Same as run_activation_eval.py — 3 read-only tools.

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


# ── Tool execution via BookLoader ────────────────────────────────

_loader = BookLoader(PROJECT_ROOT)


def execute_tool_call(tool_name: str, tool_input: dict) -> str:
    """Execute a tool call locally using BookLoader. Returns text content."""
    if tool_name == "get_task_checklist":
        task_type = tool_input.get("task_type", "")
        detail_level = tool_input.get("detail_level", "standard")
        focus = tool_input.get("focus", "")
        content = _loader.read_checklist(task_type, detail_level)
        if focus:
            content = _loader.filter_by_focus(content, focus)
        return content

    elif tool_name == "get_book_knowledge":
        book_id = tool_input.get("book_id", "")
        section = tool_input.get("section", "key_ideas")
        return _loader.read_book_section(book_id, section)

    elif tool_name == "list_available_knowledge":
        parts = []
        category = tool_input.get("category", "all")
        if category in ("all", "tasks"):
            checklists = _loader.list_checklists()
            parts.append("# Available Task Checklists\n")
            for c in checklists:
                parts.append(f"- **{c['task_type']}**: {c['description']}")
        if category in ("all", "books"):
            books = _loader.list_books()
            parts.append("\n# Available Books\n")
            for b in books:
                parts.append(f"- [{b['id']}] {b['title']}")
        if category in ("all", "articles"):
            articles = _loader.list_articles()
            parts.append("\n# Available Anthropic Articles\n")
            for a in articles:
                parts.append(f"- [{a['id']}] {a['title']}")
        return "\n".join(parts)

    return f"Unknown tool: {tool_name}"


# ── Data structures ──────────────────────────────────────────────


@dataclass
class CriterionResult:
    criterion_id: int
    criterion_text: str
    verdict: str  # PASS / PARTIAL / FAIL
    score: float  # 1.0 / 0.5 / 0.0
    reasoning: str


@dataclass
class TrialResult:
    fixture_name: str
    trial_num: int
    condition: str  # "with_tools" / "without_tools"
    criteria: list[CriterionResult]
    total_score: float  # 0.0 to 1.0
    tool_calls_made: list[str]
    response_text: str
    latency_ms: int


@dataclass
class FixtureResult:
    fixture_name: str
    with_tools_trials: list[TrialResult] = field(default_factory=list)
    without_tools_trials: list[TrialResult] = field(default_factory=list)
    avg_with: float = 0.0
    avg_without: float = 0.0
    delta: float = 0.0
    per_criterion_with: dict[int, float] = field(default_factory=dict)
    per_criterion_without: dict[int, float] = field(default_factory=dict)
    most_common_tool: str = ""

    def compute_metrics(self):
        if self.with_tools_trials:
            self.avg_with = sum(t.total_score for t in self.with_tools_trials) / len(self.with_tools_trials)
            # Per-criterion averages
            for trial in self.with_tools_trials:
                for cr in trial.criteria:
                    self.per_criterion_with.setdefault(cr.criterion_id, [])
                    self.per_criterion_with[cr.criterion_id].append(cr.score)
            self.per_criterion_with = {k: sum(v) / len(v) for k, v in self.per_criterion_with.items()}

            # Most common tool called
            tool_counts: dict[str, int] = {}
            for t in self.with_tools_trials:
                for tc in t.tool_calls_made:
                    tool_counts[tc] = tool_counts.get(tc, 0) + 1
            self.most_common_tool = max(tool_counts, key=tool_counts.get) if tool_counts else "none"

        if self.without_tools_trials:
            self.avg_without = sum(t.total_score for t in self.without_tools_trials) / len(self.without_tools_trials)
            for trial in self.without_tools_trials:
                for cr in trial.criteria:
                    self.per_criterion_without.setdefault(cr.criterion_id, [])
                    self.per_criterion_without[cr.criterion_id].append(cr.score)
            self.per_criterion_without = {k: sum(v) / len(v) for k, v in self.per_criterion_without.items()}

        self.delta = self.avg_with - self.avg_without


# ── Fixture loading ──────────────────────────────────────────────


def discover_fixtures(filter_name: str | None = None) -> list[tuple[str, Path]]:
    """Find qualitative fixtures (eval_mode == 'qualitative')."""
    fixtures = []
    for d in sorted(FIXTURES_DIR.iterdir()):
        if not d.is_dir():
            continue
        gt_path = d / "ground_truth.json"
        if not gt_path.exists():
            continue
        gt = json.loads(gt_path.read_text())
        if gt.get("eval_mode") != "qualitative":
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


# ── Multi-turn conversation ──────────────────────────────────────

SYSTEM_PROMPT = "You are a senior software engineer. Complete the following task."
MAX_TOOL_TURNS = 5  # prevent runaway tool call loops


async def run_conversation(
    client: anthropic.AsyncAnthropic,
    model: str,
    prompt_text: str,
    use_tools: bool,
) -> tuple[str, list[str], int]:
    """Run a multi-turn conversation, executing tool calls if needed.

    Returns: (final_response_text, tool_calls_made, latency_ms)
    """
    messages = [{"role": "user", "content": prompt_text}]
    tool_calls_made = []

    kwargs = {
        "model": model,
        "max_tokens": 8192,
        "system": SYSTEM_PROMPT,
        "messages": messages,
    }
    if use_tools:
        kwargs["tools"] = SDK_TOOLS

    start = time.monotonic()
    turns = 0

    while turns < MAX_TOOL_TURNS:
        turns += 1
        response = await client.messages.create(**kwargs)

        if response.stop_reason == "end_turn" or response.stop_reason != "tool_use":
            # Done — collect final text
            text_parts = [b.text for b in response.content if b.type == "text"]
            final_text = "\n".join(text_parts)
            latency_ms = int((time.monotonic() - start) * 1000)
            return final_text, tool_calls_made, latency_ms

        # Handle tool calls
        assistant_content = response.content
        tool_results = []

        for block in assistant_content:
            if block.type == "tool_use":
                tool_input = dict(block.input) if hasattr(block.input, 'items') else block.input
                result_text = execute_tool_call(block.name, tool_input)
                tool_calls_made.append(
                    f"{block.name}({tool_input.get('task_type', tool_input.get('book_id', '?'))})"
                )
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result_text,
                })

        # Continue conversation with tool results
        messages.append({"role": "assistant", "content": assistant_content})
        messages.append({"role": "user", "content": tool_results})
        kwargs["messages"] = messages

    # Hit max turns — collect whatever text we have
    text_parts = [b.text for b in response.content if b.type == "text"]
    final_text = "\n".join(text_parts)
    latency_ms = int((time.monotonic() - start) * 1000)
    return final_text, tool_calls_made, latency_ms


# ── LLM Judge ────────────────────────────────────────────────────

JUDGE_PROMPT_TEMPLATE = """\
You are evaluating code quality. Score each criterion independently based on the code/response provided.

TASK DESCRIPTION:
{task_description}

RESPONSE TO EVALUATE:
{response_text}

EVALUATION CRITERIA:
{criteria_list}

For each criterion, provide:
- verdict: exactly one of "PASS", "PARTIAL", or "FAIL"
  - PASS: The response clearly and fully addresses this criterion
  - PARTIAL: The response partially addresses this criterion but has notable gaps
  - FAIL: The response does not meaningfully address this criterion
- evidence: Quote or reference specific parts of the response that support your verdict
- reasoning: Explain your verdict in 1-2 sentences

Respond with ONLY valid JSON in this exact format (no markdown, no explanation outside the JSON):
{{
  "criteria": [
    {{"id": 1, "verdict": "PASS", "evidence": "...", "reasoning": "..."}},
    {{"id": 2, "verdict": "PARTIAL", "evidence": "...", "reasoning": "..."}}
  ]
}}"""


def format_criteria_list(judge_criteria: list[dict]) -> str:
    """Format criteria for the judge prompt."""
    lines = []
    for c in judge_criteria:
        lines.append(f"{c['id']}. {c['text']}")
    return "\n\n".join(lines)


async def judge_output(
    client: anthropic.AsyncAnthropic,
    judge_model: str,
    task_description: str,
    response_text: str,
    judge_criteria: list[dict],
) -> list[CriterionResult]:
    """Use an LLM to evaluate the response against criteria.

    Returns per-criterion results.
    """
    criteria_list = format_criteria_list(judge_criteria)
    prompt = JUDGE_PROMPT_TEMPLATE.format(
        task_description=task_description,
        response_text=response_text,
        criteria_list=criteria_list,
    )

    response = await client.messages.create(
        model=judge_model,
        max_tokens=2048,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}],
    )

    # Parse JSON from response
    judge_text = response.content[0].text.strip()

    # Try to extract JSON if wrapped in markdown code blocks
    json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", judge_text, re.DOTALL)
    if json_match:
        judge_text = json_match.group(1).strip()

    try:
        judge_data = json.loads(judge_text)
    except json.JSONDecodeError:
        # Fallback: try to find JSON object in the text
        json_match = re.search(r"\{.*\}", judge_text, re.DOTALL)
        if json_match:
            judge_data = json.loads(json_match.group())
        else:
            print(f"  WARNING: Could not parse judge response as JSON. Raw: {judge_text[:200]}")
            # Return all FAIL results
            return [
                CriterionResult(
                    criterion_id=c["id"],
                    criterion_text=c["text"][:80],
                    verdict="FAIL",
                    score=0.0,
                    reasoning="Judge response could not be parsed",
                )
                for c in judge_criteria
            ]

    # Map verdicts to scores
    verdict_scores = {"PASS": 1.0, "PARTIAL": 0.5, "FAIL": 0.0}

    results = []
    criteria_by_id = {c["id"]: c for c in judge_criteria}

    for item in judge_data.get("criteria", []):
        cid = item.get("id", 0)
        verdict = item.get("verdict", "FAIL").upper()
        score = verdict_scores.get(verdict, 0.0)
        criterion_text = criteria_by_id.get(cid, {}).get("text", "")[:80]

        results.append(CriterionResult(
            criterion_id=cid,
            criterion_text=criterion_text,
            verdict=verdict,
            score=score,
            reasoning=item.get("reasoning", ""),
        ))

    return results


# ── Trial runner ─────────────────────────────────────────────────


async def run_trial(
    client: anthropic.AsyncAnthropic,
    model: str,
    judge_model: str,
    ground_truth: dict,
    prompt_text: str,
    trial_num: int,
    use_tools: bool,
) -> TrialResult:
    """Run a single qualitative eval trial: conversation + judge."""
    condition = "with_tools" if use_tools else "without_tools"

    # Run the conversation
    response_text, tool_calls_made, latency_ms = await run_conversation(
        client, model, prompt_text, use_tools
    )

    # Judge the output
    criteria_results = await judge_output(
        client,
        judge_model,
        ground_truth["task_description"],
        response_text,
        ground_truth["judge_criteria"],
    )

    total_score = sum(cr.score for cr in criteria_results) / len(criteria_results) if criteria_results else 0.0

    return TrialResult(
        fixture_name="",
        trial_num=trial_num,
        condition=condition,
        criteria=criteria_results,
        total_score=total_score,
        tool_calls_made=tool_calls_made,
        response_text=response_text,
        latency_ms=latency_ms,
    )


# ── Main eval loop ───────────────────────────────────────────────


async def run_eval(
    model: str,
    judge_model: str,
    num_trials: int,
    filter_fixture: str | None,
    use_tools: bool,
) -> list[FixtureResult]:
    """Run qualitative eval across all fixtures for one condition."""
    client = anthropic.AsyncAnthropic()
    fixtures = discover_fixtures(filter_fixture)

    if not fixtures:
        print(f"No qualitative fixtures found{f' matching {filter_fixture}' if filter_fixture else ''}.")
        return []

    async def run_fixture(fixture_name: str, fixture_dir: Path) -> list[TrialResult]:
        gt, prompt_text = load_fixture(fixture_dir)

        # Run all trials concurrently
        trial_coros = [
            run_trial(client, model, judge_model, gt, prompt_text, i, use_tools)
            for i in range(1, num_trials + 1)
        ]
        trials = await asyncio.gather(*trial_coros)

        for trial in trials:
            trial.fixture_name = fixture_name

            # Print per-trial status
            mode = "TOOLS" if use_tools else "BASE"
            tools_info = f" [{', '.join(trial.tool_calls_made)}]" if trial.tool_calls_made else ""
            criteria_summary = " ".join(
                f"C{cr.criterion_id}:{cr.verdict[0]}"
                for cr in trial.criteria
            )
            print(f"  [{mode}] {fixture_name} trial {trial.trial_num}/{num_trials} "
                  f"({trial.latency_ms}ms) score={trial.total_score:.0%} "
                  f"{criteria_summary}{tools_info}")

        return list(trials)

    # Run all fixtures concurrently (trials within each fixture also concurrent)
    fixture_coros = [run_fixture(name, fdir) for name, fdir in fixtures]
    all_trials = await asyncio.gather(*fixture_coros)
    await client.close()

    # Group trials by fixture
    results = []
    for (name, _), trials in zip(fixtures, all_trials):
        result = FixtureResult(fixture_name=name)
        for trial in trials:
            if trial.condition == "with_tools":
                result.with_tools_trials.append(trial)
            else:
                result.without_tools_trials.append(trial)
        results.append(result)

    return results


# ── Output formatting ────────────────────────────────────────────


def print_summary(results: list[FixtureResult], use_tools: bool):
    """Print a summary table for one condition."""
    mode = "WITH TOOLS" if use_tools else "WITHOUT TOOLS (baseline)"
    k = len(results[0].with_tools_trials if use_tools else results[0].without_tools_trials) if results else 0

    print(f"\n{'=' * 78}")
    print(f"  {mode} — k={k}")
    print(f"{'=' * 78}")

    print(f"{'Fixture':<40} {'Avg Score':>10} {'Trials':>10}")
    print(f"{'-' * 40} {'-' * 10} {'-' * 10}")

    for r in results:
        trials = r.with_tools_trials if use_tools else r.without_tools_trials
        if not trials:
            continue
        avg = sum(t.total_score for t in trials) / len(trials)
        print(f"{r.fixture_name:<40} {avg:>9.0%} {len(trials):>10}")

    n = len(results)
    if n > 0:
        overall_avg = sum(
            sum(t.total_score for t in (r.with_tools_trials if use_tools else r.without_tools_trials))
            / max(len(r.with_tools_trials if use_tools else r.without_tools_trials), 1)
            for r in results
        ) / n
        print(f"{'-' * 40} {'-' * 10} {'-' * 10}")
        print(f"{'AVERAGE':<40} {overall_avg:>9.0%}")
    print()


def print_comparison(results: list[FixtureResult]):
    """Print comparison table: with_tools vs without_tools."""
    print(f"\n{'=' * 90}")
    print(f"  QUALITATIVE EVAL RESULTS")
    print(f"{'=' * 90}")
    print(f"{'Fixture':<40} {'With Tools':>10} {'Without':>10} {'Delta':>10} {'Tool Called':>18}")
    print(f"{'-' * 40} {'-' * 10} {'-' * 10} {'-' * 10} {'-' * 18}")

    for r in results:
        delta_str = f"{r.delta:>+9.0%}" if r.delta != 0 else f"{'0%':>10}"
        print(f"{r.fixture_name:<40} {r.avg_with:>9.0%} {r.avg_without:>9.0%} "
              f"{delta_str} {r.most_common_tool:>18}")

    n = len(results)
    if n > 0:
        avg_with = sum(r.avg_with for r in results) / n
        avg_without = sum(r.avg_without for r in results) / n
        avg_delta = avg_with - avg_without
        delta_str = f"{avg_delta:>+9.0%}" if avg_delta != 0 else f"{'0%':>10}"
        print(f"{'-' * 40} {'-' * 10} {'-' * 10} {'-' * 10} {'-' * 18}")
        print(f"{'AVERAGE':<40} {avg_with:>9.0%} {avg_without:>9.0%} {delta_str}")

    # Per-criterion breakdown
    print(f"\n  Per-Criterion Breakdown:")
    print(f"  {'Criterion':<55} {'With':>8} {'Without':>8} {'Delta':>8}")
    print(f"  {'-' * 55} {'-' * 8} {'-' * 8} {'-' * 8}")

    for r in results:
        print(f"\n  {r.fixture_name}:")
        # Get criteria text from first trial
        all_trials = r.with_tools_trials + r.without_tools_trials
        if not all_trials:
            continue
        criteria_texts = {cr.criterion_id: cr.criterion_text for cr in all_trials[0].criteria}

        for cid in sorted(criteria_texts.keys()):
            w_score = r.per_criterion_with.get(cid, 0.0)
            wo_score = r.per_criterion_without.get(cid, 0.0)
            d = w_score - wo_score
            d_str = f"{d:>+7.0%}" if d != 0 else f"{'0%':>8}"
            text = criteria_texts[cid][:50]
            print(f"    C{cid}: {text:<50} {w_score:>7.0%} {wo_score:>7.0%} {d_str}")

    print()
    print("  Scoring: PASS=100%, PARTIAL=50%, FAIL=0%")
    print("  Delta: positive = tools improved quality")
    print()


# ── Main ─────────────────────────────────────────────────────────


async def async_main():
    parser = argparse.ArgumentParser(description="Run qualitative eval with LLM-as-judge")
    parser.add_argument("--trials", type=int, default=5, help="Number of trials per fixture (default: 5)")
    parser.add_argument("--model", default="claude-sonnet-4-20250514", help="Model for code generation")
    parser.add_argument("--judge-model", default=None, help="Model for judging (defaults to same as --model)")
    parser.add_argument("--fixture", default=None, help="Run only this fixture")
    args = parser.parse_args()

    judge_model = args.judge_model or args.model

    print(f"\nModel: {args.model} | Judge: {judge_model} | Trials: {args.trials}")
    print(f"Fixtures: {args.fixture or 'all qualitative fixtures'}\n")

    # Run both conditions concurrently
    print("--- Running both conditions concurrently ---\n")
    with_results, without_results = await asyncio.gather(
        run_eval(args.model, judge_model, args.trials, args.fixture, use_tools=True),
        run_eval(args.model, judge_model, args.trials, args.fixture, use_tools=False),
    )

    # Merge results by fixture name
    merged = []
    without_by_name = {r.fixture_name: r for r in without_results}
    for wr in with_results:
        wor = without_by_name.get(wr.fixture_name)
        if wor:
            wr.without_tools_trials = wor.without_tools_trials
        wr.compute_metrics()
        merged.append(wr)

    # Print results
    print_summary(merged, use_tools=True)
    print_summary(merged, use_tools=False)
    if merged:
        print_comparison(merged)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
