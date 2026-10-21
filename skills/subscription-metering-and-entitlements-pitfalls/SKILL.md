---
name: subscription-metering-and-entitlements-pitfalls
description: "Use when a server-side subscription or usage-billing engine is designed or debugged: usage events and their deduplication, event time versus ingest time and late usage, attribution of usage to a customer, aggregation that matches the price metric, graduated versus volume tiers, balances and grants as derived caches, entitlements as the access answer kept apart from the schedule and from the invoice, cancellation where access and billing end on different dates, plan-change timing and billing anchors, previewing an invoice before a change, and dunning as an account-level state machine with a timer. Method only; payments and tax law are not legal advice."
---

# subscription-metering-and-entitlements-pitfalls

A defensive block for the engine behind a subscription product: who is subscribed to what, what they used, what they
may use now, and what they owe. These engines fail in familiar ways: the usage pipeline counts a retried event
twice, a late event lands in an invoice that was already sent, a customer keeps access after cancelling because
nobody decided which date wins, a plan change recreates a row and the entitlement vanishes, a dunning job suspends
service for the wrong customer. The sources are the documentation of two open-source engines, a usage-metering
platform and a subscription-billing platform (both Apache-2.0); their design choices are two designs, not an
industry standard. Method only: payments, tax and consumer-protection law differ by country and this is not legal
advice.

Already covered, not repeated: the invoice model, issuing, credit notes, billing-run idempotency, proration as
stored inputs and payment webhooks are in `skills/invoicing-app-build-pitfalls`; the customer-facing side of a
price change, the preview habit and the proration mechanics of one vendor are in
`business/price-change-and-billing-pitfalls`; metric definitions (MRR, churn) are in
`skills/saas-metric-definition-pitfalls`; money arithmetic is in `skills/money-arithmetic-and-rounding-pitfalls`;
VAT in code is in `skills/vat-handling-in-software-pitfalls`; webhooks from a billing provider are in
`skills/webhook-contract-and-delivery-pitfalls`. This block adds metering, entitlements, the lifecycle of the
subscription itself, and dunning as a state machine.

## When
- A service ingests usage events to bill or to enforce a limit.
- Access to a feature depends on a plan, a trial, a quota or a payment state.
- A plan change, cancellation, pause or trial end is implemented.
- An overdue or dunning flow decides what a non-paying customer can still do.

## Steps

**Read the part for the area you are changing.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Usage metering: event identity and deduplication, event time and late usage, attribution, aggregation versus price metric, tiers, derived balances, reconciliation | a usage pipeline or a usage-based price is designed or debugged | [`01-usage-metering.md`](./references/01-usage-metering.md) |
| 2 | Entitlements, the subscription schedule, access versus billing dates, plan changes, preview, dunning and overdue states | access, cancellation, plan change or non-payment handling is designed | [`02-entitlements-lifecycle-and-dunning.md`](./references/02-entitlements-lifecycle-and-dunning.md) |

## Output / checkpoint
For metering: the event identity and how long a duplicate is remembered, the meter definition per priced metric
(event type, value path, aggregation, dimensions), the cutoff and policy for late usage, the attribution mapping
and its validity dates. For lifecycle: the three owners of state (access, schedule, money), which date wins on each
cancellation policy, the timing options of a plan change, the dunning states with their conditions and actions, and
the timer that re-evaluates them. Evidence is a test that replays the same event ten times and bills once, a late
event after the period closed that follows the written policy, a cancellation test at each policy, a plan change on
the anchor date, and a clock-driven dunning test that advances a state with no payment event. Nothing here was run
by us.

## Guardrails
- This block does not replace an accountant, a tax adviser, a legal or consumer-protection adviser, or a payments
  specialist. It is engineering method, not legal, tax or financial advice.
- Give every usage event an identity and remember it longer than any producer retries. Never count by arrival
  (part 1, rules 1 and 2).
- Bucket usage by event time and write the late-usage policy. Never put late usage into an issued invoice, and
  never drop it silently (part 1, rule 4).
- Keep access, the subscription schedule and the invoice as three records with three owners, reconciled
  asynchronously. Never let one boolean answer all three (part 2, rules 1 and 2).
- Decide per cancellation policy which date ends access and which ends billing, and write it down. Never leave it
  to whichever code path ran (part 2, rule 3).
- Preview the invoice a change produces before applying it, with a fixed date. Never explain an amount from memory
  (part 2, rule 11).
- Drive dunning from state plus a timer, not from payment events alone. Never rely on a payment event arriving to
  advance an overdue account (part 2, rule 13).
- Treat derived balances and caches as rebuildable. Never make correctness depend on which snapshots exist (part 1,
  rule 9).
- Do not copy a window, a retention period or a tier boundary from a source; set them from the contract and policy.

## Origin
Rewritten from the architecture and domain notes of the OpenMeter repository (`openmeterio/openmeter`,
Apache-2.0) and the subscription, entitlement, overdue and usage pages of the Kill Bill documentation
(`killbill/killbill-docs`, Apache-2.0), read 2026-10-20, plus our own guidance, flagged in the text. The review
list named a different repository for the metering platform; the correct one was read and its LICENSE file
checked. Full provenance, removals and what is not verified are in [`references/origin.md`](./references/origin.md).
🟡: never run by us.
