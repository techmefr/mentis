# admin-back-office-pitfalls: origin and source stamps

> Provenance of `skills/admin-back-office-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of building admin and support tools. No admin-framework or audit-log library documentation was opened; no LICENSE file was read because no source was used. |

Neighbouring blocks of this repository were read to avoid duplication: `skills/feature-flag-lifecycle`
(flag creation, ramp and removal), `skills/field-and-row-permission-ui-api-pitfalls`,
`skills/laravel-permissions-not-roles`, `skills/data-table-ui-pitfalls`, `skills/csv-xlsx-import-export-pitfalls`,
`skills/crm-app-build-pitfalls` and `business/data-protection`. The overlap check found no block that covers
building an admin back office (audit log, impersonation, dangerous and bulk actions); flag lifecycle is already
covered, so this block only cross-links it.

## Removed
1. **Every numeric threshold, cap, expiry and retention period.** None is stated; set them by policy.
2. **Any statement of law on access logging, retention or notification.** Not read; method only.
3. **Named admin frameworks and impersonation packages:** not used.

## Not verified
1. **All points are our own guidance** and were not compared with any open-source admin tool.
2. **Legal questions** (logging of staff access, retention, notification duties) belong to the data-protection
   owner; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** (Laravel, Nuxt) are short and were not checked against a current release; re-read
   before relying.

## Related blocks
`skills/feature-flag-lifecycle`, `skills/field-and-row-permission-ui-api-pitfalls`, `skills/laravel-no-cascade-delete`,
`skills/laravel-idempotent-jobs`, `business/data-protection`.
