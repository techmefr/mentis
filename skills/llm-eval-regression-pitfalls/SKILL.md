---
name: llm-eval-regression-pitfalls
description: "Use when the behaviour of a prompt, skill, agent or model change has to be measured and not just eyeballed: test cases and the with-versus-without baseline, assertions that discriminate (deterministic first, evidence required for a pass), the biases of a model judge (position, length, self-enhancement, injected grades), grader fallback and reproducibility, and what errors and retries do to the numbers (fail_on_error, retried samples, errored samples that are scored or dropped)."
---

# llm-eval-regression-pitfalls

A block for the moment a change to a prompt, a skill or a model is called "better". The three sections share one
premise: **an eval is a measurement instrument, and a number from an instrument nobody calibrated is an
opinion with decimals**. Writing the skill or agent under test is in `writing-skills` and `writing-agents`;
fanning runs out in parallel is in `dispatch-parallel`; the gate that stops a broken change is in `gate`.

## When
- Comparing a skill, prompt or model against no skill, a previous version or another model.
- Writing assertions or a rubric for a judge model.
- An eval passes in every configuration, fails in every configuration, or changes between runs.
- Samples error out, are retried, or are skipped, and the pass rate is quoted anyway.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Cases, baseline and assertions: with and without, clean context, discriminating assertions, human review | an eval is designed or its results look uninformative | [`01-baseline-and-assertions.md`](./references/01-baseline-and-assertions.md) |
| 2 | Judges: deterministic first, rubric, bias controls, injected grades, grader fallback, reproducibility | a model grades another model | [`02-judges.md`](./references/02-judges.md) |
| 3 | Errors and retries: tolerance, retries and distribution shift, scoring errored samples, coverage | runs fail, are retried or are partly scored | [`03-errors-and-retries.md`](./references/03-errors-and-retries.md) |

## Output / checkpoint
The eval ran with and without the change in clean contexts, the assertions that pass in both arms were removed
or replaced, and a person read outputs next to grades (§1). A judge was checked against human labels on a
sample and its position and length behaviour were measured (§2). The report states how many samples errored,
were retried and were scored, next to the pass rate (§3). A report with one number and no coverage is not a
result.

## Guardrails
- Never report a with-skill score without the baseline it is compared with (§1).
- Never keep an assertion that passes in every arm; it measures nothing (§1).
- Never grade by a model what a script can check (§2).
- Never let one pass in one order decide a pairwise comparison (§2).
- Never quote a pass rate without the count of errored and retried samples (§3).
- Never set the error tolerance to ignore everything in a run that gates a release (§3).
- Restates the documentation of three projects as of the commits in [`references/origin.md`](./references/origin.md).
  No eval was run while writing it, and no numeric threshold from the sources is carried over.

## Origin
Rewritten from the Agent Skills specification site's guide to evaluating skills (Apache-2.0), the UK AI Security
Institute Inspect documentation on model grading and error handling (MIT) and the advanced-evaluation skill of a
context-engineering collection (MIT, thresholds dropped), read 2026-10-15. 🟡: never run by us; open points are
in [`references/origin.md`](./references/origin.md).
