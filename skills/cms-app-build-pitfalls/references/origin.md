# cms-app-build-pitfalls: origin and source stamps

> Provenance of `skills/cms-app-build-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against the Payload documentation. Never run by us: no application was built and no test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | Payload documentation (`payloadcms/payload`, commit `582c25b`): `docs/versions/overview.mdx`, `docs/versions/drafts.mdx`, `docs/versions/autosave.mdx`, `docs/admin/locked-documents.mdx`, `docs/live-preview/overview.mdx` | MIT: file `LICENSE.md` read | Status field with three admin states, draft saves without required checks, unpublish as status change, scheduled publish needing a job worker, document lock with take-over and expiry, versions in a separate collection with author and a per-entry cap, draft reads returning the newest version, live preview in a frame |

Neighbouring blocks were read to avoid duplication: `skills/rich-text-editor-pitfalls`, `skills/astro-images-templates-pitfalls`
(building a site, not the CMS), `skills/admin-back-office-pitfalls`, `skills/document-file-management-pitfalls`,
`skills/search-index-sync-pitfalls`, `skills/i18n-catalog-workflow-pitfalls`, `business/content-creation` and
`business/content-brief-writing-pitfalls` (writing content, not building the system). The overlap check found
no block that covers building a CMS, so a new block was justified.

## Verified
1. §1 points 2, 4, 5 and 6 and §2 point 1: source 1, as the points now say.

## Corrected
1. None: no earlier statement contradicted the source.

## Removed
1. **Every numeric threshold, size cap, revision retention period and cache lifetime.** None is stated; set them
   by policy.
2. **Any statement of copyright, privacy or accessibility law.** Not read; method only.
3. **Vendor feature lists** (named CMS products): not used.

## Not verified
1. **Still our own guidance:** three-step model changes (§1 point 1), the minimal model (point 3), media records (point 7), slugs
   and redirects (point 8), locales (point 9), archive (point 10), and in §2 unpublish propagation, roles, approval, rich text,
   delivery API, derived navigation, import, accessibility, build order and v2 regrets. No other permissive CMS
   documentation was identified (searched: the Payload documentation tree).
2. **Legal questions** (media rights, personal data in content, accessibility duties) belong to the relevant
   owner; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** (Laravel, Nuxt) are short and unchecked; re-read before relying.

## Related blocks
`skills/rich-text-editor-pitfalls`, `skills/admin-back-office-pitfalls`, `skills/document-file-management-pitfalls`,
`skills/laravel-no-cascade-delete`, `skills/crm-app-build-pitfalls`.
