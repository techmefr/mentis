# ecommerce-store-build-pitfalls: origin and source stamps

> Provenance of `skills/ecommerce-store-build-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against an open-source commerce framework's documentation and one payment platform's webhook page. Never run by us: no application was built and no test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | Medusa documentation (`medusajs/medusa`, commit `829a622`): `www/apps/resources/app/commerce-modules/` pages `cart/concepts`, `cart/tax-lines`, `order/order-versioning`, `order/transactions`, `order/secure-order-retrieval`, `order/return`, `payment/payment-collection`, `payment/webhook-events`, `pricing/concepts`, `pricing/tax-inclusive-pricing`, `inventory/inventory-in-flows`, `inventory/reservations-lifecycle` | MIT: file `LICENSE` read (its enterprise carve-out lists role-based access and single sign-on files only, not these pages) | Product options and variants, price per currency with date-bound price lists and a separate tax-inclusive preference, decimal major-unit amounts, cart currency fixed by region, payment webhooks for interrupted checkouts, several payments per collection, versioned order lines with unversioned original details, stock check at cart then reservation at order, tax lines per line and shipping method needing a country, return items with received and damaged quantities, outstanding amount from transactions, order retrieval by random id |
| 2 | Stripe documentation, page "Receive Stripe events in your webhook endpoint" (`docs.stripe.com/webhooks`) | Vendor documentation, no open licence stated: facts only, rewritten, no sentence copied | Raw-body signature check, fast success response, duplicate events, no ordering guarantee |
| 3 | Stripe documentation, pages "Refund and cancel payments" (`docs.stripe.com/refunds`) and "Fulfill orders" (`docs.stripe.com/checkout/fulfillment`), read in their French versions | Vendor documentation, no open licence stated: facts only, rewritten, no sentence copied | Several refunds allowed but total capped at the original amount, refunds can fail later with a failure reason; webhooks required for fulfilment, redirect page may also trigger it, fulfilment function must tolerate repeat and concurrent calls |
| 4 | Laravel documentation, page "Queues" (`laravel.com/docs/12.x/queues`), first 100000 characters only | Vendor documentation, no open licence read: facts only, restated | Dispatch after commit, discarded on rollback |

Neighbouring blocks of this repository were read to avoid duplication: `business/ecommerce-store-quality-pitfalls`
(audit of catalogue, feed, checkout friction and price display; this block is the build counterpart and links to it
rather than repeating it), `skills/inventory-stock-app-pitfalls`, `skills/invoicing-app-build-pitfalls`,
`skills/unknown-payment-outcome-pitfalls`, `skills/vat-handling-in-software-pitfalls` and
`skills/money-arithmetic-and-rounding-pitfalls`. No block covered designing the store application itself (cart,
checkout state, order snapshots, reservation, refunds), so a new block was justified.

## Verified
1. §1 points 1, 2, 5, 6, 7, 8, 9 and 10 and §2 points 1 and 3: backed by sources 1 and 2, as the points now say.
2. §1 point 9 (refund cap, failed refunds) and point 5 (fulfilment from events): source 3. §2 point 5 (after commit): source 4.

## Corrected
0. §1 point 5 (second pass): the block said to confirm from the signed event, not the redirect; the payment platform's guide uses both, the event as the guarantee and the redirect as an extra trigger of the same idempotent step. The point now says so.
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
3. **Nothing was run.** The tests named in the checkpoint were not written or executed. Refund behaviour of other payment
   providers was not read (one platform's refund page was).
4. **Framework pointers** (Laravel, Nuxt) were not checked against a current release; re-read before relying.

## Second pass, strict re-read (2026-10-21)

Re-opened: Medusa `cart/concepts`, `cart/tax-lines`, `order/order-versioning`, `order/transactions`,
`order/secure-order-retrieval`, `order/return`, `payment/payment-collection`, `payment/webhook-events`,
`pricing/concepts`, `pricing/tax-inclusive-pricing`, `inventory/*`; Stripe "Refund and cancel payments", "Fulfill
orders" and the webhook page (English versions); Laravel "Queues".
- Corrected: the pricing page says amounts are stored "as an integer in major units" while its own example is 20.5, so the
  block no longer claims exact decimals; it tells the reader to check the data type.
- Corrected: currency-matching on cart creation is dated by its page to Medusa v2.21.0.
- Confirmed: option and variant split, price sets per currency, date-bound price lists, separate tax-inclusive
  preference, tax lines per item and shipping method with no tax before a country is set, order and order-item versioning
  with the original line unversioned, outstanding amount as a sum of transactions, guest order retrieval by random id,
  received and damaged quantities on returns, one payment collection with several sessions and payments, payment webhooks
  for interrupted front-end payments, fulfilment from webhooks with a redirect as an extra trigger and a function that must
  tolerate repeated and concurrent calls, several refunds capped at the original amount and a card refund that can fail.
- Still unsourced: cart state machine and merge, discount rules, address validation, delete versus erase, time, section 2
  staff roles and integrations.
Counts: 16 claims re-checked, 2 corrected.

## Related blocks
`business/ecommerce-store-quality-pitfalls`, `skills/marketplace-app-build-pitfalls`,
`skills/inventory-stock-app-pitfalls`, `skills/invoicing-app-build-pitfalls`, `skills/unknown-payment-outcome-pitfalls`,
`skills/laravel-no-cascade-delete`, `business/data-protection`.
