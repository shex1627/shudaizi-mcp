# Anthropic Engineering Blog — Research Reference
**Category:** LLM / AI Engineering — Anthropic-Specific
**Relevance to AI-assisted / vibe-coding workflows:** Direct source material from the creators of Claude — the most authoritative reference for building applications with Claude models, prompt engineering, agent design, and responsible AI deployment.
**Sources:** All content sourced directly from anthropic.com/engineering and docs.anthropic.com via web fetch, Feb 2026.

---

## Overview

Anthropic's engineering blog (https://www.anthropic.com/engineering) is the primary source for practical guidance on building with Claude. As of February 2026, it contains 18+ articles spanning agent design, context engineering, evaluation, tool design, security, and production patterns. The blog complements the official API docs at docs.anthropic.com and the research blog at anthropic.com/research.

The content is uniquely valuable because it reflects lessons learned from building Claude Code itself — Anthropic's own agentic coding product — making it first-party operational knowledge rather than theoretical guidance.

---

## Complete Article Index

| # | Title | Date | URL |
|---|-------|------|-----|
| 1 | Quantifying infrastructure noise in agentic coding evals | Feb 2026 | anthropic.com/engineering/infrastructure-noise |
| 2 | Building a C compiler with a team of parallel Claudes | Feb 05, 2026 | anthropic.com/engineering/building-c-compiler |
| 3 | Designing AI-resistant technical evaluations | Jan 21, 2026 | anthropic.com/engineering/AI-resistant-technical-evaluations |
| 4 | Demystifying evals for AI agents | Jan 09, 2026 | anthropic.com/engineering/demystifying-evals-for-ai-agents |
| 5 | Effective harnesses for long-running agents | Nov 26, 2025 | anthropic.com/engineering/effective-harnesses-for-long-running-agents |
| 6 | Introducing advanced tool use | Nov 24, 2025 | anthropic.com/engineering/advanced-tool-use |
| 7 | Code execution with MCP: Building more efficient agents | Nov 04, 2025 | anthropic.com/engineering/code-execution-with-mcp |
| 8 | Beyond permission prompts: Claude Code sandboxing | Oct 20, 2025 | anthropic.com/engineering/claude-code-sandboxing |
| 9 | Effective context engineering for AI agents | Sep 29, 2025 | anthropic.com/engineering/effective-context-engineering-for-ai-agents |
| 10 | A postmortem of three recent issues | Sep 17, 2025 | anthropic.com/engineering/a-postmortem-of-three-recent-issues |
| 11 | Writing effective tools for agents — with agents | Sep 11, 2025 | anthropic.com/engineering/writing-tools-for-agents |
| 12 | Desktop Extensions: One-click MCP installation | Jun 26, 2025 | anthropic.com/engineering/desktop-extensions |
| 13 | How we built our multi-agent research system | Jun 13, 2025 | anthropic.com/engineering/multi-agent-research-system |
| 14 | Claude Code: Best practices for agentic coding | Apr 18, 2025 | anthropic.com/engineering/claude-code-best-practices |
| 15 | The "think" tool | Mar 20, 2025 | anthropic.com/engineering/claude-think-tool |
| 16 | Raising the bar on SWE-bench Verified | Jan 06, 2025 | anthropic.com/engineering/swe-bench-sonnet |
| 17 | Building effective agents | Dec 19, 2024 | anthropic.com/engineering/building-effective-agents |
| 18 | Introducing Contextual Retrieval | Sep 19, 2024 | anthropic.com/engineering/contextual-retrieval |

Additional key resources:
- Equipping agents for the real world with Agent Skills (Dec 18, 2025) — claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills
- Building agents with the Claude Agent SDK (Sep 29, 2025) — claude.com/blog/building-agents-with-the-claude-agent-sdk
- Claude 4 best practices (docs) — platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices

---

## Key Articles & Their Core Ideas

### 1. Agent Design & Architecture

#### Building Effective Agents (Dec 19, 2024)
**URL:** https://www.anthropic.com/research/building-effective-agents
**Core thesis:** The most successful agent implementations use simple, composable patterns rather than complex frameworks. Start simple, add complexity only when measurably necessary.

