# Shape Up — Ryan Singer (2019)

**Skill Category:** Product Strategy & Feature Design
**Relevance to AI-assisted / vibe-coding workflows:** Introduces "appetite" and fixed-time/variable-scope thinking — useful for scoping features and writing product docs that acknowledge constraints and tradeoffs. When working with AI coding tools, the shaping discipline forces you to define boundaries, risk, and rabbit holes *before* generating code — preventing the common failure mode of building the wrong thing quickly.

---

## What This Book Is About

Shape Up is Basecamp's methodology for how to do product development work. Written by Ryan Singer (Head of Strategy at Basecamp at the time of publication), it describes the system Basecamp used internally to ship software — one that rejects both rigid waterfall planning and the endless treadmill of two-week sprints. The book is freely available at basecamp.com/shapeup.

The core thesis: most product teams fail not because they lack talent or speed, but because they work on poorly defined projects with no time boundaries, or they over-specify work and leave builders no room for creative problem-solving. Shape Up proposes a middle path — *shape* the work at a high level before committing to it, *bet* on shaped work in fixed six-week cycles, and give small teams full autonomy to figure out the details within that time box.

The book is organized in three parts:

1. **Shaping (Chapters 1-6):** How to define work at the right level of abstraction before committing to build it. Covers appetite, fat marker sketches, breadboards, finding elements, setting boundaries, and identifying risks/rabbit holes.

2. **Betting (Chapters 7-9):** How to decide what to work on. Covers the betting table, six-week cycles, cool-down periods, and why backlogs are harmful.

3. **Building (Chapters 10-15):** How autonomous teams take shaped work and deliver it. Covers getting oriented, discovering tasks, mapping scopes, showing progress (the hill chart), and deciding when to cut scope vs. extend.

The book is short, opinionated, and practical. It is not a theoretical framework but a documented practice — how one specific company (Basecamp/37signals) actually ships software. This is both its strength (concrete, battle-tested) and its limitation (shaped by a specific organizational context).

---

## Key Ideas & Mental Models

### 1. Appetite vs. Estimate

The single most important concept in the book. Traditional product development asks "how long will this take?" (an estimate). Shape Up flips this: "how much time is this *worth*?" (an appetite).

Appetite is a fixed time budget — typically either a **small batch** (one to two weeks) or a **big batch** (six weeks) — set *before* the work is shaped in detail. The appetite constrains the solution. If the shaped solution does not fit within the appetite, you either simplify the solution or walk away from the idea entirely.

This inversion is powerful because it forces honest conversations about value. Instead of negotiating deadlines, you negotiate scope. "We could spend six weeks on a full calendar feature, or we could spend two weeks on a simpler date-picker that solves 80% of the use case." The appetite makes the tradeoff explicit.

### 2. Shaping (The Right Level of Abstraction)

Shaping is the pre-work that happens before a project is bet on. A shaped pitch is neither a vague user story ("As a user, I want to manage events") nor a detailed specification with wireframes. It occupies the sweet spot: specific enough to be buildable, rough enough to leave room for builders to make design decisions.

A well-shaped pitch includes:
- **Problem definition:** What is the pain, who has it, and why does it matter now?
- **Appetite:** How much time this is worth.
- **Solution direction:** Rough sketches of the approach (fat marker sketches or breadboards), showing the key elements and flows without specifying pixel-level details.
- **Rabbit holes:** Known risks, edge cases, or technical unknowns that could derail the project. Ideally with strategies for how to avoid them.
- **No-gos:** Things explicitly out of scope.

Shaping is done by senior people (typically a small group that combines product, design, and technical perspective). It is closed-door work, not a committee process.

### 3. Fat Marker Sketches

A deliberate UI sketching technique where you draw with a thick marker (or equivalent large-tip digital tool) so that you *cannot* add detail. The physical constraint of the fat marker prevents you from specifying layouts, fonts, colors, or pixel positions. You can only convey the essential elements and their rough spatial relationship.

This is not about art quality — it is about abstraction level. A fat marker sketch says "there's a list here and a form here" without saying "the list has a 12px font and the form has rounded corners." This leaves the builder free to make those decisions.

### 4. Breadboards

Borrowed from electronics, a breadboard is a schematic representation of a user flow stripped of all visual design. It shows:
- **Places** (screens, dialogs, pages)
- **Affordances** (buttons, fields, links)
- **Connection lines** (what leads where)

