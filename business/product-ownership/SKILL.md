---
name: product-ownership
description: "Use when deciding what gets built and in what order, or whether a request should become a story at all: priority, refusal, acceptance criteria, ready and done, decomposition sized to one MR, estimation, and the case where the story's author is also the builder."
---

# product-ownership

Business layer (`business/README.md`), product.

**Relation to an org skill catalogue.** Where a company ships its own project-management skills, they are the
authority on **its** artefacts — its tracker fields, its info-panel presentation charter, its label
taxonomy, its MCP tooling — and override this block on all of that. What's below is the generic form: the
decisions, the story anatomy and the review axes, with no tracker or project named (rule C). The technical
specification that follows a ready story is `skills/spec`; the story anatomy is §6, reviewing it §7, and decomposition plus estimation §8.

This block owns: **whether the thing should exist, in what order, how it's written down, how it's reviewed,
and how anyone will know it's finished.**

**Applying an override is silent.** Write what the governing rule requires and move on — never report "a
conflict between mentis and the house rules" to whoever's watching. That framing reads as broken to a
non-technical stakeholder even when the case is a normal, resolved one, and has already caused a real
project to get abandoned and restarted over nothing. Surface it as a specific, named question only when no
rule anywhere actually resolves the case.

## When
When a request arrives from a customer, a colleague or a stakeholder; when a backlog needs ordering; when
a story is about to be picked up and it isn't clear what "done" means.

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; a request arriving is §1–§3, writing the story is §4 and §6, reviewing one is §7, breaking
one down is §8. Loading all nine to answer one question is waste.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | A request is not a story yet | a request arrives, before anything is written down | [`01-request-is-not-a-story.md`](./references/01-request-is-not-a-story.md) |
| 2 | Order by consequence | a backlog needs ordering, or two items are being argued about | [`02-order-by-consequence.md`](./references/02-order-by-consequence.md) |
| 3 | Saying no is the job | something is being declined, deferred or reshaped | [`03-saying-no.md`](./references/03-saying-no.md) |
| 4 | Acceptance criteria | criteria are written, or delivered work is accepted against them | [`04-acceptance-criteria.md`](./references/04-acceptance-criteria.md) |
| 5 | Ready and done | a story is about to be picked up, or is being called finished | [`05-ready-and-done.md`](./references/05-ready-and-done.md) |
| 6 | The story document | a story is written or modified | [`06-the-story-document.md`](./references/06-the-story-document.md) |
| 7 | Reviewing a story | reviewing a story someone else wrote | [`07-reviewing-a-story.md`](./references/07-reviewing-a-story.md) |
| 8 | Decomposition and estimation | a ready story is broken into tasks, or a number is attached to work | [`08-decomposition-estimation.md`](./references/08-decomposition-estimation.md) |
| 9 | When the author is also the builder | one person writes the story and implements it | [`09-author-is-the-builder.md`](./references/09-author-is-the-builder.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the problem stated separately from the requested
solution, a rank with its reasoning, refusals written down with which kind of "no" they are, acceptance
criteria a third party can check including the unhappy paths, an explicit ready/done bar, a story written to
the fixed section set, and — when reviewing — a criticality level, the axes actually read, and blocking gaps
separated from improvements.

## Guardrails
- **Never turn a request into a story without the problem behind it.**
- **Never commit scope or a date the people who'd build it haven't seen.**
- **Never trade the tests or the review for a date.**
- **Never leave a criterion nobody can verify** — it guarantees an argument at acceptance.
- **Never create a label, rewrite a description, or transition someone else's story without confirmation.**
- **Never produce an estimate without having read the code.**
- **Never fill a gap in a story with an invented rule, and never specify the interface inside one.**
- **Never present a hypothesis as a decision.**
- Where an org catalogue defines the tracker fields, the presentation charter or the label taxonomy, **it
  wins** — this block's §6–§8 are the generic form, not a competing charter.
- Where a company has a product owner or a project manager, they decide; this block structures the
  decision, it doesn't take it. Where the same person writes the story and builds it (§9), that
  applies to whoever owns the epic — **never decide an unsettled business rule because you happen
  to hold both roles.**

## Origin
Written without internal product-management expertise; §6–§8 come from an org skill catalogue for this
function, extracted and de-identified, and §9 from a real organisational change. The full provenance, the
source stamps and the refresh log are in [`references/origin.md`](./references/origin.md). Read it when
checking whether a rule is still current, not when applying one.
