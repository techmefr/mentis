# kubernetes-workload-pitfalls §4 — Rollout and images

A Deployment replaces pods gradually. Whether users notice depends on four things you set: the rollout
parameters, whether old and new versions can coexist, whether the pods are really ready, and whether the
image reference means the same thing on every node.

## 4.1 Rolling update parameters
1. **The fields**: `maxUnavailable` (replicas that may be unavailable during the rollout), `maxSurge` (extra
   replicas above the desired count), `minReadySeconds`, `progressDeadlineSeconds` (how long before the rollout
   is marked failed) and `revisionHistoryLimit` (old ReplicaSets kept for rollback). Defaults suit simple
   workloads; production manifests state them (Learnk8s). The Deployment page gives them: `maxUnavailable` and
   `maxSurge` 25 percent (rounded down and up respectively), `progressDeadlineSeconds` 600 (it must exceed
   `minReadySeconds`, default 0) and `revisionHistoryLimit` 10; setting that to 0 erases rollback history.
   A rollout starts only when the pod template changes, never on a scale (Kubernetes documentation).
2. **`maxUnavailable: 0` keeps capacity from dropping and needs `maxSurge` of at least 1**, plus enough spare
   capacity in the cluster for the surge pods. For a critical service the Niessen skill uses `maxSurge: 1`
   with `maxUnavailable: 0`:

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0
    maxSurge: 1
```

3. **A high `maxUnavailable` on few replicas takes most of the service down**: with two replicas, one
   unavailable is half the capacity (Niessen skill).
4. **`minReadySeconds`**: a new pod must be ready, with no container crashing, for this long before the
   Deployment counts it as available. It catches pods that start and then crash. It affects rollout progress and
   the scale-down of old pods; it does not delay traffic once the readiness probe passes (Learnk8s).
5. **These settings rely on readiness probes** to say when a new pod can take traffic; they do not replace
   them (`01-probes.md` §1.3).
6. **kube-score checks** that Deployments targeted by a Service use the RollingUpdate strategy.

## 4.2 Old and new versions run together
1. **With `RollingUpdate` the workload must handle mixed versions** behind one Service. A new pod may write
   data an old pod cannot read, or call an API the old backend does not understand. Every pod can be healthy
   and the rollout still fails (Learnk8s).
2. **`Recreate` avoids mixed versions** by stopping the old pods first, at the cost of downtime unless
   something else serves traffic. Use it with care (Learnk8s).
3. **Make the compatibility a design step**, not a hope: schema and message changes go in two releases.
   That last sentence is own guidance; the Deployment page confirms only that old and new pods coexist during a
   rolling update.

## 4.3 Image references
1. **Never `:latest` in a workload.** It is mutable and nondeterministic, makes it hard to know what runs and
   to go back (Learnk8s; Niessen skill; kube-score and kube-linter both check for it).
2. **Use a version tag, a git SHA tag or a `sha256` digest** (Niessen skill, Learnk8s).
3. **`imagePullPolicy` is a decision, not a rule.** The Niessen skill says `IfNotPresent` with immutable tags and
   `Always` only for mutable ones. kube-score wants `Always`, so that `imagePullSecrets` are checked on every
   start rather than being bypassed by a cached image. Pick one and note the trade-off: `IfNotPresent` is
   faster and relies on immutable tags; `Always` re-validates pull credentials each time.
4. **`:latest` with `IfNotPresent` gives version drift**: cached layers mean some pods run the old image and
   some the new one (Niessen skill).
5. **The default pull policy is fixed when the object is created.** It is `Always` for `:latest` or no tag and
   `IfNotPresent` for any other tag or a digest; changing the tag later does not update it, so switching a
   Deployment from a versioned tag to `:latest` leaves `IfNotPresent` in place. With both a tag and a digest,
   only the digest is used. The documentation says to avoid `:latest` in production
   (Kubernetes documentation).
6. **Image build rules** are in `dockerfile-build-pitfalls` §2.2.

## 4.4 Verify
Run `kubectl rollout status` while a request loop runs, and `kubectl rollout history` to confirm the previous
revision is kept for `kubectl rollout undo`. List every image in the namespace and check each has a tag that is
not `latest`.

*Attribution.* Points marked "(Kubernetes documentation)" are based on "Deployments" and "Images", © The Kubernetes Authors, from kubernetes/website, licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); rephrased and condensed, no endorsement by the Kubernetes Authors is implied.
