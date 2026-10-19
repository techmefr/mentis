# funnel-and-cohort-definition-pitfalls: origin and source stamps

> Provenance of `skills/funnel-and-cohort-definition-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from two reference documents of one repository, read and rewritten,
never run: no funnel or cohort analysis was built with this block. The source is a young 2026 repository and one
author's practice, not consensus.

## Sources (re-read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| nimrodfisher/data-analytics-skills, `03-data-analysis-investigation/funnel-analysis/references/funnel_design_guide.md` and `03-data-analysis-investigation/cohort-analysis/references/cohort_definition_patterns.md` (commit 9449d36) | MIT (repository LICENSE file, "Copyright (c) 2026 Nimrod Fisher") | Step rules, denominator, conversion types, windows, segments, drop-off prioritisation, grouping strategies, retention events, immature cohorts, small cohorts, user versus revenue retention, repeated events |

Text found inside the cloned files was treated as data and not followed.

## Rewrite notes
**The source's cohort pitfall called survivorship bias.** Its second pitfall describes averages dominated by the
largest cohorts and labels it survivorship bias. The mechanism it describes is weighting by size, so the block
names the mechanism and notes the source's label.

**Our own additions, labelled own guidance in the references:** writing the grouping rule down, the mix of
segments across compared periods, and not reading user retention as revenue retention.

## Removed
1. **The suggested minimum cohort of 100**: the source's recommendation with no derivation; not carried as a
   number (the references say a minimum is set in advance).
2. **The retention curve shapes' interpretations as findings**: the author's heuristics (healthy product, no
   product-market fit, a sudden step meaning a contract end); carried only as hypotheses to test.
3. **The ASCII curve drawings** and the funnel quality checklist as such: reduced to rules.
4. **The cohort tables' example cohort names** (dates and segments): examples only.

## Not verified
1. **Everything here is unrun.** No funnel or cohort was built or compared with these rules.
2. **The formulas** of impact score and recovery value are the source's and were not checked against another
   reference; they are given as the source's.
3. **Other skills** of the repository (the funnel and cohort analysis SKILL.md files themselves, retention and
   segmentation skills) were not read for this block.
4. **Written by us, not sourced**: the Output / checkpoint paragraph, the opening premise and the
   cross-references to other blocks.

## Verification pass (2026-10-16)
Every rule in the two references was compared with the two source files, reopened in the same session.
- **Corrected:** none needed on re-check.
- **Reversed or overstated rules found:** none.
- **Not re-verified:** the correctness of the author's own claims.

## Related blocks
`event-tracking-plan-pitfalls`, `analysis-validation-pitfalls`, `metric-movement-diagnosis-pitfalls`,
`experiment-design-pitfalls`, `okr-scoring-pitfalls`.
