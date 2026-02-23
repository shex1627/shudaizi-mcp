# The Design of Everyday Things — Don Norman (2013)

**Skill Category:** UX & Interaction Design
**Relevance to AI-assisted / vibe-coding workflows:** The foundational mental model for human-centered design — anchors agents to consider the user's perspective, affordances, and error prevention in any UI task. When an agent generates a UI component, designs a form, or structures an error message, the principles in this book provide the first-order checklist: Is the action discoverable? Does the user get feedback? Will they form the right mental model? Can we prevent the predictable error?

---

## What This Book Is About

The Design of Everyday Things (DOET) is Don Norman's argument that most product failures are not the user's fault — they are design failures. Originally published in 1988 as *The Psychology of Everyday Things*, the 2013 revised and expanded edition updates the framework for the digital age while preserving the core thesis: good design starts with understanding human psychology, not with aesthetics or engineering convenience.

The book is organized around seven chapters:

1. **The Psychopathology of Everyday Things:** Introduces affordances, signifiers, mappings, constraints, and feedback — the vocabulary for analyzing any interaction.
2. **The Psychology of Everyday Actions:** Presents the Seven Stages of Action model and the Gulf of Execution / Gulf of Evaluation framework.
3. **Knowledge in the Head and in the World:** Explains how people navigate complex systems using a mix of memorized knowledge and environmental cues — and why designs should minimize memory burden.
4. **Knowing What to Do: Constraints, Discoverability, and Feedback:** Deepens the treatment of constraints (physical, cultural, semantic, logical) and how they guide users toward correct actions without instruction manuals.
5. **Human Error? No, Bad Design:** Reframes errors as predictable consequences of design choices. Introduces the slip vs. mistake taxonomy and design strategies for error prevention and recovery.
6. **Design Thinking:** Outlines the human-centered design process — observation, ideation, prototyping, testing — as a double-diamond of finding the right problem and finding the right solution.
7. **Design in the World of Business:** Addresses the organizational pressures that work against good design — featuritis, competitive feature matching, schedule pressure — and argues for design as a business discipline.

Norman's through-line is that human cognition is remarkably consistent and predictable. When you design *with* those cognitive patterns rather than against them, products become intuitive. When you ignore them, you get doors people push when they should pull, stove controls nobody can map to burners, and error messages that blame the user for the system's ambiguity.

---

## Key Ideas & Mental Models

### 1. Affordances and Signifiers (The Most Misused Concept in UX)

**Affordance** is the relationship between the properties of an object and the capabilities of the agent that determines how the object could possibly be used. A flat plate on a door *affords* pushing. A handle *affords* pulling. Affordances exist whether or not they are visible — they are properties of the interaction between object and agent, not properties of the object alone.

**Signifiers** are the perceivable cues that communicate where the action should take place and how. A "PUSH" label on a door is a signifier. A button's raised appearance on a screen is a signifier. Norman added this term in the 2013 edition specifically because the design community had been misusing "affordance" to mean "visual cue." The distinction matters:

- Affordance = what actions are *possible*
- Signifier = what actions are *communicated*

A touchscreen affords tapping anywhere, but only the visible buttons signify where to tap.

**Practical implication for UI work:** Every interactive element must have a clear signifier. Flat design trends that remove visual depth, hover states, and border cues often destroy signifiers while preserving affordances — the button still works, but the user cannot tell it is a button.

### 2. Conceptual Models

A conceptual model is the user's internal understanding of how a system works. It does not need to be technically accurate — it needs to be *functionally useful*. The designer has a design model (how the system actually works). The user forms a user model (their understanding of how it works). The system image — the totality of the product's appearance, behavior, documentation, and feedback — is the only thing mediating between the two.

**The design principle:** The system image must communicate a coherent, correct-enough conceptual model. When the system image is ambiguous or contradictory, users form wrong mental models and make systematic errors.

