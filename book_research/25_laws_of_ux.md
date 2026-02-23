# Laws of UX — Jon Yablonski (2020)

**Skill Category:** UX & Interaction Design / Cognitive Psychology
**Relevance to AI-assisted / vibe-coding workflows:** The most directly "agent-encodable" UX book — each law is a concrete principle with clear application criteria, perfect for anchoring UI design and review tasks. Every law maps to a testable heuristic an AI agent can check when generating or reviewing UI code.

---

## What This Book Is About

Jon Yablonski's *Laws of UX* (O'Reilly, 2020) distills psychological research into a concise collection of maxims that designers and developers can apply directly to product decisions. The book grew out of Yablonski's side project — the website lawsofux.com — which catalogs principles from cognitive psychology, perception, and human-computer interaction as discrete, memorable "laws."

The core thesis: **users bring predictable psychological tendencies to every interface, and ignoring those tendencies produces friction, confusion, and abandonment.** Rather than offering vague design philosophy, the book provides named principles, each rooted in peer-reviewed research, with clear applicability criteria and concrete examples.

The book is organized into three thematic sections:
1. **Laws relating to cognitive load and decision-making** (how users process information)
2. **Laws relating to perception and visual organization** (how users see and group elements)
3. **Laws relating to memory, experience, and effort** (how users remember and evaluate interactions)

Each law follows a consistent format: statement of the principle, the psychological origin, key takeaways, and design implications. This structure makes it uniquely suited for extraction into actionable reference material.

---

## Key Ideas & Mental Models

### 1. Fitts's Law

**Definition:** The time to acquire a target is a function of the distance to and size of the target.

**When it applies:** Any time a user must click, tap, or move a cursor to interact with an element — buttons, links, navigation items, form controls, and interactive targets of any kind.

**Concrete UI example:** A mobile app's primary call-to-action button (e.g., "Add to Cart") should be large and placed in the thumb zone (bottom center of screen), not as a small link in the top-right corner. On desktop, destructive actions like "Delete" should be smaller and further from the primary action to reduce accidental clicks.

**Key takeaways:**
- Make touch/click targets large enough (minimum 44x44pt on mobile per Apple HIG, 48x48dp per Material Design).
- Place frequently used actions in easily reachable areas.
- Reduce the distance between related sequential actions (e.g., a confirmation dialog should appear near the trigger element).
- Edge and corner targets on desktop are effectively infinite in size (the cursor stops at screen edge), which is why OS menus live at screen edges.

---

### 2. Hick's Law (Hick-Hyman Law)

**Definition:** The time it takes to make a decision increases with the number and complexity of choices.

**When it applies:** Navigation menus, feature selection, settings panels, onboarding flows, any moment where the user must choose among options.

**Concrete UI example:** A restaurant ordering app that presents 200 items in a flat list forces slow, overwhelming decisions. Breaking the menu into categories (Appetizers, Mains, Desserts) with 5-8 items each dramatically reduces decision time. Similarly, a SaaS pricing page with 3 tiers converts better than one with 7.

**Key takeaways:**
- Minimize the number of choices presented at any single decision point.
- Break complex tasks into smaller, sequential steps (progressive disclosure).
- Highlight recommended or default options to simplify the decision.
- This law applies to *decision-relevant* options — decorative elements or clearly labeled groups don't count the same way.
- Hick's Law does NOT mean "fewer is always better" — it means structuring choices to reduce cognitive effort per decision.

---

### 3. Miller's Law

**Definition:** The average person can hold approximately 7 (plus or minus 2) items in working memory at one time.

**When it applies:** Information architecture, content organization, navigation depth, dashboard design, any context where the user must hold multiple pieces of information simultaneously.

**Concrete UI example:** A dashboard displaying 15 ungrouped metrics overwhelms the user. Chunking them into 3-4 groups of 3-5 related metrics (e.g., "Revenue," "Engagement," "Performance") makes the information parseable. Phone numbers are formatted as (555) 867-5309 rather than 5558675309 for this reason.

**Key takeaways:**
- Organize content into chunks of 5-9 items.
- Use chunking (grouping related items) to extend effective working memory.
- The "7 plus or minus 2" is about *chunks*, not raw items — well-labeled groups effectively multiply capacity.
- Don't use this as a hard rule for UI element counts; use it as a guide for cognitive load management.
- This law is often misapplied as "never have more than 7 nav items" — the real insight is about working memory demands, not item counts.

