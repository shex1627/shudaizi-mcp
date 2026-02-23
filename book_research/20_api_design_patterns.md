# API Design Patterns — JJ Geewax (2021)
**Skill Category:** API Design
**Relevance to AI-assisted / vibe-coding workflows:** The most systematic treatment of API design decisions — prevents agents from making ad-hoc choices on versioning, pagination, errors, and resource naming. When an LLM generates API endpoints, it tends to invent inconsistent conventions on the fly. This book provides the canonical decision framework that makes AI-generated APIs predictable and interoperable.

---

## What This Book Is About

JJ Geewax, a Google engineer who worked on Google Cloud APIs, distills the patterns behind Google's API Improvement Proposals (AIPs, documented at aip.dev) into a language-agnostic guide for designing web APIs. The book is organized around the idea that APIs are fundamentally about *resources* — not procedures — and that a small set of recurring design patterns can handle the vast majority of API surface area decisions.

The book is structured in five parts:

1. **Introduction** — What makes an API "good," why consistency matters, the resource-oriented design philosophy
2. **Design Principles** — Naming, resource relationships, standard methods (CRUD), data types and default values
3. **Fundamentals** — Partial updates (field masks), pagination, filtering, importing/exporting
4. **Resource Relationships** — Singleton sub-resources, cross-references, association resources, polymorphism
5. **Collective Operations** — Copy/move, batch operations, criteria-based operations, long-running operations (LROs), rerunnable jobs, notifications/events

The book draws heavily from Google's real-world experience designing APIs for Cloud, Maps, YouTube, and other services. It is not a REST tutorial or an HTTP methods primer — it assumes you understand HTTP basics and jumps directly into the *design decision patterns* that arise once you start building non-trivial API surfaces.

**Primary audience:** Backend engineers designing resource-oriented APIs, API platform teams establishing standards, and anyone reviewing API surface area decisions.

**Protocol stance:** The book presents patterns in a protocol-agnostic way but with clear dual-track thinking: REST/HTTP+JSON and gRPC/Protocol Buffers. Most patterns are illustrated with both. The Google AIP origin means gRPC/protobuf idioms are first-class, not afterthoughts.

---

## Key Ideas & Mental Models

### 1. Resource-Oriented Design as the Core Paradigm

The foundational mental model: **APIs expose resources, not actions.** Every entity in the system is a resource with a unique identifier, and the API provides a consistent set of operations on those resources. This is the single most important idea in the book and the one most commonly violated in practice.

- Resources have *identifiers* (names/paths), not just IDs
- Resources form *hierarchies* expressed through URL path segments
- The hierarchy encodes ownership and access scope: `projects/123/databases/456/documents/789`
- Thinking in resources forces you to model your domain before you model your endpoints

**Why this matters for AI-assisted workflows:** When an LLM generates API code, it naturally gravitates toward RPC-style "verb" endpoints (`/getUserProfile`, `/sendNotification`). The resource-oriented model provides a simple rule: if it's not a resource with standard methods, it needs explicit justification as a custom method.

### 2. Standard Methods Are the Default; Custom Methods Are the Exception

The book defines five standard methods that map to CRUD operations:

| Standard Method | HTTP Verb | Description |
|----------------|-----------|-------------|
| List           | GET       | Retrieve a collection of resources |
| Get            | GET       | Retrieve a single resource |
| Create         | POST      | Create a new resource |
| Update         | PATCH/PUT | Modify an existing resource |
| Delete         | DELETE    | Remove a resource |

**The key insight:** These five methods handle 80-90% of API interactions. Any operation that doesn't fit these should be a *custom method* — explicitly named, documented, and justified. Custom methods use a colon syntax in REST (`/resources/123:archive`) or additional RPC methods in gRPC.

### 3. The Identifier Hierarchy Is Your Data Model's Public Contract

Resource names follow a strict pattern: `{collection}/{id}/{sub-collection}/{id}`. Examples:
- `users/alice`
- `users/alice/posts/42`
- `projects/my-project/locations/us-east1/instances/prod-db`

This hierarchy is *not* your database schema — it's your API's public contract. The book stresses that the resource hierarchy should reflect *logical ownership and access patterns*, not internal storage layout.

### 4. Field Masks: The Right Way to Do Partial Updates

