# Book Research Prompt Library
## For Building Skill Reference Documents

**How to use:** Run each prompt in a Claude session with web search enabled.
The agent will combine its training knowledge with online research (articles,
summaries, author talks, YouTube transcripts, reviews) to build a reference doc.
You do NOT need the full book text.

**Tone goal:** Neutral and advisory. Surfaces considerations and tradeoffs,
not mandates. Flags where context matters and where reasonable practitioners disagree.

---

## MASTER PROMPT TEMPLATE
*(Pre-filled versions for each book follow below)*

```
Research the book "[TITLE]" by [AUTHOR] ([YEAR]) to build a practical
reference document for the skill category: [SKILL CATEGORY].

Use both your training knowledge AND online research — summaries, reviews,
author talks, YouTube videos, blog posts, and articles referencing this book.
You do NOT need the full book text.

Structure your output as follows:

---
# [Book Title] — [Author] ([Year])
**Skill Category:** [category]
**Relevance to AI-assisted / vibe-coding workflows:** [1-2 sentences]

## What This Book Is About
2-3 sentences on the core problem it addresses and its intended audience.

## Key Ideas & Mental Models
The 6-10 most influential ideas from this book. For each:
- Name the concept
- Explain it neutrally in 3-5 sentences
- Note when it applies well — and when it may NOT apply

## Patterns & Approaches Introduced
Techniques, frameworks, or methods the book advocates.
Present these as options with context, not mandates.
Note any prerequisites, constraints, or scale assumptions.

## Tradeoffs & Tensions
Where does the book acknowledge tradeoffs?
Where do practitioners or the broader community disagree with its recommendations?
What has aged or been challenged since publication?

## What to Watch Out For
Anti-patterns the book identifies.
Frame as "tends to cause problems when..." rather than absolute rules.

## Applicability by Task Type
For each relevant task below, note what from this book is most useful:
- Architecture planning
- Code / API design
- Code review
- Feature design on existing systems
- Bug diagnosis & fixing
- Writing technical documentation
- Data modeling
[Remove irrelevant tasks, add others specific to this book]

## Relationship to Other Books in This Category
Where does it agree, extend, or conflict with other well-known books
on [SKILL CATEGORY]? Keep this brief — 3-5 comparisons max.

## Freshness Assessment
- Published: [year]
- Core ideas that remain highly relevant today:
- Ideas that may be context-specific or stack-specific:
- What the book predates or doesn't cover (e.g., LLMs, cloud-native, serverless):
- Anything the field has substantially moved on from:

## Key Framings Worth Preserving
3-5 short paraphrased ideas — memorable anchors that capture the book's
most distinctive contributions. These are good candidates for skill file distillation.
---

Keep the tone neutral and informative. Present options, not rules.
Where reasonable practitioners disagree, show both sides.
Where something is highly context-dependent, say so explicitly.
Aim for depth over breadth — better to explain 7 ideas well than list 20 shallowly.
```

---

## 🏗️ ARCHITECTURE & SYSTEM DESIGN

---

### 1. Designing Data-Intensive Applications

```
Research the book "Designing Data-Intensive Applications" by Martin Kleppmann (2017)
to build a practical reference document for the skill category: Architecture & System Design / Data Systems.

Use both your training knowledge AND online research — summaries, reviews,
author talks, YouTube videos, blog posts, and articles referencing this book.
You do NOT need the full book text.

Structure your output as follows:

---
# Designing Data-Intensive Applications — Martin Kleppmann (2017)
**Skill Category:** Architecture & System Design / Data Systems
**Relevance to AI-assisted / vibe-coding workflows:** Foundational for any
architecture planning involving databases, distributed systems, or data pipelines —
helps agents avoid naive storage and consistency decisions.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Architecture planning
- Data modeling & schema design
- API design
- Feature design on existing systems
- Bug diagnosis & fixing (especially data consistency bugs)
- Writing technical documentation

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Keep tone neutral. Emphasize the book's focus on tradeoffs and the CAP theorem /
consistency model discussions — these are the most practically useful for an AI
agent doing architecture work. Flag what has evolved with cloud-managed databases.
```

---

### 2. Fundamentals of Software Architecture

```
Research the book "Fundamentals of Software Architecture" by Mark Richards
and Neal Ford (2020) to build a practical reference document for the skill
category: Architecture & System Design.

Use both your training knowledge AND online research — summaries, reviews,
author talks, YouTube videos, blog posts, and articles referencing this book.
You do NOT need the full book text.

Structure your output as follows:

---
# Fundamentals of Software Architecture — Richards & Ford (2020)
**Skill Category:** Architecture & System Design
**Relevance to AI-assisted / vibe-coding workflows:** Best broad foundation
for helping agents understand architectural styles, quality attributes, and
how to reason about architectural decisions — not just implement patterns.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Architecture planning
- Feature design on existing systems
- Code review (architectural fitness)
- Writing technical documentation (ADRs)
- Team / component boundary design

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Pay special attention to: the architectural styles catalog (layered, event-driven,
microservices, etc.) with their tradeoffs, the concept of architectural
characteristics (quality attributes), and the "first law of software architecture"
framing. These are the most anchor-worthy concepts for an AI agent.
```