Breadboards are used during shaping to work out interaction design without getting pulled into visual design. They are particularly useful for complex flows with multiple states or conditional paths.

### 5. The Betting Table

Shape Up replaces the traditional backlog with a **betting table** — a meeting held during the cool-down period where senior stakeholders look at shaped pitches and decide what to bet on for the next six-week cycle.

Key principles of the betting table:
- **No backlogs.** If a pitch is not bet on, it does not automatically carry forward. Anyone can re-pitch it later, but there is no accumulating queue of "approved" work that never gets done. This eliminates the guilt and overhead of backlog grooming.
- **Few bets at a time.** The team bets on a small number of shaped projects per cycle — typically one to three, depending on team size.
- **Informed bets, not commitments.** The word "bet" is deliberate. You are placing a time-boxed wager that this work will pay off. If it does not, you learn and move on.
- **Separate tracks.** Basecamp uses separate tracks for different team sizes and project types (big batch vs. small batch).

### 6. Six-Week Cycles

Shape Up uses six-week work cycles instead of the more common two-week sprints. The rationale:
- **Two weeks is not enough** to finish meaningful features without cutting corners or spilling into the next sprint.
- **Six weeks is long enough** to build something substantial from start to finish.
- **Six weeks is short enough** that the deadline creates healthy pressure. People can see the finish line from day one.

There is no daily standup, no sprint planning ceremony, no sprint review. The team has six weeks and full autonomy to ship.

### 7. Cool-Down

After each six-week cycle, there is a **two-week cool-down** period. This is not vacation — it is unstructured time where teams can:
- Fix bugs
- Explore ideas
- Refactor technical debt
- Prepare pitches for the next betting table
- Do professional development

The cool-down prevents the relentless pace of back-to-back cycles and provides the breathing room needed for shaping and strategic thinking.

### 8. The Circuit Breaker

One of the most distinctive and controversial ideas in the book. If a project is not finished at the end of its six-week cycle, it does not automatically get an extension. By default, **the project is killed.**

This is the "circuit breaker" — it prevents runaway projects from consuming unlimited time. If the work was shaped well and still could not be finished in six weeks, something was wrong with the shape, the appetite, or the bet. The team should go back to the shaping phase and rethink, not just push through.

In practice, the betting table *can* choose to re-bet on a project for another cycle, but this is a deliberate decision, not an automatic continuation. The circuit breaker forces this deliberation.

### 9. Scopes (Not Tasks)

During the building phase, teams organize work into **scopes** — meaningful slices of the project that integrate front-end, back-end, and design. A scope is a piece of the project that can be completed and demoed independently.

This contrasts with traditional task lists, which divide work by discipline (design tasks, backend tasks, frontend tasks) and create handoff dependencies. Scopes integrate across disciplines: "Implement the invoicing flow" is a scope; "Create invoice table migration" is a task.

Good scopes are discovered, not pre-planned. Teams figure out the scopes as they orient themselves in the work during the first few days of a cycle.

### 10. The Hill Chart

A visual progress tracking tool shaped like a hill. The left slope represents the **uphill phase** (figuring things out — uncertainty, exploration, unknowns). The peak is where uncertainty is resolved. The right slope represents the **downhill phase** (execution — known work, grinding through tasks).

Each scope is plotted as a dot on the hill. A scope on the uphill side means "we're still figuring this out." A scope cresting the hill means "we know what to do, we just need to do it." A scope at the bottom-right means "done."

The hill chart replaces percentage-complete tracking (which is notoriously inaccurate) with a qualitative signal about **certainty**. A project manager looking at a hill chart can instantly see which scopes are stuck in the figuring-out phase and which are on track.

### 11. Getting Oriented (The First Days)

Singer emphasizes that the first few days of a cycle should be spent *getting oriented* rather than immediately breaking work into tasks. Teams read the pitch, explore the codebase, spike on uncertain areas, and discover the scopes organically.

This is counterintuitive for teams accustomed to sprint planning. In Shape Up, the expectation is that "nothing visible happens" in the first few days — and that is fine. The team is building the mental model they need to execute efficiently for the remaining five weeks.

### 12. Fixed Time, Variable Scope

