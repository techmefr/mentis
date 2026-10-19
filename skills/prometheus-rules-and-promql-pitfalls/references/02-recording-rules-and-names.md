# prometheus-rules-and-promql-pitfalls §2 — Recording rules and names

A name is the only metadata a plain YAML rule file shows. A consistent scheme makes a wrong calculation look wrong
at a glance, which is the whole point of the recording-rule form and the metric conventions below.

## 2.1 Recording-rule names
1. **Name a recording rule `level:metric:operations`** (Prometheus docs). `level` is the aggregation level and the
   labels of the output, `metric` is the metric name, and `operations` lists what was applied, newest first.
2. **Keep the metric name unchanged**, except for stripping `_total` from a counter when `rate()` or `irate()` is
   applied. The unchanged name is what makes the series easy to find in the codebase (Prometheus docs).
3. **Keep the operations short.** Omit `_sum` when other operations are present, merge associative operations
   (`min_min` is `min`), use `sum` when no operation is obvious, and for a division separate the two metrics with
   `_per_` and call the operation `ratio` (Prometheus docs).
4. **For an average from a summary or histogram**, keep the metric name without the `_count` or `_sum` suffix and
   write `mean` in place of `rate` in the operations, for example `...:mean5m` (Prometheus docs).

## 2.2 Aggregating inside a rule
1. **Always write a `without` clause naming the labels you aggregate away.** It preserves every other label, such
   as `job`, which avoids conflicts and gives more useful metrics and alerts (Prometheus docs).
2. **Read the level against the name.** Labels listed in `without` leave the level of the output name compared with
   the input name; with no aggregation the levels match. A mismatch between the two means a mistake has probably
   been made in the rule (Prometheus docs).
3. **Aggregate ratios in the same two steps as a query** (§1.2): record the numerator and the denominator rates,
   sum each, then divide, at each level you need.

```yaml
groups:
  - name: shop_requests
    rules:
      - record: instance_path:request_failures:rate5m
        expr: rate(request_failures_total{job="shop"}[5m])
      - record: instance_path:requests:rate5m
        expr: rate(requests_total{job="shop"}[5m])
      - record: job:request_failures_per_requests:ratio_rate5m
        expr: |2
            sum without (instance, path) (instance_path:request_failures:rate5m{job="shop"})
          /
            sum without (instance, path) (instance_path:requests:rate5m{job="shop"})
```

4. **A linter can hold the label contract.** pint's `aggregate` check can require that matching rules keep a label
   such as `job` or strip one such as `instance` (for series meant for federation, where only aggregates are
   allowed). It is not enabled by default and needs `rule` blocks that say which rules it applies to (pint).

## 2.3 Metric and label names
1. **The conventions are a style guide, not a requirement.** The Prometheus page says organisations may approach
   some of them, naming among them, differently. Pick one scheme and enforce it with a linter instead of by memory
   (Prometheus docs; the enforcement is our own guidance).
2. **Use base units and name the unit as a plural suffix.** Seconds, bytes and meters rather than milliseconds,
   megabytes and kilometers; `http_request_duration_seconds`; an accumulating count ends in `_total`, after the
   unit when there is one (`process_cpu_seconds_total`). Bits are exported as bytes, and a percentage is a ratio
   from 0 to 1 (Prometheus docs).
3. **One name, one unit and one quantity.** Never mix seconds with milliseconds, or request size with request
   duration. As a test, either `sum()` or `avg()` over all dimensions of the metric should be meaningful; if not,
   split it into several metrics (Prometheus docs).
4. **Use a label for a characteristic, not a new metric and not part of the name.** One `http_responses_total` with
   a `code` label, not `http_responses_500_total` and `http_responses_403_total`. No part of a metric name should be
   procedurally generated, except when proxying metrics from another monitoring system. Do not put a label's name
   in the metric name: it is redundant and confusing once that label is aggregated away (Prometheus docs).
5. **Every label combination is a series.** Never use a user id, an email address or another unbounded set as a
   label. The instrumentation page's guidance is to keep cardinality below 10, to limit metrics above that to a
   handful across the whole system, to investigate anything above 100 or able to grow that far, and to start with
   no labels and add them when a use case appears (Prometheus docs). That is a different figure from the 100-value
   heuristic in `telemetry-sampling-and-cardinality-pitfalls` §2.2, and both are sources' numbers, not measured
   limits; classify the attribute first.
6. **Keep unit and type in the name even if the data model stores them elsewhere.** The Prometheus page says so
   explicitly while noting that OpenTelemetry conventions do not recommend it, with two reasons: rules, dashboards
   and alerts are mostly read as plain YAML where the name is the only hint, and series with the same name in
   seconds and milliseconds collide (Prometheus docs). Where a metric travels OpenTelemetry to Prometheus, how the
   suffixes are added was not read.
7. **Export a timestamp, not an elapsed time.** For "time since the last success", export the Unix timestamp and
   compute `time() - my_timestamp_metric` in the query: there is no update logic to get stuck (Prometheus docs).
