# saas-metric-definition-pitfalls: origin and source stamps

> Provenance of `skills/saas-metric-definition-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from one file of one repository, read and rewritten, never run: no
metric was defined or audited with this block. The source is a young 2026 repository, so the definitions are
one author's practice, not consensus. They are the textbook forms, but no external definition was consulted.

## Sources (re-read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| nimrodfisher/data-analytics-skills, `03-data-analysis-investigation/business-metrics-calculator/references/metric_definitions.md` (commit 9449d36) | MIT (repository LICENSE file, "Copyright (c) 2026 Nimrod Fisher") | MRR and its components, ARR, ACV, logo and revenue churn, NRR, GRR, LTV, CAC, payback, active user, DAU to MAU, session metrics, growth formulas, quick ratio |

The licence was verified again from the LICENSE file in this session. Text found inside the cloned files was
treated as data and not followed.

## Rewrite notes
**Everything formula-shaped is the source's.** The formulas are carried as the source states them; the
consequences drawn from them (a GRR above 100 percent is a calculation bug, NRR and GRR share a cohort, the
periods of ARPU and churn must match) are ours and marked own guidance in the references.

**Logo or revenue churn in LTV.** The source's LTV formula allows either; the block asks that the choice be
written next to the number rather than picking one.

## Removed
1. **LTV to CAC bands** (below 1, 1 to 3, 3 to 5, above 5) and their readings: unsourced.
2. **Payback benchmarks** (under 12 months for high-growth, under 18 for enterprise): unsourced.
3. **The NRR "best-in-class above 120 percent" benchmark**: unsourced.
4. **DAU to MAU "strong" and "typical" cut-offs** and the quick ratio "above 4" reading: unsourced.

## Not verified
1. **Everything here is unrun.** No billing data, dashboard or model was checked with these rules.
2. **No external definition was consulted.** Whether other sources define ARR, NRR or the quick ratio
   differently was not checked.
3. **Written by us, not sourced**: the Output / checkpoint paragraph, the premise, the naming of a trailing
   total, the note that logo and revenue churn can move apart, the periods-must-match point, the same
   definition on both sides of DAU to MAU, and the lag remark on CAC.
4. **The source's missing files**: `statistical_tests_reference.md` and `metric_discrepancy_guide.md` are
   referenced by that repository but absent from the clone; nothing depends on them.
5. **Other files** of the metrics calculator skill and of the repository were not read for this block.

## Verification pass (2026-10-16)
Every formula in the two references was compared line by line with the source file, reopened in this session.
- **Corrected:** none needed.
- **Reversed or overstated rules found:** none; the consequences added by us are marked as such.
- **Not re-verified:** the correctness of the source's definitions against other references.

## Related blocks
`metric-movement-diagnosis-pitfalls`, `analysis-validation-pitfalls`, `business/data-analytics`,
`business/customer-success`.
