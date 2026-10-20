---
name: invoicing-app-build-pitfalls
description: "Use when an invoicing or billing application is designed or built: invoices, credit notes, recurring subscriptions and usage billing, payments and allocation, dunning. Draft versus issued invoice, numbering at issue, immutable issued invoices corrected by credit note, price and tax snapshots, rounding and currency, proration, partial payments and unapplied cash, idempotent billing runs, payment-provider webhooks, roles, imports and exports, what to split first and what gets regretted at v2. Method only; invoice content, VAT rates, numbering continuity and retention rules are not stated and this is not legal advice."
---

# invoicing-app-build-pitfalls

A defensive block for building the application that issues invoices and collects what they ask for. These tools
fail in familiar ways: an issued invoice is edited and no longer matches the PDF, the monthly run bills a
customer twice after a crash, a partial payment is applied to the wrong invoice, a prorated amount rounds
differently on screen and in the export, and a webhook replay marks an invoice paid twice. The content is mostly craft knowledge; some points are checked against open-source billing sources and a payment vendor's documentation (see `references/origin.md`). The document backbone shared with orders
is in `skills/light-erp-document-flow-pitfalls`; money arithmetic is in
`skills/money-arithmetic-and-rounding-pitfalls`; VAT handling in code is in `skills/vat-handling-in-software-pitfalls`;
structured e-invoicing obligations are in `skills/e-invoicing-obligations-pitfalls`; the tax and ledger side of
the exported data is in `skills/gl-subledger-reconciliation-pitfalls`. Subscription metrics are in
`skills/saas-metric-definition-pitfalls`.

## When
- A tool issues invoices or credit notes, with or without subscriptions or metered usage.
- A billing run, a payment webhook, a reminder schedule or a refund flow is built.
- An export to an accountant, a tax portal or an e-invoicing platform is planned.

## Steps

**Read the part you need before the invoice schema or the billing run is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Invoice model, draft versus issued, numbering, snapshots, credit notes, rounding, currency, payments, tenants | a schema, an issue step or a payment flow is designed | [`01-invoice-model-and-payments.md`](./references/01-invoice-model-and-payments.md) |
| 2 | Billing runs, webhooks, roles, imports and exports, what to split first, v2 regrets, framework pointers | a recurring run, an integration or the first release are planned | [`02-runs-integrations-and-v2.md`](./references/02-runs-integrations-and-v2.md) |

## Output / checkpoint
Before building: the invoice lifecycle with who may issue and void, the numbering policy obtained from the
accountant, the snapshot fields, the correction mechanism, the rounding rule, the payment allocation rule, and
the idempotency key of each billing run. Evidence is a test that an issued invoice is read-only, a
parallel-issue test that never repeats a number, a billing-run test that is killed halfway and rerun without
a double charge, a webhook replay test, and a rounding test where lines and total agree. Nothing here was run
by us.

## Guardrails
- This block is not legal advice and states no mandatory mention, VAT rate, numbering-continuity or retention
  rule. Get them from the accountant and the tax authority and date what you read (see
  `skills/e-invoicing-obligations-pitfalls`).
- Never edit an issued invoice; issue a credit note and, if needed, a new invoice (§1, point 4).
- Never number a draft, and never allocate numbers outside the issuing transaction (§1, point 2).
- Never recompute an issued invoice from current prices, rates or customer data (§1, point 3).
- Never let a billing run lack an idempotency key per customer and period (§2, point 1).
- Never mark an invoice paid from a webhook without verifying its signature and deduplicating the event id
  (§2, point 3).
- Never store money as a float or without a currency (§1, point 6).
- Never delete an issued invoice or a customer who has one; archive (§1, point 9).

## Origin
Written from craft knowledge of building invoicing and billing applications, then checked on 2026-10-20 against
the Kill Bill documentation and the Apache OFBiz data model (both Apache-2.0) and three pages of a payment
vendor's documentation (facts only), credited in the origin file; no text was taken. See
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
