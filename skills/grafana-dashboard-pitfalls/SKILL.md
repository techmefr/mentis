---
name: grafana-dashboard-pitfalls
description: "Use when a Grafana dashboard defined as code (JSON) is written, generated or reviewed, especially for Prometheus or Loki data: $__rate_interval versus a fixed range, $__auto in Loki range queries, job and instance matchers, the datasource, job and instance template variables, reloading variables on time change, panels that hard-code a datasource, missing titles, descriptions and units, non-editable dashboards, and lint exclusions with a reason using dashboard-linter."
---

# grafana-dashboard-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for dashboards kept as files. The two sections share one premise: **a
dashboard that renders at one zoom level on one data source can be wrong at the next zoom or in the next
environment, and nothing in the UI says so: a range that is too short for the scrape interval, a datasource named in
the panel, a variable that was never refreshed**. The PromQL itself (counters, ratios, joins) is in
`prometheus-rules-and-promql-pitfalls`; what an alert pages on is in `observability-instrumentation` §4. Grafana
variable names, the rule list of the linter and the panel types it covers move with releases, so each such fact
below is labelled as the source states it and must be re-checked against the Grafana and linter versions in use.

## When
- Writing or generating a dashboard JSON, or reviewing a change to one.
- A graph shows gaps or flat zeros when the time range is zoomed in or out.
- A dashboard works in one environment and shows nothing in another.
- Adding a lint step for dashboards to CI, or writing an exclusion for a rule.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Queries: `$__rate_interval`, `$__auto`, job and instance matchers, valid queries | a panel query is written or a graph looks wrong when zoomed | [`01-queries.md`](./references/01-queries.md) |
| 2 | Variables, panels and exceptions: the datasource, job and instance variables, titles, units, editable dashboards, `.lint` exclusions, CI | a dashboard is structured, linted or an exclusion is written | [`02-variables-panels-and-exceptions.md`](./references/02-variables-panels-and-exceptions.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the dashboard was opened at the shortest and the longest time range
it is meant for and the series were compared, it was loaded against a second environment with a different data
source name and job, and the linter was run with `--strict` and its findings read (§2.5). A dashboard that only
rendered in the author's environment is not verified.

## Guardrails
- Never write a fixed `[5m]` range in a `rate`, `irate` or `increase` unless the fixed period is deliberate and the
  exclusion records why (§1.1).
- Never write a fixed range in a Loki range query where `$__auto` fits (§1.2).
- Never name a data source in a panel, and never have more than one datasource variable without a recorded
  exclusion (§2.1).
- Never exclude a rule for a whole dashboard when one panel or target needs it, and never exclude without a
  reason (§2.5).
- Never leave a panel without a title, a description and a unit unless the exclusion says why (§2.3).
- This block states linter and Grafana behaviour as of the repository read on the date in
  [`references/origin.md`](./references/origin.md). The Grafana documentation and the pages the linter links to were
  not read, and nothing was run while writing it.

## Origin
Rewritten from the Grafana dashboard-linter documentation (Apache-2.0), read 2026-10-16. 🟡: never run by us; open
points are in [`references/origin.md`](./references/origin.md).
