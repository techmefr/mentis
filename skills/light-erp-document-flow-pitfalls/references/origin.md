# light-erp-document-flow-pitfalls: origin and source stamps

> Provenance of `skills/light-erp-document-flow-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of document-driven business applications. No open-source ERP data-model documentation was opened, and no LICENSE file was read because no source was used. |

Neighbouring blocks of this repository were read to avoid duplication: `skills/gl-subledger-reconciliation-pitfalls`
(comparing ledgers, not building documents), `skills/accounts-payable-duplicate-and-match-pitfalls`,
`skills/e-invoicing-obligations-pitfalls`, `skills/vat-handling-in-software-pitfalls`,
`skills/money-arithmetic-and-rounding-pitfalls`, `skills/laravel-tenant-context-by-default`,
`skills/laravel-permissions-not-roles`. None covers designing the document backbone of an application, so a
new block was justified.

## Removed
1. **Any accounting, tax, invoice-content, numbering-continuity or retention rule.** Not read; each is flagged
   as a question for the accountant.
2. **Every numeric threshold** (approval amounts, retention periods, row caps): set by policy.
3. **Named ERP products and their module lists:** not used.

## Not verified
1. **All points are our own guidance** and were not compared with an open-source ERP schema.
2. **Numbering policy.** Whether gaps are allowed in a given jurisdiction was not read; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** were not checked against a current release; re-read before relying.

## Related blocks
`skills/invoicing-app-build-pitfalls`, `skills/inventory-stock-app-pitfalls`, `skills/crm-app-build-pitfalls`,
`skills/accounts-payable-duplicate-and-match-pitfalls`, `skills/laravel-no-cascade-delete`.
