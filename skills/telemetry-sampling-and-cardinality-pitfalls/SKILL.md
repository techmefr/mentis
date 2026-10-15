---
name: telemetry-sampling-and-cardinality-pitfalls
description: "Use when trace sampling, span-derived metrics or metric labels are configured in a Collector or SDK: why RED metrics computed from sampled traces are wrong and the fork that fixes it, tail sampling needing every span of a trace on one instance (a load-balancing tier), head sampling and the default SDK sampler, resource attributes copied onto every series, classifying attributes before keeping them as labels, aggregating labels instead of deleting keys, delta versus cumulative temporality, and why an unused metric is not necessarily safe to drop."
---

# telemetry-sampling-and-cardinality-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the telemetry pipeline between the application and the backend. The
three sections share one premise: **sampling and label choices change the numbers silently, and the dashboard
that shows them looks exactly as healthy as before**. What a reader must know about a sampled number, and the
bounded-label principle, are in `observability-instrumentation` §3 (rules 2, 5, 6 and 12); this block adds the
Collector mechanics and the attribute classification under them and does not restate those rules. The Collector's
own config traps are in `otel-collector-config-pitfalls`; PII in telemetry is out of scope here. Component names
and options move with Collector releases, so each such fact is labelled as the source states it and must be
re-checked against the current documentation.

## When
- Adding tail or head sampling, or a span-derived metrics connector, to a Collector.
- A dashboard or SLO is built on request rates derived from traces, and sampling is on or being added.
- A metrics bill, series count or backend limit grows, or a metric gains a label.
- A new resource attribute, instrumentation library or metrics exporter changes what lands on series.
- A backend drops or misreads metrics after a temporality or exporter change, or someone proposes dropping
  "unused" metrics.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Sampling and span-derived metrics: the fork, tail sampling topology, head sampling, the default SDK sampler | a sampler or a span-metrics connector is added or changed | [`01-sampling-and-span-metrics.md`](./references/01-sampling-and-span-metrics.md) |
| 2 | Cardinality and temporality: resource attributes, classifying labels, aggregating, delta versus cumulative, unused is not safe | a label is added, series grow, or a metric is dropped or converted | [`02-cardinality-and-temporality.md`](./references/02-cardinality-and-temporality.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the request count from the span-derived metric was compared with
the count of the traffic source over the same window with sampling on (§1.1), traces were generated across
replicas of the sampling tier and each arrived whole (§1.2), the series count of the metric was read before and
after a label change (§2.1), and the backend's own check of the dropped series was read after a temporality change
(§2.4). A config that was only reviewed is not verified.

## Guardrails
- Never compute RED metrics downstream of a sampler (§1.1).
- Never run `tail_sampling` on more than one replica without a trace-ID-keyed load balancing tier in front (§1.2).
- Never put an identifier, a stack trace or a raw URL on a metric (§2.2).
- Never delete a label key to cut cost; aggregate the label away (§2.3).
- Never convert temporality before checking the source, the backend and the replica routing (§2.4).
- Never drop a metric because no dashboard or alert uses it, without asking what else reads it (§2.5).
- Never take `AlwaysOn` in the SDK as a rule; it is one vendor's recommendation with a cost (§1.3).
- This block states Collector and backend behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md). The official OpenTelemetry documentation was not read, and
  nothing was run while writing it.

## Origin
Rewritten from the Dash0 agent skills (Apache-2.0, Collector sampling and RED metrics rules, spans rule), the
otelcol-doctor skill (Apache-2.0), the o11y-dev OpenTelemetry skill anti-patterns (Apache-2.0) and the SigNoz agent
skills (MIT, two telemetry cost references), read 2026-10-15. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