**Key architectural distinction:**
- **Workflows** = LLMs orchestrated through predefined code paths
- **Agents** = LLMs dynamically directing their own processes and tool usage

**The 5 workflow patterns + 1 agent pattern:**

1. **Prompt Chaining** — Sequential steps where each LLM call processes previous output. Best for tasks cleanly decomposable into fixed subtasks. Example: generate outline → validate → write full document.

2. **Routing** — Classify inputs, direct to specialized downstream tasks. Example: route simple questions to Haiku, complex ones to Sonnet/Opus.

3. **Parallelization** — Two variants:
   - *Sectioning*: independent subtasks run simultaneously (e.g., guardrails + query processing)
   - *Voting*: identical tasks run multiple times for diverse outputs (e.g., code vulnerability review)

4. **Orchestrator-Workers** — Central LLM dynamically breaks tasks into subtasks, delegates to workers, synthesizes results. Key advantage: subtasks determined by input, not predefined.

5. **Evaluator-Optimizer** — One LLM generates, another evaluates in a loop. Effective when clear evaluation criteria exist.

6. **Autonomous Agents** — LLMs using tools in feedback loops. Require: ground truth from environment, clear success criteria, sandboxed environments, appropriate guardrails.

**Decision framework:** Start with single LLM calls → workflows for well-defined tasks → agents only for open-ended problems requiring flexibility.

**Tool design principle (ACI):** "Treat agent-computer interfaces with the rigor applied to human-computer interfaces." Anthropic's SWE-bench agent spent more time optimizing tools than the overall prompt. Example: requiring absolute filepaths instead of relative paths eliminated a class of errors.

---

#### How We Built Our Multi-Agent Research System (Jun 13, 2025)
**URL:** https://www.anthropic.com/engineering/multi-agent-research-system
**Core thesis:** Multi-agent orchestrator-worker pattern achieves 90.2% better performance than single-agent Claude Opus 4 on research tasks.

**Key findings:**
- **Token usage explains 80% of variance** in research task success
- Multi-agent systems consume ~15x more tokens than standard chat but justify costs on complex tasks
- Spinning up 3-5 subagents in parallel and enabling parallel tool calls **cut research time by up to 90%**
- Subagents should write results to filesystem rather than passing through conversation history
- Lead agents require detailed task descriptions — vague instructions cause duplication

**Evaluation insight:** Start with ~20 representative queries, not hundreds. A single LLM-as-judge proved more consistent than multiple specialized judges. Human validation still essential — automated evals missed agents favoring "SEO-optimized content farms over authoritative sources."

---

#### Building Agents with the Claude Agent SDK (Sep 29, 2025)
**URL:** https://claude.com/blog/building-agents-with-the-claude-agent-sdk
**Core principle:** "Agents work best when given access to a computer." The agent loop: Gather Context → Take Action → Verify Work.

**Key capabilities:**
- *Context retrieval*: agentic search (grep, tail), semantic search, subagents for parallel work, compaction for long conversations
- *Action*: custom tools, bash scripts, code generation, MCP integrations
- *Verification*: rules-based feedback, visual feedback (screenshots), LLM-as-judge

**Design insight:** The SDK "treats file systems as a form of context engineering" — agents navigate information hierarchies naturally rather than requiring pre-engineered retrieval.

---

#### Effective Harnesses for Long-Running Agents (Nov 26, 2025)
**URL:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
**Core problem:** Agents lose memory across context windows — the "shift-change" problem.

**Two-part solution:**
- **Initializer Agent** (first session): creates init.sh, progress.txt, feature list, baseline git commit
- **Coding Agent** (subsequent sessions): works on single features sequentially, commits with descriptive messages, updates progress docs

**Key findings:**
- JSON-formatted feature specs resist accidental modification better than Markdown
- One feature per session >> attempting comprehensive implementation
- Agents testing like human users (Puppeteer) catch issues code-level testing misses
- Standard startup: verify directory → read progress + git history → run basic tests → select next feature

---

