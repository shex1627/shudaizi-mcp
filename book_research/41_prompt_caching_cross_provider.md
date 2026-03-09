# Prompt Caching: Cross-Provider Research Synthesis (2025–2026)
**Skill Category:** LLM / AI Engineering — Cost & Latency Optimization
**Relevance to AI-assisted / vibe-coding workflows:** Directly applicable to any system making repeated LLM API calls with shared context — reduces cost by up to 90% and latency by up to 80%.

---

## What This Research Covers

This is a cross-provider synthesis of prompt caching mechanisms across the three major LLM API providers: Anthropic (Claude), OpenAI (GPT/o-series), and Google (Gemini). Prompt caching stores the KV-cache (key-value attention tensors) of previously processed prompt prefixes so subsequent requests with identical prefixes skip recomputation. All three providers support it as of 2025, but with fundamentally different implementation philosophies.

---

## Key Ideas & Mental Models

### 1. The Three Caching Philosophies

**Anthropic: Developer-Controlled Precision.** Offers both automatic and explicit caching with up to 4 breakpoints per request, two TTL tiers (5 min, 1 hour), and mixed TTLs within a single request. Charges a write premium (1.25–2×) but gives 90% read discount. Best for developers who want fine-grained control over what gets cached and for how long.

**OpenAI: Zero-Configuration Automation.** Fully automatic — no code changes, no configuration, no write fees. Routes requests to servers that recently processed the same prefix using a hash of the first ~256 tokens. Best for developers who want caching without thinking about it. Trade-off: no control over cache behavior.

**Google: Named Cache Objects.** Explicit caching creates named, managed cache objects with configurable TTLs (default 1 hour). Implicit caching (automatic, since May 2025) provides opportunistic savings. Best for large static contexts (video, documents) that are reused across many requests over extended periods.

### 2. The Golden Rule: Static First, Dynamic Last

Across all providers, prompt caching works on **prefixes** — the beginning of the prompt. The single most impactful optimization is structuring prompts so static content (system instructions, tool definitions, reference documents, few-shot examples) appears first, and dynamic content (user queries, session state) appears last. Any change to prefix content invalidates the cache for everything after it.

### 3. The Caching-Compaction Trade-Off

This is the most important insight for agentic workloads: **caching rewards stable prefixes, but context engineering techniques (compaction, summarization, truncation) modify the prefix and break the cache.** You must evaluate whether the token savings from compaction outweigh the cache savings from prefix stability. In many cases, paying for a longer but stable prefix is cheaper than a shorter but constantly-changing one.

### 4. Break-Even Economics

Each provider has different break-even points:
- **OpenAI**: Every cache hit is beneficial (no write premium). Always use.
- **Anthropic (5-min TTL)**: Breaks even at 2 reads per write. Very favorable for active conversations.
- **Anthropic (1-hr TTL)**: Breaks even at 2+ reads per write. Better for periodic access patterns.
- **Gemini**: Storage costs apply but 75–90% read discounts make any meaningful reuse profitable.

### 5. Prefix Stability Is an Engineering Discipline

Cache hits require **exact** prefix matches. Subtle changes that break caching:
- Timestamps or request IDs embedded in system prompts
- Non-deterministic JSON key ordering (Python dicts, some serialization libraries)
- Tool definition changes (adding, removing, or reordering tools)
- Whitespace or formatting differences
- Different image encodings of the same image

---

## Patterns & Approaches

### Pattern 1: Layered TTL Architecture (Anthropic)
Use mixed TTLs within a single request — 1-hour TTL for truly static content (system instructions, reference documents), 5-minute TTL for session-level context (conversation history). This minimizes write costs while maximizing hit rates.

```json
{
    "system": [
        {"type": "text", "text": "System instructions...",
         "cache_control": {"type": "ephemeral", "ttl": "1h"}},
        {"type": "text", "text": "Session context...",
         "cache_control": {"type": "ephemeral"}}
    ]
}
```

### Pattern 2: Routing-Sticky Keys (OpenAI)
Use `prompt_cache_key` to improve routing stickiness. Per-user or per-conversation keys ensure requests from the same context land on the same inference server:

```python
response = client.chat.completions.create(
    model="gpt-4.1",
    prompt_cache_key="user-12345",
    messages=[...]
)
```

### Pattern 3: Named Cache Objects for Document Analysis (Gemini)
Create explicit cache objects for large reference documents that will be queried multiple times:

```python
cache = genai.caching.CachedContent.create(
    model="gemini-2.5-flash",
    display_name="quarterly-report",
    contents=[large_document],
    ttl=datetime.timedelta(hours=4),
)
model = genai.GenerativeModel.from_cached_content(cached_content=cache)
```

