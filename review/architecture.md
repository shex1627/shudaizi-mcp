# Architecture Review

**Frameworks applied:** [01] DDIA, [02] Fundamentals of Software Architecture, [03] Software Architecture: The Hard Parts, [04] Clean Architecture, [06] Philosophy of Software Design, [36] DDD, [38] Enterprise Integration Patterns
**Checklist source:** knowledge/checklists/architecture_review.md
**Verdict: Strong** — Deliberately simple with sound structure. A few gaps in dependency direction and the knowledge mutation path worth addressing.

---

## System Overview

Shudaizi is a read-mostly knowledge retrieval system with a narrow write path for knowledge management. The system has two delivery interfaces (Claude Code skills, MCP server) sharing one knowledge layer (markdown files + JSON indexes). No database, no remote state, no network dependencies beyond the MCP protocol connection from the client agent.

```
┌─────────────────────────────────────────────────────────┐
│                    Coding Agent                          │
│            (Claude Code / Cursor / Windsurf)             │
└──────────┬──────────────────────┬───────────────────────┘
           │ Skills (Claude Code)  │ MCP Protocol
           │                       │
     ┌─────▼─────┐          ┌─────▼──────────────┐
     │  skills/   │          │  MCP Server         │
     │  SKILL.md  │          │  (Python, 5 tools)  │
     └─────┬─────┘          └─────┬───────────────┘
           │                       │
     ┌─────▼───────────────────────▼──────────────┐
     │           knowledge/ layer                   │
     │  routing.json  |  book_index.json            │
     │  checklists/*.md                             │
     └─────────────────────┬──────────────────────┘
                           │ references
                     ┌─────▼──────────────────────┐
                     │    book_research/*.md        │
                     │    (source of truth)         │
                     └─────────────────────────────┘
```

---

## Phase 1: Structural Assessment

**Architecture style:** Flat file system + stdio protocol adapter. Correct for the scale and requirements. [02]

**What works well:**

- **Module depth is appropriate.** `BookLoader`, `TaskRouter`, and `KnowledgeManager` each have simple interfaces that hide real complexity (regex-based markdown parsing, JSON mutation, filesystem glob resolution). This is "deep module" design in the Philosophy of Software Design sense [06]. ✓
- **The shared knowledge layer is a correct architectural decision.** Both delivery interfaces (skills, MCP) read from the same `knowledge/` directory. This avoids the DRY violation of maintaining two content sets. ✓
- **Convention-based discovery is clean.** The server scans `book_research/[0-9]*.md` at startup rather than maintaining a separate list. A new file dropped in the directory is immediately available. This is a well-bounded "open for extension" design. ✓
- **Dependency direction is correct for read tools.** `server.py` → `tools.py` → `{BookLoader, TaskRouter}` → filesystem. Higher-level modules depend on abstractions; the filesystem is at the bottom. ✓

**Concerns:**

- **Information leakage between `BookLoader` and `KnowledgeManager`.** Both classes independently compute `book_research_dir` and `checklists_dir` from `project_root`. There is no shared path configuration. If the directory structure changes, both must be updated in sync. This is a mild duplication but creates coupling risk. [06]

- **`PROJECT_ROOT` is resolved by path count, not by an explicit marker.** `server.py:14`: `Path(__file__).resolve().parent.parent.parent.parent`. This is fragile — if the package is installed in a different structure (e.g., editable install with different nesting), `PROJECT_ROOT` will be wrong and all file operations will silently fail. [06]

- **The `routing.py` / `book_loader.py` split is conceptually awkward.** `TaskRouter` formats human-readable lists (it knows about UI formatting) and also handles routing logic. `BookLoader` handles file I/O and also implements detail-level filtering logic. Neither is quite a "deep module" — they're mixing retrieval concerns with presentation concerns. Consider: `Router` for routing decisions, `Formatter` for output formatting, `Loader` for file I/O. [06]

- **Write tools mutate shared mutable state (JSON files) without locks.** Two simultaneous `add_knowledge_source` calls could race on `book_index.json`. Not a concern at current scale (single developer, stdio transport), but worth noting for HTTP/multi-client use. [03]

---

## Phase 2: Data Architecture

**Data model assessment:**

The system has three data tiers:

| Tier | Format | Role | Mutable? |
|------|--------|------|----------|
| `book_research/*.md` | Markdown | Source of truth — full knowledge content | Via LLM write tools |
| `knowledge/*.json` | JSON | Indexes — metadata and routing | Via LLM write tools |
| `knowledge/checklists/*.md` | Markdown | Derived layer — delivery-optimized summaries | Via LLM write tools |

