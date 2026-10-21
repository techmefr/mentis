# marketplace-app-build-pitfalls §1 — Model and pitfalls

> Part 1 of `skills/marketplace-app-build-pitfalls`. Read it when a schema or a money flow is designed. Mostly
> craft knowledge; points 1, 5, 6 and 8 and the new points 14 and 15 carry facts from pages of one payment platform's documentation and an open-source commerce framework's recipe, read 2026-10-20 and restated in our words (`references/origin.md`, sources 1 to 5). Everything not marked as sourced is our own guidance. Each point gives the symptom, the check and the fix. Not legal advice.

1. **One identity, several capabilities.** Symptom: a seller who wants to buy needs a second account with a
   second email, or a user is both sides of the same order. Check: create one user who sells and buys, and try
   to buy from themselves. Fix: a user (login, contact data) with a seller profile and a buyer profile as
   separate records, capabilities granted per profile, a rule that the buyer and seller of one order differ, and
   an organisation record when a seller is a company with several staff (staff roles belong to the seller
   organisation, not to the platform).
2. **A listing has a lifecycle and a snapshot.** States such as draft, pending review, active, paused, sold or
   out of stock, removed. Symptom: an edit after a sale changes what the buyer thought they bought. Fix:
   transitions checked in one place (see `skills/laravel-recognise-state-machine-or-pipeline`), and on order
   creation copy title, price, currency, variant, seller and the key attributes onto the order line; the order
   reads its own copy, not the live listing. Stock or availability for a unique item needs a reservation so two
   buyers cannot both win (see `skills/inventory-stock-app-pitfalls`; for time slots,
   `skills/booking-and-scheduling-app-pitfalls`).
3. **The order is a record with two parties and its own state machine.** Typical states: created, awaiting
   payment, paid, accepted by seller, shipped or delivered, completed, cancelled, refunded, disputed.
   Symptom: "paid" and "completed" mean the same thing, so a payout fires on payment. Fix: define the state
   list with entry and exit conditions and allowed next states, keep the state history as rows, give each
   state a timeout where a party can stall (seller never accepts, buyer never confirms), and let a timeout
   move the order by a visible rule, not by silence.
4. **Fees are a snapshot, not a rate lookup.** Symptom: the commission changes in settings and last month's
   reports and payouts re-price. Check: change the rate, then open an old order. Fix: store on the order the
   fee rule id, the rate, the base the fee applies to (item, shipping, tax or not), the computed amount, the
   currency and the rounding method; make who pays the fee (seller deducted, buyer added) an explicit field;
   treat a fee-free promotion as a rule with an end date, not a zero typed by hand. Rounding and allocation of
   a fee across lines follow `skills/money-arithmetic-and-rounding-pitfalls`.
5. **Money has a currency, exact arithmetic and an idempotency key.** Symptom: a retry or a replayed
   provider event moves money twice, or an amount in one currency is added to another. Fix: integer minor units
   plus a currency code on every amount, one internal ledger of entries (buyer charge, fee, seller share,
   refund, payout) that sum to zero per order, and a unique key on each provider event id and transfer id so a
   duplicate is a no-op (see `skills/laravel-idempotent-jobs`, `skills/unknown-payment-outcome-pitfalls` and
   `skills/ledger-pending-and-batch-ordering-pitfalls`). Reconcile the internal ledger against the provider's
   reports on a schedule; a difference is an alert, not a rounding note. The payment platform documents idempotency keys on write requests: the first result is saved and replayed on a retry with the same key, including 500 errors, and a key reused with different parameters is refused; the result is saved only once the endpoint began executing, so a request refused at validation can be retried (source 4).
6. **Payout is a state machine with a release condition.** Symptom: the seller is paid, then the buyer
   refunds and the platform is out of pocket, or the payout is stuck for weeks with no reason shown. Fix: states
   such as pending, held, releasable, in transit, paid, failed, reversed; the held amount belongs to a defined
   order; the release event is recorded (delivery confirmed, buyer confirmation, a hold window elapsed, no open
   dispute) and checked at release time, not only at order time; a failed payout keeps its reason and a retry
   path; a negative balance (refund after payout) is a ledger entry carried to the next payout, with a policy
   for when it cannot be recovered. The platform's dispute documentation shows why the hold must outlast the delivery: a card payment can be disputed for months after the payment (the page calls 120 days the window common for card payments, and for a future event or service the window starts on the event date, not the payment date), and a dispute debits the disputed amount plus a fee at once (source 2); its refund documentation adds that a refund uses available balance and waits as pending for card payments if the balance is too low, while on destination charges and separate charges and transfers the platform, not the seller, is debited for refunds, and the platform has to reverse the related transfers to recover that amount from the seller, so a refund flow that skips the reversal leaves the platform paying (sources 1 and 3). Whether the platform may hold funds itself or must use a regulated
   split-payment product is a legal and provider question; design so the hold lives with the provider if that
   is the answer, and state it in the specification.
