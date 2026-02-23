# Shudaizi MCP Server

MCP server that provides software engineering knowledge from 33 books + 21 Anthropic engineering articles. Works with any MCP-compatible coding agent (Claude Code, Cursor, Windsurf, Copilot, etc.).

## Installation

```bash
cd mcp_server
pip install -e .
```

## Configuration

### Claude Code

Add to `~/.claude/settings.json` or project `.claude/settings.json`:

```json
{
  "mcpServers": {
    "shudaizi": {
      "command": "shudaizi-mcp",
      "args": []
    }
  }
}
```

Or with explicit Python path:

```json
{
  "mcpServers": {
    "shudaizi": {
      "command": "python",
      "args": ["-m", "shudaizi_mcp.server"],
      "cwd": "/path/to/shudaizi/mcp_server"
    }
  }
}
```

### Cursor / Windsurf

Add to your MCP configuration (typically `.cursor/mcp.json` or similar):

```json
{
  "mcpServers": {
    "shudaizi": {
      "command": "shudaizi-mcp"
    }
  }
}
```

## Tools

### Read Tools

| Tool | Purpose | Key Params |
|------|---------|------------|
| `get_task_checklist` | Get a curated checklist for a task type | `task_type`, `focus` (optional), `detail_level` (brief/standard/detailed) |
| `get_book_knowledge` | Deep-dive into a specific book section | `book_id` (e.g. "01", "a05"), `section` |
| `list_available_knowledge` | Discover what's in the knowledge base | `category` (all/tasks/books/articles) |

### Write Tools

| Tool | Purpose | Key Params |
|------|---------|------------|
| `add_knowledge_source` | Add a new book/article to the knowledge base | `title`, `source_type`, `content`, `category`, `task_types` |
| `update_checklist` | Modify a task checklist | `task_type`, `action`, `section`, `content` |

## Available Task Types

architecture_review, code_review, security_audit, test_strategy, bug_fix, feature_design, api_design, data_viz_review, product_doc, presentation, devops, ai_ml_design, refactoring, observability, ux_review, agent_design

## Example Usage

```
"Review this architecture for security and scalability"
→ Agent calls get_task_checklist(task_type="architecture_review", focus="security,scalability")

"What does DDIA say about consistency models?"
→ Agent calls get_book_knowledge(book_id="01", section="key_ideas")

"Add knowledge about Thinking Fast and Slow"
→ Agent researches, then calls add_knowledge_source(...)
```

## Architecture

See [ARCHITECTURE.md](../ARCHITECTURE.md) for the full design document.

The server reads from:
- `knowledge/routing.json` — task → book mapping
- `knowledge/book_index.json` — book/article metadata
- `knowledge/checklists/*.md` — curated task checklists
- `book_research/*.md` — full book research files