### 2. Context Engineering

#### Effective Context Engineering for AI Agents (Sep 29, 2025)
**URL:** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
**Core thesis:** Context engineering is "the set of strategies for curating and maintaining the optimal set of tokens during LLM inference." The goal: "the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."

**Why it matters:**
- Models experience "context rot" — performance degrades as context grows
- Transformers require n² pairwise token relationships — computational strain at scale
- Models have less training experience with longer sequences

**System prompt design:**
- Strike the "right altitude" — specific enough to guide, flexible enough for autonomy
- Avoid two extremes: brittle hardcoded logic vs. vague high-level guidance
- Start minimal, add instructions based on observed failure modes
- Use XML tags or Markdown headers to organize sections

**Tool design for context:**
- Self-contained, unambiguous, minimal overlap in functionality
- Token-efficient responses, clear input parameters
- Bloated tool sets encourage misuse and waste context

**Context retrieval strategies:**
- **Just-In-Time**: maintain lightweight identifiers (file paths, URLs), use tools to retrieve data during execution — "progressive disclosure"
- **Hybrid**: pre-load critical data (CLAUDE.md files) + autonomous exploration via tools

**Long-horizon techniques:**
- **Compaction**: summarize conversation history when approaching limits; tool result clearing is the "safest lightest touch"
- **Structured Note-Taking**: agent periodically writes persistent notes outside context window; pulled back when needed
- **Sub-Agent Architectures**: specialized agents with clean context windows; return condensed summaries (1,000-2,000 tokens)

**Selection guidance:**
- Compaction → extended back-and-forth requiring flow
- Note-Taking → iterative development with clear milestones
- Multi-Agent → complex research requiring parallel work

---

### 3. Tool Design & MCP

#### Writing Effective Tools for Agents (Sep 11, 2025)
**URL:** https://www.anthropic.com/engineering/writing-tools-for-agents
**Core insight:** "Tools are a new kind of software which reflects a contract between deterministic systems and non-deterministic agents."

**Five design principles:**
1. **Selective Tool Design** — fewer, more purposeful tools > numerous generic ones. Consolidate related operations.
2. **Clear Namespacing** — hierarchical organization (e.g., "asana_projects_search")
3. **Meaningful Context Returns** — semantic clarity over technical detail; replace UUIDs with natural language; offer "concise" vs "detailed" response formats
4. **Token Efficiency** — pagination, filtering, sensible truncation (Claude Code defaults to 25,000 tokens per tool response)
5. **Prompt Engineering Descriptions** — precise naming, clear specs, contextual examples dramatically impact performance

**Development process:** Prototype → build comprehensive evals → optimize with Claude analyzing transcripts. "Most of the advice in this post came from repeatedly optimizing our internal tool implementations with Claude Code."

---

#### Advanced Tool Use (Nov 24, 2025)
**URL:** https://www.anthropic.com/engineering/advanced-tool-use
**Three new features:**

1. **Tool Search Tool** — dynamic discovery instead of loading all definitions upfront. 85% reduction in token usage (55K+ tokens saved). Opus 4.5 improved from 79.5% to 88.1% accuracy.

2. **Programmatic Tool Calling** — Claude writes Python scripts to orchestrate tools with loops, conditionals, data transformations. Reduced token usage by 37% on complex tasks. 200KB intermediate results → 1KB.

3. **Tool Use Examples** — concrete usage patterns beyond JSON schemas. Improved accuracy from 72% to 90% on complex parameter handling.

---

#### Code Execution with MCP (Nov 04, 2025)
**URL:** https://www.anthropic.com/engineering/code-execution-with-mcp
**Core pattern:** Present MCP servers as code libraries via filesystem structure instead of direct tool calls. Agents discover tools by exploring directories.

**Results:** 150,000 tokens → 2,000 tokens (98.7% reduction).

**Key benefits:**
- Progressive disclosure — models navigate filesystems, reading definitions on-demand
- Data filtering in execution environment before returning results
- Loops/conditionals execute natively in code, not via chained tool calls
- Intermediate results stay in execution environment (privacy preservation)
- State persistence via files enables resumable workflows

