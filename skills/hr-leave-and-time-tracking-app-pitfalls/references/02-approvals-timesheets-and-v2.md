# hr-leave-and-time-tracking-app-pitfalls §2 — Approvals, timesheets and v2

> Part 2 of `skills/hr-leave-and-time-tracking-app-pitfalls`. Read it when approvals, time entry, privacy or the
> first release are planned. Craft knowledge, no external source read. Not legal advice.

1. **Approval chains need a fallback.** Symptom: a request waits for weeks because the manager is away or has left.
   Fix: the approver is derived from a reporting line effective at submission, with a delegate that the approver
   or HR can set for a date range, an escalation to the next level after a stated age, a reminder before
   escalation, and a rule that nobody approves their own request. Multi-step chains (manager then HR) record each
   step as an event with actor and time. Approval by email link uses a signed one-use token and the same checks
   as the screen. Approval is not edited after the fact: reverse and redo.
2. **Timesheets: entries, then submit, then lock.** An entry is an employee, a date, a duration (or start and
   end), a project or task or cost code, and a note. A timesheet is a period of entries with states open,
   submitted, approved, locked. Symptom: hours edited after payroll took them, or days with 27 logged hours.
   Fix: validation of daily and weekly totals against stated warnings, duplicates detected, entries on leave days
   flagged, submission freezing the entries for the employee, approval by the line, and a lock at the payroll
   cut-off that allows no edit. Durations in minutes as integers, not decimal hours (see
   `skills/money-arithmetic-and-rounding-pitfalls` for the same rounding trap).
3. **Corrections after lock are new records.** Symptom: payroll and the tool disagree because someone fixed an old
   entry in place. Fix: a correction row that references the entry, carries a reason, an actor and the period it
   will be paid in, and appears in the next export as an adjustment; the original stays visible.
4. **Overtime and rest rules are policy, owned by HR.** The application can compute totals against thresholds
   that HR supplies, flag breaches for review and export the figures; it states no threshold, multiplier or
   rest-period rule. Symptom: a hard-coded constant that was right for one country and wrong for the next hire.
   Fix: thresholds and rule sets per location or contract type as dated configuration, with an owner and a
   test using the configured values, not the constants of the code.
5. **Timer versus manual entry.** A running timer stores a start instant and a zone; stopping it creates an entry.
   Symptom: timers left running overnight, or a laptop clock change producing negative durations. Fix: a maximum
   timer age that prompts for correction, server time for start and stop, and editing allowed until submission
   with an audit trail of changes. Clock handling follows `skills/booking-and-scheduling-app-pitfalls`.
6. **Privacy of absence data.** Absence reasons, and especially medical ones, are sensitive personal data. The
   rules for what may be stored, who may see it and for how long are set by the data protection owner and legal;
   not stated here. Fix: the team calendar shows "away" without the type unless the viewer's role needs it, the
   reason and documents sit in a restricted field read by HR only (see
   `skills/field-and-row-permission-ui-api-pitfalls`), exports exclude them by default, and every read of a
   restricted field is logged.
7. **Roles and abilities.** Employee, manager (own reports), delegate, HR, payroll, admin, auditor (read only).
   Abilities: request, approve, reject, adjust a balance, edit policy, see reasons, export, lock a period,
   impersonate. Symptom: a manager approves for someone outside their reporting line, or HR adjusts a balance with
   no trace. Fix: scope by reporting line and location in one place, name abilities as permissions (see
   `skills/laravel-permissions-not-roles`), require a reason on every adjustment, and test each ability on every
   read path: list, calendar, export, API, notification.
8. **Payroll export is a contract.** The export has a fixed column set, an employee key that payroll knows, the
   period, the leave and time totals per type or cost code, corrections as separate lines, and a file id with a
   row count and a checksum. Symptom: a rerun exports the same hours twice or misses a correction. Fix: an
   export run record, rows marked as exported by run id, an idempotent rerun, a dry-run preview, and cells
   quoted against formula injection (see `skills/csv-xlsx-import-export-pitfalls`).
9. **What to split first.** Order: employee, schedule and location calendar; leave types and the ledger with the day
   count function; requests with the state machine and balance posting; approvals with delegation; accrual job
   with its idempotency test; carry-over and expiry; timesheets with submit and lock; corrections; roles and
   privacy; export; overtime flags. Ship the ledger, accrual-twice and day-count tests before any approval flow.
10. **What is regretted at v2.** Balance as an editable column; accrual that is not idempotent; no per-employee
    schedule; holidays typed per request; one leave type for everything; no delegation; timesheets editable after
    payroll; decimal hours; hard-coded legal constants; absence reasons visible to the team; deleted requests; no
    effective dating on contracts. Each is cheap in the first migration and costly after balances exist.
11. **Laravel and Nuxt pointers, short.** In Laravel: a ledger table with no update path, a unique key on
    (employee, type, period) for accrual, a scheduled command per period (see `skills/laravel-scheduling`), a
    state machine for requests, locks on the employee while posting, a global tenant scope (see
    `skills/laravel-tenant-context-by-default`) and policies per ability. In Nuxt: preview the charged amount from
    the server's day-count function, show balances with their as-of date, mask restricted fields from the
    payload rather than hiding them in the client, and never decide an entitlement in the browser.