---

### 3. Software Architecture: The Hard Parts

```
Research the book "Software Architecture: The Hard Parts" by Neal Ford,
Mark Richards, Pramod Sadalage, and Zhamak Dehghani (2021) to build a
practical reference document for the skill category: Architecture & System Design
/ Distributed Systems.

Use both your training knowledge AND online research — summaries, reviews,
author talks, YouTube videos, blog posts, and articles referencing this book.
You do NOT need the full book text.

Structure your output as follows:

---
# Software Architecture: The Hard Parts — Ford, Richards, Sadalage, Dehghani (2021)
**Skill Category:** Architecture & System Design / Distributed Systems
**Relevance to AI-assisted / vibe-coding workflows:** Most useful when an AI
agent is designing or reviewing distributed systems — forces explicit tradeoff
reasoning rather than defaulting to microservices or monoliths uncritically.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Architecture planning (especially distributed/microservice decisions)
- Feature design on existing systems
- Data modeling in distributed contexts
- Code review at service boundary level
- Bug diagnosis in distributed systems

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Focus heavily on: the coupling vs cohesion analysis, data ownership patterns,
saga patterns for distributed transactions, and the "fitness function" concept.
These are the most distinctive and anchor-worthy ideas in the book.
```

---

### 4. Clean Architecture

```
Research the book "Clean Architecture: A Craftsman's Guide to Software Structure
and Design" by Robert C. Martin (2017) to build a practical reference document
for the skill category: Architecture & System Design / Code Design.

Use both your training knowledge AND online research — summaries, reviews,
author talks, YouTube videos, blog posts, and articles referencing this book.
You do NOT need the full book text.

Structure your output as follows:

---
# Clean Architecture — Robert C. Martin (2017)
**Skill Category:** Architecture & System Design / Code Design
**Relevance to AI-assisted / vibe-coding workflows:** Provides the most
explicit framework for thinking about dependency direction and boundary design —
helps agents avoid architectures where business logic bleeds into infrastructure.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Architecture planning
- Code / API design
- Feature design on existing systems
- Code review
- Bug diagnosis (tracing through layers)

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Emphasize: the dependency rule, the distinction between policies and details,
use cases as the center of architecture, and the plugin model for frameworks/DBs.
Also note where practitioners find the approach over-engineered for smaller systems —
this is important nuance for an AI agent that shouldn't apply Clean Architecture
uniformly to all project sizes.
```

---

### 5. Building Microservices (2nd ed.)

```
Research the book "Building Microservices" (2nd edition) by Sam Newman (2021)
to build a practical reference document for the skill category:
Architecture & System Design / Microservices.

Use both your training knowledge AND online research — summaries, reviews,
author talks, YouTube videos, blog posts, and articles referencing this book.
You do NOT need the full book text.

Structure your output as follows:

---
# Building Microservices (2nd ed.) — Sam Newman (2021)
**Skill Category:** Architecture & System Design / Microservices
**Relevance to AI-assisted / vibe-coding workflows:** Essential reference
when an agent is designing service decomposition, inter-service communication,
or data ownership — prevents common microservice anti-patterns.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Architecture planning
- API design (inter-service contracts)
- Data modeling (per-service data ownership)
- Feature design on existing systems
- Bug diagnosis in distributed systems
- Release & deployment strategy

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Pay attention to: service boundary identification (domain-driven), the
communication style tradeoffs (sync vs async), data decentralization challenges,
and the "monolith first" argument. Also note Sam Newman's own caveats about
when NOT to use microservices — this nuance is valuable for an AI agent.
```

---

### 6. A Philosophy of Software Design

```
Research the book "A Philosophy of Software Design" by John Ousterhout (2018,
2nd ed. 2021) to build a practical reference document for the skill category:
Code Design & Complexity Management.

Use both your training knowledge AND online research — summaries, reviews,
author talks (Stanford lectures available on YouTube), blog posts, and articles
referencing this book. You do NOT need the full book text.

Structure your output as follows:

---
# A Philosophy of Software Design — John Ousterhout (2018/2021)
**Skill Category:** Code Design & Complexity Management
**Relevance to AI-assisted / vibe-coding workflows:** Provides the clearest
articulation of what makes code complex and how to fight it — extremely useful
for code review and design tasks where agents tend to produce shallow modules.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Code / API design
- Code review
- Refactoring decisions
- Feature design on existing systems
- Writing technical documentation

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

This book is notably controversial in places (e.g., its stance on comments,
its critique of Clean Code's function length advice). Make sure to capture
those tensions honestly — where Ousterhout disagrees with Robert Martin and why.
The "deep modules vs shallow modules" distinction is the single most important
concept to extract.
```

---

## 🔒 SECURITY

---

### 7. The Web Application Hacker's Handbook (2nd ed.)

