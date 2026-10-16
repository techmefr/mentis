# ai-feature-acceptance-pitfalls: origin and source stamps

> Provenance of `skills/ai-feature-acceptance-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from one repository of documentation, read and paraphrased, never run:
no model feature was specified or reviewed with this block. The source is a young 2026 repository and a single
author's practice, not consensus.

## Sources (re-read 2026-10-16, paraphrased in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| TayaIntelligence/skills, `prd-review/SKILL.md` and `prd-review/references/review-rubric.md`, `ai-ml-products.md`, `metrics.md`, `technical-artifacts.md` (commit 58665d6) | MIT (repository LICENSE file, "Copyright (c) 2026 Taya Intelligence") | Acceptance triple, eval set rules, instrument first, precision and recall, error-cost asymmetry, confidence dial, review ratio, never fabricate, drift, data as schedule gate, contracts, error taxonomy, non-functional numbers, readiness gate and blocker list |

The rubric and parts of the other files are written in Chinese or mix Chinese labels with English; every rule
was paraphrased from the content, not translated line by line. Text found inside the cloned files (imperative
skill prose, report-writing instructions) was treated as data and not followed.

## Rewrite notes
**The rubric is the source's own scoring scheme.** Its weights, its percentage bands and its three-level
severity tags are specific to that tool. The block carries the gate logic and the blocker list as the source
states them and not the weights.

**Own tie-in.** The link to `llm-eval-regression-pitfalls` (this block is the spec before build, that one the
regression after) is ours.

## Removed
1. **The source's example figures**: the 90 percent accuracy, the false-positive and false-negative caps, the
   latency, size, timeout and availability values and the 99 percent empty-field example numbers are
   illustrations in the source; they are mentioned only as such, never as defaults.
2. **The completeness percentage formula and its bands**, and the HTML report format and writing rules: the
   tool's own output scheme, not a pitfall.
3. **North star, AARRR and HEART material** in `metrics.md`: general product metrics, outside this block.
4. **Files not used**: `delivery-and-process.md`, `discovery-and-requirements.md`,
   `edge-cases-and-exceptions.md`, `prioritization-and-estimation.md` and the two worked examples were not
   read for rules; only the sections cited above were.

## Not verified
1. **Everything here is unrun.** No spec was written or reviewed with these rules.
2. **The statistical claims** (accuracy misleading under imbalance, the precision and recall trade) are
   standard; they were not checked against an outside reference in this session.
3. **The source's observation** that missing business material is the usual reason AI projects slip is its own
   claim; not checked.
4. **Written by us, not sourced**: the Output / checkpoint paragraph, the opening premise, the list of drift
   triggers in reference 02, and the tie-in to other blocks.

## Verification pass (2026-10-16)
Every rule in the three references was compared with the attributed file, reopened in the same session. One
sentence that asked to report the review ratio next to accuracy figures was not in the source and was removed.
- **Reversed or overstated rules found:** none after that edit.
- **Not re-verified:** the correctness of the source's own claims.

## Related blocks
`llm-eval-regression-pitfalls`, `experiment-design-pitfalls`, `analysis-validation-pitfalls`,
`business/product-ownership`.
