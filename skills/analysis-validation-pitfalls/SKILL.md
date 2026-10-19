---
name: analysis-validation-pitfalls
description: "Use when an analysis, report, dashboard figure or query result is about to be shared or reviewed: the pre-delivery review and a three-level verdict, join explosion and double counting, partial-period comparisons, shifting denominators, average of averages, timezones, null handling, survivorship and selection bias, Simpson's paradox, outliers, false precision, red flags in results, cross-validation, leading with the finding and making the analysis reproducible."
---

# analysis-validation-pitfalls

Not a step of the pipeline: a craft block for checking a result before someone acts on it. The four sections
share one premise: **a wrong number delivered with confidence costs more than a late right one, and most
wrong numbers come from a short list of known mechanisms**, each cheap to test for. The data-handling
invariants (read-only, traceable, filters stated, no assumed missing values) are in `business/data-analytics`
§4; this block does not repeat them and adds the checks that apply to a result already computed. Experiments
are in `experiment-design-pitfalls`; explaining a movement or a discrepancy is in
`metric-movement-diagnosis-pitfalls`.

## When
- An analysis, a figure in a message or a dashboard tile is about to be sent to a stakeholder.
- Reviewing someone else's analysis, or being asked "can I trust this number".
- A result looks too clean, jumps unexpectedly, or confirms the hypothesis perfectly.
- Writing up an analysis that someone else must be able to redo.

## Steps

**Read only the section the task meets.** §1 comes first on a review; §2 and §3 are read when the
checklist points at them; §4 when the write-up is being prepared.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Review and verdict: frame, four-group checklist, spot-checks, three-level verdict and sign-off | an analysis is reviewed before it is shared | [`01-review-and-verdict.md`](./references/01-review-and-verdict.md) |
| 2 | Calculation traps: joins, partial periods, denominators, average of averages, timezones, nulls | a number may be inflated, shifted or mis-aggregated | [`02-calculation-traps.md`](./references/02-calculation-traps.md) |
| 3 | Logic and statistics traps: survivorship, selection, Simpson, outliers, precision, red flags, cross-checks | the numbers are right but the conclusion may not follow | [`03-logic-and-statistics.md`](./references/03-logic-and-statistics.md) |
| 4 | Delivery and reproducibility: the finding first, assumptions, documentation template, charts | the write-up is being prepared or checked | [`04-delivery-and-reproducibility.md`](./references/04-delivery-and-reproducibility.md) |

## Output / checkpoint
A review is done when it ends in one of three verdicts with its reasons: ready, share with the listed caveats,
or needs revision with the changes in priority order. A write-up is done when a person who was not involved
can find the headline in the first paragraph, see each definition, period and timezone, and re-run the work
from the stored queries. Read it once looking for a rate whose parts come from different places, a comparison
of a partial and a full period, and a conclusion drawn from a group defined by the outcome; none should
survive unexplained. Nothing here was verified by running a review process: the check is a read of the text.

## Guardrails
- Never share a figure whose join row counts were not checked (§2.1).
- Never compare a partial period with a full one, and never average pre-computed averages (§2.2, §2.4).
- Never fill a missing value to complete a number without saying so; the data-handling rule wins (§2).
- Never define a segment by the outcome measured (§3.1).
- Never remove outliers automatically; investigate, then report what was excluded and why (§3.3).
- Never present a result without its verdict level and the caveats the reader needs (§1.4).
- The magnitudes and red flags here are prompts to investigate, not tolerances; this block carries no
  threshold table (§3.4).

## Origin
Rewritten from anthropics' knowledge-work-plugins (Apache-2.0) and nimrodfisher's data-analytics-skills (MIT),
read 2026-10-16. Both are young repositories, one author's practice and not consensus. 🟡: never run by us;
open points are in [`references/origin.md`](./references/origin.md).
