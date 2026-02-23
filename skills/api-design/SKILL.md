---
name: api-design
description: >
  Systematic API design and review using API Design Patterns (Geewax), Clean Architecture,
  Building Microservices, Philosophy of Software Design, DDIA, and Anthropic's tool design articles.
  Use when designing new APIs, reviewing API surface area, or building tools for AI agents.
---

## When to Activate

- User asks to design a new API or set of endpoints
- User wants to review or critique an existing API surface
- User needs help with pagination, versioning, error handling, or resource modeling decisions
- User is designing tools or MCP servers for AI agents
- User asks about backwards compatibility or API evolution strategy

## Procedure

1. Read `knowledge/checklists/api_design.md`
2. Assess the API design against each relevant checklist phase (resource modeling, standard methods, pagination/errors, versioning, consistency, agent compatibility)
3. For items needing deeper context, read the cited book file (e.g., `book_research/20_api_design_patterns.md`)
4. Present findings organized as: **Resource Model Assessment** -> **Operation Design** -> **Evolution & Consistency** -> **Risk Areas**
5. Cite the source book/principle for each finding

## Always-Apply Principles

- APIs expose resources, not actions — if you need a verb in the URL, it should be a justified custom method, not the default [20: API Design Patterns]
- Field masks make intentions explicit — the difference between "updating this field" and "sending the full object" is the source of countless API bugs [20: API Design Patterns]
- Consistency across an API surface is worth more than local optimization — if 49 of 50 resources paginate the same way, the 50th should too [20: API Design Patterns]
- The interface should be simpler than its implementation — every API module must absorb significant complexity to justify its existence [06: Philosophy of SW Design]
- Source-code dependencies point inward — domain logic must not depend on API transport or framework details [04: Clean Architecture]
- Tools are a contract between deterministic systems and non-deterministic agents — treat agent-computer interfaces with the rigor applied to human-computer interfaces [a06: Writing Effective Tools]

## Deep-Dive References

- Resource-oriented design, standard methods, pagination, versioning: `book_research/20_api_design_patterns.md`
- Deep modules & interface simplicity: `book_research/06_philosophy_of_software_design.md`
- Dependency rule & clean boundaries: `book_research/04_clean_architecture.md`
- Service decomposition & bounded contexts: `book_research/05_building_microservices.md`
- Data consistency & isolation levels: `book_research/01_designing_data_intensive_applications.md`
- Tool design principles for agents: `book_research/anthropic_articles/06_writing_effective_tools.md`
- Tool search, programmatic calling, token efficiency: `book_research/anthropic_articles/07_advanced_tool_use.md`
