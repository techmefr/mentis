# chart-choice-pitfalls §1 — Distributions and lengths

Two groups can share a mean and a spread and still differ in shape. The first section is about the charts that
cannot show it, and about bars, whose length is the value.

## 1.1 Bar plots and comparing means
1. **A bar plot of means hides the distribution.** The source's example is two groups with similar means and
   standard deviations and quite different distributions; the question it asks of the bar plot is whether they
   are "really the same".
2. **The task decides the chart.** If the point is to show the mean and the spread across groups, show the
   observations themselves, with the mean and its dispersion beside them. The source recommends plotting every
   data point for small and moderate samples, with a beeswarm-style layout to avoid overlap (a technique of
   its own R ecosystem; any layout that separates overlapping points does the same job).
3. **The source says to check a couple of things before settling on a bar plot** without listing them. The
   obvious ones (the shape of each group, how many observations each has, whether a few extreme values drive the
   mean) are own guidance.

## 1.2 Small samples and smoothed shapes
1. **Violin plots and any smoothed distribution curve make little sense for small n**: shapes and quartiles
   vary widely between samples drawn from the same distribution, and they carry information only when n is
   large (source). Show the points instead.
2. **Histograms are not robust to the number of bins for small and even moderate samples.** Samples from the
   same distribution look different with different bin counts; only a fairly large sample gives a stable
   shape. For small samples, plot all points. The source's own cut-offs come from its simulations and are not
   carried here.
3. **Say how many observations stand behind each shape** next to the chart, so the reader can discount a
   smooth curve drawn over a handful of points (own guidance).

## 1.3 Boxplots and several modes
1. **A boxplot summarises with the median and quartiles, so it cannot show a bimodal or multi-modal
   distribution.** Look at the distribution before choosing it (source).
2. **When in doubt plot the points**, for small to moderate samples, since distribution-shaped graphics are
   unreliable at small n (source).

## 1.4 Length is not position
1. **A bar encodes its value as its length from the axis; a dot, a line or a boxplot encodes it as a
   position.** The source calls confusing the two the root of many misleading charts.
2. **A bar chart must start at zero.** Truncating the axis exaggerates the ratio between bars; the source's
   example makes one bar look about three times another when the true ratio of the means is about 1.6, an
   illustration from its own figure, not a general rule.
3. **A broken axis is acceptable for position-based charts but not for bars.** Moving the break changes how long
   bars look, so the same data can be made to look different. If the range is wide, the source's alternative is
   a logarithmic axis, or a position-based chart.

## 1.5 Multi-factor layouts
1. **A wall of bars covering every combination of factors does not communicate** (the source calls it a bar
   plot meadow). Group and facet by the factors of interest.
2. **The layout depends on the question.** Comparing the effect of one pair of factors at each level of a third
   needs a different arrangement from comparing another pair at each level of the first; choose the layout
   from the comparison, not the other way round (source).
3. **Check the data range at each factor level.** When the range of the response differs widely between levels
   (one compound has a much narrower range than the others), a shared axis hides a strong effect on the narrow
   one. Look at each level's range, or give each its own axis and say so (source).
