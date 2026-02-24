# Shudaizi

A knowledge system that gives AI coding agents (Claude Code, Cursor, Windsurf, Copilot) access to curated software engineering wisdom from 33 books and 21 Anthropic engineering articles — delivered as focused, token-efficient checklists at the moment they're needed.

## The Problem

When vibe-coding with AI, models lack awareness of established best practices. This causes blind spots in architecture reviews, shallow code reviews, security oversights, and design anti-patterns. The knowledge exists in books — the problem is *delivery*: getting the right subset to the right agent at the right moment without drowning it in tokens.

## How It Works

```
You: "review this architecture"
  │
  ├─ Claude Code ──→ skills/architecture-review/SKILL.md
  │                    reads knowledge/checklists/architecture_review.md
  │                    drills into book_research/01_ddia.md if needed
  │
  └─ Cursor/Other ─→ MCP Server
                       get_task_checklist("architecture_review")
                       get_book_knowledge("01", "patterns") for deep-dive
```

Two delivery interfaces, one shared knowledge layer. No content duplication.

## What's Implemented

### Knowledge Base (34 sources)

32 books + 1 consolidated Anthropic blog + 21 individual Anthropic articles covering:

| Domain | Books | Examples |
|--------|-------|---------|
| Architecture & System Design | 01-06 | DDIA, Clean Architecture, Philosophy of SW Design |
| Security | 07-08 | Web App Hacker's Handbook, LLM Security Playbook |
| AI/ML Engineering | 09-11 | AI Engineering (Huyen), LLM Engineer's Handbook |
| Testing | 12-13 | Unit Testing (Khorikov), GOOS |
| Code Quality | 14-16 | Pragmatic Programmer, Clean Code, Refactoring |
| Operations & Reliability | 17-19 | Release It!, Observability Engineering, SRE |
| API & Data | 20-22 | API Design Patterns, Database Internals, Python Concurrency |
| UX & Design | 23-25 | Design of Everyday Things, Don't Make Me Think, Laws of UX |
| Data Visualization | 26-28 | Storytelling with Data, Tufte, Wilke |
| Product & Process | 29-32 | Inspired, Shape Up, Continuous Discovery, DevOps Handbook |
| Anthropic Engineering | 33 + a01-a21 | Agent design, tool design, evals, context engineering |

### 16 Task-Specific Checklists

Each checklist is a phased, citation-backed review guide (~3-6K tokens) in `knowledge/checklists/`:

`architecture_review` `code_review` `security_audit` `test_strategy` `bug_fix` `feature_design` `api_design` `data_viz_review` `product_doc` `presentation` `devops` `ai_ml_design` `refactoring` `observability` `ux_review` `agent_design`

Every item cites its source (`[06]` = Philosophy of SW Design, `[a01]` = Building Effective Agents) so the agent can drill into the full book for context.

### 17 Claude Code Skills

Task-specific skills in `skills/` that Claude Code activates by keyword or slash command:

```
/code-review       /architecture-review   /security-audit
/test-strategy     /bug-fix               /feature-design
/api-design        /data-viz-review       /product-doc
/presentation      /devops                /ai-ml-design
/refactoring       /observability         /ux-review
/agent-design      /get-book-wisdom
```

Skills use progressive disclosure — 50 tokens of metadata at startup, 500-800 tokens of instructions when triggered, 2-20K tokens of content on-demand.

### MCP Server (5 Tools)

A Python MCP server in `mcp_server/` for universal agent access:

| Tool | Purpose |
|------|---------|
| `get_task_checklist` | Get a focused checklist by task type, with optional focus filtering and detail levels |
| `get_book_knowledge` | Deep-dive into a specific book's ideas, patterns, tradeoffs, or pitfalls |
| `list_available_knowledge` | Discover available tasks, books, and articles |
| `add_knowledge_source` | Add a new book/article (auto-assigns ID, updates indexes) |
| `update_checklist` | Modify an existing checklist (add/remove items, replace sections) |

### Test & Eval System (3 Levels)

27 evaluation fixtures in `tests/eval_fixtures/` with a 3-level test harness:

**Level 1 — Structural Integrity** (`test_level1_integrity.py`)
Validates all files exist, JSON is valid, cross-references resolve, checklists parse correctly. No LLM needed.

**Level 2 — MCP Protocol** (`test_level2_mcp_protocol.py`)
Tests the MCP server through the actual protocol layer — tool listing, schema validation, read/write tool dispatch.

**Level 3 — LLM Evaluation** (`run_llm_eval.py`, `test_level3a_eval.py`)
Sends code with seeded issues + checklists to Claude, grades whether the response identifies the issue. Computes Pass@k (capability) and Pass^k (reliability). Supports A/B comparison (with checklist vs. without).

Fixtures are tiered:

| Tier | Purpose | Example |
|------|---------|---------|
| **A** — Obvious bugs | Regression tests (8 fixtures) | SQL injection, plaintext passwords, missing timeouts |
| **B** — Structural smells | Where checklists add value (4 fixtures) | Shallow modules, information leakage, shared databases |
| **Activation** | Does the model invoke tools proactively? (4 fixtures) | Architecture review trigger, security audit trigger |
| **Qualitative** | Open-ended reasoning (3 fixtures) | Data viz quality, MCP server design |

## Project Structure

```
shudaizi/
├── knowledge/
│   ├── routing.json            # task type → book mapping
│   ├── book_index.json         # metadata for all 34 books + 21 articles
│   └── checklists/             # 16 task-specific checklists
├── skills/                     # 17 Claude Code skill definitions
├── book_research/              # 34 source documents (32 books + Anthropic blog + LLM eval)
│   └── anthropic_articles/     # 21 individual Anthropic engineering articles
├── mcp_server/                 # Python MCP server (5 tools)
│   └── src/shudaizi_mcp/
├── tests/                      # 3-level test suite + 27 eval fixtures
│   └── eval_fixtures/
├── ARCHITECTURE.md             # Full design document
└── CONTRIBUTING.md             # How to add knowledge
```

## Getting Started

### Claude Code (Skills)

Clone the repo and point Claude Code at it. Skills are auto-discovered from `skills/*/SKILL.md`. Use slash commands like `/code-review` or `/architecture-review`, or just ask naturally — "review this code" activates the code-review skill.

### MCP Server (Any Agent)

```bash
cd mcp_server
pip install -e .
```

Add to your agent's MCP config (e.g., `~/.claude/settings.json`):

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

### Running Tests

```bash
# Level 1: Structural integrity (fast, no LLM)
pytest tests/test_level1_integrity.py -v

# Level 2: MCP protocol
pytest tests/test_level2_mcp_protocol.py -v

# Level 3: LLM eval (requires ANTHROPIC_API_KEY)
python tests/run_llm_eval.py --compare    # A/B: with vs. without checklists
```

## Adding Knowledge

Ask any connected agent:

> "Add knowledge about Thinking Fast and Slow"

The agent will research the book, generate a structured markdown file, and call `add_knowledge_source` — which auto-assigns an ID, writes the file, and updates `routing.json` and `book_index.json`. All live immediately, no rebuild needed.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the manual path.

## Design Principles

- **Token efficiency** — Checklists under 6K tokens. Full books only on drill-down.
- **Zero infrastructure** — Plain markdown + JSON. No database, no embeddings, no build step.
- **Progressive disclosure** — Metadata at startup, instructions on trigger, content on demand.
- **Single source of truth** — Books are reference, checklists are delivery. Citation keys bridge them.
- **LLM-extensible** — The system can grow itself through tool calls.
