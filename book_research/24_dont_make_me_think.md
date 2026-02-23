# Don't Make Me Think (3rd ed.) — Steve Krug (2014)

**Skill Category:** UX & Web Usability
**Relevance to AI-assisted / vibe-coding workflows:** The most practical and immediately applicable UX book — its principles directly translate into UI code review criteria and feature design guidance. When an AI agent is generating UI code, Krug's heuristics serve as a checklist: Is this self-evident? Will a user have to think about what to click? Is there a clear visual hierarchy? The book's emphasis on cheap, fast usability testing ("hallway testing") maps perfectly to rapid iteration cycles in vibe-coding, where you ship fast but still need reality checks.

---

## What This Book Is About

*Don't Make Me Think* is a concise, opinionated guide to web and mobile usability. First published in 2000, this third edition (subtitled "A Common Sense Approach to Web and Mobile Usability," published by New Riders/Pearson in 2014) updates Krug's original work with mobile considerations while preserving the core insight that has made the book a design classic: **every page, every screen, every interaction should be self-evident — the user should never have to expend cognitive effort figuring out what things are or how to use them.**

The book is organized in three broad arcs:

1. **Guiding Principles (Chapters 1-5):** The "don't make me think" rule, how people actually use the web (scanning, satisficing, muddling through), designing for scanning with visual hierarchy and conventions, why users don't read (and what to do about it), and navigation design.

2. **Making Sure You Get It Right (Chapters 6-9):** The critical importance of usability testing (especially low-cost "hallway" testing), how to run a usability test on a budget, the home page dilemma, and the "trunk test" for evaluating navigation.

3. **Larger Concerns and Mobile (Chapters 10-13):** Usability as common courtesy, accessibility, mobile usability, and making the case for usability within organizations.

Krug's distinctive voice is conversational, funny, and relentlessly practical. The book is intentionally short (under 200 pages with large illustrations) because Krug practices what he preaches: he removes every unnecessary word so the reader doesn't have to think about what's important.

---

## Key Ideas & Mental Models

### 1. The First Law of Usability: Don't Make Me Think

Krug's foundational principle. A web page or screen should be **self-evident** — the user should be able to "get it" without expending any cognitive effort. When that's not possible, it should at least be **self-explanatory** — with minimal effort, the user can figure it out. Every question mark that pops up in a user's head (What do I click? Is that a button? Where am I? What's this label mean?) adds to their cognitive load and increases the probability they'll give up, make errors, or lose trust. The goal is zero question marks.

Concrete applications: Button labels should be unambiguous verbs ("Buy Now" not "Submit"). Links should clearly indicate where they go. Form fields should be self-labeling. If something is clickable, it must look clickable. Names, categories, and navigation labels should use the user's language, not internal jargon.

### 2. How People Actually Use the Web: Scanning, Satisficing, Muddling Through

Krug identifies three "facts of life" about web usage that most designers ignore:

- **People don't read, they scan.** Users glance at each page, scan some of the text, and click on the first link that catches their interest or vaguely resembles what they're looking for. They do not read word-by-word in a linear fashion.
- **People don't make optimal choices, they satisfice.** Users don't choose the best option — they choose the first reasonable option. Herbert Simon's concept of "satisficing" (satisfying + sufficing) describes how users pick "good enough" rather than scanning all options to find the best one. They're in a hurry, the penalty for a wrong click is low (they can hit Back), and weighing all options doesn't improve outcomes enough to justify the effort.
- **People don't figure out how things work, they muddle through.** Users don't read instructions or try to understand the underlying conceptual model. They find something that sort of works and keep using it, even if it's not the intended or optimal way. If it works, they don't care whether they understand it.

The design implication: stop designing for the "rational user" who reads everything and makes deliberate choices. Design for scanners who satisfice.

### 3. Visual Hierarchy and Designing for Scanning

Since users scan, pages must be designed to support scanning. Krug's guidance for making pages scan-friendly:

