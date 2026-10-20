---
name: inventory-stock-app-pitfalls
description: "Use when an inventory or stock application is designed or built: item, variant, location and lot or serial model, stock as an append-only movement ledger rather than an editable quantity, on-hand versus reserved versus available, concurrent decrements and oversell, unit of measure and conversion, receipts, transfers, adjustments and counts, valuation method as a stated policy, negative stock, archive versus delete, multi-warehouse and multi-tenant boundaries, imports and scanner or marketplace sync, roles, what to split first and what gets regretted at v2. Method only; accounting valuation rules are not stated and this is not accounting advice."
---

# inventory-stock-app-pitfalls

A defensive block for building the application that knows how much of what is where. Stock tools fail in
familiar ways: the quantity is a number someone edits and nobody can say why it changed, two orders take the
last unit, a transfer loses units in transit, a count overwrites history, units of measure mix, and a marketplace
sync sets the quantity to a stale value. The content is craft knowledge with no external source read (see
`references/origin.md`). The purchase and sales documents that move stock are in
`skills/light-erp-document-flow-pitfalls`; invoicing is in `skills/invoicing-app-build-pitfalls`; exact
quantities and money are in `skills/money-arithmetic-and-rounding-pitfalls`; an e-commerce store's catalogue
and checkout are in `business/ecommerce-store-quality-pitfalls`; idempotent writes are in
`skills/laravel-idempotent-jobs`.

## When
- A tool tracks quantities of goods across locations, with receipts, shipments, transfers or counts.
- A reservation, an allocation or an oversell guard is added.
- Stock is synchronised with a shop, a marketplace, a scanner or an accounting tool.
- A valuation or cost figure is shown next to stock.

## Steps

**Read the part you need before the schema or the stock write path is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Item and location model, movement ledger, reservation, concurrency, units, lots, valuation, counts, archive versus delete, tenants | a schema or the stock write path is designed | [`01-movements-and-quantities.md`](./references/01-movements-and-quantities.md) |
| 2 | Roles, imports and exports, scanner and marketplace sync, what to split first, v2 regrets, framework pointers | permissions, an integration or the first release are planned | [`02-roles-integrations-and-v2.md`](./references/02-roles-integrations-and-v2.md) |

## Output / checkpoint
Before building: the item, variant and location list, the movement types with the sign and the document each
needs, the on-hand, reserved and available definitions, the unit and conversion rule, the lot or serial policy,
the valuation policy chosen with the accountant, the negative-stock policy, and the sync source of truth.
Evidence is a test that on-hand always equals the sum of movements, a parallel test where N buyers compete
for fewer than N units, a transfer test that never loses a unit in transit, and a count test that posts a
difference as a movement. Nothing here was run by us.

## Guardrails
- This block is not accounting advice and states no valuation or write-down rule. Choose the method with the
  accountant and write it with its date.
- Never store on-hand as the only truth that is edited in place; derive it from movements, or keep a cached
  value that is verified against them (§1, point 1).
- Never decrement stock with read, compute, write in application code; use a conditional update or a lock
  (§1, point 4).
- Never post a count by overwriting the quantity; post the difference as an adjustment movement with a reason
  (§1, point 8).
- Never let a sync job set an absolute quantity from an external system without a version or timestamp
  check and a source-of-truth decision (§2, point 3).
- Never delete an item, a location or a movement that has history; archive (§1, point 10).
- Never mix units in one quantity column; store a base unit and convert at the edge (§1, point 6).

## Origin
Written from craft knowledge of building inventory and stock applications; no open-source inventory or ERP
documentation was read, so no source is credited and no text was taken. See
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