```
Research the book "The Web Application Hacker's Handbook" (2nd edition) by
Dafydd Stuttard and Marcus Pinto (2011) to build a practical reference document
for the skill category: Security / Web Application Security.

Use both your training knowledge AND online research — summaries, OWASP
documentation, articles, security blogs, and references to this book.
Note: this book is older; supplement with current OWASP Top 10 and
modern web security resources where the book may have gaps.

Structure your output as follows:

---
# The Web Application Hacker's Handbook (2nd ed.) — Stuttard & Pinto (2011)
**Skill Category:** Security / Web Application Security
**Relevance to AI-assisted / vibe-coding workflows:** Builds attacker mental
models that help an agent identify vulnerabilities during code review and
feature design — without this, agents tend to produce functionally correct
but insecure code.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced (attack categories and defenses)
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Code review (security lens)
- API design
- Feature design on existing systems
- Architecture planning (trust boundaries)
- Bug diagnosis (security bugs)

## Relationship to Other Books in This Category
## Freshness Assessment
*(Important: this book predates modern SPAs, JWT, OAuth 2.0 widespread
adoption, and serverless. Flag what is outdated and what the current
equivalents are.)*
## Key Framings Worth Preserving
---

Supplement with current OWASP Top 10 (2021 version) where the book has gaps.
Note what has changed in the threat landscape since 2011.
```

---

### 8. The Developer's Playbook for LLM Security

```
Research the book "The Developer's Playbook for Large Language Model Security"
by Steve Wilson (O'Reilly, 2024) to build a practical reference document for
the skill category: Security / AI & LLM Security.

Use both your training knowledge AND online research — reviews, author
interviews, OWASP LLM Top 10, and related security research.
This is a recent book so online coverage may be limited; supplement with
the OWASP Top 10 for LLM Applications and current AI security research.

Structure your output as follows:

---
# The Developer's Playbook for LLM Security — Steve Wilson (2024)
**Skill Category:** Security / AI & LLM Security
**Relevance to AI-assisted / vibe-coding workflows:** Directly relevant when
building AI-powered features — covers attack vectors unique to LLM systems
that traditional security resources don't address.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Architecture planning (AI systems)
- Feature design for LLM-powered features
- Code review of AI integrations
- Prompt design and system prompt hardening
- RAG pipeline security

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Make sure to cover: prompt injection (direct and indirect), data poisoning,
model inversion, insecure output handling, and the OWASP LLM Top 10.
This is the most immediately relevant security book for someone building
AI applications like a Cisco chatbot assistant.
```

---

## 🤖 LLM / AI ENGINEERING

---

### 9. AI Engineering — Chip Huyen

```
Research the book "AI Engineering: Building Applications with Foundation Models"
by Chip Huyen (O'Reilly, 2025) to build a practical reference document for
the skill category: LLM / AI Engineering.

Use both your training knowledge AND online research — reviews, author talks,
YouTube videos, blog posts, and the author's own writing (chip.huyen.com).
This is a very recent book so also incorporate current industry knowledge
on LLM application architecture.

Structure your output as follows:

---
# AI Engineering — Chip Huyen (2025)
**Skill Category:** LLM / AI Engineering
**Relevance to AI-assisted / vibe-coding workflows:** The most comprehensive
and current guide to building production LLM applications — directly applicable
to Control Hub AI Assistant-type systems.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Architecture planning (AI systems)
- Feature design for LLM-powered features
- Evaluation & testing of AI outputs
- Prompt design
- RAG pipeline design
- Deployment & monitoring of AI systems
- Cost vs latency optimization

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Prioritize: the evaluation framework (evals), RAG architecture patterns,
agent design, fine-tuning vs prompting decisions, and the operational
challenges of LLM systems. These are the most practically anchoring topics
for an AI coding agent working on AI features.
```

---

### 10. Designing Machine Learning Systems — Chip Huyen

```
Research the book "Designing Machine Learning Systems" by Chip Huyen
(O'Reilly, 2022) to build a practical reference document for the skill
category: LLM / AI Engineering / ML Systems.

Use both your training knowledge AND online research — reviews, author talks,
blog posts, and the author's writing. Note the distinction between this book
(ML systems design) and her 2025 AI Engineering book.

Structure your output as follows:

---
# Designing Machine Learning Systems — Chip Huyen (2022)
**Skill Category:** LLM / AI Engineering / ML Systems Design
**Relevance to AI-assisted / vibe-coding workflows:** Covers the production
system concerns that pure ML tutorials skip — data pipelines, monitoring,
drift, feature stores, and feedback loops.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Architecture planning (ML systems)
- Data modeling (feature engineering, training data)
- Feature design for ML-powered features
- Observability & monitoring of ML systems
- Bug diagnosis in ML pipelines

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Focus on: the data pipeline design, training-serving skew, concept drift monitoring,
and the human-in-the-loop design patterns. These are the most transferable
concepts for someone building AI applications rather than training models from scratch.
```

---

### 11. LLM Engineer's Handbook

```
Research the book "LLM Engineer's Handbook: Master the art of engineering
large language models from concept to production" by Paul Iusztin and
Maxime Labonne (Packt, 2024) to build a practical reference document for
the skill category: LLM / AI Engineering.

Use both your training knowledge AND online research — reviews, author GitHub
repos, blog posts, and related resources.

Structure your output as follows:

---
# LLM Engineer's Handbook — Iusztin & Labonne (2024)
**Skill Category:** LLM / AI Engineering
**Relevance to AI-assisted / vibe-coding workflows:** Hands-on engineering
guide covering the full LLM app stack — complementary to Huyen's more
theoretical treatment.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Architecture planning (LLM pipelines)
- RAG pipeline design and implementation
- Fine-tuning decisions
- Deployment patterns
- Prompt engineering

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
```

