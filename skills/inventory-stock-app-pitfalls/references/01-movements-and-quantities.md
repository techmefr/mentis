# inventory-stock-app-pitfalls §1 — Movements and quantities

> Part 1 of `skills/inventory-stock-app-pitfalls`. Read it when a schema or the stock write path is designed.
> Craft knowledge, no external source read. No valuation or accounting rule is stated.

1. **Stock is a ledger of movements.** Symptom: the quantity is a column people edit, and nobody can say why it
   dropped. Fix: an insert-only movement table (item or variant, location, lot or serial if tracked, signed
   quantity in the base unit, movement type, source document and line, actor, event time, recorded time),
   with on-hand defined as the sum of movements. A cached balance table is allowed for speed, updated in the
   same transaction as the movement, and verified against the sum by a scheduled check that reports drift.
   Corrections are new movements; no update or delete on movements.
2. **Model: item, variant, location, container.** An item is what you describe; a variant is what you count
   (size, colour); a location is where it is (warehouse, bin, in-transit, customer, supplier, scrap) and can be
   a tree; a stock balance is item by location by lot. Count at variant level only. Symptom of counting at
   the item level: "T-shirt, 40" cannot be picked. Give every item a stable internal id, and keep SKU and
   barcode as unique attributes within the tenant, changeable with history.
3. **On-hand, reserved, available are three numbers.** On-hand is physically there; reserved is promised to
   orders; available is on-hand minus reserved, optionally plus expected receipts shown separately. Symptom:
   a shop shows "in stock" for units already allocated. Fix: reservations as rows with item, location, quantity,
   source line and expiry; release on cancel, ship or expiry; define in the spec which of the three each screen
   and each integration reads.
4. **Decrement atomically.** Symptom: two orders take the last unit, on-hand goes negative by accident. Check:
   fire N parallel orders for fewer than N units. Fix: a conditional update (`set reserved = reserved + q
   where on_hand - reserved >= q`, checking affected rows), or a row lock on the balance row inside the
   transaction; never read, compute in code, then write. A reservation or movement carries an idempotency key
   from its source line so a retry does not apply twice (see `skills/laravel-idempotent-jobs`).
5. **Negative stock is a policy, not an accident.** Decide per tenant or location: forbidden, allowed with a
   warning (goods shipped before the receipt was entered), or allowed and reconciled later. If allowed, the
   system flags it and the receipt that follows clears it with a movement; the valuation consequence belongs
   to the accountant.
6. **One base unit, conversions at the edge.** Symptom: boxes and pieces summed in one column. Fix: store the
   quantity in the item's base unit as an exact integer or decimal with a declared scale (not a float),
   store pack sizes as conversion rows with a fixed factor, convert on input and display, and round only
   at the conversion, with a rule for fractions (some units, such as weight or length, are decimal; pieces
   are integers). See `skills/money-arithmetic-and-rounding-pitfalls` for the same discipline on amounts.
7. **Lots and serials only where needed.** Lot (batch, expiry) and serial (one unit, one identity) multiply
   cost and screens. Symptom: lot tracking turned on for everything and receipts take minutes. Fix: a
   tracking mode per item (none, lot, serial) fixed once there is stock, a lot record with code and expiry,
   a pick rule per tracked item (first expiry first out or first in first out, as the business chooses), and
   traceability reports from movement rows. Whether lot or serial recording is a legal requirement for a
   product class is a compliance question to ask, not to assume.
8. **Counts and adjustments are movements.** A stock count freezes or snapshots expected quantities, records
   counted quantities, computes differences, and posts each difference as an adjustment movement with a
   reason and an approver above a limit set by policy. Symptom: counting overwrites the balance and erases
   the evidence. Movements made during a count window are handled by the snapshot time.
9. **Transfers go through a transit location.** Symptom: units vanish between two warehouses. Fix: shipping
   creates a movement out of the source into an in-transit location; receiving creates a movement from transit
   into the destination; a difference at receipt is an adjustment from transit with a reason; transit stock is
   visible and aged. A same-transaction two-sided write is allowed only if shipping and receiving are the same
   event.
10. **Archive, never delete.** An item, variant or location with history is archived: hidden from pickers,
    resolvable from old documents; foreign keys restrict (see `skills/laravel-no-cascade-delete`). Unique
    SKU rules decide whether an archived SKU can be reused; reuse breaks history, so prefer not. Soft delete
    hides rows and is not erasure; stock rows hold no personal data except actors, which are users to archive,
    not delete.
11. **Valuation is a stated policy, kept apart from quantity.** Methods exist (average, first in first out,
    standard cost, specific identification), each with accounting and sometimes legal consequences; the choice
    is the accountant's. Store a unit cost on receipt movements, derive value from the chosen method in a
    separate calculation, and never mutate old movement costs; a cost correction is a new revaluation entry.
    Do not state any rule as required here: this block is not accounting advice.
12. **Tenant and warehouse boundaries on every row.** Tenant id on items, locations, movements, reservations
    and counts, and scope once by default (see `skills/laravel-tenant-context-by-default`). A user's access to a
    location is a permission, enforced in the query that feeds lists, search, exports and sync. Symptom of
    missing: another customer's SKU appears in a picker.
