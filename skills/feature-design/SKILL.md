---
name: feature-design
description: >
  Systematic feature design from problem discovery through scoping, UX design, and technical architecture
  using Philosophy of Software Design, Inspired (Cagan), Shape Up (Singer), Continuous Discovery Habits (Torres),
  and foundational architecture and UX references. Use when designing new features, scoping product work,
  or evaluating feature proposals.
---

## When to Activate

- User asks to design a new feature or product capability
- User presents a feature idea and wants structured feedback
- User needs help scoping work or defining an MVP
- User asks about discovery, opportunity mapping, or user research framing
- User wants to evaluate a product proposal or feature spec

## Procedure

1. Read `knowledge/checklists/feature_design.md`
2. Assess the feature proposal against each relevant checklist phase (discovery, scoping, technical design, UX, validation)
3. For items needing deeper context, read the cited book file (e.g., `book_research/29_inspired_cagan.md`)
4. Present findings organized as: **Problem Clarity** -> **Scoping Assessment** -> **Design Recommendations** -> **Risk Areas**
5. Cite the source book/principle for each finding

## Always-Apply Principles

- "Fall in love with the problem, not the solution" — explore the opportunity space before committing to a solution [29: Inspired]
- Set an appetite before estimating — "How much is this worth?" constrains the design to fit reality [30: Shape Up]
- Generate at least three solution concepts before selecting one to prevent first-idea bias [31: Continuous Discovery]
- Interfaces should be simpler than their implementations — every new module must absorb significant complexity to justify its existence [06: Philosophy of SW Design]
- Design for the user's mental model, not the engineer's — every interaction must be discoverable and provide clear feedback [23: Design of Everyday Things]

## Deep-Dive References

- Complexity management & interface design: `book_research/06_philosophy_of_software_design.md`
- Product discovery & empowered teams: `book_research/29_inspired_cagan.md`
- Appetite-based scoping & shaping: `book_research/30_shape_up.md`
- Opportunity mapping & assumption testing: `book_research/31_continuous_discovery_habits.md`
- Architecture styles & characteristics: `book_research/02_fundamentals_of_software_architecture.md`
- Decomposition & service boundaries: `book_research/03_software_architecture_hard_parts.md`
- Dependency rule & clean boundaries: `book_research/04_clean_architecture.md`
- Affordances, signifiers & error design: `book_research/23_design_of_everyday_things.md`
- Web usability & scanning: `book_research/24_dont_make_me_think.md`
- Cognitive psychology laws for UI: `book_research/25_laws_of_ux.md`
- Agent architecture patterns: `book_research/anthropic_articles/01_building_effective_agents.md`
