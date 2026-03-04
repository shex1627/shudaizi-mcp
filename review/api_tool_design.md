# API & Tool Design Review

**Frameworks applied:** [20] API Design Patterns, [24] Don't Make Me Think (developer UX lens), [40] Working Backwards, [a06] Claude Tools Best Practices, [a07] Tool Use Best Practices
**Checklist source:** knowledge/checklists/api_design.md
**Verdict: Strong** — 5 tools with clear intent separation, good input schemas, and proactive usage guidance. Two discoverability gaps and one routing limitation worth addressing.

---

## Working Backwards from the API Consumer [40]

Before evaluating the API mechanically, frame the evaluation from the perspective of the consumer: an AI coding agent (Claude Code, Cursor, or any MCP-compatible tool) that must decide when to call which tool and with what arguments.

**The agent's journey:**
1. The agent is activated by a user request ("review this architecture")
2. The agent must recognize that Shudaizi tools are relevant
3. The agent must pick the correct tool (`get_task_checklist` vs. `get_book_knowledge`)
4. The agent must supply valid parameters (`task_type` must be a valid slug)
5. The agent must decide whether to drill down further (`get_book_knowledge` after reading a citation)
6. The agent must decide when to write (`add_knowledge_source`) vs. just use existing knowledge

The API is good if an agent can complete this journey with minimal ambiguity at each step. Apply this lens to each finding below.

---

## Tool Inventory Assessment

### Tool 1: `get_task_checklist` ✓ Well-designed

**Description quality:** Strong. The description includes an explicit `IMPORTANT: Call this tool proactively in these situations:` block with concrete trigger conditions. This is the correct pattern for guiding agent behavior — it teaches the agent *when* to use the tool, not just *what* the tool does. [a06]

**Schema quality:**
- `task_type`: required, string with available values in the description. Good. Could be an `enum` to enable schema validation.
- `focus`: optional comma-separated string for sub-topic filtering. Good for token efficiency. The implementation (`filter_by_focus`) works by section heading matching — this is documented only in the description as "narrow to specific sub-topics (comma-separated)." An agent that doesn't understand this may pass `focus="sql injection"` and get a fallback full response with a note. The fallback message is clear.
- `detail_level`: optional enum `["brief", "standard", "detailed"]`. Well-documented with token estimates. This is the right abstraction — the agent can control the trade-off between token cost and detail.

**What the agent gets back:** The full checklist content, filtered by detail level. No metadata about which books were used, no indication of checklist version. The agent cannot tell if the checklist is stale without checking the frontmatter.

**Concern:** The `task_type` parameter accepts any string; the server returns an error string (`"Checklist 'X' not found"`) in a normal `TextContent` response. The agent cannot distinguish a correct empty response from a "task_type not found" failure without string-matching the error. A proper MCP error response would be cleaner. [20]

---

### Tool 2: `get_book_knowledge` ✓ Well-designed

**Description quality:** Good. The trigger condition is clear: "Use when you need deeper understanding of a principle cited in a checklist (e.g., [01] → book 01)." The citation system is the linking mechanism, and the description makes this explicit.

**Schema quality:**
- `book_id`: required. The description correctly points to `list_available_knowledge` for ID discovery. Good.
- `section`: optional enum `["key_ideas", "patterns", "tradeoffs", "pitfalls", "framings", "applicability", "full"]`. The enum values are well-chosen for the book research file structure. The `"full"` option (returning the entire file) is correctly noted as "use sparingly."

**Concern:** The section enum is fixed to the section types defined in `SECTION_PATTERNS`. If a book file has a custom section heading that does not match any pattern, the section request returns a fallback error string embedded in a normal text response. The agent has no way to know what sections are actually available in a given book — `list_available_knowledge` does not expose this. A `list_book_sections(book_id)` capability (or including section availability in the book list output) would close this gap. [20]

**Concern:** The description says "Returns the requested section for deep-dive context" but does not tell the agent how long the response will be. Token budget uncertainty may cause agents to hesitate before calling `full`. The `2-5K tokens` estimate in the description is good; it could be more precise by including the `"full"` case estimate.

