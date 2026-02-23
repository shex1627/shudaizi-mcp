---
task: test_strategy
description: Evaluate and design a test strategy for a codebase, feature, or system
primary_sources: ["12", "13"]
secondary_sources: ["06", "14", "16"]
anthropic_articles: ["a11", "a13"]
version: 1
updated: 2026-02-22
---

# Test Strategy Checklist

## Phase 1: Test Philosophy & Goals

- [ ] Clarify the goal: maximize value per test, not coverage percentage — coverage is an indicator, not a target [12]
- [ ] Determine which school of testing fits the codebase: Classical (test behavior spanning classes) vs. London (test individual classes via mocks) — default to Classical unless outside-in design discovery is the explicit goal [12][13]
- [ ] Identify the domain complexity profile: rich domain logic (favor unit tests) vs. thin orchestration/CRUD (favor integration tests) [12]
- [ ] Confirm that tests will verify observable behavior, not implementation details — apply the litmus test: "Would the end user or calling code notice if this changed?" [12]
- [ ] Decide whether the project needs a Walking Skeleton — a thin end-to-end slice proving all integration points work before writing feature tests [13]

## Phase 2: Test Architecture & Boundaries

- [ ] Map the codebase onto Khorikov's complexity/collaborator grid to determine what gets unit-tested, integration-tested, or left untested [12]
- [ ] Identify the Humble Object boundary: separate code that is hard to test (infrastructure, UI, frameworks) from code that contains logic (domain model, algorithms) [12]
- [ ] Classify dependencies: managed (own database — use real instances, do NOT mock), unmanaged (third-party APIs, message buses — MOCK these), and private/internal (do NOT mock) [12]
- [ ] Verify that modules are deep enough to warrant boundary testing — shallow modules that just pass calls through may not need their own tests [06]
- [ ] Ensure each layer provides a different abstraction — flag pass-through methods that add interfaces without absorbing complexity [06]
- [ ] Check for information leakage: if the same design decision is encoded in both production code and test code, the test is coupled to implementation [06][12]

## Phase 3: Test Design Patterns

- [ ] Use the AAA pattern (Arrange-Act-Assert) with one Act per test and no conditionals in test code [12]
- [ ] Prefer output-based testing (input/output, no side effects) over state-based, and state-based over communication-based (mocks) [12]
- [ ] Organize tests around behaviors, not around classes — test names should read as behavior specifications [12][13]
- [ ] Use Test Data Builders or Object Mothers for complex setup; keep Act and Assert inline for readability [12]
- [ ] For the GOOS outside-in workflow: write a failing acceptance test (outer loop), then unit tests (inner loop) to build inward until the acceptance test passes [13]
- [ ] Apply "Listen to the Tests": hard-to-write tests signal design problems (too many dependencies, missing abstractions, entangled concerns) — fix the design, not the test [13]
- [ ] Consider property-based testing for behaviors that should hold across all inputs [14]

## Phase 4: Integration & End-to-End Tests

- [ ] Write integration tests for orchestration/controller code that wires domain logic to infrastructure — these should use real managed dependencies (database, file system) [12]
- [ ] Ensure distributed trace context propagates through every service and async boundary so integration tests can verify cross-service behavior [13]
- [ ] For end-to-end tests, use driver objects (page objects) to separate test intent from UI mechanics [13]
- [ ] Verify that each integration test exercises the actual wiring, not mocked wiring — mocking managed dependencies in integration tests defeats their purpose [12]
- [ ] Keep end-to-end tests few but high-value: they validate the Walking Skeleton and critical user paths [13]

## Phase 5: Test Quality & Maintenance

- [ ] Apply the Four Pillars to every test: (1) Protection against regressions, (2) Resistance to refactoring, (3) Fast feedback, (4) Maintainability [12]
- [ ] Prioritize Resistance to Refactoring — it is binary (coupled to implementation or not) and the #1 reason teams lose trust in test suites [12]
- [ ] Never test private methods directly; the desire to do so signals a class with too many responsibilities — extract into its own class [12]
- [ ] Avoid leaking domain knowledge into tests: hard-code expected values rather than recomputing them with the same algorithm [12]
- [ ] Refactoring should not break tests; if tests break during a pure refactoring, either the refactoring changed behavior (real bug) or the test was coupled to implementation (fix the test) [12][16]
- [ ] Apply "Make the change easy, then make the easy change" — refactor test infrastructure when tests become brittle [16]

## Phase 6: AI/Agent-Specific Testing (when applicable)

- [ ] Build evals early: start with 20-50 tasks from actual failures and convert manual checks into automated tests [a11]
- [ ] Design unambiguous tasks where two experts would agree on pass/fail; create reference solutions [a11]
- [ ] Use Pass@k (capability: at least one success in k trials) and Pass^k (reliability: all k succeed) to separate capability from consistency [a11]
- [ ] Favor outcome-based graders over step-sequence checking — verify the end state, not the exact path [a11]
- [ ] For AI-resistant evaluations, prioritize novelty over realism; include multiple independent sub-problems [a13]

---

## Key Questions to Ask

1. "If I refactored the internal structure without changing observable behavior, would this test break?" — the single best diagnostic for test fragility [12]
2. "Is this test verifying what the system does, or how it does it?" — catches implementation-detail coupling [12]
3. "What does this test tell me when it fails?" — a good failure message eliminates the need for a debugger [13]
4. "Does this code have high complexity with many collaborators?" — if yes, refactor to separate concerns before testing [12]
5. "Am I mocking something the outside world can observe, or something internal?" — the mocking decision rule [12]
6. "Could I run this use case from a test harness with no web server, no database, and no UI?" — the architectural testability test [06]
7. "Is this test exercising meaningful logic, or is it testing trivial code?" — do not test getters/setters [12]

---

## Anti-Patterns to Flag

| Anti-Pattern | Signal | Source |
|---|---|---|
| **Testing implementation details** | Mocking internal collaborators, verifying method call sequences, asserting on private state | [12] |
| **Over-mocking** | Every dependency is mocked, test re-implements production code in mock expectations | [12][13] |
| **Mocking managed dependencies** | Own database mocked in integration tests — misses real integration bugs | [12] |
| **Leaking domain knowledge** | Test duplicates production algorithm to compute expected result instead of hard-coding values | [12] |
| **Test-per-class organization** | One test file per production class rather than tests organized by behavior | [12] |
| **Coverage as a goal** | Optimizing for coverage percentage leads to tests that verify trivial code and miss risky logic | [12] |
| **Big-bang test refactoring** | Rewriting all tests at once instead of improving incrementally under existing coverage | [16] |
| **Shallow module testing** | Many tiny test files for wrapper classes that add interfaces without absorbing complexity | [06] |
| **No acceptance tests** | Unit tests pass but the system does not work end-to-end — missing the outer feedback loop | [13] |
| **Ignoring test difficulty** | Hard-to-write test treated as a testing problem rather than a design signal | [13] |
