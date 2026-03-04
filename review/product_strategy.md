# Product Strategy Review

**Frameworks applied:** [40] Working Backwards, [29] Inspired, [35] Agenda Mover, [37] Pyramid Principle, [30] Shape Up
**Verdict: Strong** — Clear problem, defensible solution, genuine differentiation. Gap: customer definition could be sharper; PR/FAQ has never been written explicitly.

---

## Working Backwards Analysis: Reconstructed PR/FAQ

Applying the PR/FAQ framework [40] to Shudaizi — a useful diagnostic even for an already-built system, because it surfaces assumptions that were made implicitly.

---

### Reconstructed Press Release

**Shudaizi Gives AI Coding Agents Access to 40 Books of Software Engineering Wisdom — Exactly When They Need It**

*Token-efficient delivery of curated knowledge from DDIA, Clean Architecture, Threat Modeling, and 37 more titles makes best-practice-aware coding accessible in Claude Code, Cursor, and any MCP-compatible agent.*

**San Francisco, March 2026** — Developers using AI coding agents to write and review software often find that the agent produces plausible-looking output that misses established best practices: architectures without timeout handling, code reviews that miss information leakage, API designs that violate consistency principles. The problem is not that the model lacks the knowledge — it is that the knowledge is not in context when the task is performed.

Shudaizi is a knowledge system that delivers curated software engineering wisdom from 40 books and 21 Anthropic engineering articles to any coding agent at the moment of need. When an agent performs an architecture review, it has immediate access to the relevant principles from DDIA, Clean Architecture, Domain-Driven Design, and Enterprise Integration Patterns — not the full books (too many tokens), but a focused, citation-backed, phased checklist that fits in 3-6K tokens.

The system runs as a set of Claude Code skills and an MCP server with 5 tools, sharing a single knowledge layer of plain markdown and JSON files. No database. No embedding pipeline. No infrastructure to maintain. It works out of the box by cloning a repository, and it grows itself — any agent can research a new book and call `add_knowledge_source` to add it, live, without a rebuild.

"I was tired of my vibe-coded architecture reviews being 80% confident and 20% wrong on exactly the things that bite you in production," said the developer who built Shudaizi. "Now every review cites DDIA, Release It!, and the SRE book — and I can tell which principle I'm applying."

A developer using Shudaizi with Claude Code said: "I asked for an architecture review and got 7 phases of structured checklist items, each citing the specific book the principle came from. I could drill into the full book for any citation I wanted to understand better. It caught three anti-patterns I'd been blind to."

To get started, clone the repository and add `shudaizi-mcp` to your MCP server configuration. Skills for Claude Code are auto-discovered from the `skills/` directory.

---

### What the PR/FAQ Reveals

**The product definition is clear and honest.** The problem statement (agents lack best-practice awareness; the challenge is *delivery* not knowledge), the solution (token-efficient checklists with citation-backed drill-down), and the differentiation (curated over raw, progressive disclosure over full context) are all coherent and defensible.

**The customer quote is convincing.** A developer doing architecture review in Claude Code who wants specific, cited, actionable checklist items — this persona is specific enough to write a real testimonial.

**The competition paragraph is weak.** The README does not address the alternatives: (1) adding books directly to the context window, (2) using a semantic search/RAG system over books, (3) writing custom system prompts. The differentiation is real — token efficiency, progressive disclosure, citation chains — but it is not made explicit. This matters for anyone evaluating the tool.

**The TAM is unstated.** How many developers actively use AI coding agents and would benefit from structured knowledge injection? The market is large (millions of GitHub Copilot users, hundreds of thousands of Claude Code users) and growing. This does not need to be in a README, but the builder should know the number.

---

## Inspired Opportunity Assessment [29]

Cagan's 4 questions before any product investment:

**1. What problem does this solve?**
AI coding agents (Claude Code, Cursor, Windsurf, Copilot) perform code, architecture, and security reviews without awareness of established software engineering best practices from the literature. The agent has the capability to reason about code; it lacks the curated knowledge context.

**Assessment:** Specific, real, validated by daily experience. ✓

**2. Who has this problem?**
Developers using AI coding agents for professional-grade software engineering tasks — particularly those who (a) care about code quality beyond "does it work", (b) use multiple agents/IDEs, and (c) have awareness that best practices exist but can't inject all of them manually.

**Assessment:** The persona is real but defined implicitly, not explicitly. The system currently serves Claude Code users most natively (via skills), with MCP as the cross-agent interface. A user who only uses one agent and is satisfied with default quality is not the target. Could be sharper. ~✓

**3. Why does the existing solution fail?**
- Adding books as full context: ~100-500K tokens per book; context budget exhausted immediately
- Custom system prompts: not citation-backed, not task-specific, not extensible
- Generic "act like a senior engineer" prompts: no specificity, no drill-down capability
- Semantic search / RAG systems: require infrastructure (embedding pipeline, vector DB), can't self-extend

**Assessment:** The differentiation is real. The token budget constraint is the fundamental forcing function, and Shudaizi's progressive disclosure architecture correctly addresses it. ✓

**4. What evidence tells us this is worth solving?**
The project was built by the user who experienced the problem directly. The eval system (3-level test harness with LLM-as-judge) provides some empirical evidence that checklists improve model performance on seeded-issue detection. The 40-book corpus reflects deliberate curation, not breadth-first collection.

