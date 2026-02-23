---
name: test-strategy
description: >
  Systematic test strategy design and review using Unit Testing (Khorikov), GOOS (Freeman & Pryce),
  Philosophy of Software Design, The Pragmatic Programmer, and Refactoring.
  Use when designing a test approach, evaluating test quality, or deciding what/how to test.
---

## When to Activate

- User asks to design or review a test strategy for a project or feature
- User asks what to test, how to test, or whether tests are good quality
- User is deciding between unit tests, integration tests, or end-to-end tests
- User wants to evaluate or improve an existing test suite
- User asks about mocking decisions or test architecture
- User is building evals for an AI agent or LLM-powered system

## Procedure

1. Read `knowledge/checklists/test_strategy.md`
2. Assess the codebase or feature against each relevant checklist phase
3. For items needing deeper context, read the cited book file (e.g., `book_research/12_unit_testing_khorikov.md`)
4. Present findings organized as: **Current State** -> **Gaps** -> **Recommended Strategy**
5. Cite the source book/principle for each recommendation

## Always-Apply Principles

- Test observable behavior, not implementation details — "Would the end user notice if this changed?" [12: Unit Testing]
- Resistance to refactoring is the most important test quality pillar — it is binary and the #1 cause of lost trust in test suites [12: Unit Testing]
- Mock only unmanaged out-of-process dependencies (third-party APIs, message buses); use real instances for your own database [12: Unit Testing]
- When tests are hard to write, the design is telling you something — fix the design, not the test [13: GOOS]
- Organize tests around behaviors, not classes; test names should be specifications [12: Unit Testing]
- Code that is hard to test should be made humble (trivially simple); code that contains logic should be free of infrastructure dependencies [12: Unit Testing]

## Deep-Dive References

- Test quality framework & mocking rules: `book_research/12_unit_testing_khorikov.md`
- Outside-in TDD & walking skeleton: `book_research/13_growing_oo_software_guided_by_tests.md`
- Deep modules & complexity management: `book_research/06_philosophy_of_software_design.md`
- Property-based testing & tracer bullets: `book_research/14_pragmatic_programmer.md`
- Refactoring under tests & code smells: `book_research/16_refactoring_fowler.md`
- Agent evals & grader design: `book_research/anthropic_articles/11_demystifying_evals.md`
- AI-resistant evaluation design: `book_research/anthropic_articles/13_ai_resistant_evaluations.md`
