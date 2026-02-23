---
task: api_design
description: Design or review an API surface using resource-oriented patterns, consistency rules, and agent-tool principles
primary_sources: ["20"]
secondary_sources: ["01", "04", "05", "06"]
anthropic_articles: ["a06", "a07"]
version: 1
updated: 2026-02-22
---

# API Design Checklist

## Phase 1: Resource Modeling

- [ ] Identify every entity as a resource with a unique identifier — APIs expose resources, not actions [20]
- [ ] Define resource hierarchies that reflect logical ownership and access patterns, not internal storage layout: `{collection}/{id}/{sub-collection}/{id}` [20]
- [ ] Keep hierarchies shallow (2-3 levels); flatten with cross-references instead of deep nesting [20]
- [ ] Use plural nouns in camelCase for collection names: `users`, `chatRooms`, `billingAccounts` [20]
- [ ] For many-to-many relationships, create explicit association resources with their own properties rather than embedding lists [20]
- [ ] For configuration or preferences that have exactly one instance per parent, use singleton sub-resources (Get + Update only, no Create/Delete) [20]
- [ ] Ensure source-code dependencies point inward — domain logic must not depend on API transport or framework details [04]

## Phase 2: Standard Methods & Operations

- [ ] Default to the five standard methods (List, Get, Create, Update, Delete) — they should handle 80-90% of interactions [20]
- [ ] Use PATCH with field masks for partial updates rather than PUT full-replacement — field masks make client intentions explicit and prevent unintended overwrites [20]
- [ ] Support idempotent Create via `requestId` parameter for safe retries [20]
- [ ] Support optimistic concurrency control via ETags / `If-Match` on Update [20]
- [ ] For Delete, decide between hard delete and soft delete explicitly; soft delete requires `expireTime`, `undelete`, and filtered List behavior [20]
- [ ] Justify every custom method (`:archive`, `:translate`, `:move`) — if many custom methods accumulate, reconsider the resource model [20]
- [ ] For operations taking longer than a synchronous response, return a Long-Running Operation resource that supports Get, List, Delete, Cancel, and Wait [20]

## Phase 3: Pagination, Filtering & Errors

- [ ] Use opaque page-token pagination, not page numbers or offsets — the server owns the iteration state [20]
- [ ] Return `nextPageToken` in every List response; empty string means no more pages [20]
- [ ] Accept `pageSize` as a client hint with server-enforced defaults and caps [20]
- [ ] Provide structured error responses: `code` (enum), `message` (human-readable), `details` (machine-readable typed array) — never leak implementation details [20]
- [ ] Map internal errors to appropriate external codes: INVALID_ARGUMENT, NOT_FOUND, ALREADY_EXISTS, PERMISSION_DENIED, RESOURCE_EXHAUSTED, FAILED_PRECONDITION [20]
- [ ] Document whether paginated List provides snapshot or eventual consistency across pages [20]
- [ ] For data-heavy queries, verify the isolation level matches the actual requirement — many databases default to weaker isolation than developers assume [01]

## Phase 4: Versioning & Evolution

- [ ] Design for evolution, not for versioning — versioning is a failure mode [20]
- [ ] Use additive-only changes as the default evolution strategy: adding a field is safe; removing, renaming, or retyping a field is breaking [20]
- [ ] Use stability levels (alpha/beta/GA) rather than proliferating version numbers [20]
- [ ] When breaking changes are unavoidable, use major versions in the URL path (`v1`, `v2`) and provide a deprecation lifecycle with sunset dates [20]
- [ ] Never add a required field to an existing request — this is a breaking change [20]
- [ ] Decompose services along bounded contexts — each service boundary should be independently deployable [05]
- [ ] Ensure the API interface is "somewhat general-purpose": stable enough for future extension without interface changes, but not speculatively over-engineered [06]

## Phase 5: Consistency & Naming Conventions

