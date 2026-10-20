---
name: model-migration-pitfalls
description: "Use when the model behind an application changes (a provider retires or replaces a version, a floating alias moves, a cheaper or newer model is proposed, a self-hosted model is swapped): pinning and a deprecation calendar, a side-by-side run on your own cases before any traffic moves, reading the diff by case instead of by average, prompts and parameters that do not transfer, and a staged cutover with a way back."
---

# model-migration-pitfalls

A defensive block for the day a model is replaced, on purpose or because the vendor decided. The two sections
share one premise: **a model swap is a behaviour change to every prompt you have, and generic benchmark gains say
little about your cases, so run your own set on both models and read the differences before moving traffic**.
Gating a prompt edit is in `prompt-versioning-and-change-gating-pitfalls`; the measurement method is in
`llm-eval-regression-pitfalls`; choosing a model for a task is in `choose-model`; cost and latency effects are in
`llm-cost-latency-control-pitfalls`; attack cases that must still pass are in
`llm-app-prompt-injection-and-exfiltration-pitfalls` §3; date-stamping any fact about a vendor is
`source-freshness`.

## When
- A provider announces that a model version will be retired, or a floating alias is about to point elsewhere.
- Someone proposes a newer, cheaper or faster model, or a self-hosted replacement.
- Behaviour changed overnight with no deploy and the provider model is the suspect.
- A fallback model has never been exercised.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Pinning and calendar: version identifiers, aliases, deprecation dates, the inventory of calls | before any change, and as a standing practice | [`01-pinning-and-calendar.md`](./references/01-pinning-and-calendar.md) |
| 2 | The migration run: your own case set, side-by-side diff, prompt and parameter drift, staged cutover, rollback | a candidate model exists | [`02-migration-run.md`](./references/02-migration-run.md) |

## Output / checkpoint
An inventory lists every call site with its model identifier, whether it is pinned, the retirement date the
provider published (dated and sourced) and the owner (§1). The candidate ran the same cases as the current model,
in clean contexts, with repeats, and the report lists case-level wins, losses and errors, plus cost and latency
(§2.2). Attack cases and known-bad cases were part of the set (§2.2). The cutover is staged with a named rollback
and an observation window (§2.5). An average score alone does not decide a migration.

## Guardrails
- Never point production at a floating alias without knowing when it moves; pin where the provider allows (§1).
- Never swap the model and edit the prompt in the same step, or you cannot tell which one did it (§2).
- Never decide from a public benchmark or a vendor claim; run your own cases (§2).
- Never carry the old model's sampling parameters, token limits or stop settings over unchecked (§2).
- Never leave the fallback model untested; exercise it on the same cases (§2).
- This block is idea-level guidance from the sources in [`references/origin.md`](./references/origin.md), read on the
  date there. No migration was run and no vendor dates or limits are stated.

## Origin
promptfoo documentation (MIT) on comparing models over your own cases and on drift detection by repeated runs,
plus craft knowledge marked "own guidance", read 2026-10-20. Two vendors' deprecation pages and one models overview were read for facts (no dates or figures are stated). 🟡:
never run by us; open points are in [`references/origin.md`](./references/origin.md).
