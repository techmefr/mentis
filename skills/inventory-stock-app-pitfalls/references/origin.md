# inventory-stock-app-pitfalls: origin and source stamps

> Provenance of `skills/inventory-stock-app-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of inventory and stock applications. No open-source inventory or ERP documentation was opened, and no LICENSE file was read because no source was used. |

Neighbouring blocks of this repository were read to avoid duplication: `business/ecommerce-store-quality-pitfalls`
(store catalogue and checkout quality, not stock application design), `skills/money-arithmetic-and-rounding-pitfalls`,
`skills/laravel-idempotent-jobs`, `skills/laravel-tenant-context-by-default`, `skills/laravel-permissions-not-roles`,
`skills/gl-subledger-reconciliation-pitfalls`. None covers designing a stock application, so a new block was
justified.

## Removed
1. **Any valuation, write-down, traceability-law or retention rule.** Not read; each is flagged as a question
   for the accountant or compliance owner.
2. **Every numeric threshold** (safety buffers, adjustment limits, reorder formulas): set by policy.
3. **Named inventory and marketplace products and their APIs:** not used.

## Not verified
1. **All points are our own guidance** and were not compared with an open-source inventory schema.
2. **Valuation and traceability obligations** were not read; this is not accounting or legal advice.
3. **Nothing was run.** The concurrency and ledger tests named in the checkpoint were not written or executed.
4. **Framework pointers** were not checked against a current release; re-read before relying.

## Related blocks
`skills/light-erp-document-flow-pitfalls`, `skills/invoicing-app-build-pitfalls`,
`business/ecommerce-store-quality-pitfalls`, `skills/money-arithmetic-and-rounding-pitfalls`,
`skills/laravel-idempotent-jobs`.