---

#### The "Think" Tool (Mar 20, 2025)
**URL:** https://www.anthropic.com/engineering/claude-think-tool
**What it is:** A designated space for Claude to pause and reflect during tool-use sequences (different from extended thinking which occurs before response generation).

**When to use:** Tool output analysis, policy-heavy environments, sequential decision-making.
**When NOT useful:** Non-sequential tool calls, simple instruction-following.

**Results:** 54% relative improvement on airline domain (τ-Bench), 1.6% on SWE-bench.

**Note (Dec 2025 update):** Extended thinking has improved enough that it's recommended over the think tool in most cases, though think tool remains valuable for complex sequential tool use.

---

#### Agent Skills (Dec 18, 2025)
**URL:** https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills

**What they are:** Organized directories of instructions, scripts, and resources that agents discover and load dynamically.

**Progressive disclosure architecture:**
- Level 1 (Metadata): skill name/description in system prompt — signals availability
- Level 2 (Core Content): full SKILL.md loaded when relevant
- Level 3+ (Supplementary): additional files loaded on-demand

**Key insight:** "The amount of context that can be bundled into a skill is effectively unbounded" because agents load information on-demand via filesystem access.

**Best practices:** evaluation-driven development, split unwieldy files, monitor real usage patterns, ask Claude to self-reflect on mistakes.

---

### 4. Evaluation & Testing

#### Demystifying Evals for AI Agents (Jan 09, 2026)
**URL:** https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
**Core thesis:** Teams without evals face reactive debugging loops; teams investing early experience accelerated development.

**Key terminology:**
- Task = single test with defined inputs and success criteria
- Trial = one attempt at a task (run multiple for consistency)
- Grader = logic scoring performance (code-based, model-based, or human)
- Transcript = complete record including outputs, tool calls, reasoning

**Three types of graders:**
- **Code-based**: string matching, regex, binary tests, static analysis — fast, cheap, reproducible but brittle
- **Model-based**: rubric scoring, pairwise comparison, multi-judge consensus — flexible but non-deterministic
- **Human**: gold standard but expensive and slow

**Critical metrics for non-determinism:**
- **Pass@k** = probability of at least one correct solution in k attempts (increases with k)
- **Pass^k** = probability ALL k trials succeed (decreases with k). A 75% per-trial rate yields only ~42% pass^3.

**8-step roadmap:**
1. Start early with 20-50 tasks from real failures
2. Convert manual pre-release checks into test cases
3. Write unambiguous tasks (two experts should agree on pass/fail)
4. Build balanced problem sets (test presence AND absence)
5. Establish robust infrastructure (clean environments per trial)
6. Design thoughtful graders (avoid overly brittle step-sequence checking)
7. Monitor for saturation (refresh with harder tasks)
8. Maintain long-term (treat as living artifacts)

**Swiss cheese model:** No single evaluation method catches everything — layer automated evals, production monitoring, A/B testing, user feedback, manual transcript review.

---

#### Quantifying Infrastructure Noise in Agentic Coding Evals (Feb 2026)
**URL:** https://www.anthropic.com/engineering/infrastructure-noise
**Core finding:** Infrastructure configuration alone can produce 6 percentage point differences on benchmarks — often exceeding leaderboard margins.

**Key insight:** "Leaderboard differences below 3 percentage points deserve skepticism until the eval configuration is documented and matched."

**Recommendation:** Specify dual parameters (guaranteed allocation + hard kill limits), calibrate at 3x ceiling, document all configuration.

---

#### Designing AI-Resistant Technical Evaluations (Jan 21, 2026)
**URL:** https://www.anthropic.com/engineering/AI-resistant-technical-evaluations
**Problem:** Anthropic's performance engineering take-home required 3 redesigns since early 2024 because successive Claude models defeated each iteration.

**Key findings:**
- Knowledge-based problems fail fastest (sufficient training data)
- Out-of-distribution problems persist longer but sacrifice job-realism
- Human advantage persists at unlimited time horizons on novel problems
- Prioritize novelty over realism; include multiple independent sub-problems

