"""Shared fixtures for shudaizi tests."""

import sys
from pathlib import Path

import pytest

# Add the MCP server source to the path
MCP_SRC = Path(__file__).resolve().parent.parent / "mcp_server" / "src"
sys.path.insert(0, str(MCP_SRC))

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def project_root():
    return PROJECT_ROOT


@pytest.fixture
def book_loader():
    from shudaizi_mcp.book_loader import BookLoader
    return BookLoader(PROJECT_ROOT)


@pytest.fixture
def task_router():
    from shudaizi_mcp.routing import TaskRouter
    return TaskRouter(PROJECT_ROOT / "knowledge")


@pytest.fixture
def knowledge_manager(tmp_path):
    """KnowledgeManager pointed at a temp copy to avoid mutating real data."""
    import shutil
    import json

    # Copy the project structure to tmp_path for write-operation tests
    for subdir in ["book_research", "knowledge"]:
        src = PROJECT_ROOT / subdir
        dst = tmp_path / subdir
        shutil.copytree(src, dst)

    from shudaizi_mcp.knowledge_manager import KnowledgeManager
    return KnowledgeManager(tmp_path)


@pytest.fixture
def book_index(project_root):
    import json
    return json.loads((project_root / "knowledge" / "book_index.json").read_text())


@pytest.fixture
def routing_data(project_root):
    import json
    return json.loads((project_root / "knowledge" / "routing.json").read_text())
