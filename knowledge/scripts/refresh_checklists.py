#!/usr/bin/env python3
"""Staleness detector: compare book research file mtimes vs. checklist mtimes.

Usage:
    python knowledge/scripts/refresh_checklists.py

Reports which checklists may need updating because their source books
have been modified more recently.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def load_routing() -> dict:
    routing_path = PROJECT_ROOT / "knowledge" / "routing.json"
    with open(routing_path) as f:
        return json.load(f)


def get_book_path(book_id: str) -> Path | None:
    """Resolve a book/article ID to its file path."""
    if book_id.startswith("a"):
        # Anthropic article
        pattern = f"{book_id[1:].zfill(2)}_*.md"
        matches = list((PROJECT_ROOT / "book_research" / "anthropic_articles").glob(pattern))
    else:
        pattern = f"{book_id.zfill(2)}_*.md"
        matches = list((PROJECT_ROOT / "book_research").glob(pattern))
    return matches[0] if matches else None


def get_checklist_version(checklist_path: Path) -> tuple[int, str]:
    """Extract version and updated date from checklist frontmatter."""
    text = checklist_path.read_text()
    version_match = re.search(r"^version:\s*(\d+)", text, re.MULTILINE)
    updated_match = re.search(r"^updated:\s*(.+)", text, re.MULTILINE)
    version = int(version_match.group(1)) if version_match else 0
    updated = updated_match.group(1).strip() if updated_match else "unknown"
    return version, updated


def check_staleness() -> list[dict]:
    """Check each checklist against its source files for staleness."""
    routing = load_routing()
    results = []

    for task_type, info in routing["tasks"].items():
        checklist_path = PROJECT_ROOT / "knowledge" / info["checklist_file"]
        if not checklist_path.exists():
            results.append({
                "task": task_type,
                "status": "MISSING",
                "message": f"Checklist file does not exist: {info['checklist_file']}",
            })
            continue

        checklist_mtime = checklist_path.stat().st_mtime
        version, updated = get_checklist_version(checklist_path)

        all_sources = (
            info.get("primary_sources", [])
            + info.get("secondary_sources", [])
            + info.get("anthropic_articles", [])
        )

        stale_sources = []
        for source_id in all_sources:
            source_path = get_book_path(source_id)
            if source_path and source_path.stat().st_mtime > checklist_mtime:
                stale_sources.append(source_id)

        if stale_sources:
            results.append({
                "task": task_type,
                "status": "STALE",
                "version": version,
                "updated": updated,
                "stale_sources": stale_sources,
                "message": f"Sources newer than checklist: {', '.join(stale_sources)}",
            })
        else:
            results.append({
                "task": task_type,
                "status": "OK",
                "version": version,
                "updated": updated,
                "message": "Up to date",
            })

    return results


def main() -> None:
    results = check_staleness()

    # Summary
    missing = [r for r in results if r["status"] == "MISSING"]
    stale = [r for r in results if r["status"] == "STALE"]
    ok = [r for r in results if r["status"] == "OK"]

    print(f"\n{'='*60}")
    print(f"  Shudaizi Checklist Staleness Report")
    print(f"{'='*60}\n")

    if missing:
        print(f"MISSING ({len(missing)}):")
        for r in missing:
            print(f"  - {r['task']}: {r['message']}")
        print()

    if stale:
        print(f"STALE ({len(stale)}):")
        for r in stale:
            print(f"  - {r['task']} (v{r['version']}, {r['updated']}): {r['message']}")
        print()

    print(f"OK ({len(ok)}):")
    for r in ok:
        print(f"  - {r['task']} (v{r['version']}, {r['updated']})")

    print(f"\nTotal: {len(ok)} ok, {len(stale)} stale, {len(missing)} missing")


if __name__ == "__main__":
    main()
