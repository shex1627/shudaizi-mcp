# Prompt Caching: Cross-Provider Research & Best Practices

**Date:** 2026-03-08
**Providers covered:** Anthropic (Claude), OpenAI (GPT/o-series), Google (Gemini)

---

## Executive Summary

Prompt caching is a technique where LLM providers store the KV-cache (key-value attention tensors) of previously processed prompt prefixes, allowing subsequent requests with identical prefixes to skip recomputation. This yields **50–90% cost reduction** on input tokens and **up to 80% latency reduction** (time-to-first-token). All three major providers now support it, but with fundamentally different implementation philosophies.

| Dimension | Anthropic (Claude) | OpenAI (GPT/o-series) | Google (Gemini) |
|-----------|--------------------|-----------------------|-----------------|
| **Activation** | Explicit + Automatic | Fully automatic | Explicit + Implicit |
| **Developer control** | High (breakpoints, TTL) | Low (automatic only) | High (named caches, TTL) |
| **Min tokens** | 1024–4096 (model-dependent) | 1024 | 1024–4096 (model-dependent) |
| **Cache duration** | 5 min (default) or 1 hour | 5–10 min (up to 24h extended) | 1 hour default, configurable |
| **Write cost premium** | 1.25× (5 min) / 2× (1 hr) | None | Storage-based billing |
| **Read discount** | 90% off base input | 50–90% off (model-dependent) | 75–90% off (model-dependent) |
| **Max breakpoints** | 4 per request | N/A (automatic) | N/A (whole cache object) |

---

## 1. Anthropic (Claude) — Prompt Caching

### How It Works

Anthropic caches KV representations and cryptographic hashes of cached content (not raw text). The system checks if a prompt prefix up to a cache breakpoint matches a recent query. Cache prefixes are created in this hierarchy: **tools → system → messages**.

### Two Implementation Modes

**Automatic Caching** (recommended for multi-turn conversations):
```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    cache_control={"type": "ephemeral"},  # top-level
    system="You are an AI assistant analyzing literary works.",
    messages=[{"role": "user", "content": "Analyze Pride and Prejudice."}],
)
```
- System auto-applies breakpoint to the last cacheable block
- Cache point moves forward as conversation grows
- No manual breakpoint management needed

**Explicit Breakpoints** (for fine-grained control):
```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    system=[
        {"type": "text", "text": "You are a helpful assistant."},
        {
            "type": "text",
            "text": "[50-page legal document...]",
            "cache_control": {"type": "ephemeral"},
        },
    ],
    messages=[{"role": "user", "content": "What are the key terms?"}],
)
```
- Max 4 explicit breakpoints per request
- Use when different sections change at different frequencies
- Place breakpoints before editable content

### TTL Options

| TTL | Write Cost | Use When |
|-----|-----------|----------|
| 5 minutes (default) | 1.25× base input | Content reused within minutes (active conversations) |
| 1 hour | 2× base input | Content reused every few minutes to hourly |

TTLs can be mixed in the same request (longer TTLs must appear before shorter ones):
```json
{
    "system": [
        {"type": "text", "text": "Long-lived instructions",
         "cache_control": {"type": "ephemeral", "ttl": "1h"}},
        {"type": "text", "text": "Session-specific context",
         "cache_control": {"type": "ephemeral"}}
    ]
}
```

### Minimum Token Requirements

| Model | Minimum Cached Tokens |
|-------|-----------------------|
| Claude Opus 4.6 / 4.5, Haiku 4.5 | 4,096 |
| Claude Sonnet 4.6, Haiku 3.5/3 | 2,048 |
| Claude Opus 4.1/4, Sonnet 4.5/4 | 1,024 |

### Pricing (per million tokens)

| Model | Base Input | 5m Cache Write | 1h Cache Write | Cache Read | Savings on Read |
|-------|-----------|----------------|----------------|------------|-----------------|
| Claude Opus 4.6 | $5 | $6.25 | $10 | $0.50 | 90% |
| Claude Sonnet 4.6 | $3 | $3.75 | $6 | $0.30 | 90% |
| Claude Haiku 4.5 | $1 | $1.25 | $2 | $0.10 | 90% |