- **Create a clear visual hierarchy.** The relative importance of elements should be visually obvious. More important = more prominent (bigger, bolder, higher on the page, more whitespace). Related items should be visually grouped. Items that are logically nested should be visually nested.
- **Use conventions.** Don't reinvent patterns that users already know. Logos in the top left. Navigation at the top or left. Underlined blue text is a link. Shopping cart icon means shopping cart. Conventions are your friend because they reduce cognitive load to zero for familiar patterns.
- **Break up pages into clearly defined areas.** Users should be able to quickly identify which areas of the page contain what type of content, then ignore the areas that are irrelevant to their current goal.
- **Make it obvious what's clickable.** The user should never have to guess whether something is a link, a button, or just text. Shape, color, location, and formatting should make clickability unambiguous.
- **Minimize noise (visual and informational).** Busy pages are hard to scan. Every element on the page is competing for attention. Reduce clutter by removing anything that doesn't directly serve the user's task. When in doubt, take it out.

### 4. Omit Needless Words

Krug borrows Strunk and White's dictum and makes it a usability law: get rid of half the words on each page, then get rid of half of what's left. This applies to:

- **Happy talk** — the self-congratulatory introductory text that no one reads ("Welcome to our award-winning platform for collaborative solutions..."). Remove all of it.
- **Instructions** — if the design needs instructions, the design is wrong. If instructions are truly unavoidable, make them as brief as possible. No one reads them anyway.
- **Filler words** — every extra word makes the remaining words harder to find. Tightening prose isn't just about brevity; it's about making the important content more visible to scanners.

### 5. Navigation Design and the "Trunk Test"

Navigation is Krug's most detailed design topic. Navigation serves multiple simultaneous purposes: it tells users what the site contains, it tells them how the site is organized, it tells them where they are, and it tells them how to use the site. Good navigation gives users a sense of place in a virtual space.

**Persistent navigation** should appear on every page and include: Site ID (logo), primary navigation (sections), a search box, and utilities (account, help, cart). The only exception is forms and checkout flows, where persistent navigation can be reduced to avoid distraction.

**Breadcrumbs** show the user's path through the hierarchy. They're secondary navigation, not primary, and should be visually small but present.

**The Trunk Test:** Krug's diagnostic for navigation quality. The idea: imagine being blindfolded and dropped at a random page deep in a site (like being dropped in the middle of a dense forest and trying to find a trail marker — you're at the "trunk" of a random tree). You should be able to answer these five questions without hesitation:

1. What site is this? (Site ID)
2. What page am I on? (Page name)
3. What are the major sections of this site? (Sections/primary nav)
4. What are my options at this level? (Local navigation)
5. Where am I in the scheme of things? ("You are here" indicators)

If a user landing on any random page can't answer all five, the navigation has failed. This is an excellent heuristic for AI-assisted code review of any generated UI.

### 6. The Home Page Problem

The home page has to accomplish too many things at once: communicate the site identity and mission, provide navigation to content, show what's new, provide teasers for deeper content, offer search, promote key items, and handle cross-selling. Because every stakeholder wants presence on the home page, it tends toward bloat.

Krug's key insight about the home page is the **tagline test**: can a new visitor, looking at the home page for the first time, answer "What is this site, and what can I do here?" within a few seconds? A good tagline is six to eight words, conveys the value proposition, and is positioned near the site ID. The most common home page failure is assuming the user already knows what the site is.

### 7. Usability Testing: Do It Yourself, Do It Cheap, Do It Often

This is arguably Krug's most impactful contribution to the field. He makes the case that usability testing doesn't require labs, professional moderators, or large sample sizes:

- **Test with 3-4 users per round.** You find the majority of serious problems with just a few people. Testing with 3 users and iterating is far more valuable than testing with 15 users once.
- **Test early and continuously.** Test paper prototypes, wireframes, or partially built pages. Don't wait until the design is "done."
- **Recruit loosely.** You don't need exact demographic matches for your target audience. Most usability problems are problems for everyone. "Hallway testing" — grabbing the next person who walks by — is infinitely better than no testing.
- **Use the "think aloud" protocol.** Ask users to narrate their thoughts as they attempt tasks. What they say reveals confusion that their behavior alone might not.
- **Focus on finding the most serious problems and fixing them.** Don't try to find every issue. Find the three biggest problems, fix them, test again.

