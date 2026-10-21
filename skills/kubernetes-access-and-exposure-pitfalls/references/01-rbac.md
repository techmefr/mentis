# kubernetes-access-and-exposure-pitfalls §1 — RBAC

RBAC is meant to give users and workloads only the access their role needs. The Kubernetes RBAC good
practices page (kubernetes.io, CC BY 4.0, see the attribution at the end of this file) lists where that
breaks down. The points below are rephrased and condensed from it.

## 1.1 Least privilege
1. **Assign permissions at the namespace level where possible.** Use a RoleBinding rather than a
   ClusterRoleBinding to give rights only within one namespace.
2. **Avoid wildcard permissions, especially on all resources.** Kubernetes is extensible, so a wildcard
   grants access not only to every object type that exists today but also to every type created later.
3. **Do not use `cluster-admin` accounts except where specifically needed.** The page suggests a low
   privileged account with impersonation rights to avoid accidental modification of cluster resources.
4. **Avoid adding users to the `system:masters` group.** Members bypass all RBAC checks and always have
   superuser access, which removing RoleBindings or ClusterRoleBindings cannot revoke. If an authorization
   webhook is used, their requests are never sent to it.

## 1.2 Tokens and service accounts
1. **Pods should not be given service accounts with powerful permissions**, meaning any of the rights in
   §1.3. Where a workload needs them, apply the next two points.
2. **Limit the number of nodes that run powerful pods.** Run only the DaemonSets that are necessary, with
   least privilege, to limit the blast radius of a container escape.
3. **Keep powerful pods off nodes that run untrusted or publicly exposed pods.** The page suggests taints and
   tolerations, node affinity or pod anti-affinity, and says to pay special attention to less-trusted pods
   that do not meet the Restricted standard (§3.2).
4. **Review the bindings for the `system:unauthenticated` group and remove them where possible**: they give
   access to anyone who can reach the API server on the network. The page advises against changing the
   rights of `system:` accounts in general.
5. **Turn off the default auto-mount of service account tokens** with `automountServiceAccountToken: false`.
   Set on a pod it overrides the service account's setting, so workloads that need a token can still mount it.

## 1.3 Privilege-escalation paths
Each of these grants more than it names; review a grant of any of them as an escalation.
1. **Listing Secrets**: `get` reveals a Secret's contents, and so do `list` and `watch`, because a list
   response (for example `kubectl get secrets -A -o yaml`) includes the contents of all Secrets.
2. **Workload creation**: permission to create pods, or the workload resources that manage pods, implicitly
   grants access to the Secrets, ConfigMaps and PersistentVolumes that can be mounted in a pod. Pods can run
   as any service account in the namespace, so the permission also grants every one of those service
   accounts' API access.
3. **Privileged pods**: a user who can run privileged pods can use that to gain node access and escalate
   further. Where you do not fully trust a principal to create suitably isolated pods, enforce the Baseline
   or Restricted standard (§3).
4. **Boundaries inside a namespace are weak.** Use namespaces to separate resources that need different
   levels of trust or tenancy; keep least privilege as well.
5. **Persistent volume creation**: arbitrary PersistentVolumes include `hostPath` volumes, which give a pod
   the node's filesystem. Allow it only to trusted cluster operators and to the control-plane components
   that provision volumes; constrained users use PersistentVolumeClaims.
6. **The `nodes/proxy` subresource** gives rights to the Kubelet API, which allows command execution on every
   pod on the node and bypasses audit logging and admission control. It can be reached with a websocket
   `GET`, so `get` on `nodes/proxy` is not read-only.
7. **The `escalate` verb** lets a user create roles with more rights than they hold; **the `bind` verb**
   lets a user create bindings to roles with rights they do not have; **the `impersonate` verb** lets a user
   act as other users and so reach their rights.
8. **CSRs and certificate issuing**: `create` on CertificateSigningRequests plus `update` on
   `certificatesigningrequests/approval` for the signer `kubernetes.io/kube-apiserver-client` allows new
   client certificates with arbitrary names, including those of system components.
9. **Token request**: `create` on `serviceaccounts/token` issues tokens for existing service accounts.
10. **Admission webhooks**: control of `validatingwebhookconfigurations` or `mutatingwebhookconfigurations`
    allows reading every admitted object and, for mutating webhooks, changing them.
11. **Namespace modification**: `patch` on a Namespace lets a user change its labels. Where Pod Security
    admission is used that can select a more permissive policy; where NetworkPolicy is used the labels can
    indirectly allow access that was not intended (§4.2).
12. **Object creation can exhaust the cluster.** Users who can create many or large objects can cause a
    denial of service; the page mentions resource quotas on object counts as one mitigation.
13. **You cannot grant what you do not hold, unless given the verbs for it.** Creating or updating a Role
    requires holding all its permissions at that scope or the `escalate` verb on roles or clusterroles;
    creating or updating a binding requires the referenced role's permissions or the `bind` verb on it. Treat
    `escalate` and `bind` as privileged verbs in their own right (the RBAC reference).
14. **Wildcards grow by themselves.** `*` on resources or verbs also covers kinds and verbs added later, for
    example by a new CRD. Name what is needed.
15. **A binding's `roleRef` cannot be edited.** Changing the role means deleting and recreating the binding,
    and a manifest that tries to patch it fails.
16. **Do not set `rules` on an aggregated ClusterRole**: the control plane fills them from matching labels and
    overwrites a manual value. At each API server start-up, default cluster roles get any missing permissions back and default bindings any missing subjects, unless the `rbac.authorization.kubernetes.io/autoupdate` annotation is `"false"`; so a permission you removed from a default role returns after a restart (the page speaks of missing permissions and subjects only, not of removing extra ones you added).

## 1.4 Periodic review
1. **Review RBAC regularly for redundant entries and possible escalations.** The page's reason: an attacker
   who can create a user account with the name of a deleted user inherits that user's rights.

## 1.5 Verify
Run `kubectl auth can-i` as the subject, with `--as` for each verb and resource above, in the namespace and
cluster-wide, and read the answers against the intent. List ClusterRoleBindings and bindings to
`system:unauthenticated` and `system:masters`.

*Attribution.* Points 13 to 16 are based on "Using RBAC Authorization", © The Kubernetes Authors, from
kubernetes/website, licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Also based on "Role Based Access Control Good Practices", © The Kubernetes Authors, from
kubernetes/website, licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Changes:
rephrased, condensed and reorganised; no endorsement by the Kubernetes Authors is implied.
