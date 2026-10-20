# reporting-analytics-app-build-pitfalls: origin and source stamps

> Provenance of `skills/reporting-analytics-app-build-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against the Apache Superset documentation. Never run by us: no application was built and no test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | Apache Superset documentation (`apache/superset`, commit `1df897b`): `docs/docs/using-superset/embedding.mdx`, `docs/docs/using-superset/exporting-dashboard-data.mdx`, `docs/docs/security/granular-export-controls.mdx` | Apache-2.0: file `LICENSE.txt` read | Row restrictions requested server-side with a service account, separate export abilities, export under the requester's permissions, expiring export link streamed through the application, short-lived embed token, allowed origins, revocation, redacted errors |

Neighbouring blocks were read to avoid duplication: `skills/chart-choice-pitfalls`, `skills/dashboard-ui-pitfalls`,
`skills/grafana-dashboard-pitfalls`, `skills/filters-search-and-saved-views-pitfalls` (screen-side views),
`skills/delivery-metrics-definition-pitfalls` (defining one family of metrics), `business/data-analytics`
(analysis practice), `skills/laravel-cache`, `skills/laravel-scheduling`. The overlap check found no block that
covers building a reporting application (metric governance, row-level access, schedules, freshness), so a new
block was justified.

## Verified
1. §2 points 1, 2, 4 and 7 (partly): source 1, as the points now say.

## Corrected
1. None: no earlier statement contradicted the source.

## Removed
1. **Every numeric threshold, timeout, row cap, cache lifetime and retention period.** None is stated; set them
   by policy.
2. **Any statement of privacy or retention law.** Not read; method only.
3. **Vendor feature lists** (named BI products and semantic-layer tools): not used.

## Not verified
1. **Still our own guidance:** the metric record (§1 point 1), the model (point 2), time rules (point 3), saved-report survival
   (point 4), snapshots (point 5), freshness (point 6), cache keys (point 7), query bounds (point 8), ratios (point 9), null and
   test data (point 10), and in §2 schedules, audit, self-service guard rails, personal data, build order and v2 regrets. The
   Superset documentation was searched for caching and semantic-layer material; the pages in the sparse copy held none that
   applies, so those points stay unsourced.
2. **Legal questions** (reporting on individuals, masking, retention) belong to the data-protection owner; this
   is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** (Laravel, Nuxt) are short and unchecked; re-read before relying.

## Related blocks
`skills/dashboard-ui-pitfalls`, `skills/delivery-metrics-definition-pitfalls`, `business/data-analytics`,
`business/data-protection`, `skills/crm-app-build-pitfalls`.
