---
name: marketplace-app-build-pitfalls
description: "Use when a two-sided marketplace application is designed or built: buyer and seller accounts that are one person or two, listings with a lifecycle, an order that carries both parties, payouts and held funds as a state machine, fees stored as a snapshot, disputes with evidence and deadlines, reviews that cannot be bought or faked, off-platform leakage, moderation, and what to split first and regret at v2. Method only; payments regulation, escrow-like licensing and consumer law are not legal advice."
---

# marketplace-app-build-pitfalls

A defensive block for building the application, not for growing a marketplace. A marketplace fails in familiar
ways: a seller is also a buyer and the account model cannot say so, a fee rate changes and old orders re-price,
a payout is sent twice or before a refund window ends, a dispute has no deadline and no evidence, reviews are
written by the seller's cousin, and the two parties swap phone numbers on the first message. The content is
craft knowledge with no external source read (see `references/origin.md`). Single-merchant store mechanics
(cart, checkout, returns) are in `skills/ecommerce-store-build-pitfalls`; store quality audits are in
`business/ecommerce-store-quality-pitfalls`. Money arithmetic is `skills/money-arithmetic-and-rounding-pitfalls`,
an unknown payment result is `skills/unknown-payment-outcome-pitfalls`, tax on sales is
`skills/vat-handling-in-software-pitfalls`, the ledger side of held funds is
`skills/ledger-pending-and-batch-ordering-pitfalls`, tenant boundaries are `skills/laravel-tenant-context-by-default`,
comments and feeds are `skills/comments-and-activity-feed-pitfalls`, uploads are `skills/file-upload-ui-pitfalls`.

## When
- A marketplace, rental platform, service-booking platform or classifieds site is specified or its schema drafted.
- A feature touches payouts, fees, commissions, disputes, reviews or the messaging between buyer and seller.
- A single-vendor store is being opened to third-party sellers.

## Steps

**Read the part you need before the schema or the payment flow is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Accounts and roles, listings, the order with two parties, fees as snapshots, payout and hold states, disputes, reviews, leakage | a schema or a money flow is designed | [`01-model-and-pitfalls.md`](./references/01-model-and-pitfalls.md) |
| 2 | Onboarding and verification, moderation, notifications, integrations, what to split first, v2 regrets, framework pointers | seller onboarding, a provider integration or the first release are planned | [`02-roles-integrations-and-v2.md`](./references/02-roles-integrations-and-v2.md) |

## Output / checkpoint
Before building: the account model (one identity with buyer and seller capabilities, or two), the order state
list with entry and exit conditions and allowed transitions, the payout state list and the event that releases
each payout, the fee snapshot fields, the dispute states with a deadline per state, the review eligibility rule,
and the provider event list with the idempotency key of each. Evidence is a test that a fee change leaves old
orders unchanged, a test that a replayed provider event moves no money twice, a test that a refund blocks or
reverses its payout, and a test that a seller cannot read another seller's orders through list, search and export.
Nothing here was run by us.

## Guardrails
- This block is not legal advice. Whether holding or moving customer funds needs a licence, a regulated partner
  or a hosted split-payment product, what a platform owes consumers, and tax collection duties all depend on the
  jurisdiction; ask a qualified person and state no rule here (see `business/data-protection` for personal data).
- Never model buyer and seller as two unrelated account types; one identity holds capabilities (§1, point 1).
- Never compute a fee from the current rate for a past order; snapshot rate, base and amount on the order (§1, point 4).
- Never treat a provider's success callback as the only truth, and never apply a provider event twice; key every
  money movement by the provider's event or transfer id (§1, point 5).
- Never release a payout without the release condition recorded and the refund window and open dispute checked
  (§1, point 6).
- Never let a dispute stay open without an owner and a deadline (§1, point 8).
- Never accept a review that is not tied to a completed order of that reviewer (§1, point 9).
- Never store money as a float or without a currency (§1, point 5).

## Origin
Written from craft knowledge of building marketplace-style applications; no open-source marketplace
documentation or payment-provider documentation was read, so no source is credited and no text was taken. See
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
