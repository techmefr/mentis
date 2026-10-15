# prometheus-rules-and-promql-pitfalls: origin and source stamps

> Provenance of `skills/prometheus-rules-and-promql-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No Prometheus server was
started, no rule was evaluated and no linter was run while writing it. The Prometheus reference documentation
(function and operator pages) was not read; every claim rests on the two repositories below.

## Sources (all re-read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| prometheus/docs (sparse checkout, commit e473448), `docs/practices/alerting.md`, `rules.md`, `naming.md`, `instrumentation.md` and `histograms.md`, each in full | Apache-2.0 (repository LICENSE file, standard Apache-2.0 text; the NOTICE file credits the Prometheus Authors) | Counter versus gauge, the average and quantile aggregation rules, histogram and summary trade-offs, the recording-rule naming form and `without`, metric and label naming, the alert guidance per kind of service, batch jobs, metamonitoring, missing series, timestamps |
| cloudflare/pint (commit df254f8), `docs/checks/promql/rate.md`, `fragile.md`, `impossible.md`, `aggregate.md`, `vector_matching.md`, `regexp.md`, `range_query.md` and `docs/checks/alerts/absent.md`, each in full | Apache-2.0 (repository LICENSE file, standard Apache-2.0 text) | The two-sample range rule, rate on counters, `rate(sum())`, metadata mismatch, topk and restart flapping, impossible and mismatched matching, anchored regexp, smelly selectors, retention versus range, the `absent` `for` rule, the `aggregate` check |

The licence of both repositories was verified again from the LICENSE file in this session. Nothing in the cloned
files was an instruction to us; the Prometheus alerting page opens by pointing at an external document on alerting
philosophy, which was not read and is not used. Samples are our own, built on the sources' mechanisms with our own
metric and job names; the `|2` block-scalar layout of the recording-rule sample is the layout the Prometheus
rules page uses.

## Rewrite notes
Labels "(Prometheus docs)" and "(pint)" mark which source states a rule. Figures (2x the scrape interval, 10 hours
for a 4-hour job, cardinality 10 and 100, 15 days of retention, 15 minutes for a daemon) are the sources' and are
labelled as such where they are not mechanisms.

## Removed
Nothing from the review item was dropped for lack of a source. Left out as outside the item or tool-specific:
1. The alerting-philosophy paragraph's external document (not read) and the `promql/*` pint checks outside the
   item (`counter`, `nan`, `offset`, `series`, `selector`, `features`, `syntax`) and the `alerts/*` and `rule/*`
   checks other than `absent` (not read in this pass).
2. The Prometheus pages on consoles, pushing, remote write and the Zen page (not read).
3. Pint's configuration blocks, snooze and disable comment syntax.
4. The apdex expressions of the histograms page and its heatmap discussion.

## Decisions where sources disagree
1. **The length of `for` after a restart**: pint's `absent` check says at least 2x the scrape interval, and its
   `fragile` check says at least one scrape interval. The block states 2x for both, as our decision, because it
   satisfies both.
2. **Unit and type in the metric name**: the Prometheus naming page recommends them strongly and says
   OpenTelemetry conventions do not. The block follows the Prometheus page for metrics queried in PromQL and notes
   that the OpenTelemetry side was not read.
3. **Cardinality figures**: the instrumentation page says below 10, investigate above 100; another block of ours
   carries a different source's "below 100 per attribute". The block states both as sources' numbers.

## Not verified
1. **Every default and feature status**: the 15 days of retention, native histograms and their custom-bucket
   ingestion path, and which client libraries support them, are as the Prometheus pages state them at commit
   e473448; the histograms page itself links a 2026 blog post. Re-check against the Prometheus version in use.
2. **pint's behaviour** (what each check samples, which flags it reads) is its documentation's description; pint
   was not run. That a lint run without a configured server cannot make the server-backed checks is our reading of
   "enabled for all configured Prometheus servers".
3. **That `rate(sum())` always returns invalid results** is pint's statement, which links an external post that was
   not read.
4. **The arithmetic of the sources' worked examples** (the 295 ms estimate, the 10-hour threshold) was not
   reproduced.
5. **Written by us, not sourced:** the decision on the length of `for`, the advice to run pint in CI, the reading of
   the server-backed checks, the sample queries and rules, the Output / checkpoint paragraph, and the sentence in
   §2.3 that the enforcement of a naming scheme should be by a linter.

## Related blocks
`observability-instrumentation`, `telemetry-sampling-and-cardinality-pitfalls`, `otel-collector-config-pitfalls`,
`source-freshness`.
