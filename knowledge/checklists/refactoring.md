---
task: refactoring
description: Plan and execute code refactoring safely
primary_sources: ["16", "06", "15"]
secondary_sources: ["04", "12", "14"]
version: 1
updated: 2026-02-22
---

# Refactoring Checklist

## Phase 1: Pre-Refactoring Assessment

- [ ] Verify a solid test suite exists before starting — refactoring without tests is not refactoring, it is gambling [16]
- [ ] If tests are absent, write characterization tests first to capture current behavior before changing anything [16]
- [ ] Identify the code smells driving the refactoring: Long Function, Feature Envy, Duplicated Code, Shotgun Surgery, or another named smell [16]
- [ ] Confirm you are wearing the refactoring hat, not the adding-functionality hat — never both simultaneously [16]
- [ ] Assess complexity: does the code exhibit change amplification, cognitive load, or unknown unknowns? [06]
- [ ] Check for information leakage — is the same design decision (data format, protocol, algorithm) reflected in multiple modules? [06]
- [ ] Evaluate whether this is a refactoring opportunity or a rewrite situation — if incremental steps are impossible, the threshold for rewriting has been crossed [16]

## Phase 2: Design Direction

- [ ] Determine the target shape: are you making modules deeper (simple interface, rich functionality) or splitting shallow modules? [06]
- [ ] Check if the refactoring will increase or decrease the module depth — avoid decomposing past the point where decomposition itself becomes the complexity [06]
- [ ] Verify each layer provides a fundamentally different abstraction than adjacent layers — flag pass-through methods and pass-through variables [06]
- [ ] Ensure interfaces are "somewhat general-purpose": specific enough for current needs, stable enough for future extension without interface changes [06]
- [ ] Check that dependencies point inward toward higher-level policies — source-code dependencies must not point from domain logic to infrastructure [04]
- [ ] Consider whether the refactoring should pull complexity downward into implementations, away from callers [06]
- [ ] Apply the DRY principle correctly: eliminate duplicated knowledge, not just duplicated code — premature abstraction of coincidentally similar code creates worse coupling [14]

## Phase 3: Smell Identification & Refactoring Selection

- [ ] For Long Function: apply Extract Function, Replace Temp with Query, Decompose Conditional, or Replace Conditional with Polymorphism [16]
- [ ] For Feature Envy: apply Move Function to the module whose data the function uses most [16]
- [ ] For Duplicated Code: apply Extract Function, Pull Up Method, or Slide Statements to unify [16]
- [ ] For Long Parameter List: apply Introduce Parameter Object, Preserve Whole Object, or Replace Parameter with Query [16]
- [ ] For Shotgun Surgery: apply Move Function, Move Field, or Combine Functions into Class to consolidate [16]
- [ ] For Divergent Change: apply Split Phase or Extract Class to separate unrelated reasons to change [16]
- [ ] For Primitive Obsession: apply Replace Primitive with Object or Replace Type Code with Subclasses [16]
- [ ] For Message Chains: apply Hide Delegate or Extract Function to break the chain [16]
- [ ] For Data Clumps: apply Extract Class or Introduce Parameter Object — groups of data traveling together signal a missing abstraction [16]
- [ ] For Repeated Switches: apply Replace Conditional with Polymorphism [16]
- [ ] Consider whether errors can be designed out of existence by broadening the method specification [06]

## Phase 4: Safe Execution

- [ ] Take small steps — each refactoring should be completable in minutes, not hours [16]
- [ ] Keep the code compiling and tests passing after every single step [16]
- [ ] Commit frequently — each commit should represent one named refactoring [16]
- [ ] Avoid long-lived feature branches — refactoring produces many small commits that touch many files; long branches cause merge conflicts [16]
- [ ] If tests break, you know exactly which small step caused the problem — revert and try again [16]
- [ ] Do not change behavior while refactoring — if you discover a bug, note it and fix it separately [16]
- [ ] Resist refactoring-driven scope creep — note other improvements but stay focused on the current transformation [16]

