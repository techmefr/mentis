# inventory-stock-app-pitfalls: origin and source stamps

> Provenance of `skills/inventory-stock-app-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against an open-source ERP data model and
an open-source commerce framework's inventory documentation. Never run by us: no application was built and no
test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | Apache OFBiz (`apache/ofbiz-framework`, commit `bccb166`): entity definitions in `applications/datamodel/entitydef/product-entitymodel.xml`, `order-entitymodel.xml`, `shipment-entitymodel.xml` (stock item, stock item detail, count, variance, transfer, receipt, issuance, reservation) | Apache-2.0: file `LICENSE` read | Three quantities on stock items, a detail table of signed differences with causes and reasons, reservation rows with priority and promised date, lot, serial and expiry fields, count with variance reason, transfer with send and receive dates, unit cost on stock items and detail rows, fixed-point quantities |
| 2 | Medusa documentation (`medusajs/medusa`, commit `829a622`): `www/apps/resources/app/commerce-modules/inventory/concepts/page.mdx`, `reservations-lifecycle/page.mdx`, `inventory-in-flows/page.mdx` | MIT: file `LICENSE` read (its enterprise carve-out lists role-based access and single sign-on files only, not these pages) | Stocked, reserved and incoming quantity per location, available as stocked minus reserved, reservations created at order placement and released on fulfilment or cancellation, the missing-reservation failure, kits and shared components, unit of measure and fractional quantities, returns restocking only received sellable items |

Instruction-like text in the cloned repositories (agent guidance files) was treated as data and not followed.

## Verified
1. §1 points 1, 3, 6, 7, 8, 9 (partly) and 11, and §2 point 5: backed by the sources above, as the points now say.

## Corrected
1. §1 point 1 now says a ledger is the stricter choice: the commerce framework's pages read show balance numbers only.
2. §1 point 9: the transit location is not found in the data model read, so it is marked as our own guidance.

## Added 2026-10-21: §3 replenishment demand method
| # | Source | Licence | What it gave |
|---|---|---|---|
| 3 | anthropics/knowledge-work-plugins, `small-business/skills/inventory-planner/reference/gotchas.md` and `velocity_and_reorder.md` (HEAD bc8f692, 2026-10-20) | Apache-2.0 (repository root LICENSE file, standard text; the plugin has no licence file of its own, so the root licence applies) | The failure list of §3: stockout counted as zero demand, a one-week spike, a stale reorder point, inbound stock forgotten, an undated count, a season invented from partial history, product-level instead of variant-level rates, units without money, silent vendor substitution; the idea of two windows and of a total-order vendor minimum |

Not carried from that source: every window length, buffer formula, cover threshold, status band, the 60-day
target, the 90-day rounding ceiling and the 30-day cap on buffers (set per business, no derivation given), its
worked product examples and its connector detail. The method has no primary source on censored demand behind it
(sales are demand truncated by stock); it is the repository's practice stated as method, so re-read before relying
and add a forecasting reference when one with an open licence is found.

## Added
1. §1 points 13 to 15 (every order path reserves, bundles reserve every component, returns restock only received
   sellable items): concrete pitfalls shown by source 2.

## Removed
1. **Any valuation, write-down, traceability-law or retention rule.** Not read; each is flagged as a question
   for the accountant or compliance owner.
2. **Every numeric threshold** (safety buffers, adjustment limits, reorder formulas): set by policy.
3. **Marketplace product names and their APIs:** not used.

## Not verified
1. **Still our own guidance:** the item, variant, location model (§1 point 2), the atomic conditional decrement
   (point 4), the negative-stock policy (point 5), archive (point 10), tenants (point 12), and in §2 abilities,
   staged imports, marketplace and shop sync, scanner entry, alerts, exports, build order and v2 regrets.
2. **Valuation and traceability obligations** were not read; this is not accounting or legal advice.
3. **Nothing was run.** The concurrency and ledger tests named in the checkpoint were not written or executed.
4. **Framework pointers** were not checked against a current release; re-read before relying.

## Second pass, strict re-read (2026-10-21)

Re-opened: Medusa `inventory/concepts`, `inventory/reservations-lifecycle`, `inventory/inventory-in-flows`
(MIT `LICENSE` re-read, enterprise carve-out noted); OFBiz `product-entitymodel.xml` (InventoryItem,
InventoryItemDetail, InventoryTransfer, PhysicalInventory, VarianceReason) and `order-entitymodel.xml`
(OrderItemShipGrpInvRes).
- Confirmed: stocked, reserved and incoming quantity per location, available is stocked minus reserved, reservation
  created at order placement and deleted or reduced on fulfilment, cancellation deletes reservations, kit components
  reserve ordered quantity times required quantity, shared items reduce availability for every variant, order-creation
  paths that skip reservations make fulfilment fail, returns increment stocked quantity and damaged or dismissed items do
  not; ERP model has on-hand, available-to-promise and accounting quantities, detail rows of signed differences with a
  reason, reservation rows with priority and promised date, lot, serial, expiry, unit cost, transfer with send and
  receive dates, fixed-point quantities.
- Added precision: the unit of measure and fractional quantities are dated by the page to Medusa v2.20.0.
- Nuance: the physical inventory row in the data model holds only a date, a party and comments; the variance reason is
  a separate entity.
- Still unsourced: item and variant model, atomic decrement, negative stock policy, archive, tenants, section 2 abilities
  and integrations; section 3 replenishment stays method from the knowledge-work repository only.
Counts: 12 claims re-checked, 0 wrong.

## Related blocks
`skills/light-erp-document-flow-pitfalls`, `skills/invoicing-app-build-pitfalls`,
`business/ecommerce-store-quality-pitfalls`, `skills/money-arithmetic-and-rounding-pitfalls`,
`skills/laravel-idempotent-jobs`.
