---
name: assumption-validation-pitfalls
description: "Use when a product or business assumption is tested before building (prototype, interview, survey, data mining, spike) or a finding is promoted to a learning: success and failure criteria written before the test, one hypothesis per test, a time budget that forces an explicit decision, confidence per risk (value, usability, feasibility, viability) that moves only on evidence and can go down, disconfirming evidence, inconclusive as an honest result, evidence required by cost and reversibility, and promotion of a result to a learning only with independent evidence, context coverage and kept contradictions."
---

# assumption-validation-pitfalls

Not a step of the pipeline: a craft block for testing an idea before it is built, so that validation is not
theatre. The three sections share one premise: **a test with no stated way to fail will confirm, and a
learning promoted from one story will mislead**, so the criteria, the budget and the bar for promotion are
fixed before the evidence arrives. Online controlled experiments (A/B tests) are in
`experiment-design-pitfalls`; attacking a whole plan before committing is `premortem-review-pitfalls`.

## When
- A hypothesis is written before building a feature, a flow or a price.
- A test (prototype, interview round, one-question survey, data mining, code spike) is designed or read.
- A deadline passes with no conclusion, or every test so far "confirmed" the idea.
- A finding is about to be written up as a principle for the product.

## Steps

**Read only the section the task meets.** §1 comes first when a test is being planned; §2 when confidence
or a result is recorded; §3 when something is promoted.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Criteria, budget and the smallest test: what is written before testing, timeout, decomposing, test methods, honest interpretation | a validation is planned or reviewed | [`01-criteria-and-budget.md`](./references/01-criteria-and-budget.md) |
| 2 | Confidence, evidence and recording: four risks, how much is enough, updating confidence, result record | confidence is scored or a result written up | [`02-confidence-and-results.md`](./references/02-confidence-and-results.md) |
| 3 | Promoting a finding: tiers, independent evidence, context coverage, kept contradictions, freshness | a result is proposed as a learning or principle | [`03-promoting-learnings.md`](./references/03-promoting-learnings.md) |

## Output / checkpoint
A validation is done when someone who was not in it can answer from the record: what was believed, what
observation would have proved it right and what wrong (written before the test), how much time was allowed and
what was decided at the end of it, which risk was tested and why that one, what the evidence was and how
confidence moved on each risk, and whether the result was validated, invalidated or inconclusive. Read it
once looking for a success criterion written after the result, a confidence that only ever rose, and a
learning with a single source. Nothing here was verified by running a discovery programme: the check is a
read of the text.

## Guardrails
- Never start a test without success and failure criteria and a time budget (§1.1).
- Never test several hypotheses in one test, and never let the author alone set the criteria (§1.1, §1.4).
- Never let a deadline pass silently; a timeout ends in extend, pivot or abandon, decided in writing (§1.2).
- Never raise or lower confidence without new evidence, and allow it to go down (§2.3).
- Never force a verdict from thin evidence; write inconclusive and what would settle it (§2.4).
- Never promote a finding on retellings of one observation or beyond the contexts it covers (§3.2).
- Never delete a contradiction or a rejected hypothesis; record its conditions (§2.4, §3.3).
- The numeric confidence scale and tier layout are the source's choices, not requirements (§2.1).

## Origin
Rewritten from shinpr's claude-code-discover (MIT: hypothesis-discipline, product-principles, recipe-validate and
the hypothesis-verifier and knowledge-distiller agents), read 2026-10-16. A young 2026 repository, one author's
practice and not consensus. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
