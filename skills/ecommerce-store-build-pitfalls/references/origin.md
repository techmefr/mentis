# ecommerce-store-build-pitfalls: origin and source stamps

> Provenance of `skills/ecommerce-store-build-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of building online-store applications. No open-source e-commerce code, payment-provider documentation or platform policy was opened; no LICENSE file was read because no source was used. |

Neighbouring blocks of this repository were read to avoid duplication: `business/ecommerce-store-quality-pitfalls`
(audit of catalogue, feed, checkout friction and price display; this block is the build counterpart and links to it
rather than repeating it), `skills/inventory-stock-app-pitfalls`, `skills/invoicing-app-build-pitfalls`,
`skills/unknown-payment-outcome-pitfalls`, `skills/vat-handling-in-software-pitfalls` and
`skills/money-arithmetic-and-rounding-pitfalls`. No block covered designing the store application itself (cart,
checkout state, order snapshots, reservation, refunds), so a new block was justified.

## Removed
1. **Every numeric threshold, expiry, refund limit and return window.** None is stated; set them by policy.
2. **Any statement of tax, consumer-protection, withdrawal-right or payments law.** Not read; method only.
3. **Named platform, plugin or provider features:** not used.

## Not verified
1. **All points are our own guidance** and were not compared with any open-source store schema.
2. **Legal and tax questions** (rates, place of supply, price display, return rights, retention, erasure) belong
   to a qualified person; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Provider behaviour** (event delivery, refunds) and **framework pointers** (Laravel, Nuxt) were not checked
   against current documentation; re-read before relying.

## Related blocks
`business/ecommerce-store-quality-pitfalls`, `skills/marketplace-app-build-pitfalls`,
`skills/inventory-stock-app-pitfalls`, `skills/invoicing-app-build-pitfalls`, `skills/unknown-payment-outcome-pitfalls`,
`skills/laravel-no-cascade-delete`, `business/data-protection`.
