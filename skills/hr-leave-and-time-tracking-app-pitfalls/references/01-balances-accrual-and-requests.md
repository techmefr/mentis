# hr-leave-and-time-tracking-app-pitfalls §1 — Balances, accrual and requests

> Part 1 of `skills/hr-leave-and-time-tracking-app-pitfalls`. Read it when a schema or the balance write path is
> designed. Mostly craft knowledge; points 2 and 6 carry facts from an open-source data model (Apache-2.0), read 2026-10-20 and restated in our words (`references/origin.md`, source 1). Everything not marked as sourced is our own guidance. Not legal advice: no entitlement, rate or limit is stated.

1. **A balance is a ledger.** Symptom: a number on the employee row that people edit, and nobody can say why it
   dropped. Fix: an insert-only table of entries (employee, leave type, signed amount in the policy unit,
   entry type such as accrual, usage, adjustment, carry-over, expiry, reversal, effective date, source request or
   job run, actor, recorded time); the balance is the sum up to a date, so "balance as of last March" has an
   answer. A cached balance is allowed, updated in the same transaction, and verified by a scheduled check that
   reports drift. Corrections are new entries. Same idea as `skills/inventory-stock-app-pitfalls`.
2. **Leave types are data with a unit.** A type has a name, a unit (days, half days, hours), whether it draws a
   balance, whether it needs approval, whether it needs a document, whether it is paid, and a visibility level
   for its label. Symptom: sick leave and annual leave sharing one counter, or hours stored in a days column.
   Fix: the unit is a property of the type, amounts are stored in the smallest unit the type uses, and
   conversion between units happens at the edge by a stated rule. The reference ERP data model keeps leave types as data, in a hierarchy through a parent type, and keeps the reason for a leave in a separate type table (source 1). The unit as a property of the type is our own guidance. The same model has leave records with a start, an end, an approver and a status but no balance, accrual or carry-over table (none found in the file read), so points 1, 3 and 4 rest on our own guidance alone.
3. **Accrual is a policy run once per period.** The policy (how much, how often, from when, prorated for part
   periods, capped or not) is written by HR and versioned with an effective date. Symptom: a scheduled job that
   runs twice after a deploy and grants twice, or a new joiner who gets nothing for the first month. Fix: the
   job posts one entry per employee, type and period key, with a unique constraint on that key so a rerun is a
   no-op (see `skills/laravel-idempotent-jobs`); it can be replayed for a past period after a policy fix by
   posting a difference, not by editing entries; joiners, leavers and contract changes are handled by explicit
   rules written down. Check: run the job twice and across a mid-period start date and assert the totals.
4. **Carry-over and expiry are entries, not silent resets.** Symptom: on the first of the year balances vanish
   with no trace, or an expiry rule removes days that were already requested. Fix: a year-end job posts an
   expiry entry and a carry-over entry per the policy, with the policy's limits as parameters, after counting
   approved future requests as used by their date; show employees the date and the amount that will expire
   before it does. The limits themselves come from HR and legal.
5. **Counting days needs the person's calendar.** Symptom: a Friday-to-Monday request charged four days to someone
   who does not work Fridays, a bank holiday charged as leave taken, a half day counted whole. Fix: a work
   schedule per employee (weekdays and hours, versioned for part-time changes), a holiday calendar per location
   (regional ones differ; the source is maintained and dated, not typed per request), and a day-count function
   that walks the dates, skips non-working days and holidays, applies half-day flags on the first and last day,
   and returns the charged amount in the type's unit. One function backs the form preview, the approval screen
   and the ledger posting. Dates are calendar dates in the employee's location, not instants; see
   `skills/booking-and-scheduling-app-pitfalls` for clock-change effects on hour-based entries.
6. **A request is a state machine.** States: draft, submitted, approved, rejected, cancelled by employee,
   cancelled by approver, taken. Symptom: a request that is "approved" but nobody can say whether the days were
   deducted. Fix: a transition table, a ledger usage entry at approval (or at submission as a reservation, by
   policy), reversed on cancel or reject, and the same function for the day count. See
   `skills/laravel-recognise-state-machine-or-pipeline`. The reference leave record carries the approver and a status beside its date range (source 1). Insufficient balance either blocks or warns by type
   policy, and negative balances are allowed only where the policy says so.
7. **Overlap and coverage.** Reject overlapping requests for one person, across types. Team coverage ("at most
   two people away") is a warning for the approver, not a hard rule, unless the business says so; show who else is
   away in the approval screen without revealing reasons. Symptom: two overlapping requests both approved,
   charging twice. Check: submit overlapping ranges in parallel and assert one passes; use a lock on the
   employee while posting.
8. **Cancel and amend after approval.** An employee cancelling an approved request posts a reversal and tells the
   approver; amending dates is a cancel plus a new request in one action, with the approval needed again if the
   range grows. A request already taken (in the past) is corrected by an HR adjustment with a reason. Never
   delete requests, entries, employees or leave types with history; archive and reverse.
9. **Contract and employment changes.** Joining, leaving, a move between locations, a change of hours and an
   unpaid period all change accrual, schedule and holidays. Symptom: a leaver's balance paid wrongly or not at all.
   Fix: effective-dated contract rows, a leaver process that produces a balance report for HR to decide, and no
   automatic payout rule in the application. The rule is HR's and legal's.