---

## 🧪 TESTING

---

### 12. Unit Testing: Principles, Practices, and Patterns

```
Research the book "Unit Testing: Principles, Practices, and Patterns" by
Vladimir Khorikov (Manning, 2020) to build a practical reference document
for the skill category: Testing.

Use both your training knowledge AND online research — reviews, author blog
(enterprisecraftsmanship.com), YouTube talks, and articles referencing this book.

Structure your output as follows:

---
# Unit Testing: Principles, Practices, and Patterns — Vladimir Khorikov (2020)
**Skill Category:** Testing
**Relevance to AI-assisted / vibe-coding workflows:** Provides the clearest
modern framework for what makes a good test — helps agents avoid writing tests
that are technically present but provide little value or are brittle.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Writing tests for new features
- Code review (evaluating test quality)
- Refactoring decisions
- Bug fixing (regression tests)
- Integration test vs unit test decisions

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Critical concepts to extract: the four pillars of a good unit test, the
distinction between London vs Classical schools of TDD, what to mock vs
not mock, the test pyramid vs test trophy debate, and the observable behavior
vs implementation detail distinction. These directly shape how an AI agent
should approach test generation.
```

---

### 13. Growing Object-Oriented Software, Guided by Tests

```
Research the book "Growing Object-Oriented Software, Guided by Tests" by
Steve Freeman and Nat Pryce (Addison-Wesley, 2009) to build a practical
reference document for the skill category: Testing / TDD.

Use both your training knowledge AND online research — reviews, author talks,
blog posts, and articles referencing this book.

Structure your output as follows:

---
# Growing Object-Oriented Software, Guided by Tests — Freeman & Pryce (2009)
**Skill Category:** Testing / TDD
**Relevance to AI-assisted / vibe-coding workflows:** The canonical text on
using tests to drive design — relevant when asking an agent to write tests
alongside code, not just after.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Test-driven feature development
- API design (tests as first consumer)
- Code review
- Refactoring

## Relationship to Other Books in This Category
## Freshness Assessment
*(Note: Java-centric and older — which concepts transfer well to Python/JS?)*
## Key Framings Worth Preserving
```

---

## ⚙️ ENGINEERING BEST PRACTICES

---

### 14. The Pragmatic Programmer (20th Anniversary Ed.)

```
Research the book "The Pragmatic Programmer" (20th Anniversary Edition) by
David Thomas and Andrew Hunt (Addison-Wesley, 2019) to build a practical
reference document for the skill category: Engineering Best Practices.

Use both your training knowledge AND online research — reviews, summaries,
author talks, blog posts, and articles referencing this book. Note differences
between original (1999) and 20th anniversary edition where relevant.

Structure your output as follows:

---
# The Pragmatic Programmer (20th Anniversary Ed.) — Thomas & Hunt (2019)
**Skill Category:** Engineering Best Practices
**Relevance to AI-assisted / vibe-coding workflows:** The broadest collection
of engineering wisdom in a single volume — useful as a general-purpose anchor
for good engineering judgment across all task types.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Architecture planning
- Code / API design
- Code review
- Feature design
- Bug diagnosis & fixing
- Writing technical documentation
- Career / engineering mindset

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Prioritize: DRY (and its limits), tracer bullets vs prototypes, broken windows
theory, the concept of good enough software, orthogonality, and the "don't
outrun your headlights" principle. These are the most durable and broadly
applicable ideas for anchoring an AI coding agent.
```

---

### 15. Clean Code

```
Research the book "Clean Code: A Handbook of Agile Software Craftsmanship"
by Robert C. Martin (2008) to build a practical reference document for the
skill category: Engineering Best Practices / Code Quality.

Use both your training knowledge AND online research — reviews, blog posts,
critiques (there are notable ones), and articles referencing this book.

Structure your output as follows:

---
# Clean Code — Robert C. Martin (2008)
**Skill Category:** Engineering Best Practices / Code Quality
**Relevance to AI-assisted / vibe-coding workflows:** Widely influential
standard for code readability and structure — useful as a code review anchor,
but important to also surface its known criticisms and limitations.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Code review
- Refactoring
- Code / API design
- Writing technical documentation (comments section)

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

IMPORTANT: This book has significant critics (including Ousterhout and others).
Be sure to capture the main counterarguments — especially around function length,
comment philosophy, and whether the advice scales to all contexts and languages.
An AI agent anchored only on Clean Code can produce over-abstracted, over-fragmented
code. Present this book as one important perspective, not the final word.
```

---

### 16. Refactoring (2nd ed.)

