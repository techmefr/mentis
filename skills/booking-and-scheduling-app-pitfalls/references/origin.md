# booking-and-scheduling-app-pitfalls: origin and source stamps

> Provenance of `skills/booking-and-scheduling-app-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of booking and scheduling applications. No open-source scheduling code or documentation was opened, and no LICENSE file was read because no source was used. |

Neighbouring blocks of this repository were read to avoid duplication: `skills/python-patching-and-time-pitfalls`
and `skills/dotnet-testcontainers-and-time-seam-pitfalls` (time in tests), `skills/laravel-date-via-localised-accessors`
(date display), `skills/laravel-scheduling`, `skills/laravel-idempotent-jobs`, `skills/inventory-stock-app-pitfalls`
(concurrent decrements). None covers designing a booking application, so a new block was justified.

## Removed
1. **Cancellation fees, refund rules and no-show penalties:** not read; flagged as business policy, not legal advice.
2. **Every numeric value** (hold lifetime, lead time, grace period, buffers): set by policy.
3. **Named calendar and booking products and their APIs:** not used.

## Not verified
1. **All points are our own guidance** and were not compared with an open-source scheduling schema.
2. **Zone database and clock-change behaviour** were not re-read against the current release; re-read before
   relying, since rules change by decree.
3. **Nothing was run.** The zone, clock-change, double-booking and hold-expiry tests named in the checkpoint
   were not written or executed.
4. **Framework and database pointers** (range constraints, locks) were not checked against a current release;
   re-read before relying.

## Related blocks
`skills/helpdesk-ticketing-app-build-pitfalls`, `skills/hr-leave-and-time-tracking-app-pitfalls`,
`skills/inventory-stock-app-pitfalls`, `skills/python-patching-and-time-pitfalls`,
`skills/laravel-date-via-localised-accessors`, `skills/laravel-scheduling`.
