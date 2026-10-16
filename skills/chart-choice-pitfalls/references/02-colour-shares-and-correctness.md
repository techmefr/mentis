# chart-choice-pitfalls §2 — Colour, shares, matrices and correctness

Colour and angle are the weakest carriers of a value. Use them for it only with the checks below, and check the
internal consistency of each chart type before it is called finished.

## 2.1 Colour scales
1. **The ends of a numeric colour scale must mean something**: a maximum, a minimum, a mean, zero. The source
   treats a scale whose lightest or darkest colour is an arbitrary number as a serious error, as bad as the
   longest bar not being the largest value.
2. **Do not use a two-direction scale on one-direction data.** A diverging scale puts a neutral midpoint in
   the centre; on values that only go one way, that midpoint is arbitrary (source).
3. **Avoid red and green together, and rainbow scales.** Red and green shades at once are a problem for readers
   with red-green colour blindness, and both red-green and rainbow lose information when printed in grey. The
   source recommends perceptually uniform scales of the viridis family, which survive both. The source's
   figures on how common colour blindness is are second-hand and not carried.
4. **A chart palette is not a text palette.** The plugin87 skill warns that chart colours are tuned for large
   filled shapes; text set on a chart colour (initials in an avatar, a label on a bar) needs its own contrast
   check. Contrast thresholds are in `accessibility`.

## 2.2 Heatmaps
1. **Order the rows and columns.** Without ordering, a heatmap usually shows nothing useful; clustering is one
   way, not the only one. The exception is rows and columns that map to physical positions (the source's
   example is a 96-well plate), which must keep their places.
2. **Cap the colour scale against outliers.** One extreme value stretches the scale so that the rest look the
   same. The source's example caps near the 95th percentile of the data and then sees that two observations
   differ across all features. The percentile is the example's, not a rule; say where the cap is.
3. **Check the range at each factor level** before sharing one scale across levels (see reference 01).
4. **Apply the same care to any colour-coded numeric display** (source: it generalises beyond heatmaps).

## 2.3 Shares of a whole
1. **Prefer stacked bars to pie charts.** People read angle and area worse than length (the source points to
   the data-to-viz caveat page for this claim; that page was not read). A pie is hard to compare across groups;
   unwrapping a donut gives a stacked bar, which sits side by side.
2. **Concentric donuts mislead.** Outer rings have longer arcs for the same angle, so equal values look
   unequal and the ring order changes the impression. The value is carried by the angle, which readers judge
   poorly. Use a stacked bar (source).
3. **Reorder many stacked bars.** With many samples and classes the arrangement decides whether any pattern is
   visible; group and order the samples (source).
4. **Do not mix stacked bars with a mean comparison.** Proportions that add to 100 percent and a difference in
   means with dispersion are two different tasks; overlaying error bars and points on stacks makes it unclear
   what is compared and shifts the upper stacks so the axis cannot be read for them. Show the proportions as
   stacked bars, and the means in their own panel (source).

## 2.4 Consistency checks per chart type
The plugin87 skill states that automated checks cannot catch a chart that is drawn well and means nothing, so
the checks are done by hand and by looking at the render.
1. **A correlation matrix is symmetric** and its diagonal is exactly 1.
2. **A stacked area sums to the total**; the bands do not cross or leave gaps. The skill names the usual bug as
   reversing the baseline by index instead of by coordinate.
3. **A waterfall closes**: the final bar equals the opening value plus the steps, and connectors show the
   levels.
4. **A donut whose segments do not add up to the whole is a pie chart that lies** (skill's wording).
5. **A depth chart rises away from the midpoint on both sides** and never falls. This one is specific to order
   books and is carried only for that case.
6. **Look at the render.** The skill's point is that every automated gate can pass while the picture is wrong;
   open the chart and read it as its audience would.
