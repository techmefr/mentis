---
name: light-erp-document-flow-pitfalls
description: "Use when a light ERP or back-office application is designed or built around business documents: quote, sales order, delivery, invoice, purchase order, goods receipt, supplier bill. Header and line model, document status machines, numbering series without silent gaps, conversion from one document to the next with quantity tracking, price and tax snapshots on the line, immutable posted documents and corrections by reversal, party master data, multi-tenant and multi-entity boundaries, roles and approvals, imports and integrations, what to split first and what gets regretted at v2. Method only; accounting and tax rules are not stated and this is not legal advice."
---

# light-erp-document-flow-pitfalls

A defensive block for building the document backbone of a small ERP: the chain from quote to order to delivery
to invoice on the sales side, and from purchase order to receipt to supplier bill on the purchase side. Such
tools fail in familiar ways: an edited invoice changes last year's total, numbers skip or repeat, a converted
order can be delivered twice, a price change rewrites old lines, and one customer's documents leak into
another tenant's list. The content is mostly craft knowledge; a few points are checked against two open-source ERP and billing sources (see `references/origin.md`). Invoicing specifics are in `skills/invoicing-app-build-pitfalls`, stock movements in
`skills/inventory-stock-app-pitfalls`, the customer side in `skills/crm-app-build-pitfalls`, money in
`skills/money-arithmetic-and-rounding-pitfalls`, VAT handling in `skills/vat-handling-in-software-pitfalls`.
Reconciling the ledger to its subledgers is in `skills/gl-subledger-reconciliation-pitfalls`.

## When
- A tool is specified that creates quotes, orders, deliveries, purchase orders, receipts or bills.
- A document gets a number, a status, a conversion button, a PDF or an approval.
- A change touches prices, taxes, multi-company use or the audit trail of documents.

## Steps

**Read the part you need before the schema or the numbering is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Document model, statuses, numbering, conversion, snapshots, immutability, soft delete versus archive, currency, tenants | a schema, a status or a numbering rule is designed | [`01-documents-numbering-and-history.md`](./references/01-documents-numbering-and-history.md) |
| 2 | Roles and approvals, imports and exports, integrations, what to split first, v2 regrets, framework pointers | permissions, an integration or the first release are planned | [`02-roles-integrations-and-v2.md`](./references/02-roles-integrations-and-v2.md) |

## Output / checkpoint
Before building: the document types and the allowed conversions between them, a status table per type with who
may move it and what becomes read-only, the numbering policy per series and who owns it, the line snapshot
fields, the correction mechanism, and the tenant and entity boundary. Evidence is a test that a posted
document cannot be edited, a concurrency test that two simultaneous postings never share a number, a test that
a partial conversion tracks remaining quantity, and a test that changing a product price leaves old lines
unchanged. Nothing here was run by us.

## Guardrails
- This block is not legal advice and states no accounting, tax or invoice-content rule. Numbering continuity,
  retention and required mentions depend on the jurisdiction; ask the accountant and see the invoicing block.
- Never edit a posted document; reverse or credit it with a new document that references it (§1, point 6).
- Never allocate a number from `max()+1` in application code or from a database sequence you expect to be
  gapless; allocate in the posting transaction from a counter row and decide the gap policy (§1, point 3).
- Never compute an old document from the current product or price record; copy price, tax and description onto
  the line (§1, point 5).
- Never let a conversion bypass remaining-quantity tracking (§1, point 4).
- Never delete a document that has a number; cancel or void it and keep the row (§1, point 8).
- Never store money as a float or without a currency (§1, point 9).
- Never apply the tenant filter only in the screen (§1, point 10).

## Origin
Written from craft knowledge of building document-driven business applications, then checked on 2026-10-20
against the Apache OFBiz data model and the Kill Bill documentation (both Apache-2.0), credited in the origin
file; no text was taken. See
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
