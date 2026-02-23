---
task: product_doc
description: Write or review product documentation, specs, and PRDs
primary_sources: ["29", "30", "31"]
secondary_sources: ["23", "24", "26"]
anthropic_articles: []
version: 1
updated: 2026-02-22
---

# Product Documentation Checklist

## Phase 1: Problem & Audience Clarity

- [ ] Identify the specific audience and what action you need them to take — "leadership" is too vague; name the role and the decision [29]
- [ ] Articulate the customer problem using customer-centric framing, not business jargon — "users struggle to X" not "we need to build Y" [31]
- [ ] Apply the Opportunity Assessment: what business objective, how will you measure success, what problem for customers, which customer segment? [29]
- [ ] Frame opportunities as customer needs/pain points/desires, not as features or internal goals [31]
- [ ] Confirm the document has a single "Big Idea" — one sentence capturing point of view, what is at stake, and a complete thought [26]
- [ ] Verify the stated problem was discovered through actual customer contact (interviews, data), not assumed from stakeholder requests [31]

## Phase 2: Solution Shaping & Scope

- [ ] Set an appetite before describing the solution — "how much time is this worth?" not "how long will it take?" [30]
- [ ] Describe the solution at the right abstraction level: specific enough to be buildable, rough enough to leave room for builders [30]
- [ ] Include explicit no-gos — things deliberately out of scope for this appetite [30]
- [ ] Catalog known rabbit holes and technical risks that could derail the project, with mitigation strategies [30]
- [ ] Ensure at least three solution alternatives were considered before selecting the one documented — avoid first-idea bias [31]
- [ ] Address all four risk categories: value (will they use it?), usability (can they use it?), feasibility (can we build it?), viability (does it work for the business?) [29]
- [ ] Verify the scope follows fixed-time/variable-scope thinking — core must-haves are non-negotiable, nice-to-haves are explicitly marked as cuttable [30]

## Phase 3: Success Metrics & Outcomes

- [ ] Define success as an outcome (measurable change in behavior or business result), not an output (feature shipped) [29]
- [ ] Specify concrete key results with numbers — "increase 7-day retention by 5%" not "improve retention" [29]
- [ ] Include the assumption map: which assumptions are high-importance/low-evidence and need testing before full build? [31]
- [ ] Identify the riskiest assumption and the smallest experiment that could test it [31]
- [ ] Ensure metrics are ones the team can actually influence — avoid vanity metrics disconnected from the team's work [29]

## Phase 4: Communication & Visual Clarity

- [ ] Use action titles for any charts or data sections — "Southeast revenue declined 15%" not "Revenue by Region" [26]
- [ ] Apply the "don't make me think" test: can a reader scanning this doc understand the key points in under 60 seconds? [24]
- [ ] Eliminate happy talk — remove self-congratulatory or filler text that no one reads [24]
- [ ] Structure the document for scanning: clear visual hierarchy, defined sections, bold key terms [24]
- [ ] Ensure any data visuals use the gray-plus-accent-color strategy to focus attention on what matters [26]
- [ ] Check that the system image (terminology, structure, flow) communicates a coherent conceptual model a reader can follow [23]

## Phase 5: Stakeholder Alignment

- [ ] Share problems and objectives with stakeholders, not just proposed solutions [29]
- [ ] Include discovery evidence (user quotes, prototype test outcomes, data) to build stakeholder confidence [29]
- [ ] Apply horizontal logic: if you read only the section headings in sequence, do they tell a coherent story? [26]
- [ ] Apply vertical logic: does each section stand on its own — does the heading match the content below? [26]
- [ ] Verify the document distinguishes between stakeholder needs (business viability) and customer needs (value/usability) [29]

## Phase 6: Review & Iteration

- [ ] Run the Trunk Test on the document: can a reader on any page identify what doc this is, where they are, and what their options are? [24]
- [ ] Verify signifiers are clear — every link, button reference, or action item in the doc is unambiguous [23]
- [ ] Check for the feature factory anti-pattern: is this doc framed around outcomes to achieve, or features to ship? [29]
- [ ] Confirm the doc can serve as effective context for a builder — it provides problem, constraints, and solution direction without over-specifying implementation [30]
- [ ] Ensure the Opportunity Solution Tree is referenced or implied: the doc traces from outcome to opportunity to solution [31]

---

## Key Questions to Ask

1. "What business objective does this address, and how will we know if we succeeded?" — Forces clarity before effort [29]
2. "How much time is this worth?" — The appetite question prevents gold-plating and forces scope tradeoffs [30]
3. "What is the riskiest assumption, and how will we test it before committing to build?" — The assumption test [31]
4. "If we only had three minutes to explain this to the audience, what would we say?" — The 3-Minute Story test for message clarity [26]
5. "Will the reader have to think about what to do with this information?" — The usability test for docs [24]
6. "What are we explicitly NOT doing, and why?" — Forces honest scope conversations [30]
7. "Is this doc framed around the customer's problem or the team's solution?" — Catches solution-first thinking [31]
8. "What happens if the reader only scans the headings?" — The horizontal logic test [26]
9. "What mental model will the reader form from this structure?" — The conceptual model test [23]
10. "Have we fallen in love with the solution instead of the problem?" — The discovery discipline check [29]

---

## Anti-Patterns to Flag

| Anti-Pattern | Signal | Source |
|---|---|---|
| **Feature factory doc** | Document lists features to ship with no stated outcome or success metric | [29] |
| **Solution-first framing** | Jumps to "we need to build X" without articulating the customer problem | [31] |
| **Missing appetite** | No time budget or scope constraint — invites gold-plating and scope creep | [30] |
| **Discovery theater** | References user research but the solution was already committed on the roadmap | [29] |
| **Vague success metrics** | "Improve user experience" with no measurable key result | [29] |
| **Happy talk padding** | Self-congratulatory introductions that add words but no information | [24] |
| **Data dump** | Charts and tables with no action titles, no "so what," no narrative | [26] |
| **Over-specification** | Includes wireframes, database schemas, and step-by-step implementation — leaves builders no creative autonomy | [30] |
| **Under-specification** | A vague problem statement with no solution direction — disguised user story | [30] |
| **Stakeholder capture** | Document is a list of features dictated by stakeholders rather than discovered through customer research | [29][31] |
| **Missing error states** | Doc describes the happy path but not what happens when things go wrong | [23] |
| **Conceptual model mismatch** | Internal jargon and org-chart structure instead of user-mental-model structure | [23][24] |
