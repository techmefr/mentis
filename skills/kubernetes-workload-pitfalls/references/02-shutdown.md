# kubernetes-workload-pitfalls §2 — Shutdown

Kubernetes may stop a pod, start a replacement elsewhere, or change the replica count at any time. The
failure this section prevents is a deploy or a node drain that drops in-flight requests because the pod was
stopped while traffic still arrived.

## 2.1 What happens when a pod is terminated
1. **Several things start together**: the pod is marked terminating and removed from the Service endpoints
   (asynchronously), the `preStop` hook runs if there is one, `SIGTERM` is sent to PID 1 of the container, and
   the kubelet waits up to `terminationGracePeriodSeconds` (default 30 seconds) before sending `SIGKILL`
   (Niessen skill).
2. **The endpoint removal is the slow one**, so the pod can still receive requests for some seconds after
   `SIGTERM`. Kubernetes also tracks terminating backends through EndpointSlice conditions, and for some
   traffic (for example Services with `externalTrafficPolicy: Local`) it can deliberately keep sending
   traffic to stopping pods so connections close smoothly (Learnk8s).
3. **The `preStop` hook runs before the TERM signal and its time counts against the same grace period**
   (Learnk8s).

## 2.2 What the application does
1. **Handle `SIGTERM`.** Stop accepting new requests, keep serving in-flight ones for a short drain period,
   close idle and keep-alive connections cleanly, and exit before the grace period ends (Learnk8s).
2. **Wait for the endpoint removal before closing.** kube-score's advice: start failing the readiness probe
   on `SIGTERM` and wait until the Service is unregistered from the load balancers before shutting down; the
   alternative is a `preStop` hook with a sleep. The Niessen skill's checklist suggests a sleep of 3 to 5
   seconds; that figure is one source's starting value, so measure the propagation in your cluster.
3. **Size `terminationGracePeriodSeconds`** to the time you need to drain, plus the `preStop` time. The
   default 30 seconds may not be enough (Niessen skill).
4. **A `preStop` hook does not replace signal handling** in the application (Learnk8s).
5. **Long-lived connections need care**: gRPC, WebSockets, HTTP keep-alive and connection pools stay on the
   same pod until closed, so more replicas do not spread existing work. Clients must be able to reconnect,
   and servers must drain on shutdown (Learnk8s).

## 2.3 The signal must arrive
1. **Kubernetes sends the stop signal to PID 1**, so the entrypoint has to start the application so that
   signals are passed on. In a Dockerfile use the exec form (`CMD ["node", "server.js"]`, not `CMD node
   server.js`). A wrapper script must replace itself with the application using `exec` (Learnk8s).
2. **The image side of this** (init process, package manager scripts) is in `node-container-runtime` §1.3 and
   `dockerfile-build-pitfalls` §3.1.

## 2.4 Verify
Delete a pod under load (`kubectl delete pod`) while a client loops requests, and count failures. Roll out a
new version under the same load. The shutdown path was not exercised if the test ran against an idle pod.
