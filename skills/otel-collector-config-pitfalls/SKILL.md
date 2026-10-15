---
name: otel-collector-config-pitfalls
description: "Use when an OpenTelemetry Collector configuration is written, debugged or reviewed, especially when it starts but no data arrives: wiring components into per-signal pipelines, core versus contrib distributions, connectors, validating, memory_limiter and its limit, the batch processor question, OTTL path forms and typing, otlp versus otlphttp, prometheus pull versus remote write and their queue keys, removed components, persistent queue storage, and where receivers and debug extensions are bound."
---

# otel-collector-config-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the Collector's own YAML. The three sections share one premise: **a
Collector config that parses is not a config that works, because most of its failures are silent: a component
nobody wired, a limit above the pod's limit, a queue the exporter ignores**. Signal-level rules (what to log,
which label, which span) are in `observability-instrumentation`; sampling and span-derived metrics are in
`telemetry-sampling-and-cardinality-pitfalls`; probes, resource limits and volumes of the pod that runs the
Collector are in `kubernetes-workload-pitfalls`. Component names, removals and defaults move with every Collector
release, so each such fact below is labelled as the source states it and must be re-checked against the current
Collector documentation.

## When
- Writing a Collector config, or reading one that starts and sends nothing.
- A component is rejected at startup, or the Collector is OOM-killed under load.
- Choosing receivers, processors, exporters or connectors, or moving to the contrib image.
- Adding a persistent queue, an OTTL transform or a Prometheus exporter.
- Reviewing a config before it is deployed.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Wiring and distribution: pipelines, core versus contrib, connectors, validate, review | a config is written, or starts and sends nothing | [`01-wiring-and-distribution.md`](./references/01-wiring-and-distribution.md) |
| 2 | Processors and memory: memory_limiter, the batch question, order, OTTL | a processor chain is written or the Collector is OOM-killed | [`02-processors-and-memory.md`](./references/02-processors-and-memory.md) |
| 3 | Exporters, queues and exposure: otlp versus otlphttp, Prometheus, queue keys, removed components, binding | an exporter is chosen, a queue added, or an endpoint exposed | [`03-exporters-queues-and-exposure.md`](./references/03-exporters-queues-and-exposure.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the config was loaded by the validator of the distribution that
will run it (§1.4), data was sent through each pipeline and arrived at its destination, the Collector's memory
limit and the limiter's `limit_mib` were read side by side (§2.1), the queue was exercised by stopping the backend
and restarting the Collector (§3.2), and the exposed ports were listed from outside the pod (§3.3). A config that
only passed the validator is not verified (§1.4).

## Guardrails
- Never call a config done because `otelcol validate` accepts it (§1.4).
- Never leave a component defined and unreferenced by a pipeline (§1.1).
- Never use a contrib component on the core image, and never assume the image from the YAML (§1.2).
- Never declare a connector in only one pipeline, or use one without declaring it under `connectors:` (§1.3).
- Never put another processor before `memory_limiter` (§2.1).
- Never set `limit_mib` above the container's memory limit (§2.1).
- Never carry a rule on the `batch` processor from this block; check the current documentation (§2.2).
- Never mix the two OTTL path forms in one statement list (§2.4).
- Never back a file-storage queue with a network or shared-write volume (§3.2).
- Never bind `pprof` or `zpages` to all interfaces in production (§3.3).
- This block states Collector behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md). The official Collector documentation was not read, and nothing
  was run while writing it.

## Origin
Rewritten from the otelcol-doctor skill (Apache-2.0), the o11y-dev OpenTelemetry skill anti-patterns reference
(Apache-2.0) and the Dash0 agent skills Collector rules (Apache-2.0), read 2026-10-15. 🟡: never run by us; open
points are in [`references/origin.md`](./references/origin.md).