---

### 5. Production Engineering & Security

#### Claude Code Sandboxing (Oct 20, 2025)
**URL:** https://www.anthropic.com/engineering/claude-code-sandboxing
**Two-boundary approach:**
1. **Filesystem Isolation** — Claude can only access/modify specific directories
2. **Network Isolation** — Claude can only connect to approved servers

Both boundaries essential: network isolation alone allows SSH key theft; filesystem isolation alone enables sandbox escape. Uses OS-level primitives (Linux bubblewrap, macOS seatbelt). Reduced permission prompts by 84%.

---

#### A Postmortem of Three Recent Issues (Sep 17, 2025)
**URL:** https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues
**Three bugs in Aug-Sep 2025:**

1. **Context window routing error** — Sonnet 4 requests misrouted to 1M-token servers; affected up to 16% of requests at peak
2. **Output corruption** — Runtime optimization occasionally assigned high probability to wrong tokens (e.g., Thai characters in English responses)
3. **XLA:TPU compiler miscompilation** — Mixed precision arithmetic caused incorrect top-k token selection

**Why detection was hard:** Eval gaps, privacy constraints on user data, overlapping symptoms, noisy baselines.

**Lessons:** More sensitive evals, continuous production monitoring (not just pre-deployment), faster debugging tools, user feedback integration.

---

#### Building a C Compiler with Parallel Claudes (Feb 05, 2026)
**URL:** https://www.anthropic.com/engineering/building-c-compiler
**Architecture:** 16 parallel Claude agents in Docker containers with shared Git repo. Task-locking via text files prevents duplicate work. Role-based specialization (core dev, dedup, optimization, review, docs).

**Results:** ~2 billion input tokens across ~2,000 sessions over two weeks (~$20,000). Produced 100,000-line Rust compiler building Linux 6.9 across x86, ARM, RISC-V.

---

### 6. RAG & Retrieval

#### Introducing Contextual Retrieval (Sep 19, 2024)
**URL:** https://www.anthropic.com/news/contextual-retrieval
**Core technique:** Prepend chunk-specific explanatory context to each chunk before embedding and BM25 indexing.

**Example:** Instead of "revenue grew by 3%", index as "This chunk discusses ACME Corp's Q2 2023 performance; previous quarter revenue was $314M. The company's revenue grew by 3%."

**Performance:**
- Contextual Embeddings alone: 35% reduction in retrieval failures
- Combined with BM25: 49% reduction
- With reranking: 67% reduction

**Implementation:** Claude generates 50-100 token contextual summaries per chunk. Prompt caching reduces cost to ~$1.02 per million document tokens. Include 20 chunks (not 5 or 10) for optimal downstream performance.

---

### 7. Prompt Engineering Best Practices (Claude 4.6)

**Source:** https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices

#### General Principles
- **Be explicit** — if you want "above and beyond" behavior, explicitly request it
- **Add context/motivation** — explain WHY, not just WHAT. Claude generalizes from explanations.
- **Be vigilant with examples** — Claude follows examples precisely; ensure they model desired behavior

#### Claude 4.6-Specific Guidance

**Long-horizon reasoning:**
- Claude 4.6 excels at multi-context-window workflows with state tracking
- Context awareness lets Claude track remaining token budget
- Key prompt: "Your context window will be automatically compacted... do not stop tasks early due to token budget concerns"

**Multi-context window workflows:**
1. Use different prompt for first context window (setup: write tests, create scripts)
2. Have model write tests in structured format (tests.json)
3. Set up quality-of-life tools (init.sh)
4. Consider starting fresh vs. compacting — Claude discovers state well from filesystem
5. Provide verification tools (Playwright, computer use)
6. Encourage complete usage of context

**Communication style:** More concise, direct, grounded. May skip verbal summaries after tool calls. Add "provide a quick summary of the work you've done" if you want visibility.

**Tool usage:** Claude 4.6 follows instructions precisely. "Can you suggest changes" → suggestions only. "Make these changes" → implementation. Use system prompt to set default behavior.

