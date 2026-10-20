# document-file-management-pitfalls: origin and source stamps

> Provenance of `skills/document-file-management-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of building document and file-management applications. No open-source document system, storage or antivirus documentation was opened; no LICENSE file was read because no source was used. |

Neighbouring blocks of this repository were read to avoid duplication: `skills/security-hardening` (web
hardening), `skills/dsar-handling-pitfalls`, `skills/light-erp-document-flow-pitfalls` (document numbering and
history), `skills/field-and-row-permission-ui-api-pitfalls`, `skills/laravel-no-cascade-delete`,
`skills/laravel-pruning-fires-delete-events`, `skills/search-index-sync-pitfalls` and `business/data-protection`.
The overlap check found no block that covers building a document or file store (versions, storage layout,
sharing, retention, scanning). Upload and viewer screens are written by a sibling lot as UI-component blocks,
so this block covers data, storage and rules only.

## Removed
1. **Every numeric threshold, size limit, retention period, quota and timer.** None is stated; set them by policy.
2. **Any statement of retention, records or erasure law.** Not read; method only.
3. **Named storage services, scanners and converters:** not used.

## Not verified
1. **All points are our own guidance** and were not compared with any open-source document system.
2. **Legal questions** (retention periods, legal hold, erasure) belong to the data-protection owner and legal
   counsel; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** (Laravel, Nuxt) are short and were not checked against a current release; re-read
   before relying.

## Related blocks
`skills/security-hardening`, `skills/dsar-handling-pitfalls`, `skills/laravel-no-cascade-delete`,
`skills/laravel-idempotent-jobs`, `skills/admin-back-office-pitfalls`, `business/data-protection`.
