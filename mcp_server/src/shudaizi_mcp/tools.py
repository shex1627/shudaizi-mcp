"""MCP tool definitions — 5 tools (3 read + 2 write)."""

from __future__ import annotations

from pathlib import Path

from mcp.server import Server
from mcp.types import TextContent, Tool

from .book_loader import BookLoader
from .knowledge_manager import KnowledgeManager
from .routing import TaskRouter


def register_tools(
    server: Server,
    project_root: Path,
) -> None:
    """Register all MCP tools on the server."""

    loader = BookLoader(project_root)
    router = TaskRouter(project_root / "knowledge")
    manager = KnowledgeManager(project_root)

    # ── Read Tools ──────────────────────────────────────────────

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        task_types = router.list_task_types()
        task_enum_desc = ", ".join(task_types) if task_types else "check knowledge/checklists/ directory"

        return [
            Tool(
                name="get_task_checklist",
                description=(
                    "Get a curated checklist for a software engineering task. "
                    "Returns actionable items drawn from 33 books and 21 Anthropic articles, each citing its source. "
                    "Use this as your primary review/design companion."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task_type": {
                            "type": "string",
                            "description": f"Task type. Available: {task_enum_desc}",
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
            ),
            Tool(
                name="get_book_knowledge",
                description=(
                    "Retrieve knowledge from a specific book or Anthropic article. "
                    "Returns the requested section for deep-dive context. "
                    "Use when you need deeper understanding of a principle cited in a checklist (e.g., [01] → book 01)."
                ),
                inputSchema={
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
            ),
            Tool(
                name="list_available_knowledge",
                description=(
                    "List all available knowledge in the system: task checklists, books, and articles. "
                    "Use this to discover what's available before requesting specifics."
                ),
                inputSchema={
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
            ),
            # ── Write Tools ──────────────────────────────────────────
            Tool(
                name="add_knowledge_source",
                description=(
                    "Add a new book, article, or blog post to the knowledge base. "
                    "You provide the research content (following the standard template with Key Ideas, Patterns, Tradeoffs, etc.), "
                    "and this tool handles file creation, index updates, and routing. "
                    "The research template is in book_research_prompts.md."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Title of the book, article, or blog post.",
                        },
                        "source_type": {
                            "type": "string",
                            "enum": ["book", "article", "blog"],
                            "description": "Type of knowledge source.",
                        },
                        "content": {
                            "type": "string",
                            "description": "Full research markdown content following the standard template.",
                        },
                        "category": {
                            "type": "string",
                            "description": "Knowledge category (e.g., 'Architecture & System Design', 'Security', 'UX & Interaction Design').",
                        },
                        "task_types": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": f"Which task types this source is relevant to. Available: {task_enum_desc}",
                        },
                        "author": {
                            "type": "string",
                            "description": "Author name(s). Optional.",
                            "default": "",
                        },
                        "year": {
                            "type": "integer",
                            "description": "Publication year. Optional.",
                        },
                    },
                    "required": ["title", "source_type", "content", "category", "task_types"],
                },
            ),
            Tool(
                name="update_checklist",
                description=(
                    "Update a task checklist by adding, removing, or replacing items. "
                    "Use after adding a new knowledge source to incorporate its insights into relevant checklists."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task_type": {
                            "type": "string",
                            "description": f"Which checklist to update. Available: {task_enum_desc}",
                        },
                        "action": {
                            "type": "string",
                            "enum": ["add_items", "remove_items", "replace_section"],
                            "description": "add_items: append items to a section. remove_items: remove matching lines. replace_section: replace entire section content.",
                        },
                        "section": {
                            "type": "string",
                            "description": "Section name to target (e.g., 'Data Architecture', 'Security'). For add_items, creates section if it doesn't exist.",
                        },
                        "content": {
                            "type": "string",
                            "description": "The checklist items to add/replace, or patterns to remove. Each item should cite its source: '- [ ] Item description [XX]'",
                        },
                    },
                    "required": ["task_type", "action", "section", "content"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        if name == "get_task_checklist":
            task_type = arguments["task_type"]
            focus = arguments.get("focus", "")
            detail_level = arguments.get("detail_level", "standard")

            content = loader.read_checklist(task_type, detail_level)
            if focus:
                content = loader.filter_by_focus(content, focus)

            return [TextContent(type="text", text=content)]

        elif name == "get_book_knowledge":
            book_id = arguments["book_id"]
            section = arguments.get("section", "key_ideas")

            content = loader.read_book_section(book_id, section)
            return [TextContent(type="text", text=content)]

        elif name == "list_available_knowledge":
            category = arguments.get("category", "all")
            router.reload()  # refresh from disk

            parts = []
            if category in ("all", "tasks"):
                parts.append(router.format_task_list())
            if category in ("all", "books"):
                parts.append(router.format_book_list())
            if category in ("all", "articles"):
                parts.append(router.format_article_list())

            return [TextContent(type="text", text="\n\n".join(parts))]

        elif name == "add_knowledge_source":
            result = manager.add_knowledge_source(
                title=arguments["title"],
                source_type=arguments["source_type"],
                content=arguments["content"],
                category=arguments["category"],
                task_types=arguments["task_types"],
                author=arguments.get("author", ""),
                year=arguments.get("year"),
            )
            return [TextContent(type="text", text=result["message"])]

        elif name == "update_checklist":
            result = manager.update_checklist(
                task_type=arguments["task_type"],
                action=arguments["action"],
                section=arguments["section"],
                content=arguments["content"],
            )
            if "error" in result:
                return [TextContent(type="text", text=f"Error: {result['error']}")]
            return [TextContent(type="text", text=result["message"])]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
