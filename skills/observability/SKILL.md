---
name: observability
description: >
  Observability review using Observability Engineering, Release It!, and SRE principles.
  Use when designing instrumentation, reviewing telemetry coverage, debugging production issues, or setting up SLOs and alerting.
---

## When to Activate

- User asks to review or design observability, monitoring, or alerting for a system
- User is debugging a production issue and needs a structured diagnostic approach
- User is setting up SLOs, SLIs, or error budgets
- User is adding instrumentation, tracing, or structured logging to code
- User asks about incident response, postmortem practices, or on-call improvements
- User is evaluating whether a system can be debugged by someone unfamiliar with it

## Procedure

1. Read `knowledge/checklists/observability.md`
2. Assess the system against relevant checklist phases:
   - For new systems: start with Phase 1 (SLOs) and Phase 2 (instrumentation)
   - For existing systems: start with Phase 4 (debugging capability) to identify gaps
   - For incidents: use the core analysis loop from Phase 4 and Key Questions
3. For items needing deeper context, read the cited book file
4. Present findings organized by priority: **Critical gaps** -> **High-value improvements** -> **Polish items**
5. For each finding: describe the gap, cite the source, suggest a concrete fix
6. Always check Phase 3 (alerting) — alert fatigue and missing runbooks are universal problems

## Always-Apply Principles

- Observability is the ability to ask arbitrary questions about production without deploying new code — if you cannot do this, you have monitoring, not observability [18: Observability Engineering]
- Every outbound call needs a timeout; missing timeouts are the #1 stability anti-pattern and the #1 cause of cascading failures [17: Release It!]
- Alert on symptoms (user-visible impact), not causes (infrastructure metrics); pages should only fire when immediate human action is required [19: SRE]
- High-cardinality data is the sine qua non of observability — if you cannot query by user ID, request ID, or feature flag, you cannot debug real production issues [18]
- SLOs convert vague reliability desires into concrete, measurable targets that drive engineering decisions — without them, reliability is undefined [19]

## Deep-Dive References

- Observability philosophy & structured events: `book_research/18_observability_engineering.md`
- Stability patterns & failure modes: `book_research/17_release_it.md`
- SLOs, error budgets & SRE practices: `book_research/19_site_reliability_engineering.md`
- Deployment telemetry & feedback loops: `book_research/32_devops_handbook.md`
- Data system reliability: `book_research/01_designing_data_intensive_applications.md`
- Infrastructure noise in evals: `book_research/anthropic_articles/12_infrastructure_noise.md`
- Production monitoring lessons: `book_research/anthropic_articles/15_postmortem.md`
