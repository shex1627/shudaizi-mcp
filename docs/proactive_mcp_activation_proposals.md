# Proactive MCP Activation — Design Proposals

## Problem

Skills have per-task-type "When to Activate" triggers that fire proactively (e.g., "activate when writing async code"). MCP tools are passive — they only get called when the agent decides to. The tool description is the only lever we have to influence that decision.

**Goal:** Get MCP clients (Cursor, Windsurf, Copilot) to call `get_task_checklist` *before* writing or reviewing code, without the user explicitly asking for it.

### Why This Matters (from the literature)

> "Tool descriptions directly steer agent behavior. Think of how you'd describe your tool to a new hire. Clear, detailed specifications dramatically improve performance." — Writing Effective Tools [a06]

Anthropic's own SWE-bench agent achieved state-of-the-art results "after making precise refinements to tool descriptions" [a06]. Tool design has more impact on agent performance than prompt optimization [a01]:

> "Anthropic's SWE-bench agent spent more time optimizing tools than the overall prompt." — Building Effective Agents [a01]

The question is *how* to encode proactive activation in tool descriptions without violating the context engineering principle of token efficiency:

> "The smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." — Context Engineering [a05]

---

## Proposal A: Rich Tool Description

Put proactive activation guidance directly in the `get_task_checklist` tool description.

This follows Anthropic's "Prompt-Engineered Descriptions" principle [a06] — treat the tool description as a behavioral specification, not just documentation.

### Current description (~45 tokens)
```
Get a curated checklist for a software engineering task.
Returns actionable items drawn from 33 books and 21 Anthropic articles,
each citing its source. Use this as your primary review/design companion.
```

### Proposed description (~120 tokens)
```
Get a curated checklist for a software engineering task. Returns actionable
items drawn from 33 books and 21 Anthropic articles, each citing its source.

IMPORTANT: Call this tool proactively in these situations:
- Before writing code that involves async/concurrent I/O, external API calls,
  or new module/class/service design
- Before reviewing any code, architecture, or security-sensitive changes
- Before designing APIs, data visualizations, or deployment pipelines
- When the user asks about best practices, patterns, or tradeoffs

Match the user's intent to a task_type:
  architecture_review, code_review, security_audit, test_strategy,
  bug_fix, feature_design, api_design, data_viz_review, product_doc,
  presentation, devops, ai_ml_design, refactoring, observability,
  ux_review, agent_design
```

### Analysis

**Aligns with:**
- "Fewer, more purposeful tools" [a06] — we're enriching an existing tool, not adding another
- "Self-contained, unambiguous" tool design [a05] — the description tells the agent everything it needs: *when* to call, *what* to pass, *what* it gets back
- The progressive disclosure model [a10] — the description is L1 metadata (loaded at startup), the checklist response is L2/L3 content (loaded on-demand)

**Tradeoffs:**

| Pro | Con |
|-----|-----|
| Zero additional infrastructure | Description bloat (~120 tokens loaded on every tool listing) |
| Works immediately with any MCP client | Generic triggers — can't express "when writing async code, use code_review" level specificity |
| Single source of truth | Some agents may ignore long descriptions |
| Follows Anthropic's own tool design recommendations [a06] | Token cost is per-session, not per-call (mitigated) |

---

## Proposal B: Companion Discovery Tool

Add a lightweight 6th tool that returns activation rules for a given coding context. The main tool description stays short and tells agents to check activation rules first.

This follows the "Routing" workflow pattern from Building Effective Agents [a01] — classify the input, then direct to the right downstream tool.

### New tool: `should_i_use_shudaizi`
```python
Tool(
    name="should_i_use_shudaizi",
    description=(
        "Check whether shudaizi knowledge should be consulted for your current task. "
        "Call this when you're about to write or review code to find out which "
        "task_type checklist to load. Returns the matching task type or 'none'."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "context": {
                "type": "string",
                "description": "Brief description of what you're about to do. "
                "Examples: 'writing an async API handler', 'reviewing a PR', "
                "'designing a database schema'",
            },
        },
        "required": ["context"],
    },
)
```

The tool would use keyword matching to return the right task type:
```
Input:  "writing an async API handler with retry logic"
Output: "Use task_type='code_review' (async patterns, retry logic) and
         task_type='architecture_review' (resilience patterns)"
```

### Analysis

**Aligns with:**
- The Routing pattern [a01] — classify intent, direct to the right handler
- "Meaningful context returns" [a06] — the response tells the agent exactly which task_type to use and why
- Can return *multiple* relevant task types (e.g., both `code_review` and `security_audit` for auth code)

**Conflicts with:**
- "Fewer, more purposeful tools" [a06] — adding a 6th tool increases the tool listing from 5 to 6
- "Bloated tool sets encourage misuse and wasted context" [a05] — every additional tool consumes tokens in the tool listing
- Token efficiency [a05] — extra round-trip per task adds latency and tokens
- The Advanced Tool Use article [a07] showed that with 10+ tools, models start to degrade. We're at 5-6, so this is within bounds, but each addition moves toward the threshold.

**Tradeoffs:**

| Pro | Con |
|-----|-----|
| Rich, context-aware activation rules | Extra tool call before every task (latency + tokens) |
| Can encode per-task-type specificity | Agents may not call it — same discovery problem, just moved |
| Activation logic is updatable without changing tool schemas | 6th tool adds to tool listing token cost |
| Can return multiple relevant task types | Keyword matching is fragile; LLM-based matching is expensive |

