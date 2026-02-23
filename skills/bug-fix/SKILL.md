---
name: bug-fix
description: >
  Systematic bug diagnosis and fix using Refactoring (Fowler), The Pragmatic Programmer,
  Release It!, DDIA, Philosophy of Software Design, Unit Testing (Khorikov), and Observability Engineering.
  Use when diagnosing bugs, fixing production issues, or hardening systems against failure recurrence.
---

## When to Activate

- User asks to diagnose or fix a bug
- User reports a production incident or unexpected behavior
- User asks for help with a failing test or regression
- User wants to understand why a system is behaving unexpectedly
- User asks about stability patterns, cascading failures, or data consistency issues

## Procedure

1. Read `knowledge/checklists/bug_fix.md`
2. Assess the bug against each relevant checklist phase (diagnosis, refactoring, testing, fix, hardening, verification)
3. For items needing deeper context, read the cited book file (e.g., `book_research/17_release_it.md` for stability patterns)
4. Present findings organized as: **Root Cause Analysis** -> **Fix Strategy** -> **Hardening Recommendations**
5. Cite the source book/principle for each recommendation

## Always-Apply Principles

- Understand why the fix works, not just that it works — never program by coincidence [14: Pragmatic Programmer]
- "Make the change easy, then make the easy change" — refactor to make the bug obvious before fixing it [16: Refactoring]
- Every integration point will eventually fail; design every outbound call with a timeout, circuit breaker consideration, and fallback [17: Release It!]
- Write a failing regression test before applying the fix — the test verifies observable behavior and becomes a permanent guard [12: Unit Testing]
- When tests are hard to write around the bug, the problem is architectural, not testing — fix the design [06: Philosophy of SW Design]

## Deep-Dive References

- Code smells & refactoring catalog: `book_research/16_refactoring_fowler.md`
- Engineering wisdom & debugging heuristics: `book_research/14_pragmatic_programmer.md`
- Stability patterns & failure modes: `book_research/17_release_it.md`
- Data consistency & distributed systems: `book_research/01_designing_data_intensive_applications.md`
- Complexity management & deep modules: `book_research/06_philosophy_of_software_design.md`
- Test quality & regression testing: `book_research/12_unit_testing_khorikov.md`
- Observability & production debugging: `book_research/18_observability_engineering.md`
- Think tool for sequential debugging: `book_research/anthropic_articles/09_think_tool.md`
- Postmortem practices: `book_research/anthropic_articles/15_postmortem.md`
