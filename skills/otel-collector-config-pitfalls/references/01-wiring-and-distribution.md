# otel-collector-config-pitfalls §1 — Wiring and distribution

A Collector config is five kinds of component block plus a `service` block that wires them. Most "it starts and
nothing arrives" reports are in the wiring or in the image, not in a component's settings.

## 1.1 What the config does
The blocks are `receivers` (data in), `processors` (the middle, in listed order), `exporters` (data out),
`connectors` (the output of one pipeline as the input of another) and `extensions` (not in the data path). The
`service` block holds `extensions`, `pipelines` and `telemetry` (otelcol-doctor).
1. **Defining a component does nothing until a `service.pipelines.<signal>` entry references it.** otelcol-doctor
   calls such a config valid yet inert; Dash0 says the Collector rejects a config with a declared receiver,
   processor or exporter that no pipeline uses. The sources disagree on what happens, so the rule is not about the
   outcome: treat an unreferenced component as a defect, read the `service` block last, and learn what the
   Collector version in use does by validating a config that has one.
2. **A name used in a pipeline but not defined fails validation** (otelcol-doctor).
3. **Pipelines are per signal.** `traces`, `metrics` and `logs` are separate, and a component must support the
   signal of the pipeline it sits in: the `prometheus` receiver is metrics-only, so in a `traces` pipeline it fails
   (otelcol-doctor). Mixing signals in one pipeline is a configuration error (Dash0).
4. **Several pipelines of one signal use names**: `metrics/internal`, `metrics/app`, `traces/application`
   (otelcol-doctor; Dash0).
5. **A `health_check` extension has to be listed under `service.extensions` too**, or probes have no target
   (otelcol-doctor; Dash0).

## 1.2 Core versus contrib
1. **Many common components ship only in the contrib distribution.** otelcol-doctor lists: the `prometheus`
   receiver, `hostmetrics`, `filelog`, `kafka`, `resourcedetection`, the `transform` and `filter` processors,
   `tail_sampling`, the `spanmetrics` connector and the `prometheusremotewrite` exporter. The list is the
   source's, as of the commit in `origin.md`; check a component's own page for where it ships.
2. **Using a contrib component on the core image is a startup crash, not a YAML error**, so the config looks fine
   to a reader and to a linter (otelcol-doctor).
3. **The fix is the contrib image or a custom build with the OpenTelemetry Collector Builder** (otelcol-doctor).
   When a config uses a contrib-only component, say which image or build it needs.

## 1.3 Connectors
1. **A connector is an exporter in one pipeline and a receiver in another.** Declare it under `connectors:` and
   reference it in both pipelines; wiring it once produces no metrics or a validation error (otelcol-doctor).
2. **The usual miss is referencing `forward/x` or `spanmetrics` in `service.pipelines` without declaring it** under
   `connectors:`. Cross-check every name in `service.pipelines` against the blocks above it before handing a
   config back (otelcol-doctor).
3. **Several exporters in one pipeline each receive an independent copy of the data**, which roughly doubles the
   memory and network cost per extra exporter (Dash0).
4. **Shape of the wiring** (the `connectors:` block that declares `spanmetrics`, with its settings, is omitted;
   skeleton, not run through the validator):

```yaml
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter]
      exporters: [spanmetrics, otlp]
    metrics/spans:
      receivers: [spanmetrics]
      processors: [memory_limiter]
      exporters: [otlphttp]
```

## 1.4 Validate, and then review
1. **Run the Collector's own validator before declaring a config done**: `otelcol validate --config=config.yaml`,
   or `otelcol-contrib validate` for the contrib build. It loads and type-checks the whole config without starting
   it (otelcol-doctor). If the binary is not available, say so rather than claiming the config was validated.
2. **A config that parses is not reviewed** (o11y-dev). It can still have a memory limit above the pod's, stateful
   processors with no sticky routing, a queue on an unsafe filesystem and contradictory rollout settings. Review
   memory limits, replica strategy, routing, metric temporality state, queue storage medium and the disruption and
   autoscaling settings together, not the YAML alone.
3. **For "it starts but nothing arrives", check in this order** (otelcol-doctor): unwired components; undefined
   references; a signal mismatch; core versus contrib; processor order; a pull exporter where push was meant; a
   removed component (§3.1); a gRPC versus HTTP port mismatch; and the endpoint binding (§3.3). State the diagnosis
   as what was wrong, why it failed, and the fix, then validate the corrected config.
