# lms-app-build-pitfalls: origin and source stamps

> Provenance of `skills/lms-app-build-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against the xAPI specification. Never run by us: no application was built and no test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | xAPI specification (`adlnet/xAPI-Spec`, commit `ca782a1`): `xAPI-Data.md` (statement immutability, voiding, registration, timestamp and stored) and `xAPI-Communication.md` (writing a statement with an id already stored) | Apache-2.0: file `LICENSE` read | Immutable learning records, voiding instead of deleting, registration as attempt or session, occurred time versus stored time, conflict on a changed duplicate id |

Neighbouring blocks were read to avoid duplication: `skills/training-objectives-and-formative-assessment-pitfalls`
and `skills/learning-mode-exercise-pitfalls` (designing and checking learning, not building the platform),
`business/learning-development`, `skills/document-file-management-pitfalls`, `skills/file-upload-ui-pitfalls`,
`skills/crm-app-build-pitfalls` (shape model). The overlap check found no block that covers building an LMS, so
a new block was justified.

## Verified
1. §1 points 3, 5 and 6 and §2 point 3 (partly): source 1, as the points now say.

## Corrected
1. §2 point 3: the "none was read" remark now says that only the xAPI specification was read; SCORM, cmi5 and launch
   protocols remain unread.

## Removed
1. **Every numeric threshold, size cap, retention period and pass mark.** None is stated; set them by policy.
2. **Any statement of records, accessibility or certification law.** Not read; method only.
3. **Vendor feature lists** (named LMS products) and the details of packaged-content standards: not used.

## Not verified
1. **Still our own guidance:** versioned courses (§1 point 1), the minimal model (point 2), the completion rule (point 4),
   certificates (point 7), cohort deadlines and zones (point 8), archive and reminders (points 9 and 10), and in §2 visibility,
   enrolment sources, media serving, imports, accessibility, reports, build order and v2 regrets. No permissive LMS
   documentation was identified (searched: the xAPI specification; LMS projects were not opened).
2. **Legal questions** (learner records, erasure, certificate standing) belong to the data-protection owner; this
   is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **SCORM, cmi5, learning-tool launch protocols and framework pointers** (Laravel, Nuxt) are short and unchecked;
   re-read before relying.

## Related blocks
`skills/training-objectives-and-formative-assessment-pitfalls`, `business/learning-development`,
`business/data-protection`, `skills/laravel-no-cascade-delete`, `skills/laravel-recognise-state-machine-or-pipeline`.