**Practical implication:** When building interfaces, ask: "What mental model will a user form from looking at this?" If the visual hierarchy, labeling, and behavior would lead a reasonable person to a wrong conclusion about what will happen when they click, the design is broken — regardless of whether it is "technically correct."

### 3. The Seven Stages of Action

Norman models any human interaction as a cycle of seven stages:

**Goal (top):**
1. Goal — Form the goal (what do I want to accomplish?)

**Execution side (Gulf of Execution):**
2. Plan — What are the alternative action sequences?
3. Specify — What action can I do now?
4. Perform — How do I do it?

**Evaluation side (Gulf of Evaluation):**
5. Perceive — What happened?
6. Interpret — What does it mean?
7. Compare — Is this OK? Have I accomplished my goal?

The **Gulf of Execution** is the gap between the user's intention and the available actions. The **Gulf of Evaluation** is the gap between the system's state and the user's ability to perceive and interpret that state.

**Practical implication:** Every UI friction can be diagnosed as a failure at a specific stage. User cannot figure out what to click? Gulf of Execution (stages 2-4). User clicked but cannot tell what happened? Gulf of Evaluation (stages 5-7). This framework turns vague usability complaints into specific, actionable design problems.

### 4. Feedback

Feedback is the communication of the results of an action. Norman argues that feedback must be:
- **Immediate** — delayed feedback breaks the causal link between action and result
- **Informative** — it must convey what happened, not just that something happened
- **Non-excessive** — too much feedback (beeps, flashes, popups for every micro-action) trains users to ignore all feedback, including critical feedback

**Practical implication:** Loading spinners without progress indication are poor feedback. Toast notifications that vanish in 2 seconds are poor feedback for destructive actions. Error messages that say "Something went wrong" are anti-feedback. The gold standard is feedback that confirms the action, shows the result, and indicates the new state — all without requiring the user to go looking for it.

### 5. Mapping

Mapping is the relationship between controls and their effects. **Natural mapping** exploits spatial analogies and cultural standards to make the relationship obvious. The classic bad example: a row of identical stove knobs in a line, controlling burners arranged in a square grid. The classic good example: stove knobs arranged in the same spatial pattern as the burners they control.

Norman identifies three levels of mapping quality:
- **Best (natural mapping):** Spatial correspondence between control layout and device layout
- **Good:** Cultural or conventional mapping (red = stop, green = go)
- **Poor:** Arbitrary mapping requiring memorization or labels

**Practical implication for digital UI:** Group controls near the things they affect. Place format controls adjacent to the text they format. Put settings toggles next to the feature they control, not buried in a distant settings panel. The more spatial separation between control and effect, the worse the mapping.

### 6. Constraints (Physical, Cultural, Semantic, Logical)

Constraints limit the possible actions, ideally narrowing the user's choices to only correct ones:

- **Physical constraints:** The USB plug only fits one way (pre-USB-C). Physical size prevents wrong insertion.
- **Cultural constraints:** Conventions like "red means danger" or "X means close." These vary by culture and can change over time.
- **Semantic constraints:** The meaning of the situation restricts possibilities. A rearview mirror goes on the front windshield because that is the only place its purpose makes sense.
- **Logical constraints:** If there are three components and two are placed, the third must go in the remaining spot. Logical constraints use reasoning to eliminate alternatives.

**Practical implication:** Form validation is a constraint system. Disabling the submit button until required fields are filled is a logical constraint. Restricting a phone number input to digits is a physical constraint (digitally enforced). The best constraint is one the user never notices because it silently prevents the wrong action rather than punishing it after the fact.

### 7. Slips vs. Mistakes (The Error Taxonomy)

This is one of Norman's most practically valuable contributions:

**Slips** are errors where the user has the right goal but performs the wrong action. They occur during automatic, skilled behavior.
- **Action-based slips:** Performing the wrong action (typing "teh" instead of "the," clicking the adjacent button)
- **Memory-lapse slips:** Forgetting to complete a step in a sequence (leaving the original on the copier glass)
- **Mode-error slips:** Performing the right action in the wrong mode (typing in caps because Caps Lock is on without noticing)
- **Capture slips:** A frequently performed action "captures" a less frequent one that shares initial steps (driving to work on a Saturday when you meant to go to the store, because the route shares the first few turns)

