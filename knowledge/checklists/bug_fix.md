---
task: bug_fix
description: Systematic approach to diagnosing, fixing, and hardening code against bugs
primary_sources: ["16", "14", "17"]
secondary_sources: ["01", "06", "12", "18"]
anthropic_articles: ["a09", "a15"]
version: 1
updated: 2026-02-22
---

# Bug Fix Checklist

## Phase 1: Diagnosis & Understanding

- [ ] Reproduce the bug reliably before attempting any fix — if you cannot reproduce it, you cannot verify the fix [14]
- [ ] Resist guessing: use binary search debugging to systematically bisect the problem space [14]
- [ ] Rubber duck the problem: articulate what should happen vs. what actually happens — the act of explaining often reveals the gap [14]
- [ ] Check whether this is a slip (correct intent, wrong action) or a mistake (wrong mental model of the system) — each requires a different investigation approach [a09]
- [ ] Examine the failure through the observability lens: slice by dimensions (user, endpoint, region, build, feature flag) to isolate the affected cohort [18]
- [ ] Use structured events and trace context to identify the causal chain across service boundaries [18]
- [ ] Ask: "Is this a cascading failure?" — check whether a slow or failing downstream dependency is exhausting resources upstream (blocked threads, full connection pools) [17]
- [ ] For data consistency bugs: identify which anomaly is being observed (stale read, phantom, write conflict) and which isolation level or replication lag could cause it [01]

## Phase 2: Preparatory Refactoring

- [ ] Before fixing the bug, refactor the surrounding code to make the bug obvious — "Make the change easy, then make the easy change" [16]
- [ ] Use Extract Function to isolate the buggy logic into a named, testable unit [16]
- [ ] Use Rename Variable to clarify what values represent — mysterious names hide bugs [16]
- [ ] Use Decompose Conditional to make branching logic clear and each branch independently verifiable [16]
- [ ] If the bug is in a deep, complex method, apply "pull complexity downward" — simplify the interface so the fix does not leak complexity to callers [06]
- [ ] Flag code smells near the bug: Feature Envy, Long Parameter List, Shotgun Surgery, Duplicated Code — these often indicate the root cause is a missing abstraction [16]

## Phase 3: Write a Failing Test First

- [ ] Write a failing test that demonstrates the bug through observable behavior, not by poking at internals [12]
- [ ] The test should verify the correct behavior from the user/caller perspective — it becomes a permanent regression guard [12]
- [ ] If the bug crosses service boundaries, write an integration test using real managed dependencies (not mocks) [12]
- [ ] Ensure the test fails for the right reason: the assertion should fail on the buggy behavior, not on setup or unrelated issues [12]
- [ ] If writing the test is hard, that signals a design problem — use "Listen to the Tests" to identify missing abstractions before proceeding [13]

## Phase 4: Apply the Fix

- [ ] Understand why the fix works, not just that it works — do not program by coincidence [14]
- [ ] Wear only the "refactoring hat" or the "fix hat" at one time — do not refactor and change behavior simultaneously [16]
- [ ] Keep the fix as small as possible: each change should be independently testable and the code should pass tests after every step [16]
- [ ] If the bug involves an integration point, verify: Is there a timeout? A circuit breaker? A fallback? Missing any of these is the root cause of most production instability [17]
- [ ] For bugs caused by slow responses or hung connections: add explicit connection and read timeouts, use bounded resource pools (bulkheads) [17]
- [ ] For retry-related bugs: ensure retries use exponential backoff with jitter, a maximum retry count, and only retry on retriable errors [17]
- [ ] For data consistency bugs: verify the transaction isolation level matches the actual requirement — many databases default to weaker isolation than developers assume [01]

## Phase 5: Harden Against Recurrence

- [ ] Add assertions that encode your understanding of the fix — when they fire in the future, you learn something valuable [14]
- [ ] Apply "Design errors out of existence" where possible: broaden the interface specification so the formerly-erroneous condition is now valid behavior [06]
- [ ] Check for the same bug pattern elsewhere in the codebase (Shotgun Surgery smell) — if the same logic is duplicated, fix all occurrences or extract a shared abstraction [16]
- [ ] Add structured telemetry around the fix: attach relevant context (user ID, request ID, feature flags) to events so the fix can be verified in production [18]
- [ ] Verify the system reaches steady state without human intervention: log rotation, cache eviction, data cleanup are all automated [17]
- [ ] Consider whether the fix needs a circuit breaker or back-pressure mechanism to prevent the failure from cascading if it recurs [17]

## Phase 6: Verify & Deploy

- [ ] Run the full test suite — the failing test now passes, and no existing tests break [16]
- [ ] If refactoring was part of the fix, verify each refactoring step preserved behavior independently [16]
- [ ] Deploy and observe: actively monitor production telemetry for the first few minutes — look for changes in latency distributions, error rates, and SLO burn rates [18]
- [ ] For production incidents, use the think-tool pattern: pause between investigation steps to analyze tool outputs before proceeding [a09]
- [ ] Document what happened and why in a blameless postmortem grounded in data, not narratives [a15]

---

## Key Questions to Ask

1. "Can I reproduce this bug with a test?" — if not, the diagnosis is incomplete [14]
2. "Why does the fix work?" — not just "does it work?" — understanding prevents coincidence-based fixes [14]
3. "What happens when this dependency is slow? Down? Returns garbage?" — force failure mode analysis [17]
4. "Is this a data consistency bug caused by replication lag or weak isolation?" — check the actual guarantees of your data layer [01]
5. "Is the same bug pattern hiding elsewhere in the codebase?" — Shotgun Surgery means one fix is not enough [16]
6. "What assertion can I add that would catch this class of bug in the future?" — defense in depth [14]
7. "Could this failure cascade to other services?" — check for missing timeouts, unbounded pools, and missing circuit breakers [17]
8. "What telemetry would have made this bug obvious immediately?" — add it now [18]

---

## Anti-Patterns to Flag

| Anti-Pattern | Signal | Source |
|---|---|---|
| **Programming by coincidence** | Fix works but developer cannot explain why — relying on undocumented behavior or lucky test outcomes | [14] |
| **Fix without a test** | Bug fixed but no regression test written — the same bug will return | [12][16] |
| **Big-bang fix** | Refactoring + behavior change + fix all in one commit — impossible to diagnose if something breaks | [16] |
| **Missing timeouts** | Outbound calls without explicit connection and read timeouts — the #1 stability anti-pattern | [17] |
| **Naive retries** | Immediate, unlimited retries without backoff or jitter — turns a transient failure into a thundering herd | [17] |
| **Unbounded result sets** | Query that returns "all records" — works in dev (50 rows), crashes in prod (5M rows) | [17] |
| **Blame the user** | Error message says "invalid input" without explaining what is valid or how to recover | [14] |
| **Fix the symptom, not the cause** | Wrapping the buggy code in a try/catch instead of understanding and addressing the root cause | [14][17] |
| **Unstructured logging** | Adding `print` or `log.info()` strings instead of structured events with rich context | [18] |
| **Hope-based deployment** | Deploying the fix without actively observing production telemetry afterward | [18] |
| **Cascading failure blindness** | Fixing one service without checking whether the failure propagated to callers | [17] |
| **Shallow fix on a deep problem** | Patching the surface without addressing the missing abstraction or information leakage underneath | [06][16] |
