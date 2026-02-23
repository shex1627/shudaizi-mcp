---
task: agent_design
description: Design, review, or improve an LLM-powered agent system — architecture, tools, context, evaluation, and production readiness
primary_sources: ["33"]
secondary_sources: ["09", "11"]
anthropic_articles: ["a01", "a02", "a03", "a04", "a05", "a06", "a07", "a08", "a09", "a10"]
version: 1
updated: 2026-02-22
---

# Agent Design Checklist

## Phase 1: Architecture Selection

- [ ] Start with the simplest pattern that works — single LLM call first, then workflows, then agents; add complexity only when measurably necessary [a01]
- [ ] Classify the task: is it well-defined (use a workflow) or open-ended (may need an agent)? Workflows = predefined code paths; agents = LLM-directed tool use [a01]
- [ ] Select the right workflow pattern for well-defined tasks: prompt chaining, routing, parallelization, orchestrator-workers, or evaluator-optimizer [a01]
- [ ] Use autonomous agents only when the task requires flexibility, ground truth comes from the environment, and clear success criteria exist [a01]
- [ ] For complex research or multi-file tasks, consider the orchestrator-worker pattern — it achieves 90% better performance than single-agent on research tasks [a02]
- [ ] When using multi-agent, spin up 3-5 subagents in parallel to cut research time by up to 90% [a02]
- [ ] Design the agent loop explicitly: Gather Context -> Take Action -> Verify Work -> Iterate [a03]
- [ ] Evaluate whether a compound AI system (retrieval + generation + validation) is needed vs. a single model call [09]

## Phase 2: Tool Design

- [ ] Apply the ACI principle: treat agent-computer interfaces with the rigor applied to human-computer interfaces [a01]
- [ ] Use selective tool design: fewer, more purposeful tools > numerous generic ones; consolidate related operations [a06]
- [ ] Implement clear namespacing for tools: hierarchical prefixes (e.g., `asana_projects_search`) reduce confusion [a06]
- [ ] Return meaningful context: replace UUIDs with human-readable fields; offer concise vs. detailed response formats [a06]
- [ ] Enforce token efficiency: pagination, filtering, sensible truncation (default ~25K tokens per tool response) [a06]
- [ ] Craft tool descriptions as prompt engineering — describe tools as you would to "a new hire"; precise specs dramatically improve performance [a06]
- [ ] For 10+ tools, use the Tool Search Tool pattern: load definitions on-demand, not all upfront — achieves 85% token reduction [a07]
- [ ] Consider programmatic tool calling: let Claude write Python to orchestrate tools with loops/conditionals, keeping intermediate results out of context (37% token reduction) [a07]
- [ ] Provide concrete tool-use examples beyond JSON schemas — improves accuracy from 72% to 90% on complex parameter handling [a07]

## Phase 3: Context Engineering

- [ ] Treat context as a finite attention budget — the goal is "the smallest possible set of high-signal tokens that maximize the likelihood of the desired outcome" [a05]
- [ ] Design system prompts at the right altitude: specific enough to guide, flexible enough for autonomy; avoid brittle if-else logic and vague platitudes [a05]
- [ ] Start with a minimal system prompt and add instructions based on observed failure modes, not hypothetical ones [a05]
- [ ] Use just-in-time context retrieval: maintain lightweight identifiers (file paths, URLs) and retrieve data during execution — progressive disclosure [a05]
- [ ] For long-horizon tasks, choose the right strategy: compaction for flow, structured note-taking for milestones, sub-agents for parallel research [a05]
- [ ] Subagents should write results to filesystem rather than passing through conversation history — prevents context bloat in the lead agent [a02]
- [ ] Use the filesystem as context engineering — agents navigate file hierarchies naturally for state management and tool discovery [a03] [a10]
- [ ] Monitor for context rot: performance degrades as context grows; periodically clear tool results or compact conversation history [a05]

## Phase 4: Skills & Progressive Disclosure

- [ ] Package procedural knowledge as agent skills: directories with SKILL.md files that agents discover and load dynamically [a10]
- [ ] Implement three-tier progressive disclosure: Level 1 (metadata in system prompt), Level 2 (full SKILL.md on relevance), Level 3+ (supplementary files on demand) [a10]
- [ ] Skills should be self-contained with YAML frontmatter (name, description), instructional body, and optional linked files [a10]
- [ ] For MCP integrations, present servers as code libraries via filesystem structure instead of direct tool calls — achieves 98.7% token reduction [a08]
- [ ] Develop skills using evaluation-driven development: build evals, then iterate skill content based on measured failures [a10]

