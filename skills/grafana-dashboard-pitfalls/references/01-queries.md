# grafana-dashboard-pitfalls §1 — Queries

A panel query runs at whatever resolution the viewer selects. A range that fits one zoom level starves the next, and
a query that names no job or instance mixes everything it can reach.

## 1.1 The range of `rate`, `irate` and `increase`
1. **Use `$__rate_interval` as the range of every `rate`, `irate` and `increase` in a panel target.** The linter's
   rule ensures there is always a sufficient number of data points to calculate a useful result, which a fixed range
   such as `[5m]` does not guarantee at every zoom level (dashboard-linter).
2. **A fixed period is the deliberate exception.** When the panel is meant to show the rate or increase over a fixed
   span, such as the last 24 hours, or over the selected range, such as a "top 10" for the current range, keep the
   fixed value and write a lint exclusion for that panel with the reason (dashboard-linter; §2.5).
3. **Version-bound, re-check.** The rule's linked explanation is a Grafana blog post whose address names Grafana 7.2;
   the version that introduced `$__rate_interval` and how it is computed were not read, so check the Grafana
   documentation for the version in use before relying on its exact semantics.
4. **The range still has to cover the scrape interval.** `$__rate_interval` is a Grafana variable; the rule that a
   `rate` range must hold at least two samples is a Prometheus one, in `prometheus-rules-and-promql-pitfalls` §1.1
   (our own link between the two).

```
sum by (job) (rate(requests_total{job=~"$job", instance=~"$instance"}[$__rate_interval]))
```

## 1.2 Loki range queries and `$__auto`
1. **Use `$__auto` for the range vector of a Loki metric query instead of a fixed range.** The linter's rule says it
   gives a consistent approach across the dashboard and picks the right form for the query type: the interval for a
   range query and the selected time range for an instant query, substituted automatically with the step value or
   the time range respectively (dashboard-linter).

```
sum(count_over_time({job="mysql"} |= "duration" [$__auto]))
```

2. **A fixed Loki range is allowed when the query needs it**, with an exclusion that says so (dashboard-linter).
3. **Version-bound, re-check.** The rule links Grafana Cloud documentation for the variable, which was not read;
   confirm `$__auto` support in the Grafana and Loki data source versions in use.

## 1.3 Matchers and valid queries
1. **Every PromQL query carries a `job` matcher and an `instance` matcher**, filtered by the dashboard's variables.
   The two rules go with the two template variables of §2.2: they enforce a practice for dashboards over a single
   Prometheus or Loki data source, because the `job` and `instance` labels are generated automatically on scraped
   data and so are always present to filter on (dashboard-linter).
2. **A dashboard over several data sources is the documented exception.** Filtering on `job` and `instance` then
   needs heavy relabelling so the two labels match across sources, because their defaults differ or are absent in
   logs; the source's example is a combination of container metrics and Docker daemon logs. For such a dashboard
   create a lint exclusion and filter on a separate label that exists in all of the sources (dashboard-linter).
3. **Every query must parse.** One rule checks that each Prometheus target uses a valid PromQL query, another that
   each Loki target uses a valid LogQL query, and a third that the PromQL of a template variable's own query is
   valid. The PromQL check does not run against non-Prometheus targets (dashboard-linter).
4. **A counter metric (ending in `_total`) is aggregated with `rate`, `irate` or `increase`**, and every panel has
   at least one target. Both are named in the linter's rule list without a page of their own, so only their
   one-line descriptions were read (dashboard-linter, index line).