The fundamental equation of Shape Up. Time is fixed (the appetite). Scope is variable (the team can cut, simplify, or defer parts of the work to fit within the time). This is the opposite of most traditional project management, which fixes scope and lets time vary.

Variable scope does not mean shipping garbage. It means having mature conversations about which aspects of a feature are essential (the "must-haves") and which are "nice-to-haves" that can be deferred. The shaping process identifies the core of the solution; the building team decides how much of the polish and edge-case handling fits within the time.

---

## Patterns & Approaches Introduced

| Pattern | Description | When to Use |
|---|---|---|
| **Appetite-first scoping** | Set a time budget before exploring solutions. Let the budget constrain the design. | Any feature prioritization discussion. Prevents gold-plating and scope creep. |
| **Fat marker sketches** | Sketch UI concepts with deliberately coarse tools to prevent over-specification. | Early product/design discussions. When you need to communicate a solution direction without dictating implementation details. |
| **Breadboards** | Schematic flow diagrams showing places, affordances, and connections — no visual design. | Working out complex interaction flows before committing to a visual direction. |
| **Pitch documents** | Structured write-ups combining problem, appetite, solution sketch, rabbit holes, and no-gos. | Proposing work for a betting table. Also useful as lightweight PRDs in any team. |
| **Betting table** | Time-boxed decision meeting where shaped pitches compete for the next cycle's capacity. | Replacing backlog grooming with a deliberate resource allocation decision. |
| **Six-week cycles + two-week cool-down** | Fixed rhythm of focused building followed by unstructured recovery/planning time. | Teams that find two-week sprints too short for meaningful delivery. |
| **Circuit breaker** | Projects that miss their deadline are killed by default, not extended. | Preventing sunk-cost-driven death marches. Requires organizational courage. |
| **Scope mapping** | Organize building-phase work into integrated, cross-discipline "scopes" rather than discipline-specific task lists. | Any project where handoffs between design/frontend/backend are a bottleneck. |
| **Hill charts** | Plot scopes on an uphill (uncertainty) / downhill (execution) curve to visualize progress as certainty. | Tracking project health without misleading percentage-complete metrics. |
| **Uphill vs. downhill work** | Distinguish "figuring it out" work from "grinding it out" work. Different phases need different management approaches. | Sprint health checks, 1:1s, identifying blocked work. |
| **Rabbit hole identification** | During shaping, proactively catalog known technical and design risks that could blow up the timeline. | Risk management in shaping/design phase. Prevents nasty mid-project surprises. |
| **De-risking during shaping** | Spike on the riskiest parts of a project *during shaping*, before betting on it. | Any project with significant technical unknowns. The spike happens before the clock starts. |

---

## Tradeoffs & Tensions

### Shaping Requires Senior Time and Skill
Shaping is the critical bottleneck. It requires someone (or a small group) who can think across product strategy, user experience, and technical feasibility simultaneously. This is a rare skill set. If your organization lacks strong shapers, the entire system degrades — poorly shaped work leads to blown cycles and demoralized teams. Shape Up does not offer much guidance for developing shaping skills; it assumes you have people who can do it.

### Small Teams vs. Large Organizations
Shape Up was developed at Basecamp, a company with fewer than 60 employees building a single product. The methodology works well for small, autonomous teams with full-stack capability. It translates poorly to:
- **Large organizations** with complex coordination needs across many teams
- **Platform teams** whose work is driven by other teams' needs rather than direct user value
- **Compliance-heavy environments** where work must be tracked, audited, and approved at granular levels
- **Teams with deep specialization** where a single "scope" cannot be owned by one or two people

### No Backlog Is Liberating — and Terrifying
Eliminating the backlog removes the guilt of unfinished work and the overhead of grooming. But it also means good ideas can be lost if no one re-pitches them. Organizations accustomed to a product backlog as their "source of truth" for what matters will find this transition culturally difficult.

### The Circuit Breaker Requires Trust and Psychological Safety
Killing a project at the end of six weeks requires an organizational culture where this is not perceived as failure. If the team fears blame for an incomplete cycle, they will crunch to finish rather than let the circuit breaker fire. This undermines the entire model.

