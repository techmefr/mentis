---
name: ai-feature-acceptance-pitfalls
description: "Use when the acceptance bar of a model-driven feature (extraction, classification, generation, OCR, matching, recommendation) is written or reviewed before build: the eval set, metric and threshold as the acceptance criterion, a representative held-out eval set reported per class, features that cannot be evaluated yet, accuracy versus precision and recall under class imbalance, asymmetric error costs, the confidence threshold and human review, never fabricating a value, drift, labelled data as a schedule gate, null semantics, system errors versus business warnings, non-functional numbers, readiness that is not an average."
---

# ai-feature-acceptance-pitfalls

Not a step of the pipeline: a craft block for the spec of a feature whose core is a model, read before anything
is built. The three sections share one premise: **a model produces a distribution of outcomes, so "the output is
correct" is not a testable criterion and a spec that uses it hides every decision the engineers will have to
make**. Regression of an eval that already exists (baselines, judges, retries) is in
`llm-eval-regression-pitfalls`; this block is about what the spec must say before there is anything to
regress. Experiments on a live product are in `experiment-design-pitfalls`.

## When
- Writing or reviewing the requirements, acceptance criteria or review checklist of an AI feature.
- A spec promises an accuracy figure and nobody can say how it will be measured.
- A demo worked and someone wants to accept the feature on it.
- A feature crosses a system boundary and its fields, nulls and errors are not yet defined.

## Steps

**Read only the section the task meets.** Reference 01 comes first; 02 and 03 are independent of each other.

| Ref | Covers | Read it when | File |
|---|---|---|---|
| 01 | The acceptance bar: eval set, metric, threshold, behaviour on misses; the eval set as the spec; instrument first; accuracy versus precision and recall; error-cost asymmetry | an acceptance criterion or a quality target is being written | [`01-acceptance-bar-and-eval-set.md`](./references/01-acceptance-bar-and-eval-set.md) |
| 02 | Thresholds and fallback: the confidence dial, human review, the needs-review ratio, never fabricate, drift, data as a schedule gate | the feature must act on uncertain output or depends on labels and rule tables | [`02-confidence-and-fallback.md`](./references/02-confidence-and-fallback.md) |
| 03 | Contracts and readiness: null semantics, field ownership, system errors versus business warnings, numbers for non-functional needs, the readiness gate | the feature has an interface or someone must decide whether the spec can go to build | [`03-contracts-and-readiness.md`](./references/03-contracts-and-readiness.md) |

## Output / checkpoint
A spec is done when an engineer who was not in the discussion can answer from it alone: which eval set decides,
how it was labelled and how representative it is, which metric and why, which threshold, what the system does
with the cases below the threshold, what a null means, which failures are errors and which are warnings, and
which inputs the business still owes and by when. A review is done when each blocker found has a named fix and
the verdict says why it is what it is. Read the spec once looking for a quality word with no number behind it,
and for a section that is present but only covers the successful path. Nothing here was verified on a real
project: the check is a read of the text.

## Guardrails
- Never accept a model feature on a demo; accept it on an eval set, a metric, a threshold and a defined
  behaviour on the misses (reference 01).
- Never write a target nobody can measure; if there are no labels or no method yet, the first deliverable is the
  instrument and the eval set, and the spec says so as a risk (reference 01).
- Never report one blended score when classes are imbalanced or the cost of errors differs; split by class and
  by error type (reference 01).
- Never pick the confidence threshold by feel; set it on the eval set against the cost of each error, and
  watch the review ratio at both ends (reference 02).
- Never let the feature invent a value when it cannot decide; it returns null and a reason (reference 02).
- Never plan a launch without the data, rule tables and labels it runs on; they gate the schedule
  (reference 02).
- Never average a readiness verdict: one missing blocker blocks, whatever the completeness percentage
  (reference 03).
- Never carry the example thresholds of the source (error rates, accuracy figures) as defaults; they were
  illustrations (reference 01).

## Origin
Paraphrased from TayaIntelligence's skills, the `prd-review` skill and its `references/review-rubric.md`,
`ai-ml-products.md`, `metrics.md` and `technical-artifacts.md` (MIT), read 2026-10-16. The rubric is written in
Chinese; the rules here are our own English paraphrase. A young 2026 repository, one author's practice and not
consensus. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
