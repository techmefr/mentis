---
name: datastore-broker-alerting-signals
description: "Use when writing or reviewing alert rules for Redis, Elasticsearch, RabbitMQ or Kafka: which store and broker signals to alert on (instance down, replication, cluster state, memory and connections, broker alarms, in-sync replicas, consumer lag and its trend, red and yellow status, unassigned shards, thread-pool rejections, circuit breakers), with which hold duration and severity."
---

# datastore-broker-alerting-signals

Step 6 of the pipeline (`WORKFLOW.md`), complementing `observability-instrumentation` §4 (what an alert must
be) with the engine-specific signals that a generic rule cannot name. The premise: **a store or a broker
usually announces its own failure through a few well-known states** (a broker alarm that blocks every
publisher, a cluster that cannot serve queries, a lag that only grows), **and an alert on the raw count of
something noisy finds them later than an alert on the state itself**. This block lists those states for Redis,
Elasticsearch, RabbitMQ and Kafka, each with the hold duration and severity of the source.

Alert rules rewritten from awesome-prometheus-alerts by Samuel Berthe (CC BY 4.0). Credit, link and the changes
made are in [`references/origin.md`](./references/origin.md).

## When
- An alert is written or reviewed for one of the four engines.
- An incident went unnoticed because the signal was not alerted, or a noisy alert is being replaced.
- A dashboard is turned into alerts and needs conditions that mean something.

## Steps

**Read §1 first, then the section for the engine.** The signals are tables of what each alert fires on; the
metric names belong to the exporter named in each section and must be checked against the exporter you run.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | How to read and adapt the signals: hold, severity, ratios, counters, thresholds, exporter names | always, before copying a rule | [`01-reading-the-signals.md`](./references/01-reading-the-signals.md) |
| 2 | Redis and Elasticsearch | the engine is a store | [`02-stores.md`](./references/02-stores.md) |
| 3 | RabbitMQ and Kafka | the engine is a broker | [`03-brokers.md`](./references/03-brokers.md) |

## Output / checkpoint
Each alert carries its signal, its hold duration, its severity, the exporter metric it reads (checked against
the exporter's own output), the threshold's origin (§1.5), and what the responder does when it fires. An alert
that was never made to fire has not been checked (`observability-instrumentation` §4.2).

## Guardrails
- Never copy a threshold without saying where its number came from (§1.5).
- Never alert on a cumulative counter's raw value (§1.4).
- Never copy a rule that hard-codes a placeholder queue or topic name as if it were a rule (§3.1).
- Never assume a metric name from another exporter or another version (§1.6).
- Metric names and thresholds are the source's at the stamped commit; nothing here was run against an
  exporter (🟡).

## Origin
Rewritten from the Redis, Elasticsearch, RabbitMQ and Kafka rule groups of `_data/rules.yml` in
samber/awesome-prometheus-alerts (alert rules and content CC BY 4.0, commit 822af1e), read 2026-10-16. Credit,
changes, decisions and open points are in [`references/origin.md`](./references/origin.md).
