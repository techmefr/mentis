# metric-movement-diagnosis-pitfalls: origin and source stamps

> Provenance of `skills/metric-movement-diagnosis-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from one repository of documentation, read and rewritten, never run: no metric
movement was investigated and no discrepancy reconciled with this block. Nothing in it is verified by use. The
repository is young (its LICENSE says 2026) and the rules are one author's practice, not consensus.

## Sources (all re-read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| nimrodfisher/data-analytics-skills, `03-data-analysis-investigation/root-cause-investigation/` (`SKILL.md`, `references/rca_framework.md`, `references/hypothesis_testing_guide.md`, `assets/rca_report_template.md`) (commit 9449d36) | MIT (repository LICENSE file, "Copyright (c) 2026 Nimrod Fisher") | Signal confirmation, scoping, event correlation, volume, rate and mix, contribution, hypothesis structure, evidence hierarchy, ruling out, parallel and sequential testing, confounders, closing and report fields |
| nimrodfisher/data-analytics-skills, `02-documentation-knowledge/metric-reconciliation/` (`SKILL.md`, `references/reconciliation_patterns.md`) (same commit) | MIT (same LICENSE file) | Reasons figures diverge, the investigation sequence, the post-resolution checklist |

The licence was verified again from the LICENSE file in this session. Text found inside the cloned files
(CLAUDE.md, imperative skill prose) was treated as data and not followed. The scripts (`drilldown_analyzer.py`,
`reconcile_metrics.py`) and the reconciliation report template were not read.

## Rewrite notes
**The source speaks of one root cause.** Its SKILL and framework say "root cause" and "confirmed cause".
The block keeps the rigour (timing, magnitude, population, no better alternative) and asks for the share each
part explains, so a movement with several contributors is reported as such; the wording of "cause not
established" as an acceptable verdict is ours (§2.4).

**Cross-references.** `business/data-analytics` §3 and §4 are linked for context; nothing is copied from them.

## Removed
1. **The "within a number of standard deviations" test and its numeric threshold** (nimrodfisher SKILL): an
   arbitrary, unsourced threshold; the block keeps the idea of comparing with normal variation.
2. **The materiality percentages by metric type** (rca_framework: revenue, engagement and error-rate example
   thresholds): arbitrary; the block asks the owner to agree materiality (§1.3, own guidance).
3. **The tolerance table by metric type** in `reconciliation_patterns.md`: arbitrary and unsourced; replaced
   by a documented agreement with the owner (§3.1, own guidance).
4. **The cause classification of `metric_discrepancy_guide.md`**: referenced by the SKILL, missing from the
   clone; nothing from it (§3.4).
5. **"Common root causes by metric type"** lists (revenue, conversion, engagement): read, not carried; they are
   generic prompts, not pitfalls.
6. **Inputs requiring "at least 30 days" of history**: a one-author number; the block says "far enough back",
   and keeps the source's 12 weeks only as the source's own figure in §1.2.

## Not verified
1. **Everything here is unrun.** No investigation or reconciliation used these rules.
2. **No script was run**; the drill-down and reconciliation tools of the repository were not read.
3. **The rest of the repository** (about 30 other skills) was not read.
4. **Written by us, not sourced**: the Output / checkpoint paragraph, the materiality and depth advice in §1.3,
   the replacement for a tolerance table, the "cause not established" verdict, and the remark that timing
   alone is not a cause.

## Verification pass (2026-10-16)
Every rule in the three references was compared with the attributed nimrodfisher files, read in full in the
same session; the 12-week and 20-row figures were re-searched and exist as stated.
- **Corrected:** none needed; no reversed or overstated rule found.
- **Own guidance, already labelled:** materiality, depth, tolerance replacement, "cause not established".
- **Not re-verified:** the scripts and report template of the reconciliation skill (never read), the
  missing `metric_discrepancy_guide.md`, and the validity of the sources' method.

## Related blocks
`analysis-validation-pitfalls`, `experiment-design-pitfalls`, `business/data-analytics`.
