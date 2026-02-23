"""Task routing — maps task types to book sources using routing.json."""

from __future__ import annotations

import json
from pathlib import Path


class TaskRouter:
    """Routes task types to their relevant knowledge sources."""

    def __init__(self, knowledge_dir: Path):
        self.knowledge_dir = knowledge_dir
        self.routing_path = knowledge_dir / "routing.json"
        self.book_index_path = knowledge_dir / "book_index.json"
        self._routing_data: dict | None = None
        self._book_index: dict | None = None

    @property
    def routing_data(self) -> dict:
        """Lazy-load routing.json, re-read on each access for live updates."""
        if self._routing_data is None:
            self._reload_routing()
        return self._routing_data

    @property
    def book_index(self) -> dict:
        """Lazy-load book_index.json."""
        if self._book_index is None:
            self._reload_book_index()
        return self._book_index

    def _reload_routing(self) -> None:
        if self.routing_path.exists():
            self._routing_data = json.loads(
                self.routing_path.read_text(encoding="utf-8")
            )
        else:
            self._routing_data = {"tasks": {}}

    def _reload_book_index(self) -> None:
        if self.book_index_path.exists():
            self._book_index = json.loads(
                self.book_index_path.read_text(encoding="utf-8")
            )
        else:
            self._book_index = {"books": {}, "articles": {}}

    def reload(self) -> None:
        """Force reload all data from disk."""
        self._routing_data = None
        self._book_index = None

    def list_task_types(self) -> list[str]:
        """Return all available task type slugs."""
        return list(self.routing_data.get("tasks", {}).keys())

    def get_task_info(self, task_type: str) -> dict | None:
        """Get routing info for a task type."""
        return self.routing_data.get("tasks", {}).get(task_type)

    def get_book_info(self, book_id: str) -> dict | None:
        """Get metadata for a book or article."""
        if book_id.startswith("a"):
            return self.book_index.get("articles", {}).get(book_id)
        return self.book_index.get("books", {}).get(book_id)

    def format_book_list(self) -> str:
        """Format all books as a readable list."""
        lines = ["# Available Books\n"]
        for bid, info in sorted(self.book_index.get("books", {}).items()):
            lines.append(f"- [{bid}] {info['title']} — {info['author']} ({info.get('year', '?')})")
        return "\n".join(lines)

    def format_article_list(self) -> str:
        """Format all articles as a readable list."""
        lines = ["# Available Anthropic Articles\n"]
        for aid, info in sorted(self.book_index.get("articles", {}).items()):
            lines.append(f"- [{aid}] {info['title']} ({info.get('date', '?')})")
        return "\n".join(lines)

    def format_task_list(self) -> str:
        """Format all task types as a readable list."""
        lines = ["# Available Task Checklists\n"]
        for task_type, info in sorted(self.routing_data.get("tasks", {}).items()):
            desc = info.get("description", "")
            primary = ", ".join(info.get("primary_sources", []))
            lines.append(f"- **{task_type}**: {desc}")
            lines.append(f"  Primary sources: [{primary}]")
        return "\n".join(lines)
