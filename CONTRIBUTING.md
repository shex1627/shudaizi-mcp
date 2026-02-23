# Contributing to Shudaizi Knowledge System

## Adding Knowledge: Two Paths

### Path 1: LLM-Driven (Recommended)

Ask any MCP-connected coding agent:

```
"Add knowledge about Thinking Fast and Slow by Daniel Kahneman"
```

The agent will:
1. Research the book/article using web search
2. Generate research markdown following the standard template
3. Call `add_knowledge_source(...)` — which creates the file, updates `book_index.json`, and updates `routing.json`
4. Optionally call `update_checklist(...)` to add relevant items to affected task checklists

### Path 2: Manual

1. **Create the research file** in `book_research/` following the template in `book_research_prompts.md`
   - Books: `book_research/XX_title_slug.md` (next sequential number)
   - Articles: `book_research/anthropic_articles/XX_title_slug.md`

2. **Update `knowledge/book_index.json`** — add an entry with id, title, author, year, category, file path

3. **Update `knowledge/routing.json`** — add the new source ID to relevant task types' `primary_sources` or `secondary_sources`

4. **Update relevant checklists** in `knowledge/checklists/` — add checklist items citing the new source with `[XX]` notation

## Research File Template

Each research file should contain these sections:

```markdown
# [Title] — [Author] ([Year])
**Skill Category:** [e.g., Architecture & System Design]
**Relevance to AI-assisted workflows:** [1-2 sentences]

---

## Key Ideas
[Core concepts and principles]

## Patterns
[Named patterns, techniques, and approaches]

## Tradeoffs
[Key tradeoffs and tensions the book surfaces]

## Pitfalls
[Common mistakes and anti-patterns]

## Key Framings
[Memorable mental models and quotable insights]

## Applicability
[When and where these ideas apply — and when they don't]
```

See `book_research_prompts.md` for the full master template with detailed instructions.

## Checklist Format

Each checklist item must cite its source:

```markdown
- [ ] Verify retry logic uses exponential backoff with jitter [17]
- [ ] Check for cascading failure paths between services [17][05]
```

Citation keys:
- `[01]`–`[33]` = book IDs (see `knowledge/book_index.json`)
- `[a01]`–`[a21]` = Anthropic article IDs

## Adding a New Task Type

1. Create `knowledge/checklists/your_task_type.md` with YAML frontmatter
2. Add the task to `knowledge/routing.json` with source mappings
3. Create `skills/your-task-type/SKILL.md` for Claude Code integration
4. The MCP server auto-discovers new checklists on reload

## Updating Existing Checklists

Via MCP:
```
update_checklist(task_type="code_review", action="add_items", section="Security", content="- [ ] Check for SQL injection in dynamic queries [07]")
```

Manually: edit the checklist file directly, bump the `version` in frontmatter.

## Quality Guidelines

- **Token budget**: Checklists should be 100-150 lines (~3-6K tokens at standard detail)
- **Cite everything**: Every checklist item must reference at least one source
- **Actionable items**: Each item should be a concrete check, not a vague principle
- **No duplicates**: Before adding, check if the insight is already covered under a different framing
- **Tradeoff awareness**: Flag items where context matters — "if X, then Y; otherwise Z"
