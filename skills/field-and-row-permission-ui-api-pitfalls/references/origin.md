# field-and-row-permission-ui-api-pitfalls: origin and source stamps

> Provenance of `skills/field-and-row-permission-ui-api-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from craft knowledge; no application was tested and no framework or
library behaviour was run while writing it.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read. No source with a LICENSE file read and verified as MIT, Apache-2.0 or CC BY was used. | n/a | n/a |

## Rewrite notes
Every rule is own guidance from general practice in access control for business applications. No text, example
or number was copied. The term "object-level authorisation failure" and the mass assignment name are common
industry vocabulary; the security-community lists that use them were not opened (their licences were not
verified).

## Removed
- Any percentage, incident statistic or ranking of flaws: no verified source, so none given.
- Framework-specific policy and serializer calls: left to the stack blocks named in Related blocks.

## Not verified
1. **Status-code choice** (401, 403, 404 for hidden records) is a convention with trade-offs; confirm it with the
   API's own contract and consumers.
2. **Timing and enumeration** advice is general; the cases where it matters depend on the product.
3. **Retention and audit-log content** touches data protection law; this block gives method only and is not
   legal advice.
4. **Own guidance, not sourced:** all points on rule definition, hide versus disable versus mask, allow-listing,
   bulk actions, layers and bypasses, the matrix test and the review checklist.

## Related blocks
`laravel-permissions-not-roles`, `laravel-scope-dont-check-after-fetch`, `laravel-tenant-context-by-default`,
`postgres-operations-and-exposed-api-pitfalls`, `firebase-rules-and-client-trust-pitfalls`, `auth-session-conventions`,
`frontend-ux-antipattern-review-pitfalls`, `search-index-sync-pitfalls`, `csv-xlsx-import-export-pitfalls`,
`data-protection`.
