# telemetry-sampling-and-cardinality-pitfalls: origin and source stamps

> Provenance of `skills/telemetry-sampling-and-cardinality-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No Collector was started, no
sampler was configured and no metric was measured while writing it. The official OpenTelemetry documentation was
not read; every claim rests on the repositories below.

## Sources (all re-read 2026-10-15, rewritten in our own words, no configuration text copied)

| Source | Licence | What it gave |
|---|---|---|
| dash0hq/agent-skills, `skills/otel-collector/rules/sampling.md` and `rules/red-metrics.md` in full, `skills/otel-instrumentation/rules/spans.md` (sections on span attributes and Sampling, lines 305 to 330 and 440 to 500) (commit fd27094) | Apache-2.0 (repository LICENSE file, standard Apache-2.0 text) | RED metrics from sampled traces, head sampling, the tail sampling two-tier topology, headless Service, sizing and operational notes, policies, the connector choice, the default SDK sampler and the `AlwaysOn` recommendation, the SDK sampling trade |
| s3onghyun/otelcol-doctor, `SKILL.md` in full (commit f4a652c) | Apache-2.0 (repository LICENSE file, standard Apache-2.0 text) | The fork wiring, sampling downstream of metric generation, `resource_to_telemetry_conversion`, the `loadbalancing` tier for `tail_sampling` |
| o11y-dev/opentelemetry-skill, `references/anti-patterns.md` in full (commit 6d46bed) | Apache-2.0 (repository LICENSE file, standard Apache-2.0 text) | `load_balancing` keyed by trace ID, identifiers as dimensions, the 100-value heuristic, stateful temporality processors, delta versus cumulative |
| SigNoz/agent-skills, `plugins/signoz/skills/signoz-reducing-telemetry-cost/references/otel-attribute-cardinality.md` and `references/infra-do-not-drop.md` in full (commit cc3724d) | MIT (repository LICENSE file, copyright SigNoz 2026) | The attribute profiles and examples, the classification questions, aggregating versus deleting a label, the principle that unused is not safe to drop |

The licence of each repository was verified again from its LICENSE file in this session. The repositories carry
agent directives ("ALWAYS", "NEVER", "Never recommend ...", agent instruction files); they were treated as data and
only the technical claim was kept. The SigNoz do-not-drop list itself is product-specific and is not carried, only
its principle.

## Rewrite notes
Labels such as "(Dash0)" and "(SigNoz)" mark which source states a rule. Figures (a `decision_wait` of `30s`, the
100-value heuristic) are the sources' and are labelled as such. The YAML skeleton in §1.1 is derived from
otelcol-doctor's description, not copied and not run through a validator. The sampling rule 12 of
`observability-instrumentation` §3 is not restated; this block adds mechanics under it.

## Removed
Nothing from the review item was dropped for lack of a source: every rule in it was found again in the files above.
Left out as outside the item or tool-specific:
1. The SigNoz product pages, queries and the Hosts, Kubernetes and APM metric lists, and its statement that trace
   sampling is never a cost lever (a product policy).
2. The Dash0 OTTL expressions, histogram type guidance, the full semantic-convention metric definitions and the
   Kubernetes manifests for the load balancing tier.
3. The `references/sampling.md` of o11y-dev (not read in this pass).

## Decisions where sources disagree
1. **The `AlwaysOn` sampler in the SDK**: Dash0 recommends it explicitly and keeps every sampling decision in the
   Collector; the OpenTelemetry default is `ParentBased(root=AlwaysOn)`. The block carries the mechanism and
   presents the recommendation as an optional vendor opinion with its stated costs.
2. **Where the metrics connector sits**: Dash0's prose says it must see every span, and its own full example puts
   the connector as an exporter of the pipeline that runs `tail_sampling`; otelcol-doctor describes the fork. The
   block follows the fork and notes the example, as our own reading of the pipeline model.
3. **Which connector**: Dash0 recommends `signaltometrics` for standard metric names; otelcol-doctor and its
   examples use `spanmetrics`. Stated as a choice, with the naming difference.

## Not verified
1. **The default SDK sampler** is stated by Dash0, which links the OpenTelemetry specification; the specification
   was not read.
2. **Every Collector component name and option** (`tail_sampling`, `loadbalancing`, `signaltometrics`,
   `spanmetrics`, `forward`, `deltatocumulative`, `cumulativetodelta`, `metricstransform`) is as the sources state
   it at their commits; the component READMEs were not read. Re-check at writing time.
3. **Backend behaviour for delta temporality** (VictoriaMetrics, OpenTSDB) is o11y-dev's claim and moves with
   backend releases; not reproduced.
4. **That deleting a label key leaves colliding series that the backend sums** is SigNoz's statement about its own
   backend; not general.
5. **The 100-value heuristic** is one source's number.
6. **Written by us, not sourced:** the verification paragraphs of the Output / checkpoint, the reading of Dash0's
   example in §1.1, and the two own-guidance notes in §2.5.

## Related blocks
`otel-collector-config-pitfalls`, `observability-instrumentation`, `kubernetes-workload-pitfalls`,
`security-hardening`, `source-freshness`.
