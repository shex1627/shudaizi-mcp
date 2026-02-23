# Clean Architecture — Robert C. Martin (2017)
**Skill Category:** Architecture & System Design / Code Design
**Relevance to AI-assisted / vibe-coding workflows:** Provides the most explicit framework for thinking about dependency direction and boundary design — helps agents avoid architectures where business logic bleeds into infrastructure. When an AI generates code, the dependency rule gives a single, mechanically-checkable invariant ("do source-code dependencies point inward?") that a reviewer — human or automated — can enforce without understanding the full domain.

---

## What This Book Is About

*Clean Architecture* synthesizes roughly four decades of software design thinking — Structured Design (Larry Constantine), Hexagonal Architecture (Alistair Cockburn, 2005), Onion Architecture (Jeffrey Palermo, 2008), DCI (James Coplien & Trygve Reenskaug), and BCE (Ivar Jacobson) — into a single, opinionated model. Martin's thesis: **the architecture of a software system is the shape given to that system by those who build it, and that shape should scream the intent of the system (its use cases), not the delivery mechanism (web, mobile, CLI) or the storage technology (SQL, NoSQL, filesystem).**

The book is organized in six parts:

1. **What is Design and Architecture?** — Argues there is no meaningful distinction between "design" and "architecture"; both are about the structure of the system at every level of detail.
2. **Programming Paradigms** — Surveys structured programming, object-oriented programming, and functional programming as disciplines that *remove* capabilities (goto, indirect transfer of control, assignment) rather than grant them. Each paradigm corresponds to a concern of architecture: sequence (structured), polymorphism/dependency inversion (OO), immutability/side-effect control (FP).
3. **Design Principles (SOLID)** — A mid-level chapter restating the five SOLID principles with an architectural lens, emphasizing how they govern the arrangement of functions and data into classes/modules.
4. **Component Principles** — Introduces principles for grouping code into deployable units: the Reuse/Release Equivalence Principle, the Common Closure Principle, the Common Reuse Principle; and for managing inter-component dependencies: the Acyclic Dependencies Principle, the Stable Dependencies Principle, the Stable Abstractions Principle.
5. **Architecture** — The core of the book. Presents the concentric-circles diagram, the Dependency Rule, use-case-driven design, and the concept of screaming architecture.
6. **Details** — Treats databases, the web, and frameworks as *details* that should be kept at the periphery.

The book also includes extended case studies (a video-sales system) and a chapter on the "missing chapter" by Simon Brown on how packaging models map to real directory/module structures.

---

## Key Ideas & Mental Models

### 1. The Dependency Rule

> Source code dependencies must point only inward, toward higher-level policies.

This is the single most important sentence in the book. In the concentric-circles diagram:

- **Entities** (innermost) — Enterprise-wide business rules, plain objects with no framework annotations, no ORM decorators, no HTTP awareness.
- **Use Cases** — Application-specific business rules. Orchestrate the flow of data to and from entities. Define input/output port interfaces.
- **Interface Adapters** — Convert data between the format most convenient for use cases/entities and the format required by external agencies (web, DB, devices). Controllers, presenters, gateways live here.
- **Frameworks & Drivers** (outermost) — The web framework, the database driver, the UI toolkit. This is glue code.

Nothing in an inner circle may know about — import, reference, name — anything in an outer circle. Data that crosses a boundary does so via simple data structures (DTOs, value objects), never via a row object from an ORM or a request object from a web framework.

**Mental model:** Think of the inner circles as a library that has no idea it is being hosted by a web server. If you can run your use cases from a test harness with no web server, no database, and no UI, you have honored the dependency rule.

### 2. Policies vs. Details

Martin draws a hard line:

| Policies | Details |
|----------|---------|
| Business rules | Database |
| Use case logic | Web framework |
| Domain entities | UI framework |
| Validation rules | Message queue |
| Authorization logic | File system |

The architecture should make the *policies* the most important, most visible, most stable part of the system. Details should be *plugins* that can be swapped without rewriting business logic.

### 3. The Plugin Model

Frameworks, databases, and delivery mechanisms should relate to the core system the way a plugin relates to a host application:

- The core defines interfaces (ports).
- External systems implement those interfaces (adapters).
- The core never references the adapter implementation; it references only the interface.
- The adapter depends on (imports) the interface definition from the core.

