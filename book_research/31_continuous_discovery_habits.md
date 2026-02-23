# Continuous Discovery Habits -- Teresa Torres (2021)
**Skill Category:** Product Strategy & User Research
**Relevance to AI-assisted / vibe-coding workflows:** Provides the framework for assumption-testing and opportunity mapping that prevents building the wrong thing -- useful for feature design tasks. Before writing a single line of code (or prompting an AI to generate it), this book's discipline ensures you are solving a real customer problem and have tested the riskiest assumptions. In vibe-coding contexts where speed of generation is high, the cost of building the wrong thing is proportionally higher -- discovery habits act as the essential governor.

---

## What This Book Is About

Teresa Torres codifies a structured, repeatable approach to **continuous product discovery** -- the activities a product team undertakes to decide *what* to build. The book is aimed at product trios (product manager, designer, tech lead) and argues that discovery should not be a phase or a project but a set of **weekly habits** embedded into the team's normal workflow.

The core thesis: Most product teams either skip discovery entirely (shipping features based on stakeholder requests or gut instinct) or treat it as a one-time research project. Both approaches lead to waste. Instead, teams should maintain a continuous cadence of customer interviewing, opportunity mapping, assumption testing, and small experiments -- all structured around a clear desired **outcome** rather than a list of features to deliver.

The book is practical and prescriptive. Torres draws on over a decade of coaching product teams and provides specific techniques, visual frameworks, and step-by-step processes. It is not a theory book -- it is a habit-formation manual for product teams.

**Publication context:** Self-published through Product Talk LLC in 2021. Torres had been teaching these concepts through her Product Talk blog (producttalk.org) and coaching practice for years before the book. The book consolidates and extends that body of work.

---

## Key Ideas & Mental Models

### 1. The Outcome-Over-Output Mindset
Teams should be measured by the **outcomes** they drive (changes in customer behavior or business metrics) rather than the **outputs** they ship (features, story points). This is the foundational orientation. Torres argues that an outcome-oriented team naturally needs discovery because you cannot guarantee outcomes with a feature list -- you must learn your way to them.

### 2. The Opportunity Solution Tree (OST)
The signature framework of the book. A visual tree structure with four levels:

- **Desired Outcome** (top): The measurable business or product metric the team is trying to move. Set by leadership or negotiated with the team.
- **Opportunities** (second level): Customer needs, pain points, and desires discovered through research. These are framed from the customer's perspective, not the company's. Opportunities branch and nest -- large opportunity spaces contain sub-opportunities.
- **Solutions** (third level): Possible product changes, features, or interventions that could address a given opportunity. Multiple solutions should map to each opportunity.
- **Experiments** (bottom level): Small, fast tests designed to evaluate whether a solution will work before building it fully.

The OST serves multiple purposes:
- **Shared understanding**: The whole trio can see the decision landscape.
- **Scope management**: You compare and prioritize opportunities rather than arguing about features.
- **Prevents solution-jumping**: By requiring you to explore the opportunity space before ideating solutions.
- **Living artifact**: Updated weekly as new interview data comes in and experiments resolve.

Key rules for a well-formed OST:
- Opportunities are framed as customer needs/pain points/desires, not company goals.
- Each opportunity should be distinct (not overlapping).
- Solutions are connected to specific opportunities (not floating).
- The tree is never "done" -- it evolves.

### 3. Continuous Interviewing
Torres advocates for **weekly customer interviews** conducted by the product trio (not outsourced to a research team). Key principles:

- **Automate recruiting**: Set up a pipeline so that recruiting participants is not a bottleneck. Use in-product prompts, customer success handoffs, or scheduled panels.
- **Story-based interviewing**: Rather than asking customers what they want (which produces unreliable data), ask them to tell specific stories about past behavior. "Tell me about the last time you..." elicits concrete details about actual behavior rather than hypothetical preferences.
- **Interview snapshots**: After each interview, the team synthesizes a one-page snapshot capturing: key moments, opportunities identified, and insights. These feed directly into the opportunity space of the OST.
- **Separate interviewing from selling/testing**: Discovery interviews are about understanding the customer's world, not pitching solutions or running usability tests.

