# How We Built Our Multi-Agent Research System
**Date:** June 13, 2025
**URL:** https://www.anthropic.com/engineering/multi-agent-research-system
**Source:** Web-fetched Feb 2026

---

## Core Thesis

Multi-agent orchestrator-worker pattern achieves 90.2% better performance than single-agent Claude Opus 4 on research tasks. Token usage explains 80% of variance in research quality.

## Architecture

- **Lead agent**: Analyzes user queries, develops strategy, spawns specialized subagents
- **Subagents**: Explore different research aspects simultaneously
- **Citation agent**: Synthesizes findings and adds citations
- Pattern: Orchestrator-Worker (from Building Effective Agents)

## Key Performance Findings

| Metric | Detail |
|--------|--------|
| Performance gain | 90.2% better than single-agent Opus 4 |
| Token variance | 80% of quality variance explained by token usage |
| Token multiplier | ~15x more tokens than standard chat |
| Time reduction | 3-5 parallel subagents cut research time by up to 90% |

## Critical Engineering Principles

### Prompt Engineering Over Hard Rules
- Encoded research heuristics into prompts, mirroring expert human approaches
- Lead agent needs explicit scaling guidelines:
  - Simple fact-finding → 1 agent, 3-10 tool calls
  - Complex research → 10+ specialized subagents

### Tool Design Matters Immensely
- Agent-tool interfaces proved as critical as HCI
- Poorly described tools send agents down wrong paths
- Claude models themselves excel at improving tool descriptions

### Filesystem Over Conversation
- Subagents should write results to filesystem rather than passing through conversation history
- Prevents context bloat in the lead agent
- Enables parallel work without coordination overhead

### Task Descriptions Must Be Detailed
- Vague instructions from lead agent cause duplication across subagents
- Specific, detailed task descriptions prevent overlap

## Evaluation Methodology

- **Small-sample testing**: Start with ~20 representative queries — revealed substantial impacts from prompt adjustments
- **LLM-as-judge**: Single prompt evaluating against rubrics (factual accuracy, citation precision, completeness, source quality, efficiency) — scaled across hundreds of outputs
- **Human oversight**: Manual testing caught edge cases automation missed, including biases toward "SEO-optimized content farms over authoritative sources"
- **Key insight**: A single LLM-as-judge proved more consistent than multiple specialized judges

## Production Challenges

### Resume-from-Checkpoint
Rather than restarting failed agents, systems recover from last known state.

### Production Tracing
Monitor decision patterns and interaction structures — without examining conversation contents — to diagnose failure modes.

### Rainbow Deployments
Gradually shift traffic between versions to prevent disrupting long-running agents. Can't do standard blue-green when agents run for minutes.

## Architectural Limitations

- Current synchronous execution model creates bottlenecks
- Lead agents wait for subagent completion before proceeding
- Asynchronous execution could enable additional parallelism but introduces state consistency complexity

## Key Quotable

> "Token usage by itself explains 80% of the variance."

---

## Applicability
- Multi-agent system design
- Research automation architecture
- Evaluation methodology for non-deterministic systems
- Production deployment of agentic systems
