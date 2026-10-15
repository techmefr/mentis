---
name: kubernetes-workload-pitfalls
description: "Use when a Kubernetes Deployment, StatefulSet or pod template is written or reviewed for runtime behaviour: liveness, readiness and startup probes (what each may check, why liveness must not depend on a database, readiness and dependencies as a decision), graceful shutdown (endpoint removal is asynchronous, preStop, terminationGracePeriodSeconds, signals reaching PID 1), resource requests and limits (memory limit, the CPU limit as a decision, QoS and eviction, ephemeral storage) and rolling updates (maxUnavailable and maxSurge, minReadySeconds, mixed versions, latest tag, imagePullPolicy)."
---

# kubernetes-workload-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the pod template. The four sections share one premise: **a pod
that Kubernetes can start is not a pod Kubernetes can safely stop, restart, replace or squeeze, and the
manifest is where you tell it how**. Placement, disruption budgets, configuration reload, secrets and manifest
validation are in `kubernetes-availability-config-pitfalls`; RBAC and network exposure are in
`kubernetes-access-and-exposure-pitfalls`, and chart authoring in `helm-chart-pitfalls`. The image side of signals is in `node-container-runtime` §1.3 and `dockerfile-build-pitfalls`.

## When
- Writing or reviewing a Deployment, StatefulSet or the pod spec of a Job or CronJob.
- A rollout drops requests or 502s, pods restart together when a dependency is down, or a pod is killed
  before it finishes a request.
- A pod is OOM-killed, evicted, stays Pending, or its latency spikes under a CPU limit.
- Choosing probes, `terminationGracePeriodSeconds`, requests and limits, or the rolling update fields.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Probes: what each answers, liveness and readiness rules, startup probe, probe endpoints | a probe is added or changed, or pods restart in a group | [`01-probes.md`](./references/01-probes.md) |
| 2 | Shutdown: what runs when a pod stops, SIGTERM, preStop, grace period, long-lived connections | a deploy or drain drops requests | [`02-shutdown.md`](./references/02-shutdown.md) |
| 3 | Resources: requests, limits, the CPU limit decision, QoS, ephemeral storage | a pod is OOM-killed, evicted or throttled, or resources are chosen | [`03-resources.md`](./references/03-resources.md) |
| 4 | Rollout and images: rolling update fields, mixed versions, tags and pull policy | the update strategy or an image reference changes | [`04-rollout-and-images.md`](./references/04-rollout-and-images.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the dependency was stopped in a test environment and no pod
restarted (§1), a pod was deleted and a rollout run under request load and the failures were counted (§2),
the QoS class and OOM history were read from the cluster and a load test reached the expected peak (§3), and
the rollout was watched with `kubectl rollout status` while requests ran (§4). A manifest that was only
linted is not verified.

## Guardrails
- Never let a liveness probe check a database, a cache or another service (§1.2).
- Never use the same check for liveness and readiness (§1.2).
- Never add a liveness probe without a startup probe sized to the worst start (§1.4).
- Never assume the pod stops receiving traffic when `SIGTERM` arrives (§2.1).
- Never leave a container without requests and a memory limit (§3.1).
- Never carry "always" or "never" set a CPU limit as a rule; it is a recorded decision (§3.2).
- Never use `:latest` in a workload (§4.3).
- This block states Kubernetes behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md). The official Kubernetes probe pages were not read, so
  check a field or default against the documentation for the cluster version in use. Nothing was run while
  writing it.

## Origin
Rewritten from the Learnk8s production best-practices chapters (MIT), the Kubernetes agent skill by Niessen
(MIT, two references), kube-score's probe notes and check list (MIT) and the kube-linter check list (Apache-2.0),
read 2026-10-15. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