---

### 4. Jakob's Law

**Definition:** Users spend most of their time on *other* sites, so they prefer your site to work the same way as all the other sites they already know.

**When it applies:** Every design decision involving conventions — navigation placement, icon meaning, interaction patterns, form behavior, e-commerce flows, signup/login patterns.

**Concrete UI example:** Placing a shopping cart icon in the top-right corner of an e-commerce site follows convention. Moving it to the bottom-left for "originality" forces users to re-learn a pattern they've internalized from hundreds of other sites. Similarly, using a hamburger menu icon on mobile is expected; replacing it with a novel glyph creates unnecessary friction.

**Key takeaways:**
- Leverage existing mental models and platform conventions by default.
- Innovation should happen in the value proposition, not in basic interaction patterns.
- When you must deviate from convention, do so gradually and provide clear affordances.
- Users transfer expectations from one product to another — this is the foundation of design patterns and component libraries.
- This is arguably the single most important law for AI-assisted UI generation: default to convention.

---

### 5. Law of Proximity (Gestalt)

**Definition:** Objects that are near each other tend to be perceived as a group.

**When it applies:** Layout design, form design, card layouts, dashboard organization, any visual arrangement of elements that should communicate relationships.

**Concrete UI example:** In a form, the label "Email" should be visually closer to its input field than to the next field's label. When labels float equidistant between two fields, users cannot quickly determine which label belongs to which input. Similarly, grouping related settings (e.g., all notification preferences) with tighter spacing and separating groups with more whitespace communicates structure without needing explicit borders.

**Key takeaways:**
- Use spacing to communicate relationships — related items should be close together; unrelated items further apart.
- Proximity is more powerful than boxes, lines, or colors for grouping.
- Consistent spacing creates a visual rhythm that aids scanning.
- This principle applies at every scale: within components, between components, and across page sections.

---

### 6. Law of Common Region (Gestalt)

**Definition:** Elements tend to be perceived as grouped if they share an enclosed area.

**When it applies:** Card-based layouts, form sections, grouped actions, any case where visual containment communicates belonging.

**Concrete UI example:** A credit card form that places card number, expiry, and CVV inside a single bordered card-shaped container instantly communicates that these fields are related — versus scattering them as separate form rows.

**Key takeaways:**
- Borders, background colors, and containers create perceived groups.
- Combine with proximity for strongest grouping signals.
- Cards are the most common UI pattern leveraging this principle.
- Useful when proximity alone is insufficient to communicate grouping (e.g., dense dashboards).

---

### 7. Law of Pragnanz (Gestalt — Law of Simplicity)

**Definition:** People tend to interpret ambiguous or complex images in the simplest form possible, because it requires the least cognitive effort.

**When it applies:** Icon design, logo design, data visualization, any visual element that must be quickly parsed.

**Concrete UI example:** The Olympics logo is perceived as five overlapping rings, not a complex interlocking shape, because the brain defaults to the simplest interpretation. In UI, simple geometric icons (circle for profile, house for home) are processed faster than ornate illustrations.

**Key takeaways:**
- Reduce visual complexity wherever possible.
- Simple shapes and clear visual hierarchies are processed faster.
- Users will simplify what they see regardless — design with that simplification in mind so they arrive at the *correct* simplified interpretation.

---

### 8. Law of Similarity (Gestalt)

**Definition:** Elements that share visual characteristics (color, shape, size, orientation) are perceived as related.

**When it applies:** Button styling, navigation items, status indicators, list items, any repeated UI elements that need to signal sameness or difference.

**Concrete UI example:** If all clickable links in a body of text are blue and underlined, users can instantly identify which text is interactive. If some links are blue, some are green, and some are styled like body text, the user must examine each element individually to determine its function.

**Key takeaways:**
- Consistent styling for functionally equivalent elements reduces scanning time.
- Use visual differentiation (color, size, weight) to signal functional differences.
- Breaking similarity deliberately draws attention (the Von Restorff Effect, below).

---

### 9. Law of Uniform Connectedness (Gestalt)

**Definition:** Elements that are visually connected (by lines, arrows, or continuity) are perceived as more related than elements with no connection.

**When it applies:** Process flows, step indicators, timelines, navigation breadcrumbs, relationship diagrams.