```
Research the book "Refactoring: Improving the Design of Existing Code"
(2nd edition) by Martin Fowler (Addison-Wesley, 2018) to build a practical
reference document for the skill category: Engineering Best Practices / Refactoring.

Use both your training knowledge AND online research — reviews, the refactoring.com
catalog, author talks, and articles referencing this book.

Structure your output as follows:

---
# Refactoring (2nd ed.) — Martin Fowler (2018)
**Skill Category:** Engineering Best Practices / Refactoring
**Relevance to AI-assisted / vibe-coding workflows:** Provides the vocabulary
and catalog for safe, incremental code improvement — essential for code review
and bug fix tasks where agents need to suggest improvements without breaking things.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced (key refactoring catalog items)
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Code review
- Bug fixing
- Feature design on existing systems
- Refactoring decisions
- Technical debt assessment

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

The most important thing to extract is the catalog structure itself — the
named refactorings with their mechanics. Also capture the "when to refactor"
heuristics and the relationship between refactoring and testing (you need
tests before you refactor safely). Note the shift to JavaScript in 2nd ed.
```

---

## 🚀 OBSERVABILITY, RELIABILITY & DEVOPS

---

### 17. Release It! (2nd ed.)

```
Research the book "Release It!: Design and Deploy Production-Ready Software"
(2nd edition) by Michael Nygard (Pragmatic Bookshelf, 2018) to build a
practical reference document for the skill category: Reliability / Production Engineering.

Use both your training knowledge AND online research — reviews, author talks,
blog posts, and articles referencing this book.

Structure your output as follows:

---
# Release It! (2nd ed.) — Michael Nygard (2018)
**Skill Category:** Reliability / Production Engineering
**Relevance to AI-assisted / vibe-coding workflows:** The most practically
useful book for production reliability patterns — agents almost never think
about failure modes without explicit anchoring from this kind of material.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Architecture planning (stability patterns)
- Feature design (failure mode consideration)
- Code review (production readiness)
- Bug diagnosis (cascading failures)
- Release & deployment strategy

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Must-capture patterns: circuit breakers, timeouts, bulkheads, back pressure,
retry with exponential backoff, and the concept of "let it crash" vs defensive
coding. Also capture the anti-patterns (the "chain reaction," "cascading failures,"
"blocked threads" patterns). These are directly encodable as code review checklist items.
```

---

### 18. Observability Engineering

```
Research the book "Observability Engineering: Achieving Production Excellence"
by Charity Majors, Liz Fong-Jones, and George Miranda (O'Reilly, 2022) to
build a practical reference document for the skill category: Observability & Monitoring.

Use both your training knowledge AND online research — reviews, author talks
(Charity Majors is prolific on Twitter/blog), YouTube videos, and articles.

Structure your output as follows:

---
# Observability Engineering — Majors, Fong-Jones & Miranda (2022)
**Skill Category:** Observability & Monitoring
**Relevance to AI-assisted / vibe-coding workflows:** Defines the modern
standard for production observability — helps agents think beyond basic
logging to structured events, distributed tracing, and actionable telemetry.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Architecture planning (observability strategy)
- Feature design (instrumentation design)
- Code review (logging and tracing quality)
- Bug diagnosis
- Production incident response

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Core concepts to extract: structured events vs logs, the three pillars
(logs/metrics/traces) and their limitations, high-cardinality data, the
difference between monitoring and observability, and "debugging with data
you didn't know you'd need." Also capture the OpenTelemetry story.
```

---

### 19. Site Reliability Engineering (Google)

```
Research the book "Site Reliability Engineering: How Google Runs Production
Systems" edited by Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall
Murphy (O'Reilly, 2016) to build a practical reference document for the
skill category: Reliability / SRE.

Use both your training knowledge AND online research — the book is freely
available at sre.google/sre-book — reviews, author talks, and the SRE
community's writing on how these concepts apply outside Google-scale.

Structure your output as follows:

---
# Site Reliability Engineering — Google (2016)
**Skill Category:** Reliability / SRE
**Relevance to AI-assisted / vibe-coding workflows:** Defines SLOs, error
budgets, and toil elimination — concepts that should inform any architecture
or feature design that has reliability implications.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Architecture planning (reliability targets)
- Feature design (SLO impact)
- Release & deployment strategy
- Bug diagnosis & postmortems
- Observability design

## Relationship to Other Books in This Category
## Freshness Assessment
*(Note: Google-scale assumptions. Flag what applies at smaller scales
and what requires significant adaptation.)*
## Key Framings Worth Preserving
---

Most transferable concepts: SLIs/SLOs/SLAs, error budgets, toil definition,
the on-call rotation philosophy, and the blameless postmortem culture.
Flag where the Google-scale context makes direct application unrealistic
for smaller teams.
```

---

## 🗄️ DATA MODELING & APIs

---

### 20. API Design Patterns

```
Research the book "API Design Patterns" by JJ Geewax (Manning, 2021) to
build a practical reference document for the skill category: API Design.

Use both your training knowledge AND online research — reviews, author talks,
the Google API Design Guide (aip.dev) which this book draws from, and
blog posts referencing this book.

Structure your output as follows:

---
# API Design Patterns — JJ Geewax (2021)
**Skill Category:** API Design
**Relevance to AI-assisted / vibe-coding workflows:** The most systematic
treatment of API design decisions — prevents agents from making ad-hoc
choices on versioning, pagination, errors, and resource naming.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- API design (primary)
- Architecture planning
- Code review of API endpoints
- Feature design (API surface changes)
- Writing technical documentation (API docs)

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Key areas to cover: resource naming conventions, standard methods vs custom methods,
partial updates (PATCH semantics), pagination patterns, long-running operations,
error response structures, versioning strategies, and backwards compatibility.
This book is Google-influenced — note where REST vs gRPC assumptions affect advice.
```

