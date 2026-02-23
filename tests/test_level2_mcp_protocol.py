"""Level 2: MCP protocol tests.

Tests the MCP server through the actual protocol layer — verifies
tool schemas, tool dispatch, response formats, and error handling.
Run with: pytest tests/test_level2_mcp_protocol.py -v
"""

import asyncio
import json
from pathlib import Path

import pytest
from mcp.types import (
    CallToolRequest,
    CallToolRequestParams,
    ListToolsRequest,
    TextContent,
)

from shudaizi_mcp.server import create_server


@pytest.fixture
def mcp_server():
    return create_server()


async def list_tools(server):
    handler = server.request_handlers[ListToolsRequest]
    result = await handler(ListToolsRequest(method="tools/list"))
    return result.root.tools


async def call_tool(server, name: str, arguments: dict | None = None):
    handler = server.request_handlers[CallToolRequest]
    result = await handler(
        CallToolRequest(
            method="tools/call",
            params=CallToolRequestParams(name=name, arguments=arguments or {}),
        )
    )
    return result.root


# ── Tool listing ──────────────────────────────────────────────────


class TestToolListing:
    """The server exposes the correct tools with valid schemas."""

    @pytest.mark.asyncio
    async def test_lists_five_tools(self, mcp_server):
        tools = await list_tools(mcp_server)
        assert len(tools) == 5

    @pytest.mark.asyncio
    async def test_tool_names(self, mcp_server):
        tools = await list_tools(mcp_server)
        names = {t.name for t in tools}
        expected = {
            "get_task_checklist",
            "get_book_knowledge",
            "list_available_knowledge",
            "add_knowledge_source",
            "update_checklist",
        }
        assert names == expected

    @pytest.mark.asyncio
    async def test_tool_schemas_have_required_fields(self, mcp_server):
        tools = await list_tools(mcp_server)
        for tool in tools:
            assert tool.name, "Tool missing name"
            assert tool.description, f"Tool {tool.name} missing description"
            assert tool.inputSchema, f"Tool {tool.name} missing inputSchema"
            assert "properties" in tool.inputSchema, (
                f"Tool {tool.name} schema missing properties"
            )

    @pytest.mark.asyncio
    async def test_get_task_checklist_schema(self, mcp_server):
        tools = await list_tools(mcp_server)
        tool = next(t for t in tools if t.name == "get_task_checklist")
        props = tool.inputSchema["properties"]
        assert "task_type" in props
        assert "focus" in props
        assert "detail_level" in props
        assert tool.inputSchema["required"] == ["task_type"]

    @pytest.mark.asyncio
    async def test_get_book_knowledge_schema(self, mcp_server):
        tools = await list_tools(mcp_server)
        tool = next(t for t in tools if t.name == "get_book_knowledge")
        props = tool.inputSchema["properties"]
        assert "book_id" in props
        assert "section" in props
        assert "full" in props["section"]["enum"]
        assert tool.inputSchema["required"] == ["book_id"]

    @pytest.mark.asyncio
    async def test_add_knowledge_source_schema(self, mcp_server):
        tools = await list_tools(mcp_server)
        tool = next(t for t in tools if t.name == "add_knowledge_source")
        required = set(tool.inputSchema["required"])
        assert {"title", "source_type", "content", "category", "task_types"} == required

    @pytest.mark.asyncio
    async def test_update_checklist_schema(self, mcp_server):
        tools = await list_tools(mcp_server)
        tool = next(t for t in tools if t.name == "update_checklist")
        required = set(tool.inputSchema["required"])
        assert {"task_type", "action", "section", "content"} == required


# ── Read tool calls ───────────────────────────────────────────────


