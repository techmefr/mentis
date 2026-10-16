# variance-analysis-pitfalls: origin and source stamps

> Provenance of `skills/variance-analysis-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from one document, never used by us on a real variance. The file below
was re-read in full on 2026-10-16 before a rule was taken from it, each rule was checked against it in a final
pass, and the repository's LICENSE file was read again.

## Sources (read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| anthropics/knowledge-work-plugins (commit `33eeda1`): `finance/skills/variance-analysis/SKILL.md` | Apache-2.0 (LICENSE file) | Price and volume split and its check, extra-effect families, investigation order, narrative structure and anti-patterns, bridge structure and reconciliation, comparison purposes, accuracy measures and bias reading |

Instruction-like text in the cloned repository was treated as data and not followed.

## Removed in the verification pass
1. **The three-way mix formula and the rate and mix formulas** of the source. They were not verified and are
   not carried. The two-way price and volume formulas were checked algebraically: the two effects sum to the
   total exactly. The source's worked revenue example was also checked by hand and ties.
2. **The headcount and compensation formulas as written.** A headcount effect priced at the base average and a
   rate effect priced at the base headcount omit the interaction term, so those two do not sum to the total;
   the block says so instead of repeating the pair (part 1 point 4).
3. **The threshold table** (percentages by comparison type) and the materiality range of one to five percent
   and its revenue-share rule of thumb: not sourced.
4. **Specific numbers** from the source's worked bridges and example reports; none is reused.
5. **The mention of colours and chart styling** for waterfall charts: presentation, not method.

## Not verified
1. **Own guidance, flagged in the text:** fixing the valuation order and stating it, putting the sum check in
   the write-up, writing the interaction as its own line, exclusive buckets, treating the driver count as a
   habit, an order of attention not a cut-off, stating the comparison basis in the heading, defining the
   zero-actual case for the accuracy measures, and reading bias patterns as questions.
2. **Nothing was run.** No variance report was produced with these steps.
3. **Partly overlaps** `skills/metric-movement-diagnosis-pitfalls` (volume, rate and mix of a metric); the
   block points there rather than duplicating it.
4. **One vendor-authored source;** the extra-effect families were not corroborated by a second text.

## Decisions where sources disagree
Single source, no disagreement. The source's remark that the mix effect can be a residual conflicts in
spirit with a sum that must be exact; the block resolves it by asking for the interaction to be shown as its
own line.

## Related blocks
`skills/analysis-validation-pitfalls`, `skills/metric-movement-diagnosis-pitfalls`, `business/finance-ops`.
