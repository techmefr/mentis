---
name: hr-leave-and-time-tracking-app-pitfalls
description: "Use when an HR leave or time-tracking application is designed or built: employee, contract and leave-type model, balances as an append-only ledger of accruals, usage and adjustments, accrual as a stated policy, carry-over and expiry, half days and part-time conversion, public holidays and work calendars per location, requests with approval chains, delegation and absence of the approver, overlap and coverage checks, cancellation after approval, timesheets with entries, submission and lock, overtime as a policy, corrections with audit, payroll export, privacy of absence data, roles, what to split first and what gets regretted at v2. Method only; this is not legal advice and no statutory rule, rate or threshold is stated."
---

# hr-leave-and-time-tracking-app-pitfalls

A defensive block for building the application that records who is absent, who worked, and what is left. Leave
and time tools fail in familiar ways: a balance is a number someone edits, an accrual runs twice, a half day
counts as a whole one, a holiday is counted as a day off taken, an approver is on holiday and the request
sits, a cancelled request does not give the days back, a timesheet is edited after payroll took it, and sick
leave reasons are visible to the whole team. The content is craft knowledge with no external source read (see
`references/origin.md`). **Employment law differs by country, sector and contract: this block gives a method
for modelling and testing, states no statutory entitlement, rate, carry-over limit, rest rule or overtime
threshold, and is not legal advice. The rules are owned by HR and legal, written with a date.** Time-zone and
clock-change handling is in `skills/booking-and-scheduling-app-pitfalls`; scheduled accrual jobs are in
`skills/laravel-scheduling`; idempotent runs are in `skills/laravel-idempotent-jobs`; status handling is in
`skills/laravel-recognise-state-machine-or-pipeline`; sensitive fields and row scope are in
`skills/field-and-row-permission-ui-api-pitfalls`; the ledger idea is shared with
`skills/inventory-stock-app-pitfalls`; the payroll export is a file export in
`skills/csv-xlsx-import-export-pitfalls`; request lists and calendars use `skills/data-table-ui-pitfalls` and
`skills/filters-search-and-saved-views-pitfalls`; long request forms are in
`skills/long-and-multistep-form-pitfalls`.

## When
- A tool tracks paid and unpaid leave, sick days or other absences, with balances and approvals.
- Employees or contractors log hours against days, projects or tasks.
- Leave or hours are exported to payroll or an accounting tool.
- An accrual, a carry-over, an approval chain or an overtime rule is added.

## Steps

**Read the part you need before the balance model or the approval flow is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Leave types, balance ledger, accrual, carry-over and expiry, units and part-time, calendars and holidays, requests, overlap, cancellation | a schema or the balance write path is designed | [`01-balances-accrual-and-requests.md`](./references/01-balances-accrual-and-requests.md) |
| 2 | Approval chains and delegation, timesheets and lock, overtime as policy, corrections, payroll export, privacy, roles, what to split first, v2 regrets, framework pointers | approvals, time entry, privacy or the first release are planned | [`02-approvals-timesheets-and-v2.md`](./references/02-approvals-timesheets-and-v2.md) |

## Output / checkpoint
Before building: the leave types with their unit and whether they draw a balance; the balance ledger entry types
with sign and source; the accrual policy written by HR with its effective date; the carry-over and expiry
policy; the work calendar per location and the holiday source; the approval chain with the fallback when an
approver is absent; the timesheet states and the lock point; the payroll export contract; the visibility matrix.
Evidence is a test that a balance equals the sum of its ledger, that an accrual run twice posts once, that a
half day and a part-time day convert as the policy says, that a holiday inside a request is not charged, that a
cancel restores the days, and that a locked timesheet cannot change except by a logged correction. Nothing here
was run by us, and the rules were not checked with HR or legal.

## Guardrails
- This block is not legal advice and states no entitlement, accrual rate, carry-over limit, rest-period or
  overtime rule; HR and legal write them with a date, per jurisdiction.
- Never store the balance as the only truth that is edited in place; derive it from a ledger, or verify a cached
  value against it (§1, point 1).
- Never run accrual without a period key that makes a second run a no-op (§1, point 3).
- Never count a day without the person's own calendar; apply the schedule and the holidays of their location
  (§1, point 5).
- Never lose a request when the approver is absent; define delegation and escalation (§2, point 1).
- Never edit a locked timesheet in place; post a correction with a reason and an actor (§2, point 3).
- Never show the reason for an absence to people who only need to know that someone is away (§2, point 6).
- Never delete a request, entry or balance row with history; reverse it (§1, point 8).

## Origin
Written from craft knowledge of building leave and time-tracking applications; no open-source HR or
timesheet documentation and no labour-law text was read, so no source is credited and no text was taken. See
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
