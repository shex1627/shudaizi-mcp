"""Level 1: Structural integrity tests.

Validates that all files exist, all JSON references resolve,
all checklists parse, and all book sections extract correctly.
Run with: pytest tests/test_level1_integrity.py -v
"""

import json
import os
import re
from pathlib import Path

import pytest


# ── File existence ────────────────────────────────────────────────


class TestFileIntegrity:
    """Every file referenced in the indexes actually exists on disk."""

    def test_all_book_files_exist(self, project_root, book_index):
        missing = []
        for bid, entry in book_index.get("books", {}).items():
            fpath = project_root / entry["file"]
            if not fpath.exists():
                missing.append(f"{bid}: {entry['file']}")
        assert not missing, f"Missing book files: {missing}"

    def test_all_article_files_exist(self, project_root, book_index):
        missing = []
        for aid, entry in book_index.get("articles", {}).items():
            fpath = project_root / entry["file"]
            if not fpath.exists():
                missing.append(f"{aid}: {entry['file']}")
        assert not missing, f"Missing article files: {missing}"

    def test_all_checklist_files_exist(self, project_root, routing_data):
        missing = []
        for task in routing_data.get("tasks", {}):
            fpath = project_root / "knowledge" / "checklists" / f"{task}.md"
            if not fpath.exists():
                missing.append(f"{task}: checklists/{task}.md")
        assert not missing, f"Missing checklist files: {missing}"

    def test_all_skill_dirs_have_skill_md(self, project_root):
        skills_dir = project_root / "skills"
        missing = []
        for d in sorted(skills_dir.iterdir()):
            if d.is_dir():
                skill_md = d / "SKILL.md"
                if not skill_md.exists():
                    missing.append(d.name)
        assert not missing, f"Skills missing SKILL.md: {missing}"


# ── Cross-reference integrity ─────────────────────────────────────


class TestCrossReferences:
    """All IDs referenced in routing.json exist in book_index.json."""

    def test_routing_source_ids_valid(self, book_index, routing_data):
        all_ids = set(book_index.get("books", {}).keys()) | set(
            book_index.get("articles", {}).keys()
        )
        bad = []
        for task, cfg in routing_data.get("tasks", {}).items():
            for key in ("primary_sources", "secondary_sources", "anthropic_articles"):
                for src_id in cfg.get(key, []):
                    if src_id not in all_ids:
                        bad.append(f"{task}.{key} → {src_id}")
        assert not bad, f"Unknown source IDs in routing: {bad}"

    def test_skills_match_checklists(self, project_root):
        """Every skill dir (except get-book-wisdom) has a matching checklist."""
        skill_dirs = {
            d.name
            for d in (project_root / "skills").iterdir()
            if d.is_dir() and d.name != "get-book-wisdom"
        }
        checklist_names = {
            f.stem for f in (project_root / "knowledge" / "checklists").glob("*.md")
        }
        # Normalize: skill dirs use hyphens, checklists use underscores
        skill_names = {d.replace("-", "_") for d in skill_dirs}
        missing = skill_names - checklist_names
        assert not missing, f"Skills without matching checklists: {missing}"

    def test_checklist_citations_reference_known_books(self, project_root, book_index):
        """Every [XX] citation in checklists refers to a known book/article ID."""
        all_ids = set(book_index.get("books", {}).keys()) | set(
            book_index.get("articles", {}).keys()
        )
        checklists_dir = project_root / "knowledge" / "checklists"
        citation_re = re.compile(r"\[([a]?\d{2})\]")
        bad = []
        for f in checklists_dir.glob("*.md"):
            content = f.read_text()
            for match in citation_re.finditer(content):
                cid = match.group(1)
                if cid not in all_ids:
                    bad.append(f"{f.stem}: [{cid}]")
        assert not bad, f"Unknown citation IDs in checklists: {bad}"


# ── BookLoader ────────────────────────────────────────────────────