This is Dependency Inversion in action at the architectural scale. Martin calls it "the most important architectural principle."

### 4. Use Cases as the Center of Architecture

Architecture should be organized around *what the system does* (its use cases), not *how it is delivered*. When you look at the top-level directory structure of a system, you should see use case names — `PlaceOrder`, `ApproveExpenseReport`, `TransferFunds` — not framework names like `controllers/`, `models/`, `views/`.

Martin calls this **Screaming Architecture**: the architecture should "scream" its intent. A healthcare system's top-level structure should scream "healthcare," not "Rails" or "Spring."

### 5. Humble Objects

At every architectural boundary, the testability problem is solved by the Humble Object pattern: you split behavior into two parts — one that is hard to test (because it depends on something external) and one that is easy to test (pure logic). The hard-to-test part is made so humble (thin) that it barely needs testing.

Examples:
- A **Presenter** (testable) produces a ViewModel; a **View** (humble) just renders it.
- A **Gateway** interface is defined in the use-case layer; the **Gateway Implementation** (humble) is a thin wrapper around the ORM.

### 6. The Stable Abstractions Principle (SAP)

A component should be as abstract as it is stable. Stable components (many dependents) should consist mostly of interfaces and abstract classes. Volatile components (few dependents) should be concrete. This creates a system where change is easy: you modify concrete, unstable components without rippling through stable, abstract ones.

### 7. Boundaries and the Cost of Boundaries

Martin is explicit that every boundary has a cost — more interfaces, more data-transfer objects, more indirection. He distinguishes:

- **Full boundaries** — Separate compilable components on both sides, with interfaces and data structures.
- **One-dimensional boundaries** — A strategy pattern or a simple interface without the full reciprocal structure.
- **Facade boundaries** — A class that delegates to lower-level classes, without polymorphism.

The architect's job is to choose the right level of boundary formality for the current risk and anticipated change.

### 8. The Main Component

`Main` (or the composition root) is the outermost, dirtiest, most concrete component. It knows about everything. It wires the dependency injection. It is a plugin to the application — the lowest-level detail. In Clean Architecture, `Main` creates all the concrete implementations and injects them into the core.

---

## Patterns & Approaches Introduced

### Interactor Pattern (Use Case Interactor)
A use case is implemented as an object (the Interactor) that:
1. Accepts a Request Model (simple data structure) through an Input Port (interface).
2. Orchestrates entities and gateways.
3. Produces a Response Model (simple data structure) delivered through an Output Port (interface).

The Controller creates the Request Model, calls the Input Port, and the Presenter receives the Response Model via the Output Port.

### Port & Adapter (Hexagonal) Alignment
Clean Architecture is essentially Hexagonal Architecture with more prescriptive layering. The "ports" are the Input/Output Port interfaces; the "adapters" are controllers, presenters, gateways, and their implementations.

### Boundary-Crossing Data Structures
Data that crosses a boundary is always a plain data structure — no entities, no ORM objects, no framework-specific types. This prevents inner layers from gaining transitive dependencies on outer-layer frameworks.

### Package-by-Feature vs. Package-by-Layer vs. Package-by-Component
Simon Brown's "missing chapter" (Chapter 34) maps the abstract circles to real code organization strategies:
- **Package by layer** — Traditional `controllers/`, `services/`, `repositories/` structure. Weak encapsulation; the dependency rule is not enforced by the package structure.
- **Package by feature** — `orders/`, `users/`, `payments/`. Better cohesion, but still no explicit boundary enforcement.
- **Package by component** — A hybrid where each component is a coarse-grained unit with an internal structure that enforces the dependency rule through access modifiers or module systems.

### The Test Boundary
Tests are a component. They depend on the system under test but nothing depends on them. They are the *most outer* component — even more so than `Main`. This positioning means tests should depend on stable inner interfaces, not volatile outer implementations.

---

## Tradeoffs & Tensions

### Indirection Cost vs. Change Cost
Every boundary adds indirection: an interface, a data-transfer object, a mapping step. For a two-person team building an MVP, full Clean Architecture can feel like carrying a loaded backpack on a sprint. The benefit pays off when requirements change, teams grow, or the delivery mechanism shifts — but you pay the cost upfront.