---

### 21. Database Internals

```
Research the book "Database Internals: A Deep Dive into How Distributed Data
Systems Work" by Alex Petrov (O'Reilly, 2019) to build a practical reference
document for the skill category: Data Modeling & Storage.

Use both your training knowledge AND online research — reviews, author talks,
and blog posts referencing this book.

Structure your output as follows:

---
# Database Internals — Alex Petrov (2019)
**Skill Category:** Data Modeling & Storage / Database Internals
**Relevance to AI-assisted / vibe-coding workflows:** Provides the "why"
behind database design decisions — helps agents make informed choices about
indexes, storage engines, and consistency that they'd otherwise make by cargo-cult.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Data modeling & schema design
- Architecture planning (storage layer)
- Performance optimization
- Bug diagnosis (data consistency issues)

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Focus on the practically applicable concepts: B-tree vs LSM-tree tradeoffs
(and when to choose each), write amplification, read/write path design, and
distributed consensus basics. This is a deep technical book — extract the
concepts that most directly impact everyday schema and storage decisions.
```

---

## ⚡ CONCURRENCY & ASYNC

---

### 22. Python Concurrency with asyncio

```
Research the book "Python Concurrency with asyncio" by Matthew Fowler
(Manning, 2022) to build a practical reference document for the skill
category: Concurrency & Async / Python.

Use both your training knowledge AND online research — reviews, Python
asyncio documentation, blog posts, and articles referencing this book.

Structure your output as follows:

---
# Python Concurrency with asyncio — Matthew Fowler (2022)
**Skill Category:** Concurrency & Async / Python
**Relevance to AI-assisted / vibe-coding workflows:** Directly applicable
to FastAPI development — agents regularly write async Python incorrectly
without this kind of anchoring.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Code / API design (async FastAPI endpoints)
- Code review (async correctness)
- Bug diagnosis (deadlocks, race conditions, blocking the event loop)
- Feature design for concurrent systems
- Performance optimization

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Critical concepts: the event loop model, coroutines vs threads vs processes,
when asyncio helps vs hurts (CPU-bound vs I/O-bound), common blocking mistakes
(blocking the event loop with sync code), and async context managers.
These directly apply to FastAPI work with Tortoise ORM.
```

---

## 🎨 UX & INTERACTION DESIGN

---

### 23. The Design of Everyday Things

```
Research the book "The Design of Everyday Things" (Revised & Expanded Edition)
by Don Norman (Basic Books, 2013) to build a practical reference document for
the skill category: UX & Interaction Design.

Use both your training knowledge AND online research — reviews, author talks,
YouTube summaries, design blog posts, and articles referencing this book.

Structure your output as follows:

---
# The Design of Everyday Things — Don Norman (2013)
**Skill Category:** UX & Interaction Design
**Relevance to AI-assisted / vibe-coding workflows:** The foundational
mental model for human-centered design — anchors agents to consider the
user's perspective, affordances, and error prevention in any UI task.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- UI / component design
- Feature design (user flow)
- Error handling design (user-facing)
- Usability review
- Information architecture

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Core concepts: affordances and signifiers, feedback and conceptual models,
the seven stages of action, error types (slips vs mistakes), and human-centered
design process. These are foundational and highly transferable to software UI design.
```

---

### 24. Don't Make Me Think (3rd ed.)

```
Research the book "Don't Make Me Think: A Common Sense Approach to Web and
Mobile Usability" (3rd edition) by Steve Krug (New Riders, 2014) to build a
practical reference document for the skill category: UX & Web Usability.

Use both your training knowledge AND online research — reviews, summaries,
author talks, and articles referencing this book.

Structure your output as follows:

---
# Don't Make Me Think (3rd ed.) — Steve Krug (2014)
**Skill Category:** UX & Web Usability
**Relevance to AI-assisted / vibe-coding workflows:** The most practical
and immediately applicable UX book — its principles directly translate
into UI code review criteria and feature design guidance.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- UI / component design
- Navigation & information architecture
- Feature design (user flows)
- Usability review
- Mobile design considerations

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Extract: the core "don't make me think" principle applied concretely, scanning
vs reading behavior, happy path design, the importance of visual hierarchy,
and the "trunk test" for navigation. Also Krug's usability testing philosophy
(hallway testing) is worth capturing.
```

---

### 25. Laws of UX