One of the book's most practical contributions is its thorough treatment of *field masks* — explicit lists of which fields a client wants to read or update. Instead of sending a full resource and guessing what changed, the client sends both the resource and a mask listing exactly which fields to apply.

```
PATCH /users/alice
{
  "user": { "displayName": "Alice B.", "email": "new@example.com" },
  "updateMask": "displayName"
}
```

Only `displayName` is updated; `email` is ignored despite being in the payload. This eliminates an entire class of bugs around unintended field overwrites.

### 5. Pagination as a Contract, Not an Afterthought

Pagination is treated as a first-class design decision with specific patterns:
- Use opaque *page tokens*, not page numbers or offsets
- Return a `nextPageToken` in every response; empty string means no more pages
- Accept `pageSize` (max results per page) with server-enforced defaults and caps
- The server owns the iteration state, not the client

### 6. Long-Running Operations (LROs) as Resources

When an operation takes too long for a synchronous response, the book introduces the LRO pattern: the API returns an *operation resource* that the client can poll or watch.

```
POST /databases:backup → returns Operation { name: "operations/abc", done: false, ... }
GET /operations/abc → returns Operation { done: true, result: { ... } }
```

Operations are themselves resources with standard methods (Get, List, Delete, Cancel). This is one of the most powerful patterns in the book — it makes async work observable and manageable through the same resource-oriented lens.

### 7. Consistency Beats Cleverness

A recurring theme: **a slightly suboptimal but consistent API is better than a locally optimal but inconsistent one.** If every resource uses the same pagination pattern, the same error format, and the same naming conventions, the API becomes learnable. If each endpoint invents its own approach, the API becomes a collection of special cases.

---

## Patterns & Approaches Introduced

### Resource Naming Conventions
- **Collection names** are plural nouns in camelCase: `users`, `chatRooms`, `billingAccounts`
- **Resource IDs** are typically server-assigned, URL-safe strings; optionally client-assignable
- **Resource names** (full paths) are the canonical identifier: `projects/123/topics/my-topic`
- Avoid encoding meaning or hierarchy in IDs themselves — that's what the path structure is for
- Use `-` as a wildcard for collection-level operations: `projects/-/topics` means "topics across all projects"

### Standard Methods in Detail

**Create:**
- POST to the parent collection: `POST /users`
- Optionally support client-specified IDs via a `userId` query parameter
- Return the created resource with server-populated fields (createTime, etag, etc.)
- Idempotency via `requestId` parameter for safe retries

**Get:**
- GET with the resource name: `GET /users/alice`
- Should return the full resource representation
- Use field masks (via `readMask` or `fields` parameter) to request partial responses

**List:**
- GET on the collection: `GET /users`
- Always paginated; return `nextPageToken`
- Support `filter` for server-side filtering (with a defined filter syntax)
- Support `orderBy` for sorting
- Return `totalSize` cautiously — it can be expensive to compute

**Update:**
- PATCH with a field mask is the recommended approach
- PUT (full replacement) is discouraged because it forces clients to know all fields
- Handle missing fields carefully: absent field + no mask = don't touch; absent field + in mask = clear to default
- Support ETags/`If-Match` for optimistic concurrency control

**Delete:**
- DELETE on the resource: `DELETE /users/alice`
- Decide between *hard delete* (gone forever) and *soft delete* (marks as deleted, recoverable)
- Soft delete pattern: set an `expireTime`, provide an `undelete` custom method
- Decide what happens to child resources: cascade delete, or reject if children exist

### Custom Methods
- Named actions that don't fit standard CRUD: `:archive`, `:translate`, `:move`, `:cancel`
- Use POST in REST (even for read-only custom methods, to avoid URL length limits and caching confusion)
- In gRPC, these are additional RPC methods on the service
- Should be rare — if you have many custom methods, reconsider your resource model

### Pagination Patterns
- **Page token pagination:** Opaque cursor-based tokens (preferred)
- Page tokens encode server-side state; clients treat them as opaque strings
- `maxPageSize` is a server-side cap; `pageSize` is a client hint
- Consistency guarantees: the book discusses eventual vs. snapshot consistency during pagination
- Total count (`totalSize`) is optional and should be clearly documented as exact or estimated