**Hallway usability testing** is Krug's term for extremely lightweight testing: literally grab someone in the hallway, show them the page for a minute, and ask them a few questions. The insight is that the bar for "useful testing" is much lower than people assume. Any testing with any user is better than no testing. The search for methodological perfection is the enemy of actually learning something.

### 8. Usability as Common Courtesy: The Reservoir of Goodwill

Users arrive with a reservoir of goodwill toward your site or app. Every frustration, confusion, or annoyance drains that reservoir. Every moment of clarity, helpfulness, or delight refills it. When the reservoir runs dry, users leave and may not come back.

Things that drain goodwill: hiding information users need (like phone numbers, shipping costs), requiring personal information unnecessarily, making things look like ads (banner blindness), inconsistent UI patterns, and amateur visual design.

Things that replenish goodwill: proactively helping users recover from errors, reducing the number of steps in common tasks, providing clear error messages, answering FAQ-type questions before users have to ask, and admitting errors honestly.

### 9. Accessibility Is a Continuum, Not a Checklist

Krug advocates for accessibility as an extension of good usability. His practical approach: start by making the site work well for everyone, then layer on specific accessibility improvements. The most impactful accessibility improvement is also the cheapest — adding proper headings to create a document outline that screen readers can navigate. He acknowledges the tension between comprehensive WCAG compliance and practical constraints, and argues that doing something is always better than doing nothing because "perfect" feels too hard.

### 10. Mobile Usability: It's Still "Don't Make Me Think"

The third edition adds dedicated mobile coverage. Krug's position: the fundamental principles don't change for mobile, but the constraints are tighter. Smaller screens mean:

- Every element must earn its place even more aggressively.
- Touch targets must be large enough (the "fat finger" problem).
- The temptation to create a separate "mobile version" with reduced functionality is usually wrong — users expect to be able to do everything on mobile. Responsive design that preserves full capability is preferred.
- The concept of "managing real estate" becomes critical: prioritize ruthlessly, use progressive disclosure (show the top-level info first, let users tap for more), and don't shrink things to the point of unusability.

---

## Patterns & Approaches Introduced

### The "Don't Make Me Think" Test
Hold up any page or screen and ask: "Is there anything on this page that could make someone stop and think, even for a moment?" Every hesitation point is a usability failure to fix.

### The Trunk Test
A repeatable navigation audit you can apply to any page at any time. Five questions, immediate pass/fail. Excellent for automated or semi-automated UI review.

### Hallway Usability Testing
The lowest-cost, highest-return testing method. Three users, think-aloud protocol, one morning per month. Krug provides a complete script for running a test in his companion book *Rocket Surgery Made Easy*.

### The Reservoir of Goodwill Model
A mental model for understanding cumulative UX impact. Individual annoyances may seem trivial, but they accumulate. This model helps prioritize: fix the things that drain goodwill fastest, even if they're small individually.

### Happy Talk Elimination
A concrete editing pattern: identify and remove all self-congratulatory, marketing-inflated, or otherwise unnecessary introductory text. If a paragraph's removal wouldn't make the page less useful, remove it.

### The Billboard Test for Page Design
Design each page as if it were a billboard that users will see at 60 mph. Key content must be immediately scannable. Secondary content can exist but must not compete with the primary message.

### Tabs as Best-in-Class Navigation (When Done Right)
Krug highlights physical-metaphor tabs (with the active tab visually "in front") as one of the most effective navigation patterns because they create a strong "you are here" signal. The key requirement: the active tab must be a clearly different color and visually connected to the content area below it.

### Breadcrumb Navigation Pattern
Always present, always small, always use ">" as separator, always bold the last item (current page) and don't make it a link. Breadcrumbs are secondary wayfinding, not primary navigation.

