# survey-form-builder-app-build-pitfalls: origin and source stamps

> Provenance of `skills/survey-form-builder-app-build-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of building form and survey tools. No open-source form-builder or survey-platform documentation was opened; no LICENSE file was read because no source was used. |

Neighbouring blocks were read to avoid duplication: `skills/long-and-multistep-form-pitfalls` (one form screen,
not a builder), `business/customer-interview-synthesis-pitfalls`, `skills/security-questionnaire-answer-pitfalls`
(answering questionnaires, not building them), `skills/csv-xlsx-import-export-pitfalls`,
`skills/file-upload-ui-pitfalls`, `skills/rich-text-editor-pitfalls`. The overlap check found no block that
covers building a survey or form-builder application, so a new block was justified.

## Removed
1. **Every numeric threshold, rate limit, size cap, minimum group size and retention period.** None is stated;
   set them by policy.
2. **Any statement of consent, anonymisation or retention law.** Not read; method only.
3. **Vendor feature lists** (named survey or form products): not used.

## Not verified
1. **All points are our own guidance** and were not compared with any open-source form-builder schema.
2. **Legal questions** (what counts as anonymous, consent, special-category data, erasure) belong to the
   data-protection owner; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** (Laravel, Nuxt) are short and unchecked; re-read before relying.

## Related blocks
`skills/long-and-multistep-form-pitfalls`, `business/data-protection`, `skills/laravel-no-cascade-delete`,
`skills/crm-app-build-pitfalls`, `skills/reporting-analytics-app-build-pitfalls`.
