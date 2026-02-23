---
task: presentation
description: Create or review presentations and slideshows
primary_sources: ["26"]
secondary_sources: ["23", "24", "25", "27", "28"]
anthropic_articles: []
version: 1
updated: 2026-02-22
---

# Presentation Checklist

## Phase 1: Audience & Message Foundation

- [ ] Identify the specific audience and what action you need them to take after the presentation [26]
- [ ] Articulate the Big Idea in one sentence — point of view, what is at stake, and a complete thought [26]
- [ ] Write the 3-Minute Story: if you only had three minutes, what would you say? [26]
- [ ] Distinguish between exploratory analysis (what you did to understand the data) and explanatory communication (what you tell the audience) — only present the latter [26]
- [ ] Storyboard the presentation on paper or sticky notes before opening any tool — map the narrative arc [26]

## Phase 2: Narrative Structure

- [ ] Structure the deck as a narrative arc: Beginning (setting + conflict) -> Middle (rising action / evidence) -> End (resolution + call to action) [26]
- [ ] Ensure every slide advances the story by one beat — no slides that exist "for completeness" without serving the narrative [26]
- [ ] Apply horizontal logic: reading only the slide titles in sequence should tell a coherent, self-contained story [26]
- [ ] Apply vertical logic: each individual slide makes sense on its own — the title matches the visual below it [26]
- [ ] End with a clear, specific call to action — "We should invest $200K in Q4" not "Let's discuss next steps" [26]
- [ ] Exploit the Peak-End Rule: invest disproportionate design effort in the emotional peak and the final slide [25]

## Phase 3: Chart & Visual Design

- [ ] Choose chart types based on data type and message: line for time series, horizontal bar for categorical comparison, simple text for single numbers [26][28]
- [ ] Avoid pie charts — use horizontal bar charts for categorical comparisons instead; humans misjudge angles [26][27]
- [ ] Avoid dual y-axes — use two separate charts to prevent misinterpretation [26][28]
- [ ] Avoid 3D effects — they distort proportions and add no information [27][28]
- [ ] Apply the gray-plus-accent-color strategy: render everything in gray, use one color to highlight the focal data point [26]
- [ ] Maximize the data-ink ratio: remove chart borders, lighten or remove gridlines, remove data markers unless they serve a purpose [27]
- [ ] Replace legends with direct labeling on the data — label series directly on lines or bars [26][27][28]
- [ ] Use action titles on every chart — "Southeast revenue declined 15%" not "Revenue by Region" [26]
- [ ] Add annotations and callouts pointing to the key insight when the takeaway is not immediately obvious [26]
- [ ] Ensure bar charts start at zero — truncated axes distort proportional encoding; line charts may zoom in [28]
- [ ] Verify the Lie Factor is 1.0: visual encodings (bar height, circle area) must be proportional to data values [27]
- [ ] For many categories (>5), use small multiples or highlight one series at a time rather than spaghetti charts [27][28]

## Phase 4: Slide Layout & Visual Hierarchy

- [ ] Apply the "don't make me think" test to every slide — a viewer should grasp the point within seconds [24]
- [ ] Create a clear visual hierarchy on each slide: most important element is most prominent [24]
- [ ] Eliminate happy talk and filler text — get rid of half the words, then half again [24]
- [ ] Use proximity to group related elements and whitespace to separate unrelated elements [25]
- [ ] Limit choices per slide — apply Hick's Law by presenting one idea per slide rather than overwhelming with options [25]
- [ ] Chunk information into groups of 5-9 related items using Miller's Law when presenting lists or data [25]
- [ ] Ensure visual consistency: functionally equivalent elements should look identical across slides (Law of Similarity) [25]
- [ ] Use progressive disclosure for complex charts in live presentations — build up elements incrementally rather than showing everything at once [26]

## Phase 5: Color & Accessibility