### 4. Assumption Mapping
Before investing in building a solution, teams should identify and test the **underlying assumptions** that must be true for the solution to succeed. Torres categorizes assumptions into types:

- **Desirability assumptions**: Will customers want this? Will they choose it?
- **Viability assumptions**: Will this work for our business? Can we sustain it?
- **Feasibility assumptions**: Can we build this? Do we have the technical capability?
- **Usability assumptions**: Can customers figure out how to use this?
- **Ethical assumptions**: Should we build this? Are there unintended consequences?

The mapping process:
1. Generate a comprehensive list of assumptions for a given solution.
2. Plot them on a 2x2 matrix: **importance** (how critical is this assumption to the solution working) vs. **evidence** (how much evidence do we already have).
3. Prioritize testing assumptions that are high-importance and low-evidence -- these are the "leap of faith" assumptions.

### 5. Experiment Design and Types
Torres provides a taxonomy of experiments, ordered roughly from fastest/cheapest to slowest/most expensive:

- **One-question surveys**: Embedded in the product, testing a single assumption.
- **Data mining**: Analyzing existing behavioral data to test an assumption.
- **Fake door / painted door tests**: Presenting a feature option to gauge interest before building it.
- **Wizard of Oz**: Delivering the experience manually behind the scenes while the customer thinks it is automated.
- **Concierge tests**: Delivering the value proposition manually and personally to a small number of customers.
- **Prototypes**: Clickable or paper prototypes for usability and desirability testing.
- **Smoke tests / landing pages**: Marketing the solution before building it to test demand.
- **A/B tests and small releases**: Shipping a minimal version to a subset of users and measuring outcomes.

The key insight: You should run the **smallest, fastest experiment** that can generate enough evidence to reduce uncertainty on your riskiest assumption. Do not default to building an MVP when a survey or data mining could answer the question in a day.

### 6. Compare and Contrast (Diverge Then Converge)
Torres emphasizes that teams should generate **at least three** solutions for any opportunity before selecting one to test. This prevents the common anti-pattern of falling in love with the first idea. The compare-and-contrast approach creates better solutions through:
- Broadening the solution space
- Surfacing different assumption profiles
- Allowing recombination of ideas

### 7. The Product Trio
Discovery is best done by a cross-functional **trio** of product manager, designer, and tech lead working together -- not by the PM alone handing off requirements. Each role brings essential perspective: the PM understands the business and customer context, the designer understands usability and experience, and the tech lead understands feasibility and system constraints. The trio should co-interview, co-map, and co-decide.

---

## Patterns & Approaches Introduced

### The Weekly Discovery Cadence
Torres prescribes a specific rhythm:
- **At least one customer interview per week** (ideally by the full trio).
- **Synthesize interview snapshots** immediately after each interview.
- **Update the opportunity solution tree** weekly with new data.
- **Identify and run at least one experiment** per week (can be very small).
- **Review and iterate** on the tree as a team.

This weekly cadence is the "habit" in the title. Torres argues that doing discovery in bursts (e.g., a two-week research sprint every quarter) is far less effective than a continuous, lightweight practice.

### Interview Snapshot Format
A structured one-page synthesis created after each interview:
- Quick summary of the interviewee and context
- Key moments/stories from the interview
- Opportunities identified (mapped to the OST)
- Surprises or contradictions to existing beliefs

### Opportunity Scoring / Prioritization
When choosing which opportunity to pursue:
- **Opportunity sizing**: How many customers are affected? How frequently?
- **Customer importance**: How painful or important is this to customers?
- **Satisfaction with current solutions**: Are existing alternatives adequate?
- **Strategic alignment**: Does this connect to our desired outcome?

Torres does not prescribe a rigid scoring formula but recommends teams develop a lightweight, consistent way to compare opportunities.

### The "Story-Based" Interview Protocol
Specific prompts and techniques:
- Start with "Tell me about the last time you [did relevant activity]."
- Follow the thread: "What happened next? What did you do then?"
- Avoid hypotheticals: Never ask "Would you use X?" or "How much would you pay for Y?"
- Probe for emotions: "How did that make you feel? What was frustrating?"
- End with "Is there anything else I should have asked?"