**Overtriggering fix:** Claude 4.6 is more responsive to system prompts. Replace "CRITICAL: You MUST use this tool when..." with "Use this tool when...".

**Overthinking fix:** Remove anti-laziness prompts ("be thorough", "think carefully"). Remove explicit think tool instructions. Use `effort` parameter as primary control lever. If still too aggressive, add: "Prioritize execution over deliberation."

**Parallel tool calling:** Claude 4.6 excels at this. Steerable to ~100% with prompt guidance.

**Adaptive thinking:** Claude 4.6 uses `thinking: {type: "adaptive"}` instead of manual `budget_tokens`. Use `effort` parameter (low/medium/high/max) to control depth.

**Prefilled responses deprecated:** Claude 4.6 no longer supports prefills on last assistant turn. Migrate to: structured outputs, direct instructions, XML tags, or tool calling.

**Subagent orchestration:** Claude 4.6 proactively delegates to subagents. May overuse — add guidance: "Use subagents when tasks can run in parallel or require isolated context. For simple tasks, work directly."

**Overengineering tendency:** Add explicit guidance to keep solutions minimal — "Don't add features, refactor code, or make improvements beyond what was asked."

---

## Patterns & Approaches Across Articles

### Recurring Themes

1. **Start simple, add complexity only when measured** — appears in Building Effective Agents, Context Engineering, Multi-Agent Research, Evals. The consistent message: resist the urge to build complex architectures before proving simpler approaches insufficient.

2. **Progressive disclosure** — the dominant pattern across Agent Skills, Code Execution with MCP, Context Engineering. Load information only when needed rather than upfront.

3. **Filesystem as context engineering** — agents navigate file hierarchies naturally. Appears in Agent SDK, Agent Skills, Code Execution with MCP, Long-Running Agents. Files serve as persistent memory, tool discovery, and state management.

4. **Tools matter more than prompts** — the SWE-bench finding that tool optimization outweighed prompt optimization. Echoed in Writing Tools for Agents, Advanced Tool Use, Multi-Agent Research.

5. **Token efficiency as a first-class concern** — every article addresses token management. Advanced Tool Use achieves 85-98% reductions. Context Engineering frames tokens as "finite attention budget."

6. **Evals are the foundation** — from "start with 20-50 tasks" to "Swiss cheese model." Multiple articles emphasize that without measurement, you cannot improve.

7. **Human-in-the-loop remains essential** — even the most autonomous systems (C compiler project, multi-agent research) emphasize human review for alignment, quality, and catching subtle failures.

---

## Tradeoffs & Tensions

1. **Autonomy vs. Safety** — Claude 4.6 is more proactive but may take irreversible actions. The sandboxing article and prompt engineering guide address this with dual isolation and explicit confirmation prompts.

2. **Token usage vs. quality** — Multi-agent research uses 15x more tokens but achieves 90% better results. Advanced Tool Use reduces tokens 85-98%. The right tradeoff depends on task value.

3. **Simplicity vs. capability** — Building Effective Agents says start simple. But multi-agent research, long-running harnesses, and agent skills all add substantial complexity. The key: measure whether complexity improves outcomes.

4. **Thorough exploration vs. speed** — Claude 4.6 does significantly more upfront exploration. Sometimes helpful, sometimes wasteful. Use `effort` parameter as the control lever.

5. **Structured vs. unstructured state** — JSON for test results and task status; freeform text for progress notes; git for checkpoints. Different state types need different formats.

6. **Compaction vs. fresh start** — Claude's latest models are "extremely effective at discovering state from the local filesystem." Sometimes starting fresh beats compaction.

---

## What to Watch Out For

1. **Over-engineering agent architectures** — the most common mistake. Use workflows before agents, single agents before multi-agent.

2. **Bloated tool sets** — "encourage misuse and wasted context." Fewer, focused tools outperform large catalogs.

3. **Ignoring infrastructure in evals** — 6 percentage point differences from config alone. Leaderboard gaps under 3% are noise.

4. **Anti-laziness prompts on Claude 4.6** — "be thorough," "think carefully" cause runaway thinking. Remove them.