---

## Proposal C: Structured Description with Activation Matrix

Keep a single tool but encode activation hints in per-enum-value descriptions on the `task_type` parameter.

This mirrors the API Design Patterns [20] philosophy of encoding domain knowledge in the schema itself — the enum values become self-documenting.

### Implementation
```python
"task_type": {
    "type": "string",
    "description": "Task type to get checklist for.",
    "enum": [
        "architecture_review",
        "code_review",
        "security_audit",
        ...
    ],
    "x-enum-descriptions": {
        "architecture_review": "Use before designing systems, reviewing ADRs, or evaluating service boundaries",
        "code_review": "Use before writing async code, reviewing PRs, or creating new modules",
        "security_audit": "Use before handling auth, user input, or LLM output",
        "test_strategy": "Use before writing tests or designing test architecture",
        "bug_fix": "Use when diagnosing production issues or unexpected behavior",
        "feature_design": "Use before scoping or designing new features",
        "api_design": "Use before designing REST/GraphQL/MCP APIs or tool interfaces",
        "data_viz_review": "Use before creating charts, dashboards, or data presentations",
        "product_doc": "Use before writing PRDs, specs, or product briefs",
        "presentation": "Use before creating slide decks or visual communications",
        "devops": "Use before designing CI/CD, deployment, or infrastructure",
        "ai_ml_design": "Use before building LLM apps, RAG pipelines, or agent systems",
        "refactoring": "Use before restructuring code or extracting modules",
        "observability": "Use before adding logging, metrics, tracing, or alerts",
        "ux_review": "Use before designing user interfaces or interaction flows",
        "agent_design": "Use before designing AI agent architectures or tool interfaces",
    },
}
```

Combined with a shorter top-level description:
```
Get a curated checklist for a software engineering task. Call this
proactively before writing, reviewing, or designing code — not just
when explicitly asked. Returns items from 33 books + 21 articles.
```

### Analysis

**Aligns with:**
- Resource-oriented design [20] — the enum values are the "resources" the agent navigates, and each has its own documentation
- Token efficiency [a05] — top-level description stays short; per-value context loads only in the schema
- "Exploit model strengths in parameter design" [a05] — LLMs are good at matching context to enum descriptions

**Conflicts with:**
- `x-enum-descriptions` is non-standard JSON Schema — most MCP clients pass the raw schema to the LLM without interpreting extensions
- Falls back to just the enum list if the client doesn't forward the extension
- The MCP spec doesn't define how extended schema properties should be handled

**Tradeoffs:**

| Pro | Con |
|-----|-----|
| Per-task-type activation guidance without description bloat | `x-enum-descriptions` is non-standard — most MCP clients ignore it |
| Clean separation of "what" (description) and "when" (enum hints) | Falls back to generic description if client doesn't support it |
| Scales well as task types grow | Depends on MCP client surfacing schema extensions to the LLM |

---

## Recommendation

**Proposal A** — for pragmatism. Here's why:

### 1. Anthropic's own data supports description-driven behavior

"State-of-the-art results on SWE-bench Verified after making precise refinements to tool descriptions" [a06]. The description *is* the behavioral contract between a deterministic system and a non-deterministic agent. Making it richer is the intended mechanism.

### 2. The token cost is negligible

Tool descriptions load once per session (L1 in the progressive disclosure model [a10]). The system already loads ~850 tokens of metadata at startup. An extra ~75 tokens in one tool description is noise against a 200K context window.

The Context Engineering article [a05] warns against bloated context, but also says to optimize for *signal density*, not raw size. A 120-token description with clear behavioral instructions has higher signal density than a 45-token description that leaves the agent guessing.

### 3. The specificity gap is acceptable

Skills can say "when writing async code, activate code_review." The MCP description says "before writing async code, call this tool." The agent still picks the `task_type`, but the task descriptions in the parameter enum guide that mapping. LLMs are good at intent→category mapping — this is exactly the "Routing" pattern from Building Effective Agents [a01].

### 4. Proposal B violates "fewer, more purposeful tools"

> "More tools don't always lead to better outcomes. Build a few thoughtful tools targeting specific high-impact workflows." [a06]

If agents ignore long descriptions, they'll also ignore a discovery tool. The activation problem is about the agent's willingness to call tools proactively — that's driven by the primary tool's description, not by adding more tools.

### 5. Proposal C depends on unproven MCP client behavior

It's the most elegant design, but it bets on MCP clients forwarding `x-enum-descriptions` to the LLM. Most don't today. If the ecosystem evolves to support it, this becomes the right answer — but we should measure first and avoid building for hypothetical future capabilities:

> "Start with the simplest approach that works. Only increase complexity when measurement proves it's necessary." [a01]

### Escalation path

If Proposal A proves insufficient (agents still don't call the tool proactively), measure with the activation eval fixtures (`tests/eval_fixtures/activation_*`) before escalating to Proposal B.

---

## Sources

| Citation | Source |
|----------|--------|
| [a01] | Building Effective Agents — Anthropic (2024) |
| [a05] | Effective Context Engineering for AI Agents — Anthropic (2025) |
| [a06] | Writing Effective Tools for Agents — Anthropic (2025) |
| [a07] | Introducing Advanced Tool Use — Anthropic (2025) |
| [a10] | Agent Skills: Equipping Agents for the Real World — Anthropic (2025) |
| [20] | API Design Patterns — JJ Geewax (2021) |
