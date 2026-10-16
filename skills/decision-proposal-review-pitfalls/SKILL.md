---
name: decision-proposal-review-pitfalls
description: "Use when a proposal that needs team agreement (RFC, enhancement proposal, design proposal) is written, reviewed or run through a process: socialising before writing, what an accepted proposal does and does not commit anyone to, an explicit final comment stage with a stated disposition, not rewriting review history, postponed versus closed, marking live disagreement, merging early with small edits, one proposal per feature, and which template sections earn their place (goals and non-goals, risks, honest alternatives, test plan, rollout and rollback, decision drivers, confirmation, roles)."
---

# decision-proposal-review-pitfalls

Not a step of the pipeline: a craft block for the **process around a proposal**, from the first draft to the
decision. The premise: **a proposal process fails quietly when its stages are implicit**, so people disagree
about whether a thing is approved, prioritised, postponed or dead. For the record format of one finished
architectural decision and the supersede rule see `documentation-adr`; this block does not repeat them.

## When
- Writing a proposal that needs agreement from several people or teams.
- Designing or reviewing the process (stages, owners, deadlines, dispositions) for such proposals.
- A merged proposal is read as a promise of delivery, or old proposals sit open with no outcome.
- Choosing which sections a proposal or decision template should have.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Before writing, the stages, the final comment period, dispositions | a proposal is about to be written, or the process is being defined | [`01-process-and-stages.md`](./references/01-process-and-stages.md) |
| 2 | During and after review: history, disagreement markers, small edits, lifecycle, what acceptance means | a proposal is under review or already accepted | [`02-review-and-lifecycle.md`](./references/02-review-and-lifecycle.md) |
| 3 | Template sections worth keeping and roles | a proposal or decision template is being written or trimmed | [`03-template-sections.md`](./references/03-template-sections.md) |

## Output / checkpoint
Pick one proposal in the process and answer from its page alone: what stage is it in, who must approve the
next move, what happens when the period ends, and what does acceptance commit the author and the team to. If
any answer needs asking someone, the stages are not explicit. Read the alternatives section once looking for
an option nobody would choose. Nothing here was run with a team.

## Guardrails
- Never treat an accepted proposal as scheduled work or as an obligation on its author (§2.3).
- Never leave a proposal without a stated disposition; "postponed" is not a polite "no" (§1.4).
- Never squash or rewrite review history once others have seen it (§2.1).
- Never change an accepted proposal substantially in place; write a new one that links to it (§2.3).
- Never present a strawman as an alternative or hide a drawback (§3.1).
- The ten calendar day period, the five business day minimum and the section lists in this block are
  single-project choices, shown as examples (§1.3, §3); nothing here is a legal or HR rule.

## Origin
Rewritten from the Rust RFC process (MIT or Apache-2.0), the Kubernetes enhancement proposal template
(Apache-2.0) and the MADR decision template (MIT or CC0-1.0), read 2026-10-16. Text is reworded and
condensed, and none of it is those projects' endorsement. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
