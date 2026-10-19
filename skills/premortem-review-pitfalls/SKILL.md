---
name: premortem-review-pitfalls
description: "Use when a plan, launch, migration, purchase or other hard-to-undo decision is stress-tested before it is committed (pre-mortem, red team, what could go wrong): the attack run by someone who did not make the decision from a brief that states facts and does not argue, a date to be judged by, a sweep of every risk area with the empty ones accounted for, no quota of risks, likelihood, severity and detectability scored separately, tigers, paper tigers and elephants, load-bearing claims attacked after a steelman, the cheapest test and a kill criterion, and a verdict decided last and printed first."
---

# premortem-review-pitfalls

Not a step of the pipeline: a craft block for the review that tries to break a decision before it is taken.
The three sections share one premise: **a risk list written by the people who made the plan, or padded to look
thorough, protects the plan and not the decision**, so the attack is independent, anchored in a brief of
facts, and ends on a verdict the author cannot skim past. Reviewing a failure after it happened is
`blameless-incident-review-pitfalls`; checking whether a discovery-stage belief holds is
`assumption-validation-pitfalls`.

## When
- A decision is about to be agreed that is hard to undo: a contract, a launch, a migration, a price change.
- Someone asks "what are we missing", "poke holes in this", for a pre-mortem or a red team.
- A risk register exists but every risk is rated medium and nothing was ever dropped.
- A plan has been reviewed only by the people who wrote it.

## Steps

**Read only the section the task meets.** §1 comes first when a review is being set up; §2 and §3 follow in
order when the attack is written.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The brief and who runs the attack: independence, brief fields, date to be judged by, depth | a pre-mortem is being set up or its brief checked | [`01-brief-and-independence.md`](./references/01-brief-and-independence.md) |
| 2 | The sweep and the risk cards: outside view, nine areas, no quota, tigers, paper tigers and elephants, the card | risks are being found and written | [`02-sweep-and-risk-cards.md`](./references/02-sweep-and-risk-cards.md) |
| 3 | Attack the assumptions and the verdict: load-bearing claims, steelman, cheapest test, kill criterion, verdict and report | the plan's assumptions are attacked or the report is composed | [`03-red-team-and-verdict.md`](./references/03-red-team-and-verdict.md) |

## Output / checkpoint
A pre-mortem is done when a reader who did not make the decision can answer from the first screen: the verdict
and why, the worst case, the biggest risks (few, each with a chain), the belief nobody is questioning, and what
to fix before committing; and from the detail: which class of decision this is and what usually kills it,
which areas were swept and what each produced (the empty ones too), the card of each surviving risk with three
separate scores and an early warning, and which claims were attacked with their cheapest test and kill
criterion. Read it once looking for a risk with no anchor in the brief, a score collapsed into "risky", and a
verdict that is not the first thing on the page. Nothing here was verified on a real decision: the check is a
read of the text.

## Guardrails
- Never let the author, or an agent that helped decide, be the independent attacker; when no fresh reader is
  available, say the review is not independent (§1.1).
- Never write a brief that argues for the decision; state facts and mark assumptions (§1.2).
- Never attack a decision that has no date by which success or failure is judged (§1.2).
- Never pad to a quota, and never drop an area from the report because it produced nothing (§2.2).
- Never collapse likelihood, severity and detectability into one word (§2.4).
- Never attack a strawman or invent a weakness; say what holds (§3.1, §3.2).
- Never give a verdict that is assembled from the risks by the reader; decide it last and print it first (§3.4).
- Sources differ on unsure risks ("default to a tiger" against "only what is anchored"); this block follows the
  anchored stance (§2.3).

## Origin
Rewritten from kharmanskyi's open-steps (MIT: os-what-could-go-wrong) and phuryn's pm-skills (MIT: pre-mortem
and strategy-red-team), read 2026-10-16. Both are young 2026 repositories, one author's practice and not
consensus. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