---

### Tool 3: `list_available_knowledge` ✓ Good

**Description quality:** Adequate. "Use this to discover what's available before requesting specifics" is the right guidance.

**Schema quality:**
- `category`: optional enum `["all", "tasks", "books", "articles"]`. Well-designed for incremental discovery.

**Output quality:** The formatted output from `format_task_list()`, `format_book_list()`, `format_article_list()` is readable markdown. The task list includes the primary sources for each task type, which is useful for an agent deciding whether to use a task checklist or go direct to a book.

**Concern:** The book list output includes only `[id] Title — Author (Year)`. It does not include the category, which means an agent trying to find books on "security" must read all 40 entries and infer from titles. Adding category would improve discoverability. [24]

**Concern:** The article list sorts by `aid` (alphanumeric). Since articles are named `a01` through `a21`, this is chronological — but the agent has no way to know that. Including the date in the article list (which `format_article_list` already does: `({info.get('date', '?')})`) is correct. ✓

---

### Tool 4: `add_knowledge_source` ⚠ Functional but with routing limitation

**Description quality:** Good. The description points to `book_research_prompts.md` as the template, which is the correct behavior — a caller that doesn't use the template will produce non-standard files. The description could be stronger about what "following the standard template" means in terms of required sections.

**Schema quality:**
- `title`, `source_type`, `content`, `category`, `task_types`: required. Clear.
- `author`, `year`: optional. Appropriate.
- `task_types`: accepts an array of task type slugs. The tool routes the new source into `secondary_sources` only, regardless of its actual importance.

**Critical routing limitation:** `knowledge_manager.py:132-138`:
```python
source_key = "anthropic_articles" if is_article else "secondary_sources"
if source_id not in task_info.get(source_key, []):
    task_info[source_key].append(source_id)
```

Every book added via `add_knowledge_source` is placed in `secondary_sources`, never `primary_sources`. This means that regardless of how important a book is, it can never become a primary source through the tool — it requires manual JSON editing. The six books added in this session (35-40) were added manually and correctly assigned to primary_sources where appropriate. If they had been added via the tool, they would only be secondary sources.

**Recommendation:** Add a `primary_task_types` parameter (list of task types where this source should be primary) alongside `task_types` (which becomes the secondary list). Or rename `task_types` to `secondary_task_types` and add `primary_task_types`. [20]

**No return of the generated book_id in a structured way.** The response is a string: `"Added 'X' as 41. File: ..."`. An agent cannot programmatically extract the new ID to pass to `get_book_knowledge` — it must parse the string. A structured response `{id: "41", file_path: "...", tasks_updated: [...]}` would be cleaner. [20]

---

### Tool 5: `update_checklist` ✓ Well-designed

**Description quality:** Good. The action enum (`add_items`, `remove_items`, `replace_section`) is the correct abstraction — three distinct operations on checklist content.

**Schema quality:**
- `task_type`, `action`, `section`, `content`: all required. Clear.
- The `section` parameter note ("creates section if it doesn't exist" for `add_items`) is correctly documented.
- The `content` format hint ("Each item should cite its source: `- [ ] Item description [XX]`") is excellent — it teaches the caller the correct format. ✓

**Concern:** `remove_items` uses substring matching (`any(p in line for p in patterns)`). This means a remove pattern of "authentication" would remove any checklist line containing the word "authentication" — including lines from other sections. No section scoping for removal. [20]

---

## Cross-Tool Consistency Assessment [20]

**Naming convention:** Snake case throughout. ✓ Consistent.

**Error signaling:** All errors (book not found, checklist not found, unknown tool) are returned as normal `TextContent` string responses. The MCP protocol supports structured error responses (`McpError`), which would allow callers to programmatically distinguish error states. All 5 tools should use proper error codes for the "not found" and "invalid parameter" cases. [20]

**Parameter naming consistency:**
- `task_type` is used consistently across all task-related tools. ✓
- `book_id` is used in `get_book_knowledge`. ✓
- `source_type` is used in `add_knowledge_source` (not `book_type` or `content_type`). Acceptable but slightly inconsistent with the naming convention if "source" maps to "book" in other contexts.