### The 20-Block Lookback Window

The system checks up to 20 blocks backward from each explicit `cache_control` breakpoint. If your conversation has >20 blocks, place additional breakpoints earlier to avoid cache misses on modified early blocks.

### Cache Invalidation Triggers

Changes to these invalidate downstream cache: tool definitions, web search toggle, citations toggle, speed setting, tool choice, images, thinking parameters.

### What Can Be Cached
- Tool definitions, system content blocks, text messages (user & assistant), images & documents, tool use and tool results

### What Cannot Be Cached
- Thinking blocks with explicit `cache_control`, sub-content blocks (citations) directly, empty text blocks

### Monitoring
```python
response.usage = {
    "cache_creation_input_tokens": 248,   # written to cache
    "cache_read_input_tokens": 1800,      # read from cache
    "input_tokens": 50                    # tokens after last breakpoint
}
```

### Key Gotchas
- Cache isolated per organization (per workspace starting Feb 5, 2026)
- Exact prefix match required — any change invalidates
- Concurrent requests: cache only available after first response begins
- JSON key order must be stable (some languages randomize)
- Output generation is identical regardless of caching

---

## 2. OpenAI (GPT/o-series) — Prompt Caching

### How It Works

OpenAI's caching is **fully automatic** — no code changes, no special parameters, no additional fees. The system routes requests to servers that recently processed the same prompt prefix, using a hash of the first ~256 tokens for routing.

### Supported Models
- GPT-4o, GPT-4.1, GPT-5-nano, GPT-5.2, GPT-realtime (audio)
- Pre-GPT-5 models lack caching support on the Batch API

### Cache Policies

**In-Memory (Default)**:
- Duration: 5–10 minutes of inactivity, up to 1 hour
- No additional fees
- Automatic on all API requests

**Extended Prompt Caching**:
- Duration: Up to 24 hours
- Parameter: `prompt_cache_retention: "24h"`
- Stores KV tensors to GPU-local storage
- ~10% improvement in cache hit rates
- Not eligible for Zero Data Retention (ZDR) compliance

### Requirements
- Minimum prefix: **1,024 tokens**
- Cache hits in **128-token increments**
- Exact prefix match required

### Pricing (per million tokens)

| Model | Input | Cached Input | Discount |
|-------|-------|-------------|----------|
| GPT-4o | $2.50 | $1.25 | 50% |
| GPT-4.1 | $2.00 | $0.50 | 75% |
| GPT-5-nano | $0.05 | $0.005 | 90% |
| GPT-5.2 | $1.75 | $0.175 | 90% |
| GPT-realtime | $32.00 | $0.40 | 98.75% |

No cache write premium — OpenAI absorbs the cost.

### What Gets Cached
- System messages, tool definitions, multi-modal content (images, audio), structured output schemas, previous conversation turns

### `prompt_cache_key` Parameter
Improves routing stickiness by combining with the prefix hash. Use cases:
- Per-user keys (same codebase work)
- Per-conversation keys (multiple parallel threads)
- Bucketed approaches (hash user ID to distribute load)
- Rate limit: ~15 requests/minute per prefix+key combination

### Responses API Advantage
The Responses API shows "40–80% better cache utilization" compared to Chat Completions, especially with reasoning models via `previous_response_id`.

### Monitoring
```python
response.usage.prompt_tokens_details.cached_tokens  # number of cached tokens
```

### Key Gotchas
- Caching is best-effort — no guarantee of cache hits
- Load-balancing distributes excess traffic across machines (each with empty cache)
- Cache breaks when: tool/schema definitions change, system prompts modify, timestamps appear in early tokens, reasoning effort changes
- Context engineering (compaction, summarization, truncation) conflicts with caching

---

## 3. Google (Gemini) — Context Caching

### How It Works

Gemini offers two distinct mechanisms: **implicit caching** (automatic, no guaranteed savings) and **explicit caching** (manual setup, guaranteed discount).

