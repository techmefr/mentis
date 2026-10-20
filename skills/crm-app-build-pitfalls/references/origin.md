# crm-app-build-pitfalls: origin and source stamps

> Provenance of `skills/crm-app-build-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of building CRM-style applications. No open-source CRM or ERP data-model documentation was opened; no LICENSE file was read because no source was used. |

Neighbouring blocks of this repository were read to avoid duplication: `business/outbound-sales-and-crm-hygiene-pitfalls`
(sales-ops cleaning and reporting, not building), `skills/money-arithmetic-and-rounding-pitfalls`,
`skills/laravel-tenant-context-by-default`, `skills/laravel-permissions-not-roles`, `business/data-protection`
and `business/spreadsheet-data-cleaning-pitfalls`. The overlap check found no block that covers designing a CRM
application, so a new block was justified.

## Removed
1. **Every numeric threshold, row cap and retention period.** None is stated; set them by policy.
2. **Any statement of consent, marketing, retention or erasure law.** Not read; method only.
3. **Vendor feature lists** (named CRM products): not used.

## Not verified
1. **All points are our own guidance** and were not compared with any open-source CRM schema.
2. **Legal questions** (consent, erasure, retention, lawful basis) belong to the data-protection owner; this is
   not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** (Laravel, Nuxt) are short and were not checked against a current release; re-read
   before relying.

## Related blocks
`business/outbound-sales-and-crm-hygiene-pitfalls`, `business/data-protection`, `skills/laravel-no-cascade-delete`,
`skills/laravel-recognise-state-machine-or-pipeline`, `skills/light-erp-document-flow-pitfalls`.