### Filtering and Search
- Simple field-based filtering: `filter="status=ACTIVE AND priority>3"`
- The book advocates for a structured filter syntax (similar to Google's AIP-160 filtering)
- Search (full-text) is treated as a separate concern from filtering (structured)

### Error Response Structure
- Errors are structured objects, not just HTTP status codes
- Standard error format includes: `code` (enum), `message` (human-readable), `details` (machine-readable array)
- Error details are typed — each detail type provides specific structured information
- Map internal errors to appropriate external error codes; don't leak implementation details
- Common error codes: INVALID_ARGUMENT, NOT_FOUND, ALREADY_EXISTS, PERMISSION_DENIED, RESOURCE_EXHAUSTED, FAILED_PRECONDITION, ABORTED, INTERNAL

### Versioning Strategies
- **Major versions in the URL path:** `v1`, `v2` — used for breaking changes
- **No minor versions exposed** — additive changes are non-breaking by definition
- Backward compatibility rules:
  - Adding a field: safe
  - Removing a field: breaking
  - Renaming a field: breaking
  - Changing a field type: breaking
  - Adding a new enum value: potentially breaking (for clients with exhaustive switches)
  - Adding a new method: safe
  - Adding a required field to a request: breaking
- The book advocates *stability levels* (alpha, beta, GA) rather than proliferating version numbers
- Alpha APIs can break freely; beta APIs should be cautious; GA APIs must not break

### Backwards Compatibility
- Additive-only changes as the default evolution strategy
- Use field masks to allow old clients to ignore new fields
- Use oneof/polymorphic fields carefully — adding to a oneof can break clients
- Deprecation lifecycle: mark deprecated, set sunset date, remove after notice period
- Versioning is a last resort — design for evolution from day one

### Singleton Sub-Resources
- Resources that have exactly one instance per parent: `users/alice/settings`
- No Create/Delete — they exist implicitly with the parent
- Only Get and Update methods
- Useful for configuration, preferences, metadata

### Association Resources
- For many-to-many relationships: instead of nesting, create an explicit association resource
- `memberships` instead of embedding members in groups: `groups/123/memberships/alice`
- Association resources can carry their own properties (role, joinedTime, etc.)

### Batch Operations
- Batch versions of standard methods: `BatchGet`, `BatchCreate`, `BatchUpdate`, `BatchDelete`
- Request contains an array of individual sub-requests
- Response contains an array of individual sub-responses (preserving order)
- Atomicity decision: all-or-nothing vs. partial success with per-item error reporting
- The book recommends documenting the atomicity guarantee explicitly

### Copy and Move
- Copy creates a new resource based on an existing one: `POST /resources/123:copy`
- Move changes a resource's parent or location: `POST /resources/123:move`
- Both are custom methods, not standard methods
- Move must handle all child resources transitively
- Copy should define whether it deep-copies children or not

### Long-Running Operations (Detailed)
- Operation resource fields: `name`, `done`, `metadata` (progress), `result` or `error`
- Metadata can include progress percentage, status messages, ETAs
- Operations support: Get, List, Delete (cleanup), Cancel (best-effort), Wait (long-poll)
- The `Wait` method is a long-poll alternative to repeated polling — blocks until done or timeout
- LROs decouple the request lifecycle from the operation lifecycle

### Rerunnable Jobs
- For operations that need to be executed repeatedly (scheduled backups, data exports)
- Separate the *configuration* (Job resource) from the *execution* (Execution sub-resource)
- `backupJobs/daily → backupJobs/daily/executions/20210315`
- Jobs have Run custom method; Executions are read-only records

### Notifications and Events
- Push-based alternatives to polling
- The book discusses webhooks and event-driven patterns
- Subscription resources that define callback URLs and filter criteria
- Delivery guarantees and retry policies as explicit API surface

---

## Tradeoffs & Tensions

### 1. Resource Purity vs. Pragmatic RPC
The book strongly advocates resource-oriented design, but real systems frequently need actions that don't map cleanly to CRUD on a resource. The `:archive`, `:translate`, `:approve` pattern works, but teams often face pressure to create dozens of custom methods that effectively recreate an RPC API wearing resource-oriented clothing. **The tension:** When do you stop force-fitting into resources and admit you need an RPC-style endpoint? The book's answer — custom methods with the colon syntax — is pragmatic but can feel like a workaround.

### 2. Field Masks vs. JSON Merge Patch (RFC 7396)
The book advocates field masks (a list of paths to update), which is native to Protocol Buffers and central to Google's APIs. The broader REST ecosystem more commonly uses JSON Merge Patch (send a partial JSON document; null means delete). **The tension:** Field masks are more precise (can distinguish "set to empty string" from "don't touch"), but less familiar to developers outside the Google ecosystem. If your API is REST-only with no protobuf layer, field masks add cognitive overhead. JSON Merge Patch is simpler but can't handle certain edge cases (clearing a field to its default value).

### 3. Opaque Page Tokens vs. Developer-Friendly Pagination
Page tokens are correct (they prevent the skipped-item and duplicate-item bugs of offset pagination), but they frustrate developers who want to jump to page 5 or share a URL for page 3. **The tension:** Correctness vs. developer experience. The book rightly chooses correctness but doesn't deeply address the UX challenges this creates for admin dashboards and similar use cases.

### 4. Consistency vs. Performance in Listing
Paginated List operations face a consistency choice: snapshot isolation (see a consistent view across pages) vs. eventual consistency (cheaper, but items may appear/disappear between pages). The book discusses this but acknowledges there's no universally right answer — it depends on the data store and the use case.

### 5. gRPC-First vs. REST-First Assumptions
The book's Google heritage means patterns are often described in protobuf-native terms first, then translated to REST. This works well for teams using gRPC or both protocols, but can create friction for teams building REST-only APIs. Specific examples:
- Field masks are a native protobuf type (`google.protobuf.FieldMask`) but require manual implementation in REST
- Enum handling differs: protobuf enums have numeric values and `UNSPECIFIED` sentinels; JSON enums are typically strings
- The `oneof` concept has no direct REST equivalent
- Error detail types rely on protobuf's `Any` type for extensibility

### 6. Strict Hierarchy vs. Flat Resources
The book's hierarchical resource naming (`parent/child/grandchild`) works brilliantly for tree-structured data but creates friction when resources have multiple valid parents or don't naturally nest. The association resource pattern helps but adds indirection. Teams frequently debate how deep the hierarchy should go before it becomes unwieldy.

### 7. Soft Delete Complexity
Soft delete (mark deleted, allow undelete) is more user-friendly but significantly more complex:
- Deleted resources shouldn't appear in List results by default
- But they need to be findable for undelete
- Name/ID uniqueness conflicts when a new resource wants the deleted resource's name
- Purge timelines and storage costs
- The book addresses these but the implementation burden is real

### 8. Versioning Discipline vs. Iteration Speed
The book's "additive-only changes with stability levels" approach requires significant discipline. In early-stage products, the desire to rename fields, restructure resources, or change semantics is constant. The alpha/beta/GA stability model helps but creates a long path to stability. **The tension:** Premature stability commitments vs. breaking early adopters.

---

## What to Watch Out For

### Google-Centrism
The book is excellent but reflects Google's specific context: massive scale, long-lived APIs, internal service mesh, Protocol Buffers everywhere, dedicated API review teams. Smaller teams may find some patterns over-engineered for their scale. Specifically:
- LRO patterns are critical at Google's scale but may be premature for a startup's MVP
- The filter syntax (AIP-160) is powerful but implementing a full filter parser is non-trivial
- Stability levels (alpha/beta/GA) assume a large user base that needs migration windows

### Not a REST Best Practices Book
This book assumes you already know REST, HTTP, and JSON. It doesn't cover content negotiation, HATEOAS, cache headers, rate limiting details, or authentication patterns. It's about *design patterns for API resources*, not about HTTP protocol mechanics.

### Limited Coverage of GraphQL and Event-Driven Architectures
The book is focused on request-response APIs (REST and gRPC). GraphQL is barely mentioned. Event-driven architectures (Kafka, event sourcing, CQRS) are touched on only in the notifications chapter. If your API surface is primarily GraphQL or event-based, you'll need supplementary material.

### Implementation Gap
The book describes *what* patterns to use but largely leaves *how to implement them* to the reader. For example, it explains that pagination should use opaque tokens but doesn't discuss how to encode cursor state, handle cursor expiration, or implement cursors over different database backends. This is deliberate (the book is language-agnostic) but can leave implementers with questions.

### The Field Mask Learning Curve
If your team isn't using Protocol Buffers, field masks will feel foreign. The concept is sound, but expect pushback from developers accustomed to JSON Merge Patch or simple PUT-full-replacement approaches. Budget time for education.

### Naming Convention Rigidity
The book's naming conventions (camelCase fields, plural collections, specific patterns for boolean fields like `isActive` vs. `active`) are well-reasoned for Google's ecosystem but may conflict with existing conventions in your stack (e.g., snake_case in Python/Ruby ecosystems, singular table names in some ORM conventions).

---

## Applicability by Task Type

### API Design (Primary)
This is the book's core use case. Every pattern directly applies when designing new API surfaces. Use it as a checklist: Have you defined your resources? Are standard methods sufficient? What's your pagination strategy? Error format? Versioning plan?

### Architecture Planning
The resource hierarchy design and the LRO/job patterns are directly relevant to architecture decisions. The book helps answer "how should services expose their capabilities?" which is a foundational architecture question.

### Code Review of API Endpoints
Use the book's patterns as a review checklist:
- Are resource names following conventions?
- Is pagination using tokens, not offsets?
- Are partial updates using field masks or merge patch (not PUT-everything)?
- Are custom methods justified, or could they be standard methods on a better resource model?
- Are errors structured and using appropriate codes?
- Is the API additive-only compatible with previous versions?

### Feature Design (API Surface Changes)
When adding features to an existing API, the book's backwards compatibility rules and versioning guidance are essential. It answers: "Can I add this field? Do I need a new version? Should this be a new resource or a custom method on an existing one?"

### Writing Technical Documentation (API Docs)
The book's emphasis on structured error details, explicit pagination contracts, and field-level semantics directly informs what good API documentation should cover. The resource-oriented model gives documentation a natural structure.

### AI-Assisted Code Generation
When prompting an LLM to generate API code, the patterns from this book serve as constraints:
- "Generate a REST API for managing X using resource-oriented design with standard methods"
- "Use page-token pagination, not offset pagination"
- "Implement partial updates with field masks"
- "Return structured error responses with code, message, and details"

Without these constraints, LLMs default to inconsistent, ad-hoc API designs.

---

## Relationship to Other Books in This Category

### vs. "REST API Design Rulebook" (Mark Masse, 2011)
Masse's book is an earlier, more HTTP-focused treatment. It covers URI design, media types, and HTTP method semantics in detail but predates many modern patterns (page tokens, field masks, LROs). Geewax's book is the spiritual successor with a decade more industry experience baked in.

### vs. "Designing Web APIs" (Brenda Jin, Saurabh Sahni, Amir Shevat, 2018)
The O'Reilly book covers a broader scope: API business strategy, developer experience, API management platforms. It's more about the *what and why* of APIs at a product level. Geewax goes much deeper on the *how* of individual design decisions. They complement each other well.

### vs. "The Design of Web APIs" (Arnaud Lauret, 2019)
Lauret's book emphasizes the API design process — how to go from user stories to API contracts using an "API Goals Canvas." It's more methodology-focused. Geewax is more pattern-focused. Use Lauret for the design process, Geewax for the design decisions within that process.

### vs. Google's AIP Site (aip.dev)
The book is essentially a readable, structured version of the Google API Improvement Proposals with added rationale and examples. The AIP site is more reference-oriented and continues to evolve (new AIPs are added). The book provides better pedagogy; the site provides more complete coverage and stays current. Use both: the book for learning, the site for reference.

### vs. "RESTful Web Services" (Richardson & Ruby, 2007) and "RESTful Web APIs" (Richardson, Amundsen & Ruby, 2013)
These books ground REST in the original architectural constraints (Fielding's dissertation). They care deeply about hypermedia, content negotiation, and HATEOAS. Geewax's book is more pragmatic — it doesn't pursue hypermedia purity but instead provides patterns that work in real production APIs. If you want theoretical REST grounding, read Richardson. If you want practical patterns, read Geewax.

### vs. "gRPC: Up and Running" (Kasun Indrasiri, 2020)
The gRPC book covers the protocol mechanics — how to define services in protobuf, implement them, handle streaming, etc. Geewax's patterns apply to gRPC services but focus on the *design level*, not the implementation level. Read the gRPC book for how gRPC works; read Geewax for how to design good services regardless of protocol.

### vs. "Building Microservices" (Sam Newman, 2015/2021)
Newman covers the broader microservices architecture — service decomposition, deployment, testing, organizational concerns. API design is one chapter. Geewax provides the detailed patterns for the API surfaces *between* those microservices. They pair naturally.

---

## Freshness Assessment

**Publication date:** September 2021

**What has aged well:**
- Resource-oriented design remains the dominant paradigm for web APIs
- Standard methods (CRUD) mapping is unchanged
- Pagination with page tokens is now industry standard (Stripe, Twilio, GCP, AWS all use variants)
- Field mask / partial update patterns are stable
- Error response structure recommendations align with RFC 7807 (Problem Details) direction
- The AIP framework continues to grow at aip.dev with the same foundational patterns
- Versioning advice (additive-only, stability levels) is more relevant than ever as API ecosystems grow

**What has shifted since publication:**
- **OpenAPI 3.1 adoption** has accelerated; tooling for API-first design (Stoplight, Redocly) has matured. The book doesn't deeply cover spec-driven design workflows.
- **GraphQL maturity** — GraphQL has continued to mature with federation, persisted queries, and better tooling. The book's REST/gRPC focus is still relevant but covers less of the API landscape than it did in 2021.
- **AI-generated APIs** — LLMs generating API code didn't exist as a use case when the book was written. The patterns are *more* valuable now because they provide constraints for AI generation, but the book doesn't discuss this workflow.
- **gRPC-Web and Connect protocol** — The Connect protocol (from Buf) has simplified gRPC for web clients, making the book's gRPC patterns more accessible to frontend-heavy teams.
- **Event-driven APIs** (AsyncAPI, CloudEvents) have gained significant traction. The book's brief treatment of notifications is now the weakest chapter relative to industry practice.
- **API governance tools** — Linting tools (Spectral, Buf lint) can now enforce many of the book's patterns automatically. The book predates widespread adoption of these tools.

**Overall freshness: 8.5/10** — The core patterns are durable. The main gap is around event-driven APIs and modern API-first tooling workflows. The patterns themselves haven't been superseded.

---

## Key Framings Worth Preserving

### "An API is a user interface for developers"
Just as UI design has principles (consistency, feedback, affordance), API design has analogous principles. Every naming choice, every error message, every pagination decision is a UX decision for the developer consuming your API.

### "The resource model is your API's most important design decision"
Before you think about endpoints, methods, or data formats, figure out what your resources are, how they relate to each other, and what their hierarchy looks like. Everything else follows from this.

### "Standard methods are the verbs; resources are the nouns"
This framing immediately clarifies API structure. You shouldn't need a verb in your URL because the HTTP method *is* the verb. If you need a verb, it's a custom method, and you should think hard about whether there's a resource model that eliminates the need for it.

### "Field masks make intentions explicit"
The difference between "I'm sending you this field because I want to update it" and "I'm sending you this field because I had to send you the whole object" is the source of countless API bugs. Field masks eliminate this ambiguity.

### "Operations are resources too"
When you reify a long-running operation as a resource, you get observability (Get), discoverability (List), cleanup (Delete), and control (Cancel) for free. This is the resource-oriented philosophy applied to its logical conclusion.

### "Design for evolution, not for versioning"
Versioning is a failure mode, not a feature. The goal is to design APIs that can evolve without breaking changes. Additive-only changes, optional fields, field masks, and stability levels are all tools for avoiding the need for version bumps.

### "Consistency across an API surface is worth more than local optimization"
If your API has 50 resources and 49 of them paginate the same way, the 50th should too — even if a slightly different approach would be marginally better for that specific resource. The learning cost of inconsistency exceeds the local optimization benefit.

### The Custom Method Litmus Test
"If you find yourself creating many custom methods on a resource, step back and ask: is there a sub-resource or association resource hiding in here?" Often, what feels like an action (`/orders/123:ship`) is actually a state transition that could be modeled as updating a status field or creating a `shipment` sub-resource.

### The Hierarchy Depth Rule
Keep resource hierarchies shallow (typically 2-3 levels). Deep hierarchies create long URLs, complex permission models, and rigid coupling between resources. If you're past three levels, consider flattening with cross-references instead of nesting.

### "Soft delete is a feature, not a default"
Don't implement soft delete everywhere just because it seems safer. It adds complexity (filtering, uniqueness conflicts, storage costs, GDPR implications). Implement it where users genuinely need undo capability or where audit requirements demand it.
