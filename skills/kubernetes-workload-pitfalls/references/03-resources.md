# kubernetes-workload-pitfalls §3 — Resources

Requests and limits decide where a pod lands, what happens when the node is short, and whether the kernel
kills the container. Leaving them out does not fail the deploy; it moves the failure to a busy day.

## 3.1 Requests and limits do different jobs
1. **Requests are a scheduling input.** The scheduler uses them to choose a node with room before the pod
   starts. It does not use the real future usage and it does not enforce the request afterwards (Learnk8s).
2. **Limits are enforced at runtime** by the kubelet, the container runtime and the kernel. Over its CPU limit a
   container is slowed; over its memory limit it can be killed (Learnk8s).
3. **Every container gets CPU and memory requests and a memory limit.** Memory is incompressible: unlike CPU,
   exceeding it kills the container (Learnk8s; Niessen skill).
4. **A limit without a request**: Kubernetes may use the limit as the request unless another default applies
   (Learnk8s). Say both.
5. **Base requests on measured usage**, not on round numbers (`cpu: 1`, `memory: 1Gi`) copied from an example
   (Niessen skill).
6. **Leave headroom in the memory limit.** The Niessen skill suggests 25 to 50 percent above the observed p99.
   One source's figure; set yours from your own measurement. Limits set too close to requests leave no room
   for legitimate bursts.

## 3.2 The CPU limit is a decision
The sources disagree. The Niessen skill advises setting no CPU limit in most cases, because CFS throttling
causes latency spikes that are hard to see, and lists exceptions: a multi-tenant cluster enforcing fairness,
batch work that must not starve interactive pods, and a need for Guaranteed QoS. Learnk8s says every container
should have CPU requests and a memory limit, and that setting a CPU limit depends on the workload and the
cluster. kube-score requires a CPU limit by default and has a flag to drop that requirement.
1. **Decide per workload and write the reason down** (in the review or the commit message), instead of
   inheriting a default copied from a template.
2. **Do not carry "never set a CPU limit" or "always set one" as a rule.**
3. **Whichever you pick, measure throttling** before and after (the CPU throttling counters of your
   metrics stack; the sources do not name one).

## 3.3 Quality of service and eviction
1. **Three classes**, assigned from the requests and limits: Guaranteed (every container has CPU and memory
   requests and limits and each request equals its limit), BestEffort (none set anywhere), Burstable
   (everything else). They influence which pods the kubelet evicts first when a node runs short; BestEffort
   goes first (Learnk8s; Niessen skill).
2. **BestEffort is not acceptable in production** (Niessen skill).
3. **QoS is not priority.** A PriorityClass is a separate signal for scheduling and eviction; the scheduler can
   preempt lower-priority pods and the kubelet also considers priority during eviction (Learnk8s).
4. **A LimitRange gives a namespace defaults and ceilings**, so a pod that slips through without resources
   gets something (Niessen skill).

## 3.4 Ephemeral storage
1. **Local ephemeral storage counts**: the container's writable layer, its logs and disk-backed `emptyDir`
   volumes. If it grows too much the kubelet can evict the pod when the node runs low (Learnk8s).
2. **Set `ephemeral-storage` requests and limits** for containers that write meaningful data: temporary
   files, caches, upload buffers, unpacked archives, large logs:

```yaml
resources:
  requests:
    ephemeral-storage: 1Gi
  limits:
    ephemeral-storage: 2Gi
```

3. **Writable paths on a read-only root**: mount an `emptyDir` where the application needs to write and set a
   `sizeLimit` when you know the bound. This pairs with `readOnlyRootFilesystem: true`; the image stays
   read-only and the writable paths are few and bounded (Learnk8s).
4. **kube-score checks it by default**: containers need ephemeral-storage requests and limits.

## 3.5 Verify
`kubectl get pod <name> -o jsonpath='{.status.qosClass}'` for the class; `kubectl top pods --containers`
against the requests; look for `OOMKilled` in `lastState.terminated.reason`. A load test that drives the
service to its expected peak is the only check that the figures are right.
