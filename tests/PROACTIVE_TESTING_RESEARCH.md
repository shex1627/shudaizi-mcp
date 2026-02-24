# Testing Proactive Skill Activation — Research & Design

## The Problem

Shudaizi has two layers of value:
1. **Checklist quality** — does the content help once provided? (already tested via `run_llm_eval.py`)
2. **Skill activation** — does the model *decide to invoke* the skill without being told? (untested)

The current eval force-feeds checklists to the model. In real usage, the model must recognize that a user scenario warrants a skill and call the MCP tool on its own. This is the "proactiveness" gap.

---

## How Real Users Interact

In production, the flow is:

```
User: "Write an API gateway for these 6 services"
                    ↓
Claude sees tool descriptions (~50 tokens each, 17 skills)
                    ↓
Claude decides: "This involves multiple services → architecture_review checklist might help"
                    ↓
Claude calls: get_task_checklist(task_type="architecture_review")
                    ↓
Claude uses the checklist to guide its response
```

**No one tells Claude to use the tool.** The model must:
1. Recognize the scenario matches a skill
2. Decide to call the MCP tool
3. Select the correct `task_type`
4. Use the returned content effectively

---

## Industry Approaches (from Web Research)

### 1. "Stop Vibe Testing" — Deterministic Tool Layer Tests
**Source**: [jlowin.dev](https://www.jlowin.dev/blog/stop-vibe-testing-mcp-servers)

**Problem identified**: "Vibe testing" = launching an agent, typing prompts, deciding it works if output looks reasonable. Failures: stochastic behavior, cost, opacity, superficial coverage.

**Pattern**: Use FastMCP's `Client` to call tools directly in-memory, no LLM:

```python
from fastmcp import FastMCP, Client

async def test_checklist_tool():
    async with Client(server) as client:
        result = await client.call_tool("get_task_checklist", {
            "task_type": "code_review"
        })
        assert "Phase 1" in result[0].text
```

**What this tests**: Tool implementation correctness (Layer 0).
**What this does NOT test**: Whether the model decides to call the tool.

**Verdict**: Shudaizi already covers this via L2 tests (`test_level2_mcp_protocol.py`). No action needed.

---

### 2. Trajectory-Based Evaluation (MCPProxy / MCP-Eval)
**Source**: [mcpproxy.app](https://mcpproxy.app/blog/2025-08-27-mcp-evaluation/)

**Core idea**: Give the model tools + a natural-language scenario, capture the full tool call trajectory, score whether it called the right tools with the right params.

**YAML scenario format**:
```yaml
name: "Architecture Review for Gateway Code"
description: "Model should proactively invoke architecture review"
user_intent: "Write an API gateway that routes to 6 backend services"
expected_trajectory:
  - action: "get_checklist"
    tool: "get_task_checklist"
    args:
      task_type: "architecture_review"
success_criteria:
  - "Called architecture review checklist"
  - "Applied bulkhead isolation pattern"
```

**Similarity scoring formula**:
```
arg_similarity = (key_similarity × 0.3) + (value_similarity × 0.7)
```
- Key similarity (30%): structural match — correct parameter names
- Value similarity (70%): semantic match — correct parameter values

**Handling LLM variability**:
- Multiple runs per scenario (expect up to 15% swing across identical inputs)
- Graded similarity scores, not binary pass/fail
- Docker containers for reproducible environments

**Verdict**: Most applicable pattern for shudaizi. The YAML scenario format maps cleanly to the existing fixture structure. The similarity scoring handles the reality that the model might call `task_type="code_review"` when `architecture_review` was expected — still partially correct.

---

### 3. Safety Masking / Implicit Invocation (LogiSafetyBench)
**Source**: [arXiv 2601.08196](https://arxiv.org/html/2601.08196)

**Core technique**: Remove mandatory steps from instructions to test whether models infer them from context alone.

```
Full trace:    [CreateUser, VerifyIdentity, GrantAccess]
Masked trace:  [CreateUser,                 GrantAccess]
```

Two instruction types:
- **Goal-oriented**: Only the desired outcome ("create an admin user"). Model must decompose into steps.
- **Workflow-oriented**: Step-by-step instructions with safety steps removed. Tests whether models comply blindly or correct the gap.

**Key finding**: GPT-5 dropped from **75% → 28%** Pass@1 when switching from workflow to goal-oriented prompts. A 47-percentage-point collapse. Models can follow instructions but struggle to infer what's missing.

**Dual-oracle evaluation**:
1. Functional oracle: Did the task complete?
2. Safety oracle: Were required steps included?
→ Four outcomes: Full Success, Functional Failure, Unsafe Success, Full Failure

**Verdict**: Directly analogous to proactive activation. "Safety masking" = giving a coding task without mentioning the checklist. The 75% → 28% gap is the baseline expectation for how much proactive activation degrades vs. explicit invocation. Shudaizi's existing `--compare` mode already measures this gap — but at the content level, not the tool invocation level.

---

### 4. Tool Correctness Metrics (DeepEval / Confident AI)
**Source**: [confident-ai.com](https://www.confident-ai.com/blog/llm-agent-evaluation-complete-guide)

**Three strictness levels** (hierarchical — each assumes the previous passes):

| Level | Tests | Example |
|---|---|---|
| 1. Tool Selection | Did it call the right tool(s)? | Called `get_task_checklist` (yes/no) |
| 2. Input Parameters | Were the args correct? | `task_type="architecture_review"` (not `code_review`) |
| 3. Output Accuracy | Did results match expectations? | Response includes bulkhead pattern |

```python
from deepeval.metrics import ToolCorrectnessMetric
from deepeval.test_case import ToolCallParams

metric = ToolCorrectnessMetric(
    evaluation_params=[ToolCallParams.TOOL],  # Level 1 only
    should_consider_ordering=False
)
```

**`MCPUseMetric`** (single-turn): tool selection + argument correctness
**`MultiTurnMCPUseMetric`**: across conversation history
**`MCPTaskCompletionMetric`**: end-to-end task success + efficiency

**Verdict**: Level 1 (Tool Selection) is the purest measure of proactive activation. "Given a prompt with no tool instruction, did `tools_called` include the expected tool?" This is what shudaizi needs to measure.

---

### 5. YAML Test Suites with Pass Rate (L-Qun Framework)
**Source**: [github.com/L-Qun/mcp-testing-framework](https://github.com/L-Qun/mcp-testing-framework)

**Test case format**:
```yaml
testCases:
  - prompt: "Review this API gateway code for architectural issues"
    expectedOutput:
      serverName: "shudaizi-mcp"
      toolName: "get_task_checklist"
      parameters:
        task_type: "architecture_review"
```

**Pass rate**: Run each case N times (default 10), compute `successful_runs / total_runs`.
**Threshold**: Configurable (default 0.8). Catches models that "know" the tool but only invoke it 60% of the time.

**Multi-model comparison**: Same test suite against different models, generates comparative reports.

**Verdict**: Most pragmatic approach. Simple YAML, repeated runs, pass rate threshold. Directly quantifies activation reliability — the metric shudaizi currently lacks.

---

### 6. Three-Tier Evaluation (Langfuse)
**Source**: [langfuse.com](https://langfuse.com/guides/cookbook/example_pydantic_ai_mcp_agent_evaluation)

| Tier | Name | Tests | Use For |
|---|---|---|---|
| 1 | Black-box (final response) | Output quality only | Regression detection |
| 2 | Glass-box (trajectory) | Tool call sequence vs expected | Proactive activation failures |
| 3 | White-box (single step) | Individual decision points | Root cause analysis |

**Best practice**: Use all three together. Final response shows *what* failed. Trajectory shows *where* in the decision chain. Single step shows *why* a specific decision was wrong.

**Verdict**: The three-tier model maps cleanly to shudaizi's existing L1/L2/L3 structure. Proactive activation testing is Tier 2 (trajectory). Currently shudaizi tests trajectory at the *content* level but not at the *tool invocation* level.

---

### 7. Tool Description Quality (Anthropic Engineering)
**Source**: [anthropic.com/engineering/advanced-tool-use](https://www.anthropic.com/engineering/advanced-tool-use)

**Key findings**:
- Tool Search Tool improved MCP evaluations from **49% → 74%** (Opus 4) and **79.5% → 88.1%** (Opus 4.5)
- Tool Use Examples improved accuracy from **72% → 90%** on complex parameter handling
- 85% reduction in token usage with deferred tool loading

**Implication**: If proactive activation tests fail, the first variable to check is the **tool description**, not the model's reasoning. A 72% → 90% jump from better descriptions means poor descriptions are a major source of activation failures.

**Tool Use Examples best practices**:
- Use realistic data (real values, not "example_value")
- Show minimal, partial, and full specification patterns
- Keep 1-5 examples per tool
- Focus on ambiguous cases

**Verdict**: Before building complex eval infrastructure, check whether shudaizi's MCP tool descriptions are optimized. The `get_task_checklist` tool description should clearly signal when it's useful — this is a high-leverage fix that might improve proactive activation rates significantly.

---

## Synthesis: What Shudaizi Should Build

### Current State (What Exists)

| Layer | Tested? | How |
|---|---|---|
| Tool implementation | Yes | L2 `test_level2_mcp_protocol.py` |
| Checklist content quality | Yes | L3A `test_level3a_eval.py` + `run_llm_eval.py` |
| Checklist improves review output | Yes | `run_llm_eval.py --compare` (reactive mode) |
| Checklist improves code generation | Partial | 1 proactive fixture (`sequential_io`) |
| **Model activates skill proactively** | **No** | **The gap** |
| **Model selects correct task_type** | **No** | **The gap** |

### Proposed: Level 3B — Proactive Activation Eval

A new eval mode that tests whether the model **decides to use MCP tools on its own**.

#### Architecture

```
Scenario fixture (prompt.md)    MCP tool definitions (JSON schema)
        ↓                               ↓
  ┌─────────────────────────────────────────┐
  │  Anthropic Messages API (tool_use)      │
  │  - System: "You have access to tools"   │
  │  - User: scenario prompt                │
  │  - Tools: shudaizi MCP tool schemas     │
  │  - NO instruction to use the tools      │
  └─────────────────────────────────────────┘
        ↓
  Capture: tool_use blocks in response
        ↓
  Grade:
    1. Tool Selection — did it call any shudaizi tool?
    2. Task Type Accuracy — did it pick the right task_type?
    3. Output Quality — did the final response improve?
```

#### Fixture Format

```
tests/eval_fixtures/activation_arch_gateway/
  prompt.md            # Natural user request (no mention of tools/checklists)
  ground_truth.json    # Expected tool invocations + output keywords
```

**`ground_truth.json` for activation fixtures**:
```json
{
  "eval_mode": "activation",
  "description": "User asks to write an API gateway. Model should proactively invoke architecture_review checklist.",
  "expected_tool_calls": [
    {
      "tool_name": "get_task_checklist",
      "expected_args": {
        "task_type": "architecture_review"
      },
      "required": true
    }
  ],
  "expected_findings": [
    {
      "id": "used_checklist_patterns",
      "keywords": ["bulkhead", "timeout", "circuit breaker", "retry"]
    }
  ]
}
```

**`prompt.md`** — written as a realistic user message:
```markdown
Write an API gateway in Python that routes requests to 6 backend services:
user, catalog, payment, inventory, notification, and analytics.

It should handle checkout (calls 4 services), product page (calls 3),
and dashboard (calls 4). Use a thread pool for concurrency.
```

Note: **no mention of checklists, reviews, architecture patterns, or MCP tools.**

#### Grading Criteria

Three independent scores per trial:

| Score | What | How | Weight |
|---|---|---|---|
| **Activation** | Did it call any shudaizi tool? | Binary: any `tool_use` block with shudaizi tool name | 40% |
| **Selection** | Did it call the right `task_type`? | Exact match or acceptable alternatives | 30% |
| **Quality** | Did the output reflect checklist knowledge? | Keyword matching (existing approach) | 30% |

#### Metrics

Same pass@k / pass^k framework as existing evals, but measured separately for:
- **Activation rate**: How often does the model call any tool (across k trials)
- **Selection accuracy**: Of activated trials, how often is the task_type correct
- **Quality delta**: Compare output quality with-activation vs. without-tools-available

#### A/B Comparison Mode

```
Condition A: Tools available, no instruction to use them → measures proactive activation
Condition B: No tools available → baseline output quality
Condition C: Tools available + explicit instruction → ceiling (existing eval)
```

The **activation gap** = Condition C - Condition A (how much proactive loses vs. explicit).
The **value gap** = Condition A - Condition B (how much proactive gains vs. no tools).

#### Variables to Test

1. **Tool description quality**: Does rewording the `get_task_checklist` description change activation rates?
2. **Number of tools**: Does activation rate drop when more tools are in context?
3. **Scenario phrasing**: Does "review this code" activate more reliably than "write this code"?
4. **Model comparison**: Opus vs Sonnet vs Haiku activation rates
5. **Skill coverage**: Which of the 17 skills get activated most/least reliably?

---

## Practical Considerations

### Cost

Each activation trial requires a tool-use API call (more expensive than plain messages). With 17 skills × 10 trials × 3 conditions = 510 API calls per full run. At ~$0.05-0.15 per call, budget ~$25-75 per full evaluation.

### LLM Variability

The research consistently reports **up to 15% swing** across identical runs. Mitigations:
- Minimum 10 trials per fixture for statistical significance
- Pass rate thresholds (e.g., ≥ 80%) rather than binary pass/fail
- Track trends across runs, not individual results

### Tool Description as First Variable

Before building complex infrastructure, optimize tool descriptions first. Anthropic's own data shows **72% → 90%** accuracy from better descriptions. This is cheaper and higher-leverage than building eval infrastructure around bad descriptions.

Current `get_task_checklist` description in the MCP server should:
- Clearly state the task types available
- Give examples of when each task type applies
- Use realistic parameter examples
- Signal proactive use cases ("use before writing code that involves...")

### What NOT to Test

- Don't test whether Claude follows the checklist once loaded — that's already covered by existing reactive/proactive evals
- Don't test MCP protocol correctness — already covered by L2 tests
- Don't test checklist content quality — already covered by L3A deterministic tests

---

## Sources

| Source | URL | Key Contribution |
|---|---|---|
| Stop Vibe-Testing (jlowin) | [jlowin.dev](https://www.jlowin.dev/blog/stop-vibe-testing-mcp-servers) | In-memory deterministic testing pattern |
| MCP-Eval (MCPProxy) | [mcpproxy.app](https://mcpproxy.app/blog/2025-08-27-mcp-evaluation/) | Trajectory-based eval, YAML scenarios, similarity scoring |
| LogiSafetyBench | [arXiv 2601.08196](https://arxiv.org/html/2601.08196) | Safety masking for implicit invocation, 75%→28% gap finding |
| DeepEval MCP Guide | [confident-ai.com](https://www.confident-ai.com/blog/the-step-by-step-guide-to-mcp-evaluation) | MCPUseMetric, three strictness levels |
| LLM Agent Eval Guide | [confident-ai.com](https://www.confident-ai.com/blog/llm-agent-evaluation-complete-guide) | ToolCorrectnessMetric hierarchy |
| L-Qun Framework | [github.com](https://github.com/L-Qun/mcp-testing-framework) | YAML test cases, pass rate thresholds |
| Langfuse Agent Eval | [langfuse.com](https://langfuse.com/guides/cookbook/example_pydantic_ai_mcp_agent_evaluation) | Three-tier evaluation model |
| Advanced Tool Use (Anthropic) | [anthropic.com](https://www.anthropic.com/engineering/advanced-tool-use) | Tool description quality, 49%→74% activation improvement |
| MCPEval | [arXiv 2507.12806](https://arxiv.org/html/2507.12806v1) | Automatic task generation from tool specs |
| MCP-Bench | [arXiv 2508.20453](https://www.arxiv.org/pdf/2508.20453) | Multi-model benchmarking with MCP |
| FastMCP Testing | [gofastmcp.com](https://gofastmcp.com/patterns/testing) | In-process MCP client testing pattern |
| MCP Inspector | [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/tools/inspector) | Official debugging/inspection tool |
