---
name: spec
description: Use when locking down the scope of a feature before the plan, clarification interview, explicit scope + out-of-scope, CONTEXT.md and ADR.
---

# spec

Step 2 of the pipeline (`WORKFLOW.md`). Lock down *what* we're building, with a shared
vocabulary and traced decisions. Every rule below holds in a repo with **nothing installed**
(`CONVENTIONS.md`, rule A).

Upstream of this block, `business/product-ownership` owns whether the thing should exist at all and what
the story says; this block turns a ready story into the technical contract the rest of the pipeline works
from. Downstream, §3's criteria are what `tdd` writes failing tests against.

## When
After `brainstorm`, before `/PLAN`. Or as soon as the scope / acceptance criteria are unclear.

## Steps

**Read only the sections the step actually needs.** The rules live one file per section under
`references/`; the normal path is §1 first, then §2 to §5 in order as the interview produces their
content.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The clarification interview | starting the step, before anything is written down | [`01-the-interview.md`](./references/01-the-interview.md) |
| 2 | `CONTEXT.md`, the shared vocabulary | writing the feature's terms, entities and business rules | [`02-context-md.md`](./references/02-context-md.md) |
| 3 | Acceptance criteria, the contract for `tdd` | turning the story's criteria into what the tests assert | [`03-acceptance-criteria.md`](./references/03-acceptance-criteria.md) |
| 4 | Out of scope, explicitly | the scope is being locked | [`04-out-of-scope.md`](./references/04-out-of-scope.md) |
| 5 | ADRs | a structural decision is taken | [`05-adr.md`](./references/05-adr.md) |

## Output / checkpoint
`spec_done` + `CONTEXT.md` + ADR(s), plus the numbered acceptance criteria and the explicit out-of-scope
list. What it owes: a scope a third party could implement without asking a blocking question, and no
invented rule anywhere in it.

## Guardrails
- No code.
- **Never fill a gap with a plausible assumption** — the need for an invented rule is the finding (§1.7).
  If the scope is still unclear after the interview, `escalate` rather than guess.
- **Never leave a hypothesis unlabelled** once it has been written down (§1.8).
- **Never hide an undecided question inside the out-of-scope list** (§4.9).
- **Never renumber the acceptance criteria** — the tests, the review and the gate's evidence cite them
  (§3.8).
- Never restate the story's criteria in different words; correct the story instead (§3.10).

## Origin
A recognised market skill author (grill-with-docs → CONTEXT.md + ADR) + internal `spec-clarification`,
rewritten. The full provenance and the refresh log are in
[`references/origin.md`](./references/origin.md).
