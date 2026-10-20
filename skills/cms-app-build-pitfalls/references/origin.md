# cms-app-build-pitfalls: origin and source stamps

> Provenance of `skills/cms-app-build-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of building content management systems. No open-source CMS documentation was opened; no LICENSE file was read because no source was used. |

Neighbouring blocks were read to avoid duplication: `skills/rich-text-editor-pitfalls`, `skills/astro-images-templates-pitfalls`
(building a site, not the CMS), `skills/admin-back-office-pitfalls`, `skills/document-file-management-pitfalls`,
`skills/search-index-sync-pitfalls`, `skills/i18n-catalog-workflow-pitfalls`, `business/content-creation` and
`business/content-brief-writing-pitfalls` (writing content, not building the system). The overlap check found
no block that covers building a CMS, so a new block was justified.

## Removed
1. **Every numeric threshold, size cap, revision retention period and cache lifetime.** None is stated; set them
   by policy.
2. **Any statement of copyright, privacy or accessibility law.** Not read; method only.
3. **Vendor feature lists** (named CMS products): not used.

## Not verified
1. **All points are our own guidance** and were not compared with any open-source CMS schema.
2. **Legal questions** (media rights, personal data in content, accessibility duties) belong to the relevant
   owner; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** (Laravel, Nuxt) are short and unchecked; re-read before relying.

## Related blocks
`skills/rich-text-editor-pitfalls`, `skills/admin-back-office-pitfalls`, `skills/document-file-management-pitfalls`,
`skills/laravel-no-cascade-delete`, `skills/crm-app-build-pitfalls`.