```
Research the book "Laws of UX: Using Psychology to Design Better Products
and Services" by Jon Yablonski (O'Reilly, 2020) to build a practical reference
document for the skill category: UX & Interaction Design / Cognitive Psychology.

Use both your training knowledge AND online research — the lawsofux.com website,
reviews, author talks, and articles referencing this book.

Structure your output as follows:

---
# Laws of UX — Jon Yablonski (2020)
**Skill Category:** UX & Interaction Design / Cognitive Psychology
**Relevance to AI-assisted / vibe-coding workflows:** The most directly
"agent-encodable" UX book — each law is a concrete principle with clear
application criteria, perfect for anchoring UI design and review tasks.

## What This Book Is About
## Key Ideas & Mental Models

[For each law, include: name, 1-sentence definition, when it applies,
and a concrete UI example. Cover at minimum: Fitts's Law, Hick's Law,
Miller's Law, Jakob's Law, Law of Proximity, Aesthetic-Usability Effect,
Peak-End Rule, Doherty Threshold, Tesler's Law, Zeigarnik Effect]

## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- UI / component design
- Navigation design
- Form design
- Loading / performance perception
- Feature complexity decisions

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

This book is particularly well-suited for direct distillation into a skill file
because each law is discrete and applicable. Make sure each law entry is
actionable — "Hick's Law means: when designing navigation menus, consider..."
```

---

## 📊 DATA VISUALIZATION

---

### 26. Storytelling with Data

```
Research the book "Storytelling with Data: A Data Visualization Guide for
Business Professionals" by Cole Nussbaumer Knaflic (Wiley, 2015) to build
a practical reference document for the skill category: Data Visualization.

Use both your training knowledge AND online research — reviews, author blog
(storytellingwithdata.com), YouTube talks, and articles referencing this book.

Structure your output as follows:

---
# Storytelling with Data — Cole Nussbaumer Knaflic (2015)
**Skill Category:** Data Visualization
**Relevance to AI-assisted / vibe-coding workflows:** The most practical
dataviz book for business/product contexts — directly applicable when an
agent generates plots, dashboards, or data slides.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Chart / plot generation
- Dashboard design
- Slide / presentation design
- Data storytelling in product docs
- Choosing chart types

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Key concepts: the importance of context, choosing the right chart, eliminating
clutter, focusing attention, thinking like a designer, and telling a story with
data. The "choose an effective visual" framework and the de-cluttering principles
are the most directly encodable into a dataviz skill file.
```

---

### 27. The Visual Display of Quantitative Information

```
Research the book "The Visual Display of Quantitative Information" (2nd edition)
by Edward Tufte (Graphics Press, 2001) to build a practical reference document
for the skill category: Data Visualization / Principles.

Use both your training knowledge AND online research — reviews, summaries,
design blog posts, and critiques of Tufte's principles where they exist.

Structure your output as follows:

---
# The Visual Display of Quantitative Information — Edward Tufte (2001)
**Skill Category:** Data Visualization / Foundational Principles
**Relevance to AI-assisted / vibe-coding workflows:** The foundational
aesthetic and intellectual framework for data visualization — provides the
"why" behind good chart design that agents otherwise lack.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Chart / plot generation
- Dashboard design
- Presentation / slide design
- Choosing visual encodings

## Relationship to Other Books in This Category
## Freshness Assessment
*(Note: predates interactive visualization and modern BI tools — flag what applies
to static charts vs interactive dashboards)*
## Key Framings Worth Preserving
---

Core concepts: data-ink ratio, chartjunk, small multiples, sparklines, and the
idea that graphical excellence is about showing data clearly. Also note where
Tufte's minimalism is occasionally taken too far (the "no gridlines ever" critique).
```

---

### 28. Fundamentals of Data Visualization

```
Research the book "Fundamentals of Data Visualization" by Claus O. Wilke
(O'Reilly, 2019 — freely available at clauswilke.com/dataviz) to build a
practical reference document for the skill category: Data Visualization.

Use both your training knowledge AND online research — the free online version,
reviews, and blog posts referencing this book.

Structure your output as follows:

---
# Fundamentals of Data Visualization — Claus Wilke (2019)
**Skill Category:** Data Visualization
**Relevance to AI-assisted / vibe-coding workflows:** The most comprehensive
modern guide to chart selection and visual encoding — covers color theory,
perception, and accessibility in ways other dataviz books skip.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Chart / plot generation
- Color palette selection
- Accessibility in visualizations (colorblind-friendly)
- Choosing between chart types
- Dashboard design

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Key areas: the chart type selection framework (what relationship are you showing?),
color theory for data (sequential vs diverging vs qualitative palettes), perceptual
principles, and accessibility (colorblind-safe palettes). The color section is
the most underrepresented topic in other dataviz books and should be captured fully.
```

---

## 📦 PRODUCT STRATEGY & FEATURE DESIGN

---

### 29. Inspired (2nd ed.) — Marty Cagan

```
Research the book "Inspired: How to Create Tech Products Customers Love"
(2nd edition) by Marty Cagan (Wiley, 2018) to build a practical reference
document for the skill category: Product Strategy & Feature Design.

Use both your training knowledge AND online research — reviews, author talks
(Silicon Valley Product Group blog), YouTube videos, and articles referencing this book.

Structure your output as follows:

---
# Inspired (2nd ed.) — Marty Cagan (2018)
**Skill Category:** Product Strategy & Feature Design
**Relevance to AI-assisted / vibe-coding workflows:** Provides the product
thinking framework that prevents agents from jumping straight to implementation —
useful for feature design, product doc, and architecture tasks.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Product documentation
- Feature design & scoping
- Architecture planning (product context)
- Stakeholder communication

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Key concepts: product discovery vs delivery, the empowered product team model,
product vs feature teams, outcome vs output thinking, opportunity assessment,
and the role of prototyping. Also capture the critique of the "feature factory"
anti-pattern — this is the most useful anchor for an AI agent that tends to
default to "here's the implementation" without questioning the problem.
```