- [ ] A slightly suboptimal but consistent API is better than a locally optimal but inconsistent one — consistency across the surface beats local optimization [20]
- [ ] Apply the same pagination pattern, error format, and naming conventions to every resource [20]
- [ ] Avoid encoding meaning in IDs — use the path structure for hierarchy and relationships [20]
- [ ] Use `-` as a wildcard for collection-level operations: `projects/-/topics` [20]
- [ ] The interface should be simpler than its implementation — every API module must absorb significant complexity to justify its existence (deep module test) [06]
- [ ] Design errors out of existence where possible: broaden method specifications so formerly-error cases become valid behavior [06]

## Phase 6: Agent & Tool Compatibility

- [ ] Consolidate related operations into fewer, more purposeful tools — more tools do not always lead to better agent outcomes [a06]
- [ ] Use clear hierarchical namespacing for tool discovery: common prefixes for services and resources [a06]
- [ ] Return meaningful context: replace cryptic UUIDs with human-readable fields; include a `response_format` parameter for concise vs. detailed responses [a06]
- [ ] Optimize for token efficiency: implement pagination, filtering, and truncation with sensible defaults; include helpful error messages that guide toward efficient strategies [a06]
- [ ] Treat tool descriptions as prompt engineering: describe tools as you would to a new hire, with clear specifications [a06]
- [ ] For large tool catalogs (10+ tools), consider tool search patterns with deferred loading to reduce context usage by 85% [a07]
- [ ] Support programmatic tool calling: design responses that are parseable and composable for multi-step orchestration [a07]

---

## Key Questions to Ask

1. "Is every endpoint a resource with standard methods, or am I smuggling RPC-style verbs into the URL?" [20]
2. "Is this interface simpler than the implementation it hides?" — the deep module test [06]
3. "If I have many custom methods on one resource, is there a sub-resource or association resource hiding in here?" [20]
4. "What happens when a client sends a partial update without a field mask — does the API know what the client intends?" [20]
5. "Can this API evolve without a version bump? What is the smallest additive change that solves the need?" [20]
6. "Would an AI agent be able to discover, invoke, and parse the response of this endpoint without human help?" [a06]
7. "Does this dependency point inward toward domain logic or outward toward infrastructure?" [04]
8. "What consistency guarantee does this paginated list provide across pages?" [01][20]

---

## Anti-Patterns to Flag

| Anti-Pattern | Signal | Source |
|---|---|---|
| **RPC in REST clothing** | URLs contain verbs (`/getUserProfile`, `/sendNotification`) instead of resource nouns with standard methods | [20] |
| **Offset pagination** | Using page numbers or offsets instead of opaque tokens — causes skipped/duplicate items when data changes | [20] |
| **PUT-everything updates** | Requiring clients to send the full resource on every update — causes unintended overwrites of fields the client did not mean to change | [20] |
| **Unstructured errors** | Returning bare HTTP status codes or free-text error messages without machine-readable codes and typed details | [20] |
| **Premature versioning** | Creating `v2` for what could have been an additive, non-breaking change | [20] |
| **Deep hierarchy sprawl** | Resource paths exceeding 3 levels of nesting — creates long URLs, rigid coupling, and complex permission models | [20] |
| **Shallow module** | API endpoint is a thin wrapper that just passes calls through — increases interface surface without absorbing complexity | [06] |
| **Leaking internals** | Error messages, field names, or resource structures that expose database schema, internal service names, or implementation details | [04][20] |
| **Tool explosion** | Dozens of narrow, overlapping tools that confuse agents — consolidate related operations into fewer purposeful tools | [a06] |
| **Opaque tool responses** | Returning only UUIDs and codes without human-readable context — forces agents into extra lookup calls | [a06] |
| **Missing idempotency** | Create operations without a `requestId` — retries cause duplicate resources | [20] |
| **Cargo-cult soft delete** | Implementing soft delete everywhere without considering uniqueness conflicts, storage costs, and GDPR implications | [20] |