### Iterative Solution Refinement
Rather than big-bang solution design:
1. Start with the opportunity (customer need).
2. Generate multiple solution concepts (at least three).
3. Identify assumptions for each.
4. Map assumptions (importance vs. evidence).
5. Test the riskiest assumption with the smallest possible experiment.
6. Update your understanding and iterate.
7. Only build the full solution after critical assumptions are validated.

---

## Tradeoffs & Tensions

### Speed vs. Rigor
The book advocates for weekly experiments, which implies speed. But thorough assumption mapping and multi-solution generation can feel slow to teams under delivery pressure. Torres addresses this by emphasizing that experiments can be tiny (a single-question survey, a data query), but teams accustomed to "just ship it" cultures may struggle with the perceived overhead.

### Continuous Interviewing vs. Research Depth
Weekly 30-minute interviews with customers yield breadth and ongoing contact with the customer's world, but they do not replace deep ethnographic research, diary studies, or large-scale quantitative studies. Teams that rely solely on continuous interviewing may miss structural insights that require more intensive methods.

### The Trio Model vs. Organizational Reality
The trio model assumes the PM, designer, and tech lead are co-located (or synchronously available), share a single product area, and have the authority to make discovery decisions. In practice, many organizations have shared designers, distributed teams, or strong top-down feature mandates that undermine the trio's autonomy. Torres acknowledges this but does not deeply address organizational change management.

### Outcome-Driven Teams vs. Roadmap-Driven Organizations
The book assumes teams are empowered with outcomes rather than handed feature roadmaps. This is aspirational for many organizations. Teams in roadmap-driven environments can adopt some discovery practices (interviewing, assumption testing) but will hit friction when the OST suggests a different direction than the committed roadmap.

### Opportunity Framing Difficulty
Framing opportunities from the customer's perspective (rather than as business needs or solution ideas) is genuinely hard. Teams frequently slip into framing opportunities as "We need a better onboarding flow" (solution-shaped) rather than "New users struggle to understand how the product connects to their existing workflow" (customer-need-shaped). The book provides guidance but this remains a persistent challenge.

### Small Experiments vs. Meaningful Evidence
Some assumption types (especially viability and ethical assumptions) are difficult to test with small, fast experiments. A one-question survey can test desirability, but testing whether a business model will sustain at scale often requires more substantial investment. The book's emphasis on speed can sometimes lead to false confidence from weak evidence.

### Discovery Paralysis
Teams new to discovery sometimes over-rotate: they keep researching and mapping and testing and never feel confident enough to commit to building. Torres cautions against this but the framework's thoroughness can exacerbate the tendency in risk-averse cultures.

---

## What to Watch Out For

1. **Treating the OST as a one-time exercise.** The tree is a living artifact that must be updated weekly. Drawing it once and referencing it for months defeats the purpose. If it is static, it has become a roadmap in disguise.

2. **Skipping story-based interviewing in favor of usability testing.** Usability tests evaluate a specific solution. Discovery interviews explore the problem space. They are different activities and both are needed, but the book's emphasis is on the latter.

3. **Confusing customer requests with opportunities.** A customer saying "I want a dark mode" is a solution request. The underlying opportunity might be "Users struggle to use the product in low-light environments" or "Users want the product to feel modern and customizable." Always dig for the underlying need.

4. **Assumption mapping without follow-through.** Identifying assumptions is only valuable if you actually run experiments to test the risky ones. Some teams treat assumption mapping as a checkbox exercise and then build anyway.

5. **Survivorship bias in interview recruiting.** If you only interview current, active users, you miss churned users, non-adopters, and edge cases. Torres recommends diversifying your interview pipeline, but teams often default to whoever is easiest to recruit.

6. **The trio becoming a bottleneck.** If only three people do discovery and the broader team is disconnected from insights, you recreate an ivory-tower dynamic. Sharing interview snapshots and the OST broadly is essential.

7. **Applying the full framework to trivial decisions.** Not every feature needs a full OST, assumption map, and experiment series. Torres's framework is most valuable for strategic bets and areas of high uncertainty. For well-understood, low-risk changes, lighter-weight decision processes are appropriate.

8. **Neglecting quantitative data.** The book's emphasis is on qualitative discovery (interviews, small experiments). Teams should complement this with behavioral analytics, funnel analysis, and quantitative research. Torres acknowledges this but the book skews qualitative.

