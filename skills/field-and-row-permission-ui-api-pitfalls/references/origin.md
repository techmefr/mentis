# field-and-row-permission-ui-api-pitfalls: origin and source stamps

> Provenance of `skills/field-and-row-permission-ui-api-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from craft knowledge; no application was tested and no framework or
library behaviour was run while writing it.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| RFC 9110, HTTP Semantics, <https://www.rfc-editor.org/rfc/rfc9110>, read 2026-10-20 (status-code sections 15.5.2, 15.5.4, 15.5.5 only) | IETF Trust document; facts only, restated in own words | Meaning of 401, 403, 404, and that a server may answer 404 to hide a forbidden resource |
| Permissive source on field and row permission design | n/a | No permissive source found, searched: OWASP and framework documentation known to the author; OWASP cheat sheets are CC BY-SA and were not opened, framework docs had no verified licence. |

## Rewrite notes
Every rule is own guidance from general practice in access control for business applications. No text, example
or number was copied. The term "object-level authorisation failure" and the mass assignment name are common
industry vocabulary; the security-community lists that use them were not opened (their licences were not
verified).

## Removed
- Any percentage, incident statistic or ranking of flaws: no verified source, so none given.
- Framework-specific policy and serializer calls: left to the stack blocks named in Related blocks.

## Not verified
1. **Verified 2026-10-20:** the meaning of 401, 403 and 404 and the permission to hide with 404 (RFC 9110). **Still unverified:** the recommendation to use 404 per resource and the enumeration trade-off; confirm with the API's own contract and consumers.
2. **Timing and enumeration** advice is general; the cases where it matters depend on the product.
3. **Retention and audit-log content** touches data protection law; this block gives method only and is not
   legal advice.
4. **Own guidance, not sourced:** all points on rule definition, hide versus disable versus mask, allow-listing,
   bulk actions, layers and bypasses, the matrix test and the review checklist.

Second pass 2026-10-20: no further checkable fact found that a permissive or official source covers; cache scoping, enumeration timing and mass assignment stay own guidance (security cheat sheets are CC BY-SA, not opened).

## Related blocks
`laravel-permissions-not-roles`, `laravel-scope-dont-check-after-fetch`, `laravel-tenant-context-by-default`,
`postgres-operations-and-exposed-api-pitfalls`, `firebase-rules-and-client-trust-pitfalls`, `auth-session-conventions`,
`frontend-ux-antipattern-review-pitfalls`, `search-index-sync-pitfalls`, `csv-xlsx-import-export-pitfalls`,
`data-protection`.