**Concrete UI example:** A checkout progress bar showing "Cart -> Shipping -> Payment -> Confirmation" with a connecting line makes the sequential relationship explicit. Without the line, four separate labels could be perceived as independent options rather than sequential steps.

**Key takeaways:**
- Use lines, arrows, and visual connections to show relationships and sequences.
- Particularly valuable for multi-step processes and hierarchical navigation.
- Combine with color changes (completed vs. upcoming steps) for maximum clarity.

---

### 10. Aesthetic-Usability Effect

**Definition:** Users perceive aesthetically pleasing designs as more usable than less attractive ones, regardless of actual usability.

**When it applies:** Overall visual design, first impressions, error tolerance, trust-building, any user-facing surface.

**Concrete UI example:** Two banking apps with identical functionality — one with polished typography, balanced whitespace, and cohesive color palette; the other with inconsistent fonts, cramped layout, and clashing colors. Users will rate the polished app as "easier to use" and will tolerate more minor usability issues before complaining.

**Key takeaways:**
- Visual polish is not vanity — it directly impacts perceived usability and trust.
- Beautiful design creates a positive emotional response that increases tolerance for friction.
- **Danger:** Aesthetic quality can mask genuine usability problems in testing. Pretty prototypes may receive artificially positive usability feedback.
- This effect is strongest during first impressions and weakens over time if real usability issues persist.
- For AI-generated UIs: investing in consistent, clean visual output pays disproportionate dividends.

---

### 11. Von Restorff Effect (Isolation Effect)

**Definition:** When multiple similar objects are present, the one that differs from the rest is most likely to be remembered.

**When it applies:** Call-to-action buttons, pricing page emphasis, notification badges, alerts, any element that must stand out from its context.

**Concrete UI example:** On a SaaS pricing page with three tiers, making the recommended "Pro" plan visually distinct (larger card, different background color, "Most Popular" badge) draws the user's eye and anchors the comparison. The distinct plan is remembered and chosen more often.

**Key takeaways:**
- Use visual contrast to make the most important element stand out.
- Limit the number of visually distinct elements — if everything is emphasized, nothing is.
- Restraint is essential: one CTA per view should be the primary visual anchor.
- Over-use of this effect creates visual noise and negates the benefit.

---

### 12. Doherty Threshold

**Definition:** Productivity soars when a computer and its users interact at a pace (<400ms) that ensures neither has to wait on the other.

**When it applies:** Page load times, API response feedback, animation duration, any system response to user action.

**Concrete UI example:** After a user clicks "Submit Order," showing a loading spinner within 100ms and completing the transaction feedback within 400ms maintains flow state. If the server takes 2 seconds, use optimistic UI (immediately show the order as placed, then confirm in background) or a skeleton screen to stay under the perceived threshold.

**Key takeaways:**
- System responses under 400ms feel instantaneous and maintain user engagement.
- If operations take longer, provide immediate visual feedback (progress indicators, skeleton screens, optimistic updates).
- Perceived performance matters as much as actual performance — animation and progressive loading can bridge the gap.
- This is the law most directly relevant to frontend performance optimization.
- Target: 100ms for direct manipulation feedback, 400ms for system operations, 1000ms as the outer limit before users feel the system is "slow."

---

### 13. Tesler's Law (Law of Conservation of Complexity)

**Definition:** For any system, there is a certain amount of complexity that cannot be reduced; it can only be moved between the system and the user.

**When it applies:** Feature design, form design, configuration vs. convention decisions, API design, any simplification effort.

**Concrete UI example:** An airline booking form can ask the user to manually enter departure city, arrival city, dates, passenger counts, class, and meal preferences (complexity on the user). Or it can auto-detect location, suggest popular routes, pre-fill dates based on patterns, and default to standard options (complexity absorbed by the system). The total complexity is the same — the question is who bears it.

**Key takeaways:**
- Simplifying the UI doesn't eliminate complexity — it moves it to the backend/system.
- The goal is to ensure the *user* bears as little complexity as possible.
- Smart defaults, auto-detection, and progressive disclosure are mechanisms for absorbing complexity.
- **Danger:** Over-simplification can remove necessary user control. The goal is appropriate distribution, not minimum surface area.
- Every "simple" UI is backed by complex logic — this is the law that justifies investing engineering effort in smart defaults.

---

### 14. Postel's Law (Robustness Principle)

