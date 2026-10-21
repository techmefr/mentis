# marketplace-app-build-pitfalls §2 — Roles, integrations and v2

> Part 2 of `skills/marketplace-app-build-pitfalls`. Read it when onboarding, a provider integration or the
> first release are planned. Mostly craft knowledge; point 2 carries facts from the payment platform pages and point 4 one from a framework's queue documentation, in `references/origin.md` (sources 3, 4 and 6), read 2026-10-20. Everything not marked as sourced is our own guidance. Not legal advice.

1. **Roles are abilities per scope.** Typical shape: platform admin, platform support, seller owner, seller
   staff, buyer. Platform support sees orders and disputes but not payout bank details; a seller staff member
   answers messages but cannot change the payout destination. Symptom: one "admin" flag decides everything.
   Fix: named abilities (view order, refund, change payout destination, decide dispute, hide review) checked in
   one place, and every sensitive change on a seller (payout destination, email, verification) written to an
   audit trail with a notification to the seller (see `skills/field-and-row-permission-ui-api-pitfalls`).
2. **The payment provider is an integration with its own state.** Store the provider's account, charge,
   transfer and payout references on your records, treat webhooks as untrusted until verified with the
   provider's signature scheme, handle events out of order and more than once (see
   `skills/unknown-payment-outcome-pitfalls`), and reconcile on a schedule. Keep keys in a secret store, never
   in the repository. That platform's webhook documentation confirms the handling: verify the signature against the raw request body, answer with a success status before slow work, expect the same event twice and keep the ids of processed events, do not rely on delivery order or on the creation timestamp to order events, and expect retries for days (source 4). Check the provider's current documentation for the split-payment and payout features
   before design; only one platform's pages were read here (§1 point 14), so re-read before relying on any other provider.
3. **Moderation is a queue with actions and an audit.** Listings, reviews, messages and sellers can each be
   flagged by users or rules. Symptom: a removed listing leaves no trace and the seller cannot appeal. Fix: a
   flag record, a moderation decision with reason and actor, a notice to the affected user stating the reason
   and the way to contest it, and a restore path. Handle prohibited-item and consumer-protection duties as a
   policy owned by a person who can answer for them; none is stated here.
4. **Notifications follow the state machine.** Each order, payout and dispute transition names who is told,
   through which channel, and what link they get (see `skills/in-app-notifications-pitfalls` and
   `skills/laravel-mail-via-notifications`). A notification is sent after the transaction commits, not inside it. The framework's queue documentation describes the same trap: a job dispatched inside an open transaction can run before the commit and miss its data, and the framework can hold dispatch until commit and discard jobs of a rolled-back transaction, per connection or per job (source 6).
   Symptom: a seller learns of a dispute from the buyer.
5. **Imports and exports follow the same visibility.** Bulk listing upload from a spreadsheet is staged,
   previewed and idempotent (see `skills/csv-xlsx-import-export-pitfalls`); a seller's order export uses the
   same scope as their list and is logged; the seller's payout report matches the ledger, not a separately
   computed figure.
6. **Search and browse are a product surface.** Ranking is policy: say which signals (relevance, price,
   rating, recency, seller quality, paid placement) and mark sponsored results visibly. Filters and saved
   searches are in `skills/filters-search-and-saved-views-pitfalls`; do not let a seller's fee tier silently
   decide ranking without a rule written down.
7. **Reports read a defined, dated number.** Gross merchandise value, net revenue, take rate and active
   sellers each name the date field, the states counted (paid, completed, net of refunds), the currency and the
   scope. Symptom: finance and product show different revenue. Fix: one query per metric reused by screen and
   export, and ledger-derived revenue as the only source for money.
8. **What to split first.** Build in this order and keep each independent: accounts with seller and buyer
   capabilities and scope; listings with lifecycle and snapshot; the order state machine with the internal
   ledger; payment and payout through the provider with held states; disputes and refunds; reviews and
   messaging; then moderation tooling, search tuning, analytics and growth features. Ship the first four with
   manual support before automating disputes.
9. **What is regretted at v2.** Two account types for one person; fees read from a settings table at report time;
   payouts triggered by payment; no internal ledger so finance rebuilds it from provider exports; no dispute
   clock; reviews open to anyone; messaging that exposes contact details; hard-deleted sellers; permissions
   written as role-name checks in screens; no scope on the search index. Each is cheap at the first migration
   and expensive after money has moved.
10. **Laravel and Nuxt pointers, short.** In Laravel: a ledger table with a unique key on provider event id,
    an action class per state transition inside a database transaction, queued jobs that are idempotent for
    payout and webhook handling, policies for abilities, a global scope per seller, and a scheduled
    reconciliation command. In Nuxt: never trust the front to hide another seller's data or to compute a fee,
    show order and payout states from the server's state list, keep list filters in the URL, and treat exports
    as downloads from the API.
