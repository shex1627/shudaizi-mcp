---
name: code-review
description: >
  Code review using Philosophy of Software Design, Clean Code, Refactoring, Pragmatic Programmer,
  Unit Testing, and more. Use when reviewing code for quality, readability, maintainability, and correctness.
---

## When to Activate

- User asks for a code review
- User asks about code quality, readability, or maintainability
- User wants feedback on a PR or code change
- User asks about refactoring opportunities

## Procedure

1. Read `knowledge/checklists/code_review.md`
2. Assess the code against relevant checklist phases
3. For items needing deeper context, read the cited book file
4. Present findings as: **What's Good** → **Concerns** → **Suggested Changes**
5. Cite the source principle for each finding
6. Prioritize: correctness > readability > performance > style

## Always-Apply Principles

- Modules should be deep: simple interfaces hiding complex implementations [06: Philosophy of SW Design]
- Code should read like well-written prose — names reveal intent [15: Clean Code]
- DRY is about knowledge, not text — duplication of logic, not of code [14: Pragmatic Programmer]
- If you see a code smell, name the specific refactoring that addresses it [16: Refactoring]
- Test observable behavior, not implementation details [12: Unit Testing]
- Orthogonality: changes should be localized, not ripple across modules [14: Pragmatic Programmer]

## Deep-Dive References

- Module depth & complexity: `book_research/06_philosophy_of_software_design.md`
- DRY, orthogonality, tracer bullets: `book_research/14_pragmatic_programmer.md`
- Naming, functions, formatting: `book_research/15_clean_code.md`
- Smells & refactorings catalog: `book_research/16_refactoring_fowler.md`
- Dependency rules: `book_research/04_clean_architecture.md`
- Test quality framework: `book_research/12_unit_testing_khorikov.md`
- TDD & outside-in design: `book_research/13_growing_oo_software_guided_by_tests.md`
- Async patterns: `book_research/22_python_concurrency_asyncio.md`
