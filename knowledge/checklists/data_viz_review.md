---
task: data_viz_review
description: Review or design data visualizations for clarity, accuracy, and storytelling effectiveness
primary_sources: ["26", "27", "28"]
secondary_sources: ["23", "24", "25"]
version: 1
updated: 2026-02-22
---

# Data Visualization Review Checklist

## Phase 1: Message & Context

- [ ] Articulate the Big Idea in one sentence: your point of view + what is at stake + a complete thought — if you cannot do this, you are not ready to build a chart [26]
- [ ] Identify the audience and what action you need them to take — data visualization is persuasive communication, not data reporting [26]
- [ ] Distinguish between exploratory analysis (understanding data) and explanatory communication (presenting findings) — they require different approaches and different charts [26]
- [ ] Write the 3-Minute Story: if you only had three minutes to explain your findings, what would you say? [26]
- [ ] Verify the chart title is an action title stating the takeaway, not a topic label — "Southeast revenue declined 15%" not "Revenue by Region" [26]

## Phase 2: Chart Type Selection

- [ ] Match the data type to the correct chart type — the data dictates the chart, not preference or familiarity [28]
- [ ] Use line charts for time series (never bar charts for continuous temporal data) [26][28]
- [ ] Use horizontal bar charts for categorical comparisons — they are easier to label and read than vertical bars [26][28]
- [ ] Use simple text for 1-2 data points — often the best choice when you have a single KPI [26]
- [ ] Avoid pie charts — humans are bad at judging angles; horizontal bar charts communicate the same data more accurately [26][27]
- [ ] Avoid secondary y-axes — they are arbitrary and misleading; use two separate charts instead [26][28]
- [ ] Avoid 3D charts — they add no information and distort perception through foreshortening and occlusion [27][28]
- [ ] For comparing distributions across many categories, consider ridgeline plots, violin plots, or small multiples instead of overlaid spaghetti lines [28]
- [ ] When in doubt about a bivariate relationship, start with a scatterplot — it is the most honest, least distorting representation [28]

## Phase 3: Declutter & Data-Ink

- [ ] Maximize the data-ink ratio: every bit of ink should present new information — if removing an element does not change the reader's understanding, remove it [27]
- [ ] Remove chart borders, reduce or eliminate gridlines, remove data markers unless they serve a specific purpose [26][27]
- [ ] Replace legends with direct labeling on the data — every legend is a failure of direct labeling [26][28]
- [ ] Remove excessive decimal places, rotated text, and diagonal axis labels [26]
- [ ] Use white space strategically — it is not wasted space; it reduces cognitive load [26]
- [ ] Check the Lie Factor: `(Size of effect in graphic) / (Size of effect in data)` should equal 1.0 — distortions arise from area/volume encodings, truncated axes, and inconsistent scales [27]
- [ ] Bar charts must start at zero (they encode values as length); line charts may zoom into a region of interest (they encode values as position) [28]
- [ ] Verify area encodings are proportional to data values, not radius or side length — a common source of visual exaggeration [28]

## Phase 4: Color & Attention

- [ ] Apply the gray + one accent color strategy: default everything to gray, use a single strong color to highlight the key data point or series [26]
- [ ] Identify which of the three uses of color applies: distinguish (qualitative palette), represent values (sequential palette), or highlight (accent palette) [28]
- [ ] For sequential palettes, verify they work in grayscale — luminance must vary monotonically [28]
- [ ] For qualitative palettes, use the Okabe-Ito palette or a colorblind-safe alternative; limit to 5-8 colors [28]
- [ ] Never encode critical information using only the red-green contrast — ~8% of men have color vision deficiency [28]
- [ ] Use redundant encoding (color + shape, color + direct labels) so color is never the only channel [28]
- [ ] If more than 5-8 categories need distinguishing in one chart, switch to small multiples or highlight only 2-3 categories of interest and gray out the rest [28]
- [ ] Use preattentive attributes (color, size, position, bold, enclosure) strategically to direct the viewer's eye — if nothing draws attention, you have not focused the chart [26]

## Phase 5: UX & Comprehension

