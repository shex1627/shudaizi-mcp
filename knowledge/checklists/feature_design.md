---
task: feature_design
description: Design a new feature from problem definition through scoping, discovery, and technical design
primary_sources: ["06", "29", "30", "31"]
secondary_sources: ["02", "03", "04", "23", "24", "25"]
anthropic_articles: ["a01"]
version: 1
updated: 2026-02-22
---

# Feature Design Checklist

## Phase 1: Problem Definition & Discovery

- [ ] Answer the Opportunity Assessment: What business objective? How will we know we succeeded? What customer problem? Which customer segment? [29]
- [ ] Frame the opportunity as a customer need/pain/desire, not a feature request — "Users struggle to X" not "We need a Y button" [31]
- [ ] Articulate the Big Idea in one sentence: your point of view + what is at stake + a complete thought [29]
- [ ] Assess the four risks before committing engineering resources: Value (will they use it?), Usability (can they use it?), Feasibility (can we build it?), Business Viability (should we?) [29]
- [ ] Generate at least three solution concepts before selecting one — prevent first-idea bias [31]
- [ ] Map assumptions using the importance-vs-evidence matrix; test the highest-importance, lowest-evidence assumptions first [31]
- [ ] Run the smallest, fastest experiment that reduces uncertainty on the riskiest assumption (survey, data mining, fake door, prototype) before building [31]

## Phase 2: Scoping & Appetite

- [ ] Set an appetite — "How much time is this worth?" — before exploring solutions; let the time budget constrain the design [30]
- [ ] Shape the solution at the right abstraction: specific enough to be buildable, rough enough to leave room for builder decisions — use fat marker sketches and breadboards [30]
- [ ] Identify rabbit holes: known risks, edge cases, or technical unknowns that could derail the timeline — define strategies to avoid them [30]
- [ ] Define explicit no-gos: what is out of scope for this appetite [30]
- [ ] Apply fixed-time/variable-scope thinking: the core of the solution is non-negotiable, peripheral concerns are variable [30]
- [ ] Apply "Don't outrun your headlights" — scope to what you can see clearly; plan to iterate [14]
- [ ] Ensure "good enough" quality targets are set deliberately with user input, not gold-plated or cut carelessly [14]

## Phase 3: Technical Design

- [ ] Design interfaces first: ask "Is this interface simpler than the implementation it hides?" (deep module test) [06]
- [ ] Ensure the feature can be implemented by extending an existing deep module rather than adding a new shallow one [06]
- [ ] If the feature requires touching many modules (change amplification), consider refactoring abstraction boundaries [06]
- [ ] Check source-code dependencies point inward toward domain logic, not outward toward frameworks or infrastructure [04]
- [ ] Identify the architecture quantum: what is the smallest independently deployable unit affected by this feature? [02][03]
- [ ] Verify bounded contexts align with the feature's scope — does the feature fit within one service boundary or require cross-service coordination? [03]
- [ ] Design the interface to be "somewhat general-purpose" — stable enough for future extension without interface changes, but not speculatively over-engineered [06]
- [ ] Apply "define errors out of existence" — broaden method specifications so formerly-error cases become valid behavior where possible [06]

## Phase 4: User Experience Design

- [ ] Verify every interactive element has a clear signifier — the user must be able to tell what is clickable and what it does [23]
- [ ] Walk through the Seven Stages of Action for the target user flow: Can they form the right goal? Figure out what to click? Tell what happened? Tell if they succeeded? [23]
- [ ] Check for natural mapping: controls are grouped near the things they affect [23]
- [ ] Design for scanning, not reading — use visual hierarchy, conventions, and clearly defined page areas [24]
- [ ] Apply Hick's Law: minimize choices at any single decision point; break complex selections into progressive steps [25]
- [ ] Apply Fitts's Law: primary actions should be large and easily reachable; destructive actions should be smaller and further away [25]
- [ ] Design error states using the slip vs. mistake taxonomy: undo for accidental actions, better conceptual models for wrong plans [23]
- [ ] Ensure the feature provides immediate, informative, non-excessive feedback at every interaction [23]

## Phase 5: Validation & Integration

- [ ] Plan the Walking Skeleton or tracer bullet: build a thin end-to-end slice before fleshing out the full feature [14]
- [ ] Define the instrumentation plan before shipping: what questions would you want to ask about this feature in production? [18]
- [ ] Verify the feature's architectural characteristics (performance, scalability, security) are compatible with the system's top 3-7 priorities [02]
- [ ] Document the design decision as an ADR capturing context, decision, and accepted tradeoffs [02][03]
- [ ] Plan for deploy-and-observe: actively monitor production telemetry after launch [18]
- [ ] For agent/AI features: use the simplest viable pattern (single LLM call before workflow, workflow before autonomous agent) [a01]

---

## Key Questions to Ask

1. "What are you giving up by building this feature?" — every feature is a tradeoff; name the downsides [02]
2. "Fall in love with the problem, not the solution" — can the problem be solved more simply? [29]
3. "What is the riskiest assumption, and have I tested it with the smallest possible experiment?" [31]
4. "How much is this feature worth in time?" — set appetite before estimating [30]
5. "Is this interface simpler than the implementation it hides?" — the deep module test [06]
6. "Would a new user be able to figure out this feature without instructions?" — the discoverability test [23]
7. "If this feature's dependencies are unavailable, what happens?" — design the degraded mode explicitly [17]
8. "What questions will I want to ask about this feature in production?" — define telemetry before shipping [18]
9. "Can the user tell what happened?" — the Gulf of Evaluation test for every state change [23]
10. "Is this the simplest architecture that meets these requirements?" — resist unnecessary complexity [02]

---

## Anti-Patterns to Flag

| Anti-Pattern | Signal | Source |
|---|---|---|
| **Solution-jumping** | Team commits to a feature before exploring the problem space or generating alternatives | [29][31] |
| **Feature factory** | Success measured by features shipped, not outcomes achieved — no learning loops | [29] |
| **Vague user story** | "As a user I want X" with no problem definition, success metrics, or appetite | [30] |
| **Over-specification** | Pitch includes wireframes, database schemas, and step-by-step plans — no room for builder decisions | [30] |
| **Shallow module addition** | New feature adds a thin wrapper class that just passes calls through — increases interfaces without absorbing complexity | [06] |
| **Temporal decomposition** | Code organized by execution order (read, parse, process) rather than by information to be hidden | [06] |
| **Tactical programming** | Getting the feature working as quickly as possible with no design investment — shortcuts accumulate within weeks | [06] |
| **Discovery theater** | Running user tests but ignoring results because the feature is already committed on the roadmap | [29] |
| **Ignoring the Gulf of Evaluation** | User performs an action but cannot tell what happened or whether it succeeded | [23] |
| **Cargo-cult complexity** | Choosing microservices or complex architecture because it is trendy rather than because driving characteristics demand it | [02][03] |