**Practitioner consensus:** Start with clear dependency direction (inner layers must not import outer layers) even if you do not build full port/adapter pairs for every boundary. Add formal boundaries as the system's change rate and team size justify them.

### Screaming Architecture vs. Framework Conventions
Most popular frameworks (Rails, Django, Spring Boot, Next.js) impose a directory structure that screams the framework, not the domain. Fighting the framework's conventions creates friction for new team members, breaks generator/scaffolding tools, and diverges from community examples.

**Practical resolution:** Many teams keep the framework's outer structure but enforce the dependency rule *inside* each feature/module. The use-case layer and entity layer live in framework-agnostic packages/modules, even if the top-level directory says `app/` or `src/`.

### Premature Boundary Extraction
Martin himself notes the danger: extracting a boundary too early creates complexity without payoff; extracting too late means expensive refactoring. The book offers guidelines (the "Zone of Pain" and "Zone of Uselessness" in the I/A graph from the Stable Abstractions Principle) but no algorithm. Judgment is required.

### Microservices Confusion
Clean Architecture describes *logical* boundaries, not *physical* (deployment) boundaries. Some readers conflate "separate component" with "separate microservice." Martin is careful to distinguish these, but the confusion persists in the community. A Clean Architecture can live entirely inside a single deployable monolith.

### Entity Purity vs. Pragmatism
In the strictest reading, entities have zero dependencies on any technology. In practice, many teams annotate entities with ORM metadata, validation decorators, or serialization hints. This violates the dependency rule but dramatically reduces boilerplate. The tension is real and each team must choose their tolerance.

### Functional vs. Object-Oriented Styles
The book leans heavily on OO polymorphism to achieve dependency inversion. In functional ecosystems (Elixir, Haskell, Clojure), the dependency rule is enforced through module boundaries and function signatures rather than interfaces and abstract classes. The principle survives; the mechanism changes.

---

## What to Watch Out For

1. **Cargo-culting the concentric circles.** Drawing four circles on a whiteboard does not produce a clean architecture. The circles are a *dependency direction diagram*, not a file-organization chart. What matters is that source dependencies point inward. If they do not, the circles are decorative.

2. **Mapping-layer explosion.** A naive implementation can produce six mapping steps for a single request: HTTP request -> Controller DTO -> Request Model -> Entity -> Response Model -> Presenter DTO -> HTTP response. Each mapping is a place for bugs and boilerplate. Use mapping only at true architectural boundaries, not at every method call.

3. **"Clean" as a reason to avoid frameworks.** The book does not say "don't use frameworks." It says "don't marry them." Use the framework; just isolate the parts of your code that would survive a framework change.

4. **Ignoring the cost dimension.** Martin discusses boundary costs but many summaries omit this. The book explicitly supports partial boundaries and deferred boundaries. Not every project needs full port/adapter pairs from day one.

5. **Over-abstraction of the database.** In data-intensive applications (reporting, analytics, ETL), the database *is* the architecture. Abstracting it behind a repository interface can destroy performance by preventing query optimization. The dependency rule still applies in principle — but the boundary may be thinner, or the "entity" layer may be closer to the query model.

6. **Testing theater.** The book emphasizes testability as a primary benefit. But if your test suite only tests through the adapters (integration tests) and never exercises use cases in isolation, you have the structure without the benefit. The value comes from *actually writing* fast, isolated use-case tests.

7. **Confusing layers with microservices.** Each concentric ring is a source-code dependency boundary, not a network boundary. Deploying each layer as a separate service adds latency, operational complexity, and distributed-system failure modes — all without any benefit from the dependency rule, which is a compile-time concern.

---

## Applicability by Task Type

### Architecture Planning
**High applicability.** Clean Architecture provides the primary vocabulary for early architectural decisions: Where are the boundaries? Which direction do dependencies flow? What are the use cases? What are the policies vs. details? For greenfield systems, the concentric-circles model is an excellent starting framework for the initial component diagram.

For AI-assisted architecture planning: an LLM can be prompted with the dependency rule as a constraint and asked to propose module/package structures that comply. The rule is simple enough to be mechanically verifiable.