---

## Tradeoffs & Tensions

### Simplicity vs. Completeness
Krug advocates ruthless simplification, but real products have complex feature sets. The tension: making things simple enough for first-time users while still serving power users. Krug's resolution is progressive disclosure — start simple, let users drill down — but this adds interaction cost for expert users.

### Convention vs. Innovation
Following conventions reduces cognitive load, but sometimes a product needs to differentiate or a better pattern exists. Krug's rule of thumb: innovate only when the new approach is so clearly better that it's self-evident. If your innovation requires explanation, stick with the convention. The threshold for "clearly better" should be very high.

### Designer's Model vs. User's Model
Designers understand the system's structure; users have a (usually incomplete, sometimes wrong) mental model of how things work. Navigation labels, category names, and workflows should match the user's model, not the designer's. This creates tension with internal stakeholders who want labels and structures that match the org chart or the database schema.

### Stakeholder Wants vs. User Needs (The Home Page)
Every department wants home page space. Krug's observation is that the home page is inherently a political compromise. The design challenge is making that compromise coherent to the user. No one "wins" the home page — the user has to win.

### Testing Rigor vs. Testing Frequency
Professional usability testing with recruited participants, screened demographics, and formal analysis produces more methodologically sound results. Hallway testing produces rougher results much more often. Krug argues that frequency beats rigor: three rounds of informal testing beat one round of formal testing every time. The tradeoff is that hallway testing may miss edge cases specific to your actual user demographics.

### Mobile-First vs. Desktop-First
Krug acknowledges the mobile-first design philosophy but doesn't fully commit to it. He observes that most teams still design desktop-first and adapt for mobile. His practical advice: whichever you do first, the other version should not lose functionality, only rearrange and reprioritize the visual hierarchy.

### Accessibility Investment vs. Practical Constraints
Full WCAG 2.0 AA compliance is the ideal but requires significant investment. Krug's pragmatic position: do the high-impact, low-cost things first (headings, alt text, color contrast, keyboard navigation). Don't let the scale of "full compliance" become an excuse for doing nothing.

---

## What to Watch Out For

### Overconfidence in "Common Sense"
Krug's principles feel like common sense after you read them, which can lead to the belief that you don't need to test. You do. "Common sense" usability is surprisingly uncommon in practice, and your intuitions about what's self-evident are colored by your own expertise. Test anyway.

### Using "Simplicity" as an Excuse to Remove Features
Krug advocates omitting needless words and reducing clutter, but this should not be misread as "remove features users need." The goal is to make existing features findable and usable, not to have fewer features. Complexity should be managed, not amputated.

### Treating the Book as a Complete UX Education
*Don't Make Me Think* is intentionally narrow. It covers usability heuristics and lightweight testing. It does not cover: user research methods beyond usability testing, information architecture in depth, interaction design patterns comprehensively, visual design theory, design systems, accessibility standards in detail, or quantitative UX measurement. It's a starting point, not a complete curriculum.

### Applying Web Patterns Uncritically to Native Apps
The book's patterns originate in web design. Native mobile and desktop apps have different interaction paradigms (gesture-based navigation, platform-specific patterns, system-level UI components). Applying Krug's web-centric advice to native apps requires translation.

### The "Three Users Is Enough" Misapplication
Krug's advice that 3-4 users per round is sufficient applies to finding major usability problems during iterative design. It does not mean 3 users is sufficient for validating a design, measuring task completion rates, or any form of statistical analysis. The advice is about problem discovery, not validation.

### Ignoring the Organizational Advice
The later chapters about making the case for usability within organizations get less attention than the design chapters, but they're critical. Usability improvements that never ship because they can't get organizational buy-in don't help users.

---

## Applicability by Task Type

### UI / Component Design
**Directly and immediately applicable.** Every component should pass the "don't make me think" test. Buttons should look like buttons. Labels should be unambiguous. Visual hierarchy should signal importance. Clickable elements should be obviously clickable. This is the single most useful reference for reviewing AI-generated UI code: hold each element up to the "would this cause a moment's confusion?" standard.

