# Introducing Advanced Tool Use
**Date:** November 24, 2025
**URL:** https://www.anthropic.com/engineering/advanced-tool-use
**Source:** Web-fetched Feb 2026

---

## Overview

Three beta features enabling Claude to work more efficiently with large tool libraries. Each addresses a different scaling bottleneck.

## 1. Tool Search Tool — Dynamic Discovery

Instead of loading all tool definitions upfront, Claude discovers tools on-demand.

### How It Works
- Tools marked with `defer_loading: true` become discoverable but not loaded
- Claude initially sees only the search tool
- Retrieves full definitions when needed for the current task

### Metrics
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Token usage (50+ tools) | ~72K | ~8.7K | 85% reduction |
| Opus 4 accuracy | 49% | 74% | +25 pts |
| Opus 4.5 accuracy | 79.5% | 88.1% | +8.6 pts |
| Context preserved | ~5% | ~95% | 95% of window preserved |

### When to Deploy
- Tool definitions exceed 10K tokens
- 10+ tools available
- Many tools rarely needed per-task

## 2. Programmatic Tool Calling — Code-Orchestrated Execution

Claude writes Python scripts to orchestrate multiple tool calls, keeping intermediate results out of the model's context entirely.

### How It Works
- Claude generates Python code that calls tools with loops, conditionals, data transformations
- Intermediate results stay in execution environment
- Only final summary returns to Claude's context

### Metrics
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Avg token usage | 43,588 | 27,297 | 37% reduction |
| Knowledge retrieval | 25.6% | 28.5% | +2.9 pts |
| Benchmark scores | 46.5% | 51.2% | +4.7 pts |
| Data size in context | 200KB | 1KB | 99.5% reduction |

### Use Case
Budget compliance: previously fetched 2,000+ expense line items → now processes programmatically, returns only final summary.

## 3. Tool Use Examples — Concrete Invocation Patterns

Provide concrete examples of correct tool invocation beyond what JSON schemas can express.

### What They Show
- Format conventions
- Nested structures
- Parameter correlations
- Domain-specific conventions

### Metrics
| Metric | Before | After |
|--------|--------|-------|
| Complex parameter accuracy | 72% | 90% |

## Synergy

The three features work together:
1. **Search** → correct tool discovery
2. **Programmatic calling** → efficient execution
3. **Examples** → accurate invocation

## Key Quotable

> Tool Search Tool achieves "85% reduction in token usage" while improving accuracy.

---

## Applicability
- Large tool catalog management
- Data-heavy agent workflows
- Multi-step tool orchestration
- Token budget optimization
