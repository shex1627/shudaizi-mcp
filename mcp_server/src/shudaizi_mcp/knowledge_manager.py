"""Knowledge management — add sources, update checklists (write operations)."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


class KnowledgeManager:
    """Handles write operations: adding knowledge sources and updating checklists."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.book_research_dir = project_root / "book_research"
        self.articles_dir = self.book_research_dir / "anthropic_articles"
        self.knowledge_dir = project_root / "knowledge"
        self.checklists_dir = self.knowledge_dir / "checklists"
        self.routing_path = self.knowledge_dir / "routing.json"
        self.book_index_path = self.knowledge_dir / "book_index.json"

    def _load_json(self, path: Path) -> dict:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return {}

    def _save_json(self, path: Path, data: dict) -> None:
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def _next_book_id(self) -> str:
        """Find the next available book ID."""
        index = self._load_json(self.book_index_path)
        existing = [int(k) for k in index.get("books", {}).keys() if k.isdigit()]
        next_num = max(existing, default=0) + 1
        return f"{next_num:02d}"

    def _next_article_id(self) -> str:
        """Find the next available article ID."""
        index = self._load_json(self.book_index_path)
        existing = [
            int(k[1:])
            for k in index.get("articles", {}).keys()
            if k.startswith("a") and k[1:].isdigit()
        ]
        next_num = max(existing, default=0) + 1
        return f"a{next_num:02d}"

    def _slugify(self, title: str) -> str:
        """Convert a title to a filename-safe slug."""
        slug = title.lower()
        slug = re.sub(r"[^a-z0-9\s]", "", slug)
        slug = re.sub(r"\s+", "_", slug.strip())
        return slug[:60]  # cap length

    def add_knowledge_source(
        self,
        title: str,
        source_type: str,
        content: str,
        category: str,
        task_types: list[str],
        author: str = "",
        year: int | None = None,
    ) -> dict:
        """Add a new book or article to the knowledge base.

        Returns dict with: id, file_path, tasks_updated.
        """
        is_article = source_type in ("article", "blog")

        # Assign ID
        if is_article:
            source_id = self._next_article_id()
            num = source_id[1:]  # e.g., "22" from "a22"
        else:
            source_id = self._next_book_id()
            num = source_id

        # Create filename
        slug = self._slugify(title)
        filename = f"{num}_{slug}.md"

        if is_article:
            file_path = self.articles_dir / filename
        else:
            file_path = self.book_research_dir / filename

        # Write the content file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

        # Update book_index.json
        index = self._load_json(self.book_index_path)
        relative_path = str(file_path.relative_to(self.project_root))

        if is_article:
            if "articles" not in index:
                index["articles"] = {}
            index["articles"][source_id] = {
                "title": title,
                "date": date.today().isoformat(),
                "category": category,
                "file": relative_path,
            }
        else:
            if "books" not in index:
                index["books"] = {}
            entry = {
                "title": title,
                "category": category,
                "file": relative_path,
            }
            if author:
                entry["author"] = author
            if year:
                entry["year"] = year
            index["books"][source_id] = entry

        index["updated"] = date.today().isoformat()
        self._save_json(self.book_index_path, index)

        # Update routing.json
        routing = self._load_json(self.routing_path)
        tasks_updated = []

        for task_type in task_types:
            if task_type in routing.get("tasks", {}):
                task_info = routing["tasks"][task_type]
                source_key = "anthropic_articles" if is_article else "secondary_sources"
                if source_id not in task_info.get(source_key, []):
                    if source_key not in task_info:
                        task_info[source_key] = []
                    task_info[source_key].append(source_id)
                    tasks_updated.append(task_type)

        routing["updated"] = date.today().isoformat()
        self._save_json(self.routing_path, routing)

        return {
            "id": source_id,
            "file_path": relative_path,
            "tasks_updated": tasks_updated,
            "message": f"Added '{title}' as {source_id}. File: {relative_path}. Updated routing for: {', '.join(tasks_updated) or 'none'}.",
        }

    def update_checklist(
        self,
        task_type: str,
        action: str,
        section: str,
        content: str,
    ) -> dict:
        """Update a task checklist.

        Actions: add_items, remove_items, replace_section.
        Returns dict with: task_type, action, diff summary.
        """
        checklist_path = self.checklists_dir / f"{task_type}.md"
        if not checklist_path.exists():
            return {"error": f"Checklist '{task_type}' not found."}

        original = checklist_path.read_text(encoding="utf-8")
        lines = original.split("\n")

        if action == "add_items":
            result = self._add_items_to_section(lines, section, content)
        elif action == "remove_items":
            result = self._remove_items(lines, content)
        elif action == "replace_section":
            result = self._replace_section(lines, section, content)
        else:
            return {"error": f"Unknown action '{action}'. Use: add_items, remove_items, replace_section."}

        # Bump version
        result = self._bump_version(result)

        new_content = "\n".join(result)
        checklist_path.write_text(new_content, encoding="utf-8")

        # Count changes
        added = len(set(result) - set(lines))
        removed = len(set(lines) - set(result))

        return {
            "task_type": task_type,
            "action": action,
            "section": section,
            "lines_added": added,
            "lines_removed": removed,
            "message": f"Updated '{task_type}' checklist: {action} in '{section}'. +{added}/-{removed} lines.",
        }

    def _add_items_to_section(
        self, lines: list[str], section: str, content: str
    ) -> list[str]:
        """Add items to a specific section of the checklist."""
        result = []
        found = False
        inserted = False

        for i, line in enumerate(lines):
            result.append(line)
            if not found and line.startswith("## ") and section.lower() in line.lower():
                found = True
                continue
            if found and not inserted:
                # Find the end of the current section's items
                if line.startswith("## ") or (line.strip() == "" and i + 1 < len(lines) and lines[i + 1].startswith("## ")):
                    # Insert before the next section
                    new_items = content.strip().split("\n")
                    result = result[:-1] + new_items + ["", line]
                    inserted = True

        # If section found but we reached end of file
        if found and not inserted:
            result.append("")
            result.extend(content.strip().split("\n"))

        # If section not found, append as new section
        if not found:
            result.append("")
            result.append(f"## {section}")
            result.extend(content.strip().split("\n"))

        return result

    def _remove_items(self, lines: list[str], content: str) -> list[str]:
        """Remove lines matching the given content patterns."""
        patterns = [p.strip() for p in content.strip().split("\n") if p.strip()]
        return [line for line in lines if not any(p in line for p in patterns)]

    def _replace_section(
        self, lines: list[str], section: str, content: str
    ) -> list[str]:
        """Replace an entire section with new content."""
        result = []
        skipping = False

        for line in lines:
            if line.startswith("## ") and section.lower() in line.lower():
                skipping = True
                result.append(line)
                result.extend(content.strip().split("\n"))
                continue
            if skipping and line.startswith("## "):
                skipping = False
            if not skipping:
                result.append(line)

        return result

    def _bump_version(self, lines: list[str]) -> list[str]:
        """Increment version number and update date in frontmatter."""
        result = []
        for line in lines:
            if line.startswith("version:"):
                try:
                    current = int(line.split(":")[1].strip())
                    result.append(f"version: {current + 1}")
                except (ValueError, IndexError):
                    result.append(line)
            elif line.startswith("updated:"):
                result.append(f"updated: {date.today().isoformat()}")
            else:
                result.append(line)
        return result