## Phase 5: Evaluation & Testing

- [ ] Build evals before building the feature — teams without evals face reactive debugging loops [a11]
- [ ] Start with 20-50 tasks drawn from real failures, not synthetic benchmarks [a11]
- [ ] Write unambiguous task definitions: two experts should agree on pass/fail [a11]
- [ ] Use layered graders: code-based (fast, reproducible) + model-based (flexible) + human (gold standard) — the Swiss cheese model [a11]
- [ ] Track pass@k (at least one success in k trials) AND pass^k (all succeed) — a 75% per-trial rate yields only ~42% pass^3 [a11]
- [ ] Build balanced problem sets: test what agents should NOT do, not just what they should [a11]
- [ ] Account for infrastructure noise: 6-point benchmark swings from config alone; differences under 3% deserve skepticism [a12]
- [ ] For agent evals, use "evals are to AI engineering what tests are to software engineering" as the guiding principle [09]
- [ ] Run multiple trials per task to account for non-determinism; single-trial results are misleading [a11]

## Phase 6: Production Readiness

- [ ] For long-running agents, solve the "shift-change" problem: use an initializer agent (first session) and a coding agent (subsequent sessions) with structured state handoff [a04]
- [ ] Use JSON-formatted specs for task state — they resist accidental modification better than Markdown [a04]
- [ ] One feature/task per session outperforms attempting comprehensive implementation in one go [a04]
- [ ] Implement continuous production monitoring, not just pre-deployment testing — evals miss real-world degradation [a15]
- [ ] Set cost controls: step limits, budget caps, and timeouts for agentic loops that could run away [09]
- [ ] Design for model portability: the model is a component, not the product — own your data, evals, and orchestration [09]
- [ ] Agent reliability = tool reliability ^ number of steps; invest in per-step reliability before adding more steps [09]
- [ ] Remove anti-laziness prompts ("be thorough", "think carefully") on Claude 4.6 — they cause runaway thinking; use the `effort` parameter instead [33]

## Key Questions to Ask

1. "Is a single LLM call sufficient, or do I actually need an agent?" — most tasks do not need agent autonomy [a01]
2. "What is the simplest pattern that solves this?" — prompt chaining and routing handle most well-defined tasks [a01]
3. "How will I know if this agent is working correctly?" — if you cannot define success criteria and evals, do not build the agent [a11]
4. "What is the token budget and how is it managed?" — every token depletes the finite attention budget [a05]
5. "What happens when the agent fails mid-task?" — design recovery, checkpointing, and structured state for long-running work [a04]
6. "Who bears the complexity — the tool or the agent?" — well-designed tools absorb complexity from the agent's context [a06]
7. "Is the tool set bloated?" — fewer, focused tools outperform large catalogs; bloated tool sets encourage misuse [a06]

## Anti-Patterns

| Anti-Pattern | Why It Fails | Source |
|---|---|---|
| Complex multi-agent framework as the starting point | Simple patterns outperform; add complexity only when measured improvement justifies it | [a01] |
| Loading all tool definitions upfront | Wastes 85%+ of context window; use Tool Search for dynamic discovery | [a07] |
| Vague task descriptions to subagents | Causes duplication and wasted work; subagents need specific, detailed instructions | [a02] |
| Passing all results through conversation history | Context bloat; subagents should write to filesystem, lead agent reads summaries | [a02] [a05] |
| "CRITICAL: You MUST use this tool when..." | Causes overtriggering on newer models; use normal instructional language | [33] |
| Anti-laziness prompts on Claude 4.6 | "Be thorough", "think carefully" cause runaway thinking and token waste | [33] |
| Single-trial evaluation of non-deterministic agents | One run is not representative; use pass@k and pass^k across multiple trials | [a11] |
| Evals only at deploy time, not in production | Pre-deploy evals miss real-world degradation; continuous monitoring is essential | [a15] |
| Building without evals | "Teams without evals face reactive debugging loops" — invest in measurement first | [a11] |