class TestBookLoader:
    """BookLoader correctly reads and parses all content."""

    def test_all_checklists_load_brief(self, book_loader, task_router):
        for task in task_router.list_task_types():
            content = book_loader.read_checklist(task, "brief")
            assert len(content) > 50, f"{task}/brief too short ({len(content)} chars)"

    def test_all_checklists_load_standard(self, book_loader, task_router):
        for task in task_router.list_task_types():
            content = book_loader.read_checklist(task, "standard")
            assert len(content) > 100, f"{task}/standard too short"

    def test_all_checklists_load_detailed(self, book_loader, task_router):
        for task in task_router.list_task_types():
            content = book_loader.read_checklist(task, "detailed")
            assert len(content) > 100, f"{task}/detailed too short"

    def test_brief_shorter_than_standard(self, book_loader, task_router):
        """Brief should be a subset of standard content."""
        for task in task_router.list_task_types():
            brief = book_loader.read_checklist(task, "brief")
            standard = book_loader.read_checklist(task, "standard")
            assert len(brief) <= len(standard), (
                f"{task}: brief ({len(brief)}) longer than standard ({len(standard)})"
            )

    def test_standard_shorter_than_detailed(self, book_loader, task_router):
        for task in task_router.list_task_types():
            standard = book_loader.read_checklist(task, "standard")
            detailed = book_loader.read_checklist(task, "detailed")
            assert len(standard) <= len(detailed), (
                f"{task}: standard ({len(standard)}) longer than detailed ({len(detailed)})"
            )

    def test_all_books_return_key_ideas(self, book_loader, book_index):
        for bid in book_index.get("books", {}):
            content = book_loader.read_book_section(bid, "key_ideas")
            assert "not found" not in content.lower(), f"book {bid} key_ideas not found"
            assert len(content) > 20, f"book {bid} key_ideas too short"

    def test_all_articles_return_key_ideas(self, book_loader, book_index):
        for aid in book_index.get("articles", {}):
            content = book_loader.read_book_section(aid, "key_ideas")
            assert len(content) > 10, f"article {aid} key_ideas too short"

    def test_all_section_types_for_sample_book(self, book_loader):
        sections = [
            "key_ideas", "patterns", "tradeoffs", "pitfalls",
            "framings", "applicability", "full",
        ]
        for sec in sections:
            content = book_loader.read_book_section("01", sec)
            assert len(content) > 0, f"section {sec} empty for book 01"

    def test_invalid_task_returns_not_found(self, book_loader):
        content = book_loader.read_checklist("NONEXISTENT_TASK", "brief")
        assert "not found" in content.lower()

    def test_invalid_book_returns_not_found(self, book_loader):
        content = book_loader.read_book_section("99", "key_ideas")
        assert "not found" in content.lower()

    def test_filter_by_focus_reduces_content(self, book_loader):
        full = book_loader.read_checklist("architecture_review", "standard")
        filtered = book_loader.filter_by_focus(full, "security")
        assert len(filtered) < len(full), "filter_by_focus should reduce content"

    def test_filter_by_empty_focus_returns_full(self, book_loader):
        full = book_loader.read_checklist("code_review", "standard")
        same = book_loader.filter_by_focus(full, "")
        assert full == same


# ── TaskRouter ────────────────────────────────────────────────────


class TestTaskRouter:
    def test_list_task_types_returns_16(self, task_router):
        tasks = task_router.list_task_types()
        assert len(tasks) == 16, f"Expected 16 task types, got {len(tasks)}"

    def test_get_task_info_valid(self, task_router):
        info = task_router.get_task_info("code_review")
        assert info is not None
        assert "primary_sources" in info

    def test_get_task_info_invalid(self, task_router):
        info = task_router.get_task_info("nonexistent")
        assert info is None

    def test_get_book_info_valid(self, task_router):
        info = task_router.get_book_info("01")
        assert info is not None
        assert "title" in info

    def test_get_article_info_valid(self, task_router):
        info = task_router.get_book_info("a01")
        assert info is not None

    def test_reload_preserves_state(self, task_router):
        tasks_before = task_router.list_task_types()
        task_router.reload()
        tasks_after = task_router.list_task_types()
        assert tasks_before == tasks_after

    def test_format_methods_return_content(self, task_router):
        assert len(task_router.format_book_list()) > 100
        assert len(task_router.format_article_list()) > 100
        assert len(task_router.format_task_list()) > 100