**Mistakes** are errors where the user forms the wrong goal or plan. They occur during conscious, deliberative thought.
- **Rule-based mistakes:** Applying the wrong rule to the situation (using the wrong formula because the problem was misclassified)
- **Knowledge-based mistakes:** Incomplete or incorrect mental model leads to a wrong plan
- **Memory-lapse mistakes:** Forgetting the goal itself partway through

**Design strategies differ by error type:**
- For slips: Add constraints that prevent the wrong action, add confirmation for destructive actions, make it easy to undo
- For mistakes: Provide better feedback and clearer conceptual models so the user forms the right plan, make the system state visible, support exploration without penalty

**Practical implication:** "Are you sure you want to delete?" is slip prevention (accidental click). A clear "Trash" folder with 30-day recovery is mistake recovery (user deleted intentionally but later realizes it was wrong). Both are needed; neither replaces the other.

### 8. Discoverability and Understanding

Norman argues that a well-designed product must address two questions:
- **Discoverability:** Can the user figure out what actions are possible and how to perform them?
- **Understanding:** Can the user figure out what the product is, how it works, and what the different controls and settings mean?

Five fundamental psychological concepts support discoverability: affordances, signifiers, constraints, mappings, and feedback. Together, Norman calls these the "fundamental principles of interaction."

**Practical implication:** Discoverability is not the same as simplicity. A product can be discoverable and complex (a well-organized IDE). A product can be simple and undiscoverable (a minimalist app that hides all actions behind unmarked gestures). The goal is discoverability, not minimalism for its own sake.

### 9. Knowledge in the Head vs. Knowledge in the World

People navigate complex systems using two kinds of knowledge:
- **Knowledge in the head:** Memorized procedures, learned shortcuts, internal mental models
- **Knowledge in the world:** Labels, signs, physical constraints, contextual cues — information embedded in the environment

Good design uses knowledge in the world to reduce the burden on knowledge in the head. Icons with labels, contextual tooltips, placeholder text in form fields, and visible system state are all ways of putting knowledge in the world.

**The tradeoff:** Knowledge in the head is faster (experts skip reading labels). Knowledge in the world is more accessible (novices can function without training). The best designs support both — visible cues for novices, keyboard shortcuts for experts.

### 10. The Human-Centered Design Process

Norman outlines a four-step iterative process:

1. **Observation:** Study users in their natural context. Identify the real problem (which is often different from the stated problem).
2. **Idea Generation:** Brainstorm widely. Do not commit to solutions too early. Question the problem framing.
3. **Prototyping:** Build quick, cheap representations of ideas. Test them with real users. Expect failure — that is the point.
4. **Testing:** Observe users interacting with prototypes. Identify where the design fails the seven stages of action. Iterate.

Norman emphasizes the "double diamond" — the first diamond is about finding the right problem (diverge to explore the space, converge to define the problem). The second diamond is about finding the right solution (diverge to explore solutions, converge to implement and test).

**Key principle:** "Solve the right problem." Many products fail not because they solved the problem badly, but because they solved the wrong problem well.

---

## Patterns & Approaches Introduced

