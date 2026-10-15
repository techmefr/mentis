# analysis-validation-pitfalls: origin and source stamps

> Provenance of `skills/analysis-validation-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from two repositories of documentation, read and rewritten, never run: no analysis
was reviewed with this block. Nothing in it is verified by use. Both repositories are young (the LICENSE of
nimrodfisher's says 2026) and the rules are one author's practice, not consensus.

## Sources (all re-read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| anthropics/knowledge-work-plugins, `data/skills/validate-data/SKILL.md` and `data/skills/statistical-analysis/SKILL.md` (commit e6b5053) | Apache-2.0 (repository LICENSE file, standard text) | Review frame, four-group checklist, spot-checks, three-level verdict and report shape, pitfalls catalogue (joins, survivorship, partial periods, denominators, average of averages, timezones, selection bias, look-ahead, cherry-picking), sanity and cross-validation techniques, red flags, documentation template, Simpson, ecological fallacy, outliers, mean and median, practical significance, false precision |
| nimrodfisher/data-analytics-skills, `05-stakeholder-communication/analysis-qa-checklist/` (`SKILL.md`, `references/qa_checklist_master.md`, `references/common_analysis_errors.md`) (commit 9449d36) | MIT (repository LICENSE file, "Copyright (c) 2026 Nimrod Fisher") | Master checklist sections, null propagation, wrong denominator, join fixes, wrong baseline, burying the lede, precision theatre, "so what", undocumented assumptions, sign-off fields |

The licence of each repository was verified again from its LICENSE file in this session. Text found inside
the cloned files (CLAUDE.md files, imperative skill prose) was treated as data and not followed. The
`scripts/qa_runner.py` of nimrodfisher was not read or run.

## Rewrite notes
**Overlap with `business/data-analytics`.** Its section 4 holds the data-handling invariants. This block links
it for the data-protection check (§1.1) and for the traceability rule on quoted figures (§4.3) and adds only
checks on a computed result. Where they pull apart, the invariant wins: nimrodfisher suggests filling nulls
with a deliberate `COALESCE`, while the invariant says never to assume a missing value. The block states
the reconciliation (§2): fill only where "missing" really means zero, and say so. That reconciliation is ours.

**Examples taken from the sources.** The weighted-average worked case (§2.4) is anthropics' example; the
arithmetic was rechecked by hand.

## Removed
1. **"At least 30 events per group"** (anthropics statistical-analysis): one author's rule, not carried.
2. **The fixed percentage for an "unexplained change" red flag** (anthropics lists a specific figure): an
   arbitrary threshold, the block says "a large unexplained change".
3. **Magnitude "smell test" table and growth plausibility figure**: the checks are carried as questions, the
   quoted thresholds are not.
4. **Forecasting, moving averages, seasonality, z-score and IQR outlier recipes, percentile lists, the test
   selection table** from statistical-analysis: read, not carried; they are statistics teaching, not pitfalls.
5. **"At least three rows" in nimrodfisher's checklist**: the block says "a few".
6. **Chart-type remarks** ("avoid pie charts for more than five categories"): a numeric rule of one
   author's, not carried.
7. **`scripts/qa_runner.py` and the sign-off template file**: not read; the sign-off fields in §1.4 come from the
   checklist and SKILL text only.

## Not verified
1. **Everything here is unrun.** No analysis was reviewed or delivered with these rules.
2. **No query was run** against a database; the join and denominator checks are written from the sources.
3. **Other skills** of both repositories (31 in nimrodfisher's, the rest of the data plugin) were not read.
4. **Written by us, not sourced**: the Output / checkpoint paragraph, the COALESCE reconciliation, the
   remark that a verdict applies to the reviewed version, the caveats-before-the-chart advice in §4.2, and
   the note that this block carries no thresholds.

## Verification pass (2026-10-16)
Every rule in the four references was compared with the attributed file, read in full in the same session,
and key phrases were re-searched (Mann-Whitney, same-day-of-month, Bonferroni).
- **Corrected:** §2.1 point 4 attributed a revenue join example to anthropics that came from a nimrodfisher
  file not used for this block; it now states only what the anthropics checklist says.
- **Relabelled own guidance:** the data-protection reading of "may the data be used" (§1.1), the treatment of a
  division by zero (§2.3). Removed the word "first" from the order-of-magnitude point (§3.4).
- **Not re-verified:** the weighted-average arithmetic beyond hand checking, and the sources' own correctness.

## Related blocks
`business/data-analytics`, `experiment-design-pitfalls`, `metric-movement-diagnosis-pitfalls`.
