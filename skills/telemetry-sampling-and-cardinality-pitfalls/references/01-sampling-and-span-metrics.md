# telemetry-sampling-and-cardinality-pitfalls §1 — Sampling and span-derived metrics

Sampling keeps a subset of traces. Anything computed from the subset describes the subset, and the dashboard does
not say so.

## 1.1 Metrics from sampled traces are wrong
1. **RED metrics derived from sampled traces are wrong by the sampling ratio, and nothing looks broken.** Head
   sampling underestimates counts and skews histograms; tail sampling over-represents errors and slow requests
   (Dash0; otelcol-doctor).
2. **Generate span-derived metrics from every span, upstream of any sampler.** If `tail_sampling` or any sampler
   runs before the connector that makes the metrics, the connector counts only the survivors (otelcol-doctor;
   Dash0).
3. **Fork the traces instead.** The ingest traces pipeline exports to the metrics connector and to a `forward`
   connector; a second traces pipeline receives the `forward` connector, applies the sampler and exports to the
   trace backend (otelcol-doctor). The connectors are declared under `connectors:` (`otel-collector-config-pitfalls`
   §1.3). Skeleton of the `service` block, not run through a validator:

```yaml
service:
  pipelines:
    traces/ingest:
      receivers: [otlp]
      processors: [memory_limiter]
      exporters: [spanmetrics, forward/sampled]
    traces/sampled:
      receivers: [forward/sampled]
      processors: [memory_limiter, tail_sampling]
      exporters: [otlp]
    metrics/spans:
      receivers: [spanmetrics]
      processors: [memory_limiter]
      exporters: [otlphttp]
```

4. **One source's own full example contradicts its prose.** Dash0 says the metrics connector must see every span,
   then shows a single `traces` pipeline whose processors include `tail_sampling` and whose exporters include the
   connector. By the pipeline model otelcol-doctor states (receivers, processors in listed order, then exporters),
   the processors run first, so that example would count only the sampled traces. Own reading, not run: follow the
   fork of the previous point.
5. **Two connectors make these metrics, and they differ in names.** `spanmetrics` has RED built in with generic
   metric names; `signaltometrics` is defined by OTTL expressions and can match the semantic-convention names
   exactly. Dash0 recommends `signaltometrics` where dashboards and SLOs rely on standard names (Dash0;
   otelcol-doctor). Check which of them the distribution you run includes.

## 1.2 Tail sampling topology
1. **`tail_sampling` needs every span of a trace on one instance.** With more than one replica, put a
   `loadbalancing` exporter keyed by trace ID (`routing_key: traceID`) in an agent tier in front of the gateway
   tier that samples. A plain load balancer in front of the samplers is broken sampling: spans of one trace split
   across instances and the decisions diverge (otelcol-doctor; o11y-dev; Dash0).
2. **Tail sampling on the agents themselves has the same flaw**: each agent sees only the spans of its local pods
   (Dash0).
3. **In Kubernetes the discovery has to return pod addresses**: the load balancing exporter resolves the gateway
   through DNS, so the gateway needs a headless Service; a ClusterIP returns one virtual address and defeats the
   hashing (Dash0). DNS discovery is eventually consistent, so scaling the gateway can briefly split traces.
4. **The sampling tier is stateful.** A gateway pod cannot stop without losing the spans it buffers, so it needs a
   `preStop` and a graceful period (Dash0; see `kubernetes-workload-pitfalls` §2). Spans also cross availability
   zones, because routing is by trace ID, not by zone (Dash0).
5. **There is no end-of-trace marker**: `tail_sampling` waits `decision_wait`, then decides with the spans that
   arrived. Too short a wait for long operations decides on incomplete traces; when `num_traces` is exceeded the
   oldest traces are decided early. Memory grows linearly with `decision_wait`, traces per second, spans per trace
   and span size, so size the container limit first and derive the memory limiter from it
   (`otel-collector-config-pitfalls` §2.1). Dash0's starting point is a `decision_wait` of `30s`, one source's value.
6. **Policies**, as Dash0 recommends them: keep traces with an error span, traces over a latency threshold, and a
   probabilistic baseline of normal traces; the sampler keeps a trace when any policy matches.

## 1.3 Head sampling and the SDK sampler
1. **Head sampling by trace-ID probability needs no coordination**: every instance reaches the same decision for the
   same trace. Its limit is that the decision comes before the outcome is known, so at low rates errors, latency
   spikes and rarely exercised paths are likely to be missed (Dash0). Dash0 uses it as a coarse reduction or where
   tail sampling is too complex for the environment.
2. **Where sampling lives is a trade.** Dash0 puts every decision in the Collector, because it can then change
   centrally without redeploying applications, and because an SDK-side ratio sampler decides irreversibly at the
   head of the trace (Dash0).
3. **The default SDK sampler is `ParentBased(root=AlwaysOn)`** (`parentbased_always_on`), as Dash0 states it; the
   specification page it links was not read. Under it the `sampled` flag of the incoming `traceparent` decides
   whether a service records spans, so an outside caller who clears the flag silences the service and everything
   downstream of it, with no error (Dash0).
4. **Dash0's recommendation is an explicit `always_on` in the SDK, unless every ingress path strips or replaces
   `traceparent` and `tracestate` and that was verified per path.** It is an optional vendor opinion, not a rule
   of this block: it costs export bandwidth and ingest volume, and spans whose remote parent was never exported make
   a trace appear to start at the service (Dash0). Decide with the trust boundary in view, write the decision down.
5. **The Collector cannot recover spans an SDK never recorded** (Dash0): whatever sampler the SDK runs sets the
   ceiling for the Collector's sampling.
