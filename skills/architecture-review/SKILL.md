---
name: architecture-review
description: >
  Systematic architecture review using DDIA, Fundamentals of Software Architecture, Clean Architecture,
  Philosophy of Software Design, Building Microservices, Release It, and more.
  Use when reviewing system design, evaluating ADRs, or assessing architectural tradeoffs.
---

## When to Activate

- User asks to review or critique a system architecture
- User presents a design document or ADR for feedback
- User asks about architectural tradeoffs or decisions
- User is designing a new system and wants guidance

## Procedure

1. Read `knowledge/checklists/architecture_review.md`
2. Assess the system against each checklist phase relevant to the user's context
3. For items needing deeper context, read the cited book file (e.g., `book_research/01_...md`)
4. Present findings organized as: **Strengths** → **Concerns** → **Recommendations**
5. Cite the source book/principle for each finding

## Always-Apply Principles

- Every architecture choice is a tradeoff — name both sides [01: DDIA]
- Complexity must justify itself — "what is this buying us?" [06: Philosophy of SW Design]
- Dependencies should point inward toward domain logic [04: Clean Architecture]
- "What happens if this component fails?" is the first question [17: Release It]
- Start with the simplest architecture that could work [02: Fundamentals of SW Arch]
- Service boundaries should align with bounded contexts [05: Building Microservices]

## Deep-Dive References

- Data systems & consistency: `book_research/01_designing_data_intensive_applications.md`
- Architecture styles & characteristics: `book_research/02_fundamentals_of_software_architecture.md`
- Decomposition decisions: `book_research/03_software_architecture_hard_parts.md`
- Dependency rules: `book_research/04_clean_architecture.md`
- Service boundaries: `book_research/05_building_microservices.md`
- Complexity management: `book_research/06_philosophy_of_software_design.md`
- Resilience patterns: `book_research/17_release_it.md`
- Observability: `book_research/18_observability_engineering.md`
- SRE practices: `book_research/19_site_reliability_engineering.md`