**Definition:** Be liberal in what you accept, and conservative in what you send (originally from TCP/IP protocol design, applied to UI).

**When it applies:** Form validation, search input, data entry, any point where the user provides input to the system.

**Concrete UI example:** A phone number field should accept "(555) 867-5309", "555-867-5309", "5558675309", and "+1 555 867 5309" — then normalize internally to a canonical format. Rejecting valid input because it doesn't match an arbitrary format pattern punishes the user for the system's rigidity.

**Key takeaways:**
- Accept varied input formats and normalize behind the scenes.
- Show clear, consistent output format regardless of input variation.
- Provide real-time, gentle validation rather than post-submission rejection.
- Anticipate common input variations (with/without country codes, spaces vs. dashes, case sensitivity).
- This law directly informs form validation strategy and error handling design.

---

### 15. Peak-End Rule

**Definition:** People judge an experience largely based on how they felt at its most intense point (the peak) and at the end, rather than the sum or average of every moment.

**When it applies:** Onboarding flows, checkout completion, error recovery, subscription cancellation, any multi-step experience with a defined beginning and end.

**Concrete UI example:** A checkout flow that is mediocre throughout but ends with a delightful, personalized confirmation page ("Your order is on its way, Sarah! Here's a 10% code for next time.") will be remembered more favorably than a uniformly decent experience with a bland "Order #48291 confirmed" ending.

**Key takeaways:**
- Invest disproportionately in the emotional peak and the final moment of any experience.
- Identify the most intense positive or negative moments and amplify or mitigate them.
- Endings matter enormously: confirmation pages, success states, and offboarding flows deserve premium design attention.
- Negative peaks (errors, confusing steps) disproportionately damage the overall experience memory.
- For multi-step flows: the last screen the user sees shapes their memory of the entire process.

---

### 16. Zeigarnik Effect

**Definition:** People remember uncompleted or interrupted tasks better than completed ones.

**When it applies:** Progress indicators, onboarding checklists, gamification, profile completion prompts, any experience where motivating continuation is valuable.

**Concrete UI example:** LinkedIn's profile completion bar ("Your profile is 70% complete — add a profile photo to reach 80%") exploits the Zeigarnik Effect. The incomplete state creates cognitive tension that motivates the user to finish. Similarly, a SaaS onboarding checklist showing 3/5 steps complete creates a stronger pull to finish than showing no progress at all.

**Key takeaways:**
- Show progress toward goals to create psychological motivation to complete.
- Incomplete visual indicators (progress bars, checklists) create productive tension.
- Starting a task creates commitment — showing users they've already begun (even minimally) increases completion rates.
- **Danger:** Overuse creates anxiety and fatigue. Too many incomplete indicators feels oppressive rather than motivating.
- Use selectively for high-value completion goals, not for every minor interaction.

---

### 17. Serial Position Effect

**Definition:** Users tend to best remember the first and last items in a series.

**When it applies:** Navigation ordering, list design, feature presentation, onboarding step sequencing.

**Concrete UI example:** In a mobile bottom navigation bar with 5 items, the most important actions should be placed at the first and last positions. iOS places "Home" first and the user's "Profile" last for this reason — the middle items receive less attention and recall.

**Key takeaways:**
- Place the most important items at the beginning and end of lists, menus, and sequences.
- The middle positions receive the least attention and recall.
- For navigation: anchor key actions at the extremes.
- For onboarding: make the first and last steps the most impactful.

---

### 18. Occam's Razor

**Definition:** Among competing hypotheses (or designs) that explain the same observations, the one with the fewest assumptions should be selected.

**When it applies:** Feature scoping, UI simplification, deciding between design approaches, removing unnecessary elements.

**Concrete UI example:** A settings page that could use a complex role-based permission matrix OR a simple "Admin / Member / Viewer" dropdown. If the dropdown covers 95% of use cases, it is the preferable design — the complex matrix can be offered as an "Advanced" option for the remaining 5%.

**Key takeaways:**
- Favor the simplest solution that adequately solves the problem.
- Remove elements that don't contribute to the user's goal.
- Complexity should be justified by user need, not technical capability.
- This is a design philosophy principle rather than a cognitive law, but it reinforces Tesler's Law and Miller's Law.

---

### 19. Parkinson's Law

**Definition:** Any task will inflate until all of the available time is spent.

