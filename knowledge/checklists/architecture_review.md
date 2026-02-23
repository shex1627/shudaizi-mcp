---
task: architecture_review
description: Review system architecture for soundness, tradeoffs, and maintainability
primary_sources: ["01", "02", "03", "04", "05", "06"]
secondary_sources: ["17", "18", "19"]
anthropic_articles: ["a01", "a05"]
version: 1
updated: 2026-02-22
---

# Architecture Review Checklist

## Phase 1: Structural Assessment

- [ ] Identify the driving architectural characteristics (pick 3-7 from operational, structural, cross-cutting) and confirm the chosen style supports them [02]
- [ ] Verify the architecture quantum: what is the smallest independently deployable unit? Does it match what the team claims? [02][03]
- [ ] Check if modules are connected through stable abstractions or concrete implementations — source-code dependencies must point inward toward higher-level policies [04]
- [ ] Evaluate module depth: do interfaces hide significant complexity, or are modules shallow wrappers that just pass calls through? [06]
- [ ] Check for the entity trap: are components organized around database entities instead of workflows or business capabilities? [02]
- [ ] Verify each layer provides a fundamentally different abstraction than adjacent layers — flag pass-through methods and pass-through variables [06]
- [ ] Assess coupling dimensions: identify static coupling (implementation, temporal, deployment, domain) and dynamic coupling (sync/async, orchestration/choreography) at each service boundary [03]
- [ ] Confirm bounded contexts align with service boundaries — each service should map to a cohesive domain, not a database table [05]
- [ ] Check for information leakage: is the same design decision (data format, protocol detail, algorithm) reflected in multiple modules? [06]
- [ ] Verify the top-level structure "screams" the business domain, not the framework — use cases should be first-class organizational units [04]

## Phase 2: Data Architecture

- [ ] Confirm each service owns its data exclusively — flag any shared databases between services as a distributed monolith risk [03][05]
- [ ] Verify the data model matches the access pattern: relational for joins, document for self-contained aggregates, graph for relationship traversal [01]
- [ ] Check storage engine fit: B-tree stores for read-heavy workloads, LSM-tree stores for write-heavy workloads — wrong engine class causes unfixable performance issues [01]
- [ ] Assess consistency requirements per use case: what is the actual cost of stale or inconsistent data? Strong consistency only where the business demands it [01]
- [ ] Evaluate replication topology tradeoffs: single-leader (simple, bottleneck), multi-leader (write conflicts), leaderless (tunable quorum) [01]
- [ ] Verify schema evolution strategy supports backward and forward compatibility for all inter-service data exchange [01]
- [ ] Check that derived data (caches, search indexes, materialized views) is treated as recomputable from a system of record, not manually synchronized [01]
- [ ] For distributed transactions, verify saga design includes compensating transactions, idempotency for every step, and dead-letter queue handling [03][05]
- [ ] Flag any unbounded result sets — every query that could return unbounded results is a production incident waiting to happen [17]

## Phase 3: Resilience & Operations

- [ ] Verify every integration point has a timeout (both connection and read), a circuit breaker consideration, and a defined fallback behavior [17]
- [ ] Check for cascading failure paths: can a slow downstream service exhaust thread pools or connection pools in the caller? [17]
- [ ] Confirm bulkhead isolation: separate resource pools per integration point so one hung dependency cannot drain shared resources [17]
- [ ] Verify retry logic uses exponential backoff with jitter and a maximum retry count — immediate retries create thundering herds [17]
- [ ] Check for back-pressure mechanisms: bounded queues, rate limiting, load shedding — a system without back pressure accepts work until it dies [17]
- [ ] Validate capacity for N-1 operation: what happens when one instance dies and load shifts to survivors? [19]
- [ ] Confirm SLIs are defined (latency, traffic, errors, saturation) with explicit SLO targets that reflect real user experience [19]
- [ ] Verify error budgets are established and the process for when they are exhausted (deploy freeze, reliability sprint) is agreed upon [19]
- [ ] Check that the system reaches steady state without human intervention: log rotation, cache eviction, data archival are all automated [17]
- [ ] Confirm graceful degradation is designed, not just the happy path — what does each feature do when its dependencies are unavailable? [17]

## Phase 4: Observability

- [ ] Verify distributed trace context propagates through every service, queue, and async boundary (W3C Trace Context or B3 headers) [18]
- [ ] Check that telemetry uses structured events with rich context (user ID, request ID, feature flags, build SHA) rather than unstructured log strings [18]
- [ ] Confirm alerts fire on symptoms (user-visible impact), not causes (CPU spikes) — every alert must have a clear response procedure [19]
- [ ] Verify the system is debuggable for novel failures: can an engineer who has never seen this system explore production telemetry to diagnose an unknown issue? [18]
- [ ] Check that instrumentation is treated as a first-class engineering concern — reviewed in PRs, tested, budgeted for [18]