- [ ] Design for scanning, not reading — use visual hierarchy, conventions, and clearly defined areas [24]
- [ ] Walk through the Seven Stages of Action for the chart reader: Can they form the right goal? Figure out where to look? Tell what the data shows? Tell if the takeaway is correct? [23]
- [ ] Verify every interactive element (tooltip, filter, drill-down) has a clear signifier — the user must be able to tell what is clickable [23]
- [ ] Apply Hick's Law: minimize choices at any single decision point in dashboards; break complex filter selections into progressive steps [25]
- [ ] Apply Fitts's Law: primary action buttons (export, refresh) should be large and easily reachable; destructive actions should be smaller and further away [25]
- [ ] Check for natural mapping: controls are grouped near the charts they affect [23]
- [ ] Ensure immediate, informative feedback at every interaction — hover states, loading indicators, empty-state messages [23]
- [ ] For presentations, use progressive disclosure: build up complex charts incrementally rather than showing everything at once [26]

## Phase 6: Narrative & Integration

- [ ] Structure the presentation as a narrative arc: Beginning (setting + conflict) -> Middle (data evidence) -> End (resolution + call to action) [26]
- [ ] Apply the horizontal logic test: read only the slide titles in sequence — do they tell a coherent story? [26]
- [ ] Apply the vertical logic test: does each individual slide stand on its own — does the title match the chart below? [26]
- [ ] Add annotations and callouts pointing out the key insight when the takeaway is not immediately obvious [26]
- [ ] For dashboards with multiple charts, maintain consistent color encoding, axis scales, and layout patterns across all panels [28]
- [ ] Use small multiples (faceting) instead of complex single-panel figures when comparing across many categories [27][28]
- [ ] Apply the shrink test: if the chart can be shrunk considerably without losing legibility, it is well-designed [27]

---

## Key Questions to Ask

1. "What is the Big Idea — in one sentence, what should the audience know or do?" [26]
2. "Would removing this element change the reader's understanding?" — if not, remove it [27]
3. "Where are your eyes drawn? If the answer is 'nowhere in particular,' you have not done enough to focus attention" [26]
4. "Is this ugly, bad, or wrong?" — classify the problem correctly before fixing it; wrong takes priority [28]
5. "Does this chart show the data, or show what the data means?" — aim for meaning [26]
6. "Is the lie factor 1.0? Does the visual encoding faithfully represent the data proportions?" [27]
7. "Would a colorblind viewer be able to read this chart?" — test with simulation tools [28]
8. "Would this chart survive the 3-Minute Story test — can I explain the takeaway in plain language?" [26]
9. "Can the audience tell what happened and whether it matters?" — the Gulf of Evaluation applied to charts [23]
10. "Is the chart type dictated by the data type, or by habit?" [28]

---

## Anti-Patterns to Flag

| Anti-Pattern | Signal | Source |
|---|---|---|
| **Data dump** | Chart shows all the data with no message, no emphasis, no action title — exploratory analysis presented as explanatory communication | [26] |
| **Pie chart for precision** | Using pie or donut charts when the audience needs to compare exact values across categories | [26][27] |
| **Spaghetti chart** | Too many overlapping lines on one chart — impossible to trace any individual series | [26][28] |
| **Chartjunk** | 3D effects, decorative fills, heavy borders, moiré patterns, or pictorial elements that obscure data | [27] |
| **Rainbow colormap** | Using the jet/rainbow palette — perceptually non-uniform, colorblind-hostile, creates artificial visual boundaries | [28] |
| **Truncated bar chart** | Bar chart with y-axis not starting at zero — visually exaggerates differences because bars encode length | [27][28] |
| **Legend-dependent reading** | Forcing the reader to look back and forth between data and a separate legend instead of labeling directly | [26][28] |
| **Dual y-axis** | Two different y-axes on the same chart — arbitrary alignment suggests false correlations | [28] |
| **Topic title** | Slide title says "Q3 Sales" instead of "Q3 Sales Declined 15% in the Southeast" — no takeaway for the audience | [26] |
| **Color-only encoding** | Information conveyed solely through color without redundant shape, label, or pattern — fails for colorblind viewers | [28] |
| **Overplotted scatter** | Thousands of overlapping dots with no transparency, jitter, or density encoding — obscures the data distribution | [28] |
| **Kitchen-sink dashboard** | Dashboard with 15+ charts, no visual hierarchy, no shared color system, and no clear narrative — audience cannot find the signal | [24][26] |