## Phase 5: Verification & Quality Gates

- [ ] Run the full test suite after completing the refactoring sequence [16][12]
- [ ] Verify tests are testing observable behavior, not implementation details — refactoring should not break well-written tests [12]
- [ ] If tests broke during a behavior-preserving refactoring, the tests were coupled to implementation details — fix the tests [12]
- [ ] Check that the refactored code passes the deep module test: is the interface simpler than the implementation it hides? [06]
- [ ] Verify naming clarity: can you tell what each function and variable does from its name alone? Rename if not [16][15]
- [ ] Confirm the code reads like well-written prose — the ratio of reading to writing code is over 10:1 [15]
- [ ] Apply the Boy Scout Rule: leave the code better than you found it [15][14]

## Phase 6: Post-Refactoring Assessment

- [ ] Verify the Design Stamina Hypothesis: has the refactoring made future changes easier, not just different? [16]
- [ ] Check for new shallow modules introduced — did extraction create interfaces without absorbing complexity? [06]
- [ ] Confirm no information leakage was introduced — the same design decision should not now appear in more places than before [06]
- [ ] Assess whether 10-20% of development time is being invested in design quality (strategic programming), not just shipping features (tactical programming) [06]
- [ ] Document non-obvious design decisions if the refactoring changed the module structure — comments should explain why, not what [06][15]

---

## Key Questions to Ask

1. "What is the smell, and what is the named refactoring that addresses it?" — Use the catalog as shared vocabulary, not ad-hoc restructuring [16]
2. "Is this interface simpler than the implementation it hides?" — The deep module test for every new abstraction [06]
3. "If I refactored the internal structure without changing observable behavior, would the tests break?" — If yes, the tests are fragile and need fixing [12]
4. "Am I decomposing for clarity or decomposing out of habit?" — Stop before the decomposition itself becomes the complexity [06]
5. "Make the change easy, then make the easy change." — Preparatory refactoring before implementing a feature [16]
6. "Would a new team member understand this code without explanation?" — The readability litmus test [15][16]
7. "Is this duplication representing the same knowledge, or coincidentally similar code?" — DRY applies to knowledge, not syntax [14]
8. "Do I have tests? If not, that is the first refactoring." — The prerequisite that gates everything else [16][12]

---

## Anti-Patterns to Flag

| Anti-Pattern | Signal | Source |
|---|---|---|
| **Refactoring without tests** | No test suite or tests disabled — changes are unverified gambles | [16][12] |
| **Big-bang refactoring** | "Refactoring" for days or weeks without shipping — this is restructuring, not refactoring | [16] |
| **Shallow module proliferation** | Many tiny classes/functions that each add an interface without absorbing complexity | [06] |
| **Premature abstraction** | DRY applied to coincidentally similar code, creating coupling worse than the duplication | [14][06] |
| **Refactoring sprint** | Scheduling refactoring as a phase — a sign that opportunistic refactoring has been neglected | [16] |
| **Speculative generality** | Abstractions built for imagined future needs that may never materialize — delete them | [16] |
| **Pass-through methods** | Methods that do nothing except invoke another method with a similar signature | [06] |
| **Temporal decomposition** | Code organized by execution order (read, parse, process) instead of by information to be hidden | [06] |
| **Extract-till-you-drop** | Mechanically applying "functions should be 4-6 lines" without evaluating if abstraction depth increased | [06][15] |
| **Comment phobia** | Deleting valuable "why" comments in pursuit of "self-documenting code" — code cannot express design rationale | [06][15] |
| **Mixed hats** | Adding features and refactoring simultaneously — losing the safety of behavior-preserving transformations | [16] |
| **Ignoring the economics** | Refactoring code that works and will never be touched again — refactoring is an investment in future change velocity | [16][14] |
