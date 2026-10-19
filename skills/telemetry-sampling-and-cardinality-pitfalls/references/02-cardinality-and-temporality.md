# telemetry-sampling-and-cardinality-pitfalls §2 — Cardinality and temporality

A metric's cost is its series count times its samples, and both are set by decisions made far from the bill: a
resource attribute copied onto every series, a label nobody classified, a temporality nobody checked.

## 2.1 Resource attributes on series
1. **With `resource_to_telemetry_conversion` off (the default), resource attributes land only on the `target_info`
   series.** A `sum by (service_name)` then returns nothing, and the fix is a join such as
   `... * on (job, instance) group_left(service_name) target_info` (otelcol-doctor).
2. **With it on, every resource attribute is copied onto every series**, including `k8s.pod.name`, `host.id` and
   `container.id`, which multiplies the series per pod (otelcol-doctor).
3. **Enable it only after dropping the high-cardinality resource attributes; otherwise leave it off** and keep
   `target_info` on for the join. State which you chose and why (otelcol-doctor).
4. **Span-derived metrics take only the low-cardinality attributes of the semantic convention**, plus an explicit
   list of resource attributes. `url.full`, `http.target` and user identifiers produce unbounded series (Dash0).

## 2.2 Classify before keeping an attribute as a label
The profiles are SigNoz's. Every attribute is one of them before it is a metric label; the principle that labels
are bounded is `observability-instrumentation` §3, and this adds the classes and examples.

| Profile | Meaning | Examples in the source | Action |
|---|---|---|---|
| Unbounded | grows without ceiling: every new URL, query or trace adds series for good | `url.full`, `url.query`, `http.target`, `db.query.text`, `exception.stacktrace`, `exception.message`, `process.command_line`, `client.port` | drop, or use the bounded form (`http.route`, `db.operation.name`) |
| Accumulating | grows with churn, not with concurrent load | `k8s.pod.uid`, `k8s.pod.name`, `container.id`, `k8s.replicaset.name` | aggregate away on unrelated custom metrics, after a usage review |
| Bounded | a fixed or near-fixed set | `http.route`, `http.request.method`, status codes, `rpc.method`, `k8s.namespace.name` | keep |
| Deployment-dependent | fine at ten services, dangerous at five hundred | `net.peer.name`, `client.address`, `k8s.node.name`, `service.version`, `service.instance.id` | check the real count |
| Identifier | a unique ID per request or event | `trace.id`, `span.id`, `request.id`, `session.id`, `user.id`, `messaging.message_id` | never a metric label |

1. **To classify an attribute not listed** (SigNoz's questions): can the value be user-supplied or request-scoped?
   it is likely unbounded. Does it change when a pod restarts? accumulating. Is it a timestamp, UUID or hash?
   identifier or unbounded. Is it from a fixed vocabulary set at deploy time? probably bounded. Does the count
   roughly equal the number of instances? deployment-dependent.
2. **When unsure, report the name, the observed cardinality and the value pattern** (for example "looks like
   UUIDs"), and let the owner decide (SigNoz).
3. **A route template is bounded and a raw path is not**; the same split applies to `exception.type` (bounded)
   versus `exception.message` (unbounded) (SigNoz).
4. **Identifier and unbounded data belongs on traces or structured logs**, not on metrics (o11y-dev). A heuristic
   from o11y-dev, "keep metric dimensions below 100 unique values per attribute", is one source's number, not a
   measured limit.
5. **Bounded still multiplies**: the SigNoz profile of `service.instance.id` turns accumulating when it embeds a
   UUID or timestamp, so look at its format.

## 2.3 Cutting cardinality at the Collector
1. **Cost follows samples, so merge series; do not just remove a label.** SigNoz's cost reference says to use the
   `metricstransform` processor's `aggregate_labels`, which merges the series that share the remaining labels and
   cuts the series and sample count.
2. **Deleting a label key with the `transform` processor's `delete_key` does not cut the cost**: the same number of
   samples remains and the series collide; in the backend SigNoz tests, they are summed (SigNoz). The backend
   behaviour is that source's, not general.
3. **If a label is part of the metric's identity, drop the whole metric or stop emitting the label in the SDK**
   (SigNoz).

## 2.4 Temporality
1. **Delta metrics sent to a backend that expects cumulative can be dropped silently or misread**, and the data
   appears to vanish. o11y-dev names VictoriaMetrics and OpenTSDB as examples; backend behaviour moves, so check the
   backend's own contract (o11y-dev).
2. **`deltatocumulative` and `cumulativetodelta` are stateful.** A Collector restart resets the state and produces
   a discontinuous series, and several replicas without sticky routing split the state between them (o11y-dev).
3. **Before enabling a conversion, check four things** (o11y-dev): the temporality the SDK emits, the temporality
   the backend expects, whether a discontinuity on restart is tolerable, and how traffic is routed across replicas.

## 2.5 Unused is not the same as safe to drop
1. **A usage check over dashboards and alerts does not prove a metric is dead.** SigNoz's example is a product page
   that reads metrics through built-in queries, not dashboards: the check reports no usage, and dropping the
   metrics breaks the page without an error. The metric list in that source is product-specific and not carried;
   only the principle is.
2. **Before dropping, ask what else reads the metric.** The source finds that the highest-volume infrastructure
   metrics are the ones a naive drop pass removes first, and they are the ones the built-in view needs (SigNoz).
   Own guidance, not from the source: ask the same question of saved queries and of alert rules held in another
   system.
