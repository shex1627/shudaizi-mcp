---
name: refactoring
description: >
  Systematic code refactoring using Refactoring (Fowler), A Philosophy of Software Design (Ousterhout),
  Clean Code (Martin), Clean Architecture, Unit Testing (Khorikov), and The Pragmatic Programmer.
  Use when planning refactoring, reviewing code for smells, or executing safe code transformations.
---

## When to Activate

- User asks to refactor code or improve code structure
- User asks about code smells or technical debt assessment
- User asks for help making code more maintainable or understandable
- User is preparing code for a new feature (preparatory refactoring)
- User wants to reduce complexity in an existing codebase

## Procedure

1. Read `knowledge/checklists/refactoring.md`
2. Identify the code smells present using the smell catalog from Phase 3
3. For items needing deeper context, read the cited book file (e.g., `book_research/16_refactoring_fowler.md`)
4. Present findings organized as: **Smells Identified** -> **Recommended Refactorings** -> **Execution Plan** -> **Verification Steps**
5. Cite the source book/principle for each recommendation
6. Ensure tests exist before recommending any transformation

## Always-Apply Principles

- Refactoring without tests is gambling, not engineering — verify the safety net first [16: Refactoring]
- Small steps, always runnable — code must compile and pass tests after every single transformation [16: Refactoring]
- "Make the change easy, then make the easy change" — preparatory refactoring before feature work [16: Refactoring]
- The best modules are those whose interfaces are much simpler than their implementations [06: Philosophy of SW Design]
- Stop decomposing when the decomposition itself becomes the complexity [06: Philosophy of SW Design]
- Tests should verify observable behavior, not implementation details — good tests survive refactoring [12: Unit Testing]
- DRY is about knowledge duplication, not code duplication — premature abstraction is worse than duplication [14: Pragmatic Programmer]
- Dependencies should point inward toward higher-level policies [04: Clean Architecture]
- Leave the code better than you found it, a little at a time [15: Clean Code][14: Pragmatic Programmer]

## Deep-Dive References

- Refactoring catalog & code smells: `book_research/16_refactoring_fowler.md`
- Complexity management & deep modules: `book_research/06_philosophy_of_software_design.md`
- Code readability & naming: `book_research/15_clean_code.md`
- Dependency direction & boundaries: `book_research/04_clean_architecture.md`
- Test quality & resistance to refactoring: `book_research/12_unit_testing_khorikov.md`
- DRY, orthogonality & pragmatic principles: `book_research/14_pragmatic_programmer.md`
