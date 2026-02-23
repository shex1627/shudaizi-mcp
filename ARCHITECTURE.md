# Shudaizi Knowledge System — Design Document

## 1. Problem Statement

When vibe-coding with AI agents (Claude Code, Cursor, Windsurf, Copilot), the LLM has no awareness of established best practices from software engineering literature. This leads to:

- **Blind spots**: Architecture plans that ignore security, resilience, or observability
- **Shallow defaults**: Generic code review that misses refactoring opportunities, testing gaps, or concurrency issues
- **Reinventing wheels**: Feature designs that don't leverage known patterns (saga, CQRS, progressive disclosure, etc.)
- **AI slop**: Data visualizations, UX, and presentations that violate foundational design principles

**We have the knowledge** — 33 curated research documents covering 32 books + 21 Anthropic engineering articles. The problem is *delivery*: getting the right subset of knowledge to the right agent at the right moment, without drowning it in tokens.

## 2. Desired Outcome

A developer says "review this architecture" or "add knowledge about Thinking Fast and Slow" to *any* coding agent, and the system:
1. Routes to the relevant subset of knowledge (not all 33 books)
2. Returns a focused, actionable checklist (~3-5K tokens, not ~500K)
3. Supports drill-down into specific books when deeper context is needed
4. Allows the LLM itself to research and add new knowledge sources

## 3. Constraints & Quality Attributes

| Attribute | Requirement | Rationale |
|-----------|------------|-----------|
| **Token efficiency** | Checklist response < 6K tokens | Context engineering: "smallest possible set of high-signal tokens" [Anthropic] |
| **Cross-platform** | Works with Claude Code, Cursor, Windsurf, Copilot | User uses multiple agents |
| **Zero infrastructure** | No database, no embedding pipeline, no running services beyond the MCP server | "Start simple, add complexity only when measured" [Building Effective Agents] |
| **LLM-extensible** | Any coding agent can add new books/articles via tool calls | User wants to say "add knowledge about X" and have it work |
| **Maintainable** | Plain markdown + JSON — human-readable, git-diffable, no build step | Long-term sustainability |
| **Progressive disclosure** | Load metadata at startup, content on-demand, deep-dive on request | "Three-tier information architecture" [Agent Skills article] |

## 4. Architecture

