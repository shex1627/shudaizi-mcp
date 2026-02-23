# Building Effective Agents
**Date:** December 19, 2024
**URL:** https://www.anthropic.com/engineering/building-effective-agents
**Source:** Web-fetched Feb 2026

---

## Core Thesis

The most successful agent implementations use simple, composable patterns rather than complex frameworks. Start simple, add complexity only when measurably necessary.

## Key Architectural Distinction

- **Workflows** = LLMs orchestrated through predefined code paths — predictable, suited for well-defined tasks
- **Agents** = LLMs dynamically directing their own processes and tool usage — flexible, suited for open-ended problems

## The 5 Workflow Patterns + 1 Agent Pattern

### 1. Prompt Chaining
Sequential steps where each LLM call processes previous output. Best for tasks cleanly decomposable into fixed subtasks.
- Example: generate marketing copy → translate into different language
- Add programmatic checkpoints between steps to verify progress
- Gate on intermediate output quality before proceeding

### 2. Routing
Classify inputs, direct to specialized downstream tasks.
- Example: route simple questions to Haiku, complex ones to Sonnet/Opus
- Example: sort customer service queries by type (billing, technical, general)
- Separates concerns, allows specialized optimization per route

### 3. Parallelization
Execute multiple LLM calls simultaneously via two approaches:
- **Sectioning**: independent subtasks run in parallel (e.g., guardrails + query processing simultaneously)
- **Voting**: identical tasks run multiple times for diverse outputs (e.g., code vulnerability review from multiple angles)

### 4. Orchestrator-Workers
Central LLM dynamically breaks tasks into subtasks, delegates to workers, synthesizes results.
- Key advantage: subtasks determined by input, not predefined
- Example: coding products that make complex changes to multiple files
- Central orchestrator decides decomposition strategy at runtime

### 5. Evaluator-Optimizer
One LLM generates, another evaluates in a loop.
- Effective when clear evaluation criteria exist
- Example: literary translation where nuances require multiple refinement rounds
- Loop continues until quality threshold met

### 6. Autonomous Agents
LLMs using tools in feedback loops with environment grounding.
- Require: ground truth from environment, clear success criteria, sandboxed environments, appropriate guardrails
- Gain "ground truth from the environment at each step" through tool results
- Can pause for human feedback at checkpoints

## Decision Framework

```
Single LLM calls → Workflows (well-defined tasks) → Agents (open-ended problems)
```

Start with the simplest approach that works. Only increase complexity when measurement proves it's necessary.

## Agent-Computer Interface (ACI) Design

"Treat agent-computer interfaces with the rigor applied to human-computer interfaces."

- Anthropic's SWE-bench agent spent more time optimizing tools than the overall prompt
- Requiring absolute filepaths instead of relative paths eliminated a class of errors
- Tool design > prompt optimization in agent performance

## Framework Guidance

While tools like Claude Agent SDK, Strands Agents SDK, Rivet, and Vellum simplify implementation, Anthropic recommends starting "with LLM APIs directly: many patterns can be implemented in a few lines of code."

## Key Quotable

> "Simple, composable patterns rather than complex frameworks."

---

## Applicability
- Agent architecture selection
- System design for LLM-powered applications
- Tool design philosophy
- Build vs. buy framework decisions
