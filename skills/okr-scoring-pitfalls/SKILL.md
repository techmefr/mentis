---
name: okr-scoring-pitfalls
description: "Use when a completed OKR set is scored at cycle close or someone reviews a scorecard: classifying each objective (committed, aspirational, learning, operational health, compliance or safety) before scoring, no retroactive change of target or scope, a failed guardrail not averaged away, effort is not impact, key results not yet observable deferred instead of forced, evidence confidence on every score, scores kept out of individual performance and pay, sandbagged targets."
---

# okr-scoring-pitfalls

Not a step of the pipeline: a craft block for closing an OKR cycle honestly. The two sections share one premise:
**a score carries meaning only if the rules for earning it were fixed before the cycle ended**, so the pitfalls
are the ways a score gets reshaped afterwards (a softer convention, a smaller scope, an averaged-out failure)
and the ways it gets over-read (as impact, as performance). Writing the OKRs themselves, running the
retrospective and designing experiments are out of scope; experiments are in `experiment-design-pitfalls`.

## When
- Closing a cycle: turning final key result values into a review.
- Reviewing a scorecard where a miss is described as stretch, or a pass is claimed on a reduced scope.
- A key result cannot be measured yet (a retention window that ends after the cycle) but a number is wanted.
- Someone proposes using OKR scores in a performance review or a bonus.

## Steps

**Read only the section the task meets.** Reference 01 comes first: every other rule depends on the type.

| Ref | Covers | Read it when | File |
|---|---|---|---|
| 01 | Classify, then score: the five objective types, the per-type convention, the guardrail rule, deferred states | a scorecard is being built or its numbers are questioned | [`01-classify-then-score.md`](./references/01-classify-then-score.md) |
| 02 | Integrity and evidence: frozen targets and scope, effort versus impact, confidence, sandbagging, misuse for individuals | a result is being explained, defended or turned into a consequence | [`02-integrity-and-evidence.md`](./references/02-integrity-and-evidence.md) |

## Output / checkpoint
A scorecard is done when each key result shows its type, its final value or an explicit deferred marker, the
score in the convention of that type, and an evidence confidence, and when a failed guardrail appears on its
own line instead of inside an average. Read it once looking for a sentence that explains why a convention, a
target or a scope was different at grading time than at writing time. Nothing here was verified by scoring a
real cycle: the check is a read of the text.

## Guardrails
- Never score before the type is known; the same 0.7 is a success for one type and a miss for another
  (reference 01).
- Never change a baseline, target or scope after the fact without grading against both the original and the
  changed version (reference 02).
- Never let a failed guardrail be diluted by the primary key result (reference 01).
- Never turn a partial result on a committed or compliance key result into a pass on the part that was done
  (reference 01).
- Never force a number on a key result that cannot be observed yet; defer it with a date (reference 01).
- Never treat shipped work as impact (reference 02).
- Never use scores for an individual's rating or pay, and expect sandbagging if anyone tries (reference 02).
- The 0.6 to 0.7 sweet spot for aspirational objectives is the source's own attribution to well-known OKR
  authors and was not checked here; carry it as "per source", never as established fact (reference 01).

## Origin
Rewritten from product-on-purpose's pm-skills, `measure-okr-grader` (Apache-2.0), read 2026-10-16. A young
2026 repository, one author's practice and not consensus. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
