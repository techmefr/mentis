---
name: kubernetes-access-and-exposure-pitfalls
description: "Use when Kubernetes access control, secrets or exposure are designed or reviewed: RBAC bindings (namespace Role versus ClusterRoleBinding, wildcards, cluster-admin, system:masters, the verbs and resources that are privilege-escalation paths, list and watch on Secrets, service account token auto-mount, system:unauthenticated), who can read a Secret (access to Secrets, creating a pod that mounts one, per-container mounts, base64 manifests in git), the Pod Security Standards Baseline and Restricted field-level rules for a pod spec, NetworkPolicy starting from deny-all, and the manifest lint checks that map to them."
---

# kubernetes-access-and-exposure-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for who can reach what in a cluster. The four sections share one
premise: **a permission is rarely only the permission it names, because creating a pod, listing Secrets or
patching a namespace each reaches further than the verb suggests, and a pod spec that Kubernetes accepts is
not a pod spec that is contained**. Probes, resources and rollout are in `kubernetes-workload-pitfalls`;
placement, configuration reload, secrets as files and manifest validation are in
`kubernetes-availability-config-pitfalls`; the Docker socket on a Compose host is in
`docker-compose-file-pitfalls` §3.1.

## When
- Writing or reviewing a Role, ClusterRole, binding or service account, or granting a human or a pipeline
  access to a cluster.
- A workload needs to read Secrets, call the Kubernetes API or run with extra privileges.
- Writing the `securityContext` and volumes of a pod, or choosing a Pod Security Standard for a namespace.
- Deciding how pods in a namespace may talk to each other.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | RBAC: least privilege, tokens and service accounts, privilege-escalation paths, review | a Role, binding or service account is written or reviewed | [`01-rbac.md`](./references/01-rbac.md) |
| 2 | Secrets: who can read them, pods that mount them, manifests in git, etcd | a workload or person is given access to Secrets | [`02-secrets-access.md`](./references/02-secrets-access.md) |
| 3 | Pod Security Standards: Baseline and Restricted field-level rules, the OS field | a pod spec or a namespace policy is written | [`03-pod-security-standards.md`](./references/03-pod-security-standards.md) |
| 4 | NetworkPolicy from deny-all, and the lint checks that map to §1 to §3 | pods in a namespace should not all reach each other | [`04-network-and-lint.md`](./references/04-network-and-lint.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: `kubectl auth can-i` was run as the subject for the verbs of §1
and §2 and returned what was intended, the pod spec was applied to a test namespace that enforces the
profile of §3 and was admitted, a pod without the matching labels in the policy of §4 failed to reach the
protected pod, and a manifest linter ran on the final tree (§4.3). A manifest that was only read is not
verified.

## Guardrails
- Never bind a role cluster-wide when a namespace binding does it (§1.1).
- Never grant `list` or `watch` on Secrets without treating it as read access to their contents (§1.3, §2.1).
- Never treat creating pods as a harmless permission (§1.3, §2.2).
- Never leave the service account token mounted in a pod that does not call the API (§1.2).
- Never ship a pod spec that does not meet the Restricted fields of §3.2 without recording which field and
  why.
- Never start network isolation by writing allow rules before a deny-all (§4.1).
- This block states Kubernetes behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md); the Pod Security Standards carry version numbers and are
  revised, so check the page for the cluster version in use. Nothing was run while writing it.

## Origin
Rewritten with attribution from the Kubernetes documentation pages on RBAC good practices, Secrets good
practices and the Pod Security Standards (kubernetes/website, CC BY 4.0; changes: rephrased, condensed and
reorganised), the network policy recipe on denying all traffic (ahmetb, Apache-2.0) and the kube-linter check
list (Apache-2.0), read 2026-10-16. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
