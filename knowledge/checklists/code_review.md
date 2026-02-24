---
task: code_review
description: Review code for quality, readability, maintainability, and correctness
primary_sources: ["06", "14", "15", "16"]
secondary_sources: ["04", "12", "13", "22"]
anthropic_articles: ["a05", "a20"]
version: 1
updated: 2026-02-22
---

# Code Review Checklist

## Phase 1: Readability & Naming

- [ ] Every name reveals intent -- `elapsedTimeInDays` over `d` [15]
- [ ] Names are pronounceable, searchable, and free of encodings or abbreviations [15]
- [ ] Class names are nouns; method names are verbs [15]
- [ ] No "mysterious names" -- you can tell what something does from its name alone [16]
- [ ] If a name is hard to pick, treat it as a design smell -- the abstraction may be confused [06]
- [ ] No disinformation -- `accountList` is actually a list, not some other structure [15]
- [ ] Comments explain *why* and link to external context, not *what* the code does line-by-line [06][15]
- [ ] Interface-level comments describe the module's abstraction, preconditions, and side effects [06]
- [ ] No stale or misleading comments that have drifted from the code [15][16]
- [ ] Code reads top-down like a narrative (stepdown rule) [15]

## Phase 2: Structure & Design

- [ ] Modules are deep -- interface is simpler than the implementation it hides [06]
- [ ] No shallow modules: thin wrappers, manager classes, or pass-through methods that just delegate [06]
- [ ] Each layer provides a fundamentally different abstraction than adjacent layers [06]
- [ ] No information leakage -- design decisions are encapsulated in one module, not scattered [06]
- [ ] No temporal decomposition -- code is organized by information domain, not execution order [06]
- [ ] DRY applied to *knowledge*, not just code appearance -- each fact has one authoritative home [14]
- [ ] Orthogonality check: "If I change requirements behind one function, how many modules break?" [14]
- [ ] Dependencies point inward toward higher-level policies; business logic does not import infrastructure [04]
- [ ] No pass-through variables threaded through long call chains unused [06]
- [ ] Interfaces are somewhat general-purpose without being speculative [06]
- [ ] Configuration parameters are avoided when the module can determine a reasonable default [06]
- [ ] Complexity is pulled downward into implementations, not pushed up to callers [06]

## Phase 3: Functions & Methods

- [ ] Each function does one thing at one level of abstraction [15]
- [ ] Functions are not decomposed past the point where decomposition itself becomes the complexity [06]
- [ ] Extracted sub-methods have interfaces simpler than the body they replaced [06]
- [ ] No flag arguments -- split into separate explicit functions instead [16]
- [ ] Long parameter lists replaced with parameter objects or preserved whole objects [16]
- [ ] Command-query separation: functions either change state or return a value, not both [15][16]
- [ ] Guard clauses used to flatten deeply nested conditionals [16]
- [ ] No "programming by coincidence" -- code relies on documented contracts, not accidental behavior [14]

## Phase 4: Error Handling

- [ ] Errors are designed out of existence where possible -- broaden specs so edge cases become valid [06]
- [ ] Exceptions used rather than error codes; error handling does not obscure main logic [15]
- [ ] Null is neither returned nor accepted -- use special case objects or Optional patterns [15]
- [ ] Assertions document and enforce assumptions that "can't happen" [14]
- [ ] Design by contract: preconditions, postconditions, and invariants are explicit [14]
- [ ] Each error provides enough context to diagnose without a debugger [15]

## Phase 5: Testing

- [ ] Tests verify observable behavior, not implementation details [12]
- [ ] Refactoring internals without changing behavior does not break the tests [12]
- [ ] Mocks used only for unmanaged out-of-process dependencies (APIs, message buses), not internal collaborators [12]
- [ ] No testing of private methods -- if they need tests, extract them into their own class [12]
- [ ] Tests organized around behaviors, not around classes [12]
- [ ] Test names read as behavior specifications a non-author can understand [13]
- [ ] Tests follow Arrange-Act-Assert with one Act per test and no branching logic [12]
- [ ] Domain logic with few collaborators has unit tests; orchestration code has integration tests [12]
- [ ] Trivial code (simple getters, no logic) is not tested -- focus coverage on complex domain logic [12]
- [ ] Refactoring is supported by existing tests before it begins; no refactoring without tests [16]

## Phase 6: Refactoring Opportunities

