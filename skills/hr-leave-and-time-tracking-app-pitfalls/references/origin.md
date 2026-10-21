# hr-leave-and-time-tracking-app-pitfalls: origin and source stamps

> Provenance of `skills/hr-leave-and-time-tracking-app-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against an open-source data model and the iCalendar standard. Never run by us: no application was built and no test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | Apache OFBiz (`apache/ofbiz-framework`, commit `bccb166`): entity definitions in `applications/datamodel/entitydef/humanres-entitymodel.xml` (leave, leave type, leave reason type) and `workeffort-entitymodel.xml` (timesheet, time entry) | Apache-2.0: file `LICENSE` read | Leave records with range, approver and status, hierarchical leave types, a separate reason type, no accrual or balance table, timesheet period with status and approver, entries with decimal hours linked to a task, a timesheet and an invoice line |
| 2 | RFC 5545, iCalendar (IETF, 2009), the end-date property of an event | IETF standard text, read for facts only and restated | End of an event is non-inclusive |

Neighbouring blocks of this repository were read to avoid duplication: `skills/inventory-stock-app-pitfalls`
(the ledger pattern), `skills/booking-and-scheduling-app-pitfalls` (clock handling), `skills/laravel-scheduling`,
`skills/laravel-idempotent-jobs`, `skills/field-and-row-permission-ui-api-pitfalls`. None covers designing a
leave or time-tracking application, so a new block was justified.

## Verified
1. §1 points 2 and 6 (leave types as data, request with approver and status) and §2 point 2 (timesheet, entry shape): source 1.

## Corrected
1. §1: the block now says plainly that the data model read has no balance, accrual or carry-over structure, so the
   ledger, accrual and carry-over points are not confirmed by any source.

## Added
1. §2 point 12, exclusive end date of a leave exported as an all-day event: source 2.

## Removed
1. **Every statutory rule:** entitlements, accrual rates, carry-over limits, rest periods, overtime thresholds and
   multipliers, medical-data rules, retention periods. Not read; each is flagged as a question for HR and legal.
   This is not legal advice.
2. **Every numeric value** (reminder ages, timer limits, daily warning totals): set by policy.
3. **Named HR and payroll products and their APIs:** not used.

## Not verified
1. **Still our own guidance:** the balance ledger, accrual run and carry-over (§1 points 1, 3, 4), the day-count function
   (point 5), overlap, cancel and contract changes (points 7 to 9), and in §2 approval chains, lock and corrections,
   overtime ownership, timers, privacy, roles, payroll export, build order and v2 regrets. No permissive source states them.
2. **Employment law by jurisdiction** was not read; re-read the owner's rules before relying on any default. No other permissive HR or
   timesheet documentation was identified (searched: the data model files above).
3. **Second pass 2026-10-20:** no remaining point states a checkable standard, limit or product behaviour (the rest is design method or policy), so nothing further was sourced.
4. **Nothing was run.** The ledger, accrual-twice, day-count, overlap and lock tests named in the checkpoint were
   not written or executed.
5. **Framework pointers** were not checked against a current release; re-read before relying.

## Second pass, strict re-read (2026-10-21)

Re-opened: OFBiz `humanres-entitymodel.xml` (EmplLeave, EmplLeaveType, EmplLeaveReasonType) and
`workeffort-entitymodel.xml` (Timesheet, TimeEntry) at the trunk; RFC 5545 section 3.8.2.2 and its worked example
(`LICENSE` of the ERP project Apache-2.0 re-read).
- Confirmed: leave record keyed by person, type and from-date with thru-date, approver and status; hierarchical leave
  types; a separate reason type; no balance, accrual or carry-over entity found; timesheet with person, client, period,
  status, approver; time entries with rate type, task, timesheet and invoice line links; DTEND for a VEVENT is the
  non-inclusive end, the standard's example of an all-day range ending July 8 is written with DTEND July 9.
- Corrected: the time entry hours field is declared floating-point, not decimal; the block now says so.
- No other permissive HR source found (searched: the two ERP data model files and the standard).
Counts: 7 claims re-checked, 1 corrected.

Independent verification 2026-10-21: 11 checked, 11 matched, 0 corrected, 0 unverified

## Related blocks
`skills/booking-and-scheduling-app-pitfalls`, `skills/inventory-stock-app-pitfalls`,
`skills/helpdesk-ticketing-app-build-pitfalls`, `skills/laravel-scheduling`, `skills/laravel-idempotent-jobs`,
`skills/field-and-row-permission-ui-api-pitfalls`.