---

## Applicability by Task Type

### Feature Design & Scoping
**High applicability.** This is the book's primary use case. Before designing a feature:
- Map the opportunity space to ensure you are solving a real customer problem.
- Generate multiple solution concepts (at least three).
- Identify and map assumptions.
- Run small experiments before committing to a full build.
- In AI-assisted workflows, use the OST to generate a clear brief for what to build and why, reducing the risk of fast-but-wrong code generation.

### Product Documentation
**Moderate applicability.** The interview snapshot format and OST provide excellent source material for PRDs, product briefs, and decision logs. When writing product documentation, the OST serves as a visual table of contents for the problem space, and assumption maps document the evidence base for decisions. Documentation grounded in discovery artifacts is more defensible and easier to update.

### User Research Framing
**High applicability.** The book's story-based interviewing protocol is directly useful for framing and conducting user research. Key contributions:
- The distinction between discovery interviews (exploring the problem space) and evaluative research (testing solutions).
- The interview snapshot as a lightweight synthesis format.
- The principle of continuous, small-batch research over big-bang studies.
- The automated recruiting pipeline as infrastructure.

### Assumption Identification Before Building
**Very high applicability -- this is arguably the book's greatest single contribution.** The assumption mapping framework (desirability, viability, feasibility, usability, ethical) combined with the importance-vs-evidence prioritization matrix gives teams a systematic way to identify what they do not know before investing in building. In vibe-coding or AI-assisted development, where the cost of generating code is low but the cost of building the *wrong* thing remains high, assumption identification is the critical gate.

### Sprint Planning & Backlog Management
**Moderate applicability.** The OST provides a principled way to generate and prioritize backlog items. Rather than a flat list of feature requests, the tree structure shows the relationship between outcomes, opportunities, and solutions. This helps teams say "no" to solutions that do not map to a prioritized opportunity.

### Stakeholder Communication
**Moderate applicability.** The OST is an effective communication tool for showing leadership the landscape of opportunities, the rationale for pursuing specific ones, and the evidence gathered through experiments. It replaces "we think this is a good idea" with "we have tested these assumptions and here is what we learned."

---

## Relationship to Other Books in This Category

### Inspired / Empowered (Marty Cagan)
Cagan provides the organizational model (empowered product teams, product vision, product strategy) within which Torres's discovery practices operate. Cagan says teams should be given problems to solve, not features to build. Torres tells you *how* to solve those problems through structured discovery. They are highly complementary -- Cagan provides the why and the organizational context, Torres provides the how and the weekly habits.

### The Lean Startup (Eric Ries)
Torres builds on Ries's concepts of validated learning, build-measure-learn, and MVPs but makes them more practical and structured for established product teams (not just startups). The OST is a more sophisticated decision framework than Ries's pivot-or-persevere, and Torres's experiment taxonomy goes well beyond the MVP concept. Where Ries is conceptual, Torres is operational.

### Sprint (Jake Knapp)
The Google Ventures Design Sprint is a time-boxed (5-day) discovery and prototyping process. Torres's framework is continuous rather than episodic. Sprints can be useful for kickstarting discovery or tackling a specific high-stakes question, but Torres would argue they should feed into an ongoing discovery practice, not replace it.

### Lean UX (Jeff Gothelf & Josh Seiden)
Lean UX shares Torres's emphasis on outcomes over outputs, cross-functional collaboration, and experimentation. Torres's contribution is more structured (the OST, assumption mapping matrix) and more focused on the interview-to-insight pipeline. Gothelf and Seiden are closer to the design process; Torres is closer to the product strategy process.

### Jobs to Be Done (Christensen / Ulwick / Klement)
JTBD theory deeply informs Torres's concept of "opportunities." The idea that customers "hire" products to make progress in their lives maps directly to the opportunity framing in the OST. Torres does not require teams to use JTBD language specifically but the underlying orientation is consistent. Teams familiar with JTBD will find the opportunity space intuitive.

### Escaping the Build Trap (Melissa Perri)
Perri diagnoses the organizational dysfunction (the "build trap") that Torres's habits are designed to prevent. Perri focuses on strategy and organizational design; Torres focuses on the team-level practices. They address the same problem from different altitudes.