- [ ] Duplicated code identified -- apply Extract Function or Pull Up Method [16]
- [ ] Feature envy flagged -- function uses another module's data more than its own; consider Move Function [16]
- [ ] Long functions broken down via Extract Function, Decompose Conditional, or Replace Temp with Query [16]
- [ ] Data clumps traveling together replaced with Introduce Parameter Object or Extract Class [16]
- [ ] Repeated switch/case structures consolidated via Replace Conditional with Polymorphism [16]
- [ ] Dead code removed [16]
- [ ] Preparatory refactoring applied: "Make the change easy, then make the easy change" [16]
- [ ] Boy Scout Rule followed: code left cleaner than it was found [15]

## Phase 7: Concurrency (if applicable)

- [ ] No sequential awaits that could run concurrently -- use `gather`, `create_task`, or `TaskGroup` [22]
- [ ] No blocking calls inside async functions (`time.sleep`, `requests`, sync DB drivers) [22]
- [ ] Timeouts set on all external I/O calls via `asyncio.wait_for()` or client-level timeouts [22]
- [ ] Concurrency bounded with semaphores -- no unbounded fan-out that exhausts resources [22]
- [ ] No fire-and-forget tasks -- every task is awaited or managed by a TaskGroup [22]
- [ ] Shared mutable state protected with `asyncio.Lock` across await boundaries [22]
- [ ] Async used only for I/O-bound work; CPU-bound work offloaded to `run_in_executor` or process pool [22]

## Phase 8: Implementation Patterns (Proactive)

Apply these patterns **while writing code**, not just during review.

### Concurrency & I/O
- [ ] When making 2+ independent I/O calls, use concurrent execution (`asyncio.gather`, `TaskGroup`, `Promise.all`) rather than sequential awaits [22]
- [ ] When calling external services from async code, use async-native clients (`httpx`, `aiohttp`) not synchronous libraries (`requests`) [22]
- [ ] When adding any external I/O call, set a timeout — prefer client-level defaults, override per-call when needed [22]
- [ ] When creating concurrent work, bound it with a semaphore — decide the concurrency limit explicitly [22]

### Module Design
- [ ] When creating a new class or module, verify it will be deep: the interface should be simpler than what it hides. If the class just delegates, it shouldn't exist yet [06]
- [ ] When adding a layer (service, controller, adapter), verify it provides a genuinely different abstraction than adjacent layers [06]
- [ ] When a design decision (format, algorithm, protocol) could leak across modules, encapsulate it in exactly one module before writing call sites [06]

### Functions
- [ ] When a function will both change state and compute a result, split it into a command and a query before writing the body [15][16]
- [ ] When a function will take more than 3 parameters, introduce a parameter object before adding parameters one-by-one [16]

### Error Handling
- [ ] When calling an external service, design the error path before the happy path — decide: retry with backoff? fallback? propagate? [17][14]
- [ ] When an edge case arises, first ask "can I broaden the spec to define this out of existence?" before adding a conditional [06]

---

## Code Smells to Flag

| Smell | Signal | Source |
|---|---|---|
| Mysterious Name | Cannot tell what it does from the name | [16] |
| Shotgun Surgery | One change requires edits in many places | [16] |
| Feature Envy | Function reaches into another module's data repeatedly | [16] |
| Primitive Obsession | Strings/ints used where a domain object belongs | [16] |
| Middle Man | Class delegates almost everything, does nothing itself | [16] |
| Speculative Generality | Abstractions built for imagined future needs | [16] |
| Data Clumps | Same group of parameters travels together everywhere | [16] |
| Divergent Change | One module changes for multiple unrelated reasons | [16] |
| Lazy Element | Class or function does too little to justify its existence | [16] |
| Message Chains | `a.getB().getC().doThing()` -- Law of Demeter violation | [15][16] |
| Shallow Module | Interface nearly as complex as implementation | [06] |
| Information Leakage | Same design decision reflected in multiple modules | [06] |
| Broken Window | Hack or shortcut left without acknowledgment or ticket | [14] |

---

## Key Questions to Ask

1. "Is this interface simpler than the implementation it hides?" -- the deep module test [06]
2. "Does this force callers to know about implementation details?" -- the information leakage test [06]
3. "If I dramatically change requirements behind this function, how many modules are affected?" -- the orthogonality test [14]
4. "Does the code rely on documented contracts or accidental behavior?" -- the coincidence test [14]
5. "Would the end user or calling code notice if this internal detail changed?" -- the observable behavior test [12]
6. "If I refactored internals without changing behavior, would the tests break?" -- the fragile test test [12]
7. "Is this change introducing a broken window that will compound?" [14]
8. "Can I define this error out of existence by broadening the method's specification?" [06]
9. "What is the simplest interface that covers all current needs?" [06]
10. "When I read this function, does it do what its name led me to expect?" -- principle of least surprise [15]
