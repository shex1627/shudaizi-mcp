---
task: observability
description: Review or design observability for a system — instrumentation, telemetry, SLOs, alerting, and debugging workflows
primary_sources: ["18", "17", "19"]
secondary_sources: ["32", "01"]
anthropic_articles: ["a12", "a15"]
version: 1
updated: 2026-02-22
---

# Observability Checklist

## Phase 1: Define What "Good" Looks Like (SLOs & Signals)

- [ ] Define SLIs for each user-facing service: latency (p50, p95, p99), error rate, throughput, and saturation [19]
- [ ] Set explicit SLOs with error budgets — e.g., "99.9% of requests under 300ms over 28 days" — and tie them to business outcomes [19] [18]
- [ ] Measure SLOs from real user telemetry, not synthetic checks alone — SLOs should reflect actual user experience [18]
- [ ] Monitor the four golden signals at every service boundary: latency, traffic, errors, saturation [19]
- [ ] Establish error budget policies: when the budget is depleted, what changes (deploy freeze, reliability sprint)? [19]
- [ ] Ensure MTTD (mean time to detect) is tracked alongside MTTR — you cannot fix what you cannot see [32]

## Phase 2: Instrumentation & Structured Events

- [ ] Instrument at boundaries of meaningful work units (requests, jobs, transactions), emitting wide structured events with all relevant context [18]
- [ ] Attach high-cardinality dimensions to every event: user ID, request ID, tenant, build SHA, feature flags, endpoint, region [18]
- [ ] Use OpenTelemetry (OTel) for vendor-neutral instrumentation — auto-instrumentation for baseline, custom spans/attributes for business context [18]
- [ ] Propagate distributed trace context (W3C Trace Context or B3 headers) across every service, queue, and async boundary [18]
- [ ] Ensure each trace span carries rich attributes; add custom attributes liberally — they are cheap and invaluable during debugging [18]
- [ ] Treat instrumentation as a first-class engineering concern: review in PRs, test it, budget time for it [18]
- [ ] Replace unstructured log.info() strings with structured key-value events wherever possible [18]
- [ ] For every new feature, define an instrumentation plan before writing code: what questions will you need to ask in production? [18]

## Phase 3: Alerting & Incident Response

- [ ] Alert on symptoms (user-visible impact), not causes (CPU spike) — only page for conditions requiring immediate human action [19]
- [ ] Classify monitoring output into three buckets: pages (immediate action), tickets (action needed, not urgent), logs (forensic only) [19]
- [ ] Verify every alert has a documented response procedure or runbook — alerts without clear actions cause alert fatigue [19]
- [ ] Use SLO burn rate alerts as the primary incident detection signal rather than static thresholds [18] [19]
- [ ] Ensure circuit breaker state is observable — monitor open/closed/half-open transitions at every integration point [17]
- [ ] Confirm every outbound call has both connection and response timeouts; missing timeouts are the #1 stability anti-pattern [17]
- [ ] Map failure propagation paths: can a single slow dependency cascade through the system? Verify timeout + circuit breaker coverage [17]

## Phase 4: Debugging & Exploratory Analysis

- [ ] Verify the system supports the core analysis loop: signal -> distribution -> slice by dimensions -> drill into traces -> form hypotheses [18]
- [ ] Confirm you can query by high-cardinality dimensions (user ID, request ID, feature flag combo) — if not, you have monitoring, not observability [18]
- [ ] Test the "new engineer" litmus test: can someone unfamiliar with the system debug a novel issue using only the telemetry? [18]
- [ ] Ensure traces connect end-to-end across async boundaries, message queues, and background jobs — broken propagation is the #1 tracing failure [18]
- [ ] Use structured postmortem data as the shared factual record during incident retrospectives — replace narratives with data [18] [19]
- [ ] Practice blameless postmortems with concrete action items, owners, and deadlines tracked to completion [19]

## Phase 5: Sampling, Cost, & Steady State

- [ ] Implement dynamic sampling: sample boring, healthy traffic aggressively; keep interesting/erroring traffic at high fidelity [18]
- [ ] Ensure log rotation, metric retention, and trace storage have bounded retention policies — unbounded growth is a production incident [17]
- [ ] Verify no resource grows without bound: check disk, memory, connection pools, queue depths, and log volumes for steady-state stability [17]
- [ ] Confirm telemetry pipelines (OTel Collector, Fluentd, etc.) are monitored themselves — observability infrastructure is also infrastructure [18]
- [ ] When evaluating agent/AI system telemetry, account for infrastructure noise — 6-point benchmark swings from config alone [a12]

## Phase 6: Deploy-and-Observe Culture

- [ ] Adopt observability-driven development: deploy, then verify the feature works by querying production telemetry — not just tests [18]
- [ ] Accompany every deploy with active observation of latency distributions, error rates, and SLO burn for the first minutes [18]
- [ ] Use feature flags to decouple deployment from release — canary with metric-based promotion or rollback [32]
- [ ] Integrate deployment frequency, lead time, MTTR, and change failure rate as organizational health metrics [32]
- [ ] Ensure continuous production monitoring, not just pre-deployment testing — pre-deploy evals alone miss real-world degradation [a15]

## Key Questions to Ask

1. "Can we ask arbitrary questions about production behavior without deploying new instrumentation?" — the observability litmus test [18]
2. "What are the SLIs, SLOs, and error budget for this service?" — if undefined, reliability is undefined [19]
3. "What happens when this dependency is slow, down, or returns garbage?" — every integration point [17]
4. "What grows without bound, and how is it cleaned up?" — steady-state analysis [17]
5. "If this alert fires, what is the documented response?" — alerts without runbooks cause fatigue [19]
6. "What changed?" — the single most productive question during incident response [19]
7. "Is our sampling strategy capturing the interesting traffic or just the common traffic?" [18]

## Anti-Patterns

| Anti-Pattern | Why It Fails | Source |
|---|---|---|
| Dashboards without SLOs | No definition of "good" means no signal when things degrade | [19] |
| Unstructured log strings as primary telemetry | Cannot slice, group, or query by dimensions — only good for grep | [18] |
| Alerts on causes (CPU > 90%) instead of symptoms | CPU spikes may be benign; user-facing errors may occur at low CPU | [19] |
| Missing timeouts on outbound calls | A hung dependency holds threads indefinitely, causing cascading failure | [17] |
| Monitoring the app but not the monitoring | Telemetry pipeline failures create silent blind spots | [18] |
| "Three pillars" as separate silos | Logs, metrics, traces in isolation cannot answer cross-cutting questions | [18] |
| Treating observability as a tool purchase | The system is observable because you instrumented it, not because you bought a product | [18] |
| Pre-deploy testing only, no production monitoring | Real-world issues are missed by evals; user feedback and production telemetry are essential | [a15] |
