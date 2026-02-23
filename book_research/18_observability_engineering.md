# Observability Engineering — Majors, Fong-Jones & Miranda (2022)

**Skill Category:** Observability & Monitoring
**Relevance to AI-assisted / vibe-coding workflows:** Defines the modern standard for production observability — helps agents think beyond basic logging to structured events, distributed tracing, and actionable telemetry. When an AI assistant generates code that will run in production, the observability mindset ensures that code is *born instrumented* — emitting the rich, structured context needed to debug novel failures without having predicted them in advance.

---

## What This Book Is About

*Observability Engineering* is the definitive practitioner's guide to building systems you can understand in production — not through dashboards you pre-configured, but through the ability to ask arbitrary new questions of your running systems without deploying new code. Written by three authors deeply embedded in the observability movement (Charity Majors, co-founder and CTO of Honeycomb; Liz Fong-Jones, principal developer advocate at Honeycomb and former Google SRE; George Miranda, product and developer relations leader), the book codifies what "observability" actually means as an engineering discipline distinct from traditional monitoring.

The book covers:
- **Part I — The Path to Observability:** What observability is and isn't, how it differs from monitoring, and why the shift matters for modern distributed systems.
- **Part II — Fundamentals of Observability:** Structured events, high-cardinality/high-dimensionality data, the role of wide events, and how to think about instrumentation.
- **Part III — Observability for Teams:** How to embed observability into engineering culture — SLOs, incident response, debugging workflows, and organizational patterns.
- **Part IV — Observability at Scale:** OpenTelemetry, sampling strategies, pipelines, cost management, and the practical realities of running observability infrastructure.

The book is explicitly *not* a product manual for Honeycomb. It is vendor-neutral and principles-first, though its philosophical orientation clearly reflects the Honeycomb worldview (which the authors would argue *is* the correct worldview for modern systems).

---

## Key Ideas & Mental Models

### 1. Observability Is a Property of Systems, Not a Product You Buy

The central thesis: **observability is the ability to understand the internal states of a system by examining its external outputs.** This is borrowed from control theory. A system is "observable" when you can determine what is happening inside it — including novel, never-before-seen failure modes — from the telemetry it produces. This is fundamentally different from monitoring, which checks for *known* failure conditions.

The key question observability answers: **"Why is the system behaving this way for this specific user/request/cohort?"** — not just "is the system up?"

### 2. Structured Events Over Logs

Traditional logs are unstructured strings. The book argues forcefully for **structured events** — wide, rich, machine-parseable data blobs that capture *everything relevant about a unit of work* (a request, a function call, a job execution) in a single record. A structured event might contain 200-500 fields: user ID, tenant, feature flags, request path, database query times, cache hit/miss, payload sizes, retry counts, error messages, build SHA, and so on.

The key insight: **the wider the event, the more questions you can answer later without re-deploying instrumentation.** You are capturing the *context* of work, not just the outcome.

### 3. The "Three Pillars" Critique

The industry popularized the idea that observability consists of three pillars: **logs, metrics, and traces**. The book explicitly challenges this framing:

- **Metrics** are pre-aggregated, low-cardinality summaries. They tell you *that* something is wrong but not *why*. They lose the individual event context. You cannot drill down from a metric to a specific request.
- **Logs** (in traditional form) are unstructured, expensive to store at volume, and difficult to correlate across services. They are a *symptom* of poor instrumentation, not a foundation for observability.
- **Traces** are the most structurally useful of the three, but traces alone are not sufficient — they show the shape of a request's path but need rich contextual data attached to each span.

The authors' position: **the three pillars are an accident of history, not a principled architecture.** They represent three *legacy data types* that existed before anyone thought carefully about what data you actually need. The real foundation is **arbitrarily wide structured events** that can be sliced, diced, grouped, and filtered along any dimension. Traces are events with parent-child relationships. Metrics can be derived from events. Logs are just poorly structured events.

### 4. High-Cardinality and High-Dimensionality Data

This is the book's most technically consequential argument:

