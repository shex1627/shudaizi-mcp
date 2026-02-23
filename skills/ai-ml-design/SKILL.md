---
name: ai-ml-design
description: >
  Systematic AI/ML system design using AI Engineering (Chip Huyen), Designing ML Systems,
  LLM Engineer's Handbook, DDIA, LLM Security Playbook, and Anthropic engineering articles.
  Use when designing LLM applications, agent architectures, RAG pipelines, or ML systems.
---

## When to Activate

- User asks to design or architect an AI/ML system or LLM application
- User is building a RAG pipeline, agent system, or compound AI system
- User asks about LLM evaluation, fine-tuning decisions, or model selection
- User is integrating LLM capabilities into an existing application
- User asks about AI/ML security, trust boundaries, or guardrails

## Procedure

1. Read `knowledge/checklists/ai_ml_design.md`
2. Assess the system against each checklist phase relevant to the user's context
3. For items needing deeper context, read the cited book or article file (e.g., `book_research/09_ai_engineering_chip_huyen.md`, `book_research/anthropic_articles/01_building_effective_agents.md`)
4. Present findings organized as: **Approach Selection** -> **Architecture Recommendations** -> **Security Concerns** -> **Evaluation Strategy**
5. Cite the source book/article for each recommendation

## Always-Apply Principles

- Start with the simplest approach that works — single LLM call before workflow, workflow before agent [a01: Building Effective Agents]
- Evals are to AI engineering what tests are to software engineering — build them first [09: AI Engineering]
- The model is a component, not the product — design for model-portability [09: AI Engineering]
- Retrieval quality is the ceiling for RAG quality — diagnose retrieval before generation [09: AI Engineering]
- Treat LLM output the way you treat user input — validate and sanitize before downstream use [08: LLM Security Playbook]
- The blast radius of a compromised LLM is determined by its permissions, not the attack sophistication [08: LLM Security Playbook]
- Data quality bounds application quality — invest in data before model tuning [10: Designing ML Systems]
- Context should be curated for signal density, not maximum volume [a05: Context Engineering]
- Agent-computer interfaces deserve the same design rigor as human-computer interfaces [a01: Building Effective Agents]

## Deep-Dive References

- LLM application architecture & evals: `book_research/09_ai_engineering_chip_huyen.md`
- Production ML systems & monitoring: `book_research/10_designing_ml_systems.md`
- LLM pipeline engineering (FTI pattern): `book_research/11_llm_engineers_handbook.md`
- Data systems & consistency: `book_research/01_designing_data_intensive_applications.md`
- LLM security & trust boundaries: `book_research/08_llm_security_playbook.md`
- Agent patterns & ACI design: `book_research/anthropic_articles/01_building_effective_agents.md`
- Multi-agent architecture: `book_research/anthropic_articles/02_multi_agent_research_system.md`
- Agent SDK & loop patterns: `book_research/anthropic_articles/03_agent_sdk.md`
- Long-running agent harnesses: `book_research/anthropic_articles/04_long_running_agents.md`
- Context engineering strategies: `book_research/anthropic_articles/05_context_engineering.md`
- Tool design principles: `book_research/anthropic_articles/06_writing_effective_tools.md`
- Advanced tool use (search, programmatic calling): `book_research/anthropic_articles/07_advanced_tool_use.md`
- Code execution & filesystem-as-API: `book_research/anthropic_articles/08_code_execution_mcp.md`
- Think tool for sequential reasoning: `book_research/anthropic_articles/09_think_tool.md`
- Agent skills & progressive disclosure: `book_research/anthropic_articles/10_agent_skills.md`
