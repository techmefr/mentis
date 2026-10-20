---
name: reporting-analytics-app-build-pitfalls
description: "Use when a reporting or analytics application is designed or built: the minimal model of data source, metric definition, report, saved view, schedule, export and access rule, metric definitions as one governed place instead of per-chart queries, saved reports that survive schema change, scheduled exports and delivery, row-level access enforced in the query, caching and freshness shown to the reader, query cost and timeouts, and what gets regretted at v2. Method only; privacy law is not legal advice."
---

# reporting-analytics-app-build-pitfalls

A defensive block for building the reporting product, not for choosing a chart or reading a number. A reporting
app built in a hurry fails in familiar ways: two dashboards show different revenue because each chart carries
its own query, a saved report breaks when a column is renamed, a scheduled export mails every row to someone
who should see a subset, a cached figure looks live and is a day old, and one heavy query slows the whole
application. The content is craft knowledge with no external source read (see `references/origin.md`). Chart
and layout choices are in `skills/chart-choice-pitfalls` and `skills/dashboard-ui-pitfalls`; filters and saved
views on a screen in `skills/filters-search-and-saved-views-pitfalls`; tables in `skills/data-table-ui-pitfalls`;
a dashboard tool's own pitfalls in `skills/grafana-dashboard-pitfalls`; defining delivery metrics in
`skills/delivery-metrics-definition-pitfalls`; business-side analysis in `business/data-analytics`; file
exports in `skills/csv-xlsx-import-export-pitfalls`; cache mechanics in `skills/laravel-cache`; schedules in
`skills/laravel-scheduling`; personal data duties in `business/data-protection`.

## When
- A reporting module, BI-style screen, embedded analytics or export centre is specified or its schema drafted.
- A product grows saved reports, scheduled emails, a metrics catalogue or customer-facing dashboards.
- A feature touches metric definitions, row-level access, caching, freshness or large exports.

## Steps

**Read the part you need before the schema or the first query is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Minimal model and its pitfalls: metric definitions, saved reports, time and grain, snapshots, freshness, query cost | a schema or a metric is designed | [`01-model-and-pitfalls.md`](./references/01-model-and-pitfalls.md) |
| 2 | Row-level access, scheduled delivery, exports, embedding, what to split first, v2 regrets, framework pointers | permissions, a schedule, an export or the first release are planned | [`02-roles-integrations-and-v2.md`](./references/02-roles-integrations-and-v2.md) |

## Output / checkpoint
Before building: the metric list with a one-sentence definition, source, grain, time field, filters, owner and
version for each; the row-level rule per data source; the freshness label shown with every figure; the cache
and invalidation rule; the schedule and delivery policy; the export limits. Evidence is a test that the same
metric returns the same number on every screen and in the export, a test that a restricted user gets the
reduced figure through the chart, the export and the scheduled mail, and a test that a saved report survives a
renamed column through a mapping or fails loudly. Nothing here was run by us.

## Guardrails
- This block is not legal advice. What may be reported on individuals, and for how long, depends on the
  jurisdiction and the use; ask the data-protection owner.
- Never define a metric inside a chart or a screen: define it once and reference it (§1, point 1).
- Never show a figure without its as-of time and its filters (§1, point 6).
- Never enforce access in the front end or the chart layer only: apply it in the query for every read path,
  including exports and schedules (§2, point 1).
- Never run a scheduled report as an all-seeing system user: run it as the recipient's scope (§2, point 2).
- Never cache without a key that includes the access scope (§1, point 7).
- Never let a user query run unbounded: set a timeout, a row cap and a cost guard (§1, point 8).

## Origin
Written from craft knowledge of building reporting and analytics products; no open-source BI documentation was
read, so no source is credited and no text was taken. See [`references/origin.md`](./references/origin.md). 🟡:
never run by us.
