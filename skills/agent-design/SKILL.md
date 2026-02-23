---
name: agent-design
description: >
  Agent design using Anthropic's engineering blog, AI Engineering (Huyen), and LLM Engineer's Handbook.
  Use when designing, reviewing, or improving LLM-powered agent systems — architecture, tool design, context engineering, evaluation, and production deployment.
---

## When to Activate

- User asks to design or review an LLM agent or agentic workflow
- User is choosing between workflow patterns (chaining, routing, parallelization, orchestrator-workers)
- User is designing tools for agent use (function calling, MCP servers, tool descriptions)
- User is building context engineering strategies (system prompts, progressive disclosure, compaction)
- User asks about agent evaluation, non-deterministic testing, or benchmark design
- User is building agent skills, SKILL.md files, or progressive disclosure architectures
- User is debugging agent failures, context rot, or runaway token usage

## Procedure

1. Read `knowledge/checklists/agent_design.md`
2. Determine the design phase:
   - **New agent**: Start with Phase 1 (architecture) — resist complexity; prove a simple pattern is insufficient before escalating
   - **Tool issues**: Phase 2 (tool design) — apply the five design principles; check for bloat
   - **Context/performance issues**: Phase 3 (context engineering) — audit token usage, check for context rot
   - **Quality issues**: Phase 5 (evaluation) — build evals first, then iterate
   - **Production issues**: Phase 6 (production readiness) — check state management, monitoring, cost controls
3. For items needing deeper context, read the cited article or book file
4. Present recommendations as: **Architecture decisions** -> **Implementation details** -> **Evaluation plan**
5. Always recommend starting with the simplest viable pattern and measuring before adding complexity

## Always-Apply Principles

- "Simple, composable patterns rather than complex frameworks" — start with the simplest pattern that works and add complexity only when measurably necessary [a01: Building Effective Agents]
- "Treat agent-computer interfaces with the rigor applied to human-computer interfaces" — tool design deserves the same care as UI/UX design [a01]
- "The smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome" — context is a finite attention budget; curate ruthlessly [a05: Context Engineering]
- "Teams without evals face reactive debugging loops; teams investing early experience accelerated development" — build evals before building the agent [a11: Demystifying Evals]
- "Agent reliability = tool reliability ^ number of steps" — invest in per-step reliability before adding more steps [09: AI Engineering]

## Deep-Dive References

- Agent architecture patterns (5+1): `book_research/anthropic_articles/01_building_effective_agents.md`
- Multi-agent orchestrator-worker pattern: `book_research/anthropic_articles/02_multi_agent_research_system.md`
- Agent SDK and the gather-act-verify loop: `book_research/anthropic_articles/03_agent_sdk.md`
- Context engineering strategies: `book_research/anthropic_articles/05_context_engineering.md`
- Tool design five principles: `book_research/anthropic_articles/06_writing_effective_tools.md`
- Advanced tool use (search, programmatic, examples): `book_research/anthropic_articles/07_advanced_tool_use.md`
- Agent skills and progressive disclosure: `book_research/anthropic_articles/10_agent_skills.md`
- Evaluation framework and 8-step roadmap: `book_research/anthropic_articles/11_demystifying_evals.md` (via `book_research/33_anthropic_engineering_blog.md`)
- Infrastructure noise in benchmarks: `book_research/anthropic_articles/12_infrastructure_noise.md`
- Production monitoring lessons: `book_research/anthropic_articles/15_postmortem.md`
- AI engineering patterns (evals, RAG, agents): `book_research/09_ai_engineering_chip_huyen.md`
- LLM pipeline architecture (FTI pattern): `book_research/11_llm_engineers_handbook.md`
- Consolidated Anthropic blog reference: `book_research/33_anthropic_engineering_blog.md`
