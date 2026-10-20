# ecommerce-store-build-pitfalls: origin and source stamps

> Provenance of `skills/ecommerce-store-build-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against an open-source commerce framework's documentation and one payment platform's webhook page. Never run by us: no application was built and no test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | Medusa documentation (`medusajs/medusa`, commit `829a622`): `www/apps/resources/app/commerce-modules/` pages `cart/concepts`, `cart/tax-lines`, `order/order-versioning`, `order/transactions`, `order/secure-order-retrieval`, `order/return`, `payment/payment-collection`, `payment/webhook-events`, `pricing/concepts`, `pricing/tax-inclusive-pricing`, `inventory/inventory-in-flows`, `inventory/reservations-lifecycle` | MIT: file `LICENSE` read (its enterprise carve-out lists role-based access and single sign-on files only, not these pages) | Product options and variants, price per currency with date-bound price lists and a separate tax-inclusive preference, decimal major-unit amounts, cart currency fixed by region, payment webhooks for interrupted checkouts, several payments per collection, versioned order lines with unversioned original details, stock check at cart then reservation at order, tax lines per line and shipping method needing a country, return items with received and damaged quantities, outstanding amount from transactions, order retrieval by random id |
| 2 | Stripe documentation, page "Receive Stripe events in your webhook endpoint" (`docs.stripe.com/webhooks`) | Vendor documentation, no open licence stated: facts only, rewritten, no sentence copied | Raw-body signature check, fast success response, duplicate events, no ordering guarantee |

Neighbouring blocks of this repository were read to avoid duplication: `business/ecommerce-store-quality-pitfalls`
(audit of catalogue, feed, checkout friction and price display; this block is the build counterpart and links to it
rather than repeating it), `skills/inventory-stock-app-pitfalls`, `skills/invoicing-app-build-pitfalls`,
`skills/unknown-payment-outcome-pitfalls`, `skills/vat-handling-in-software-pitfalls` and
`skills/money-arithmetic-and-rounding-pitfalls`. No block covered designing the store application itself (cart,
checkout state, order snapshots, reservation, refunds), so a new block was justified.

## Verified
1. §1 points 1, 2, 5, 6, 7, 8, 9 and 10 and §2 points 1 and 3: backed by sources 1 and 2, as the points now say.

## Corrected
1. §1 point 2: the reference framework stores exact decimal major-unit amounts, so integer minor units is no longer
   presented as the only exact choice.
2. §2 point 3: the "not read" remark now says that one platform's webhook page was read.

## Removed
1. **Every numeric threshold, expiry, refund limit and return window.** None is stated; set them by policy.
2. **Any statement of tax, consumer-protection, withdrawal-right or payments law.** Not read; method only.
3. **Named platform, plugin or provider features:** not used.

## Not verified
1. **Still our own guidance:** the cart state machine and merge rule (§1 point 4), discount rules (point 3, beyond server-side
   totals), address and contact validation (point 11), delete versus erase (point 12), time (point 13), and in §2 staff roles,
   carriers and ERP sync, emails, imports, search, reports, build order and v2 regrets. No other permissive store
   documentation was identified (searched: the Medusa commerce modules tree).
2. **Legal and tax questions** (rates, place of supply, price display, return rights, retention, erasure) belong
   to a qualified person; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed. Refund behaviour of any payment
   provider was not read.
4. **Framework pointers** (Laravel, Nuxt) were not checked against a current release; re-read before relying.

## Related blocks
`business/ecommerce-store-quality-pitfalls`, `skills/marketplace-app-build-pitfalls`,
`skills/inventory-stock-app-pitfalls`, `skills/invoicing-app-build-pitfalls`, `skills/unknown-payment-outcome-pitfalls`,
`skills/laravel-no-cascade-delete`, `business/data-protection`.