### Code / API Design
**High applicability.** The Input Port / Output Port / Interactor pattern directly shapes API design:
- Public API surfaces correspond to Input Ports.
- Response shapes correspond to Response Models (not entity internals).
- Error handling is part of the Output Port contract.

When an AI agent generates a new feature, having it produce an Interactor with explicit Request/Response models and a Gateway interface prevents the common failure mode of tangling HTTP handling with business logic.

### Feature Design on Existing Systems
**Medium-high applicability.** The most common scenario: adding a feature to a system that does not follow Clean Architecture. The practical approach:
1. Identify the use case.
2. Write the interactor with ports, even if the rest of the system does not use this pattern.
3. Implement adapters that bridge to the existing infrastructure.
4. Over time, the new pattern spreads; the old code is refactored feature-by-feature.

This "strangler fig" approach aligns with the book's pragmatism about partial boundaries. An AI agent working on a feature in a legacy codebase can be given a directive: "Business logic for this feature must not import from the web or database layers."

### Code Review
**High applicability.** The dependency rule provides a concrete, reviewable checklist:
- Does this new file import anything from an outer layer?
- Does the use case reference the HTTP request object directly?
- Does the entity import the ORM?
- Is the data crossing a boundary a simple structure or a framework-specific type?

These questions can be automated with linting rules (e.g., ArchUnit in Java, dependency-cruiser in JavaScript/TypeScript, import-linter in Python). For AI-assisted code review, the dependency rule can be stated as a system prompt constraint.

### Bug Diagnosis (Tracing Through Layers)
**Medium applicability.** Clean Architecture's layering helps localize bugs:
- If the bug is in business logic, look in the use-case/entity layers.
- If the bug is in data marshaling, look in the adapter layer.
- If the bug is in wiring, look in `Main` / the composition root.

However, the indirection can make stack traces harder to follow — especially when dependency injection containers obscure the concrete call path. For AI-assisted debugging, the clear separation of concerns helps: you can ask the agent to focus on a specific layer without worrying about side effects from other layers.

---

## Relationship to Other Books in This Category

### Complements
- **"A Philosophy of Software Design" (John Ousterhout, 2018)** — Ousterhout focuses on module-level depth vs. shallowness. Clean Architecture focuses on system-level dependency direction. They operate at different scales and reinforce each other. Ousterhout's "deep modules" make excellent ports; Clean Architecture explains which direction the arrows point.
- **"Domain-Driven Design" (Eric Evans, 2003)** — DDD provides the vocabulary for what lives *inside* the Entity and Use Case layers (Aggregates, Value Objects, Domain Events, Bounded Contexts). Clean Architecture provides the structural envelope. Together they are arguably the most influential pairing in modern software design thinking.
- **"Designing Data-Intensive Applications" (Martin Kleppmann, 2017)** — Kleppmann covers what Clean Architecture calls "details" — databases, message brokers, replication, partitioning. Understanding both helps architects know *when* the database is a detail and *when* the database is the architecture.
- **"Patterns of Enterprise Application Architecture" (Martin Fowler, 2002)** — Fowler catalogs the tactical patterns (Repository, Unit of Work, Data Mapper, Service Layer) that implement Clean Architecture's abstract layers in practice.

### Tensions
- **"A Philosophy of Software Design" (Ousterhout)** — Ousterhout explicitly argues against "classitis" and excessive decomposition, which Clean Architecture can encourage when applied dogmatically. Ousterhout would likely push back on a six-layer mapping chain as a "shallow module" anti-pattern.
- **Ruby/Rails community (DHH and "The Majestic Monolith")** — David Heinemeier Hansson and the Rails philosophy embrace framework coupling as a feature, not a bug. From this perspective, Clean Architecture's insistence on framework independence is an unnecessary abstraction tax for most applications. The tension is legitimate: for many CRUD-heavy web apps, the framework *is* the architecture, and fighting it creates friction without proportional benefit.

### Lineage
- **"Hexagonal Architecture" (Alistair Cockburn, 2005)** — The most direct ancestor. Clean Architecture adds the concentric layering on top of the ports-and-adapters model.
- **"Object-Oriented Software Engineering" (Ivar Jacobson, 1992)** — Introduced use-case-driven design and the BCE (Boundary-Control-Entity) pattern that Martin explicitly acknowledges as a precursor.
- **SOLID Principles (Martin, 2000s)** — Clean Architecture is the architectural-scale extension of the SOLID principles, particularly the Dependency Inversion Principle and the Interface Segregation Principle.