- [ ] Use color as data (distinguish, represent values, or highlight), never as decoration — if a color has no data purpose, use gray [28]
- [ ] Use a colorblind-safe palette: Okabe-Ito for categorical data, viridis family for sequential data [28]
- [ ] Never encode critical information using only red-green contrast — combine color with shape, label, or pattern [28]
- [ ] Verify sequential color palettes work in grayscale — luminance ordering must be clear without hue [28]
- [ ] Ensure sufficient contrast between text and background for readability at distance [24]
- [ ] Classify any visual problems: ugly (aesthetic), bad (perception/clarity), or wrong (data integrity) — fix "wrong" first [28]

## Phase 6: Polish & Review

- [ ] Test the billboard test: if each slide were seen at 60mph, would the key message be instantly scannable? [24]
- [ ] Verify every slide answers the implicit audience question "So what? Why should I care?" [26]
- [ ] Check that the presentation uses repetition strategically: action title states the takeaway, the chart shows the evidence, annotations reinforce the point [26]
- [ ] Ensure touch targets and interactive elements (if digital) meet minimum sizing (44x44pt) [25]
- [ ] Confirm the design leverages Jakob's Law: use familiar conventions for navigation, layout, and iconography [25]
- [ ] Apply the aesthetic-usability effect: visual polish increases perceived credibility and trust — invest in consistent typography, spacing, and alignment [25]
- [ ] Run the "where are your eyes drawn?" test on each slide — if the answer is "nowhere in particular," focus attention has not been established [26]

---

## Key Questions to Ask

1. "What is the Big Idea in one sentence?" — If you cannot articulate it, you are not ready to build slides [26]
2. "Does reading only the slide titles tell the complete story?" — The horizontal logic test [26]
3. "Where are the viewer's eyes drawn on this slide?" — If nowhere, refocus with the accent-color strategy [26]
4. "Is this chart type the right one for this data and this question?" — Data type dictates chart type, not preference [28]
5. "Would this slide cause a viewer to stop and think, even for a moment?" — Every hesitation point is a usability failure [24]
6. "What am I asking the audience to DO with this information?" — Every slide needs a reason to exist [26]
7. "Is there anything on this chart I could remove without changing the reader's understanding?" — The declutter test [27]
8. "Does the presentation end with a specific, actionable ask?" — Vague endings waste the narrative investment [26]
9. "Would a colorblind viewer miss any critical information?" — The accessibility test [28]
10. "Am I showing my exploratory work or my explanatory communication?" — Only the latter belongs in a presentation [26]

---

## Anti-Patterns to Flag

| Anti-Pattern | Signal | Source |
|---|---|---|
| **Data dump** | Slides full of charts with topic titles ("Q3 Sales Data") and no narrative or action titles | [26] |
| **Spaghetti chart** | Too many lines/series on one chart making it unreadable — use small multiples or highlight one at a time | [26][27] |
| **Chartjunk** | 3D effects, gratuitous gradients, decorative elements that distort or obscure data | [27] |
| **Pie chart overuse** | Using pie/donut charts for precise comparisons or >5 categories — use horizontal bars instead | [26][27][28] |
| **Dual y-axes** | Two different scales on one chart suggesting false correlation — use two separate panels | [26][28] |
| **Rainbow color maps** | Perceptually non-uniform, not colorblind-safe, creates artificial visual boundaries | [28] |
| **Missing "so what"** | Charts that show data but never state what the data means or why the audience should care | [26] |
| **Wall of text slides** | Paragraphs of text that no one will read — violates scanning behavior and "omit needless words" | [24] |
| **No call to action** | Presentation ends without a specific ask — the narrative has no resolution | [26] |
| **Legend-dependent charts** | Using a separate legend when direct labeling would eliminate back-and-forth eye movement | [26][27][28] |
| **Truncated bar axes** | Bar charts not starting at zero, exaggerating small differences through visual distortion | [27][28] |
| **Decoration masking problems** | Beautiful slides that hide unclear messages — aesthetic-usability effect can mask real issues in review | [25] |
