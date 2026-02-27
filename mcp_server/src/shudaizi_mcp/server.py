"""Shudaizi MCP Server — software engineering knowledge from 33 books + 21 Anthropic articles."""

from __future__ import annotations

from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server

from .tools import register_tools

# Project root is 3 levels up from this file:
# mcp_server/src/shudaizi_mcp/server.py → project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def create_server() -> Server:
    """Create and configure the MCP server."""
    server = Server("shudaizi-mcp")
    register_tools(server, PROJECT_ROOT)
    return server


async def _run() -> None:
    server = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main() -> None:
    """Entry point for the shudaizi-mcp command."""
    import asyncio

    asyncio.run(_run())


def main_http(host: str = "127.0.0.1", port: int = 8530) -> None:
    """Entry point for StreamableHTTP mode (used with Cloudflare Tunnel)."""
    import uvicorn
    from starlette.applications import Starlette
    from starlette.routing import Route
    from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

    server = create_server()
    session_manager = StreamableHTTPSessionManager(app=server, stateless=True)

    class _AsgiApp:
        async def __call__(self, scope, receive, send):
            await session_manager.handle_request(scope, receive, send)

    starlette_app = Starlette(
        routes=[Route("/mcp", endpoint=_AsgiApp())],
        lifespan=lambda app: session_manager.run(),
    )
    uvicorn.run(starlette_app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