Specific checks:
- Do form labels clearly describe what's expected?
- Are buttons labeled with verbs describing the action?
- Is there sufficient contrast between primary and secondary actions?
- Do disabled states look different from enabled states?
- Is the visual hierarchy correct (most important action most prominent)?

### Navigation & Information Architecture
**Core competency of this book.** The trunk test is a repeatable, teachable navigation audit. Apply it to every page in a flow. Persistent navigation patterns, breadcrumb implementation, and the "you are here" principle provide concrete design criteria. For AI-generated navigation components, verify: Is the current section highlighted? Are navigation labels meaningful to users (not internal terms)? Can the user always get back to known ground?

### Feature Design (User Flows)
**Strongly applicable.** Krug's model of the satisficing, scanning user should inform every flow design:
- Users will not read instructions. The flow must be self-explanatory.
- Users will click the first thing that looks reasonable. Make the "right" thing the most prominent thing.
- Users will muddle through rather than learn. Design for their first attempt, not their tenth.
- Reduce the number of steps. Every additional step is an opportunity for drop-off.
- Error states should help users recover, not blame them.

The happy path should be the most visually obvious path. Designing for the happy path means making the expected sequence of actions the easiest to find and execute — while still gracefully handling deviations.

### Usability Review
**The book's sweet spot.** Krug essentially provides a lightweight usability review framework:
1. Apply the "don't make me think" test to each screen.
2. Run the trunk test on navigation.
3. Check for happy talk and eliminate it.
4. Verify visual hierarchy supports scanning.
5. Look for anything that requires reading instructions.
6. Assess the reservoir of goodwill — are there unnecessary friction points?

This can be formalized as a review checklist for AI-generated UI. An LLM reviewing a React component or an HTML template can be prompted with these specific criteria.

### Mobile Design Considerations
**Applicable with caveats.** Krug's mobile guidance is useful but less detailed than dedicated mobile design references (e.g., Luke Wroblewski's *Mobile First*). Key mobile checks from this book:
- Touch targets are large enough (44x44pt minimum).
- Content priority is appropriate for small screens.
- Full functionality is preserved (no "desktop only" features).
- Scrolling is preferred over tiny text or cramped layouts.
- The "fat finger" problem is respected in interactive element spacing.

---

## Relationship to Other Books in This Category

### *The Design of Everyday Things* — Don Norman (1988/2013)
Norman provides the theoretical foundations (affordances, signifiers, mapping, feedback, conceptual models) that Krug applies pragmatically to web UI. Norman answers "why do people get confused by designs?" at a cognitive science level; Krug answers "here's how to make this specific web page less confusing." Read Norman for the mental models, Krug for the immediate application.

### *About Face: The Essentials of Interaction Design* — Alan Cooper (4th ed., 2014)
Cooper's work is more comprehensive and systematic — goal-directed design, persona methodology, detailed interaction patterns. Krug is the quick-start guide; Cooper is the comprehensive reference. They're complementary: Krug for heuristic evaluation, Cooper for design methodology.

### *Refactoring UI* — Adam Wathan & Steve Schoger (2018)
Refactoring UI is the visual design companion to Krug's usability principles. Krug tells you that visual hierarchy matters; Wathan/Schoger show you exactly how to create it with spacing, color, typography, and layout. Highly complementary pairing — Krug for the "what" and "why," Refactoring UI for the "how" at the CSS/design-token level.

### *100 Things Every Designer Needs to Know About People* — Susan Weinschenk (2011)
Weinschenk provides the cognitive psychology research that underlies Krug's practical advice. Why do people scan? (Peripheral vision, pattern recognition.) Why do they satisfice? (Cognitive load, decision fatigue.) Reading Weinschenk explains *why* Krug's heuristics work.

### *Rocket Surgery Made Easy* — Steve Krug (2010)
Krug's companion book, which expands the usability testing chapters of DMMT into a complete, step-by-step guide for running DIY usability tests. If you take Krug's testing advice seriously, this is the operational manual.