**When it applies:** Form design, task completion flows, time-boxed interactions, anywhere where open-endedness could lead to procrastination or over-investment.

**Concrete UI example:** A feedback form with a single text area and no constraints invites users to either write an essay or abandon the task. Constraining to "Rate 1-5, then optionally add a sentence" provides structure that helps users complete the task in reasonable time.

**Key takeaways:**
- Provide constraints and structure to help users complete tasks efficiently.
- Open-ended inputs without guidance tend to produce either over-investment or abandonment.
- Time indicators ("This takes ~2 minutes") set expectations and reduce procrastination.
- Smaller, scoped input fields lead to higher completion rates than large, unstructured ones.

---

## Patterns & Approaches Introduced

### The Psychology-First Design Process
Yablonski advocates starting design decisions from psychological principles rather than aesthetic preferences or trend-following. The workflow:
1. Identify the user's cognitive task (deciding, scanning, remembering, evaluating).
2. Map relevant psychological principles to that task.
3. Design the interface to align with — rather than fight against — those cognitive tendencies.
4. Test whether the design respects the principle under realistic conditions.

### Progressive Disclosure as Meta-Pattern
Multiple laws converge on progressive disclosure as a core strategy:
- **Hick's Law** says reduce choices at each decision point.
- **Miller's Law** says chunk information into digestible groups.
- **Tesler's Law** says absorb complexity into the system.
- Together, they prescribe: show only what's needed now, reveal more on demand, and let the system handle what the user doesn't need to see.

### Gestalt Grouping as Layout Foundation
The Gestalt laws (Proximity, Common Region, Similarity, Uniform Connectedness, Pragnanz) form a hierarchy of visual organization tools:
1. **Proximity** — primary grouping mechanism (spacing)
2. **Common Region** — secondary grouping (containers/cards)
3. **Similarity** — functional equivalence signaling (consistent styling)
4. **Uniform Connectedness** — sequential/relational signaling (lines/arrows)
5. **Pragnanz** — overall simplification principle (keep it simple)

### The Performance Perception Stack
Doherty Threshold + Peak-End Rule + aesthetic-usability effect combine into a perception management strategy:
- Make it fast (Doherty: <400ms).
- If you can't make it fast, make it *feel* fast (skeleton screens, optimistic UI).
- Make the end feel great (Peak-End Rule).
- Make it look good throughout (Aesthetic-Usability Effect).

---

## Tradeoffs & Tensions

### Convention vs. Innovation (Jakob's Law vs. Differentiation)
Jakob's Law says follow conventions. But products also need to differentiate. The resolution: **innovate on value, not on interaction patterns.** A novel data visualization or unique content recommendation algorithm differentiates without breaking the user's mental model of how navigation, buttons, and forms work.

### Simplicity vs. Power (Tesler's Law vs. Expert Users)
Absorbing complexity helps beginners but can frustrate power users who want direct control. The resolution: **layered interfaces** — simple defaults with accessible advanced options. Gmail's search is simple by default but supports complex operators for power users.

### Aesthetics vs. Honest Usability Testing (Aesthetic-Usability Effect)
Beautiful prototypes receive better usability ratings than they deserve. The resolution: **test with lower-fidelity prototypes for usability, then add polish.** Or explicitly instruct test participants to focus on task completion rather than overall impression.

### Motivation vs. Anxiety (Zeigarnik Effect)
Progress indicators motivate completion but can also create anxiety when users feel overwhelmed by incomplete tasks. The resolution: **use sparingly and ensure completion is achievable.** A 3/5 checklist motivates; a dashboard showing 47 incomplete items demoralizes.

### Speed vs. Accuracy (Fitts's Law vs. Error Prevention)
Large, close targets are fast to hit but increase accidental activation risk. The resolution: **size primary actions generously, separate destructive actions spatially, and add confirmation for irreversible actions.**

### Fewer Choices vs. Adequate Options (Hick's Law vs. User Needs)
Over-applying Hick's Law can result in oversimplified interfaces that lack necessary functionality. The resolution: **reduce choices per decision point through categorization and progressive disclosure, not by eliminating options entirely.**

---

## What to Watch Out For

1. **Misapplying Miller's Law as a hard cap.** "No more than 7 items" is a myth. The law is about working memory chunks, not UI element counts. A well-organized nav with 12 items (grouped into 3 categories of 4) is fine.