- **Cardinality** = the number of unique values a field can take. User ID is high-cardinality (millions of values). HTTP status code is low-cardinality (a few dozen values). Traditional monitoring systems (Prometheus, StatsD, Graphite) choke on high-cardinality dimensions because they pre-aggregate into time series — and the number of time series explodes combinatorially.
- **Dimensionality** = the number of fields/columns you can query across. Traditional monitoring limits you to a handful of tag dimensions. Real debugging requires querying across *hundreds* of dimensions simultaneously.

The central claim: **most real production bugs require high-cardinality, high-dimensionality data to diagnose.** The user ID, the specific endpoint, the build version, the feature flag combination, the particular database shard — these are the dimensions that matter, and they are all high-cardinality. Systems that cannot handle high-cardinality data *fundamentally cannot provide observability.*

### 5. "Debugging with Data You Didn't Know You'd Need"

This phrase, attributed to Charity Majors and used throughout the book, captures the core value proposition. In a complex distributed system, you cannot predict which questions you will need to ask during an incident. Traditional monitoring requires you to define alerts and dashboards for *anticipated* failure modes. Observability means you can explore *unanticipated* failures by querying your telemetry in novel ways — grouping by dimensions you never thought to check, filtering to cohorts you never expected to isolate.

The practical test: **can an engineer who has never seen this system before debug a novel production issue using only the telemetry the system emits?** If yes, the system is observable. If they need to add logging, redeploy, and reproduce the issue — it is not.

### 6. Observability Is Not Monitoring (But You Still Need Monitoring)

The book draws a clear line:
- **Monitoring** = checking known conditions. Is CPU above 90%? Is error rate above 1%? Is the queue depth growing? Monitoring answers: "Is the thing I predicted might go wrong actually going wrong?"
- **Observability** = exploring unknown conditions. Why are 3% of requests from tenant X on build Y in region Z taking 10x longer than normal? Observability answers: "What is going wrong, and why, when I have no prior hypothesis?"

Monitoring is a *subset* of observability. You still need alerts, SLOs, and dashboards. But monitoring alone is insufficient for modern distributed systems where the failure space is combinatorially vast.

### 7. SLOs as the Bridge Between Observability and Business Outcomes

The book devotes significant attention to **Service Level Objectives (SLOs)** as the mechanism that connects observability data to business decisions:
- SLOs define what "good" looks like from the user's perspective (e.g., "99.9% of requests complete in under 300ms").
- **Error budgets** — the tolerable amount of unreliability — determine when to invest in reliability vs. features.
- SLOs should be measured from observability data, not synthetic checks. They should reflect *real user experience*.
- When the error budget is being consumed, that is when you investigate — and observability data is *how* you investigate.

### 8. The Core Analysis Loop

The book describes a specific debugging workflow enabled by observability:

1. **Start with a signal** — an SLO burn rate alert, a customer complaint, a hunch.
2. **Look at the high-level distribution** — what does the overall latency/error distribution look like?
3. **Slice by dimensions** — group by endpoint, user, region, build, feature flag. Look for the dimension that *separates the good from the bad.*
4. **Drill into specific events** — once you have identified the problematic cohort, examine individual request traces with full context.
5. **Form and test hypotheses** — use the data to confirm or refute your theory, iteratively narrowing.

This is **exploratory data analysis applied to production systems**, and it requires the high-cardinality, high-dimensionality data the book advocates.

---

## Patterns & Approaches Introduced

### Instrumentation Patterns

- **Wide events / rich context propagation:** Instrument at the boundaries of meaningful work units. Attach *all* relevant context to each event — request metadata, user context, infrastructure details, feature flags, timing breakdowns. Prefer one wide event over many narrow log lines.
- **Trace context propagation:** Ensure distributed trace IDs flow through every service, queue, and async boundary. Use W3C Trace Context or B3 propagation headers. This is what turns isolated events into connected stories.
- **Span events and span attributes:** Within a trace, each span should carry rich attributes. Add custom attributes liberally — they are cheap to add and invaluable during debugging.
- **Instrumentation as a first-class engineering concern:** Treat instrumentation code with the same rigor as application code. Review it in PRs. Test it. Budget time for it. It is not an afterthought.

