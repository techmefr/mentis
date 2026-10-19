# kubernetes-availability-config-pitfalls §1 — Disruption, placement and replica counts

Replicas protect you only if they do not all disappear together. Two events do that: a voluntary disruption
(a node drain for an upgrade or a scale-down) and a shared failure domain (every replica on one node or in
one zone).

## 1.1 PodDisruptionBudget
1. **A PDB declares how many pods must stay available during a voluntary disruption.** Without one, a drain can
   take too many replicas of the same workload down at once (Learnk8s).
2. **It covers voluntary disruptions only**, such as draining a node. A node crash is involuntary and the PDB
   cannot prevent it. It also does not stop a Deployment or a HorizontalPodAutoscaler from lowering the replica
   count. It is best-effort protection, not an availability guarantee (Learnk8s).
3. **Have one for every Deployment and StatefulSet with more than one replica** (kube-score checks it by
   default; the Niessen skill says required for any workload with several replicas).
4. **Too strict a budget blocks maintenance.** `minAvailable` equal to the replica count, or `maxUnavailable`
   of 0, leaves no room for a drain. kube-linter has default checks for both. Choose a value that keeps enough
   healthy pods while letting disruptions proceed (Learnk8s; kube-linter).
5. **Pick the shape by the workload.** `maxUnavailable` suits most stateless services because it scales with
   the replica count; `minAvailable` suits a known minimum such as a quorum (Niessen skill). Set one of them,
   not both, and make sure the PDB specifies a policy at all (kube-score `poddisruptionbudget-has-policy`).
6. **`unhealthyPodEvictionPolicy`**: kube-linter flags a PDB that does not set it explicitly and recommends
   `AlwaysAllow`. What the field does was not read in a Kubernetes source here; check the documentation for
   your cluster version before copying the value.
7. **HPA and PDB together.** The Niessen skill says the HPA `minReplicas` should be at least the PDB
   `minAvailable`, otherwise a scale-down can break the budget. One source; the reasoning follows from point 2.

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-server-pdb
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app: api-server
```

## 1.2 Spread replicas across failure domains
1. **Do not run all replicas in one node or one zone.** One failure then takes them all (Learnk8s). kube-score
   and kube-linter both check for it: Deployments and StatefulSets with several replicas need a pod
   anti-affinity or topology spread constraint that keeps replicas on different nodes (kube-linter names
   `kubernetes.io/hostname` as the topology key).
2. **`topologySpreadConstraints` with `maxSkew: 1`** asks the scheduler to keep matching pods balanced across
   the chosen `topologyKey`:

```yaml
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: ScheduleAnyway
    labelSelector:
      matchLabels:
        app: my-app
```

3. **`DoNotSchedule` can leave pods Pending.** A strict rule with a zone that has no capacity blocks the pod even
   when other zones could run it. `ScheduleAnyway` places it anyway while still preferring nodes that reduce
   the skew. Autoscaled node pools, taints, node affinity and missing topology labels all change the result
   (Learnk8s).
4. **Check two details every time**: the `topologyKey` label exists consistently on the eligible nodes, and
   the `labelSelector` matches the pod template labels of the workload. Otherwise the scheduler balances
   against the wrong set (Learnk8s).
5. **Test under failure and scale-out**, not only on a healthy cluster (Learnk8s).

## 1.3 Replica counts and autoscaling
1. **A Deployment with an HPA does not hard-code `replicas`.** kube-score checks for a statically configured
   replica count on a Deployment that an HPA targets; the manifest's value would fight the autoscaler.
2. **An HPA must target an object that exists** (kube-score `horizontalpodautoscaler-has-target`; kube-linter
   `dangling-horizontalpodautoscaler`).
3. **Minimum replicas are a policy**: kube-score asks for at least two by default (configurable) for Deployments
   and HPAs, kube-linter has an optional check for three. Neither says which number your service needs.
4. **Utilisation targets of 60 to 80 percent** are the Niessen skill's guidance for the HPA (not 90, no
   headroom; not 30, wasteful). One source's starting value.

## 1.4 Verify
`kubectl get pdb -o wide` and read the allowed disruptions: 0 means a drain will hang. Drain a node in a test
cluster and watch the pods move. `kubectl get pods -o wide` to see replicas spread across nodes and zones, and
check that nothing is Pending with a scheduling message about topology.