### Implicit Caching
- Enabled by default for most Gemini models (since May 2025)
- Automatic cost savings when cache hits occur
- No developer configuration needed
- Discount applied transparently when detected

### Explicit Caching
- Developer creates a named `CachedContent` object with a TTL
- Subsequent requests reference this cache object
- Guaranteed discount on every request that references the cache
- Default TTL: 1 hour (configurable)

```python
import google.generativeai as genai

# Create cache
cache = genai.caching.CachedContent.create(
    model="gemini-2.5-flash",
    display_name="legal-docs",
    system_instruction="You are a legal document analyzer.",
    contents=[large_document_content],
    ttl=datetime.timedelta(hours=2),
)

# Use cache
model = genai.GenerativeModel.from_cached_content(cached_content=cache)
response = model.generate_content("Summarize key clauses.")
```

### Minimum Token Requirements

| Model | Minimum Tokens |
|-------|---------------|
| Gemini 3.1 Pro Preview | 4,096 |
| Gemini 3 Flash Preview | 1,024 |
| Gemini 2.5 Flash | 1,024 |
| Gemini 2.5 Pro | 4,096 |

### Pricing Discounts

| Model Generation | Cache Read Discount |
|------------------|-------------------|
| Gemini 2.5+ | 90% off input tokens |
| Gemini 2.0 | 75% off input tokens |

Additional storage costs based on token-hours and TTL duration.

### Cache Management API
- **Create**: Set content, model, TTL, display name
- **List**: Retrieve metadata (name, model, creation/expiration times)
- **Update**: Modify TTL or expiration time only
- **Delete**: Manually remove cached content

### Supported Content Types
- System instructions, video files, PDFs and text documents, code repositories

### Use Cases Best Suited
- Chatbots with extensive system instructions
- Repetitive analysis of lengthy video files
- Recurring queries against large document sets
- Code repository analysis and debugging

### Key Gotchas
- Model treats cached tokens identically to regular input tokens (no behavioral difference)
- Standard rate limits apply; no special caching rate limits
- Cannot update cached content itself — only TTL
- Token counts include both cached and non-cached tokens

---

## Cross-Provider Best Practices

### 1. Prompt Structure — The Golden Rule

**Place static content first, dynamic content last.** This is the single most impactful practice across all providers.

```
┌─────────────────────────────────────┐
│ System instructions (static)        │  ← CACHED
│ Tool definitions (static)           │  ← CACHED
│ Reference documents (static)        │  ← CACHED
│ Few-shot examples (static)          │  ← CACHED
├─────────────────────────────────────┤
│ Conversation history (semi-static)  │  ← PARTIALLY CACHED
├─────────────────────────────────────┤
│ Current user query (dynamic)        │  ← NOT CACHED
└─────────────────────────────────────┘
```

### 2. Prefix Stability

- Never embed timestamps, request IDs, or session tokens in system prompts
- Keep tool definitions stable — use `allowed_tools` (OpenAI) to restrict without modifying the tools array
- Ensure stable JSON key ordering (some languages randomize object keys)
- Use clear separators (`###`, `---`) to divide static and dynamic sections

### 3. Multi-Turn Conversation Strategy

- **Anthropic**: Use automatic caching (`cache_control` at top level) — the cache point moves forward automatically
- **OpenAI**: Benefits automatically; use `previous_response_id` with the Responses API for 40–80% better utilization
- **Gemini**: Use implicit caching for automatic savings; create explicit caches for large static contexts

### 4. Cost Optimization Decision Framework

```
Is your prompt > minimum token threshold?
  └─ No → Caching won't apply. Consider batching or prompt padding.
  └─ Yes → Is the prefix reused frequently?
       └─ Rarely → May not break even on Anthropic (write premium); still free on OpenAI
       └─ Every few minutes → Use 5-min TTL (Anthropic) or default (OpenAI/Gemini)
       └─ Every few hours → Use 1-hour TTL (Anthropic) or explicit cache (Gemini)
       └─ Across sessions → Use extended caching (OpenAI 24h) or explicit cache (Gemini)
```