### *Mobile First* — Luke Wroblewski (2011)
Wroblewski's book is a deeper treatment of the mobile design philosophy that Krug touches on in the 3rd edition. For teams building mobile-primary products, Wroblewski provides more detailed guidance on progressive disclosure, content prioritization, and touch interaction design.

---

## Freshness Assessment

**Publication date:** 2014 (3rd edition, revised and updated from the 2000 original and 2006 2nd edition).

**What has aged well:**
- The core principles are timeless. "Don't make me think" applies to any interface, any era. Scanning behavior, satisficing, and the importance of visual hierarchy are grounded in human cognition, not technology trends.
- The trunk test remains a valid navigation audit tool.
- The usability testing philosophy (test early, test cheap, test often) is as relevant as ever and has been validated by the industry's broad adoption of these practices.
- The "reservoir of goodwill" mental model applies to any product.

**What has aged or evolved:**
- The mobile treatment, while valuable, predates the maturity of modern responsive design frameworks, component libraries, and mobile-first design systems. Mobile UX is now a much richer topic.
- The book doesn't address design systems, component libraries, or the systematization of UI patterns that now dominates frontend development.
- No coverage of AI-driven interfaces, conversational UI, voice interfaces, or any interaction paradigm beyond traditional web and mobile screens.
- The accessibility guidance predates WCAG 2.1 and 2.2, and the field has evolved substantially.
- The book's examples and screenshots are dated (circa 2012-2013 web design), though the principles they illustrate remain valid.
- No discussion of dark patterns, though Krug's "usability as common courtesy" framing implicitly opposes them.

**Bottom line:** The principles are evergreen. The examples and some specific guidance show their age. For an AI agent reviewing or generating UI code in 2024+, the *principles* from this book are directly applicable; the *specific patterns* should be cross-referenced with current design system documentation (Material Design, Apple HIG, etc.).

---

## Key Framings Worth Preserving

### "Don't make me think" as a code review criterion
When reviewing any UI code — human-written or AI-generated — the single most useful question is: "Will the user have to think about what to do here?" This transforms a subjective design review into a specific, answerable question. Apply it to every interactive element, every label, every navigation choice.

### "We don't read, we scan" as a layout axiom
Any page layout — whether implemented in HTML/CSS, React components, or a design tool — should be evaluated first as a scanning surface. Ask: "If a user spends 2 seconds looking at this page, will they know what it's about and where to go next?" If not, the visual hierarchy needs work.

### The trunk test as a navigation audit protocol
Five questions, any page, any time. This is one of the few UX heuristics that is both precise enough to be actionable and general enough to apply universally. It can be embedded in a prompt for AI-assisted UI review: "For this page, can the user immediately identify: (1) what site this is, (2) what page they're on, (3) what the major sections are, (4) what their options are at this level, and (5) where they are in the overall structure?"

### Satisficing as a design constraint
Designing for users who will pick the first reasonable option — not the best option — changes everything about how you structure choices. The happy path (the most common, desired user action) must be the most visually prominent option. Secondary options should exist but not compete. This is directly applicable when prompting an AI to generate form layouts, pricing pages, or settings screens.

### Hallway testing as minimum viable research
"Any testing with any user is better than no testing" is a framing that reduces the activation energy for doing research. In vibe-coding workflows where features ship quickly, the hallway testing philosophy justifies spending 15 minutes showing a prototype to a colleague before shipping — and that 15 minutes may prevent shipping a confusing feature.

### The reservoir of goodwill as a prioritization tool
When triaging bugs and UX issues, ask: "Which of these drains the most goodwill?" This framing helps prioritize user-facing friction over technically interesting but low-impact improvements. It's especially useful for AI agents that need to rank issues by user impact rather than technical severity.

### "Get rid of half the words, then get rid of half of what's left"
A concrete, memorable editing heuristic. When an AI generates UI copy, help text, error messages, or onboarding flows, this rule should be applied as a post-processing step. The first draft always has too many words.
