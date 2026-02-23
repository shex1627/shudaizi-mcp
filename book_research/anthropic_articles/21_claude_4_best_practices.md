# Claude 4.6 Prompting Best Practices
**Source:** https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
**Source:** Web-fetched Feb 2026

---

## General Principles

### Be Explicit
Claude responds well to clear, explicit instructions. If you want "above and beyond" behavior, explicitly request it.

```
❌ "Create an analytics dashboard"
✅ "Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation."
```

### Add Context / Motivation
Explain WHY, not just WHAT. Claude generalizes from explanations.

```
❌ "NEVER use ellipses"
✅ "Your response will be read aloud by a text-to-speech engine, so never use ellipses since the engine will not know how to pronounce them."
```

### Be Vigilant with Examples
Claude follows examples precisely. Ensure they model desired behavior and don't encourage unwanted patterns.

---

## Long-Horizon Reasoning & State Tracking

### Context Awareness
Claude 4.6 tracks remaining context window ("token budget") throughout conversations. Key prompt to prevent premature stopping:

```
Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off. Therefore, do not stop tasks early due to token budget concerns.
```

### Multi-Context Window Workflows

1. **Different first-window prompt**: Use first window for setup (write tests, create scripts)
2. **Structured test tracking**: `tests.json` with status per test — better than freeform
3. **Quality-of-life scripts**: `init.sh` for graceful server starts, test suites, linters
4. **Fresh start vs. compacting**: Claude discovers state from filesystem well. Sometimes fresh > compacted
5. **Verification tools**: Playwright MCP, computer use for UI testing
6. **Encourage full context usage**: "This is a very long task... spend your entire output context working on it"

### State Management

| Format | Use For |
|--------|---------|
| JSON | Test results, task status (structured, schema-clear) |
| Freeform text | Progress notes, general context |
| Git | State tracking, checkpoints, restorable snapshots |

---

## Communication Style

Claude 4.6 is more concise, direct, grounded:
- Fact-based progress reports (not self-congratulatory)
- May skip verbal summaries after tool calls
- If you want visibility: "After completing a task, provide a quick summary of the work you've done"

---

## Tool Usage Patterns

### Precise Instruction Following
- "Can you suggest changes" → suggestions only
- "Make these changes" → implementation
- Set default behavior in system prompt

### Proactive Action Prompt
```xml
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's intent is unclear, infer the most useful likely action and proceed.
</default_to_action>
```

### Conservative Action Prompt
```xml
<do_not_act_before_instructions>
Do not jump into implementation unless clearly instructed. Default to providing information and recommendations rather than taking action.
</do_not_act_before_instructions>
```

---

## Overtriggering Fix

Claude 4.6 is more responsive to system prompts than previous models. Previous workarounds now cause overtriggering:

```
❌ "CRITICAL: You MUST use this tool when..."
✅ "Use this tool when..."
```

---

## Overthinking Fix

Claude 4.6 does significantly more upfront exploration. To constrain:

1. **Remove anti-laziness prompts**: "be thorough," "think carefully," "do not be lazy" → cause runaway thinking
2. **Soften tool-use language**: "You must use [tool]" → "Use [tool] when it would enhance understanding"
3. **Remove explicit think tool instructions**: "use the think tool to plan" → causes over-planning
4. **Use `effort` parameter**: primary control lever (low/medium/high/max)
5. **Explicit constraint prompt**:

```
Prioritize execution over deliberation. Choose one approach and start producing output immediately. Do not compare alternatives or plan the entire solution before writing. Write each piece once; do not revise. If uncertain, make a reasonable choice and continue.
```

---

## Adaptive Thinking (Claude 4.6)

Replaces manual `budget_tokens` with dynamic thinking:

```python
# Before (old models)
thinking={"type": "enabled", "budget_tokens": 32000}

# After (Claude 4.6)
thinking={"type": "adaptive"}
output_config={"effort": "high"}  # low/medium/high/max
```

- Claude calibrates thinking based on effort + query complexity
- Higher effort → more thinking; complex queries → more thinking
- Easy queries → responds directly without extended thinking

---

## Prefills Deprecated (Claude 4.6)

Prefilled responses on last assistant turn no longer supported. Migration paths:

| Use Case | Migration |
|----------|-----------|
| Output formatting (JSON/YAML) | Structured Outputs feature |
| Eliminating preambles | Direct instructions: "Respond without preamble" |
| Avoiding bad refusals | Better refusal handling in Claude 4.6 |
| Continuations | User message: "Your previous response ended with [text]. Continue." |
| Context hydration | Inject via user turn or tools |

---

## Subagent Orchestration

Claude 4.6 proactively delegates to subagents. May overuse — constrain with:

```
Use subagents when tasks can run in parallel, require isolated context, or involve independent workstreams. For simple tasks, sequential operations, or single-file edits, work directly rather than delegating.
```

---

## Overengineering Tendency

Claude 4.6 tends to create extra files, add abstractions, build unneeded flexibility:

```
Avoid over-engineering. Only make changes that are directly requested or clearly necessary.
- Don't add features, refactor, or make "improvements" beyond what was asked
- Don't add docstrings/comments to code you didn't change
- Don't add error handling for impossible scenarios
- Don't create helpers/abstractions for one-time operations
```

---

## Parallel Tool Calling

Claude 4.6 excels at this. Steerable to ~100% with:

```xml
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between them, make all independent calls in parallel. Maximize use of parallel tool calls where possible.
</use_parallel_tool_calls>
```

---

## Frontend Design

Prevent "AI slop" aesthetic with explicit design guidance:
- Typography: distinctive fonts (avoid Arial, Inter, Roboto)
- Color: cohesive aesthetic, dominant colors with sharp accents
- Motion: animations for effects, CSS-only when possible
- Backgrounds: atmosphere and depth, not solid colors

---

## Vision Capabilities

Claude 4.6 has improved vision. Boost further with:
- Crop tool / skill for "zooming" into relevant image regions
- Consistent uplift on image evaluations with crop capability
- Can analyze videos by breaking into frames

---

## Sonnet 4.6 Migration Guide

| Previous | Recommended |
|----------|-------------|
| No extended thinking | Set effort explicitly; `low` effort ≈ Sonnet 4.5 performance |
| Extended thinking | Keep budget ~16k tokens; start `medium` effort |
| Coding use cases | `medium` effort; lower if latency too high |
| Chat/non-coding | `low` effort with extended thinking |

### When to Try Adaptive Thinking on Sonnet 4.6
- Autonomous multi-step agents
- Computer use agents (best-in-class accuracy in adaptive mode)
- Bimodal workloads (mix of easy/hard tasks)

---

## Applicability
- Prompt engineering for Claude 4.6
- Agent system configuration
- Model migration planning
- Production deployment tuning
