---
name: devops
description: >
  Design or review CI/CD pipelines, deployment strategy, and infrastructure using The DevOps Handbook,
  Release It, Site Reliability Engineering, Observability Engineering, and DDIA.
  Use when designing pipelines, reviewing deployment architecture, or assessing operational readiness.
---

## When to Activate

- User asks to design or review a CI/CD pipeline
- User asks about deployment strategy (blue-green, canary, rolling, feature flags)
- User presents infrastructure or operational architecture for feedback
- User asks about reliability, SLOs, observability, or incident response
- User needs to assess production readiness of a system

## Procedure

1. Read `knowledge/checklists/devops.md`
2. Assess the system against each checklist phase relevant to the user's context
3. For items needing deeper context, read the cited book file (e.g., `book_research/32_devops_handbook.md`)
4. Present findings organized as: **Strengths** -> **Concerns** -> **Recommendations**
5. For each concern, cite the source book/principle and the specific anti-pattern or missing pattern
6. Prioritize: missing timeouts and circuit breakers before missing observability before cultural practices

## Always-Apply Principles

- Speed and safety reinforce each other — smaller, more frequent deployments are lower risk [32: DevOps Handbook]
- Every integration point is a threat vector for stability — design as if it is trying to kill your system [17: Release It]
- Optimize for MTTR over MTBF — accept that failures happen, minimize blast radius and recovery time [19: SRE]
- Deployment is not release — separate pushing code from exposing functionality [32: DevOps Handbook]
- Alerts should fire on symptoms (user-visible impact), not causes — every alert needs a response procedure [19: SRE]
- Observability means asking arbitrary questions about production without pre-defining them — structured events over log strings [18: Observability Engineering]
- Every change flows through the pipeline — no side doors, no manual deployments [32: DevOps Handbook]

## Deep-Dive References

- The Three Ways, pipeline design, feature flags, trunk-based dev: `book_research/32_devops_handbook.md`
- Stability patterns (timeouts, circuit breakers, bulkheads, backpressure): `book_research/17_release_it.md`
- SLOs, error budgets, four golden signals, blameless postmortems: `book_research/19_site_reliability_engineering.md`
- Structured events, distributed tracing, high-cardinality debugging: `book_research/18_observability_engineering.md`
- Data systems, replication, partitioning, consistency tradeoffs: `book_research/01_designing_data_intensive_applications.md`
- Dual-boundary sandboxing for agents: `book_research/anthropic_articles/14_sandboxing.md`
- Long-running agent harness patterns: `book_research/anthropic_articles/04_long_running_agents.md`