| Pattern | Description | When to Use |
|---|---|---|
| **Signifier Audit** | Systematically check every interactive element for visible, unambiguous signifiers | Any UI review — especially after adopting flat/minimal design systems |
| **Gulf Analysis** | Diagnose usability problems as Gulf of Execution or Gulf of Evaluation failures | When users report confusion — identify which gulf is the bottleneck |
| **Slip-Proof Design** | Add undo, confirmation dialogs, constraints, and spatial separation for destructive actions | Any flow involving deletion, payment, or irreversible state changes |
| **Mistake-Proof Design** | Improve conceptual models, make system state visible, support safe exploration | Onboarding flows, complex configuration, multi-step wizards |
| **Natural Mapping** | Arrange controls in spatial correspondence with the things they affect | Control panels, settings pages, dashboard layouts, WYSIWYG editors |
| **Constraint Funneling** | Layer physical, semantic, and logical constraints to narrow choices to correct ones | Form design, input validation, multi-step workflows |
| **Forcing Function** | Design sequences where one step cannot proceed until the prerequisite is complete | Checkout flows, setup wizards, safety-critical operations |
| **Knowledge in the World** | Embed necessary information in the interface rather than requiring memorization | Labels, placeholder text, inline help, contextual tooltips |
| **Feedforward** | Show what will happen *before* the action is taken (preview, hover states, dry-run) | Destructive actions, complex transformations, drag-and-drop |
| **Root Cause Analysis for Error** | When a user error occurs, trace it through the seven stages to find the design failure | Post-incident review, usability testing analysis |

---

## Tradeoffs & Tensions

### Discoverability vs. Efficiency
Making everything discoverable (visible controls, labels, explanatory text) slows down expert users who already know what to do. Hiding features behind gestures, keyboard shortcuts, or command palettes speeds up experts but locks out novices. Norman favors discoverability as the default, with progressive disclosure and shortcuts layered on top. The practical resolution: design for the novice's first experience, then add accelerators for the expert's hundredth.

### Simplicity vs. Capability
Norman warns against two failure modes: (1) feature creep ("featuritis") that makes products unusable, and (2) over-simplification that removes necessary capabilities. His position: the answer is not fewer features but better *organization* of features. Complexity in the world is fine; complexity in the interface is not. The job of design is to tame complexity, not to eliminate it.

### Conventions vs. Innovation
Norman argues that conventions (established patterns like the QWERTY layout, the desktop metaphor, the hamburger menu) should not be broken without very good reason. Conventions are knowledge in the world — they reduce learning cost by leveraging existing mental models. Innovation that breaks conventions must be dramatically better to justify the relearning cost. Most "innovative" interfaces are merely different, not better.

### Error Prevention vs. User Autonomy
Aggressive error prevention (disabled buttons, confirmation dialogs, restricted inputs) can feel paternalistic and slow. Insufficient error prevention leads to costly mistakes. Norman advocates layered prevention: make the right action easy and obvious, make the wrong action difficult but not impossible, and always provide recovery (undo). The goal is not to prevent all errors but to make errors recoverable and low-cost.

### Aesthetics vs. Usability
Norman does not dismiss aesthetics — in fact, he argues in his later book *Emotional Design* (2004) that attractive things work better because positive affect improves cognitive flexibility. But in DOET, the warning is clear: aesthetics that degrade signifiers, feedback, or mapping are net negative. A beautiful interface that no one can figure out how to use is a failed design, period.

### Blame the User vs. Blame the Design
Norman's most fundamental stance: when humans make errors, it is almost always a signal that the design failed, not that the human is deficient. This framing shift is the single most important contribution of the book. It changes the designer's job from "make something and hope users figure it out" to "observe how humans actually think and design for that reality."

---

## What to Watch Out For

### Treating Affordances as Visual Properties
The most common misapplication of Norman's vocabulary. Designers say "this button has good affordance" when they mean "this button has a clear signifier." Affordances are relational properties between object and agent — they exist independently of perception. What you are usually evaluating in a design review is the quality of the *signifiers*. This is not pedantry; confusing the terms leads to confusing the analysis.

### Applying DOET Principles Rigidly to Expert-Facing Tools
Norman's framework was developed primarily around everyday consumer products. Tools for experts (code editors, 3D modeling software, trading terminals) have different constraints: users invest significant learning time, efficiency dominates discoverability after onboarding, and power users actively resist "simplification" that removes capability. Apply DOET principles to these tools selectively — signifiers and feedback always matter, but the discoverability-vs-efficiency tradeoff tilts differently.

