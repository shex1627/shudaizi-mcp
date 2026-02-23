# Writing Effective Tools for Agents
**Date:** September 11, 2025
**URL:** https://www.anthropic.com/engineering/writing-tools-for-agents
**Source:** Web-fetched Feb 2026

---

## Core Insight

"Tools are a new kind of software which reflects a contract between deterministic systems and non-deterministic agents."

## The Five Design Principles

### 1. Selective Tool Design — Fewer, More Purposeful Tools
- More tools don't always lead to better outcomes
- Build "a few thoughtful tools targeting specific high-impact workflows"
- Consolidate related operations into single tools
- Example: Instead of separate `list_users`, `list_events`, `create_event` tools → single `schedule_event` tool that handles availability internally

### 2. Clear Namespacing
- Hierarchical organization reduces agent confusion
- Common prefixes for services: `asana_search`, `jira_search`
- Common prefixes for resources: `asana_projects_search`, `asana_users_search`
- Critical when dozens of MCP servers and hundreds of tools available

### 3. Meaningful Context Returns
- Prioritize "contextual relevance over flexibility"
- Replace cryptic identifiers (`uuid`, `mime_type`) with human-readable fields (`name`, `file_type`)
- "Resolving arbitrary alphanumeric UUIDs to more semantically meaningful language significantly improves Claude's precision in retrieval tasks"
- `response_format` enum parameter: let agents request concise vs. detailed responses

### 4. Token Efficiency
- Agent context has limits — every token counts
- Implement: pagination, filtering, truncation with sensible defaults
- Helpful error messages that guide toward efficient strategies (not opaque error codes)
- Claude Code defaults to 25,000 tokens per tool response

### 5. Prompt-Engineered Descriptions
- Tool descriptions directly steer agent behavior
- Think of how you'd "describe your tool to a new hire"
- Clear, detailed specifications dramatically improve performance
- State-of-the-art results on SWE-bench Verified "after making precise refinements to tool descriptions"

## Development Process

### Phase 1: Building Prototypes
- Use Claude Code with documentation files (like `llms.txt`) to generate initial implementations
- Wrap tools in local MCP servers or Desktop Extensions for testing

### Phase 2: Running Evaluations
- Create realistic evaluation tasks requiring multiple tool calls
- Generate prompt-response pairs grounded in actual workflows
- Measure performance programmatically using simple agentic loops

### Phase 3: Collaborating with Agents
- Paste evaluation transcripts into Claude Code for automated analysis
- "Most of the advice in this post came from repeatedly optimizing our internal tool implementations with Claude Code"
- Iterative, evaluation-driven approach ensures tools remain effective as AI evolves

## Key Quotables

> "Tools are a new kind of software which reflects a contract between deterministic systems and non-deterministic agents."

> "Treat agent-computer interfaces with the rigor applied to human-computer interfaces." (ACI = new discipline)

---

## Applicability
- MCP server development
- API design for AI agents
- Tool catalog management
- Agent performance optimization
