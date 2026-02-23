---
name: data-viz-review
description: >
  Systematic data visualization review and design using Storytelling with Data (Knaflic),
  The Visual Display of Quantitative Information (Tufte), Fundamentals of Data Visualization (Wilke),
  Design of Everyday Things, Don't Make Me Think, and Laws of UX.
  Use when reviewing charts, designing dashboards, or evaluating data presentations.
---

## When to Activate

- User asks to review or improve a chart, plot, or dashboard
- User needs help choosing the right chart type for their data
- User wants to design a data presentation or slide deck with visualizations
- User asks about color palettes, accessibility, or decluttering charts
- User is building a dashboard and wants layout or design guidance
- User asks about data storytelling or narrative structure for a presentation

## Procedure

1. Read `knowledge/checklists/data_viz_review.md`
2. Assess the visualization against each relevant checklist phase (message, chart type, declutter, color, UX, narrative)
3. For items needing deeper context, read the cited book file (e.g., `book_research/26_storytelling_with_data.md`)
4. Present findings organized as: **Message Clarity** -> **Chart Type Assessment** -> **Visual Design** -> **Narrative Structure**
5. Cite the source book/principle for each finding

## Always-Apply Principles

- "If you cannot articulate your Big Idea in a single sentence, you are not ready to build a chart" — context and message come before any tool [26: Storytelling with Data]
- Maximize the data-ink ratio within reason — every element should earn its place, but "within reason" matters [27: Visual Display of Quantitative Information]
- Color serves exactly three purposes: distinguish categories, represent data values, or highlight key points — if a color is not doing one of these, it should be gray [28: Fundamentals of Data Visualization]
- "A bar chart must start at zero; a line chart does not" — bars encode length (needs zero baseline), lines encode position (allows zooming) [28: Fundamentals of Data Visualization]
- Design for scanning, not reading — use visual hierarchy and the gray + accent color strategy to guide the eye instantly [24: Don't Make Me Think][26: Storytelling with Data]
- "Confusion and clutter are failures of design, not attributes of information" — when a chart is confusing, fix the design, not the data [27: Visual Display of Quantitative Information]

## Deep-Dive References

- Big Idea, declutter workflow, narrative arc, gray+accent color: `book_research/26_storytelling_with_data.md`
- Data-ink ratio, chartjunk, lie factor, small multiples: `book_research/27_visual_display_quantitative_info.md`
- Chart type selection, ugly/bad/wrong, three uses of color, color accessibility: `book_research/28_fundamentals_data_visualization.md`
- Affordances, signifiers, seven stages of action: `book_research/23_design_of_everyday_things.md`
- Scanning, visual hierarchy, conventions: `book_research/24_dont_make_me_think.md`
- Hick's Law, Fitts's Law, cognitive psychology for UI: `book_research/25_laws_of_ux.md`
