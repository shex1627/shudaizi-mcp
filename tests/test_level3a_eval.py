"""Level 3A: Checklist coverage evaluation (deterministic).

For each eval fixture (code sample with a known issue), verifies that the
corresponding shudaizi checklist contains guidance that would help an agent
identify the issue. This is the code-based grader layer — no LLM needed.

Run with: pytest tests/test_level3a_eval.py -v
"""

import json
from pathlib import Path

import pytest
from mcp.types import (
    CallToolRequest,
    CallToolRequestParams,
    ListToolsRequest,
)

from shudaizi_mcp.server import create_server

FIXTURES_DIR = Path(__file__).parent / "eval_fixtures"


@pytest.fixture
def mcp_server():
    return create_server()


async def call_tool(server, name: str, arguments: dict):
    handler = server.request_handlers[CallToolRequest]
    result = await handler(
        CallToolRequest(
            method="tools/call",
            params=CallToolRequestParams(name=name, arguments=arguments),
        )
    )
    return result.root


def discover_fixtures() -> list[tuple[str, Path]]:
    """Find all eval fixture directories (excludes activation/qualitative fixtures)."""
    fixtures = []
    for d in sorted(FIXTURES_DIR.iterdir()):
        if d.is_dir() and (d / "ground_truth.json").exists():
            gt = json.loads((d / "ground_truth.json").read_text())
            if gt.get("eval_mode"):
                continue  # non-standard fixtures tested by their own scripts
            fixtures.append((d.name, d))
    return fixtures


def load_fixture(fixture_dir: Path) -> tuple[str, dict]:
    """Load code sample and ground truth from a fixture directory."""
    # Find the code file (could be .py, .js, etc.)
    code_files = [f for f in fixture_dir.iterdir() if f.suffix in (".py", ".js", ".ts", ".go", ".java")]
    code = code_files[0].read_text() if code_files else ""
    ground_truth = json.loads((fixture_dir / "ground_truth.json").read_text())
    return code, ground_truth


# ── Fixture discovery ─────────────────────────────────────────────


class TestFixtureIntegrity:
    """All eval fixtures are well-formed."""

    def test_fixtures_exist(self):
        fixtures = discover_fixtures()
        assert len(fixtures) >= 8, f"Expected at least 8 fixtures, found {len(fixtures)}"

    @pytest.mark.parametrize("name,fixture_dir", discover_fixtures())
    def test_fixture_has_code_or_prompt_file(self, name, fixture_dir):
        code_files = [f for f in fixture_dir.iterdir() if f.suffix in (".py", ".js", ".ts", ".go", ".java")]
        prompt_file = fixture_dir / "prompt.md"
        assert len(code_files) >= 1 or prompt_file.exists(), (
            f"Fixture {name} missing both code file and prompt.md"
        )

    @pytest.mark.parametrize("name,fixture_dir", discover_fixtures())
    def test_ground_truth_schema(self, name, fixture_dir):
        gt = json.loads((fixture_dir / "ground_truth.json").read_text())
        assert "task_type" in gt, f"{name}: missing task_type"
        assert "expected_findings" in gt, f"{name}: missing expected_findings"
        for finding in gt["expected_findings"]:
            assert "id" in finding, f"{name}: finding missing id"
            assert "keywords" in finding, f"{name}: finding missing keywords"
            assert len(finding["keywords"]) >= 2, f"{name}/{finding['id']}: need at least 2 keywords"


# ── Checklist coverage grading ────────────────────────────────────


class TestChecklistCoverage:
    """For each fixture, the relevant checklist contains guidance to catch the issue."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("name,fixture_dir", discover_fixtures())
    async def test_checklist_covers_finding(self, name, fixture_dir, mcp_server):
        """The checklist for this fixture's task_type contains at least one keyword
        from each expected finding — meaning the guidance to catch the bug exists."""
        code, gt = load_fixture(fixture_dir)

        result = await call_tool(
            mcp_server,
            "get_task_checklist",
            {
                "task_type": gt["task_type"],
                "detail_level": gt.get("detail_level", "standard"),
                "focus": gt.get("focus", ""),
            },
        )
        checklist_text = result.content[0].text.lower()

        for finding in gt["expected_findings"]:
            matched = [kw for kw in finding["keywords"] if kw.lower() in checklist_text]
            assert matched, (
                f"Fixture '{name}', finding '{finding['id']}': "
                f"checklist '{gt['task_type']}' contains none of {finding['keywords']}"
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("name,fixture_dir", discover_fixtures())
    async def test_checklist_returns_substantial_content(self, name, fixture_dir, mcp_server):
        """The checklist should return enough content to be useful."""
        _, gt = load_fixture(fixture_dir)
        result = await call_tool(
            mcp_server,
            "get_task_checklist",
            {
                "task_type": gt["task_type"],
                "detail_level": gt.get("detail_level", "standard"),
            },
        )
        text = result.content[0].text
        assert len(text) > 500, (
            f"Fixture '{name}': checklist '{gt['task_type']}' returned only {len(text)} chars"
        )


# ── Detail level sensitivity ──────────────────────────────────────


class TestDetailLevelSensitivity:
    """Findings should be present at the specified detail level and above."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("name,fixture_dir", discover_fixtures())
    async def test_finding_present_at_detailed(self, name, fixture_dir, mcp_server):
        """At 'detailed' level, all findings should be covered regardless of the
        fixture's specified detail_level."""
        _, gt = load_fixture(fixture_dir)
        result = await call_tool(
            mcp_server,
            "get_task_checklist",
            {"task_type": gt["task_type"], "detail_level": "detailed"},
        )
        checklist_text = result.content[0].text.lower()

        for finding in gt["expected_findings"]:
            matched = [kw for kw in finding["keywords"] if kw.lower() in checklist_text]
            assert matched, (
                f"Fixture '{name}', finding '{finding['id']}': "
                f"not found even at 'detailed' level"
            )
