# lms-app-build-pitfalls: origin and source stamps

> Provenance of `skills/lms-app-build-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of building learning platforms. No open-source LMS documentation or learning-standard specification was opened; no LICENSE file was read because no source was used. |

Neighbouring blocks were read to avoid duplication: `skills/training-objectives-and-formative-assessment-pitfalls`
and `skills/learning-mode-exercise-pitfalls` (designing and checking learning, not building the platform),
`business/learning-development`, `skills/document-file-management-pitfalls`, `skills/file-upload-ui-pitfalls`,
`skills/crm-app-build-pitfalls` (shape model). The overlap check found no block that covers building an LMS, so
a new block was justified.

## Removed
1. **Every numeric threshold, size cap, retention period and pass mark.** None is stated; set them by policy.
2. **Any statement of records, accessibility or certification law.** Not read; method only.
3. **Vendor feature lists** (named LMS products) and the details of packaged-content standards: not used.

## Not verified
1. **All points are our own guidance** and were not compared with any open-source LMS schema.
2. **Legal questions** (learner records, erasure, certificate standing) belong to the data-protection owner; this
   is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Standards and framework pointers** (packaged content, Laravel, Nuxt) are short and unchecked; re-read before
   relying.

## Related blocks
`skills/training-objectives-and-formative-assessment-pitfalls`, `business/learning-development`,
`business/data-protection`, `skills/laravel-no-cascade-delete`, `skills/laravel-recognise-state-machine-or-pipeline`.
