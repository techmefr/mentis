# kubernetes-access-and-exposure-pitfalls §4 — Network isolation and the lint checks

Pod-to-pod traffic is open unless a NetworkPolicy selects the pod. This section is the starting move for
isolation, and the list of manifest checks that catch the rules of §1 to §3 before they reach a cluster.

## 4.1 Start from deny-all
1. **Isolate an application by selecting its pods with a policy that allows nothing in.** The recipe from
   the kubernetes-network-policy-recipes repository drops all traffic to the pods selected by a pod
   selector, and is the first step before allowing traffic selectively: you blacklist first, then
   whitelist.
2. **The shape of the policy**: a NetworkPolicy whose `podSelector` matches the application's labels and
   whose `ingress` list is empty:

```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: web-deny-all
spec:
  podSelector:
    matchLabels:
      app: web
  ingress: []
```

3. **A policy with no ingress rules allows no ingress traffic.** The recipe says the manifest is missing the
   `ingress` field and so allows nothing; the manifest it shows sets an empty list. The concept page
   settles why both work: when `policyTypes` is omitted, `Ingress` is always set, and `Egress` only if the
   policy has egress rules. So a selecting policy without ingress rules denies all ingress; an egress
   deny-all must name `policyTypes: [Egress]`. Still test it on your cluster.
4. **Use cases the recipe names**: starting to allow-list traffic, preventing every other pod from reaching
   a pod you run, and temporarily isolating traffic to a service.
5. **Test it from a temporary pod**: before the policy a request from another pod succeeds; after it the
   request times out (the recipe's test).

## 4.2 Policies add up, and labels carry meaning
1. **Policies are additive.** If at least one NetworkPolicy has a rule that allows the traffic, the traffic
   reaches the pod regardless of the other policies that block it. Another policy that gives some pods
   access, directly or indirectly, makes the deny-all obsolete for those flows (the recipe's remarks).
2. **The labels a policy matches are an access control.** Whoever can `patch` Namespace objects can change
   their labels, and in clusters where NetworkPolicy is used this can indirectly allow access that was not
   intended (`kubernetes-access-and-exposure-pitfalls` §1.3 point 11, from the RBAC page).
3. **A policy is enforced only if the network plugin implements it.** The concept page says a NetworkPolicy
   created without such a controller has no effect, silently; check that a deny-all really blocks a test
   request before relying on it.
4. **A namespace with no policy allows everything**, and `podSelector: {}` selects every pod in the
   namespace. Deny-all egress also blocks DNS: add a rule to the cluster DNS service.
5. **A connection needs both ends to allow it**: the source pod's egress policy and the destination pod's
   ingress policy. Replies to an allowed connection pass without a rule.
6. **`namespaceSelector` and `podSelector` in one `from` entry are ANDed; as two entries they are ORed.**
   A stray dash in the YAML turns "pods labelled x in namespaces labelled y" into "every pod of those
   namespaces plus every pod labelled x in this one".
7. **`ipBlock` is for addresses outside the cluster.** Pod IPs are ephemeral, and a load balancer or NAT may
   rewrite the source address the policy sees; traffic to and from the pod's own node is always allowed.

## 4.3 Lint checks that map to these rules
kube-linter (commit `ead88f5`, `docs/generated/checks.md`) carries checks for most of §1 to §3. The
"enabled by default" status is as that file states it for that commit; the checks that are off by default
need to be switched on.
1. **Docker socket**: `docker-sock` (default on) flags a mounted `docker.sock`, which its remediation says
   would effectively allow full control of the host. A mount of one of the sensitive host directories
   (`/`, `/boot`, `/dev`, `/etc`, `/lib`, `/proc`, `/sys`, `/usr`) is `sensitive-host-mounts` (default on);
   a writable host path is `writable-host-mount` (off).
2. **Host namespaces**: `host-network`, `host-pid` and `host-ipc` (all default on).
3. **Privilege**: `privileged-container` and `privilege-escalation-container` (default on; the second asks
   for `allowPrivilegeEscalation=false`, `privileged=false` and no `CAP_SYS_ADMIN`).
4. **Identity and filesystem**: `run-as-non-root` (default on), `no-read-only-root-fs` (default on) and
   `drop-net-raw-capability` (default on; it explains that `NET_RAW` lets an application craft raw packets).
5. **Service account**: `default-service-account` (off) flags pods that use the default service account.
6. **Exposure**: `non-isolated-pod` (off) flags pods not selected by any NetworkPolicy, `exposed-services`
   (off) flags NodePort and LoadBalancer services, and `ssh-port` (default on) flags port 22.
7. **RBAC**: `cluster-admin-role-binding`, `wildcard-in-rules`, `access-to-secrets` and
   `access-to-create-pods` (all off by default); the descriptions cite CIS Benchmark items 5.1.1 to 5.1.4.
8. **Secrets in the environment**: `env-var-secret` (default on) and `read-secret-from-env-var` (off); the
   topic is in `kubernetes-availability-config-pitfalls` §2.3.
9. **Unsafe settings of §3.3**: `unsafe-proc-mount` (off) and `unsafe-sysctls` (default on).
10. **A linter is not the policy.** Own guidance: these checks read the manifest in CI; the standards of §3
    are enforced in the cluster by admission. Use both, because a manifest that never goes through CI still
    reaches the cluster.

## 4.4 Verify
Apply the deny-all policy in a test namespace and confirm a request from a pod outside the allowed set times
out. Run the linter with the checks of §4.3 switched on over the whole manifest tree and read every finding
for the rules of §1 to §3.
