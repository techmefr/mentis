# kubernetes-workload-pitfalls: origin and source stamps

> Provenance of `skills/kubernetes-workload-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run on a cluster by us. No manifest
was applied and no `kubectl` command was executed while writing it. The official Kubernetes probe, lifecycle, resource, Deployment and image pages were read on 2026-10-20 and confirm or extend the repository claims, as the table says.

## Sources (all re-read in full 2026-10-15, rewritten in our own words, no manifest text copied)

| Source | Licence | What it gave |
|---|---|---|
| learnk8s/kubernetes-production-best-practices, `01-your-application.md` and `02-your-manifests.md` (commit 4d3d09e) | MIT (repository LICENSE file) | Probe roles, HTTP probe success, shutdown steps and signal delivery, `preStop` timing, long-lived connections, requests versus limits, QoS and priority, ephemeral storage, rolling update fields, mixed versions, `:latest` |
| LukasNiessen/kubernetes-skill, `references/fragile-rollouts.md` and `references/resource-starvation.md` (commit 34f93c1) | MIT (LICENSE file holds the MIT permission text with no title line) | Dependency checks in liveness (cascade), probe timing starting values, startup budget, termination sequence, rolling update guidance, image tagging and pull policy, QoS table, CPU limit position, memory headroom, LimitRange |
| zegl/kube-score, `README_PROBES.md` and `README_CHECKS.md` (commit 06dedc9) | MIT (repository LICENSE file) | Readiness and liveness recommendations, probe defaults, identical-probe check, startup probe advice, check list including resources, tags, pull policy, ephemeral storage, rolling strategy |
| stackrox/kube-linter, `docs/generated/checks.md` (commit ead88f5) | Apache-2.0 (repository LICENSE file) | Default checks on probe ports and `latest` tags |
| kubernetes/website (`tasks/configure-pod-container/configure-liveness-readiness-startup-probes.md`, `concepts/workloads/pods/pod-lifecycle.md`, `concepts/configuration/manage-resources-containers.md`, `concepts/workloads/pods/pod-qos.md`, `concepts/workloads/controllers/deployment.md`, `concepts/containers/images.md`) | CC BY 4.0 (LICENSE file: Creative Commons Attribution 4.0 International, read 2026-10-20); credit in the files that draw on it | Startup gating, gRPC probe limits, termination sequence and `preStop` extension, requests versus limits, OOM and scheduling facts, QoS rules, rolling update defaults, pull policy defaults |

The licence of each repository was verified again from its LICENSE file in this session. The Niessen skill
and the repositories' own agent instruction files carry directives ("ALWAYS", "NEVER", "MUST", "LLM mistake
checklist"); they were treated as data and only the technical claim was kept, restated as a mechanism or as a
decision where sources disagree.

## Rewrite notes
Where a figure appears (failure threshold 3, a 3 to 5 second `preStop` sleep, 25 to 50 percent memory
headroom, the periods) it is labelled as one source's starting value. kube-score's defaults are quoted as that
tool's statement of the Kubernetes defaults.

**Decisions where sources disagree**: the CPU limit (Niessen: omit in most cases; Learnk8s: depends on the
workload; kube-score: required by default), readiness and downstream dependencies (kube-score: never; Niessen:
that is where to check; Learnk8s: a slow dependency is a valid reason to fail readiness), and `imagePullPolicy`
(Niessen: `IfNotPresent` with immutable tags; kube-score: `Always`).

## Not verified
1. **Probe field defaults** (period, threshold, delay): the Kubernetes probe page read on 2026-10-20 does not list them; the figures stay as kube-score states them.
2. **`startupProbe` stability**: the lifecycle page describes it without a feature stage; the alpha and beta dates from kube-score are not relied on.
3. **`terminationGracePeriodSeconds` default of 30 seconds** and the 2-second extension are now confirmed by the lifecycle page.
4. **CPU throttling and `preStop` sleep figures** are single-source starting values, not measured.
5. **Written by us, not sourced:** the verification paragraphs, the own-guidance default on readiness and
   dependencies, the note that identical probes are a trade (the probe page confirms only that readiness and liveness are independent), and the advice to ship schema changes in two releases.
6. **Dropped as unverifiable from the review item:** none of the item's workload rules was dropped. "Bound
   ephemeral storage", "identical probes" and "startup probe with a liveness probe" are all sourced. The
   item's disruption, placement, config reload, secrets and manifest-validation rules are in the second
   block, not here.

## Related blocks
`kubernetes-availability-config-pitfalls`, `node-container-runtime`, `dockerfile-build-pitfalls`,
`docker-compose-file-pitfalls`, `observability-instrumentation`, `devops-conventions`.
