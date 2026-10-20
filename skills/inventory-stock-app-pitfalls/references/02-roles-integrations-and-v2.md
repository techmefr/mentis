# inventory-stock-app-pitfalls §2 — Roles, integrations and v2

> Part 2 of `skills/inventory-stock-app-pitfalls`. Read it when permissions, an integration or the first
> release are planned. Craft knowledge, no external source read.

1. **Abilities per action and location.** Receive, ship, transfer, adjust, count, approve adjustment, see cost,
   edit item master, change units, export, archive. Symptom: a picker can adjust stock or see purchase
   cost. Fix: abilities named as permissions (see `skills/laravel-permissions-not-roles`), scoped to
   locations, with adjustment above a policy limit needing a second person, and a test per ability and per
   read path (list, search, export, API).
2. **Imports are staged and posted as documents.** Opening stock, item lists and supplier catalogues arrive
   from files. Fix: a staging table, mapped preview, per-row errors, counts of create, update and skip, an
   import id kept on each row, and opening quantities entered as a dated opening movement per location, not
   as a balance edit. SKU and barcode keys follow the matching rule: external id, then SKU, never description.
   Leading zeros and scientific notation damage barcodes in spreadsheets (see
   `business/spreadsheet-data-cleaning-pitfalls`).
3. **Marketplace and shop sync: pick one source of truth.** Symptom: a shop sets the quantity to a stale
   number and overwrites newer movements, or oversells after a delayed update. Fix: the application owns stock
   and pushes available quantity; inbound orders become reservations with an external order id for
   idempotency; a push carries a version or timestamp and an older one is dropped; a failed push is retried
   with backoff and shown to a person; keep a safety buffer chosen by the business for fast-moving items;
   reconcile counts periodically and report drift rather than silently overwriting.
4. **Scanner and mobile entry are offline-tolerant and idempotent.** Each scan event has a client-generated id
   and a device time, the server dedupes by id, rejects a scan against a closed count or an archived item with
   a clear message, and records the device and user. Symptom of ignoring it: a flaky connection doubles a
   receipt.
5. **Documents drive movements, not the other way round.** A receipt, shipment, transfer or adjustment document
   posts movements in one transaction; a movement refers to its document line; cancelling a posted document
   posts a reversal. Keep the immutability and numbering rules of
   `skills/light-erp-document-flow-pitfalls`. Symptom of direct movement writes from screens: stock that no
   document explains.
6. **Alerts and reorder are derived, not stored.** Reorder point, safety stock and lead time are policy
   fields per item and location; a low-stock alert is a computed query over available quantity and open
   purchase orders, not a stored flag. Forecasting numbers are not stated here; take them from the business.
7. **Exports and audit.** Stock reports name their as-of time, location set, unit and the measure
   (on-hand, available, valued); a point-in-time balance is the sum of movements up to that time, which the
   ledger makes possible. Export is scoped and logged, with formula-starting cells quoted; adjustments, cost
   views and exports are always in the audit log.
8. **What to split first.** Order: item, variant and location master with archive and unique keys; the
   movement ledger with atomic balance update and the receipt and shipment documents; reservations and
   available quantity; counts and adjustments; transfers with transit; roles; imports and exports; then lots
   and serials, valuation, reorder, and external sync. Ship the ledger and concurrency tests before any
   integration, because every sync trusts the balance.
9. **What is regretted at v2.** Quantity as an editable column; no movement history; on-hand and available
   conflated; read-compute-write decrements; counts that overwrite; transfers with no transit; mixed units;
   lots bolted on after stock exists; valuation stored as a mutated cost on the item; sync that sets absolute
   quantities with no version; no location in the model of a single-warehouse product; deleted items. Each
   is cheap in the first migration and costly after stock exists.
10. **Laravel and Nuxt pointers, short.** In Laravel: a movements table with no update path, a balance row
    updated with a conditional query inside the same transaction as the movement insert, row locks or
    optimistic version columns, queued sync jobs with idempotency keys, a global tenant scope, and a
    scheduled command that compares cached balances to movement sums. In Nuxt: show available from the
    server, treat the browser quantity as stale, send scan events with client ids, and never decide
    availability in the client.
