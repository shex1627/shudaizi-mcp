# Agent Skills: Equipping Agents for the Real World
**Date:** December 18, 2025
**URL:** https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills
**Source:** Web-fetched Feb 2026

---

## What Agent Skills Are

Organized directories of instructions, scripts, and resources that agents discover and load dynamically. "Onboarding guides for AI agents" — packaging procedural knowledge into reusable, composable resources.

Rather than building separate custom agents per use case, extend existing agents with specialized capabilities.

## The SKILL.md Structure

At its simplest: a directory containing a `SKILL.md` file.

```yaml
---
name: skill-name
description: What this skill enables
---
```

- **YAML frontmatter**: required `name` and `description`
- **Instructional body**: detailed agent capabilities and procedures
- **Optional linked files**: additional context and specialized scenarios

Metadata appears in system prompt at startup → Claude recognizes when each skill applies.

## Progressive Disclosure Architecture

Three-tier information loading:

| Level | What Loads | When |
|-------|-----------|------|
| Level 1 (Metadata) | Skill name + description | Startup — in system prompt |
| Level 2 (Core Content) | Full SKILL.md | When skill becomes relevant |
| Level 3+ (Supplementary) | Additional referenced files | On-demand as needed |

Mirrors "a well-organized manual that starts with a table of contents, then specific chapters, and finally a detailed appendix."

## Key Insight: Unbounded Context

"The amount of context that can be bundled into a skill is effectively unbounded" because agents load information on-demand via filesystem access.

No need to fit everything in the system prompt. Skills can reference unlimited supplementary files.

## Code Execution Integration

- Skills can bundle executable scripts (typically Python)
- Claude runs them directly for deterministic tasks
- More efficient than token-based operations for: sorting, form extraction, data transformation
- Code provides reliability that prompt-based approaches can't match

## Development Best Practices

1. **Start with evaluation**: Identify capability gaps by running agents on representative tasks
2. **Structure for scale**: Split unwieldy content into separate files; use code as both executable and reference
3. **Adopt Claude's perspective**: Monitor how Claude actually uses skills; iterate based on observed patterns
4. **Iterate collaboratively**: Ask Claude to capture successful approaches into reusable skill components

## Security Considerations

- Install skills only from trusted sources
- Before deploying third-party skills, audit:
  - Bundled files
  - Code dependencies
  - External network connections instructions might trigger

## Platform Support

Skills supported across: Claude.ai, Claude Code, Claude Agent SDK, Claude Developer Platform.

## Key Quotable

> "The amount of context that can be bundled into a skill is effectively unbounded."

---

## Applicability
- Agent capability extension
- Knowledge management for AI systems
- Progressive disclosure architecture
- Reusable AI workflow design
