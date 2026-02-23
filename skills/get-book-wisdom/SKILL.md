---
name: get-book-wisdom
description: >
  Retrieve knowledge from a 33-book + 21-article software engineering research library.
  Covers architecture, security, testing, code quality, AI/ML, UX, data viz, product strategy, DevOps, and more.
  Use when you need principles, patterns, checklists, or tradeoffs for any software engineering topic.
---

## When to Activate

- User asks about best practices for any software engineering topic
- User needs principles or patterns from established literature
- User wants a checklist for a task type not covered by a specific skill
- User asks "what does [book] say about X?"

## Available Task Checklists

Read `knowledge/routing.json` for the full task → book mapping. Available task types:

| Task | Checklist File |
|------|---------------|
| architecture_review | knowledge/checklists/architecture_review.md |
| code_review | knowledge/checklists/code_review.md |
| security_audit | knowledge/checklists/security_audit.md |
| test_strategy | knowledge/checklists/test_strategy.md |
| bug_fix | knowledge/checklists/bug_fix.md |
| feature_design | knowledge/checklists/feature_design.md |
| api_design | knowledge/checklists/api_design.md |
| data_viz_review | knowledge/checklists/data_viz_review.md |
| product_doc | knowledge/checklists/product_doc.md |
| presentation | knowledge/checklists/presentation.md |
| devops | knowledge/checklists/devops.md |
| ai_ml_design | knowledge/checklists/ai_ml_design.md |
| refactoring | knowledge/checklists/refactoring.md |
| observability | knowledge/checklists/observability.md |
| ux_review | knowledge/checklists/ux_review.md |
| agent_design | knowledge/checklists/agent_design.md |

## Procedure

1. Identify which task type best matches the user's request
2. Read the corresponding checklist from `knowledge/checklists/`
3. If the user asks about a specific book or topic, check `knowledge/book_index.json` for the file path
4. For deeper context on any cited item (e.g., `[01]`), read the corresponding book research file from `book_research/`
5. Present findings focused on the user's specific question — don't dump the entire checklist

## Book Research Files

All 33 books are in `book_research/` as numbered markdown files (01-33).
All 21 Anthropic articles are in `book_research/anthropic_articles/` (01-21).
Each file contains: Key Ideas, Patterns, Tradeoffs, Pitfalls, Applicability, and Key Framings sections.

## Key Principle

Return the smallest set of high-signal knowledge that addresses the user's question. Don't load everything — use citations to drill down only when needed.
