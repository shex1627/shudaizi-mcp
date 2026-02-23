---
task: devops
description: Design or review CI/CD pipelines, deployment, and infrastructure
primary_sources: ["32", "17", "19"]
secondary_sources: ["18", "01"]
anthropic_articles: ["a14", "a04"]
version: 1
updated: 2026-02-22
---

# DevOps Checklist

## Phase 1: Value Stream & Pipeline Design

- [ ] Map the value stream from code commit to running in production — measure lead time, processing time, and wait time at each stage [32]
- [ ] Design the deployment pipeline in stages: commit (build + unit tests + static analysis) -> acceptance tests -> production-like environments -> production [32]
- [ ] Ensure the pipeline enforces the invariant: every change that passes all stages is deployable [32]
- [ ] Pipeline definition lives in version control alongside the application code — pipeline-as-code [32]
- [ ] Build artifacts once and promote the same artifact through every environment — never rebuild per environment [32]
- [ ] Every change flows through the pipeline: application code, infrastructure config, database migrations, security policies — no side doors [32]
- [ ] Limit work in progress and make work visible (Kanban boards, pipeline dashboards) to optimize flow [32]

## Phase 2: Deployment Strategy

- [ ] Separate deployment (pushing code to infrastructure) from release (exposing functionality to users) using feature flags [32]
- [ ] Choose an appropriate deployment pattern: blue-green, canary, or rolling — each has different rollback characteristics [32][17]
- [ ] Implement feature flags with lifecycle management: every flag has an owner, expiration date, and cleanup plan [32]
- [ ] Use canary deployments with metric-based promotion: deploy to a small percentage, compare SLIs against baseline, then widen [32][19]
- [ ] Ensure every deployment has a tested rollback path — either flag toggle, blue-green switch, or automated rollback on metric degradation [32][17]
- [ ] Database migrations use expand-and-contract (parallel change) pattern for zero-downtime schema changes [32]
- [ ] Treat config changes as deployments — they flow through the pipeline and have rollback procedures [19]

## Phase 3: Stability & Resilience

- [ ] Every outbound call (HTTP, RPC, database, queue) has both a connection timeout and a read/response timeout — missing timeouts are the #1 stability anti-pattern [17]
- [ ] Implement circuit breakers at every integration point: track failures per endpoint, fast-fail when open, probe in half-open state [17]
- [ ] Partition resource pools with bulkheads: separate thread/connection pools per integration point so one hung dependency cannot drain shared resources [17]
- [ ] Retry logic uses exponential backoff with jitter and a maximum retry count — immediate retries create thundering herds [17]
- [ ] Implement back-pressure mechanisms: bounded queues, rate limiting, load shedding — a system without back pressure accepts work until it dies [17]
- [ ] Design for steady state: log rotation, cache eviction, data archival are all automated — no manual "data purge" procedures [17]
- [ ] Plan capacity for N-1 operation: what happens when one instance dies and load shifts to survivors? [19]
- [ ] Design graceful degradation: every feature has a defined behavior when its dependencies are unavailable [17]
- [ ] Treat every integration point as "trying to kill your system" — map failure modes for each external dependency [17]

## Phase 4: Observability & Feedback Loops

- [ ] Define SLIs for the service: latency (p50/p99), error rate, traffic volume, saturation — the four golden signals [19]
- [ ] Set explicit SLO targets that reflect real user experience, with error budgets and a process for when they are exhausted [19]
- [ ] Create telemetry at three levels: business metrics (revenue, conversion), application metrics (request rate, errors, latency), infrastructure metrics (CPU, memory, disk) [32]
- [ ] Ensure distributed trace context propagates through every service, queue, and async boundary (W3C Trace Context) [18]
- [ ] Use structured events with rich context (user ID, request ID, feature flags, build SHA) rather than unstructured log strings [18]
- [ ] Alerts fire on symptoms (user-visible impact), not causes (CPU spikes) — every alert has a clear response procedure [19]
- [ ] Verify the system is debuggable for novel failures: can an engineer who has never seen this system explore production telemetry to diagnose an unknown issue? [18]
- [ ] Broadcast telemetry widely — dashboards visible to everyone, not locked behind ops team access [32]
- [ ] Mean time to detect (MTTD) is as important as mean time to recover (MTTR) — invest in both [32]

## Phase 5: Security & Compliance (Shift Left)

