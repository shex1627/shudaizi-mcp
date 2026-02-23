# The "Think" Tool
**Date:** March 20, 2025
**URL:** https://www.anthropic.com/engineering/claude-think-tool
**Source:** Web-fetched Feb 2026

---

## What It Is

A designated space for Claude to pause and reflect during tool-use sequences. Different from extended thinking, which occurs before response generation begins.

## Think Tool vs. Extended Thinking

| Aspect | Think Tool | Extended Thinking |
|--------|-----------|-------------------|
| When it activates | After response generation starts, between tool calls | Before any response generation |
| Purpose | Analyze tool outputs, plan next steps | Deep upfront reasoning |
| Best for | Sequential tool chains, policy compliance | Simple scenarios, non-sequential calls |

## Benchmark Results

### τ-Bench (Customer Service Scenarios)

**Airline Domain:**
| Configuration | Score |
|--------------|-------|
| Think tool + optimized prompt | 0.584 (**54% improvement**) |
| Think tool alone | 0.404 |
| Extended thinking | 0.412 |
| Baseline | 0.332 |

**Retail Domain:**
| Configuration | Score |
|--------------|-------|
| Think tool (no prompt) | 0.812 |
| Extended thinking | 0.770 |
| Baseline | 0.783 |

### SWE-Bench
- Think tool: +1.6% average improvement (statistically significant: p < .001)

## Ideal Use Cases

1. **Tool output analysis** — processing previous tool call results before proceeding
2. **Policy-heavy environments** — following detailed guidelines consistently
3. **Sequential decision-making** — multi-step problems where errors compound

## When NOT to Use

- Non-sequential parallel tool calls
- Straightforward instruction-following without complex constraints
- Performance gains don't materialize in these cases

## Implementation Strategy

- Success requires domain-specific prompting with reasoning examples
- Complex guidance belongs in system prompts, not tool descriptions
- Airline domain required explicit prompting; retail domain improved with just tool availability

## Dec 2025 Update

Extended thinking has improved enough that it's **recommended over the think tool in most cases**. Think tool remains valuable for complex sequential tool use where intermediate reflection between tool calls matters.

## Key Insight

The think tool provides a structured reflection space *between* actions, not just before them. This is its unique value vs. extended thinking.

---

## Applicability
- Sequential tool-use workflows
- Policy compliance agents
- Complex multi-step decision chains
- Agent reasoning architecture