### Sampling Strategies

The book addresses the cost problem head-on. You cannot afford to store every event forever. Sampling strategies include:
- **Head sampling:** Decide at the start of a request whether to sample it. Simple but loses interesting rare events.
- **Tail sampling:** Decide after the request completes, based on its characteristics (was it slow? did it error?). More useful but harder to implement at scale.
- **Dynamic sampling:** Adjust sampling rates based on traffic patterns — sample common, healthy requests at low rates and rare, interesting, or erroring requests at high rates. This is the book's preferred approach.
- **The key principle:** Sample *boring* traffic aggressively; keep *interesting* traffic at high fidelity.

### Organizational Patterns

- **Observability-driven development (ODD):** Before shipping a feature, add instrumentation. After deploying, verify the feature works by querying production telemetry — not just by running tests. "If you can't see it in production, you didn't ship it."
- **Deploy and observe:** Replace the "deploy and pray" pattern. Every deploy should be accompanied by active observation of production telemetry for the first few minutes. Look for changes in latency distributions, error rates, and SLO burn rates.
- **Blameless incident review grounded in data:** Use observability data as the shared factual record during incident retrospectives. Replace "I think what happened was..." with "the data shows that at 14:32, requests from build abc123 to endpoint /foo started timing out because dependency Y's p99 latency spiked to 8s."

### OpenTelemetry

The book dedicates substantial coverage to **OpenTelemetry (OTel)** as the vendor-neutral instrumentation standard:
- OTel provides **APIs and SDKs** for generating traces, metrics, and logs in a standardized format across languages.
- OTel provides **the Collector**, a pipeline component for receiving, processing, and exporting telemetry data to any backend.
- The book advocates OTel as the correct abstraction layer: **instrument once with OTel, export to any backend.** This decouples instrumentation from vendor choice.
- OTel's **auto-instrumentation** libraries provide baseline coverage for common frameworks (HTTP servers, database clients, gRPC) without manual code changes.
- The book acknowledges OTel was still maturing at publication time (traces were stable, metrics were stabilizing, logs were early) but positions it as the clear future standard.
- Practical guidance: start with auto-instrumentation for baseline coverage, then add custom spans and attributes for business-specific context. The custom instrumentation is where the real value lies.

---

## Tradeoffs & Tensions

### Cost vs. Resolution

Observability data is expensive. Wide events with hundreds of fields, stored for weeks or months, at scale, cost real money. The book acknowledges this tension and addresses it through sampling and retention strategies, but does not pretend it is free. Organizations must make deliberate choices about what to keep, at what resolution, for how long.

**The tradeoff:** Higher fidelity data enables faster debugging and more confident deploys, but at higher storage and processing cost. The book argues the ROI is positive — incidents are shorter, deploys are safer, and engineers spend less time guessing — but the upfront cost is real.

### Structured Events vs. the Existing Ecosystem

Most organizations have existing investments in traditional logging (ELK stack), metrics (Prometheus/Grafana), and APM (Datadog, New Relic, Dynatrace). The book's vision of wide structured events as the primary telemetry type is philosophically clean but practically disruptive. Migrating from three separate pillar-based systems to a unified event-based approach is a significant undertaking.

**The tension:** The book presents the ideal end-state but the migration path from "we have Prometheus and ELK" to "we have a unified observability platform built on structured events" involves organizational change, tooling changes, and a potentially long transition period where both old and new systems coexist.

### Vendor-Neutral Principles vs. Honeycomb's Worldview

The authors are transparent about their affiliations. The book's philosophy — wide events, high-cardinality exploration, BubbleUp-style group-by analysis — maps closely to Honeycomb's product capabilities. This is not dishonest (the authors built Honeycomb *because* they hold these beliefs), but readers should be aware that the "pure" observability vision as defined here is easier to implement with certain tools than others. Prometheus, for example, is structurally incapable of high-cardinality analysis; Datadog and Splunk can do some of it but with different tradeoffs.