**Assessment:** Self-validation only. There is no external user validation data (interview notes, usage metrics, adoption signals beyond the creator). This is fine for a personal knowledge tool at this stage, but would be needed before claiming broader product-market fit. ~✓

---

## Shape Up Appetite Assessment [30]

Shape Up asks: what is the right amount of work to invest in this problem?

The current project scope is appropriate for a "small batch" or "big batch" Shape Up bet:
- Knowledge base: ~40 book research files × ~250 lines = substantial curation investment
- MCP server: 5 tools, ~1000 lines of Python, well-bounded scope
- 3-level test system: 27 fixtures, meaningful engineering investment

The scope is not overcomplicated. There is no database, no UI, no embedding pipeline. The system boundary is correctly drawn at "filesystem + MCP protocol."

What has been explicitly left out of scope (correctly):
- Semantic search / vector embeddings (Phase 2 if needed)
- CI/CD for the knowledge base
- Multi-language server
- Automatic checklist regeneration from books

**Assessment:** The scope is well-shaped. The "out of scope" list in ARCHITECTURE.md shows the builder was deliberate about not over-building. ✓

---

## Agenda Mover Lens [35]

Framing: Is this an idea that could be moved into broader adoption beyond the builder?

**Anticipation:** The project correctly anticipates the key objections:
- "Why not just put books in context?" → Token budget answer is pre-empted in the README
- "Why not semantic search?" → Zero-infrastructure constraint is pre-empted
- "Does it actually work?" → 3-level eval system is the evidence answer

**Mobilization:** The project is a solo effort but has the structure of something a team could contribute to. CONTRIBUTING.md exists. The `add_knowledge_source` tool allows any agent (or human) to grow the knowledge base without code changes.

**Sustainability:** The self-extending design is the key sustainability mechanism — the system can update itself. The staleness detection script (`refresh_checklists.py`) addresses long-term drift. The citation system ties checklists to sources so updates are discoverable.

**Gap:** There is no adoption feedback loop. If this were to grow beyond a personal tool, it would need: (a) a way to discover which checklists are actually used, (b) a way for users to flag checklist items that were unhelpful or wrong, (c) a way to surface when new books' concepts have been incorporated into checklists.

---

## Pyramid Principle Assessment [37]

Evaluating the README as a communication artifact:

**SCQA check:**
- Situation: "When vibe-coding with AI..." ✓ (shared context)
- Complication: "...models lack awareness of established best practices. This causes blind spots..." ✓ (tension created)
- Question: Implied: "How do you get the right knowledge to the right agent at the right time?" ✓
- Answer: "A knowledge system that gives AI coding agents access to curated software engineering wisdom." ✓

**Pyramid structure check:**
The README is organized as: Problem → How It Works → What's Implemented → Project Structure → Getting Started → Design Principles. This is partially top-down (problem first) but then switches to a capabilities tour rather than a sustained argument for why this approach is correct. A stronger Pyramid Principle structure would be:
- Apex: Here's what it does and why it works
- Arguments: (1) Token efficiency, (2) Progressive disclosure, (3) Citation-backed drill-down, (4) Self-extending
- Evidence: Implementation details organized under each argument

**Assessment:** The README communicates what the product is but doesn't argue persuasively for why it beats alternatives. Functional for a technical audience; would benefit from Pyramid restructuring for a broader audience. ~✓

---

## Strengths

1. **Problem-solution fit is clear and specific.** The problem is not "AI doesn't know best practices" (too broad); it is "AI agents doing specific tasks (architecture review, security audit) lack access to relevant, token-efficient, citation-backed knowledge." This specificity makes the solution tractable.

2. **Deliberate scope.** The builder correctly identified what not to build (no vector DB, no UI, no CI pipeline) and stuck to it. The system is not over-engineered for its current purpose.

3. **Self-extending design.** The `add_knowledge_source` / `update_checklist` loop makes the system a platform, not just a fixed knowledge base. This is the most valuable architectural decision from a product perspective.

4. **Evidence-based quality.** The 3-level eval system is a genuine differentiator — most similar projects have no way to measure whether the knowledge delivery actually improves model output.

5. **Dual interface covers the market.** Claude Code skills for the primary user (Claude Code users) + MCP for everyone else is the right two-interface strategy given the agent landscape.

---

## Gaps and Recommendations

**Gap 1: Competition is unaddressed.**
The README never explains why Shudaizi is better than: (a) putting a book summary in a system prompt, (b) a RAG system over books, (c) a larger context window that fits more books. Each has a real answer, but it is not stated. Recommend adding a "Why not..." section.

**Gap 2: No usage metrics.**
There is no mechanism to know which task types are actually invoked, which books are most referenced in drill-downs, or which checklist items are most useful. Without this, the knowledge base is curated on intuition rather than evidence.

**Gap 3: Skills vs. MCP feature parity.**
The skills path (Claude Code) and the MCP path have different capabilities: skills can read any file, follow citation chains directly, and use all Claude Code tools in the process. The MCP path is limited to the 5 tools. This asymmetry is not documented and may surprise users who expect identical behavior.

**Gap 4: Onboarding path is implicit.**
The README's "Getting Started" section is minimal (two code blocks). A developer new to MCP configuration, or who has never used Claude Code skills, may struggle. A 5-minute tutorial or a first-use guided example would significantly lower the adoption barrier.

**Gap 5: No version / release discipline.**
The project has no versioning scheme. When breaking changes are made to the MCP protocol or checklist format, there is no way for users to know what changed or how to update.