**What works well:**
- The three-tier structure is correctly designed: source → index → derived. [01]
- JSON indexes are the right choice: lightweight, human-readable, git-diffable, no schema migration. ✓
- Checklists are correctly identified as *derived* artifacts with version tracking and a staleness detection script. This prevents the common anti-pattern of letting derived data silently drift from its source. ✓

**Concerns:**

- **The `checklists/` layer is partially stale.** Six books (35-40) were added in the most recent session. No `update_checklist` calls have been made for any of them. The checklists are derived from the source books — but the derivation step has not been performed. This is the most critical data quality issue in the current system.

  Affected checklists: `feature_design`, `product_doc`, `presentation`, `architecture_review`, `security_audit`, `api_design`, `ai_ml_design`, `ux_review`, `observability`. The new books have relevant knowledge for all of these.

- **`routing.json` has drifted from `ARCHITECTURE.md` section 8.** The architecture doc shows the original source mapping (without books 36-40). The routing.json has been updated, but the ARCHITECTURE.md table has not. Documentation drift [06].

- **No schema validation for `book_index.json` or `routing.json`.** The `KnowledgeManager` reads and writes these files but does not validate their structure against a schema. A malformed `add_knowledge_source` call that produces a non-integer year, or a `task_types` array with invalid slugs, will silently corrupt the index. [01]

---

## Phase 3: Resilience & Operations

**This is a local file system tool, not a distributed system.** Most distributed resilience concerns (timeouts, circuit breakers, bulkheads) do not apply. The relevant resilience concerns are:

**What works well:**
- The MCP server has no external dependencies during read operations — it only reads from the local filesystem. This means reads are fast and never subject to network timeouts. ✓
- The `list_available_knowledge` tool calls `router.reload()` to refresh from disk before responding. This ensures stale in-memory state does not produce incorrect results after a knowledge update. ✓

**Concerns:**

- **No error boundary around filesystem reads.** `BookLoader.read_book_section` returns the string `"Book 'XX' not found."` as normal text output rather than raising an MCP error. The agent calling the tool has no way to distinguish a successful empty response from a failure. [17]

- **Write tools have no atomicity.** `KnowledgeManager.add_knowledge_source` does three separate file operations: write the content file, update `book_index.json`, update `routing.json`. If the process crashes after step 1, the knowledge base is in a partial state: the file exists but is not indexed. There is no rollback or cleanup mechanism. For a local dev tool, this is acceptable; for multi-user, it is not. [17]

- **`KnowledgeManager._save_json` overwrites the file in-place without a temp file + rename.** If the write is interrupted (crash, disk full), the JSON file is corrupted and unreadable. A write-to-temp-then-rename pattern is safer. [17]

---

## Phase 4: Security

*(See dedicated [security.md](security.md) review for full analysis.)*

**Summary of architectural security concerns:**
- The write tools perform filesystem writes to paths derived from user-provided strings. No path traversal protection exists.
- `_slugify` strips most special characters but does not guarantee the resulting path is within `book_research/`.
- The MCP server has no authentication — any MCP client can call write tools.

---

## Phase 5: Scalability & Evolution

**Current scale:** Single developer, local filesystem, one agent at a time. No scalability concerns at this scale.

**Architectural evolution path:**

The ARCHITECTURE.md correctly identifies the planned evolution:
- Phase 1: File system only (done)
- Phase 2: Claude Code skills (done)
- Phase 3: Remaining checklists + skills (done)
- Phase 4: MCP server read tools (done)
- Phase 5: MCP server write tools (done)
- Phase 6: Polish (largely done)

**What the architecture handles well for future growth:**
- Adding new books: the `add_knowledge_source` tool + convention-based discovery makes this O(1) effort
- Adding new task types: add a checklist file + routing entry; no server code changes needed
- Multi-agent use: the knowledge layer is read-only for most operations; read parallelism is safe
- HTTP transport: the `main_http` entry point using `StreamableHTTPSessionManager` is already implemented

**What would need redesign for larger scale:**
- Multi-user write access would need locking or a proper data store
- Semantic search (Phase 2) would add an embedding pipeline dependency
- A hosted/SaaS version would need authentication, rate limiting, and usage tracking

**ADRs are missing.** The architectural decisions (plain files vs. database, markdown vs. structured format, shared knowledge layer, stdio vs. HTTP) are well-reasoned but are captured in ARCHITECTURE.md prose, not as structured ADRs. Structured ADRs make it easier to revisit and update decisions as the system evolves. [02][03]