---

## Freshness Assessment

**Publication date:** September 2017.

**Core concepts durability:** The dependency rule, the distinction between policies and details, and the plugin model are timeless structural principles. They apply to any language, any paradigm, any era. These ideas predate the book (Hexagonal Architecture, 2005; Onion Architecture, 2008) and will outlast it.

**What has evolved since publication:**
- **Serverless and edge computing** — The "Main" component and composition root may now be a cloud function entry point. The principles apply but the wiring patterns differ.
- **TypeScript / modern frontend** — Clean Architecture has been widely adopted in frontend applications (React, Angular), sometimes under the name "Feature-Sliced Design" or similar. The challenge is that frontend frameworks are more tightly coupled to UI rendering, making the Humble Object boundary harder to draw.
- **Microservices maturation** — The industry has learned (painfully) that microservices boundaries are not the same as Clean Architecture boundaries. Martin's warning about this distinction in the book has aged well.
- **AI-generated code** — Clean Architecture's clear rules make it unusually well-suited as a constraint for AI code generation. The dependency rule can be stated as a prompt instruction and verified statically.
- **Functional-first languages** — The community has adapted the model for languages without classical OO inheritance, using module boundaries, type classes, and effect systems to enforce the dependency rule.

**Verdict:** The book remains highly relevant. The principles are durable; the implementation examples (Java-heavy) may feel dated. Readers should supplement with modern language-specific implementations.

---

## Key Framings Worth Preserving

### The Dependency Rule (verbatim framing)
> "Source code dependencies must point only inward, toward higher-level policies."

This is the one rule. Everything else in the book is either justification for this rule or guidance on how to implement it. When working with AI agents, this single sentence can serve as an architectural constraint in a system prompt.

### The "Deferred Decision" Framing
> "A good architecture allows you to defer decisions about frameworks, databases, and delivery mechanisms."

This reframes architecture from "choosing technologies" to "preserving the ability to choose technologies later." It is a powerful corrective to the common practice of starting a project by choosing a framework and database, then building the domain logic around those choices.

### The "Screaming Architecture" Test
> "When you look at the top-level directory structure of a system, what does it scream? If it screams 'Rails' or 'Spring,' you have an architecture that is dominated by the framework. If it screams 'Health Care' or 'Accounting,' you have an architecture that is dominated by the use cases."

A quick litmus test for any codebase. For AI-assisted development, this framing helps an agent decide how to name and organize new modules.

### The Cost of Boundaries
> "Every boundary has a cost. Every boundary requires interfaces, data structures, and the management of dependencies across it."

This prevents the common misreading that Clean Architecture demands maximum abstraction everywhere. Martin himself advocates for partial and deferred boundaries. The architect's skill is in knowing where boundaries pay for themselves.

### Entities Are Not Database Rows
> "An Entity is an object within our computer system that embodies a small set of critical business rules operating on Critical Business Data."

Entities are not ActiveRecord models. They are not ORM-managed objects. They are pure business-logic objects that know nothing about persistence. This distinction is the single most commonly violated aspect of Clean Architecture in real codebases.

### The Plugin Analogy
> "The database is a plugin. The web is a plugin. The framework is a plugin."

This flips the conventional mental model where the database is "the foundation" and the web framework is "the skeleton." In Clean Architecture, both are peripheral. The business rules are the foundation.

### The Two-Dimensional Quality Metric
Architecture quality has two dimensions:
1. **Does the system work?** (Behavior — what stakeholders usually focus on.)
2. **Is the system easy to change?** (Structure — what architects focus on.)

Martin argues that structure is *more important* than behavior, because a system that works but cannot be changed will eventually stop working, while a system that does not work but is easy to change can be made to work.

---

*This reference is compiled from the book's content, Robert C. Martin's blog posts (particularly "The Clean Architecture," August 2012), his conference talks (NDC, GOTO, YOW!), and the extensive practitioner discourse in blog posts, podcast episodes, and community discussions. It is intended as a practical reference for architecture and code design decisions, particularly in contexts where AI agents assist with code generation and review.*