### Fixed Time / Variable Scope Can Be Misused
In the wrong hands, "variable scope" becomes an excuse for shipping incomplete, low-quality work. "We ran out of time, so we cut the error handling" is not what Singer intends. The discipline requires that the *core* of the solution is non-negotiable, and only peripheral concerns are variable. Without strong shaping and mature engineering judgment, the line between "acceptable scope cut" and "shipping garbage" blurs.

### Six Weeks Is Not Always the Right Duration
Some work genuinely needs more than six weeks (major infrastructure migrations, large platform rewrites). Some work genuinely needs less (quick experiments, small improvements). Singer acknowledges the "small batch" track for shorter work but says little about work that is inherently larger than six weeks. In practice, teams need to learn to decompose large efforts into six-week-sized bets, which is itself a skill.

### Cool-Down Under Pressure
When business pressure mounts, cool-down periods are the first thing to get cut. But cool-down is where shaping, bug fixing, and recovery happen. Skipping it creates a debt that compounds quickly — poorly shaped work in the next cycle, accumulating bugs, and burned-out teams.

### Tension with Continuous Deployment
Shape Up assumes work is deployed at the end of a cycle (or at least that the cycle is the unit of "done"). Teams practicing continuous deployment may find the six-week rhythm awkward — do you deploy features as they're finished, or wait for the cycle boundary? Singer's answer is somewhat flexible, but the methodology does not deeply address feature flagging, progressive rollouts, or trunk-based development.

---

## What to Watch Out For

### Cargo-Culting the Terminology
The most common failure mode. Teams adopt the vocabulary (appetite, betting table, pitches, hill charts) without changing the underlying dynamics. If your "betting table" is really just your old sprint planning meeting with a new name, you have not adopted Shape Up. The key test: are you actually willing to kill a project at the end of six weeks?

### Shaping Too Thin or Too Thick
- **Too thin:** The pitch is a vague problem statement with no solution direction. The building team wastes the first two weeks figuring out what to build. This is a disguised user story, not a shaped pitch.
- **Too thick:** The pitch includes wireframes, database schemas, and step-by-step implementation plans. The building team has no creative autonomy. This is a disguised specification document, not a shaped pitch.

The right level of abstraction is genuinely hard to hit. It takes practice and feedback loops.

### Ignoring the "Senior People Shape" Requirement
Shape Up explicitly states that shaping is done by senior, experienced people — not by the whole team in a brainstorming session. Democratizing shaping sounds appealing but tends to produce either vague compromises or over-specified designs. If you ignore this requirement, you lose the sharp opinionated thinking that makes shaping work.

### Applying Shape Up to Maintenance and Ops Work
Shape Up is designed for product development — building new features or significantly improving existing ones. It maps poorly to:
- On-call and incident response
- Bug triage and fixing (Singer suggests using cool-down for this, but high-bug-count products cannot wait)
- Infrastructure and DevOps work that does not map to user-facing features
- Support-driven work with unpredictable timing

Teams that try to force all work through the Shape Up framework end up frustrated.

### Neglecting Quantitative Data
Shape Up is heavily qualitative — it relies on the shaper's judgment, customer conversations, and intuition about what matters. It does not incorporate analytics, A/B testing, or data-driven prioritization in its methodology. Teams that rely on quantitative product signals may need to layer their data practices on top of Shape Up rather than replacing them.

### Underestimating Cultural Change
Shape Up requires trust, autonomy, and comfort with ambiguity at all levels. Developers must be comfortable working without detailed specs. Managers must be comfortable not seeing daily progress updates. Stakeholders must be comfortable with the possibility that a bet will not pay off. This cultural shift is harder than the process change.

---

## Applicability by Task Type

### Feature Scoping & Design
**Very high relevance.** This is the book's core use case. The appetite/shaping/pitch workflow is directly applicable to anyone defining features. Even teams that do not adopt the full Shape Up methodology can benefit from:
- Starting with appetite ("how much is this worth?") before estimating
- Using fat marker sketches and breadboards to communicate solution direction
- Explicitly cataloging rabbit holes and no-gos
- Writing pitches instead of vague user stories or overly detailed specs

For AI-assisted workflows specifically, a well-shaped pitch serves as excellent context for an AI coding agent — it provides the problem, constraints, and solution direction without over-specifying the implementation.

