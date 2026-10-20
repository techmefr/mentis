---
name: price-change-and-billing-pitfalls
description: "Use when a price of a software product is about to be raised, cut or restructured for customers who already pay, or when discounts, annual plans, proration, credits or usage invoices are being set up: a price change shipped to everyone at once, grandfathering with no end date, a customer notice that hides the change, a discount with no floor or owner, a mid-cycle change whose invoice nobody previewed, a 'was / now' price with no price history. Staged rollout, grandfathering with an end date, customer communication, discount and annual-plan discipline, billing mechanics checklist, honest total and reference prices. Method only, not legal advice."
---

# price-change-and-billing-pitfalls

Business layer (`business/README.md`), marketing. A price change usually fails in the rollout and in the billing
mechanics, not in the new number. This block is the protocol for changing a price that people already pay, for
discounts and annual plans, for checking what the billing system will do with a change, and for showing a price
without misleading the buyer. Which tiers exist, what the price scales with and how much a buyer would pay is
`business/pricing-and-packaging-pitfalls`; tax on a reduced price is `skills/vat-handling-in-software-pitfalls`;
whether a claim on a page is true is `business/marketing-claim-substantiation-pitfalls`; defining revenue and
churn after the change is `skills/saas-metric-definition-pitfalls`; the release note itself is
`business/release-communication`.

It states method only. It carries no benchmark, no discount percentage, no notice period, no churn figure and no
test slice size, because the sources gave such numbers without a derivation. Consumer-law points are marked
`method only, re-read before relying`; the one rule whose text was read (§6.3) is the only one stated. It is not
legal advice, and it does not replace the person who owns pricing, the contracts or the billing system.

## When
- A price, a plan or a billing period is about to change for existing customers.
- A discount, a promotion or an annual-plan offer is being created or renewed.
- A billing system is configured for upgrades, downgrades, credits or usage.
- A page, an email or a checkout shows a reduced price or a total.

## Steps

**Read only the section the task meets.** §1 to §3 for a price change; §4 for any discount; §5 before a billing
configuration or a customer-facing example; §6 before a price is displayed.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | A price change as a rollout: new customers first, a small slice of existing accounts, waves, a read each cycle, a stated off-ramp | a price will change for people who already pay | [`01-staged-rollout.md`](./references/01-staged-rollout.md) |
| 2 | Grandfathering as a decision with an end date: who, at what price, until when, what triggers the move, contract check | some customers will keep an old price | [`02-grandfathering-with-an-end-date.md`](./references/02-grandfathering-with-an-end-date.md) |
| 3 | The customer notice: what changes, when, what it means for this customer, choices, owner, timing | a notice, email or banner is being written | [`03-customer-communication.md`](./references/03-customer-communication.md) |
| 4 | Discounts and annual plans: floor, owner, expiry, the renewal anchor, early cancellation | a discount or an annual offer is created or renewed | [`04-discounts-and-annual-plans.md`](./references/04-discounts-and-annual-plans.md) |
| 5 | Billing mechanics checklist: proration, credits and debits, preview, unpaid invoices, usage not prorated, proration switched off | a plan change or a billing configuration is being designed or explained | [`05-billing-mechanics.md`](./references/05-billing-mechanics.md) |
| 6 | Showing prices: total from the first price shown, price history, the text of the EU price-reduction rule, method for was/now | a price, a reduction or a checkout total is about to be displayed | [`06-showing-prices.md`](./references/06-showing-prices.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: for a price change, a rollout plan (cohorts, order, what
is read each cycle, the off-ramp), a grandfathering record (who, price, end date, trigger, contract check) and
the notice draft; for a discount, its floor, owner, expiry and renewal price; for a billing change, a preview of
the invoice a real customer would get; for a displayed reduction, the price history it is compared with. The
owner of pricing decides; contract and consumer-law readings go to the person who owns legal.

## Guardrails
- Roll a change out in stages: new customers, then a small slice of existing accounts, then waves, with a read
  and an off-ramp each cycle. Never switch every account on one day because the new number tested well on
  prospects (§1).
- Write a grandfathering record with an end date and a trigger, and read the contract for price-freeze and notice
  terms. Never leave "kept at the old price" as an open-ended promise or guess what a contract allows (§2).
- Tell the customer what changes, when, what it means for them, what they can choose and who to ask. Never
  present a forced move as a favour or bury the new price in a feature announcement (§3).
- Give every discount a floor, an owner and an expiry, and write the price the renewal returns to. Never let a
  deal discount silently become the new list price (§4).
- Preview the invoice a change will produce, with a fixed date, before applying it. Never explain a proration
  from memory or promise a refund the system will not make (§5).
- Show the total a buyer will pay from the first price displayed, and keep a price history behind every "was /
  now". Never invent or inflate a reference price (§6).
- Re-read any consumer-law rule at its source before relying on it. Never state an article, a period or a
  threshold from memory (§6.3).
- This block is a method written from two young public repositories and two vendor pages, never run on a real
  price change by us. Source status and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Rewritten in our words from the price-increase and rollout notes of an MIT marketing skills repository, the
packaging notes of an MIT commercial skills repository, two billing-vendor documentation pages and the text of
Article 6a of Directive 98/6/EC as inserted by Directive 2019/2161, read 2026-10-20. 🟡: never run by us. Details
in [`references/origin.md`](./references/origin.md).
