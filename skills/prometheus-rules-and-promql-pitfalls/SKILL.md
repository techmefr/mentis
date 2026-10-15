---
name: prometheus-rules-and-promql-pitfalls
description: "Use when PromQL, a Prometheus recording rule or an alerting rule is written, reviewed or debugged, especially when an alert never fires, fires after a restart or a query returns nothing: rate on counters and gauges, the range versus the scrape interval, rate before sum, ratios and averages across series, histogram versus summary quantiles, vector matching and labels removed by an aggregation, anchored regexp matchers, recording-rule and metric naming, absent and for, batch-job and metamonitoring alerts, and linting rules with pint."
---

# prometheus-rules-and-promql-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the expressions and rule files a Prometheus server evaluates. The three
sections share one premise: **a PromQL expression that parses and returns a number can still be wrong, and the
wrong answer is an empty result, a statistically meaningless average or an alert that fires only after a restart,
none of which raises an error**. What to alert on, in principle, is in `observability-instrumentation` §4; which
label may exist at all, and the cost of series, is in `observability-instrumentation` §3 and
`telemetry-sampling-and-cardinality-pitfalls`; the Collector that feeds a Prometheus-compatible backend is in
`otel-collector-config-pitfalls`. Behaviour, defaults and feature status (native histograms, default retention) move
with Prometheus releases, so every such fact below is labelled as the source states it and must be re-checked
against the Prometheus version in use.

## When
- Writing or reviewing a query, a recording rule or an alerting rule.
- An alert never fires, fires right after Prometheus restarts, or flaps.
- A query or a join returns nothing, or a ratio, average or percentile looks plausible but is wrong.
- Naming a metric or a recording rule, or choosing between a histogram and a summary.
- Putting a rule linter into CI.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Queries: counters and gauges, the range, aggregation, quantiles, matching, regexp, retention | an expression is written, or returns nothing or a wrong number | [`01-queries.md`](./references/01-queries.md) |
| 2 | Recording rules and names: level:metric:operations, `without`, metric and label naming | a recording rule or a metric is named | [`02-recording-rules-and-names.md`](./references/02-recording-rules-and-names.md) |
| 3 | Alerting rules: `for` and restarts, what to page on, batch jobs, metamonitoring, linting with pint | an alert is written, fires at restart, or a lint step is added | [`03-alerting-rules-and-linting.md`](./references/03-alerting-rules-and-linting.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the expression was run in the Prometheus UI against the live series
and its result compared with a number computed another way (§1), the output labels of a recording rule were read
against its name (§2.2), the alert was tested by restarting a non-production Prometheus and watching for a false
firing (§3.1), and the lint run's findings were read, not only its exit code (§3.4). An expression that only parsed
is not verified.

## Guardrails
- Never take `rate()`, `irate()` or `increase()` of a gauge, and never `rate(sum(counter))` (§1.1).
- Never use a range shorter than twice the scrape interval in `rate()` (§1.1).
- Never average a ratio, an average or a summary quantile (§1.2).
- Never join or compare vectors without checking that both sides still carry the labels you match on (§1.3).
- Never write `^` or `$` in a regexp matcher, or a regexp where `=` does the job (§1.3).
- Never name a recording rule without the `level:metric:operations` form or aggregate without a `without` clause (§2).
- Never write an `absent()` alert, or an alert on two aggregations over different jobs, without `for` (§3.1).
- Never page on a batch job's last run alone: allow for at least two full runs (§3.2).
- This block states Prometheus behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md). Nothing was run while writing it; the Prometheus reference
  documentation for the functions was not read.

## Origin
Rewritten from the Prometheus documentation practices pages (Apache-2.0) and the pint rule-linter checks
documentation (Apache-2.0), read 2026-10-16. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
