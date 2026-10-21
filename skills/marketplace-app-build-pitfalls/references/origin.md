# marketplace-app-build-pitfalls: origin and source stamps

> Provenance of `skills/marketplace-app-build-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against one payment platform's documentation. Never run by us: no application was built and no test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | Stripe documentation, page "Understand how charges work in a Connect integration" (`docs.stripe.com/connect/charges`) | Vendor documentation, no open licence stated: facts only, rewritten, no sentence copied | The three charge models and whose balance bears refunds, chargebacks and fees, transfers before payment and tying a transfer to a charge |
| 2 | Stripe documentation, page "How disputes work" (`docs.stripe.com/disputes/how-disputes-work`) | Same: facts only | Dispute window in months, immediate debit with a fee, response deadline, evidence as the only way to close, final outcome |
| 3 | Stripe documentation, page "Refund and cancel payments" (`docs.stripe.com/refunds`) | Same: facts only | Refunds drawn from available balance and pending when short, platform debited for refunds on indirect charges |
| 4 | Stripe documentation, pages "Receive Stripe events in your webhook endpoint" (`docs.stripe.com/webhooks`) and "Idempotent requests" (`docs.stripe.com/api/idempotent_requests`) | Same: facts only | Raw-body signature check, fast success response, duplicates, ordering, retries, idempotency keys |
| 5 | Medusa documentation (`medusajs/medusa`, commit `829a622`): `www/apps/resources/app/recipes/marketplace/page.mdx` | MIT: file `LICENSE` read (its enterprise carve-out lists role-based access and single sign-on files only) | Vendor and vendor-admin records linked to products and orders, vendor-only routes, one order per vendor from a multi-vendor cart |
| 6 | Laravel documentation, page "Queues" (`laravel.com/docs/12.x/queues`), first 100000 characters only | Vendor documentation, no open licence read: facts only, restated | Dispatch after commit, per connection or per job; rolled-back transaction discards its jobs |

Neighbouring blocks of this repository were read to avoid duplication: `skills/crm-app-build-pitfalls` and
`skills/invoicing-app-build-pitfalls` (shape and depth), `business/ecommerce-store-quality-pitfalls` (store
quality audit, not building), `skills/unknown-payment-outcome-pitfalls`, `skills/vat-handling-in-software-pitfalls`,
`skills/money-arithmetic-and-rounding-pitfalls` and `skills/ledger-pending-and-batch-ordering-pitfalls`. The
overlap check found no block that covers designing a two-sided marketplace application, so a new block was justified.

## Verified
1. §1 points 5, 6 and 8 and §2 point 2: backed by sources 1 to 4, as the points now say.
2. §2 point 4, notifications after commit: source 6.

## Added
1. §1 point 14, who bears refunds, chargebacks and fees per charge model: source 1.
2. §1 point 15, one order per seller from a multi-vendor cart: source 5.

## Corrected
1. §2 point 2: the "not read" remark now says that one platform's pages were read and that other providers are still unread.

## Removed
1. **Every numeric threshold, fee rate, hold period and deadline.** None is stated; set them by policy.
2. **Any statement of payments, escrow, licensing, tax, consumer-protection or review law.** Not read; method only.
3. **Named platform or provider features and fee schedules:** not used.

## Not verified
1. **Still our own guidance:** one identity with several capabilities (§1 point 1), listing lifecycle and snapshot (point 2),
   the order state machine (point 3), fee snapshots (point 4), seller onboarding gating (point 7), reviews (point 9),
   off-platform leakage (point 10), scopes, delete and time (points 11 to 13), and in §2 roles, moderation, notifications,
   imports, ranking, reports, build order and v2 regrets. No permissive marketplace documentation was identified
   (searched: one payment platform's pages and the Medusa marketplace recipe).
2. **Legal and regulatory questions** (holding funds, licensing, consumer rights, tax collection, review
   handling, retention) belong to a qualified person; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Other providers' behaviour** (split payments, payout timing, webhook delivery) and **framework pointers** (Laravel,
   Nuxt) were not checked against current documentation; re-read before relying.

## Second pass, strict re-read (2026-10-21)

Re-opened: Stripe "Understand how charges work in a Connect integration", "How disputes work", "Refund and
cancel payments", "Receive Stripe events in your webhook endpoint", "Idempotent requests" (English versions); Medusa
marketplace recipe (`LICENSE` MIT with enterprise carve-out re-read); Laravel "Queues".
- Confirmed: refunds and chargebacks reduce the connected account on direct charges and the platform on destination
  charges and on separate charges and transfers; transfers can precede or exceed the charge and can be tied to a charge so
  they wait for its funds; an active dispute closes in the seller's favour only by submitting evidence, a lost dispute is
  final; refunds use available balance and card refunds wait as pending, other methods fail; the recipe splits a cart
  into one order per vendor and uses vendor-only routes with a custom actor type; dispatch after commit and discard on
  rollback.
- Made exact: dispute response time usually 7 to 21 days and issuer decision usually 60 to 75 days depending on the card
  network (whole cycle two to three months); 120 days is the window common for card payments and it starts at the event
  date for a future service; idempotent results are saved only after execution begins.
- Added: on indirect charges the platform must reverse the related transfers to recover a refund from the seller.
- Still unsourced: identity and roles, listing lifecycle, order state machine, fee snapshots, onboarding gating, reviews,
  leakage, scopes, section 2 moderation, ranking, reports.
Counts: 13 claims re-checked, 4 made exact or added, 0 wrong.

## Related blocks
`skills/ecommerce-store-build-pitfalls`, `business/ecommerce-store-quality-pitfalls`,
`skills/unknown-payment-outcome-pitfalls`, `skills/ledger-pending-and-batch-ordering-pitfalls`,
`skills/laravel-no-cascade-delete`, `skills/comments-and-activity-feed-pitfalls`, `business/data-protection`.