### 5. Break-Even Analysis

**Anthropic** (5-min TTL): Cache write costs 1.25× but reads cost 0.1×. Break-even at **2 cache reads** per write:
- 1 write + 1 read = 1.25 + 0.1 = 1.35× (vs 2.0× without caching) ✓ savings

**Anthropic** (1-hr TTL): Write costs 2×, reads cost 0.1×. Break-even at **2 cache reads**:
- 1 write + 1 read = 2.0 + 0.1 = 2.1× (vs 2.0× without caching) ✗ loss
- 1 write + 2 reads = 2.0 + 0.2 = 2.2× (vs 3.0× without caching) ✓ savings

**OpenAI**: No write premium. Every cache hit saves 50–90%. Always beneficial.

**Gemini**: Storage costs apply but read discounts of 75–90% make it beneficial for any reuse.

### 6. Agentic Workload Considerations

Agentic systems (multi-step tool-calling loops) present a tension: **caching rewards stable prefixes, but agents dynamically modify context** through tool calls, summaries, and state changes.

Strategies:
- **Maintain a large, stable system prompt** that benefits from caching; treat tool results as dynamic tail content
- **Avoid compaction/summarization of early context** if it breaks the cache prefix — the cache savings may outweigh the token savings from compaction
- **Use sub-agent architectures** where each sub-agent has its own stable prefix
- **Place tool definitions in the cacheable prefix** — they rarely change within a session

### 7. Monitoring & Iteration

Track these metrics across all providers:
- **Cache hit rate** = cached_tokens / total_prompt_tokens × 100%
- **Cost savings** = (base_cost - actual_cost) / base_cost × 100%
- **Latency improvement** = (uncached_TTFT - cached_TTFT) / uncached_TTFT × 100%

Target: >70% cache hit rate for conversation-heavy workloads, >90% for document analysis.

### 8. Provider Selection for Caching

| Scenario | Best Provider Choice |
|----------|---------------------|
| Zero-effort caching, cost flexibility | OpenAI (automatic, no config) |
| Fine-grained control, long documents | Anthropic (breakpoints, mixed TTLs) |
| Video/multimodal analysis, long TTL | Gemini (explicit cache with configurable TTL) |
| Agentic workloads, multi-turn | Anthropic automatic or OpenAI Responses API |
| Budget-sensitive, high reuse | Anthropic (90% read discount) or Gemini 2.5+ (90%) |

---

## Anti-Patterns to Avoid

1. **Dynamic content in prefix**: Timestamps, UUIDs, session IDs early in the prompt destroy cache hits
2. **Unnecessary prompt reformatting**: Rephrasing system instructions between requests invalidates caches
3. **Over-compaction**: Summarizing conversation history saves tokens but breaks the cache — evaluate the tradeoff
4. **Ignoring minimum thresholds**: Prompts below the minimum token count cannot be cached regardless of configuration
5. **Assuming cross-request caching on OpenAI**: Cache hits are best-effort and depend on request routing; don't architect around guaranteed hits
6. **Forgetting JSON key order stability**: Non-deterministic key ordering (Python dicts pre-3.7, some serialization libraries) can cause cache misses

---

## Sources

- [Anthropic Prompt Caching Documentation](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [OpenAI Prompt Caching Guide](https://platform.openai.com/docs/guides/prompt-caching)
- [OpenAI Prompt Caching 201 Cookbook](https://developers.openai.com/cookbook/examples/prompt_caching_201/)
- [Gemini Context Caching Documentation](https://ai.google.dev/gemini-api/docs/caching)
- [Vertex AI Context Caching Overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview)
- [PromptHub: Prompt Caching Comparison](https://www.prompthub.us/blog/prompt-caching-with-openai-anthropic-and-google-models)
- [PromptBuilder: Prompt Caching Token Economics 2025](https://promptbuilder.cc/blog/prompt-caching-token-economics-2025)
- [Gemini Implicit Caching Announcement](https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/)
