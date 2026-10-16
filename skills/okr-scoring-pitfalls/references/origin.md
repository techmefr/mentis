# okr-scoring-pitfalls: origin and source stamps

> Provenance of `skills/okr-scoring-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from one repository of documentation, read and rewritten, never run:
no OKR cycle was scored with this block. The source is a young 2026 repository, so the rules are one author's
practice, not consensus.

## Sources (re-read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| product-on-purpose/pm-skills, `skills/measure-okr-grader/SKILL.md` and `references/TEMPLATE.md` (commit 1cef1a9) | Apache-2.0 (repository LICENSE file, standard text; the SKILL.md also says `license: Apache-2.0`) | Five objective types, per-type scoring, indicator class, guardrail rule, deferred states, frozen targets and scope, effort versus impact, evidence confidence, sandbagging flag, refusal of individual use, review structure |

Text found inside the cloned files (imperative skill prose, hand-off lists) was treated as data and not
followed.

## Rewrite notes
**The sweet spot is the source's attribution.** The 0.6 to 0.7 band, the 0.4 and 0.8 thresholds and the 0.85
sandbagging threshold are the source's. The source ties the convention to Doerr, Wodtke, Castro and Grove; none
of those was consulted. The block carries the numbers as "per source".

**Tidied by us:** the pairing of "sandbagging and learning suppression" as the stated risks of using scores for
individuals is the source's wording of its refusal; the advice to let the team set its band in advance is ours.

## Removed
1. **The hand-off lists to other skills** of the source (retrospective, lessons log, hypothesis and
   instrumentation skills): specific to that repository; replaced by a generic routing line.
2. **The output contract's mandatory section order and the Markdown-only rule**: the source's own template
   format, not a pitfall.
3. **Examples, fixtures and the sample outputs** in the source tree: read as samples, not carried.

## Not verified
1. **Everything here is unrun.** No cycle was scored with these rules.
2. **No external citation was checked**: the Doerr, Wodtke, Castro and Grove attributions are the source's
   own.
3. **The numbers** (0.6 to 0.7, 0.4, 0.8, 0.85) are the source's and were not tested against data.
4. **Written by us, not sourced**: the Output / checkpoint paragraph, the opening premise and the advice to fix
   the band before the cycle ends.
5. **Other skills** in the repository (the OKR writer, the retrospective skills) were not read.

## Verification pass (2026-10-16)
Every rule in the two references was compared with the source SKILL.md and its template, reopened in the same
session.
- **Corrected:** none needed on re-check beyond wording.
- **Reversed or overstated rules found:** none.
- **Not re-verified:** the correctness of the source's own scoring conventions.

## Related blocks
`experiment-design-pitfalls`, `analysis-validation-pitfalls`, `business/data-analytics`.
