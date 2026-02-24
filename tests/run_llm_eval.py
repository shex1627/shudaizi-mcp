#!/usr/bin/env python3
"""Level 3A LLM Eval: End-to-end evaluation with Claude.

For each eval fixture, sends the code sample + shudaizi checklist to Claude
and grades whether the response identifies the known issues.

Computes pass@k (capability) and pass^k (reliability) across multiple trials.

Usage:
    python tests/run_llm_eval.py                  # default: 3 trials, sonnet
    python tests/run_llm_eval.py --trials 5
    python tests/run_llm_eval.py --model claude-sonnet-4-20250514
    python tests/run_llm_eval.py --fixture security_sql_injection  # single fixture
    python tests/run_llm_eval.py --no-checklist   # baseline without shudaizi

Requires: ANTHROPIC_API_KEY environment variable.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import anthropic

# Add MCP server source to path
MCP_SRC = Path(__file__).resolve().parent.parent / "mcp_server" / "src"
sys.path.insert(0, str(MCP_SRC))

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

from shudaizi_mcp.book_loader import BookLoader
from shudaizi_mcp.routing import TaskRouter


# ── Data structures ───────────────────────────────────────────────


@dataclass
class FindingResult:
    finding_id: str
    passed: bool
    matched_keywords: list[str]


@dataclass
class TrialResult:
    fixture_name: str
    trial_num: int
    findings: list[FindingResult]
    all_passed: bool
    response_text: str
    latency_ms: int


@dataclass
class FixtureResult:
    fixture_name: str
    task_type: str
    trials: list[TrialResult]
    pass_at_k: float = 0.0
    pass_pow_k: float = 0.0

    def compute_metrics(self):
        if not self.trials:
            return
        successes = sum(1 for t in self.trials if t.all_passed)
        k = len(self.trials)
        self.pass_at_k = 1.0 - ((1.0 - successes / k) ** k) if k > 0 else 0.0
        self.pass_pow_k = (successes / k) ** k if k > 0 else 0.0


# ── Fixture loading ───────────────────────────────────────────────


def discover_fixtures(filter_name: str | None = None) -> list[tuple[str, Path]]:
    fixtures = []
    for d in sorted(FIXTURES_DIR.iterdir()):
        if d.is_dir() and (d / "ground_truth.json").exists():
            gt = json.loads((d / "ground_truth.json").read_text())
            if gt.get("eval_mode") == "activation":
                continue  # activation fixtures are tested by run_activation_eval.py
            if filter_name and d.name != filter_name:
                continue
            fixtures.append((d.name, d))
    return fixtures


def load_fixture(fixture_dir: Path) -> tuple[str, dict, str]:
    code_files = [f for f in fixture_dir.iterdir() if f.suffix in (".py", ".js", ".ts", ".go", ".java")]
    code = code_files[0].read_text() if code_files else ""
    ground_truth = json.loads((fixture_dir / "ground_truth.json").read_text())
    prompt_file = fixture_dir / "prompt.md"
    prompt_text = prompt_file.read_text() if prompt_file.exists() else ""
    return code, ground_truth, prompt_text


# ── Checklist loading ─────────────────────────────────────────────


def get_checklist(task_type: str, detail_level: str = "standard", focus: str = "") -> str:
    loader = BookLoader(PROJECT_ROOT)
    content = loader.read_checklist(task_type, detail_level)
    if focus:
        content = loader.filter_by_focus(content, focus)
    return content


# ── LLM interaction ───────────────────────────────────────────────


REVIEW_PROMPT = """\
You are a senior software engineer performing a {task_type} review.

{checklist_section}

Review the following code and identify all issues, vulnerabilities, or problems.
For each issue found, explain what it is and why it matters.

```
{code}
```

Respond with a structured list of findings. Be specific and cite the relevant principle or checklist item where applicable."""


REVIEW_PROMPT_NO_CHECKLIST = """\
You are a senior software engineer performing a {task_type} review.

