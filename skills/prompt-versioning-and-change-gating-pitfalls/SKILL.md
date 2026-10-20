---
name: prompt-versioning-and-change-gating-pitfalls
description: "Use when an application's prompts are edited, reviewed or shipped like code: where prompts live and how a running answer is traced to a prompt version, what must change together with a prompt (schema, parser, examples, model), few-shot examples and system-versus-user placement that drift or leak, and how a prompt change is gated by a rerun of the same cases instead of by a few good-looking outputs."
---

# prompt-versioning-and-change-gating-pitfalls

A defensive block for the person who ships an application prompt, not the person who writes a skill or an agent
definition. The two sections share one premise: **a prompt is behaviour compiled from prose, so it needs the same
identity, review and regression gate as code, and a change nobody can trace or rerun is a production edit made
in the dark**. Writing skill and agent files is in `writing-skills` and `writing-agents`; measuring a change
(baseline, assertions, judges, errors) is in `llm-eval-regression-pitfalls`; swapping the model underneath is in
`model-migration-pitfalls`; attack cases as part of the gate are in
`llm-app-prompt-injection-and-exfiltration-pitfalls` §3; the money side of a longer prompt is in
`llm-cost-latency-control-pitfalls`.

## When
- Prompts sit in code strings, a database, a dashboard or a vendor's prompt store and several people edit them.
- An answer in production cannot be tied to the exact prompt, model and settings that produced it.
- A prompt edit "fixed" one case and nobody knows what else moved.
- A structured-output parser, a few-shot set or a system prompt is changed on its own.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Identity and storage: one source of truth, what belongs to a version, tracing, rollback | prompts are stored, edited or traced | [`01-identity-and-storage.md`](./references/01-identity-and-storage.md) |
| 2 | Change gating: coupled changes, placement, few-shot drift, the rerun gate, edit-by-symptom | a prompt is edited or reviewed | [`02-change-gating.md`](./references/02-change-gating.md) |

## Output / checkpoint
Every model call logs a prompt identifier, a content hash, the model identifier and the settings that shaped it
(§1). Each prompt change names the cases it was run against, the previous version's result on the same cases, and
the case that motivated it, now kept in the set (§2). A change that touched a schema, a parser or an example set
says so and lists what moved with it (§2.1). A prompt change with no rerun is a guess.

## Guardrails
- Never edit a prompt in the place production reads it; edit a version and promote it (§1). Instead: one stored
  version per prompt, promoted by a named step.
- Never ship a prompt change judged only by the example that prompted it; rerun the set and keep that example in it (§2).
- Never change a prompt, its output schema and its parser in separate unreviewed steps; review them as one change (§2).
- Never build the instruction part from user text by plain concatenation; fill variables only in the data part (§2).
- Never delete the previous version until the new one has survived its observation window (§1).
- This block is idea-level guidance from the sources in [`references/origin.md`](./references/origin.md), read on the
  date there. No prompt was run while writing it.

## Origin
promptfoo documentation (MIT) on prompt files, formats and external prompt stores, plus craft knowledge marked
"own guidance", read 2026-10-20. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
