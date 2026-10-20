# survey-form-builder-app-build-pitfalls: origin and source stamps

> Provenance of `skills/survey-form-builder-app-build-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against the SurveyJS form library documentation. Never run by us: no application was built and no test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | SurveyJS form library documentation (`surveyjs/survey-library`, commit `105970a`): `docs/llms/survey-json-authoring.md`, `docs/api-reference/surveymodel.md` (`clearInvisibleValues`), `docs/survey-json-validation.md`, `docs/how-to-store-survey-results.md`, `docs/data-validation.md` | MIT: file `LICENSE` read | Unique question name as result key versus title, unique choice value, load-time check missing unresolved references and a linter for them and for cycles, four clearing modes for hidden values, server-side rebuild and clearing of posted data, errors keyed by question name |

Neighbouring blocks were read to avoid duplication: `skills/long-and-multistep-form-pitfalls` (one form screen,
not a builder), `business/customer-interview-synthesis-pitfalls`, `skills/security-questionnaire-answer-pitfalls`
(answering questionnaires, not building them), `skills/csv-xlsx-import-export-pitfalls`,
`skills/file-upload-ui-pitfalls`, `skills/rich-text-editor-pitfalls`. The overlap check found no block that
covers building a survey or form-builder application, so a new block was justified.

## Verified
1. §1 points 2, 4 and 5 and §2 point 1: source 1, as the points now say.

## Corrected
1. None: no earlier statement contradicted the source.

## Removed
1. **Every numeric threshold, rate limit, size cap, minimum group size and retention period.** None is stated;
   set them by policy.
2. **Any statement of consent, anonymisation or retention law.** Not read; method only.
3. **Vendor feature lists** (named survey or form products): not used.

## Not verified
1. **Still our own guidance:** versioning (§1 point 1), the minimal model (point 3), partial responses (point 6), anonymity modes
   and group minimums (points 7 and 8), one response per respondent (point 9), archive (point 10), and in §2 spam layers, roles,
   exports, analysis, integrations, uploads, language, build order and v2 regrets. No permissive survey-platform
   documentation beyond the one above was identified (searched: the SurveyJS documentation tree).
2. **Legal questions** (what counts as anonymous, consent, special-category data, erasure) belong to the
   data-protection owner; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** (Laravel, Nuxt) are short and unchecked; re-read before relying.

## Related blocks
`skills/long-and-multistep-form-pitfalls`, `business/data-protection`, `skills/laravel-no-cascade-delete`,
`skills/crm-app-build-pitfalls`, `skills/reporting-analytics-app-build-pitfalls`.