### Sampling Fidelity vs. Completeness

Tail sampling and dynamic sampling are powerful but add complexity. Tail sampling requires buffering complete traces before making a decision, which has latency and memory implications. Dynamic sampling requires tuning sample rates, which is its own operational burden. And any sampling means you *might* miss the one weird request that held the clue.

### Cultural Change

The book's deepest tradeoff is human, not technical. Adopting observability-driven practices requires engineers to change how they think about production. Instead of "write code, throw it over the wall to ops, add logging when something breaks," the model is "instrument as you code, observe your deploys, own your services in production." This is a significant cultural shift that the book advocates passionately but cannot implement for you.

---

## What to Watch Out For

### The Purity Trap
The book can inspire a "burn it all down" mentality toward existing monitoring infrastructure. In practice, most organizations need a pragmatic migration path. You can adopt structured events and tracing incrementally while keeping existing metrics and dashboards running. Do not let the perfect be the enemy of the good.

### Instrumentation Discipline Drift
The book emphasizes rich instrumentation, but in practice, maintaining high-quality instrumentation across a large codebase requires ongoing discipline. Without code review standards and team norms, instrumentation degrades over time — fields go stale, new services ship without spans, context propagation breaks at async boundaries.

### Over-Indexing on Tooling
The book is about *principles*, not products. Teams that read the book and conclude "we need to buy Honeycomb" are missing the point. The question is: does your telemetry allow you to ask arbitrary questions about production behavior? You can make progress toward this with many different tools — the mental model matters more than the vendor.

### Sampling Gotchas
Dynamic sampling is powerful but requires understanding. Engineers unfamiliar with sampling may be confused when "their" request does not appear in the observability tool, or when counts seem off. Education about sampling and its implications is essential when rolling out these practices.

### Complexity of Distributed Tracing
Distributed tracing sounds simple in concept but is operationally demanding. Context propagation breaks at language boundaries, async job queues, message brokers, and legacy services. The book covers this but the implementation reality is harder than the theory. Expect to invest significantly in propagation plumbing.

### Log-to-Event Migration Is Gradual
Organizations with millions of lines of `log.info("processing order %s", orderId)` cannot switch to structured events overnight. The practical path is: start new services with structured events, retrofit critical paths in existing services, and gradually reduce reliance on unstructured logs. The book could be clearer about this migration reality.

---

## Applicability by Task Type

### Architecture Planning (Observability Strategy)
**Extremely high applicability.** This is the book's primary use case. When designing a new system or evolving an existing one, the book provides the mental framework for deciding: what telemetry to emit, how to propagate context, where to place instrumentation boundaries, how to handle sampling, and how to structure SLOs. An AI assistant helping with architecture decisions should apply these principles: ensure every service boundary has trace propagation, every meaningful operation emits a structured event, and the system is designed to be queryable along high-cardinality dimensions.

### Feature Design (Instrumentation Design)
**High applicability.** Every new feature should include an instrumentation plan. The book's guidance: before writing the feature, decide what questions you would want to ask about it in production. What dimensions matter? What timings should be captured? What context should be attached to events? Then implement the instrumentation *alongside* the feature code. An AI assistant generating feature code should automatically include relevant span creation, attribute attachment, and context propagation.

### Code Review (Logging and Tracing Quality)
**High applicability.** The book provides clear criteria for reviewing instrumentation quality:
- Are events structured (key-value) rather than freeform strings?
- Are trace spans properly created and closed, including in error paths?
- Is relevant context (user ID, request ID, feature flags, etc.) attached to events?
- Are custom attributes meaningful and named consistently?
- Is context propagation maintained across async boundaries?
- Are log levels used intentionally (not everything at INFO)?
An AI reviewing code should flag: unstructured log statements where structured events would serve better, missing span creation for significant operations, broken context propagation, and missing error attributes on spans.

### Bug Diagnosis
**Core use case.** The book's entire debugging methodology (the core analysis loop described above) applies directly. When diagnosing a bug:
1. Start from the observable symptom (SLO violation, error spike, latency change).
2. Use high-cardinality grouping to isolate the affected cohort.
3. Compare the affected cohort to the healthy baseline.
4. Drill into specific traces to understand the causal chain.
5. Form hypotheses and test them against the data.

