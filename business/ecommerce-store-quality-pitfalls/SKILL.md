---
name: ecommerce-store-quality-pitfalls
description: "Use when an online store's catalogue, product feed, checkout, returns or price display is built, audited or changed: a variant with no stock state of its own, a product title written for the supplier, a feed that disagrees with the page, a forced account before payment, shipping cost revealed on the last step, a price shown without the tax treatment the buyer expects, a return policy that contradicts the checkout, a conversion test run for a week on one weekday. Catalogue and feed quality, checkout friction, returns and price display, and store measurement."
---

# ecommerce-store-quality-pitfalls

Business layer (`business/README.md`), marketing. A store is a chain of promises: the listing says what the product
is, the price says what it costs, the checkout takes the money, the return policy says what happens next. Most
losses are gaps between two links: a feed that says in stock while the page says sold out, a total that grows at the
last step. This block is the check to run on a store before launch and after each change to it. Value-added tax in
software is `skills/vat-handling-in-software-pitfalls`; price changes and billing are `business/price-change-and-billing-pitfalls`
and `business/pricing-and-packaging-pitfalls`; claims about a product are `business/marketing-claim-substantiation-pitfalls`;
search visibility is `skills/seo`; experiments are `skills/experiment-design-pitfalls`; funnels are `skills/funnel-and-cohort-definition-pitfalls`.

It states method only. Marketplace and shopping-feed rules are the platform's own, change often and were not read
for this block; consumer-protection, tax and returns law differs by country, so none of it is legal advice.

## When
- A catalogue is created, imported or restructured, or a product feed is sent to a channel.
- A checkout, a cart or a shipping or return policy is designed or changed.
- Prices are displayed in a new country or customer type.
- A conversion drop, an abandoned-cart rate or a return rate is investigated.

## Steps

**Read only the section the task meets.** §1 for catalogue and feeds; §2 for cart and checkout; §3 for prices,
returns and what to measure.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Catalogue and feed: identifiers, variants, titles and attributes, stock, one source of truth, images | products are created, imported or exported to a channel | [`01-catalogue-and-feed-quality.md`](./references/01-catalogue-and-feed-quality.md) |
| 2 | Cart and checkout: surprises at the end, forced accounts, forms, payment and delivery options, errors, mobile | a cart or checkout is built or abandoned carts are studied | [`02-checkout-friction.md`](./references/02-checkout-friction.md) |
| 3 | Price display, returns and measurement: tax treatment, totals, return policy, confirmation, how to test | prices, policies or conversion figures are set or read | [`03-prices-returns-and-measurement.md`](./references/03-prices-returns-and-measurement.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: a list of mismatches found between catalogue, feed, page,
cart and policy, each with the place it was seen; a list of checkout steps with what each asks and when each cost
is shown; and, for a measurement claim, the sample and period it rests on. The store owner decides what to change;
legal and tax points go to a qualified person.

## Guardrails
- Treat the product record as the single source and generate the feed from it. Never maintain a second copy by hand
  (§1).
- Show every cost before the last step. Never reveal shipping, fees or tax for the first time at payment (§2).
- Offer guest checkout. Never force an account to take a payment (§2).
- Show prices with the tax treatment the buyer expects for their market. Never display one figure in the listing and
  another in the total without saying why (§3).
- Make the return policy match the checkout and the confirmation. Never state a window in one place and another in
  a second (§3).
- Test across full weekly cycles and watch returns, not only orders. Never call a variant a winner after a few days
  or on sales alone (§3).
- Method written from general practice, no source taken; status and open points are in
  [`references/origin.md`](./references/origin.md).

## Origin
Written from general e-commerce practice; the MIT marketing repository named by the review was not opened for
this block, and no marketplace documentation was read. 🟡: never run by us. Details in
[`references/origin.md`](./references/origin.md).
