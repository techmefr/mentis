# prometheus-rules-and-promql-pitfalls §1 — Queries

PromQL does not reject a meaningless expression: it evaluates it. The checks below are the ones that fail
silently, as an empty vector, a drifting number or a result that is right only on one instance.

## 1.1 Counters, gauges and the range
1. **`rate()`, `irate()` and `increase()` take counters only.** Any metric type is accepted and a value comes back,
   but a counter is only allowed to rise, and any drop is read as a counter overflow or reset, so a gauge gives
   wrong rates. Use `delta()` or `deriv()` for a gauge (pint). The Prometheus documentation gives the test: if the
   value can go down, it is a gauge, and a `rate()` of a gauge is never right.
2. **The range must cover at least 2x the scrape interval.** Prometheus needs at least two samples inside the range
   to calculate a rate; pint compares the range with the global `scrape_interval` of the server it checks.
3. **Rate first, then sum: never `rate(sum(counter))`.** pint states that `rate()` over `sum(counter)` always
   returns invalid results, and that such a chain can only reach a rule through a metric produced by a recording
   rule. So never record a `sum` of a counter and take the `rate` of the recorded series afterwards.
4. **One metric name, one type.** pint decides a metric's type from the metadata API, which is aggregated across
   everything scraped, so only the name tells it which series is which type. After a type is corrected, the old
   type stays in the metadata until the last target still exporting it is updated, so a warning that persists after
   a fix usually means the fix has not reached every target (pint).
5. **A summary or classic histogram `_sum` can fall when observations can be negative.** The fall is read as a
   counter reset in `rate(..._sum[5m])` and the result is wrong. Native histograms are rate'd as a whole and do
   not have this problem. If negative observations cannot be avoided with a summary or classic histogram, the
   source's way out is two metrics, one for positive values and one for negative values with the sign inverted,
   combined in PromQL (Prometheus docs).

## 1.2 Aggregating ratios, averages and quantiles
1. **Aggregate a ratio by summing the numerator and the denominator separately, then dividing.** Never take the
   average of a ratio or the average of an average: it is not statistically valid (Prometheus docs).
2. **An average observation, from a histogram or a summary, is `rate(sum)` over `rate(count)`.** Both series are
   additive, so aggregate after the `rate` and before the division, whatever the metric type (Prometheus docs).
   Per job, for a classic histogram or summary called `checkout_latency_seconds`:

```
sum by (job) (rate(checkout_latency_seconds_sum[5m]))
/
sum by (job) (rate(checkout_latency_seconds_count[5m]))
```

3. **Summary quantiles cannot be aggregated.** Averaging the pre-computed 0.95 quantile of several replicas yields
   statistically meaningless values; the source marks `avg(...{quantile="0.95"})` as the wrong form. Histogram
   buckets can be aggregated: for a classic histogram, sum the rate of the `_bucket` series `by (le)` and pass the
   result to `histogram_quantile()` (Prometheus docs).

```
histogram_quantile(0.95, sum by (le) (rate(checkout_latency_seconds_bucket[5m])))
```

4. **A quantile from a classic histogram is an estimate bounded by the width of the bucket it falls in.** The
   source's worked case puts a true value near 220 ms in a bucket spanning 200 to 300 ms and gets an estimate of
   295 ms, which looks close to a 300 ms objective when the real value is well inside it. Check the bucket layout
   against the threshold before reading a percentile against an objective (Prometheus docs).
5. **A classic-histogram fraction needs a bucket boundary exactly at the threshold.** With `le="0.3"` and no such
   bucket the query returns nothing; if only some of the series have it the result is incomplete and carries no
   warning (Prometheus docs).
6. **Which type to instrument, in the source's order** (Prometheus docs): native histograms where the client
   library and server support them, because quantiles, windows and aggregation stay ad hoc; classic histograms when
   aggregation is needed and native ones are not available, with buckets chosen to cover the range and the
   thresholds; summaries only when no aggregation across instances is needed. Changing a classic bucket layout
   later disrupts aggregation across the change. **Version-bound, re-check:** at its commit the source calls native
   histogram support in client libraries rare and limited to protobuf exposition, and describes ingesting classic
   histograms as native histograms with custom bucket boundaries as a middle path.

## 1.3 Matching, labels and selectors
1. **Vector matching between series with different label sets returns nothing.** A per-instance series divided by
   a per-cluster series matches no pair; add `ignoring(instance)` (or `on(...)`) so only the shared labels are
   compared. pint's check first runs the query and only if it is empty samples a few series from each side, so it
   can miss cases (pint).

```
http_errors / ignoring(instance) cluster:http_errors
```

2. **An aggregation removes labels, and later steps may refer to labels that are gone.** pint reports three shapes:
   `foo unless sum(foo)` can never match, because `sum()` leaves an empty label set on the right; a
   `group by (cluster)` over `sum(errors)` has no `cluster` left to group by; and `sum(foo) / on(cluster)
   count(bar)` has nothing to join on (pint).
3. **A join that adds labels must wrap the whole filtered expression.** In
   `A and on(instance) B * on(cluster) group_left(env) info`, the extra labels attach only to `B`, so they never
   reach the result; wrap `A and on(instance) B` in parentheses before the join (pint).
4. **Regexp matchers are fully anchored.** `foo=~"bar.*"` is parsed as `^bar.*$`, so an anchor you write is
   redundant (the source says written anchors would be doubled); and a regexp with no pattern, such as
   `job=~"bar"`, should be `job="bar"`, which is cheaper (pint, citing the Prometheus querying documentation).
5. **A regexp used to take one label value apart is a label design defect.** When `job` holds
   `service_cluster1_production`, every query needs a regexp, typos are easy and aggregating by cluster or
   environment is hard. Set `job`, `cluster` and `env` as separate labels from the scrape configuration and select
   on them with equality (pint).
6. **A range longer than retention returns only what is stored.** `avg_over_time(foo[40d])` on a server that keeps
   30 days is the average over 30 days, never more, which hides a mismatch between expected and real retention. pint reads the time-based retention flag
   and ignores disk-based limits, because they do not tell the effective time retention (pint). **Version-bound,
   re-check:** the source states 15 days as the default retention at its commit.