## Phase 5: Scalability & Evolution

- [ ] Verify partitioning is justified by actual single-node limitations — do not partition prematurely [01]
- [ ] Check partitioning strategy avoids hot spots: monotonically increasing keys (auto-increment, timestamps) concentrate load on one partition [01]
- [ ] Confirm the architecture can evolve: are there fitness functions (automated checks) that prevent architectural drift over time? [02][03]
- [ ] Verify architectural decisions are documented as ADRs capturing context, decision, and accepted tradeoffs [02][03]
- [ ] Assess whether the system's complexity matches the team's operational maturity — microservices require mature DevOps, CI/CD, and observability practices [02][05]

## Phase 6: Maintainability & Design Quality

- [ ] Check that complexity is pulled downward into implementations, not pushed upward into interfaces and caller code [06]
- [ ] Verify interfaces are "somewhat general-purpose" — specific enough for current needs, stable enough for future extension without interface changes [06]
- [ ] Flag temporal decomposition: code organized by execution order (read, parse, process) rather than by information to be hidden [06]
- [ ] Confirm strategic programming: is 10-20% of development time invested in design quality, or is the codebase accumulating tactical shortcuts? [06]
- [ ] Check for errors designed out of existence: are interfaces broadened to eliminate exception cases where the caller's intent is achievable either way? [06]
- [ ] At service boundaries, verify duplication is preferred over coupling — shared libraries between services create hidden deployment coupling [02][03]

## Phase 7: Agent & AI System Architecture (when applicable)

- [ ] Verify the simplest viable pattern is used: single LLM call before workflow, workflow before autonomous agent [a01]
- [ ] Check that agent-computer interfaces are designed with the same rigor as human-computer interfaces — tool design matters more than prompt optimization [a01]
- [ ] Confirm context is curated for signal density: the smallest set of high-signal tokens, not maximum context stuffing [a05]
- [ ] Verify long-horizon tasks have a context management strategy: compaction, structured note-taking, or sub-agent architectures [a05]
- [ ] Check that tools are self-contained, unambiguous, and have minimal overlap — bloated tool sets encourage misuse and waste context [a05]

---

## Key Questions to Ask

1. "What are you giving up by choosing this architecture?" — Every choice is a tradeoff; if no one can name the downsides, the tradeoffs have not been analyzed [02]
2. "What happens when this dependency is slow? Down? Returns garbage?" — Force explicit failure mode analysis for every integration point [17]
3. "Can these services actually be deployed independently, or must they be released in lockstep?" — The honest answer reveals whether you have microservices or a distributed monolith [03][05]
4. "What is the cost of reading stale data in this specific use case?" — Determines whether eventual consistency is acceptable or a stronger guarantee is required [01]
5. "If a new engineer joined tomorrow, could they debug a novel production issue using only the system's telemetry?" — The observability litmus test [18]
6. "Is this interface simpler than the implementation it hides?" — The deep module test for every new abstraction [06]
7. "What is the simplest architecture that meets these requirements?" — Resist complexity that does not serve a driving characteristic [02]
8. "Does the team/org structure support these service boundaries?" — Conway's Law is a force, not a suggestion [02][05]
9. "Where are the single points of failure, and what is the blast radius of each?" — Map failure domains explicitly [17][19]
10. "Is this a best practice, or is this a tradeoff we've analyzed for our context?" — There are no best practices in architecture, only tradeoffs [02][03]

---

## Anti-Patterns to Flag

| Anti-Pattern | Signal | Source |
|---|---|---|
| **Distributed monolith** | Services share a database or require lockstep deployment | [03][05] |
| **Premature decomposition** | Service boundaries drawn before the domain is understood; constant cross-service changes | [03][05] |
| **Entity services** | Services that are thin CRUD wrappers around database tables instead of encapsulating business behavior | [02][05] |
| **Missing timeouts** | Outbound calls without explicit connection and read timeouts — the #1 stability anti-pattern | [17] |
| **Naive retries** | Immediate, unlimited retries without backoff or jitter creating thundering herds | [17] |
| **Architecture sinkhole** | Requests passing through layers without meaningful processing in each layer | [02] |
| **Shallow module proliferation** | Many tiny classes/functions that each add an interface without absorbing complexity | [06] |
| **Stamp coupling** | Services passing entire objects when only an ID or subset is needed | [03] |
| **Unstructured logging** | Freeform log strings instead of structured events — makes novel debugging impossible | [18] |
| **Hope-based reliability** | No SLOs defined, no error budgets, no tested rollback path — "it should be fine" | [19] |
| **Cargo-cult microservices** | Choosing microservices because they are trendy rather than because driving characteristics demand distribution | [02][05] |
| **God orchestrator** | A central saga orchestrator that accumulates all business logic and becomes a single point of failure | [03] |
