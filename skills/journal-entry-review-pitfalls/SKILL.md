---
name: journal-entry-review-pitfalls
description: "Use when a manual journal entry is about to be posted or reviewed: what every entry must carry (description, calculation, source, period, preparer, approval, reversal flag), the reviewer's checklist (balanced, open period, account fit, reproducible amounts, authority, duplicates), the common errors (wrong period, flipped sign, similar account code, missing reversal, stale recurring estimate, round estimates, FX rate or date, cut-off), and which entries need a higher approver."
---

# journal-entry-review-pitfalls

A review block for manual entries in a general ledger, written for the person who approves one, not for the
person who decides how a transaction is accounted for. It carries the review method only: what the entry must
carry, what the reviewer checks and which errors recur. Every accounting treatment (how to recognise revenue,
depreciate an asset, accrue payroll or capitalise a cost) and every approval limit is deliberately absent:
those depend on the applicable standard and on the organisation's own policy, and were not verified here.
The separation between the person who prepares and the person who approves is in `business/finance-ops` part
1; this block does not repeat it. Nothing here replaces a chartered accountant, an auditor, or a legal,
compliance or financial adviser.

## When
- A manual or recurring entry is being prepared for posting and needs its support assembled.
- Someone is asked to approve an entry and wants a checklist for it.
- An entry was posted and is being checked for a known class of error before the period is locked.
- An approval matrix is being drawn up and the question is which entries deserve a higher approver.

## Steps

**Read the section the task meets.** Part 1 when preparing, part 2 when reviewing.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | What every entry carries, and who approves which kind | an entry is prepared or an approval matrix is drawn | [`01-support-and-authority.md`](./references/01-support-and-authority.md) |
| 2 | The reviewer's checklist and the recurring errors | an entry is reviewed or audited before the period is locked | [`02-review-checklist-and-errors.md`](./references/02-review-checklist-and-errors.md) |

## Output / checkpoint
A review ends in one of three states per entry: approved, returned with named reasons, or escalated to a
higher approver with the reason. The record shows the preparer, the reviewer, the date, and which checklist
lines were checked against the support rather than assumed. Evidence is that a reviewer who was not the
preparer can recompute each amount from the cited support and find the entry balanced, in an open period and
within the preparer's authority. Nothing here was run in a real close: the check is a read of the text.

## Guardrails
- Never approve an entry whose amounts you cannot reproduce from the cited support (part 2).
- Never post to a period that is closed, and never approve an out-of-period entry as if it were routine
  (parts 1 and 2).
- Never accept a round-number estimate, or a recurring one, without checking it still matches the facts
  (part 2).
- Never let the preparer approve their own entry; where headcount forbids it, name the compensating control
  (see `business/finance-ops` part 1).
- This block carries no accounting treatment and no approval limit: set both from your accounting policy and
  the applicable standard.
- This block does not replace a chartered accountant, an auditor, or a legal, compliance or financial
  adviser; an entry that touches tax, payroll or a consolidation goes to the person qualified for it.

## Origin
Rewritten from the journal-entry-prep skill of anthropics' knowledge-work-plugins (Apache-2.0), read
2026-10-16. A vendor-authored practice guide, not an accounting standard. 🟡: never run by us; what was
removed and what is our own guidance are in [`references/origin.md`](./references/origin.md).