2. **Using aesthetics to paper over usability problems.** The Aesthetic-Usability Effect means beautiful UIs *mask* problems in testing. Always test task completion separately from aesthetic evaluation.

3. **Treating each law in isolation.** The laws interact. Hick's Law (reduce choices) can conflict with Miller's Law (provide enough context) — the resolution depends on context, not rigid application of either law alone.

4. **Confusing Tesler's Law with "make everything automatic."** Some complexity rightfully belongs with the user (e.g., choosing a shipping address). The goal is appropriate allocation, not total automation.

5. **Over-indexing on the Zeigarnik Effect.** Dark patterns exploit this (endless notifications about "incomplete" profiles). Use it to motivate genuinely valuable completions, not to manufacture anxiety.

6. **Ignoring cultural and accessibility dimensions.** The laws describe general cognitive tendencies but don't account for cultural variation in reading direction, color meaning, or accessibility needs. Fitts's Law calculations change significantly for users with motor impairments.

7. **Treating the book as an exhaustive list.** These laws are a starting point, not a complete cognitive psychology curriculum. They don't cover emotional design (Norman), persuasive design (Fogg), or information architecture in depth.

8. **Applying laws without user research.** The laws provide hypotheses about what will work. They don't replace testing with actual users in actual contexts. A law might predict that reducing options helps, but only research reveals *which* options to cut.

---

## Applicability by Task Type

### UI / Component Design
- **Fitts's Law:** Size interactive targets appropriately (44px+ mobile, 24px+ desktop minimum).
- **Law of Proximity:** Space related elements closer together within components.
- **Law of Similarity:** Style functionally equivalent elements identically.
- **Aesthetic-Usability Effect:** Invest in visual polish — it directly impacts perceived quality.
- **Von Restorff Effect:** Make the primary action visually distinct from secondary actions.

### Navigation Design
- **Jakob's Law:** Follow platform conventions for nav placement (top bar desktop, bottom bar mobile).
- **Hick's Law:** Limit top-level nav items; use progressive disclosure for deep hierarchies.
- **Serial Position Effect:** Place most important nav items first and last.
- **Miller's Law:** Group nav items into meaningful categories of manageable size.
- **Law of Uniform Connectedness:** Use visual connections (breadcrumbs, step indicators) to show navigation state.

### Form Design
- **Postel's Law:** Accept varied input formats; normalize internally.
- **Fitts's Law:** Make submit buttons large and well-placed; keep related fields close.
- **Hick's Law:** Break long forms into logical steps rather than presenting all fields at once.
- **Law of Proximity:** Labels should be visually closer to their own field than to adjacent fields.
- **Tesler's Law:** Auto-fill, smart defaults, and input masks absorb complexity from the user.
- **Parkinson's Law:** Constrain open-ended inputs; provide structure and expected length cues.

### Loading / Performance Perception
- **Doherty Threshold:** Target <400ms for system responses; provide immediate feedback for anything longer.
- **Peak-End Rule:** If loading is unavoidable, make the reveal moment satisfying.
- **Aesthetic-Usability Effect:** Skeleton screens and smooth loading animations feel faster than spinners.
- **Zeigarnik Effect:** Progress bars for long operations give users a sense of momentum and completion to anticipate.

### Feature Complexity Decisions
- **Tesler's Law:** Determine who bears the complexity — user or system. Default to system.
- **Hick's Law:** Each feature adds a choice; evaluate whether the added choice justifies the added decision cost.
- **Occam's Razor:** Prefer the simplest design that solves the problem for the majority of users.
- **Jakob's Law:** New features should leverage existing mental models, not require learning novel patterns.
- **Miller's Law:** New features should fit within existing information architecture without exceeding chunking limits.

---

## Relationship to Other Books in This Category

### Direct Complements
- **Don Norman, *The Design of Everyday Things* (1988/2013):** Norman provides the foundational theory of affordances, signifiers, and conceptual models. Yablonski operationalizes many of Norman's ideas into named, applicable heuristics. Read Norman for *why* design works psychologically; read Yablonski for *which specific principles* to check.
- **Steve Krug, *Don't Make Me Think* (2000/2014):** Krug's intuition-driven usability principles overlap significantly with Yablonski's laws (especially Jakob's Law and Hick's Law), but Yablonski provides the psychological research grounding that Krug deliberately omits.
- **Susan Weinschenk, *100 Things Every Designer Needs to Know About People* (2011):** Broader in scope (covers social psychology, motivation, emotion), but less structured. Yablonski's format is more directly actionable.