An AI assistant helping with bug diagnosis should prompt engineers to query along these dimensions rather than jumping to code inspection.

### Production Incident Response
**Core use case.** The book's incident response philosophy:
- Use SLO burn rate alerts as the primary signal, not threshold-based alerts on system metrics.
- During an incident, use observability data to quickly identify *what changed* — new deploy? traffic pattern shift? dependency degradation?
- Use trace data to identify which specific service or dependency is causing the issue.
- Use wide events to understand *why* — what is different about the failing requests compared to the succeeding ones?
- After the incident, use the same data for blameless retrospectives grounded in facts rather than narratives.

---

## Relationship to Other Books in This Category

### Complements: *Site Reliability Engineering* (Google SRE Book, 2016)
The Google SRE book established SLOs, error budgets, and the reliability engineering discipline. *Observability Engineering* builds on that foundation but challenges the SRE book's implicit assumption that monitoring (dashboards, alerts, predefined checks) is sufficient. The observability book argues that SRE *goals* (reliability, error budgets) are correct but the *instrumentation approach* needs to evolve beyond traditional monitoring to handle modern distributed systems.

### Complements: *Distributed Systems Observability* by Cindy Sridharan (2018)
Sridharan's shorter work (originally an O'Reilly report) introduced many of the same themes — the limitations of the three pillars, the importance of context propagation, and the distinction between monitoring and observability. *Observability Engineering* goes deeper, with more practical guidance on implementation, organizational change, and the OpenTelemetry ecosystem. Sridharan's work is a good appetizer; Majors et al. is the full meal.

### Complements: *Designing Data-Intensive Applications* by Martin Kleppmann (2017)
Kleppmann's book explains *why* modern systems are hard to reason about — distributed state, eventual consistency, partial failures. *Observability Engineering* explains *how* to regain understanding of those systems in production. They are natural companions: Kleppmann tells you what can go wrong; Majors et al. tell you how to see what is going wrong.

### Contrasts with: *The Art of Monitoring* by James Turnbull (2016)
Turnbull's book is an excellent guide to traditional monitoring — Prometheus, Graphite, StatsD, alerting strategies. *Observability Engineering* explicitly positions itself as the *next step* beyond this approach. The Art of Monitoring is valuable for understanding metrics-based monitoring; *Observability Engineering* argues for transcending that model. They represent different generations of thinking.

### Complements: *Accelerate* by Forsgren, Humble & Kim (2018)
*Accelerate* demonstrates that deployment frequency, lead time, MTTR, and change failure rate predict organizational performance. *Observability Engineering* provides the instrumentation strategy that makes fast MTTR and confident high-frequency deploys *possible*. You cannot deploy 10 times a day safely without observability. The books share a worldview: ship fast, detect fast, recover fast.

### Complements: *Release It!* by Michael Nygard (2007/2018)
Nygard's stability patterns (circuit breakers, bulkheads, timeouts) create resilient systems. *Observability Engineering* provides the telemetry to *verify* those patterns are working in production and to detect when they are not. Nygard tells you how to build resilient systems; Majors et al. tell you how to see whether they are actually being resilient.

---

## Freshness Assessment

**Publication date:** June 2022
**Assessed as of:** February 2026

### What Remains Current
- **Core philosophy:** The distinction between monitoring and observability, the primacy of structured events, the importance of high-cardinality data, and the debugging-with-unknown-questions mental model are timeless principles. These have only become more accepted since publication.
- **SLO-based approach:** SLOs and error budgets as the bridge between engineering and business continue to be best practice.
- **Cultural guidance:** The organizational patterns (observability-driven development, deploy-and-observe, blameless retrospectives grounded in data) remain fully relevant.
- **OpenTelemetry direction:** The book's bet on OTel as the standard has been thoroughly validated. OTel has become the dominant instrumentation standard, with traces, metrics, and logs all reaching stability.