- [ ] Integrate security scanning into the deployment pipeline: SAST, dependency scanning, DAST, container image scanning — all automated, all gating [32]
- [ ] Provide shared, hardened security libraries for common patterns (authentication, encryption, input validation) rather than every team reimplementing [32]
- [ ] Conduct threat modeling in the design phase — shift security thinking to before code is written [32]
- [ ] Implement dual-boundary isolation for agent/automated tooling: filesystem isolation AND network isolation — both are essential [a14]
- [ ] Enforce sandbox boundaries at the OS/kernel level, not just userspace — cover spawned scripts and subprocesses [a14]
- [ ] Security telemetry feeds into the same monitoring and alerting systems used for operations [32]

## Phase 6: Culture & Continuous Learning

- [ ] Conduct blameless postmortems for every significant incident — focus on systemic causes, not individual blame [19]
- [ ] Track postmortem action items to completion — a postmortem without follow-through is waste [19]
- [ ] Reserve capacity (20%+) for improvement work: automation, tooling, pipeline improvements, technical debt reduction [32]
- [ ] Practice deployment as a skill, not an event: "if it hurts, do it more frequently, and bring the pain forward" [32]
- [ ] Adopt trunk-based development: developers commit to main at least daily, short-lived feature branches only [32]
- [ ] Implement structured state management for long-running automated tasks: progress files, git checkpoints, one-feature-per-session discipline [a04]
- [ ] Ensure local discoveries become global improvements: shared libraries, internal tech talks, documented patterns [32]
- [ ] Optimize for MTTR over MTBF: accept that failures happen, minimize blast radius and recovery time [32][19]

---

## Key Questions to Ask

1. "What is the lead time from code commit to running in production?" — The First Way metric; most waste lives in wait time, not work time [32]
2. "Can these services actually be deployed independently, or must they be released in lockstep?" — Reveals distributed monolith risk [32][17]
3. "What happens when this dependency is slow? Down? Returns garbage?" — Force explicit failure mode analysis at every integration point [17]
4. "What is the error budget, and what happens when it is exhausted?" — Makes the reliability-vs-velocity tradeoff explicit and data-driven [19]
5. "Can a new engineer debug a novel production issue using only the system's telemetry?" — The observability litmus test [18]
6. "Is deployment separated from release?" — Feature flags enable continuous deployment with controlled feature rollouts [32]
7. "Does every outbound call have a timeout?" — If the answer is no, stop everything and fix this first [17]
8. "What grows without bound in this system?" — Unbounded result sets, log files, queues, and tables are production incidents waiting to happen [17]
9. "Who bears the on-call pager, and what is their paging rate?" — Excessive paging means the system needs engineering, not more on-call bodies [19]
10. "Is the pipeline the single path to production for ALL changes?" — No side doors, no manual deployments, no exceptions [32]

---

## Anti-Patterns to Flag

| Anti-Pattern | Signal | Source |
|---|---|---|
| **Missing timeouts** | Outbound calls without explicit connection and read timeouts — the #1 stability anti-pattern | [17] |
| **Naive retries** | Immediate, unlimited retries without backoff or jitter creating thundering herds | [17] |
| **Cascading failures** | One slow dependency exhausts thread/connection pools in callers, propagating failure up the chain | [17] |
| **Hope-based reliability** | No SLOs defined, no error budgets, no tested rollback path — "it should be fine" | [19] |
| **Feature flag sprawl** | Flags with no owners, no expiration dates, no cleanup plan — creates combinatorial complexity and dead code | [32] |
| **Manual deployments** | Changes that bypass the pipeline — "just this one hotfix" — undermine the pipeline as a reliable control | [32] |
| **Cargo-cult DevOps** | Adopting tools (Kubernetes, microservices) without the underlying principles of flow, feedback, and learning | [32] |
| **Alert fatigue** | Alerts that fire on causes (CPU spike) rather than symptoms (user impact), or alerts with no response procedure | [19] |
| **Unstructured logging** | Freeform log strings instead of structured events — makes novel debugging impossible | [18] |
| **Single-boundary sandbox** | Only filesystem OR network isolation for agents/automation — both are required for effective security | [a14] |
| **Unbounded result sets** | Queries that could return unlimited results — works in dev (50 rows), fails in production (5M rows) | [17] |
| **Shared databases between services** | Multiple services reading/writing the same database — creates hidden deployment coupling (distributed monolith) | [32][01] |
| **Over-ambitious automation sessions** | Automated agents attempting everything at once instead of one-feature-per-session with checkpoints | [a04] |
