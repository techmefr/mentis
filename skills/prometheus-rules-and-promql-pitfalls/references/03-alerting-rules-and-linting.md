# prometheus-rules-and-promql-pitfalls §3 — Alerting rules, restarts and linting

An alerting rule is evaluated by a server that restarts, scrapes targets at different moments and loses its memory
of what it saw. Most false firings and silent non-firings come from that, not from the threshold. The philosophy of
what deserves a page is in `observability-instrumentation` §4; this section adds what the Prometheus documentation
says per kind of service and the traps of rule evaluation.

## 3.1 `for`, restarts and flapping
1. **An `absent()` alert needs a `for` of at least 2x the scrape interval.** After a restart the rule can be
   evaluated before the series it tests have been scraped, and `absent()` fires falsely. pint warns when `for` is
   missing or shorter (pint).
2. **An alert comparing two aggregations over different jobs can fire falsely right after a restart.** Prometheus
   spreads the first scrape of its targets over the first scrape interval, so until it finishes, an aggregation
   covers only the targets scraped so far, and a ratio of two such aggregations can read artificially high. Run
   by hand later, the same query uses all targets and shows nothing wrong, so the cause cannot be reproduced (pint).
3. **Decision on the length of `for`.** pint's `absent` check says at least 2x the scrape interval; its `fragile`
   check says at least one scrape interval. Use 2x for both: it satisfies the stricter of the two, and the
   difference is one interval. (Our own decision.)
4. **A sampling function in an alert makes the alert set unstable.** With `topk(10, mymetric > 0)`, the labels of
   each returned series become labels of the alert, so a different set of series on each evaluation means a
   different set of alerts, and they flap (pint).
5. **Export a default value for a series you know may exist.** A series that appears only when something happens
   breaks the usual operations; export `0` in advance. Most Prometheus client libraries do it for metrics with no
   labels (Prometheus docs).

```yaml
groups:
  - name: shop_alerts
    rules:
      - alert: ShopMetricsMissing
        expr: absent(up{job="shop"})
        for: 4m
```

The sample assumes a scrape interval of 2 minutes or less. The name is Camel Case, which the Prometheus page
reports as the community convention for alert names; alert names have no strict restriction otherwise.

## 3.2 What the rules page on, per kind of service
Everything here is the Prometheus documentation's guidance (alerting and instrumentation pages); the general
principle (symptoms, not causes) is in `observability-instrumentation` §4.
1. **Online serving: page on latency and error rate as high in the stack as possible**, and only on latency at one
   point of the stack. A slow lower-level component with fine user latency needs no page. Page on user-visible
   errors; add a page for a failure that is not user-visible only when it is severe, such as losing money.
2. **Offline processing: page on how long data takes through the system.** Last-processed-time is localised
   information; a heartbeat item passed through every stage, with each stage exporting the latest heartbeat
   timestamp it saw, shows end-to-end propagation. Systems without quiet periods may not need one.
3. **Batch jobs: page when the last success is too old, by at least two full runs.** For a job that runs every
   4 hours and takes 1 hour, the source calls 10 hours reasonable. If one failed run cannot be tolerated, run the
   job more often: one failure should not need a human. The key metrics are the last success time, stage and
   overall durations and the last completion time, all gauges pushed to a Pushgateway; for jobs that run longer
   than a few minutes, also scrape them. A job that runs more often than every 15 minutes is a candidate for a
   daemon handled as offline processing.
4. **Capacity: being close to it often needs a human before an outage**, though it is not user impact yet.
5. **Allow slack for small blips**, and link each alert to the console that shows which component is at fault.

## 3.3 Metamonitoring
1. **Alert on the monitoring itself.** Have alerts that the Prometheus servers, the Alertmanagers, the
   Pushgateways and the other monitoring components are available and working (Prometheus docs).
2. **A black-box test of the whole path beats an alert per component.** An end-to-end check that alerts reach
   Prometheus, then the Alertmanager, then the receiver (the source's example ends at email) catches what
   individual alerts miss; external black-box monitoring is also the fallback when internal systems fail
   completely (Prometheus docs).

## 3.4 Linting rules with pint
1. **pint checks several of the traps above statically**: `promql/rate` (range against twice the scrape interval,
   counters only, `rate` over `sum`), `promql/vector_matching`, `promql/impossible`, `promql/regexp`,
   `promql/range_query` against retention, `promql/fragile`, `alerts/absent` and `promql/aggregate` (pint).
2. **Several checks read from a Prometheus server, not only from the file.** The rate check uses the server's
   `scrape_interval` and metric metadata, the range check uses its retention flag, and the vector-matching check
   samples live series; these run for the Prometheus servers configured in pint. A lint run with no server
   configured cannot make them (pint; the last sentence is our reading of that).
3. **A check that found nothing is not proof.** The vector-matching check samples only a few series and says it
   may miss issues (pint). Treat the linter as a net for the common shapes, not as a replacement for running the
   expression (§1).
4. **Run the linter in CI on every change to a rule file** (our own guidance). Which checks to enable, and at
   which severity, is a decision for the team; the `aggregate` check in particular does nothing until configured.