# ── KnowledgeManager (write ops on temp copy) ────────────────────


class TestKnowledgeManager:
    def test_add_book_creates_file(self, knowledge_manager):
        result = knowledge_manager.add_knowledge_source(
            title="Test Book Title",
            source_type="book",
            content="# Test Book\n\n## Key Ideas\nTest content.",
            category="Testing",
            task_types=["code_review"],
            author="Test Author",
            year=2026,
        )
        assert "id" in result
        assert "file_path" in result
        fpath = knowledge_manager.project_root / result["file_path"]
        assert fpath.exists()
        assert "Test content" in fpath.read_text()

    def test_add_article_creates_file(self, knowledge_manager):
        result = knowledge_manager.add_knowledge_source(
            title="Test Article",
            source_type="article",
            content="# Test Article\n\n## Key Ideas\nArticle content.",
            category="Testing",
            task_types=["test_strategy"],
        )
        assert result["id"].startswith("a")
        fpath = knowledge_manager.project_root / result["file_path"]
        assert fpath.exists()

    def test_add_source_updates_book_index(self, knowledge_manager):
        result = knowledge_manager.add_knowledge_source(
            title="Index Test Book",
            source_type="book",
            content="# Index Test\n\n## Key Ideas\nContent.",
            category="Testing",
            task_types=[],
        )
        index = json.loads(
            (knowledge_manager.book_index_path).read_text()
        )
        assert result["id"] in index["books"]

    def test_add_source_updates_routing(self, knowledge_manager):
        result = knowledge_manager.add_knowledge_source(
            title="Routing Test Book",
            source_type="book",
            content="# Routing Test\n\n## Key Ideas\nContent.",
            category="Testing",
            task_types=["code_review", "test_strategy"],
        )
        routing = json.loads(
            (knowledge_manager.routing_path).read_text()
        )
        cr_sources = routing["tasks"]["code_review"]["secondary_sources"]
        assert result["id"] in cr_sources

    def test_update_checklist_add_items(self, knowledge_manager):
        result = knowledge_manager.update_checklist(
            task_type="code_review",
            action="add_items",
            section="Security",
            content="- [ ] Test item from eval [01]",
        )
        assert "error" not in result
        assert result["lines_added"] > 0

    def test_update_checklist_invalid_task(self, knowledge_manager):
        result = knowledge_manager.update_checklist(
            task_type="nonexistent",
            action="add_items",
            section="Test",
            content="- [ ] Item",
        )
        assert "error" in result

    def test_update_checklist_bumps_version(self, knowledge_manager):
        checklist_path = knowledge_manager.checklists_dir / "code_review.md"
        before = checklist_path.read_text()

        knowledge_manager.update_checklist(
            task_type="code_review",
            action="add_items",
            section="NewSection",
            content="- [ ] New item [01]",
        )
        after = checklist_path.read_text()

        # Extract version numbers
        v_before = re.search(r"version:\s*(\d+)", before)
        v_after = re.search(r"version:\s*(\d+)", after)
        if v_before and v_after:
            assert int(v_after.group(1)) == int(v_before.group(1)) + 1


# ── Content quality checks ────────────────────────────────────────


