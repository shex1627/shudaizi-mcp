---
name: ux-review
description: >
  UX review using Design of Everyday Things, Don't Make Me Think, and Laws of UX.
  Use when reviewing UI designs, auditing usability, designing user flows, or evaluating data presentations.
---

## When to Activate

- User asks for a UX review, usability audit, or design feedback
- User is building or modifying UI components, forms, navigation, or user flows
- User asks about visual hierarchy, layout, or interaction patterns
- User is designing error messages, empty states, or loading states
- User is creating charts, dashboards, or data presentations
- User asks about accessibility or cognitive load concerns

## Procedure

1. Read `knowledge/checklists/ux_review.md`
2. Assess the interface against relevant checklist phases:
   - For component-level review: Phase 1 (signifiers) + Phase 4 (feedback)
   - For page/flow review: Phase 2 (hierarchy) + Phase 3 (navigation) + Phase 5 (errors)
   - For data displays: Phase 6 (data presentation)
3. For items needing deeper context, read the cited book file
4. Apply the Trunk Test to any navigation review and the "Don't Make Me Think" test to every interactive element
5. Present findings organized by impact: **Blocks users** -> **Causes confusion** -> **Reduces polish**
6. For each finding: describe the issue, cite the psychological principle, suggest a concrete fix

## Always-Apply Principles

- "Don't make me think" — every element should be self-evident; every question mark in the user's head is a usability failure [24: Don't Make Me Think]
- Users scan, satisfice, and muddle through — design for the first glance, not the careful read [24]
- Signifiers communicate what actions are possible; affordances alone are invisible without them [23: Design of Everyday Things]
- Slips and mistakes require different prevention strategies — undo for slips, better conceptual models for mistakes [23]
- Follow conventions by default; innovate only on value, not on interaction patterns (Jakob's Law) [25: Laws of UX]
- Complexity can only be moved, not eliminated — ensure the system bears it, not the user (Tesler's Law) [25]

## Deep-Dive References

- Affordances, signifiers, conceptual models & error taxonomy: `book_research/23_design_of_everyday_things.md`
- Visual hierarchy, scanning, navigation & usability testing: `book_research/24_dont_make_me_think.md`
- Cognitive psychology laws for UI (Fitts, Hick, Miller, Gestalt, etc.): `book_research/25_laws_of_ux.md`
- Data visualization principles & chart selection: `book_research/26_storytelling_with_data.md`
- Product discovery & feature validation: `book_research/29_inspired_cagan.md`