### What Has Evolved Since Publication
- **OpenTelemetry maturity:** At publication time, OTel logs were still early-stage. By 2025-2026, OTel logs are stable and widely adopted. The OTel Collector ecosystem has matured significantly with more processors, connectors, and exporters.
- **AI/ML observability:** The book predates the LLM explosion. Observability for AI workloads — tracking token usage, model latency, prompt/response quality, hallucination rates, embedding drift — is a rapidly growing concern not covered in the book.
- **eBPF-based observability:** Tools like Pixie (acquired by New Relic), Cilium Hubble, and Grafana Beyla use eBPF for low-overhead, auto-instrumented observability without code changes. This approach was nascent in 2022 and has matured considerably.
- **Observability pipelines:** The market for telemetry pipelines (Cribl, Mezmo, observability features in vector/fluentbit) has grown substantially, addressing the cost management challenges the book raises.
- **Continuous profiling:** Continuous profiling (Pyroscope, Grafana Pyroscope, Datadog Continuous Profiler) as a "fourth signal" alongside traces, metrics, and logs has gained traction since publication.
- **Vendor landscape:** Grafana's open-source stack (Tempo for traces, Loki for logs, Mimir for metrics, with TraceQL for trace querying) has become a credible alternative to the approach the book describes, offering high-cardinality trace analysis in an open-source context.

### Verdict
The book's core principles are **durably relevant** and will remain so for years. The specific tooling landscape has evolved, but the mental models are sound. Supplement with current OTel documentation and awareness of eBPF-based and AI observability developments.

---

## Key Framings Worth Preserving

> **"Observability is about being able to ask arbitrary questions about your production environment without having to know those questions in advance."**

This is the single most important sentence in the book. It distinguishes observability from monitoring more clearly than any other formulation.

---

> **"Your system is not observable because you bought an observability tool. Your system is observable because you instrumented it to be."**

Observability is an engineering discipline, not a purchasing decision. The tool is necessary but not sufficient; the instrumentation is what creates the property.

---

> **"The three pillars of observability are an accident of history, not a deliberate design."**

Logs, metrics, and traces exist because they were invented independently by different communities. The principled approach is to start from the question "what data do I need to debug my system?" and work backward — which leads to wide structured events, not three separate data types.

---

> **"High-cardinality data is the sine qua non of observability."**

If you cannot query by user ID, request ID, build version, or feature flag combination, you cannot debug real production issues. Systems that restrict you to low-cardinality dimensions (as most metrics systems do) are monitoring systems, not observability systems.

---

> **"The best time to add instrumentation is when you're writing the code. The second best time is now."**

Instrumentation is not a separate phase or a separate team's job. It is part of writing production-quality code.

---

> **"Observability-driven development: write instrumentation first, deploy, then verify your feature works by querying production — not just by running tests."**

Testing tells you the code does what you intended. Observability tells you the code does what you intended *in the real world, under real conditions, for real users.*

---

> **"You should be able to hand a new engineer your observability tools and they should be able to debug a novel production issue without prior knowledge of the system."**

This is the practical litmus test for observability. If debugging requires tribal knowledge rather than data exploration, your system is not observable.

---

> **"Monitoring tells you whether a system is working. Observability lets you ask why it isn't."**

The crispest summary of the monitoring-vs-observability distinction.

---

> **"Events are the atoms of observability. Everything else — metrics, traces, logs — can be derived from events, but events cannot be reconstructed from the others."**

This establishes the data model hierarchy: structured events are the primitive; other telemetry types are views or aggregations of events.

---

> **"Ship, observe, iterate. If you can't observe it, you haven't shipped it."**

Production is the ultimate test environment. Code that is deployed but not observable is code you have lost control of.

---

*This reference synthesizes the book's content with the authors' extensive public writing (particularly Charity Majors' blog at charity.wtf and her prolific social media presence), conference talks (QCon, SREcon, Monitorama, KubeCon), and the broader observability discourse as it stood through mid-2025. The book remains the single best starting point for teams transitioning from monitoring-centric to observability-centric practices.*
