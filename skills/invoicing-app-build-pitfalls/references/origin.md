# invoicing-app-build-pitfalls: origin and source stamps

> Provenance of `skills/invoicing-app-build-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of invoicing and billing applications. No open-source invoicing or ERP documentation was opened, and no LICENSE file was read because no source was used. |

Neighbouring blocks of this repository were read to avoid duplication: `skills/e-invoicing-obligations-pitfalls`
(obligations and format decisions, not application design), `skills/vat-handling-in-software-pitfalls`,
`skills/money-arithmetic-and-rounding-pitfalls`, `skills/gl-subledger-reconciliation-pitfalls`,
`skills/saas-metric-definition-pitfalls`, `skills/laravel-idempotent-jobs`. None covers building the invoicing
application itself, so a new block was justified; the shared document backbone is kept in
`skills/light-erp-document-flow-pitfalls` and referenced rather than repeated.

## Removed
1. **Any invoice-content, mandatory-mention, VAT rate, numbering-continuity or retention rule.** Not read;
   each is flagged as a question for the accountant.
2. **Collection-practice and late-fee rules:** not read, flagged for the legal owner.
3. **Every numeric threshold and schedule:** set by policy.
4. **Named billing products and provider APIs:** not used; webhook handling is described as concepts only.

## Not verified
1. **All points are our own guidance** and were not compared with an open-source invoicing schema.
2. **Numbering, correction and retention law** were not read; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** were not checked against a current release; re-read before relying.

## Related blocks
`skills/light-erp-document-flow-pitfalls`, `skills/e-invoicing-obligations-pitfalls`,
`skills/vat-handling-in-software-pitfalls`, `skills/money-arithmetic-and-rounding-pitfalls`,
`skills/inventory-stock-app-pitfalls`.
