---
name: metric-movement-diagnosis-pitfalls
description: "Use when a business metric moves unexpectedly or two sources disagree on the same number and someone must explain it: confirming the signal and pipeline freshness before any story, building a timeline, decomposing into volume, rate and mix, comparing denominators and the same weekday, writing falsifiable hypotheses, ranking evidence quality, recording ruled-out causes, and the fixed order for reconciling two figures (filters, joins, grain, timezone, definition drift, refresh lag)."
---

# metric-movement-diagnosis-pitfalls

Not a step of the pipeline: a craft block for explaining a number that changed or a pair of numbers that
disagree. The three sections share one premise: **the cheapest wrong answer is a product story told about a
broken pipeline, a changed definition or ordinary noise**, so the signal is confirmed and decomposed before a
cause is named, and every candidate cause is written so that it can fail. Checking a finished analysis is in
`analysis-validation-pitfalls`; the data-handling rules of reading real data are in `business/data-analytics`
§4; consolidating figures across independent instances is `business/data-analytics` §3.

## When
- A key metric dropped or spiked and a stakeholder asks "why".
- A movement is seen but nobody knows whether it is noise or signal.
- Two dashboards, reports or pipelines show different values for what should be the same figure.
- A number changed after a pipeline, schema or definition change.

## Steps

**Read only the section the task meets.** §1 first for a movement; §3 first for two disagreeing figures;
§2 is read once the movement is real.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Confirm the signal and scope the movement: pipeline freshness, definition, independent sources, onset, event log | a movement has just been reported | [`01-confirm-and-scope.md`](./references/01-confirm-and-scope.md) |
| 2 | Decompose, hypothesise, test: volume, rate and mix, contribution, falsifiable hypotheses, evidence ranking, ruled-out record | the movement is real and needs a cause | [`02-decompose-and-test.md`](./references/02-decompose-and-test.md) |
| 3 | Reconcile two numbers: definition first, why figures differ, the investigation order, closing the loop | two sources disagree | [`03-reconcile-two-numbers.md`](./references/03-reconcile-two-numbers.md) |

## Output / checkpoint
A diagnosis is done when someone who was not in the investigation can answer from the page: was the signal
confirmed and how, when did it start and who is affected, which part of the metric moved (volume, rate or mix)
and by what share, which hypotheses were tested with what evidence at what level, which were ruled out and why,
and what is established or still open. A reconciliation is done when the divergence point is named with the
query excerpt, one source is designated, and the gap is either fixed or accepted by its owner. Read it once
looking for a cause supported only by timing, and for a hypothesis with no stated way to fail. Nothing here was
verified on a live investigation: the check is a read of the text.

## Guardrails
- Never explain a movement before the signal is confirmed: freshness, definition and a second source (§1.1).
- Never name a cause on correlation in time alone; rank the evidence and say its level (§2.3).
- Never drill by dimension before decomposing into volume, rate and mix (§2.1).
- Never compare a rate without looking at its denominator and mix (§2.1).
- Never drop a ruled-out hypothesis from the report (§2.3).
- Never close a gap as acceptable without the owner's agreement; this block carries no tolerance table (§3.1).
- Never reconcile from cached dashboards; pull both values from the authoritative sources (§3.1).

## Origin
Rewritten from nimrodfisher's data-analytics-skills (MIT: root-cause-investigation and metric-reconciliation),
read 2026-10-16. A young 2026 repository, one author's practice and not consensus. 🟡: never run by us; open
points are in [`references/origin.md`](./references/origin.md).
