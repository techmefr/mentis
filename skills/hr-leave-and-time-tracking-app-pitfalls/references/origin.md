# hr-leave-and-time-tracking-app-pitfalls: origin and source stamps

> Provenance of `skills/hr-leave-and-time-tracking-app-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of leave and time-tracking applications. No open-source HR or timesheet code or documentation was opened, no labour-law text was read, and no LICENSE file was read because no source was used. |

Neighbouring blocks of this repository were read to avoid duplication: `skills/inventory-stock-app-pitfalls`
(the ledger pattern), `skills/booking-and-scheduling-app-pitfalls` (clock handling), `skills/laravel-scheduling`,
`skills/laravel-idempotent-jobs`, `skills/field-and-row-permission-ui-api-pitfalls`. None covers designing a
leave or time-tracking application, so a new block was justified.

## Removed
1. **Every statutory rule:** entitlements, accrual rates, carry-over limits, rest periods, overtime thresholds and
   multipliers, medical-data rules, retention periods. Not read; each is flagged as a question for HR and legal.
   This is not legal advice.
2. **Every numeric value** (reminder ages, timer limits, daily warning totals): set by policy.
3. **Named HR and payroll products and their APIs:** not used.

## Not verified
1. **All points are our own guidance** and were not compared with an open-source HR schema or checked with HR or
   legal.
2. **Employment law by jurisdiction** was not read; re-read the owner's rules before relying on any default.
3. **Nothing was run.** The ledger, accrual-twice, day-count, overlap and lock tests named in the checkpoint were
   not written or executed.
4. **Framework pointers** were not checked against a current release; re-read before relying.

## Related blocks
`skills/booking-and-scheduling-app-pitfalls`, `skills/inventory-stock-app-pitfalls`,
`skills/helpdesk-ticketing-app-build-pitfalls`, `skills/laravel-scheduling`, `skills/laravel-idempotent-jobs`,
`skills/field-and-row-permission-ui-api-pitfalls`.
