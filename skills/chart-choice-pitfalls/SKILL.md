---
name: chart-choice-pitfalls
description: "Use when a chart is chosen, drawn or reviewed and the encoding itself may mislead: bar plots used to compare means while hiding the distribution, bars that do not start at zero or have a broken axis, a diverging colour scale on one-directional data, heatmaps without row and column order or a capped colour scale, pie charts and concentric donuts instead of stacked bars, red and green or rainbow colour scales, unordered stacked bars, histograms and violins on small samples, boxplots over bimodal data, a chart palette reused for text, charts that are drawn well but wrong (correlation matrix, stacked area, waterfall, donut totals)."
---

# chart-choice-pitfalls

Not a step of the pipeline: a craft block for choosing what a chart encodes and checking that it says what the
data says. The two sections share one premise: **a chart is an argument made with position, length, angle and
colour, and the reader trusts whichever of those the chart type uses**, so the pitfalls are the choices that make
the eye read something the numbers do not contain. Dashboard layout, governance and metric definitions are in
`business/data-analytics`; contrast and keyboard access of the finished page are in `accessibility`; the
numbers behind a chart are checked with `analysis-validation-pitfalls`.

## When
- Choosing a chart type for a comparison, a distribution, a share of a whole or a matrix of values.
- Reviewing a figure before it goes in a report, a paper or a dashboard.
- Replacing a chart that "looks wrong" or that two readers read differently.
- Generating chart code, where the library's defaults decide the colour scale and the axis.

## Steps

**Read only the section the task meets.** They are independent.

| Ref | Covers | Read it when | File |
|---|---|---|---|
| 01 | Distributions and lengths: bar plots and mean separation, small samples, histograms, boxplots, zero baselines and broken axes, multi-factor layouts | values are compared across groups, or a bar or a distribution is drawn | [`01-distributions-and-lengths.md`](./references/01-distributions-and-lengths.md) |
| 02 | Colour, shares, matrices and correctness: colour scales, heatmaps, pie and donut, stacked bars, chart palettes, domain checks per chart type | colour carries values, a share of a whole is shown, or a chart type has a hidden consistency rule | [`02-colour-shares-and-correctness.md`](./references/02-colour-shares-and-correctness.md) |

## Output / checkpoint
A chart is done when someone can say, from the chart alone, which visual property carries the value (position,
length, angle or colour), what the zero or the neutral point of that property is, and what the chart would hide
if the data were different from the sample shown (a second mode, an outlier, a very small group). A review is
done when each finding names the chart, the property that misleads and the replacement. Read the figure once
looking for a bar that does not start at zero, a colour scale whose ends mean nothing, and a summary shape drawn
over a handful of points. Nothing here was verified with real data: the check is a read of the text.

## Guardrails
- Never use a bar for a value when the bar does not start at zero, and never break the axis of a bar chart
  (reference 01).
- Never summarise a small sample with a smoothed shape; show the points (reference 01).
- Never let a colour scale's lightest and darkest ends mean something arbitrary (reference 02).
- Never use red with green, or a rainbow scale, to carry values (reference 02).
- Never show a stacked bar and a comparison of means in the same panel (reference 02).
- Never call a chart finished before the consistency check of its type: symmetric matrices, bands that add up,
  a waterfall that closes, segments that total the whole (reference 02).
- The source is an opinionated essay, written from R and biology practice: take its encoding arguments, not
  its tooling or its worked numbers (both references).
- Numbers the author derived from his own simulations, and the share of men with colour blindness, are not
  carried; see the origin note.

## Origin
Rewritten from cxli233's FriendsDontLetFriends, `README.md` (MIT), and from plugin87's ux-ui-agent-skills,
the `data-dashboard` skill (MIT, partial read of the repository), read 2026-10-16. Both are one author's
practice and not consensus. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