---

## Phase 6: Maintainability & Design Quality

**What works well:**

- **Module size is appropriate.** No single file is over 280 lines. Each module has a clear responsibility. [06]
- **`extract_standard` vs. `extract_items_only` vs. full content** correctly implements the detail_level hierarchy. The three levels map cleanly to the progressive disclosure architecture. ✓
- **`_add_items_to_section` implements a careful state machine** for section detection and insertion. The logic handles all edge cases (section at end of file, section not found, consecutive sections) with explicit conditions. [06]

**Concerns:**

- **`SECTION_PATTERNS` regex in `book_loader.py` is fragile.** The section extractor uses keyword-matching regexes against markdown headings to identify sections. The patterns cover common cases well, but any book research file with a non-standard heading will silently return "Section not found." The patterns were grown incrementally and mix specific phrases with generic wildcards (`"What "`, `"Note\b"`). There is no test for new book formats against these patterns.

- **`parse_frontmatter` implements custom YAML parsing.** The comment "no external dependency needed" explains the decision, but the implementation is brittle: it does not handle multi-line values, lists of objects, or unquoted values with colons. The `routing.json` uses JSON arrays for source lists (correct), but if any checklist frontmatter ever uses a more complex YAML structure, this parser will silently misparse it. [06]

- **`extract_standard` skips sections matching a regex for anti-patterns.** The logic (`in_antipatterns` flag) is correct but subtle: once the "Anti-Pattern" section heading is detected, all following content is skipped until the next heading. If a checklist has no subsequent heading after "Anti-Patterns to Flag", all content after it is correctly included. But the flag name `in_antipatterns` combined with the logic "stop skipping when next heading found" is semantically backwards — it reads as if we're including anti-pattern content, not excluding it. A comment or renamed variable would help.

---

## DDD Assessment [36]

The shudaizi system has a clear domain model, even though it is not structured as a formal DDD application:

**Implicit bounded context: Knowledge Management**
- Core domain: The curated knowledge content (book_research files)
- Supporting domain: The delivery machinery (checklists, skills, MCP server)
- Generic domain: File I/O, JSON parsing, MCP protocol

**Entities vs. Value Objects:**
- A `Book` (identified by its `book_id`) is an entity — it has identity and lifecycle
- A `ChecklistItem` is a value object — no identity, immutable, only matters for its content
- A `TaskType` (routing slug) is a value object — naming the concept that bridges books to tasks

**What's missing:** The domain model is purely implicit. The Python code has no domain classes — `BookLoader`, `TaskRouter`, and `KnowledgeManager` are service-layer classes with no domain model beneath them. For a tool of this complexity, this is acceptable. But a `Book`, `Checklist`, and `KnowledgeSource` domain class hierarchy would make the write operations safer (validation at the domain level, not in the tool handler).

---

## Enterprise Integration Patterns Assessment [38]

The MCP protocol itself is a message-passing system. Through that lens:

- The `get_task_checklist` tool is a **Request-Reply** pattern: agent sends a tool call message, server returns content. ✓
- The `add_knowledge_source` tool is a **Command Message**: it changes state rather than querying it. Correctly implemented as a separate tool. ✓
- The `list_available_knowledge` tool calling `router.reload()` is a form of **Polling Consumer**: the server re-reads from the filesystem on each request to ensure fresh state. Correct for this use case. ✓

**Concern:** There is no **Dead Letter** handling equivalent. If a tool call arrives with invalid parameters, the server returns a text error message embedded in a normal `TextContent` response. There is no MCP-level error signaling. The agent cannot programmatically distinguish success from failure.

---

## Summary Table

| Dimension | Status | Priority |
|-----------|--------|----------|
| Module depth and interfaces | ✓ Good | — |
| Shared knowledge layer | ✓ Good | — |
| Convention-based discovery | ✓ Good | — |
| PROJECT_ROOT resolution | ⚠ Fragile | Medium |
| Path configuration duplication | ⚠ Minor | Low |
| Checklist staleness (books 35-40) | ✗ Gap | **High** |
| JSON schema validation on write | ⚠ Missing | Medium |
| Atomic writes for JSON files | ⚠ Missing | Medium |
| Error distinction (success vs failure) | ⚠ Missing | Medium |
| Routing.py concern mixing | ⚠ Minor | Low |
| ADR documentation | ⚠ Missing | Low |
