# Building Agents with the Claude Agent SDK
**Date:** September 29, 2025
**URL:** https://claude.com/blog/building-agents-with-the-claude-agent-sdk
**Source:** Web-fetched Feb 2026

---

## Core Principle

"Agents work best when given access to a computer." Claude needs the same tools programmers use every day — file management, terminal access, code execution, iterative debugging.

## The Agent Loop

Four-stage feedback cycle:

```
Gather Context → Take Action → Verify Work → Iterate
```

### 1. Gather Context
- **Agentic Search**: bash commands like `grep` and `tail` to extract information from large files
- **Semantic Search**: embeddings-based retrieval for conceptual queries
- **Subagents**: parallel processing with isolated context windows — "sifting through large amounts of information where most of it won't be useful"
- **Compaction**: automatic summarization as context limits approach

### 2. Take Action
- **Custom Tools**: primary, high-frequency actions designed with context efficiency in mind
- **Bash/Scripts**: general-purpose command execution for flexible computer interactions
- **Code Generation**: precise, composable outputs for complex, reusable operations
- **MCPs**: standardized integrations to external services (Slack, GitHub, Asana) handling authentication automatically

### 3. Verify Work
- **Rules-Based Feedback**: explicit output requirements with detailed error reporting (e.g., linting)
- **Visual Feedback**: screenshots and renders for UI tasks — layout, styling, content hierarchy, responsiveness
- **LLM Judgment**: secondary models evaluate outputs against fuzzy criteria (latency tradeoff)

### 4. Iterate
Refine outputs based on verification results. Loop continues until quality criteria met.

## Filesystem as Context Engineering

The SDK "treats file systems as a form of context engineering." Agents navigate information hierarchies naturally:
- Folder structure provides organizational context
- File naming conventions signal content
- Timestamps indicate recency
- No need for pre-engineered retrieval pipelines

## Practical Applications

- Finance agents analyzing portfolios and investments
- Personal assistants managing calendars and travel
- Customer support handling ambiguous requests
- Research agents synthesizing information across document collections

## Key Quotable

> "Agents work best when given access to a computer."

---

## Applicability
- Agent development with Claude SDK
- Tool design for agent systems
- Context gathering and verification patterns
- MCP integration architecture