### Broader Context
- **Daniel Kahneman, *Thinking, Fast and Slow* (2011):** The System 1 / System 2 framework underpins many of Yablonski's laws. Hick's Law, Miller's Law, and the Aesthetic-Usability Effect all relate to System 1 (fast, automatic) vs. System 2 (slow, deliberate) processing. Kahneman provides the deep theory; Yablonski provides the UI-specific applications.
- **Aarron Walter, *Designing for Emotion* (2011):** Covers the emotional layer that Yablonski's cognitive focus doesn't deeply address. The Aesthetic-Usability Effect and Peak-End Rule are the bridges between these two perspectives.
- **Nir Eyal, *Hooked* (2014):** The Zeigarnik Effect and variable reward principles overlap with Eyal's habit-formation model. Yablonski provides the cognitive foundation; Eyal provides the behavioral design framework.

### For AI/Agent Workflows Specifically
Laws of UX is the most "agent-ready" design reference because each law is a discrete, testable heuristic. When an AI agent is generating or reviewing UI, it can check:
- Are touch targets at least 44px? (Fitts's)
- Are there more than 7 ungrouped options? (Hick's / Miller's)
- Does the nav follow platform conventions? (Jakob's)
- Is there feedback within 400ms? (Doherty)
- Are related items visually grouped? (Proximity)

No other UX book offers this level of direct encode-ability.

---

## Freshness Assessment

**Publication date:** April 2020 (1st edition). A second edition was published in 2024 expanding the content.

**Core validity:** The psychological research underlying each law is decades old (Fitts 1954, Hick 1952, Miller 1956, Gestalt principles from the 1920s). These principles are not trend-dependent and remain fully valid.

**What has evolved since publication:**
- **Mobile-first and touch-first design** has only increased the importance of Fitts's Law and target sizing.
- **AI-generated interfaces** make Jakob's Law even more critical — generated UIs must follow conventions users expect.
- **Performance expectations** have tightened — the Doherty Threshold of 400ms is now generous; modern users expect <200ms for basic interactions.
- **Dark pattern awareness** has increased, making ethical application of Zeigarnik Effect and other persuasive principles more important.
- **The 2nd edition (2024)** adds updated examples and additional principles, but the core laws remain unchanged.

**Bottom line:** The underlying science is timeless. The examples may age, but the principles will not. This book remains fully current for practical application.

---

## Key Framings Worth Preserving

1. **"Users spend most of their time on other sites."** (Jakob's Law) — The most powerful single sentence for convincing stakeholders to follow conventions instead of reinventing standard patterns. Use this exact framing when reviewing any UI that deviates from conventions without clear justification.

2. **"Complexity can only be moved, not eliminated."** (Tesler's Law) — The antidote to "just make it simpler" feedback. When stakeholders ask to simplify a form, this framing redirects the conversation to: who should bear the complexity — the user or the system?

3. **"The time to make a decision increases with the number and complexity of choices."** (Hick's Law) — Use this to justify progressive disclosure, phased onboarding, and feature gating. The word "complexity" is key — it's not just count, it's cognitive weight per option.

4. **"People judge an experience based on its peak and its end."** (Peak-End Rule) — Use this to justify investing design effort in confirmation pages, success states, and error recovery flows — the moments most teams under-invest in.

5. **"Aesthetically pleasing design creates a positive response that makes users more tolerant of minor usability issues."** (Aesthetic-Usability Effect) — Use this to justify design system investment and visual polish. Also use the flip side: warn that pretty prototypes receive artificially positive usability feedback.

6. **"Productivity soars when response time is under 400ms."** (Doherty Threshold) — The single most useful performance benchmark to give to engineers. Not a vague "make it fast" — a specific, measurable target with research backing.

7. **"People remember uncompleted tasks better than completed ones."** (Zeigarnik Effect) — Use carefully. This is the psychological basis for progress bars, onboarding checklists, and profile completion prompts. It is also the psychological basis for manipulative dark patterns. The ethical line: does completion genuinely benefit the user?

8. **"Be liberal in what you accept."** (Postel's Law) — The single best principle for form validation design. If a human can understand the input, the system should too.