class TestReadToolCalls:
    """Read tools return correct TextContent responses."""

    @pytest.mark.asyncio
    async def test_get_task_checklist_returns_content(self, mcp_server):
        result = await call_tool(
            mcp_server, "get_task_checklist", {"task_type": "code_review"}
        )
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)
        assert len(result.content[0].text) > 100

    @pytest.mark.asyncio
    async def test_get_task_checklist_with_focus(self, mcp_server):
        result = await call_tool(
            mcp_server,
            "get_task_checklist",
            {"task_type": "architecture_review", "focus": "security", "detail_level": "brief"},
        )
        assert len(result.content[0].text) > 0

    @pytest.mark.asyncio
    async def test_get_task_checklist_all_detail_levels(self, mcp_server):
        sizes = {}
        for level in ("brief", "standard", "detailed"):
            result = await call_tool(
                mcp_server,
                "get_task_checklist",
                {"task_type": "code_review", "detail_level": level},
            )
            sizes[level] = len(result.content[0].text)
        assert sizes["brief"] <= sizes["standard"] <= sizes["detailed"]

    @pytest.mark.asyncio
    async def test_get_task_checklist_invalid_task(self, mcp_server):
        result = await call_tool(
            mcp_server, "get_task_checklist", {"task_type": "nonexistent"}
        )
        assert "not found" in result.content[0].text.lower()

    @pytest.mark.asyncio
    async def test_get_book_knowledge_returns_section(self, mcp_server):
        result = await call_tool(
            mcp_server, "get_book_knowledge", {"book_id": "01", "section": "key_ideas"}
        )
        text = result.content[0].text
        assert len(text) > 50
        assert "not found" not in text.lower()

    @pytest.mark.asyncio
    async def test_get_book_knowledge_full(self, mcp_server):
        result = await call_tool(
            mcp_server, "get_book_knowledge", {"book_id": "01", "section": "full"}
        )
        assert len(result.content[0].text) > 1000

    @pytest.mark.asyncio
    async def test_get_book_knowledge_article(self, mcp_server):
        result = await call_tool(
            mcp_server, "get_book_knowledge", {"book_id": "a01"}
        )
        assert len(result.content[0].text) > 10

    @pytest.mark.asyncio
    async def test_get_book_knowledge_invalid_id(self, mcp_server):
        result = await call_tool(
            mcp_server, "get_book_knowledge", {"book_id": "99"}
        )
        assert "not found" in result.content[0].text.lower()

    @pytest.mark.asyncio
    async def test_list_available_knowledge_all(self, mcp_server):
        result = await call_tool(
            mcp_server, "list_available_knowledge", {"category": "all"}
        )
        text = result.content[0].text
        assert "Books" in text
        assert "Articles" in text
        assert "Task" in text

    @pytest.mark.asyncio
    async def test_list_available_knowledge_books_only(self, mcp_server):
        result = await call_tool(
            mcp_server, "list_available_knowledge", {"category": "books"}
        )
        text = result.content[0].text
        assert "Books" in text
        assert "Task" not in text

    @pytest.mark.asyncio
    async def test_list_available_knowledge_default(self, mcp_server):
        result = await call_tool(mcp_server, "list_available_knowledge", {})
        assert len(result.content[0].text) > 200


# ── Tool dispatch & error handling ────────────────────────────────


class TestToolDispatch:
    @pytest.mark.asyncio
    async def test_unknown_tool_returns_message(self, mcp_server):
        result = await call_tool(mcp_server, "nonexistent_tool", {})
        assert "unknown tool" in result.content[0].text.lower()

    @pytest.mark.asyncio
    async def test_every_task_type_returns_content(self, mcp_server):
        """Call get_task_checklist for every known task type."""
        task_types = [
            "architecture_review", "code_review", "security_audit", "test_strategy",
            "bug_fix", "feature_design", "api_design", "data_viz_review",
            "product_doc", "presentation", "devops", "ai_ml_design",
            "refactoring", "observability", "ux_review", "agent_design",
        ]
        for task in task_types:
            result = await call_tool(
                mcp_server, "get_task_checklist", {"task_type": task}
            )
            assert len(result.content[0].text) > 100, (
                f"Task {task} returned insufficient content"
            )

    @pytest.mark.asyncio
    async def test_every_book_returns_content(self, mcp_server):
        """Call get_book_knowledge for books 01-33."""
        for i in range(1, 34):
            bid = f"{i:02d}"
            result = await call_tool(
                mcp_server, "get_book_knowledge", {"book_id": bid}
            )
            text = result.content[0].text
            assert "not found" not in text.lower(), f"Book {bid} not found"

    @pytest.mark.asyncio
    async def test_every_article_returns_content(self, mcp_server):
        """Call get_book_knowledge for articles a01-a21."""
        for i in range(1, 22):
            aid = f"a{i:02d}"
            result = await call_tool(
                mcp_server, "get_book_knowledge", {"book_id": aid}
            )
            text = result.content[0].text
            assert len(text) > 10, f"Article {aid} returned too little content"

    @pytest.mark.asyncio
    async def test_response_is_not_error(self, mcp_server):
        """Successful tool calls should not have isError set."""
        result = await call_tool(
            mcp_server, "get_task_checklist", {"task_type": "code_review"}
        )
        assert not result.isError
