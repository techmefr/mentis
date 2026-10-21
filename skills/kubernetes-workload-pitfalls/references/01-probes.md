# kubernetes-workload-pitfalls §1 — Probes

A probe tells the kubelet what to check and what to do when the check fails. The three probes answer three
different questions, and most probe outages come from asking the wrong one the wrong thing.

## 1.1 What each probe answers
1. **Readiness: "should this container get traffic right now?"** A failing readiness probe does not restart
   anything; it removes the pod from the Service endpoints. Without one, traffic can reach a pod before the
   server has started, and keep reaching it after it has stopped (kube-score's probe notes).
2. **Liveness: "is this container stuck and in need of a restart?"** It is for a deadlock, a process that
   runs and does no useful work. Only the container whose probe fails is restarted; the other containers
   of the pod are untouched.
3. **Startup: "has the application finished initialising?"** Until it succeeds once, the liveness and
   readiness probes do not run. It exists so that a slow start does not get the container killed by a
   liveness probe that began too early. The Kubernetes documentation confirms the gating, and sizes the window as
   `failureThreshold` times `periodSeconds`; a startup probe that never succeeds gets the container killed and
   handled by the restart policy (Kubernetes documentation).

## 1.2 Liveness rules
1. **Liveness never checks a database, a cache or another service.** When the dependency goes down, the
   probe fails on every pod at once, the kubelet restarts all of them, they come back to a dependency that
   is still down, and the whole service crash-loops while the dependency recovers. A liveness check that only
   asks whether the process responds would have left the pods up (Kubernetes agent skill by Niessen; kube-score).
2. **Liveness and readiness must not be the same check** (kube-score names it as its own check,
   `pod-probes-identical`) and says liveness should never be the same as readiness. Own reasoning, not the
   source's: they decide different things, so one endpoint for both either restarts a pod for what should
   only take it out of traffic, or leaves a stuck process in traffic.
3. **A liveness probe that is too strict makes things worse**: it restarts containers that would have
   recovered on their own (Learnk8s).
4. **If you cannot say why a liveness probe is needed, leave it out** (kube-score).
5. **Do not fire on one failure.** The Niessen skill suggests `failureThreshold: 3` and a `timeoutSeconds`
   below `periodSeconds`, with a period of 10 to 30 seconds. These are one source's starting values, not
   measurements for your service.

## 1.3 Readiness rules
1. **Readiness answers only "can I serve a request now".** Typical reasons to fail it are warm-up, overload
   or a pod that has begun shutting down (§2).
2. **Readiness and downstream dependencies: the sources disagree, so this is a decision.** kube-score says not
   to depend on another service or a database in the probe, because when the dependency hiccups, pulling
   every pod out of the load balancer makes the downtime worse. The Niessen skill says the readiness probe
   is where to check dependencies, so a pod with no database stops receiving requests without being
   killed. Learnk8s lists a slow dependency among the reasons for a readiness failure. Own guidance: default
   to not checking, and add a dependency to readiness only when the pod truly cannot answer anything useful
   without it and you have decided what should happen when every replica fails it at once.
3. **Know your timing.** The Kubernetes probe concept page (read 2026-10-21) gives the defaults: an initial delay of 0 seconds, a period of 10 seconds, a timeout of 1 second, a success threshold of 1 (it must be 1 for liveness and startup probes) and a failure threshold of 3; kube-score states the same figures. With defaults clients keep sending traffic for about
   30 seconds, plus network propagation, after the application stops answering. Set them to your needs.
4. **A probe on a port the container does not expose is a bug**: kube-linter has default checks for the
   liveness, readiness and startup probes pointing at ports that are not declared.

## 1.4 Startup probe rules
1. **Configure a startup probe whenever a liveness probe exists** (kube-score).
2. **Size it to the worst start.** `failureThreshold` times `periodSeconds` must cover the maximum startup
   time; the Niessen skill's example is 30 failures at a 5-second period for a 150-second budget.
3. **With a startup probe the liveness probe needs no `initialDelaySeconds`**; the startup probe lets you
   shorten it and catch a deadlock earlier (kube-score; Niessen skill).
4. **An application that takes longer than the liveness delay and period allow will be killed in a restart
   loop** without one (Niessen skill).

## 1.5 What a probe endpoint returns
1. **For HTTP probes only the status code counts.** 200 up to but not including 400 is success; the body is
   ignored, so keep the endpoint small and focused on the status (Learnk8s). The kubelet stops reading the
   body after 10 KiB.
2. **Other mechanisms exist**: a TCP listener check, a command run in the container, or the gRPC health
   protocol for gRPC services (Learnk8s).
3. **gRPC probes have their own limits.** The app must implement the gRPC health protocol; the probe uses
   plaintext unless TLS mode is set (behind a feature gate), named ports are not supported, and every error
   counts as failure (Kubernetes documentation).
4. **Readiness and liveness do not depend on each other**: readiness runs for the whole container life, so to keep
   it from failing during start-up use a startup probe or `initialDelaySeconds` (Kubernetes documentation).
5. **Waiting for a dependency before start belongs in an init container**, not in a liveness probe (Niessen skill).

## 1.6 Verify
Break the dependency on purpose (stop the database in a test environment) and watch `kubectl get pods`:
no pod may restart because of it. Check the effect of a failing readiness probe with
`kubectl get endpoints <service> -w`. List probe failures with
`kubectl get events --field-selector reason=Unhealthy`.

*Attribution.* Points marked "(Kubernetes documentation)" are based on "Configure Liveness, Readiness and Startup Probes" and "Pod Lifecycle", © The Kubernetes Authors, from kubernetes/website, licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); rephrased and condensed, no endorsement by the Kubernetes Authors is implied.