### 4.1 System Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Coding Agent                          │
│            (Claude Code / Cursor / Windsurf)             │
└──────────┬──────────────────────┬───────────────────────┘
           │ Skills (Claude Code)  │ MCP Protocol (universal)
           │                       │
     ┌─────▼─────┐          ┌─────▼──────────────┐
     │  skills/   │          │  MCP Server         │
     │  SKILL.md  │          │  (Python, 5 tools)  │
     │  files     │          │                     │
     └─────┬─────┘          └─────┬───────────────┘
           │                       │
           │   Both read from:     │
           │                       │
     ┌─────▼───────────────────────▼──────────────┐
     │           knowledge/ layer                   │
     │  ┌──────────────┐  ┌────────────────────┐   │
     │  │ routing.json │  │ checklists/*.md    │   │
     │  │ book_index   │  │ (16 task types)    │   │
     │  └──────────────┘  └────────────────────┘   │
     └─────────────────────┬──────────────────────┘
                           │ references
                     ┌─────▼──────────────────────┐
                     │    book_research/            │
                     │    (33 books + 21 articles)  │
                     │    Source of truth            │
                     └─────────────────────────────┘
```

### 4.2 Key Architectural Decision: Shared Knowledge Layer

**Decision**: Both skills and MCP server read from the same `knowledge/` directory. No content duplication.

**Alternatives considered**:
- Embedding checklists directly in SKILL.md bodies → violates DRY, two places to update
- MCP server generating checklists dynamically from books → unpredictable output, higher token cost
- Separate content per delivery mechanism → maintenance nightmare

**Tradeoff**: The `knowledge/` layer is a derived artifact from `book_research/`. This means two representations of the same knowledge exist (full books + curated checklists). This is intentional — the books are reference material, the checklists are the *interface* optimized for token efficiency. The citation system (`[01]`, `[06]`) bridges the two.

### 4.3 Directory Structure

```
shudaizi/
├── book_research/                  # EXISTING — source of truth
│   ├── 01_designing_data_intensive_applications.md
│   ├── ... (33 files)
│   └── anthropic_articles/         # 21 individual article files
│
├── knowledge/                      # NEW — curated delivery layer
│   ├── routing.json                # Task → book mapping + metadata
│   ├── book_index.json             # Book/article metadata registry
│   ├── checklists/                 # Task-type checklists (the core output)
│   │   ├── architecture_review.md
│   │   ├── code_review.md
│   │   ├── security_audit.md
│   │   ├── test_strategy.md
│   │   ├── bug_fix.md
│   │   ├── feature_design.md
│   │   ├── api_design.md
│   │   ├── data_viz_review.md
│   │   ├── product_doc.md
│   │   ├── presentation.md
│   │   ├── devops.md
│   │   ├── ai_ml_design.md
│   │   ├── refactoring.md
│   │   ├── observability.md
│   │   ├── ux_review.md
│   │   └── agent_design.md
│   └── scripts/
│       └── refresh_checklists.py
│
├── skills/                         # NEW — Claude Code progressive disclosure
│   ├── architecture-review/SKILL.md
│   ├── code-review/SKILL.md
│   ├── ... (16 task-type skills)
│   └── get-book-wisdom/SKILL.md    # Meta-skill: general retrieval
│
├── mcp_server/                     # NEW — universal MCP interface
│   ├── pyproject.toml
│   ├── README.md
│   └── src/shudaizi_mcp/
│       ├── __init__.py
│       ├── server.py               # MCP entry point
│       ├── routing.py              # Task routing + filtering
│       ├── book_loader.py          # Markdown section parser
│       ├── knowledge_manager.py    # Add/update knowledge (write ops)
│       └── tools.py                # 5 tool definitions
│
└── CONTRIBUTING.md                 # How to add knowledge (for humans)
```

## 5. MCP Server Design

### 5.1 Tool Inventory (5 tools)

Following "fewer, more purposeful tools" [Writing Effective Tools] — one tool per *intent*, not per task type.

#### Read Tools (knowledge retrieval)

| Tool | Purpose | Params | Response Size |
|------|---------|--------|---------------|
| `get_task_checklist` | Primary interface — returns curated checklist for a task type | `task_type` (enum), `focus` (optional filter), `detail_level` (brief/standard/detailed) | 1-6K tokens |
| `get_book_knowledge` | Deep-dive — returns a specific section from a book/article | `book_id` (e.g. "01", "a05"), `section` (key_ideas/patterns/tradeoffs/pitfalls/framings/full) | 2-5K tokens |
| `list_available_knowledge` | Discovery — what's in the knowledge base | `category` (all/tasks/books/articles) | ~2K tokens |

#### Write Tools (LLM-driven knowledge management)

| Tool | Purpose | Params | What It Does |
|------|---------|--------|-------------|
| `add_knowledge_source` | Add a new book/article to the knowledge base | `title`, `type` (book/article/blog), `content` (full research markdown), `category`, `task_types` (list of relevant task slugs) | Auto-assigns ID, writes file, updates book_index.json, updates routing.json |
| `update_checklist` | Modify a task checklist | `task_type`, `action` (add_items/remove_items/replace_section), `section`, `content` | Reads checklist, applies change, bumps version, writes back |

### 5.2 Interaction Patterns

**Pattern A: Task-anchored review** (most common)
```
User: "Review this architecture for security and scalability"
Agent → get_task_checklist(task_type="architecture_review", focus="security,scalability")
Agent ← 3K token checklist with cited items
Agent → [optional] get_book_knowledge(book_id="07", section="patterns")  # deep-dive on security
```

**Pattern B: Adding knowledge**
```
User: "Add knowledge about Thinking Fast and Slow"
Agent → [web search + research]
Agent → add_knowledge_source(title="Thinking Fast and Slow", type="book", content=<md>, category="Psychology", task_types=["feature_design", "ux_review", "product_doc"])
Agent → update_checklist(task_type="feature_design", action="add_items", section="Cognitive Biases", content="- [ ] Check for anchoring bias in default values [34]\n...")
```

**Pattern C: Exploratory**
```
User: "What does DDIA say about consistency models?"
Agent → get_book_knowledge(book_id="01", section="key_ideas")
```

### 5.3 Convention-Based Auto-Discovery

The server scans the filesystem at startup — no hardcoded lists:
- Task types = filenames in `knowledge/checklists/*.md`
- Books = files matching `book_research/[0-9]*.md`
- Articles = files in `book_research/anthropic_articles/[0-9]*.md`

This means **dropping a file into the right directory makes it available immediately**, even before updating routing.json. The routing just determines which *checklists* reference it.

## 6. Skills Design

### 6.1 Progressive Disclosure (3 levels)

| Level | What Loads | When | Token Cost |
|-------|-----------|------|------------|
| L1: Metadata | YAML frontmatter (name + description) | Claude Code startup | ~50 tokens/skill, ~850 total |
| L2: Instructions | SKILL.md body (procedure, principles, file refs) | When skill is triggered | ~500-800 tokens |
| L3: Content | Checklist files + book research files | On-demand filesystem reads | 2-20K tokens (progressive) |

### 6.2 Skill Template

```yaml
---
name: architecture-review
description: >
  Architecture review using DDIA, Clean Architecture, Microservices, Philosophy of SW Design,
  and 6 more books. Use when reviewing system design, evaluating ADRs, or assessing tradeoffs.
---

## When to Activate
- User asks to review/critique a system architecture
- User presents a design document or ADR
- User asks about architectural tradeoffs

## Procedure
1. Read `knowledge/checklists/architecture_review.md`
2. Assess the system against each checklist phase
3. For items needing deeper context, read the cited book file (e.g., `book_research/01_...md`)
4. Present findings as: Strengths → Concerns → Recommendations
5. Cite source book/principle for each finding

## Always-Apply Principles
- Every architecture choice is a tradeoff — name both sides [01]
- Complexity must justify itself — "what is this buying us?" [06]
- Dependencies point inward toward domain logic [04]
- "What happens if this component fails?" is the first question [17]

## Deep-Dive References
- Data systems: book_research/01_designing_data_intensive_applications.md
- Architecture styles: book_research/02_fundamentals_of_software_architecture.md
- Decomposition: book_research/03_software_architecture_hard_parts.md
- Dependency rules: book_research/04_clean_architecture.md
- Service boundaries: book_research/05_building_microservices.md
- Complexity: book_research/06_philosophy_of_software_design.md
```

### 6.3 Meta-Skill: `get-book-wisdom`

A general-purpose skill for when the user's task doesn't match a specific task type:

```yaml
---
name: get-book-wisdom
description: >
  Retrieve knowledge from the 33-book + 21-article research library.
  Use for any software engineering topic: principles, patterns, checklists, or tradeoffs.
---
```

Instructs Claude to check `knowledge/routing.json`, read the right checklist, and drill into books as needed.

## 7. Checklist File Format

```markdown
---
task: architecture_review
description: Review system architecture for soundness, tradeoffs, and maintainability
primary_sources: ["01", "02", "03", "04", "05", "06"]
secondary_sources: ["17", "19", "20", "21", "32"]
version: 1
updated: 2026-02-22
---

# Architecture Review Checklist

## Phase 1: Structural Assessment
- [ ] Identify the architectural style (monolith, microservices, modular monolith, event-driven) [02, 03]
- [ ] Check component coupling: abstractions or concrete implementations? [04, 06]
- [ ] Evaluate dependency direction: do dependencies point inward? [04]
- [ ] Assess module depth: are modules deep (simple interface, complex implementation)? [06]
- [ ] Check for appropriate service boundaries aligned with bounded contexts [05, 03]

## Phase 2: Data Architecture
- [ ] Verify data model matches access patterns [01]
- [ ] Assess consistency requirements per data path (strong, causal, eventual) [01]
- [ ] Check for single points of data loss [01, 17]

## Phase 3: Resilience & Operations
- [ ] Identify single points of failure [17]
- [ ] Check for bulkheads and circuit breakers at service boundaries [17, 05]
- [ ] Assess observability: structured logs, distributed tracing, metrics [18]
- [ ] Evaluate deployment strategy and rollback capability [32, 19]

## Phase 4: Security
- [ ] Map trust boundaries [07]
- [ ] Verify input validation at all system boundaries [07]
- [ ] Check authentication and authorization model [07]
- [ ] Assess LLM-specific risks if applicable (prompt injection, data leakage) [08]

## Key Questions to Ask
> "What is the cost of stale or inconsistent data in this use case?" [01]
> "What happens if this component is slow for 30 seconds?" [17]
> "Is this complexity buying us something, or is it accidental?" [06]
> "Can this be a monolith first?" [05]

## Anti-Patterns to Flag
- God service that does too much [02, 04, 06]
- Distributed monolith: microservices with synchronous call chains [03, 05]
- Shared database across services without clear ownership [03]
- Architecture by hype: choosing tech without matching it to requirements [02]
```

Citations (`[01]`, `[06]`) are the routing keys for drill-down via `get_book_knowledge`.

## 8. Task → Source Routing

| Task Type | Primary Sources | Secondary | Anthropic Articles |
|-----------|----------------|-----------|-------------------|
| `architecture_review` | 01, 02, 03, 04, 05, 06 | 17, 19, 20, 21, 32 | a01, a05 |
| `code_review` | 06, 14, 15, 16 | 04, 12, 13, 22 | a05, a20 |
| `security_audit` | 07, 08 | 01, 17, 20 | a14 |
| `test_strategy` | 12, 13 | 06, 14, 16 | a11, a13 |
| `bug_fix` | 16, 14, 17 | 01, 06, 12, 18 | a09, a15 |
| `feature_design` | 06, 29, 30, 31 | 02, 03, 04, 23-25 | a01 |
| `api_design` | 20 | 01, 04, 05, 06 | a06, a07 |
| `data_viz_review` | 26, 27, 28 | 23, 24, 25 | — |
| `product_doc` | 29, 30, 31 | 23, 24, 26 | — |
| `presentation` | 26 | 23-25, 27, 28 | — |
| `devops` | 32, 17, 19 | 18, 01 | a14, a04 |
| `ai_ml_design` | 09, 10, 11 | 01, 08 | a01-a10 |
| `refactoring` | 16, 06, 15 | 04, 12, 14 | — |
| `observability` | 18, 17, 19 | 32, 01 | a12, a15 |
| `ux_review` | 23, 24, 25 | 26, 29 | — |
| `agent_design` | 33 + articles | 09, 11 | a01-a10 |

## 9. Extensibility

### LLM-Driven (Primary Path)

Any coding agent can expand the knowledge base:

1. User says "add knowledge about X"
2. Agent researches the topic (web search)
3. Agent generates research markdown following the template in `book_research_prompts.md`
4. Agent calls `add_knowledge_source(...)` → file created, indexes updated automatically
5. Agent optionally calls `update_checklist(...)` → adds relevant items to affected task checklists

The `add_knowledge_source` tool handles all plumbing:
- Auto-assigns next sequential ID
- Writes file with correct naming convention
- Updates `book_index.json` with metadata
- Updates `routing.json` to include new source in specified task types

### Manual Path (Fallback)

1. Add markdown file to `book_research/` following the template
2. Add entry to `knowledge/book_index.json`
3. Update `routing.json` task mappings
4. Update relevant checklists

### Auto-Discovery

Even without updating any indexes, a new file in `book_research/` is immediately accessible via `get_book_knowledge` because the server scans the filesystem. The indexes just determine which *checklists* reference it.

## 10. Staleness Management

| Mechanism | How It Works |
|-----------|-------------|
| Version tracking | Each checklist has `version` + `updated` in frontmatter |
| Timestamp comparison | `refresh_checklists.py` compares book file mtime vs. checklist mtime |
| Warnings | Script alerts when source material is newer than derived checklists |
| LLM refresh | Ask any agent "refresh the architecture review checklist" → it re-reads sources and updates |

## 11. Risks & Rabbit Holes

| Risk | Mitigation |
|------|-----------|
| Checklists become stale as books are updated | Staleness detection script + version tracking |
| Checklist quality varies (some too thin, some too verbose) | Start with 3 high-quality exemplars, use them as templates |
| `add_knowledge_source` produces inconsistent markdown | Validate against template structure; include template in tool description |
| Token budget exceeded for large checklists | `detail_level` parameter; default to "standard" (~3-5K tokens) |
| Agents don't discover/use the tools naturally | Good tool descriptions; skills trigger on keywords in Claude Code |
| Write tools used incorrectly (corrupting indexes) | JSON schema validation in `knowledge_manager.py`; atomic writes |

### Out of Scope (for now)
- Semantic search / vector embeddings (Phase 2 — add when task-based routing proves insufficient)
- Automatic checklist generation from books (manual curation gives higher quality)
- Multi-language MCP server (Python only)
- CI/CD pipeline for the knowledge base

## 12. Build Phases

### Phase 1: Foundation (~files only, no code)
- Save this design document as `ARCHITECTURE.md` at the project root
- Create `knowledge/` directory structure
- Write `routing.json` with full task → book mapping
- Write `book_index.json` with all 33 books + 21 articles metadata
- Write 3 exemplar checklists: `architecture_review.md`, `code_review.md`, `security_audit.md`

### Phase 2: Claude Code Skills
- Create `get-book-wisdom` meta-skill
- Create SKILL.md for the 3 initial task types
- Test with Claude Code: verify progressive disclosure, checklist loading, drill-down

### Phase 3: Remaining Checklists + Skills
- Write remaining 13 checklist files (using Phase 1 exemplars as templates)
- Create corresponding SKILL.md files (16 total)

### Phase 4: MCP Server — Read Tools
- Set up Python project (`pyproject.toml` with `mcp` SDK)
- Implement `book_loader.py` (markdown section parser)
- Implement `routing.py` (reads routing.json, filtering/focus logic)
- Implement 3 read tools in `tools.py`
- Wire up `server.py`
- Test with Claude Code as MCP client

### Phase 5: MCP Server — Write Tools
- Implement `knowledge_manager.py` (file creation, index updates, validation)
- Implement 2 write tools in `tools.py`
- Test: "add knowledge about Thinking Fast and Slow" → verify file + indexes + routing

### Phase 6: Polish
- Write `CONTRIBUTING.md`
- Staleness detection script (`refresh_checklists.py`)
- README for MCP server with config examples for Claude Code, Cursor, Windsurf

## 13. Verification

| Test | What to Verify | Pass Criteria |
|------|---------------|---------------|
| Skills: trigger | Ask Claude Code "review this architecture" | Correct skill loads, checklist returned |
| Skills: drill-down | Follow a `[01]` citation | Correct book section loaded |
| MCP: read tools | Call all 3 read tools via MCP inspector | Correct responses, < 6K tokens |
| MCP: write tools | "Add knowledge about X" workflow | File created, indexes updated, no corruption |
| MCP: auto-discovery | Drop a new .md file, query it | File accessible without config changes |
| Cross-agent | Configure in Cursor/Windsurf | Tools visible and functional |
| Token budget | Measure response sizes | standard ≤ 6K, brief ≤ 3K |

## 14. Key Files

| File | Purpose |
|------|---------|
| `book_research_prompts.md` | Template for new book research — referenced by `add_knowledge_source` |
| `book_research/*.md` (33 files) | Source of truth — knowledge content |
| `book_research/anthropic_articles/*.md` (21 files) | Anthropic article content |
| `knowledge/routing.json` | Task → book mapping (shared by skills + MCP) |
| `knowledge/book_index.json` | Book/article metadata registry |
| `knowledge/checklists/*.md` (16 files) | Curated task checklists (the primary output) |
| `skills/*/SKILL.md` (17 files) | Claude Code progressive disclosure |
| `mcp_server/src/shudaizi_mcp/server.py` | MCP entry point |
| `mcp_server/src/shudaizi_mcp/tools.py` | 5 tool definitions |
| `mcp_server/src/shudaizi_mcp/knowledge_manager.py` | Write operations (add source, update checklist) |
