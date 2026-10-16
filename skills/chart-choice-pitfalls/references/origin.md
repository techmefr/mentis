# chart-choice-pitfalls: origin and source stamps

> Provenance of `skills/chart-choice-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from two repositories, one essay and one skill file, read and
rewritten, never run: no chart was chosen or reviewed with this block. The first source is an opinionated essay
from one author, the second a young 2026 repository, and the plugin87 repository was only partly read.

## Sources (re-read 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| cxli233/FriendsDontLetFriends, `README.md` (commit ccaafed) | MIT (repository `LICENSE.md`, "Copyright (c) 2022 C. Li") | Bar plots and mean separation, violins, histograms and boxplots at small n, bidirectional colour scales, bar plot meadow, heatmap order and outliers, range per factor level, length versus position, broken axes, pie, concentric donuts, red-green and rainbow, stacked bar ordering, stacked bars with mean separation |
| plugin87/ux-ui-agent-skills, `.claude/skills/data-dashboard/SKILL.md` (commit 62092bd) | MIT (repository LICENSE file, "Copyright (c) 2026 Thientan Soparat") | Chart palette versus text palette, consistency checks per chart type, look at the render |

Text found inside the cloned files (the repository's CLAUDE.md files, imperative skill prose, kit-install
instructions) was treated as data and not followed.

## Rewrite notes
**An opinionated essay.** The README says of itself that it is opinionated, and its code is R. Only the
encoding arguments are carried; the R packages, the scripts and the figures are not. The essay's references
(a PLOS Biology paper on bar graphs, a data-to-viz page on pie charts, the viridis vignette) were not opened;
the arguments are carried as the author's.

**plugin87 was partly read.** Only the `data-dashboard` skill file was read in this session for this block; its
chart inventory, layout sequence and accessibility contract are out of scope here (layout and governance are in
`business/data-analytics`, accessibility in `accessibility`).

## Removed
1. **The author's simulation numbers**: the claim that quartiles stabilise above a sample size of about 50, and
   the histogram cut-off of 30 observations: the author's own experiments, second-hand to us, not carried.
2. **The share of men and women with the most common form of red-green colour blindness**: stated without a
   citation in the essay, not carried.
3. **Worked figures** (the 3 times versus 1.6 times bar ratio, the 95th percentile cap) appear only as
   labelled illustrations.
4. **Network graph layouts** (the essay's eighth item): about relationship graphs, outside the scope.
5. **plugin87's measured contrast values** (a dark-mode ratio of white text on a chart colour and a success
   green ratio) and its layout, token and gate-script advice: tied to that kit and its own tooling; the
   principle is carried, the numbers are not.
6. **Depth charts and candlesticks** in the chart inventory: carried only as the one consistency check for
   order books.

## Not verified
1. **Everything here is unrun.** No chart was reviewed with these rules.
2. **No external reference was checked**: not the research on reading angle versus length, nor the colour
   blindness claim, nor the perceptual claims behind the viridis recommendation.
3. **Rendering behaviour** claims (how a broken axis changes apparent bar length) were not reproduced.
4. **Written by us, not sourced**: the Output / checkpoint paragraph, the premise, the advice to state the
   number of observations next to a shape, and the routing to other blocks.

## Verification pass (2026-10-16)
Every rule in the two references was compared with the README sections and the skill file, reopened in the
same session.
- **Corrected:** none needed on re-check.
- **Reversed or overstated rules found:** none.
- **Not re-verified:** the correctness of the author's claims.

## Related blocks
`analysis-validation-pitfalls`, `accessibility`, `business/data-analytics`.