### Product Documentation
**High relevance.** The pitch format is a lightweight alternative to traditional PRDs (Product Requirements Documents). A pitch is shorter, more opinionated, and explicitly acknowledges tradeoffs and constraints. The problem/appetite/solution/rabbit-holes/no-gos structure can be adopted directly as a product documentation template.

### Architecture Planning (Fit Within Appetite)
**Moderate to high relevance.** The appetite concept translates well to architecture decisions: "Given that we want to solve this problem in six weeks, what is the simplest architecture that works?" This prevents over-engineering. The rabbit-hole identification practice maps directly to technical risk assessment.

However, Shape Up does not address the technical architecture domain specifically — it assumes the shaper has enough technical knowledge to assess feasibility and risk. For deep architectural decisions, you need additional frameworks (see "Relationship to Other Books" below).

### Project Estimation
**High relevance — but in a contrarian way.** Shape Up argues that estimation is the wrong activity. Instead of asking "how long will this take?" and then being wrong, set an appetite and shape a solution that fits. This reframe is genuinely useful for teams trapped in estimation dysfunction. However, it requires organizational buy-in — if your stakeholders demand date-based estimates, you cannot unilaterally switch to appetite-based thinking without negotiation.

---

## Relationship to Other Books in This Category

| Book | Relationship to Shape Up |
|---|---|
| **"Inspired" by Marty Cagan (2018)** | Cagan's product management framework is compatible with Shape Up but differs in emphasis. Cagan focuses on product discovery (testing ideas before building), while Singer focuses on the shaping-betting-building cycle. Cagan's "empowered teams" align with Shape Up's autonomous builders. Key difference: Cagan emphasizes continuous discovery with prototypes and user testing; Shape Up's discovery happens primarily through shaping conversations. |
| **"Lean Startup" by Eric Ries (2011)** | Lean Startup's build-measure-learn loop is philosophically aligned but methodologically different. Shape Up's six-week cycles are longer than Lean Startup's "minimum viable" experiments. Shape Up is better suited to established products adding features; Lean Startup is better suited to early-stage validation. |
| **"Sprint" by Jake Knapp (2016)** | Google Ventures' five-day design sprint is a compressed version of what Singer calls "shaping." Both create time-boxed, high-fidelity problem exploration with concrete outputs. A design sprint could feed *into* a Shape Up pitch. |
| **"Continuous Discovery Habits" by Teresa Torres (2021)** | Torres provides the continuous customer-feedback machinery that Shape Up assumes but does not prescribe. If your shaping feels disconnected from real user problems, Torres's opportunity solution trees and weekly customer interviews fill the gap. |
| **"Escaping the Build Trap" by Melissa Perri (2018)** | Perri diagnoses the organizational dysfunctions (feature factories, output-over-outcome thinking) that Shape Up aims to cure. Reading Perri helps you understand *why* Shape Up's structure exists. |
| **"The Pragmatic Programmer" by Hunt & Thomas** | Shares the emphasis on developer autonomy and craftsmanship. Shape Up provides the product-side framing that gives pragmatic programmers the space to do their best work. |
| **"An Elegant Puzzle" by Will Larson (2019)** | Larson addresses engineering management at larger scale — how to organize teams, manage technical debt, and handle organizational growth. Shape Up assumes a small, flat organization; Larson's frameworks help adapt Shape Up principles to larger contexts. |
| **"Working Backwards" by Bryar & Carr (2021)** | Amazon's "press release first" approach shares DNA with Shape Up's pitch format — both force upfront clarity about the problem and the desired outcome before diving into implementation. |

---

## Freshness Assessment

**Publication date:** 2019 (self-published by Basecamp, freely available online).
**Core content durability:** High. The principles (appetite over estimates, fixed time/variable scope, shaping at the right abstraction level, circuit breakers) are durable process ideas that do not depend on specific technologies.

### What Has Remained Fully Current
- The appetite concept and fixed-time/variable-scope thinking
- The critique of backlogs and two-week sprint treadmills
- Fat marker sketches and breadboards as communication tools
- The hill chart as a progress visualization
- The pitch format as a lightweight alternative to PRDs
- The emphasis on small autonomous teams with design+engineering integration

