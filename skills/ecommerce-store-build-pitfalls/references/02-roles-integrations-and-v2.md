# ecommerce-store-build-pitfalls §2 — Roles, integrations and v2

> Part 2 of `skills/ecommerce-store-build-pitfalls`. Read it when permissions, an integration or the first
> release are planned. Mostly craft knowledge; points 1, 3 and 5 carry facts from the sources in `references/origin.md` (sources 1 to 4), read 2026-10-20. Everything not marked as sourced is our own guidance. Not legal advice.

1. **Guests and accounts both work.** Symptom: a forced account loses buyers, or a guest cannot find their
   order. Fix: guest checkout with an order lookup by a signed link or order number plus email, an optional
   account created after purchase that adopts earlier orders by verified email, and no change to the order when
   the account is created. Account pages show only the logged-in customer's orders; check by id guess (see
   `skills/laravel-scope-dont-check-after-fetch`). The reference framework makes a deliberate trade-off here: it lets any request carrying the store's publishable API key and a valid order id read that order without signing in, so that a guest sees the confirmation page, and relies on random ids as the credential, while listing a customer's orders requires authentication; it documents how to add stricter rules when guest checkout is not offered (source 1). A signed link or order number plus email, as in this point, is the stronger choice.
2. **Staff roles are abilities.** Typical shape: owner, catalogue editor, order handler, support agent,
   read-only finance. Symptom: anyone with a back-office login can refund. Fix: named abilities (edit price,
   refund, cancel, export customers, change stock) checked in one place (see `skills/laravel-permissions-not-roles`),
   a refund limit or second approval by policy, and an audit trail of price, stock, refund and customer-data
   changes with actor and time.
3. **Webhooks and provider events are untrusted and repeatable.** Verify the signature scheme the provider
   documents, accept events out of order, key processing by the event id, return success only after the work is
   stored, and keep the raw payload for a short period. One payment platform's webhook documentation was read (source 2): verify the signature against the raw request body, return success before slow work, keep processed event ids because an event can arrive twice, and do not order events by their creation time. Re-read the current documentation of the provider you use before relying on any detail.
4. **Carriers, tax services and ERP sync are matched by stable ids.** Store the external id on shipment, tax
   result and synced order; make a retry safe; treat an outage as a pending state shown to staff, not as a
   silent skip. Shipping rates are a quote with an expiry stored on the checkout, not a number recalculated at
   payment.
5. **Emails and notices follow the state.** Order confirmation, shipment, refund and return emails are sent
   after the transaction commits (a queued send dispatched inside a transaction can run before the commit unless dispatch is held until commit, source 4), once per event, through notifications (see `skills/laravel-mail-via-notifications`
   and `skills/in-app-notifications-pitfalls`). The confirmation states the same totals, tax treatment and
   return policy the checkout showed.
6. **Imports and exports are staged and scoped.** Catalogue import by spreadsheet: staging, preview, create and
   update counts, external key decides update, empty cell does not blank a field, an undo by import id (see
   `skills/csv-xlsx-import-export-pitfalls`). Customer and order exports require an ability, follow the same
   scope and are logged. Feeds to channels are generated from the product record (see
   `business/ecommerce-store-quality-pitfalls`).
7. **Search and listing pages read an index that follows the catalogue.** Availability, price and visibility
   must update the index on change (see `skills/search-index-sync-pitfalls`); filters in the URL (see
   `skills/filters-search-and-saved-views-pitfalls`). Symptom: a sold-out or hidden product appears in search.
8. **Reports read a defined, dated number.** Revenue names the date field, the states counted, whether tax and
   shipping are included, refunds netted and the currency. One query per metric, reused by the screen and the
   export; money figures come from order lines and refund records, never from a recalculation on the live
   catalogue.
9. **What to split first.** Build in this order and keep each independent: catalogue with variants and prices;
   cart and server-side totals; checkout state with payment and idempotent order creation; stock reservation;
   order snapshots, shipments and emails; refunds and returns; then discounts, multi-currency, multi-country
   tax, channels and analytics. Ship the first five before promotions.
10. **What is regretted at v2.** Price on the product with no currency; totals computed in the browser; order
    created on the redirect; order lines that read the live catalogue; stock decremented after payment only; a
    refund as a negative order; one overloaded status; tax recomputed on old orders; guest orders not
    reachable; permissions as role-name checks in screens. Each is cheap at the first migration and expensive
    once orders exist.
11. **Laravel and Nuxt pointers, short.** In Laravel: an action class per checkout transition inside a database
    transaction, a unique index on the provider payment id, conditional stock updates, queued idempotent jobs
    for webhooks and reconciliation, policies for abilities and a global scope for customer data. In Nuxt:
    never compute or trust a total in the front, show the server's cart and checkout state, send the checkout
    token with every step, keep catalogue filters in the URL, and treat exports as API downloads.