**Tool count:** 5 tools is appropriate for the scope. The Anthropic guidance on tool design [a06] advises "fewer, more purposeful tools." The tool set has no redundancy — each tool has a distinct intent and a distinct user. ✓

---

## Progressive Disclosure Assessment [a05]

The 3-level token efficiency design is well-implemented:
- L1 (startup): ~50 tokens per skill, ~850 total for all skills
- L2 (trigger): ~500-800 tokens when a skill activates
- L3 (content): 1-10K tokens for checklist or book section on demand

The `detail_level` parameter on `get_task_checklist` (brief/standard/detailed) is the correct mechanism for managing L3 token cost. The three levels are well-calibrated:
- `brief` → checklist items only, stripped of context (~1-3K)
- `standard` → items + key questions, excluding anti-patterns section (~3-6K)
- `detailed` → full content including anti-patterns (~5-10K)

**Concern:** The `extract_standard` implementation skips the Anti-Patterns section specifically. But Anti-Patterns are often the most useful content for a practical reviewer — they're concrete and actionable. The decision to exclude them from `standard` mode may be reducing the value of the default response. Consider making `standard` include anti-patterns and defining `brief` as items-only.

---

## Tool Description Quality (Anthropic Tool Design Principles) [a06]

Evaluated against the key principles:

| Principle | Assessment |
|-----------|-----------|
| Tools have a clear, singular purpose | ✓ Each tool has one intent |
| Tool names are self-describing | ✓ `get_task_checklist`, `get_book_knowledge`, etc. |
| Parameters include sufficient context | ✓ Descriptions include format guidance and examples |
| The agent knows WHEN to call each tool | ✓ `get_task_checklist` includes explicit proactive trigger conditions |
| Tools are minimal — no overlap in capability | ✓ No redundant tools |
| Response sizes are bounded | ⚠ `get_book_knowledge(section="full")` is unbounded |
| Errors are clearly communicated | ⚠ Errors embedded in text, not MCP error protocol |

---

## Developer Experience Assessment [24]

Don't Make Me Think applied to the agent-as-user:

**What an agent should never have to figure out:**

1. **Which tool to call first** — The `get_task_checklist` IMPORTANT block handles this correctly. An agent reading the tool list knows to start here. ✓
2. **What task_type string to use** — The description lists all 16 task types. The agent can match "review this architecture" → "architecture_review" without ambiguity. ✓
3. **How to drill into a book** — The citation format `[01]` in checklist items maps to `book_id="01"` in `get_book_knowledge`. The description makes this explicit. ✓
4. **Whether a book_id is valid** — The agent must call `list_available_knowledge` or know the ID from a citation. There is no inline validation. ⚠

**What an agent sometimes has to figure out:**
- The difference between primary and secondary sources (routing.json is not exposed to agents)
- Whether a specific focus keyword will match any sections (trial-and-error with the fallback)
- What sections are available in a specific book (no discovery mechanism)

---

## Summary and Recommendations

**Strengths:**
- Tool set is correctly scoped (5 tools, no redundancy)
- Progressive disclosure is well-implemented across all three levels
- Proactive trigger conditions in `get_task_checklist` description are excellent
- The detail_level parameter is the right token management mechanism
- Citation format → book_id linkage is clear and self-documenting

**Gaps to address:**

| Issue | Priority | Fix |
|-------|----------|-----|
| `add_knowledge_source` always routes to secondary | **High** | Add `primary_task_types` parameter |
| Errors returned as text, not MCP error codes | Medium | Use `McpError` for not-found and invalid-param cases |
| Book list does not include category | Medium | Add category to `format_book_list()` output |
| No section discovery for books | Low | Add section list to book info, or add `list_book_sections` |
| `remove_items` has no section scoping | Low | Add optional `section` parameter to `remove_items` action |
| `full` section response is unbounded | Low | Add token estimate to description |
| Anti-patterns excluded from standard mode | Low | Reconsider: include in standard, make brief the stripped version |