### Thinking in Bets (Annie Duke)
Duke's framework for decision-making under uncertainty complements Torres's assumption mapping. Both argue that decisions should be evaluated by the quality of the process (did you identify and test key uncertainties?) rather than the outcome (did the feature succeed?). Duke provides the mindset; Torres provides the product-specific tools.

### User Story Mapping (Jeff Patton)
Patton's story maps organize delivery; Torres's opportunity solution trees organize discovery. Both are visual, hierarchical, and collaborative. Teams often use story maps downstream of the OST -- once a solution is validated through discovery, it gets broken down into a story map for delivery planning.

---

## Freshness Assessment

**Published:** 2021 (Product Talk LLC)
**Currency as of 2026:** The core frameworks (OST, continuous interviewing, assumption mapping) remain highly relevant and widely adopted. The book has become a standard reference in product management education and coaching. No major methodological shifts have rendered the content outdated.

**What has evolved since publication:**
- **AI-assisted product development** has accelerated build speed, making the "should we build this?" question (discovery) even more important than the "can we build this?" question (delivery). Torres's framework has arguably become *more* relevant, not less.
- **Remote and async collaboration** has become more prevalent. The trio model and co-interviewing practices may need adaptation for distributed teams (async interview review, recorded sessions, collaborative digital whiteboarding for OSTs).
- **Product ops and research ops** roles have grown, potentially handling some of the recruiting and synthesis infrastructure Torres asks the trio to build.
- Torres has continued to publish extensively on producttalk.org, expanding on topics like opportunity scoring, managing multiple outcomes, and scaling discovery across organizations. The blog is a living extension of the book.

**Verdict:** Still highly current. The frameworks are durable because they address fundamental cognitive challenges (solution-jumping, confirmation bias, building without evidence) that do not change with technology trends.

---

## Key Framings Worth Preserving

> **"At a minimum, weekly touchpoints with customers, by the team building the product, where they conduct small research activities in pursuit of a desired outcome."**
-- Torres's definition of continuous discovery. This single sentence captures the cadence (weekly), the actor (the building team, not a separate research team), the scope (small activities, not big projects), and the orientation (outcome-driven).

> **"Good discovery requires that we explore the problem space before we commit to a solution."**
-- The anti-pattern this counters is ubiquitous: teams jump from a customer complaint or stakeholder request directly to building a feature without understanding the underlying opportunity.

> **"Opportunities should be framed as customer needs, pain points, or desires -- not as features or business objectives."**
-- This is the most common mistake teams make when building an OST. The discipline of customer-centric framing is what makes the tree useful.

> **"Compare and contrast. Generate at least three solutions before selecting one."**
-- Counters the "first idea" bias. In AI-assisted development, this translates to: prompt for multiple design approaches before committing to one.

> **"Test the assumption, not the idea."**
-- The shift from "let's test the whole feature" to "let's test the single riskiest assumption" is the key to speed. You do not need to build a prototype to test a desirability assumption -- a survey or interview question might suffice.

> **"The goal of an experiment is not to validate our idea. It's to reduce the risk of moving forward."**
-- Reframes experimentation as risk reduction rather than confirmation-seeking. This counters confirmation bias in experiment design.

> **"If you are only interviewing when you have a specific question, you are not doing continuous discovery."**
-- The continuous interview habit generates serendipitous insights and keeps the team connected to the customer's evolving world, not just answering predetermined questions.

> **"An opportunity solution tree is never done. It's a living, breathing representation of your understanding of the problem space."**
-- Prevents the tree from becoming a static artifact filed away after a planning session.

### Distilled Decision Heuristics

1. **Before building anything:** Can I point to a specific opportunity (customer need) this addresses? If not, stop and discover.
2. **Before committing to a solution:** Have I considered at least three alternatives? If not, diverge further.
3. **Before investing significant build effort:** What is my riskiest assumption, and have I tested it with the smallest possible experiment? If not, design an experiment.
4. **When receiving a feature request:** What is the underlying opportunity? Reframe the request as a customer need before evaluating solutions.
5. **When planning a sprint:** Does every item trace back to a prioritized opportunity in the OST? If items are orphaned from the tree, question their priority.

---