### Pattern 4: Tool-Definition Caching
Place tool definitions at the start of the cacheable prefix. Tools rarely change within a session, making them ideal cached content. On Anthropic, place `cache_control` on the last tool definition to cache all tools as a prefix block.

### Pattern 5: Sub-Agent Prefix Isolation
In multi-agent systems, give each sub-agent its own stable system prompt. This allows each agent's prefix to be independently cached, rather than having a single monolithic prefix that breaks when any agent's context changes.

### Pattern 6: Responses API for Multi-Turn (OpenAI)
Use `previous_response_id` in the OpenAI Responses API for 40–80% better cache utilization compared to Chat Completions in multi-turn conversations.

---

## Tradeoffs & Pitfalls

### Pitfall 1: Over-Optimizing for Caching at the Cost of Intelligence
Don't sacrifice context quality for cache stability. If compacting conversation history into a summary would significantly improve model reasoning, do it — even if it breaks the cache. Evaluate empirically.

### Pitfall 2: Assuming Guaranteed Cache Hits (OpenAI)
OpenAI caching is best-effort. Load balancing distributes excess traffic across machines, each starting with an empty cache. Don't architect around guaranteed hits — treat cache savings as a bonus, not a budget line item.

### Pitfall 3: Ignoring Minimum Token Thresholds
Prompts below the minimum (1024–4096 tokens depending on provider and model) cannot be cached. Don't add `cache_control` to short prompts expecting savings.

### Pitfall 4: Dynamic Tool Definitions
If your system generates or modifies tool definitions per-request (e.g., based on user permissions), this breaks tool caching. Use `allowed_tools` (OpenAI) or filter at the application layer instead of modifying the tools array.

### Pitfall 5: The 20-Block Lookback Limit (Anthropic)
Anthropic only checks 20 blocks backward from each explicit breakpoint. Long conversations (>20 blocks) need additional breakpoints placed earlier, or early modifications won't produce cache hits.

### Pitfall 6: Storage Costs on Long TTLs (Gemini)
Explicit caches on Gemini incur storage costs based on token-hours. Very large caches with long TTLs can accumulate meaningful storage charges. Monitor and delete unused caches.

---

## Provider-Specific Quick Reference

### Anthropic
- **Activation**: `cache_control: {"type": "ephemeral"}` (automatic) or on individual blocks (explicit)
- **TTL options**: 5 min (default, 1.25× write), 1 hour (2× write)
- **Read discount**: 90% (0.1× base input)
- **Max breakpoints**: 4 per request
- **Min tokens**: 1024–4096 (model-dependent)
- **Monitoring**: `usage.cache_creation_input_tokens`, `usage.cache_read_input_tokens`
- **Isolation**: Per-organization (per-workspace from Feb 2026)
- **ZDR compatible**: Yes (stores hashes, not raw text)

### OpenAI
- **Activation**: Fully automatic (no code changes)
- **Cache policies**: In-memory (5–10 min, default), Extended (24h, opt-in)
- **Read discount**: 50–90% (model-dependent, no write premium)
- **Min tokens**: 1024, increments of 128
- **Monitoring**: `usage.prompt_tokens_details.cached_tokens`
- **Routing**: Hash of first ~256 tokens, improved with `prompt_cache_key`
- **ZDR**: Extended caching not eligible

### Gemini
- **Activation**: Implicit (automatic), Explicit (`CachedContent.create`)
- **TTL**: 1 hour default (configurable)
- **Read discount**: 90% (Gemini 2.5+), 75% (Gemini 2.0)
- **Min tokens**: 1024–4096 (model-dependent)
- **Management**: Create, List, Update (TTL only), Delete
- **Content types**: System instructions, video, PDFs, text, code

---

## Actionable Checklist for Production Systems

- [ ] Structure all prompts with static content first, dynamic content last
- [ ] Verify prompts exceed minimum token thresholds for target provider/model
- [ ] Eliminate dynamic content (timestamps, UUIDs) from prompt prefixes
- [ ] Ensure stable JSON key ordering in tool definitions and structured content
- [ ] Choose appropriate TTL based on access patterns (frequency of reuse)
- [ ] For Anthropic: decide between automatic vs explicit caching based on control needs
- [ ] For OpenAI: use `prompt_cache_key` for workloads with user/session affinity
- [ ] For Gemini: create explicit caches for large static contexts; rely on implicit for the rest
- [ ] Monitor cache hit rates and cost savings; target >70% hit rate for conversational workloads
- [ ] Evaluate the caching-vs-compaction trade-off for agentic workloads empirically
- [ ] In multi-agent systems, isolate sub-agent prefixes for independent caching
- [ ] Keep tool definitions stable within sessions; filter availability at the application layer
- [ ] For long conversations (>20 turns), add intermediate cache breakpoints (Anthropic)
- [ ] Clean up unused explicit caches (Gemini) to avoid storage cost accumulation