7. **Seller onboarding gates payouts, not listings.** Symptom: a seller sells for a month and then cannot be
   paid because identity checks were never done. Fix: a verification status on the seller profile with
   statuses (not started, submitted, verified, restricted), shown to the seller, and a rule that orders can be
   taken but payouts wait for verification; store only the provider's verification reference, not the identity
   documents, unless the platform has to hold them (see `business/data-protection`).
8. **A dispute is an object with states, evidence and deadlines.** Symptom: an unhappy buyer emails support,
   the seller never answers and the order sits for ever. Check: open a dispute and follow it with no action
   from either side. Fix: dispute states (opened, seller response due, evidence review, decided, closed,
   escalated), a deadline and an owner per state, evidence as typed attachments with who and when (see
   `skills/file-upload-ui-pitfalls`), the order's payout frozen while a dispute is open, a decision record
   (outcome, amount, reason) that produces ledger entries, and a path to the payment provider's own chargeback
   process which has its own clock, tracked separately. The platform's documentation confirms the separate clock: after a chargeback there is a limited time to answer the issuer (usually 7 to 21 days depending on the card network) and a longer time for the issuer to decide (usually 60 to 75 days), so the whole cycle can reach two to three months; an active dispute is closed in the seller's favour only by submitting evidence, even when the customer says they withdrew it, and a lost dispute is final (source 2). Decision criteria are policy, written for both
   parties; internal handling resembles `skills/support-queue-design-pitfalls`.
9. **Reviews are tied to a completed order and cannot be bought.** Symptom: a seller with a hundred five-star
   reviews written the same hour, or a buyer penalised after a refused refund. Fix: only the buyer of a
   completed order, once per order, with a time window; seller replies are separate records; no edit after
   publication except a visible edited flag; hide a review only through a moderation action with a reason; an
   aggregate rating is a computed or snapshotted figure with a stated minimum count, never an average of one.
   Symptom to watch: a review request that is conditional on a positive outcome. Detect bursts from one
   address, device or account cluster as signals for moderation, not as automatic deletion. Whether incentives
   or review handling are regulated is a legal question.
10. **Off-platform leakage is a design input, not a content problem.** Symptom: buyers and sellers swap
    contact details in the first message and the fee disappears. Fix: keep messaging on the platform tied to
    the listing or order, mask contact data until an order exists, scan for patterns as a flag for review with
    a warning shown to the sender, and make staying on the platform worth it (protection, payment, reviews)
    rather than relying on blocking alone. A hard block with silent deletion creates support tickets.
11. **Every row belongs to a seller or buyer scope, from the first migration.** Symptom: a seller reads another
    seller's orders through the list, the search, the export or an API id guess. Fix: one scoping function used
    by every read path (see `skills/laravel-scope-dont-check-after-fetch`), abilities such as view orders,
    manage listings, request payout, answer disputes (see `skills/laravel-permissions-not-roles`), and a test per
    path with a second seller logged in. Search indexes carry the same visibility fields (see
    `skills/search-index-sync-pitfalls`).
12. **Delete and erase differently.** Symptom: removing a seller cascades to their orders, reviews and ledger
    entries and totals change. Fix: archive or deactivate users and listings, restrict foreign keys (see
    `skills/laravel-no-cascade-delete`), keep order and ledger records, and run an audited erasure routine that
    anonymises personal fields while keeping the financial record the platform must retain; the retention
    period is a legal question (see `business/data-protection`).
13. **Time and place are stored precisely.** UTC timestamps, the listing's and the user's time zone kept where
    they matter (delivery windows, hold windows), a country on the seller and on the buyer address as data
    (tax treatment and shipping depend on it, `skills/vat-handling-in-software-pitfalls`), and a stable internal
    id that is never the public slug.
14. **Decide who bears refunds, chargebacks and fees before designing the ledger.** Symptom: the ledger assumes the seller
    pays every refund and the platform finds itself debited. Check: for each charge model you plan to use, write who
    holds the money first and whose balance falls on a refund, a chargeback and a processing fee. Fix: the payment
    platform's documentation lists three models with different answers: a direct charge to the seller's account, where
    refunds and chargebacks reduce the seller's balance and the platform takes an application fee; a destination charge
    to the platform with an immediate transfer, where refunds and chargebacks reduce the platform's balance and the
    platform bears the fee; and separate charges and transfers, which allow several sellers per payment and a charge
    made before the seller is known, but require watching the platform balance because a transfer can exceed or precede
    the payment, with an option to tie a transfer to a charge so it waits for the funds (source 1). Pick the model with
    the provider and the legal owner, and write it in the specification.
15. **A cart with several sellers becomes one order per seller.** Symptom: one order holds lines of several sellers, so one
    state, one payout and one dispute apply to parties who should not share them. Check: buy from two sellers in one
    checkout and follow each seller's view. Fix: split at order creation into one order per seller, each with its own state
    machine (point 3), fee snapshot (point 4) and payout, created by one operation that rolls back as a whole if any part
    fails. The open-source commerce framework's marketplace recipe describes the same split, done in a workflow with
    rollback and retry steps, and models vendors and their administrators as separate records linked to products and
    orders and authenticated as their own actor type (source 5).
