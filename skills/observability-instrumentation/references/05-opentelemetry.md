# § 5 — OpenTelemetry

> Section 5 of `skills/observability-instrumentation`. Read it when the application is instrumented with
> OpenTelemetry (traces, metrics or logs through its SDK). It does not replace §1 to §4: the questions come
> first, then the names and attributes below make the answers findable.

1. **Give every process an identity, set explicitly.** The specification requires the SDK to provide
   `service.name`; set it with the `OTEL_SERVICE_NAME` variable or the resource attributes, never leave the
   default. When both are present, `OTEL_SERVICE_NAME` wins. Set the namespace, the version (changing per release)
   and an instance id alongside it, so a record can be attributed to a service, a release and a replica. The
   `service.namespace`, `service.version` and `service.instance.id` attributes are the usual companions; treating the
   four as one unit is the practice of the instrumentation guide read, not a specification requirement.
2. **A span name is low cardinality.** For HTTP the convention is `{method} {target}` when a low-cardinality
   target exists (the route template, never the raw path), and `{method}` alone when it does not. A name with an
   id or a query string in it turns every request into its own series and defeats grouping.
3. **Span status follows the convention, not the HTTP code alone.** On a server span a 4xx leaves the status unset;
   on a client span it should be Error; a 5xx, or any outcome the client could not interpret, should be Error.
   Set the `error.type` attribute when a request fails before a status code exists. A 404 can be a normal answer:
   do not paint it red by reflex.
4. **Reuse a semantic-convention name before inventing one.** If none fits, prefix your own with a reverse domain
   name for something shared across companies, or with a reasonably unique application name for internal use, and
   never use an existing OpenTelemetry namespace as the prefix of your own attribute (a later release may take the
   name). Names are lowercase printable Latin characters, and metric names are not pluralised.
5. **Keep a small attribute registry of your own.** One file lists each custom attribute, its type, its unit and
   who sets it; a reviewer rejects a new name that is not in it. (Reasoning of ours; it applies §3's
   cardinality discipline to traces.)
6. **Choose sampling for the question it must still answer.** Head sampling decides at the start of a trace:
   simple, cheap, usable anywhere in the pipeline, but it cannot keep "all traces that contain an error", because
   the outcome is not known yet. Keeping errors and slow traces needs tail sampling, which sees most of the spans
   of a trace and costs memory and a stateful component. The SDK samplers are `always_on`, `always_off`,
   `traceidratio` and their `parentbased_` forms, selected with `OTEL_TRACES_SAMPLER` and its argument variable;
   in a service called by others, use the parent-based form so a trace is not cut in the middle.
7. **Verify once with real traffic.** After wiring, look at one trace end to end: the service name is the one you
   chose, the span names group, the status of a failing call is Error, the trace id appears in the logs of the
   same request (§2). This is §1.10 applied to traces.

**Sources:** the OpenTelemetry documentation and semantic conventions (resource, general naming, HTTP spans,
sampling concepts, SDK environment-variable configuration; CC-BY-4.0, read 2026-10-02) and the
`otel-instrumentation` skill of the public `dash0hq/agent-skills` repository (Apache-2.0, read 2026-10-02),
used for the structure of points 1 and 7. Points 1 (the four-attribute rule), 5 and 7 are practice or reasoning
of ours, not specification text. Version-bound: semantic conventions evolve; the pages read were current on
2026-10-02, so re-read the convention page of the version your SDK implements.