Review the following code and identify all issues, vulnerabilities, or problems.
For each issue found, explain what it is and why it matters.

```
{code}
```

Respond with a structured list of findings. Be specific."""


GENERATE_PROMPT = """\
You are a senior software engineer writing production code.

{checklist_section}

{prompt_text}

Write the implementation. Include all necessary imports."""


GENERATE_PROMPT_NO_CHECKLIST = """\
You are a senior software engineer writing production code.

{prompt_text}

Write the implementation. Include all necessary imports."""


async def run_trial(
    client: anthropic.AsyncAnthropic,
    model: str,
    code: str,
    ground_truth: dict,
    checklist: str | None,
    trial_num: int,
    prompt_text: str = "",
) -> TrialResult:
    task_type = ground_truth["task_type"].replace("_", " ")
    eval_mode = ground_truth.get("eval_mode", "reactive")

    if eval_mode == "proactive":
        if checklist:
            checklist_section = f"Use the following checklist to guide your implementation:\n\n{checklist}"
            prompt = GENERATE_PROMPT.format(
                checklist_section=checklist_section,
                prompt_text=prompt_text,
            )
        else:
            prompt = GENERATE_PROMPT_NO_CHECKLIST.format(prompt_text=prompt_text)
    elif checklist:
        checklist_section = f"Use the following checklist to guide your review:\n\n{checklist}"
        prompt = REVIEW_PROMPT.format(
            task_type=task_type,
            checklist_section=checklist_section,
            code=code,
        )
    else:
        prompt = REVIEW_PROMPT_NO_CHECKLIST.format(task_type=task_type, code=code)

    start = time.monotonic()
    response = await client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    latency_ms = int((time.monotonic() - start) * 1000)

    response_text = response.content[0].text
    response_lower = response_text.lower()

    # Grade each expected finding
    findings = []
    for finding in ground_truth["expected_findings"]:
        matched = [kw for kw in finding["keywords"] if kw.lower() in response_lower]
        findings.append(FindingResult(
            finding_id=finding["id"],
            passed=len(matched) > 0,
            matched_keywords=matched,
        ))

    all_passed = all(f.passed for f in findings)

    return TrialResult(
        fixture_name="",
        trial_num=trial_num,
        findings=findings,
        all_passed=all_passed,
        response_text=response_text,
        latency_ms=latency_ms,
    )


# ── Main eval loop ────────────────────────────────────────────────


async def run_eval(
    model: str,
    num_trials: int,
    filter_fixture: str | None,
    use_checklist: bool,
) -> list[FixtureResult]:
    client = anthropic.AsyncAnthropic()
    fixtures = discover_fixtures(filter_fixture)

    if not fixtures:
        print(f"No fixtures found{f' matching {filter_fixture}' if filter_fixture else ''}.")
        return []

    # Build all tasks upfront for concurrent execution
    async def run_fixture(fixture_name: str, fixture_dir: Path) -> FixtureResult:
        code, gt, prompt_text = load_fixture(fixture_dir)

        checklist = None
        if use_checklist:
            checklist = get_checklist(
                gt["task_type"],
                gt.get("detail_level", "standard"),
                gt.get("focus", ""),
            )

        # Run all trials for this fixture concurrently
        trial_coros = [
            run_trial(client, model, code, gt, checklist, trial_num, prompt_text)
            for trial_num in range(1, num_trials + 1)
        ]
        trials = await asyncio.gather(*trial_coros)

        fixture_result = FixtureResult(
            fixture_name=fixture_name,
            task_type=gt["task_type"],
            trials=[],
        )

        for trial in trials:
            trial.fixture_name = fixture_name
            fixture_result.trials.append(trial)

            status = "PASS" if trial.all_passed else "FAIL"
            findings_detail = ", ".join(
                f"{f.finding_id}:{'OK' if f.passed else 'MISS'}" for f in trial.findings
            )
            print(f"  [{status}] {fixture_name} trial {trial.trial_num}/{num_trials} "
                  f"({trial.latency_ms}ms) — {findings_detail}")

        fixture_result.compute_metrics()
        return fixture_result

    # Run ALL fixtures concurrently
    fixture_coros = [
        run_fixture(name, fdir) for name, fdir in fixtures
    ]
    results = await asyncio.gather(*fixture_coros)
    await client.close()

    return list(results)


def print_summary(results: list[FixtureResult], use_checklist: bool):
    mode = "WITH checklist" if use_checklist else "WITHOUT checklist (baseline)"
    k = results[0].trials.__len__() if results else 0

    print(f"\n{'=' * 70}")
    print(f"  EVAL SUMMARY — {mode} — k={k}")
    print(f"{'=' * 70}")
    print(f"{'Fixture':<35} {'Task':<20} {'Pass@k':>8} {'Pass^k':>8} {'Trials':>8}")
    print(f"{'-' * 35} {'-' * 20} {'-' * 8} {'-' * 8} {'-' * 8}")

    total_pass_at_k = 0
    total_pass_pow_k = 0

    for r in results:
        trial_summary = f"{sum(1 for t in r.trials if t.all_passed)}/{len(r.trials)}"
        print(f"{r.fixture_name:<35} {r.task_type:<20} {r.pass_at_k:>7.0%} {r.pass_pow_k:>7.0%} {trial_summary:>8}")
        total_pass_at_k += r.pass_at_k
        total_pass_pow_k += r.pass_pow_k

    n = len(results)
    if n > 0:
        print(f"{'-' * 35} {'-' * 20} {'-' * 8} {'-' * 8} {'-' * 8}")
        print(f"{'AVERAGE':<35} {'':<20} {total_pass_at_k / n:>7.0%} {total_pass_pow_k / n:>7.0%}")

    print()


async def async_main():
    parser = argparse.ArgumentParser(description="Run Level 3A LLM eval")
    parser.add_argument("--trials", type=int, default=3, help="Number of trials per fixture (default: 3)")
    parser.add_argument("--model", default="claude-sonnet-4-20250514", help="Model ID")
    parser.add_argument("--fixture", default=None, help="Run only this fixture")
    parser.add_argument("--no-checklist", action="store_true", help="Run baseline without checklist")
    parser.add_argument("--compare", action="store_true", help="Run both with and without checklist")
    args = parser.parse_args()

    if args.compare:
        print("\n--- Running WITH checklist ---\n")
        with_results = await run_eval(args.model, args.trials, args.fixture, use_checklist=True)
        print_summary(with_results, use_checklist=True)

        print("\n--- Running WITHOUT checklist (baseline) ---\n")
        without_results = await run_eval(args.model, args.trials, args.fixture, use_checklist=False)
        print_summary(without_results, use_checklist=False)

        # Delta summary
        print(f"\n{'=' * 70}")
        print(f"  COMPARISON: Checklist vs Baseline")
        print(f"{'=' * 70}")
        print(f"{'Fixture':<35} {'With':>8} {'Without':>8} {'Delta':>8}")
        print(f"{'-' * 35} {'-' * 8} {'-' * 8} {'-' * 8}")
        for w, wo in zip(with_results, without_results):
            w_rate = sum(1 for t in w.trials if t.all_passed) / len(w.trials)
            wo_rate = sum(1 for t in wo.trials if t.all_passed) / len(wo.trials)
            delta = w_rate - wo_rate
            sign = "+" if delta > 0 else ""
            print(f"{w.fixture_name:<35} {w_rate:>7.0%} {wo_rate:>7.0%} {sign}{delta:>7.0%}")
        print()
    else:
        print(f"\nModel: {args.model} | Trials: {args.trials} | Checklist: {not args.no_checklist}\n")
        results = await run_eval(args.model, args.trials, args.fixture, use_checklist=not args.no_checklist)
        print_summary(results, use_checklist=not args.no_checklist)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
