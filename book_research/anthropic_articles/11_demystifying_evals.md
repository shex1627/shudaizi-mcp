# Demystifying Evals for AI Agents
**Date:** January 9, 2026
**URL:** https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
**Source:** Web-fetched Feb 2026

---

## Core Thesis

"Teams without evals face reactive debugging loops; teams investing early experience accelerated development."

## Key Terminology

| Term | Definition |
|------|-----------|
| **Task** | Single test with defined inputs and success criteria |
| **Trial** | One attempt at a task (run multiple for consistency) |
| **Grader** | Logic scoring performance; tasks can have multiple graders |
| **Transcript** | Complete record: outputs, tool calls, reasoning, interactions |
| **Outcome** | Final environmental state after trial completion |
| **Evaluation harness** | Infrastructure running evals end-to-end |
| **Agent harness** | System enabling models to act as agents |

## Three Grader Types

### 1. Code-Based Graders
- String matching, regex, binary tests, static analysis, outcome verification
- **Pros**: fast, cheap, objective, reproducible
- **Cons**: brittle to valid variations

### 2. Model-Based Graders
- Rubric scoring, natural language assertions, pairwise comparisons, multi-judge consensus
- **Pros**: flexible, scalable
- **Cons**: non-deterministic, requires human calibration

### 3. Human Graders
- Subject matter expert review, crowdsourced judgment
- **Pros**: gold standard quality
- **Cons**: expensive, slow

## Critical Metrics: Pass@k and Pass^k

Handle non-determinism in agent behavior:

- **Pass@k** = probability of at least one correct solution in k attempts → **increases** with k
- **Pass^k** = probability ALL k trials succeed → **decreases** with k

**Example**: 75% per-trial rate → Pass^3 = ~42%

At k=10: Pass@k approaches 100%, Pass^k may approach 0%. The divergence reveals reliability vs. capability.

## The 8-Step Roadmap

1. **Start early** with 20-50 tasks from actual failures
2. **Convert manual checks** from development and support queues into automated tests
3. **Write unambiguous tasks** — two experts should agree on pass/fail; create reference solutions passable by agents
4. **Build balanced problem sets** — test both presence AND absence of behaviors
5. **Design robust harnesses** — isolated, clean environments per trial
6. **Choose graders thoughtfully** — favor outcomes over specific paths; avoid overly brittle step-sequence checking
7. **Check transcripts** regularly to verify grader accuracy
8. **Monitor saturation** — refresh capability evals, retire saturated tasks to regression suites

## Swiss Cheese Model

No single evaluation method catches everything. Layer:

| Layer | Purpose |
|-------|---------|
| Automated evals | Fast iteration without user impact |
| Production monitoring | Real-world performance tracking |
| A/B testing | Controlled variant comparison |
| User feedback | Explicit problem signals |
| Manual transcript review | Intuition-building |
| Human studies | Gold-standard quality |

## Key Quotables

> "Teams without evals face reactive loops; teams investing early experience accelerated development."

> Swiss cheese model: no single method catches everything.

---

## Applicability
- AI agent evaluation design
- Quality assurance for LLM applications
- Benchmark methodology
- CI/CD for AI systems
