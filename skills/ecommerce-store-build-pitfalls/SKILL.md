---
name: ecommerce-store-build-pitfalls
description: "Use when a single-merchant online store application is designed or built: product and variant model, price as a record with currency, a cart that survives price and stock changes, checkout as a state machine with payment and order creation kept consistent, order lines as snapshots, stock reservation, fulfilment and shipments, returns and refunds as records, guest versus account, tax as a computed and stored result, and what to split first and regret at v2. Method only; tax, consumer-protection and payments rules are not legal advice."
---

# ecommerce-store-build-pitfalls

A defensive block for building the store application, not for auditing or marketing one. A store built in a
hurry fails in familiar ways: the cart shows a price that is no longer true, two buyers pay for the last item, a
payment succeeds and no order exists, an order changes when the catalogue is edited, a refund is typed as a
negative order, and tax is recomputed on old orders. The content is craft knowledge with no external source read
(see `references/origin.md`). The audit side (catalogue and feed quality, checkout friction, price display) is
`business/ecommerce-store-quality-pitfalls`; opening the store to third-party sellers is
`skills/marketplace-app-build-pitfalls`. Stock mechanics are in `skills/inventory-stock-app-pitfalls`, invoices in
`skills/invoicing-app-build-pitfalls`, an unknown payment result in `skills/unknown-payment-outcome-pitfalls`, tax in
`skills/vat-handling-in-software-pitfalls`, money in `skills/money-arithmetic-and-rounding-pitfalls`, and the
state-machine pattern in `skills/laravel-recognise-state-machine-or-pipeline`.

## When
- A new shop, catalogue with checkout or order system is specified or its schema is drafted.
- A feature touches the cart, the checkout, order states, stock reservation, returns or refunds.
- A store gains new countries, currencies, shipping methods or payment methods.

## Steps

**Read the part you need before the schema or the checkout flow is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Catalogue and variants, prices, cart, checkout state, payment and order consistency, order snapshots, stock, tax result, returns and refunds | a schema or the checkout flow is designed | [`01-model-and-pitfalls.md`](./references/01-model-and-pitfalls.md) |
| 2 | Accounts and guests, roles, fulfilment and carrier integrations, emails, imports, what to split first, v2 regrets, framework pointers | permissions, an integration or the first release are planned | [`02-roles-integrations-and-v2.md`](./references/02-roles-integrations-and-v2.md) |

## Output / checkpoint
Before building: the product, variant and price entities with their keys, the cart and checkout state list with
allowed transitions, the point where stock is reserved and released, the rule that creates an order from a paid
checkout, the snapshot fields of an order line, the tax result fields stored on the order, and the return and
refund states. Evidence is a test that a price change after add-to-cart is shown to the buyer before payment, a
test that a replayed payment event creates one order, a test that two buyers cannot both reserve the last unit,
and a test that editing a product leaves past orders unchanged. Nothing here was run by us.

## Guardrails
- This block is not legal advice. Tax collection, price display, withdrawal and return rights, data protection and
  payment regulation depend on the jurisdiction; ask a qualified person and state no rule here.
- Never read a past order's price, name or tax from the live catalogue; copy them onto the order line (§1, point 6).
- Never create an order from a client-side success message; create it from the verified payment event, once, keyed
  by the provider id (§1, point 5).
- Never trust a price, discount or total sent by the browser; recompute on the server at checkout (§1, point 3).
- Never decrement stock after payment only; reserve at a defined step with an expiry (§1, point 7).
- Never model a refund as an edited or negative order; write refund records against the order (§1, point 9).
- Never store money as a float or without a currency (§1, point 2).

## Origin
Written from craft knowledge of building online-store applications; no open-source e-commerce documentation or
payment-provider documentation was read, so no source is credited and no text was taken. See
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