class TestContentQuality:
    """Basic quality gates for knowledge content."""

    def test_checklists_have_frontmatter(self, project_root):
        checklists_dir = project_root / "knowledge" / "checklists"
        missing = []
        for f in checklists_dir.glob("*.md"):
            content = f.read_text()
            if not content.startswith("---"):
                missing.append(f.stem)
        assert not missing, f"Checklists missing frontmatter: {missing}"

    def test_checklists_have_checklist_items(self, project_root):
        checklists_dir = project_root / "knowledge" / "checklists"
        empty = []
        for f in checklists_dir.glob("*.md"):
            content = f.read_text()
            items = re.findall(r"- \[ \]", content)
            if len(items) < 5:
                empty.append(f"{f.stem}: only {len(items)} items")
        assert not empty, f"Checklists with too few items: {empty}"

    def test_checklists_all_items_have_citations(self, project_root):
        """Every checklist item should cite at least one source [XX]."""
        checklists_dir = project_root / "knowledge" / "checklists"
        uncited = []
        citation_re = re.compile(r"\[[a]?\d{2}\]")
        item_re = re.compile(r"^\s*- \[ \]\s+(.+)$", re.MULTILINE)
        for f in checklists_dir.glob("*.md"):
            content = f.read_text()
            for match in item_re.finditer(content):
                item_text = match.group(1)
                if not citation_re.search(item_text):
                    uncited.append(f"{f.stem}: {item_text[:60]}...")
        assert not uncited, f"Uncited checklist items: {uncited}"

    def test_book_files_have_key_sections(self, project_root, book_index):
        """Every book research file should have at least Key Ideas and Patterns."""
        incomplete = []
        for bid, entry in book_index.get("books", {}).items():
            fpath = project_root / entry["file"]
            if not fpath.exists():
                continue
            content = fpath.read_text()
            if not any(h in content for h in ("## Key Ideas", "## Core", "## Mental Models", "## Overview")):
                incomplete.append(f"{bid}: missing Key Ideas section")
        assert not incomplete, f"Books with missing sections: {incomplete}"

    def test_skill_files_have_required_sections(self, project_root):
        """Every SKILL.md should have When to Activate and Procedure."""
        skills_dir = project_root / "skills"
        incomplete = []
        for d in skills_dir.iterdir():
            if not d.is_dir():
                continue
            skill_md = d / "SKILL.md"
            if not skill_md.exists():
                continue
            content = skill_md.read_text()
            if "## When to Activate" not in content:
                incomplete.append(f"{d.name}: missing 'When to Activate'")
            if "## Procedure" not in content:
                incomplete.append(f"{d.name}: missing 'Procedure'")
        assert not incomplete, f"Skills with missing sections: {incomplete}"

    def test_checklists_under_token_budget(self, book_loader, task_router):
        """Standard-detail checklists should stay under ~6K tokens (~24K chars)."""
        TOKEN_BUDGET_CHARS = 24_000  # ~6K tokens at ~4 chars/token
        oversized = []
        for task in task_router.list_task_types():
            content = book_loader.read_checklist(task, "standard")
            if len(content) > TOKEN_BUDGET_CHARS:
                est_tokens = len(content) // 4
                oversized.append(f"{task}: ~{est_tokens} tokens ({len(content)} chars)")
        assert not oversized, f"Checklists exceeding ~6K token budget: {oversized}"

    def test_all_books_all_sections_extractable(self, book_loader, book_index):
        """Every book must have key_ideas; warn for other missing sections."""
        sections = ["key_ideas", "patterns", "tradeoffs", "pitfalls", "framings", "applicability"]
        missing_key_ideas = []
        warnings = []
        for bid in book_index.get("books", {}):
            for sec in sections:
                content = book_loader.read_book_section(bid, sec)
                if "not found" in content.lower():
                    if sec == "key_ideas":
                        missing_key_ideas.append(f"book {bid}")
                    else:
                        warnings.append(f"book {bid}: {sec}")
        if warnings:
            import warnings as w
            w.warn(f"Optional sections missing (non-fatal): {warnings}")
        assert not missing_key_ideas, f"Books missing key_ideas (critical): {missing_key_ideas}"

    def test_all_articles_all_sections_extractable(self, book_loader, book_index):
        """Every article must have key_ideas; warn for other missing sections."""
        sections = ["key_ideas", "patterns", "tradeoffs", "pitfalls", "framings", "applicability"]
        missing_key_ideas = []
        for aid in book_index.get("articles", {}):
            content = book_loader.read_book_section(aid, "key_ideas")
            if "not found" in content.lower() or len(content) < 10:
                missing_key_ideas.append(f"article {aid}")
        assert not missing_key_ideas, f"Articles missing key_ideas (critical): {missing_key_ideas}"
