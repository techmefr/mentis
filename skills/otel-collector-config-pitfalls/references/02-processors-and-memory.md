# otel-collector-config-pitfalls §2 — Processors and memory

Processors run in the listed order, and the order is load-bearing. The first processor decides whether a burst is
shed or kept in memory until the process dies.

## 2.1 memory_limiter
1. **`memory_limiter` is the first processor in every pipeline that can be flooded.** It has to see data before
   anything buffers it; with another processor ahead of it, memory grows unchecked during a burst or back-pressure
   before the limiter can shed load (otelcol-doctor; o11y-dev; Dash0).
2. **Set `limit_mib` to roughly 80 percent of the container's memory limit** (o11y-dev; Dash0). Above the
   container limit the Go runtime can allocate beyond the cgroup limit before the limiter fires, and the container
   is OOM-killed with no graceful shedding (o11y-dev).
3. **How it behaves, as Dash0 describes it**: above `limit_mib` minus `spike_limit_mib` the processor starts
   refusing data, above `limit_mib` it drops data to protect the process. Dash0's starting values are a
   `check_interval` of `1s` and a `spike_limit_mib` of 25 percent of `limit_mib`; they are one source's values, not
   measurements for your load.
4. **The pod's own limit is a separate setting that has to agree.** Where memory also scales with a sampler's
   buffer, size the container limit first and derive `limit_mib` from it
   (`telemetry-sampling-and-cardinality-pitfalls` §1.2). Resource limits for the pod itself are in
   `kubernetes-workload-pitfalls` §3.

## 2.2 The batch processor: not settled here
1. **The sources disagree, and between two of them on where.** otelcol-doctor puts `batch` last, just before
   export; o11y-dev calls omitting it an anti-pattern and puts it immediately after `memory_limiter`, because
   without it every item is exported on its own and throughput drops. Dash0 says not to use the `batch` processor
   at all: it buffers in memory, so a crash loses what it holds, and Dash0 relies instead on the exporter's
   `sending_queue` with persistent storage (§3.2).
2. **Decision: this block records no rule on `batch`.** Check the current Collector documentation for the status of
   the processor and for exporter-level batching in the version you run, write the choice and the reason down in
   the review, and re-check on upgrade. Whatever is chosen, `memory_limiter` stays first (§2.1).

## 2.3 The rest of the order
Dash0's order is one source's sequence, not a rule of the Collector: `memory_limiter`, then `resourcedetection` and
`k8sattributes`, then `resource`, then redaction processors, then other `transform` and `filter` processors.
1. **Redaction runs after enrichment and before the exporters**, so it sees every attribute that has been set
   (Dash0).
2. **Keep SDK-set attributes**: `resourcedetection` with `override: false` preserves what the application set, and
   `insert` rather than `upsert` for the service identity attributes keeps the SDK's value. Overwriting them
   disconnects telemetry from the service that produced it (Dash0).
3. **`k8sattributes` needs RBAC** on the Collector's service account; without it the processor fails silently and
   the telemetry is not enriched (Dash0).
4. **A `filter` that drops a metric is scoped to the instrumentation scope that produces it** as well as the
   name; a name-only filter can drop a legitimate metric of the same name from another source (Dash0).

## 2.4 OTTL in transform and filter
1. **There are two statement forms with different path syntax, and mixing them fails to parse.** In a flat list,
   every path carries its context prefix (`span.attributes[...]`); inside a `context: span` block the paths are
   bare (`attributes[...]`). Pick one form per statement list (otelcol-doctor).
2. **Set `error_mode` explicitly, and remember the regular expressions are RE2**, which has no lookahead
   (otelcol-doctor).
3. **OTTL is strictly typed.** Setting an attribute to a boolean and then matching it with `IsMatch(..., "true")`
   fails silently. Use the `Int()`, `String()` and `Bool()` converters explicitly (o11y-dev).
4. **Use current semantic-convention keys**: `http.response.status_code`, not `http.status_code`. A deprecated key
   leaves gaps where a backend normalizes to the current names (o11y-dev). The key renames are version-bound;
   check the convention version the SDKs emit.
5. **Validate every OTTL change with the validator** (§1.4), and remember that the type mismatches above fail
   silently, so a config that validates has not shown that its statements match anything (o11y-dev).