---

### 30. Shape Up — Ryan Singer

```
Research the book "Shape Up: Stop Running in Circles and Ship Work that Matters"
by Ryan Singer (Basecamp, 2019 — freely available at basecamp.com/shapeup) to
build a practical reference document for the skill category: Product Strategy
& Feature Design.

Use both your training knowledge AND online research — the free online version,
reviews, author talks, and articles critiquing or extending this approach.

Structure your output as follows:

---
# Shape Up — Ryan Singer (2019)
**Skill Category:** Product Strategy & Feature Design
**Relevance to AI-assisted / vibe-coding workflows:** Introduces "appetite"
and fixed-time/variable-scope thinking — useful for scoping features and
writing product docs that acknowledge constraints and tradeoffs.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Feature scoping & design
- Product documentation
- Architecture planning (fit within appetite)
- Project estimation

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Key concepts: appetite (fixed time budget) vs estimate, shaping vs building,
fat marker sketches, breadboards, the betting table, and "circuit breaker"
for projects that run over. Also note where this model works best (small
autonomous teams) and where it doesn't translate well.
```

---

### 31. Continuous Discovery Habits

```
Research the book "Continuous Discovery Habits: Discover Products that Create
Customer Value and Business Value" by Teresa Torres (Product Talk, 2021) to
build a practical reference document for the skill category: Product Strategy
& User Research.

Use both your training knowledge AND online research — reviews, author blog
(producttalk.org), author talks, and articles referencing this book.

Structure your output as follows:

---
# Continuous Discovery Habits — Teresa Torres (2021)
**Skill Category:** Product Strategy & User Research
**Relevance to AI-assisted / vibe-coding workflows:** Provides the framework
for assumption-testing and opportunity mapping that prevents building the
wrong thing — useful for feature design tasks.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Feature design & scoping
- Product documentation
- User research framing
- Assumption identification before building

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

Key concepts: the opportunity solution tree, continuous interviewing, assumption
mapping, and experiment design. The opportunity solution tree is particularly
useful as a visual mental model for an AI agent doing feature planning.
```

---

## 🔁 DEVOPS & RELEASE

---

### 32. The DevOps Handbook

```
Research the book "The DevOps Handbook: How to Create World-Class Agility,
Reliability, and Security in Technology Organizations" (2nd edition) by
Gene Kim, Jez Humble, Patrick Debois, and John Willis (IT Revolution, 2016/2021)
to build a practical reference document for the skill category: DevOps & Release.

Use both your training knowledge AND online research — reviews, author talks,
YouTube videos, and articles referencing this book.

Structure your output as follows:

---
# The DevOps Handbook (2nd ed.) — Gene Kim et al. (2021)
**Skill Category:** DevOps & Release Engineering
**Relevance to AI-assisted / vibe-coding workflows:** Provides the cultural
and technical framework for fast, safe delivery — useful for deployment strategy,
CI/CD design, and understanding the operational context of features being built.

## What This Book Is About
## Key Ideas & Mental Models
## Patterns & Approaches Introduced
## Tradeoffs & Tensions
## What to Watch Out For

## Applicability by Task Type
- Release & deployment strategy
- Architecture planning (deployment topology)
- CI/CD pipeline design
- Feature design (feature flags, dark launches)
- Observability & feedback loops

## Relationship to Other Books in This Category
## Freshness Assessment
## Key Framings Worth Preserving
---

The three ways (flow, feedback, continuous learning) are the conceptual
spine of the book. Also extract: deployment pipeline design, feature flags
as a deployment tool, the relationship between trunk-based development and
deployment frequency, and the "shift left on security" concept.
```

---

*End of prompt library — 32 books across 10 skill categories.*

---

## SYNTHESIS PROMPT (run after completing a category)

```
I have research summaries for the following books in the [SKILL CATEGORY] category:
- [Book 1]
- [Book 2]
- [Book 3]

Using those summaries, synthesize a skill reference document for AI coding agents.

The goal is a guidance scaffold — NOT a rigid checklist. Help the agent raise
the right considerations for [SKILL CATEGORY] tasks, not mandate specific solutions.

Structure:
1. Why this category matters (what goes wrong when ignored)
2. Key considerations to raise (framed as questions or factors)
3. Common patterns and approaches — with tradeoffs for each
4. Tensions and context-dependence (where "it depends" is the honest answer)
5. Things that tend to cause problems (anti-patterns, framed softly)
6. Questions to ask before deciding (diagnostic prompts)

Tone: neutral, advisory. Where books agree, note consensus. Where they disagree,
present both views with context. Where something is highly context-dependent, say so.

Source books: [list]
Skill category: [category]
Last reviewed: [date]
```