### What Has Evolved Since 2019
- **Ryan Singer left Basecamp in 2021** following the company's controversial internal policy changes. He has continued writing and speaking about Shape Up independently. The methodology's association with Basecamp has become somewhat complicated by the company's reputational shifts.
- **Remote and distributed teams:** Shape Up was developed for a co-located (later remote-first) single-company context. Its adoption by distributed teams across multiple organizations has revealed gaps around cross-team coordination and async communication during shaping.
- **AI-assisted development:** The rise of AI coding tools (Copilot, Cursor, Claude Code, etc.) dramatically changes the building phase. Work that took six weeks in 2019 might take two weeks with AI assistance. This suggests appetites may need recalibration, though the core principle (time budget constrains scope) still holds.
- **Shape Up in larger organizations:** Companies like Shopify have adapted Shape Up for larger engineering organizations, adding layers of coordination (cross-team pitches, multi-cycle epics, program-level betting tables) that Singer's original formulation does not address. These adaptations are documented in various conference talks and blog posts.
- **Product ops and tooling:** Tools like Linear, Shortcut, and Basecamp itself have added features to support Shape Up workflows (cycle tracking, pitch management, hill charts). The tooling ecosystem has matured.
- **Criticism and alternatives:** The methodology has faced thoughtful criticism around its applicability to platform/infrastructure work, its silence on user research methodology, and the difficulty of the shaping skill. Some teams have adopted hybrid approaches (Shape Up for feature work, Kanban for maintenance, sprints for platform work).

### Recommendation
The book remains a sharp and valuable read for anyone involved in product development, especially at small to mid-size companies building user-facing products. Its biggest contribution — the appetite concept and fixed-time/variable-scope inversion — is universally applicable even if you do not adopt the full methodology. Supplement with Teresa Torres for continuous discovery practices, Marty Cagan for broader product management context, and Will Larson for adapting these ideas to larger organizations.

---

## Key Framings Worth Preserving

> **"Projects are shaped, not specified."**
> The central distinction. A specification tells builders *what to do*. A shaped pitch tells builders *what problem to solve and roughly how*, leaving the details to their judgment. This is the key to autonomy within constraints.

> **"Appetite is the opposite of an estimate. An estimate starts with a design and ends with a number. An appetite starts with a number and ends with a design."**
> The most quotable line in the book. Captures the entire fixed-time/variable-scope philosophy in two sentences.

> **"When you have a deadline with no clear end in sight, you have a runaway project. When you have a deadline with a clear set of 'must-haves' and 'nice-to-haves', you have a shaped project."**
> The practical test for whether shaping has been done well.

> **"The way to manage scope is not to say 'this is out of scope.' It's to say 'this is out of scope *for the appetite*.'"**
> Scope management is not about dismissing ideas — it is about acknowledging that every feature has a cost, and the cost must be weighed against the time budget.

> **"If we bet six weeks and the project doesn't ship, we don't automatically give it another six weeks. We call that 'the circuit breaker.'"**
> Prevents sunk-cost escalation. The circuit breaker is what makes fixed-time/variable-scope credible — without it, "fixed time" is just a suggestion.

> **"A backlog is a pile of unprocessed work. The longer it gets, the more time you spend managing it, and the less any individual item matters."**
> The argument against maintaining a product backlog. Not everyone will agree, but the reasoning is sound — if something is truly important, someone will re-pitch it.

> **"The way to really figure out what needs to be done is to start building and discover the tasks."**
> Against upfront task decomposition. Tasks are discovered during building, not predicted during planning. This is why the first few days of a cycle are for getting oriented, not for writing task lists.

> **"Work on the hill chart is either uphill or downhill. Uphill is the hard part — you're figuring things out. Downhill is execution."**
> The key insight behind the hill chart. Traditional progress tracking counts completed tasks, which says nothing about remaining uncertainty. A scope can be 80% "done" by task count but still stuck on the uphill side if the hardest problem has not been solved.

> **"Every piece of work has two phases: the figuring-it-out phase and the making-it-happen phase. The figuring-it-out phase is where all the risk is."**
> This framing changes how you evaluate project health. A team that moves quickly through tasks but avoids the hard design/architecture decisions is not making real progress — they are just building the easy parts first.

---

*This reference document was compiled from the book's freely available content (basecamp.com/shapeup), Ryan Singer's talks and subsequent writing, community discussions, and adoption reports from companies that have implemented the methodology. It is intended as a practical aid for product strategy and feature design decisions, not a substitute for reading the book.*