### Ignoring the Organizational Chapter
Chapter 7 on design in business contexts is often skipped but is practically essential. Norman explains why companies systematically degrade their own products through competitive feature matching, management-driven timelines, and the tendency to add features rather than improve existing ones. If you only internalize the psychological principles and ignore the organizational dynamics, you will design good solutions that never ship or get overridden by business pressure.

### Confirmation Dialog Fatigue
Norman advocates for error prevention, but naive application leads to confirmation dialogs on every action. Users habituate to clicking "OK" on every dialog, which means the confirmation for the actually-destructive action gets the same reflexive click. The better pattern is to make non-destructive actions immediate (no confirmation), destructive actions reversible (undo instead of confirmation), and truly irreversible actions require a qualitatively different interaction (typing the resource name to confirm deletion, not just clicking "OK").

### Overgeneralizing from Physical Product Examples
Many of Norman's iconic examples (doors, stove controls, faucets) are physical products. Digital interfaces have properties physical products lack: they can change dynamically, they can show and hide elements contextually, they can provide rich feedback at zero marginal cost, and they can offer undo. Translating DOET principles to digital design requires adaptation, not just direct application.

### Designing for the Happy Path Only
Norman's error chapter is one of the most practically important in the book, yet many designers internalize the affordance/signifier vocabulary and skip the error design. In practice, error states, edge cases, and recovery paths are where most usability failures live — and where DOET's slip vs. mistake framework pays its highest dividends.

---

## Applicability by Task Type

### UI / Component Design
**Relevance: Very High.** Every component should pass the signifier test (can the user tell it is interactive and what it does?), the feedback test (does the component communicate its state changes?), and the mapping test (is the component located near the thing it affects?). Norman's principles are the quality gate for any component library review.

Concrete checkpoints:
- Does each interactive element have a distinct visual signifier in all states (default, hover, active, disabled, focused)?
- Do state changes produce immediate, perceivable feedback?
- Are related controls grouped spatially near the content they affect?
- Do constraints (disabled states, input masks, allowed values) prevent slips before they happen?

### Feature Design (User Flow)
**Relevance: Very High.** The seven stages of action model is the primary diagnostic for user flows. Walk through each stage for the target user: Can they form the right goal from what they see? Can they figure out what action to take? Can they perform it? Can they tell what happened? Can they tell if they succeeded?

Concrete checkpoints:
- Does the entry point to the flow have a clear signifier and label? (Stages 2-3)
- Does each step provide enough context to choose the right next action? (Stage 3)
- Does each transition provide feedback that confirms the action was received? (Stage 5)
- Does the completion state clearly communicate success or failure? (Stages 6-7)
- Are error states designed with the slip vs. mistake taxonomy — prevention for slips, better models for mistakes?

### Error Handling Design (User-Facing)
**Relevance: Central — this is the book's strongest direct application.** Norman's slip vs. mistake taxonomy, combined with the seven stages of action, provides a complete framework for designing error experiences.

Concrete checkpoints:
- **Slip prevention:** Undo for accidental actions, spatial separation of destructive and routine buttons, confirmation for irreversible operations only
- **Mistake prevention:** Clear system state visibility, good conceptual models communicated through the interface, preview/dry-run capabilities
- **Error messages:** Identify what went wrong (Stage 5 — perceive), explain why (Stage 6 — interpret), and suggest what to do next (Stage 7 — compare/plan next action)
- **Recovery:** Every error state should have a clear path back to a good state. "Something went wrong — try again later" with no recourse is a design failure by Norman's standards.

