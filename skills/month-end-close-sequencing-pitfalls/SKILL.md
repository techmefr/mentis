---
name: month-end-close-sequencing-pitfalls
description: "Use when planning or running a period-end close or building a short-term cash forecast: close tasks as a dependency graph (entries and cut-off, reconciliations, adjustments, draft statements, review, lock), the critical path and how to shorten it, soft close versus hard close, task owner and status, close metrics and retrospective; cash forecast pitfalls such as a guessed opening balance, per-payer payment lag, thin data, undisclosed sources and unnamed risks."
---

# month-end-close-sequencing-pitfalls

A planning block for the order in which a period close happens and for the short-term cash forecast that
should run on clean books afterwards. A close fails less from a hard task than from a task started before
what it depends on is finished, or from an entry posted into a period that was meant to be locked. The block
carries sequencing and tracking method only. It carries no calendar day by day, no tax or equity step, no
default tolerance and nothing about whether a period lock is a legal requirement: those depend on the
organisation, the jurisdiction and the standard, and were not verified. The ledger-side rules a close relies
on are in `business/fintech-compliance` part 3 and the controls around spend in `business/finance-ops`.
Nothing here replaces a chartered accountant, an auditor, or a legal, compliance or financial adviser.

## When
- A close calendar is being drawn up, shortened or repaired.
- A close is running and the question is what is blocked and what is on the critical path.
- Entries keep arriving after the books were supposed to be final.
- A cash forecast for the next weeks is being built, or an existing one looks too optimistic.

## Steps

**Read the part the task meets.** Part 1 for the close; part 2 for the cash forecast.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Close sequencing: dependency order, critical path, soft and hard close, owners and statuses, metrics, retrospective | a close is planned, run or shortened | [`01-close-sequencing.md`](./references/01-close-sequencing.md) |
| 2 | Cash forecast pitfalls: opening balance, per-payer lag, thin data, named sources, named risks | a short-term cash forecast is built or checked | [`02-cash-forecast-pitfalls.md`](./references/02-cash-forecast-pitfalls.md) |

## Output / checkpoint
A close plan is done when every task has an owner, a deadline, a status and, if blocked, its blocker; when the
dependencies between tasks are written down and the critical path is named; when the point at which entries
become final (soft close) and the point at which the period is locked (hard close) are both defined; and when a
retrospective is scheduled. A cash forecast is done when its opening balance is sourced or the output says
there is none, the sources used are listed, and each risk is named. Evidence is a task list in which no task
starts before the tasks it depends on, and a forecast whose headline states what it was built from. Nothing
here was run in a real close: the check is a read of the text.

## Guardrails
- Never start a task whose inputs are not final; sequence by dependency, not by habit (part 1).
- Never post into a locked period; a correction after the lock follows your correction procedure (part 1).
- Never assume an opening balance for a cash forecast; if nobody knows it, say "no opening balance, net change
  only" (part 2).
- Never apply a flat settlement lag to every payer when real dates exist (part 2).
- Never give a forecast range without saying what it is based on, and never present a default range as a
  measured one (part 2).
- This block sets no close duration, tolerance or calendar: set them from your own policy.
- This block does not replace a chartered accountant, an auditor, or a legal, compliance or financial
  adviser; tax, equity and period-lock obligations go to the person qualified for them.

## Origin
Rewritten from the close-management skill (finance) and the cash-flow-snapshot skill (small-business) of
anthropics' knowledge-work-plugins (Apache-2.0), read 2026-10-16. Vendor-authored practice guides, not
standards. 🟡: never run by us; what was removed and what is our own guidance are in
[`references/origin.md`](./references/origin.md).