5. **Aggressive tool-triggering language** — "CRITICAL: You MUST" causes overtriggering on newer models. Use normal language.

6. **Testing only happy paths** — eval suites need balanced problem sets. Test what agents should NOT do, not just what they should.

7. **Relying on a single evaluation method** — Swiss cheese model. Layer automated evals, production monitoring, human review, user feedback.

8. **Ignoring the shift-change problem** — long-running agents need explicit progress tracking, structured state, and clean handoff protocols.

---

## Applicability by Task Type

### Architecture Planning (AI Systems)
- Building Effective Agents: choose workflow vs. agent pattern
- Multi-Agent Research: orchestrator-worker for complex research
- Context Engineering: design context flow upfront
- Agent Skills: progressive disclosure architecture

### Prompt Engineering
- Claude 4 Best Practices: the definitive guide for Claude 4.6
- Context Engineering: system prompt design principles
- Think Tool: when structured reflection helps

### Agent Design
- Building Effective Agents: the 5+1 pattern catalog
- Agent SDK: the gather-act-verify loop
- Long-Running Agents: harness design for multi-session work
- Agent Skills: capability extension via files

### RAG Pipeline Design
- Contextual Retrieval: the technique that reduces failures 49-67%
- Context Engineering: just-in-time vs. hybrid retrieval

### Evaluation & Testing
- Demystifying Evals: the complete framework (8-step roadmap)
- Infrastructure Noise: controlling for config variation
- AI-Resistant Evaluations: designing for advancing AI capabilities

### Tool Design
- Writing Tools for Agents: five design principles
- Advanced Tool Use: search, programmatic calling, examples
- Code Execution with MCP: filesystem-as-API pattern

### Security & Safety
- Claude Code Sandboxing: dual-boundary isolation model
- Agent Skills: security considerations for capability extension
- Postmortem: production monitoring and debugging lessons

### Production Deployment
- Postmortem: what can go wrong and how to detect it
- Long-Running Agents: session management and state persistence
- Multi-Agent Research: rainbow deployments, observability
- Infrastructure Noise: reproducible eval infrastructure

---

## Freshness Assessment

- **Published:** Sep 2024 — Feb 2026 (actively updated)
- **Core ideas that remain highly relevant:** All agent design patterns, context engineering principles, eval frameworks, tool design principles
- **Rapidly evolving areas:** Model-specific prompt engineering (changes with each model generation), thinking mode configuration, effort parameters, MCP ecosystem
- **What to re-check frequently:** Claude 4 best practices page (updated with each model release), advanced tool use features (actively expanding), agent SDK capabilities
- **Coverage gaps:** Limited coverage of fine-tuning, cost optimization strategies, multi-modal agent patterns, production monitoring tooling

---

## Key Framings Worth Preserving

1. **"Simple, composable patterns rather than complex frameworks"** — the agent design philosophy. Start with the simplest pattern that works.

2. **"The smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome"** — the context engineering objective function.

3. **"Tools are a new kind of software which reflects a contract between deterministic systems and non-deterministic agents"** — reframes tool design as a new discipline.

4. **"Treat agent-computer interfaces with the rigor applied to human-computer interfaces"** — tool design deserves the same care as UI/UX design.

5. **"Token usage by itself explains 80% of the variance"** — in multi-agent research quality. Invest tokens where they matter.

6. **"Leaderboard differences below 3 percentage points deserve skepticism"** — infrastructure noise is real and underappreciated.

7. **"Teams without evals face reactive loops; teams investing early experience accelerated development"** — the eval investment case.

8. **"The shift-change problem"** — agents losing context across windows is the fundamental challenge of long-running work.

9. **"Context rot"** — performance degrades as context grows. Treat context as a finite, precious resource.

10. **"Do the simplest thing that works"** — repeated across multiple articles as the guiding engineering principle.

11. **"Your context window will be automatically compacted... do not stop tasks early"** — the key prompt for long-horizon autonomous work.

12. **"Prioritize execution over deliberation"** — the antidote to Claude 4.6's tendency toward over-exploration.