### Usability Review
**Relevance: Very High — DOET provides the primary heuristic framework.** Norman's principles directly inform Nielsen's 10 Usability Heuristics (Nielsen was Norman's collaborator), which are the industry standard for heuristic evaluation. A DOET-informed usability review checks:

1. Visibility of system status (feedback)
2. Match between system and real world (conceptual models)
3. User control and freedom (undo, escape hatches)
4. Consistency and standards (conventions, constraints)
5. Error prevention (slips and mistakes)
6. Recognition rather than recall (knowledge in the world)
7. Flexibility and efficiency of use (novice/expert balance)
8. Aesthetic and minimalist design (signal-to-noise)
9. Help users recognize, diagnose, and recover from errors (Gulf of Evaluation)
10. Help and documentation (last resort, not first)

### Information Architecture
**Relevance: Moderate.** DOET's principles of natural mapping, logical constraints, and knowledge in the world apply to IA, but the book does not address IA specifically. The applicable principles: navigation should provide signifiers for what lies within each category (not just labels — communicate the conceptual model of the information space). Hierarchy should reflect the user's mental model, not the organization's internal structure. Grouping should follow logical constraints so that items have an obvious "home."

For deeper IA work, supplement DOET with dedicated IA resources (Rosenfeld and Morville's *Information Architecture*, card sorting techniques, tree testing).

---

## Relationship to Other Books in This Category

### Complementary Works

**"Don't Make Me Think" by Steve Krug (2000/2014):**
Krug is the practitioner's field guide to the same territory Norman maps theoretically. Where Norman explains *why* users behave as they do (cognitive psychology, mental models, stages of action), Krug shows *what to do about it* in web interfaces (visual hierarchy, navigation conventions, usability testing on a budget). Read Norman for the mental framework, Krug for the rapid-fire application to web and mobile.

**"About Face" by Alan Cooper (2014, 4th edition):**
Cooper's goal-directed design methodology is a direct descendant of Norman's human-centered design process but extends it with detailed techniques for persona development, interaction patterns, and design principles for complex applications. Where Norman gives you the vocabulary (affordances, signifiers, feedback), Cooper gives you the methodology for applying that vocabulary to a real product design process.

**"Emotional Design" by Don Norman (2004):**
Norman's own sequel addresses a gap in DOET: the role of emotion in design. DOET focuses on cognition (can the user figure it out?). Emotional Design adds three levels of processing: visceral (immediate aesthetic response), behavioral (pleasure of use), and reflective (meaning and self-image). Together, the two books argue that good design must work at both the cognitive and emotional levels.

**"Designing Interfaces" by Jenifer Tidwell et al. (3rd edition, 2020):**
A pattern library for UI design that puts Norman's principles into concrete, reusable patterns. Where Norman explains why a good form needs feedback and constraints, Tidwell catalogs specific patterns for achieving that (input hints, inline validation, forgiving formats, good defaults).

**"The Inmates Are Running the Asylum" by Alan Cooper (1999):**
Cooper's earlier polemic shares Norman's core thesis — that technology products fail because they are designed by engineers for engineers, not for the humans who use them — and pushes it into stronger organizational prescriptions. A useful companion for Chapter 7 of DOET.

### Contrasting Perspectives

**"Lean UX" by Jeff Gothelf and Josh Seiden (2013/2021):**
Lean UX de-emphasizes upfront design rigor (detailed signifier audits, thorough conceptual model work) in favor of rapid experimentation and validated learning. There is tension with Norman's thoroughness: Norman would argue that shipping a poorly-thought-through design and "learning from data" imposes unnecessary confusion on users. Lean UX would counter that shipping nothing while perfecting the design is worse. The mature position: use Norman's principles as design heuristics during rapid iteration, not as gates that block shipping.

**"Hooked" by Nir Eyal (2014):**
Eyal's habit-forming design framework can conflict with Norman's human-centered ethos. Norman designs *for* the user; Eyal designs to *retain* the user. Variable rewards and investment loops (Eyal's toolkit) can exploit the same cognitive patterns Norman aims to respect. Reading both creates a productive tension about design ethics.

---

## Freshness Assessment

**Original publication:** 1988 (as *The Psychology of Everyday Things*)
**Revised edition:** 2013 (Basic Books, Revised & Expanded)
**Core principles freshness:** Evergreen. Affordances, signifiers, feedback, conceptual models, the seven stages of action, and the slip/mistake taxonomy are grounded in cognitive psychology that has not changed. These concepts remain the foundational vocabulary of the entire UX field.

**Examples and technology references:** The 2013 revision updated examples for the smartphone era but some now feel dated (references to early smartphone interfaces, pre-voice-UI interactions). This does not affect the utility of the principles — only the illustrative examples need mental translation.

**What has evolved since 2013:**
- **Gesture-based and voice interfaces** have made signifier design harder. Norman's framework still applies but "signifier" in a voice interface is a prompt, a sound cue, or a conversational pattern — not a visual element.
- **AI-driven adaptive interfaces** create new challenges for conceptual models. When the interface changes behavior based on machine learning, the user's conceptual model may be constantly invalidated. Norman's framework highlights this as a serious problem but does not provide solutions for it.
- **Design systems and component libraries** have operationalized many of Norman's principles at the system level. Material Design, Apple's Human Interface Guidelines, and similar systems embed signifier consistency, mapping conventions, and feedback patterns into reusable components.
- **Dark patterns** have emerged as a major concern. Norman's framework is useful for diagnosing dark patterns — they deliberately exploit Gulf of Execution confusion or sabotage signifiers to trick users. The framework does not, however, address the organizational incentive structures that produce dark patterns.

**Bottom line:** The 2013 edition remains essential reading. No subsequent book has replaced it as the foundational text for understanding *why* design works or fails at the cognitive level. Supplement with contemporary pattern libraries and design system documentation for *how* to implement the principles in current technology stacks.

---

## Key Framings Worth Preserving

> **"When you have trouble with things — whether it's figuring out whether to push or pull a door, or the arbitrary, meaningless, and confusing way of turning on modern stove tops — it's not your fault. Don't blame yourself: blame the designer."**

This is the founding ethic of user-centered design. In an AI-assisted coding context, this translates to: when a user struggles with your interface, the debugging target is the design, not the user. Every support ticket is a design signal.

> **"Affordances define what actions are possible. Signifiers specify how people discover those possibilities."**

The single most important distinction in the book. Use this as a two-part checklist for every interactive element: (1) Does the affordance exist? (Can the user actually perform this action?) (2) Is there a signifier? (Can the user *perceive* that the action is possible and *how* to perform it?)

> **"The Gulf of Execution: the gap between the user's intentions and the allowable actions. The Gulf of Evaluation: the gap between the physical state of the system and the user's expectations and goals."**

Two diagnostic questions that apply to any usability problem: "Can the user figure out what to do?" (execution) and "Can the user figure out what happened?" (evaluation). If you can only remember two things from DOET for a usability review, remember these two gulfs.

> **"Two types of errors: slips and mistakes. Slips result from automatic behavior when subconscious actions are misdirected. Mistakes result from conscious deliberations."**

This reframes the entire approach to error handling. For slips: add guardrails, undo, and constraints. For mistakes: improve the conceptual model, make system state visible, and support exploration. Treating all errors the same way (confirmation dialogs everywhere, or better error messages everywhere) misses the structural difference.

> **"Design is really an act of communication, which means having a deep understanding of the person with whom the designer is communicating."**

The foundation of human-centered design in one sentence. In an AI-assisted workflow, this means the agent should always ask "who is the user and what do they already understand?" before generating any interface. A design for a developer-facing admin tool and a design for a consumer onboarding flow should look fundamentally different, even if they accomplish similar functions.

> **"Good design requires good observation. The hardest part of design is getting the requirements right, which means ensuring that the right problem is being solved."**

Norman's strongest argument against jumping to solutions. The double diamond: first find the right problem, then find the right solution. In a vibe-coding workflow, this maps to: before generating UI code, verify that the stated requirement actually matches the user's real need. The most elegant implementation of the wrong feature is still a failure.

> **"Complexity is in the world; it is simplicity we must seek in the head."**

This corrects the common misreading that Norman advocates simple products. He advocates simple *interactions with* complex products. The tax code is complex; the interface to file taxes should make that complexity manageable. The distinction matters because "make it simpler" often becomes "remove features," which Norman would reject if those features serve real user needs.
