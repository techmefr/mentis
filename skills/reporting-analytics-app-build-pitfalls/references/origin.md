# reporting-analytics-app-build-pitfalls: origin and source stamps

> Provenance of `skills/reporting-analytics-app-build-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of building reporting and analytics products. No open-source BI or semantic-layer documentation was opened; no LICENSE file was read because no source was used. |

Neighbouring blocks were read to avoid duplication: `skills/chart-choice-pitfalls`, `skills/dashboard-ui-pitfalls`,
`skills/grafana-dashboard-pitfalls`, `skills/filters-search-and-saved-views-pitfalls` (screen-side views),
`skills/delivery-metrics-definition-pitfalls` (defining one family of metrics), `business/data-analytics`
(analysis practice), `skills/laravel-cache`, `skills/laravel-scheduling`. The overlap check found no block that
covers building a reporting application (metric governance, row-level access, schedules, freshness), so a new
block was justified.

## Removed
1. **Every numeric threshold, timeout, row cap, cache lifetime and retention period.** None is stated; set them
   by policy.
2. **Any statement of privacy or retention law.** Not read; method only.
3. **Vendor feature lists** (named BI products and semantic-layer tools): not used.

## Not verified
1. **All points are our own guidance** and were not compared with any open-source BI schema.
2. **Legal questions** (reporting on individuals, masking, retention) belong to the data-protection owner; this
   is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** (Laravel, Nuxt) are short and unchecked; re-read before relying.

## Related blocks
`skills/dashboard-ui-pitfalls`, `skills/delivery-metrics-definition-pitfalls`, `business/data-analytics`,
`business/data-protection`, `skills/crm-app-build-pitfalls`.
