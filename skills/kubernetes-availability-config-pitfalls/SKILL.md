---
name: kubernetes-availability-config-pitfalls
description: "Use when Kubernetes manifests are written or reviewed for availability and configuration rather than pod runtime: PodDisruptionBudget values that block a drain, topology spread constraints and anti-affinity (DoNotSchedule leaving pods Pending), replicas under an HPA, ConfigMap and Secret changes that do not restart workloads (env versus mounted files, subPath, immutable objects, a reload controller), secrets in environment variables, selectors and references that match nothing, deprecated apiVersions, and linting manifests in CI."
---

# kubernetes-availability-config-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the parts of a manifest set that sit around the pod. The three
sections share one premise: **replicas, config and references are only as good as the thing that ties them
together, and Kubernetes accepts a manifest whose ties are broken**. What a pod does while running, stopping
and being replaced (probes, shutdown, resources, rollout) is in `kubernetes-workload-pitfalls`. RBAC,
Pod Security fields and network policies are not covered by any block yet; Helm authoring is not either.

## When
- Adding or changing a PodDisruptionBudget, topology spread constraints, anti-affinity, an HPA or a replica count.
- A node drain hangs, replicas share a node, or pods stay Pending after a zone fills up.
- A rotated Secret or edited ConfigMap does not reach the running pods.
- A manifest applies cleanly but does nothing, or a cluster upgrade breaks it.
- Setting up manifest linting in CI.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Disruption budgets, spreading replicas, replica counts and the HPA | a PDB, spread rule, replica count or HPA is written | [`01-disruption-and-placement.md`](./references/01-disruption-and-placement.md) |
| 2 | Config reload, env versus mounted files, secrets in the environment | a ConfigMap or Secret is consumed, rotated or changed | [`02-config-and-secrets.md`](./references/02-config-and-secrets.md) |
| 3 | Selectors and references, deprecated APIs, linting in CI | a manifest does nothing, or before an upgrade or a CI gate | [`03-manifest-correctness.md`](./references/03-manifest-correctness.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the allowed disruptions of every PDB were read and a node drain
was run in a test cluster (§1), a ConfigMap and a Secret were changed in a test namespace and the running pod's
view of each was checked (§2), and the linter failed on a deliberate selector typo in CI (§3). A manifest set
that only passes a linter is not verified.

## Guardrails
- Never set a PDB that allows zero disruptions on a workload that gets upgraded (§1.1).
- Never use `DoNotSchedule` spread without checking what happens when one zone is full (§1.2).
- Never hard-code `replicas` on a Deployment that an HPA targets (§1.3).
- Never assume a ConfigMap or Secret change reaches a running pod; pick a reload strategy (§2.2).
- Never pass a credential as an environment variable when a mounted file will do (§2.3).
- Never rely on apply succeeding as proof that a selector or reference matches (§3.1).
- This block states Kubernetes behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md). The official Kubernetes pages were not read; check an
  option against the documentation for the cluster version in use. Nothing was run while writing it.

## Origin
Rewritten from the Learnk8s production best-practices chapters (MIT), the Kubernetes agent skill by Niessen
(MIT), the kube-score check list (MIT), the kube-linter check list (Apache-2.0) and the Stakater Reloader README
(Apache-2.0), read 2026-10-15. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
