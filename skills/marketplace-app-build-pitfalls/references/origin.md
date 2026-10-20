# marketplace-app-build-pitfalls: origin and source stamps

> Provenance of `skills/marketplace-app-build-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of building marketplace-style applications. No open-source marketplace code, payment-provider documentation or platform policy was opened; no LICENSE file was read because no source was used. |

Neighbouring blocks of this repository were read to avoid duplication: `skills/crm-app-build-pitfalls` and
`skills/invoicing-app-build-pitfalls` (shape and depth), `business/ecommerce-store-quality-pitfalls` (store
quality audit, not building), `skills/unknown-payment-outcome-pitfalls`, `skills/vat-handling-in-software-pitfalls`,
`skills/money-arithmetic-and-rounding-pitfalls` and `skills/ledger-pending-and-batch-ordering-pitfalls`. The
overlap check found no block that covers designing a two-sided marketplace application, so a new block was justified.

## Removed
1. **Every numeric threshold, fee rate, hold period and deadline.** None is stated; set them by policy.
2. **Any statement of payments, escrow, licensing, tax, consumer-protection or review law.** Not read; method only.
3. **Named platform or provider features and fee schedules:** not used.

## Not verified
1. **All points are our own guidance** and were not compared with any open-source marketplace schema.
2. **Legal and regulatory questions** (holding funds, licensing, consumer rights, tax collection, review
   handling, retention) belong to a qualified person; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Provider behaviour** (split payments, payout timing, webhook delivery) and **framework pointers** (Laravel,
   Nuxt) were not checked against current documentation; re-read before relying.

## Related blocks
`skills/ecommerce-store-build-pitfalls`, `business/ecommerce-store-quality-pitfalls`,
`skills/unknown-payment-outcome-pitfalls`, `skills/ledger-pending-and-batch-ordering-pitfalls`,
`skills/laravel-no-cascade-delete`, `skills/comments-and-activity-feed-pitfalls`, `business/data-protection`.
