# Code Execution with MCP: Building More Efficient Agents
**Date:** November 4, 2025
**URL:** https://www.anthropic.com/engineering/code-execution-with-mcp
**Source:** Web-fetched Feb 2026

---

## Core Pattern: Filesystem-as-API

Present MCP servers as code libraries via filesystem structure instead of direct tool calls. Agents discover tools by exploring directories.

**Result:** 150,000 tokens → 2,000 tokens (**98.7% reduction**).

## The Problem: Token Inefficiency

Two scaling challenges:

1. **Tool Definition Overload**: Traditional MCP clients load all tool definitions upfront, consuming hundreds of thousands of tokens before processing requests
2. **Intermediate Result Repetition**: Large documents pass through model context multiple times (e.g., meeting transcript retrieved then written → 50K tokens doubled)

## The Solution

### Implementation
- Create file tree structure mapping servers and tools
- Each tool becomes a TypeScript module
- Agents discover tools by exploring the filesystem
- Only needed definitions load for the current task

### Key Benefits

**Progressive Disclosure**
- Models read tool definitions on-demand
- `search_tools` function with detail-level parameters helps conserve context
- Navigate filesystem → discover what's available → load what's needed

**Context-Efficient Data Processing**
- Filter and transform large datasets in execution environment before returning results
- 10,000-row spreadsheet → filter to relevant entries only
- Intermediate results stay in execution environment

**Control Flow Efficiency**
- Loops, conditionals, error handling execute in code
- Not via chained tool calls
- Improved latency, reduced model overhead

**Privacy Preservation**
- Sensitive data (PII) can be tokenized automatically
- Flows directly between systems without entering model context
- Intermediate results stay in execution environment by default

**State Persistence**
- Progress saved to files
- Enables resumable workflows
- Reusable skill libraries

## Tradeoffs

The approach trades operational complexity for efficiency:
- Running agent-generated code requires secure sandboxing
- Resource limits and monitoring needed
- Infrastructure overhead that direct tool calls avoid
- Security and operational costs must be weighed against token savings

## Key Quotable

> Filesystem-as-API: "reduces token usage from 150,000 tokens to 2,000 tokens—a time and cost saving of 98.7%."

---

## Applicability
- MCP server architecture
- Agent efficiency optimization
- Large-scale data processing with agents
- Privacy-preserving agent design
