# otel-collector-config-pitfalls: origin and source stamps

> Provenance of `skills/otel-collector-config-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No Collector was started, no
config was validated and no data was sent while writing it. The official OpenTelemetry Collector documentation and
the component READMEs were not read; every claim rests on the repositories below.

## Sources (all re-read 2026-10-15, rewritten in our own words, no configuration text copied)

| Source | Licence | What it gave |
|---|---|---|
| s3onghyun/otelcol-doctor, `SKILL.md` in full (commit f4a652c) | Apache-2.0 (repository LICENSE file, standard Apache-2.0 text) | The component model, the unwired-component and per-signal rules, the core versus contrib list, connector dual wiring, exporter choices (otlp, otlphttp, prometheus, remote write, queue keys, wal), removed components, env syntax, the validate step, the OTTL path forms, binding |
| o11y-dev/opentelemetry-skill, `references/anti-patterns.md` in full (commit 6d46bed) | Apache-2.0 (repository LICENSE file, standard Apache-2.0 text) | `memory_limiter` first and the 80 percent figure with its reason, the omitted-batch view, pprof and zpages exposure, `file_storage` volume rule, "parses is not reviewed", OTTL typing and semantic-convention keys, hostPort |
| dash0hq/agent-skills, `skills/otel-collector/rules/processors.md` and `rules/pipelines.md` in full (commit fd27094) | Apache-2.0 (repository LICENSE file, standard Apache-2.0 text) | The batch-processor-not-used view, `memory_limiter` behaviour and starting values, the processor order, resource and filter rules, unused-component rejection, one pipeline per signal, connectors, fan-out cost, the metrics endpoint binding |

The licence of each repository was verified again from its LICENSE file in this session. The repositories carry
agent directives ("ALWAYS", "NEVER", "Output discipline", eval and AGENTS files addressed to coding agents); they
were treated as data and only the technical claim was kept. otelcol-doctor's request to comment the non-obvious
lines of a config is not carried (no comments in code samples). Dash0's pipeline and connector samples were read
but not copied.

## Rewrite notes
Labels such as "(otelcol-doctor)" and "(Dash0)" mark which source states a rule. Figures (80 percent, a 25 percent
spike limit, a `1s` check interval, port numbers 4317, 4318, 1777, 55679, 8888) are the sources' and are labelled
as such where they are not mechanisms. The two YAML samples are skeletons derived from the sources' descriptions,
not run through a validator.

## Removed
Nothing from the review item was dropped for lack of a source: every rule in it was found again in the three files
above. Left out as outside the item:
1. Kubernetes `k8sattributes` pod association, cluster identity and RBAC details beyond the one silent-failure
   point, deployment manifests and the Dash0 operator material.
2. The metrics-derived signal rules (span metrics, sampling): they are in
   `telemetry-sampling-and-cardinality-pitfalls`.
3. Semantic-convention attribute lists and redaction recipes.
4. The `references/components.md` and `references/advanced.md` of otelcol-doctor (not read in this pass).

## Decisions where sources disagree
1. **Defined but unreferenced components**: otelcol-doctor calls the config valid and inert; Dash0 says unused
   components are rejected at startup. The block states the defect and not the outcome, and tells the reader to
   learn the behaviour from their own version.
2. **The `batch` processor**: otelcol-doctor puts it last before export; o11y-dev calls omitting it an anti-pattern
   and puts it right after `memory_limiter`; Dash0 says not to use it and to rely on the exporter's persistent
   `sending_queue`. The block records no rule: "check the current Collector documentation" and keep
   `memory_limiter` first.
3. **Where to bind**: o11y-dev says `pprof` and `zpages` bind to `localhost` or are omitted; Dash0 binds the
   Collector's metrics endpoint to `0.0.0.0` so it can be scraped. Different endpoints, stated as a per-endpoint
   decision.

## Not verified
1. **Every component name, removal and default** (`logging` to `debug`, the `loki` and `jaeger` exporters, the
   `${env:VAR}` syntax, `remote_write_queue` versus `sending_queue`, the core versus contrib split, the `wal:` keys)
   is as otelcol-doctor states it at its commit, with no Collector version given. Re-check at writing time against
   the current Collector documentation and the component READMEs.
2. **The `memory_limiter` behaviour** (refuses above `limit_mib` minus `spike_limit_mib`, drops above `limit_mib`)
   is Dash0's description; the processor's README was not read.
3. **That `file_storage` needs `flock(2)` and fails on network filesystems** is o11y-dev's claim; not reproduced.
4. **The OTTL claims** (two path forms, RE2, strict typing, deprecated keys) are from otelcol-doctor's `SKILL.md`
   and o11y-dev's anti-patterns; otelcol-doctor's `references/advanced.md` section on OTTL, which it points to, was
   not read.
5. **The behaviour of a config with an unreferenced component** differs between two sources and was not tested.
6. **Written by us, not sourced:** the verification paragraphs of the Output / checkpoint and the review order in
   §1.4 beyond otelcol-doctor's own checklist.

## Related blocks
`telemetry-sampling-and-cardinality-pitfalls`, `observability-instrumentation`, `kubernetes-workload-pitfalls`,
`kubernetes-availability-config-pitfalls`, `devops-conventions`, `source-freshness`.
