---
task: ux_review
description: Review UI/UX for usability, cognitive load, and design quality using established psychological principles
primary_sources: ["23", "24", "25"]
secondary_sources: ["26", "29"]
version: 1
updated: 2026-02-22
---

# UX Review Checklist

## Phase 1: Signifiers, Affordances & Discoverability

- [ ] Every interactive element has a clear visual signifier in all states (default, hover, active, disabled, focused) [23]
- [ ] The user can tell what actions are possible and how to perform them without reading instructions [23]
- [ ] Clickable elements look clickable — shape, color, depth, or cursor change distinguish interactive from static content [24]
- [ ] The system follows platform conventions (Jakob's Law): navigation placement, icon meaning, form behavior match what users know from other sites [25]
- [ ] Touch targets are at least 44x44pt (mobile) or 48x48dp (Material Design) per Fitts's Law [25]
- [ ] Primary actions are large and prominent; destructive actions are smaller, spatially separated, and require confirmation [25] [23]
- [ ] Controls are located near the things they affect — natural mapping reduces cognitive load [23]

## Phase 2: Visual Hierarchy & Scanning

- [ ] The page passes the "2-second scan test": a user glancing at it for 2 seconds knows what it is about and where to go [24]
- [ ] Visual hierarchy signals importance: more important = bigger, bolder, higher, more whitespace [24]
- [ ] Related items are grouped by proximity; unrelated items are separated — proximity is the primary grouping mechanism [25]
- [ ] Functionally equivalent elements are styled identically (Law of Similarity); deviations signal functional differences [25]
- [ ] The most important action per view is the single most visually distinct element (Von Restorff Effect) [25]
- [ ] Navigation items at the first and last positions are the most important (Serial Position Effect) [25]
- [ ] Happy talk, marketing filler, and unnecessary instructions are eliminated — get rid of half the words, then half again [24]
- [ ] Content uses chunking: groups of 5-9 related items to respect working memory limits (Miller's Law) [25]

## Phase 3: Navigation & Wayfinding

- [ ] Apply the Trunk Test to every page — can the user answer: (1) What site? (2) What page? (3) Major sections? (4) Options at this level? (5) Where am I? [24]
- [ ] Persistent navigation appears on every page: site ID, primary nav, search, utilities [24]
- [ ] Current section/page is clearly highlighted in navigation ("you are here" indicator) [24]
- [ ] Breadcrumbs show hierarchical position — always present, always small, current page bolded and not a link [24]
- [ ] Navigation labels use the user's language, not internal jargon or database schema names [24] [23]
- [ ] Decision points are limited: minimize choices at each navigation level (Hick's Law) and use progressive disclosure [25]
- [ ] Multi-step processes show progress via connected step indicators (Law of Uniform Connectedness) [25]

## Phase 4: Feedback, State & Performance

- [ ] Every user action produces immediate, informative feedback — confirm what happened, show the new state [23]
- [ ] System responses feel instantaneous: <100ms for direct manipulation, <400ms for operations (Doherty Threshold) [25]
- [ ] If an operation takes >400ms, provide immediate visual feedback: skeleton screens, progress bars, or optimistic UI [25]
- [ ] Error messages identify what went wrong, explain why, and suggest what to do next — never just "Something went wrong" [23]
- [ ] The system state is always visible: loading, empty, error, success, and partial states are all designed [23]
- [ ] Endings are designed well — confirmation pages, success states, and completion screens receive premium attention (Peak-End Rule) [25]

## Phase 5: Error Prevention & Recovery

- [ ] Classify errors as slips (wrong action, right goal) vs. mistakes (wrong goal) — use different prevention strategies [23]
- [ ] Slip prevention: undo for accidental actions, spatial separation of destructive and routine buttons, constraints that prevent wrong actions [23]
- [ ] Mistake prevention: clear system state visibility, good conceptual models, preview/dry-run for complex operations [23]
- [ ] Input validation follows Postel's Law: accept varied formats (phone numbers with/without dashes), normalize internally [25]
- [ ] Confirmation dialogs are reserved for truly irreversible actions only — overuse causes habituation [23]
- [ ] Every error state has a clear recovery path — the user should never be stuck [23]
- [ ] Forms use real-time, gentle inline validation rather than post-submission rejection [25]

## Phase 6: Product & Data Presentation

- [ ] Every chart or data display has an "action title" that states the takeaway, not just a topic label [26]
- [ ] Visual displays use the gray + accent color pattern: push everything to gray, highlight the key insight in one color [26]
- [ ] Charts are decluttered: no unnecessary gridlines, borders, legends (use direct labeling), or data markers [26]
- [ ] Features are framed as solutions to validated customer problems, not as technical capabilities (value risk first) [29]
- [ ] The design addresses the four product risks: value (will they use it?), usability (can they use it?), feasibility, and viability [29]
- [ ] Data visualizations respect accessibility: avoid red-green as sole differentiator, ensure sufficient contrast [26]

## Key Questions to Ask

1. "Will the user have to think about what to do here?" — the Don't Make Me Think test for every element [24]
2. "What mental model will the user form from looking at this?" — if it leads to wrong conclusions, the design is broken [23]
3. "Can the user figure out what happened after they clicked?" — Gulf of Evaluation diagnosis [23]
4. "Who bears the complexity — the user or the system?" — complexity can only be moved, not eliminated (Tesler's Law) [25]
5. "Does this follow the convention, or is the deviation clearly better?" — innovate on value, not interaction patterns [25]
6. "What drains the most goodwill?" — prioritize fixing the highest-friction moments [24]
7. "What is the 'so what' of this data display?" — if you cannot articulate it, the chart does not belong [26]

## Anti-Patterns

| Anti-Pattern | Why It Fails | Source |
|---|---|---|
| Flat design that removes all signifiers | Users cannot tell what is interactive — affordances exist but are invisible | [23] |
| Reinventing standard navigation patterns | Users spend most time on other sites; broken conventions create friction (Jakob's Law) | [25] |
| "Something went wrong — try again" errors | No diagnosis, no explanation, no recovery path — violates all three evaluation stages | [23] |
| Confirmation dialogs on every action | Users habituate to clicking "OK" reflexively, defeating the purpose for truly destructive actions | [23] |
| Pie charts for data comparison | Humans are bad at judging angles and areas — horizontal bar charts communicate the same data more accurately | [26] |
| Feature factory: shipping features without validating value | "At least half of our ideas are just not going to work" — discovery before delivery [29] |
| Center-aligned body text and floating elements | Harms scanning and creates visual noise; left-align text, align elements to clean visual lines | [26] |
| More than 7 ungrouped options at a decision point | Exceeds working memory; chunk into categories or use progressive disclosure (Hick's + Miller's) | [25] |
