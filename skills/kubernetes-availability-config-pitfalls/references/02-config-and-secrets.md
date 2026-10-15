# kubernetes-availability-config-pitfalls §2 — Configuration, reload and secrets

Changing a ConfigMap or a Secret does not restart a workload. The failure is a pod that keeps running on the
old value, a rotated credential that never reaches the process, or a secret that leaks through the
environment.

## 2.1 What a running pod sees
1. **Environment variables are read when the container starts.** If the ConfigMap or Secret behind them
   changes, the running container does not see it; the pod must be restarted (Learnk8s).
2. **Mounted files can be updated in a running pod**, with some delay that depends on the kubelet's sync and
   cache. A volume mounted with `subPath` receives no updates (Learnk8s).
3. **Kubernetes updates projected files through symlinks**, so a normal file watcher can miss the change.
   Reload logic that watches files must handle that (Learnk8s, citing a third-party write-up it links).
4. **One object is limited to 1 MiB** when serialised. A ConfigMap or Secret near that size does not belong
   in the API (Learnk8s). A ConfigMap is for non-sensitive settings only.
5. **Use an environment variable for simple scalar values**, and mounted files for a structured file the
   application already reads or when you want it to reload (Learnk8s).

## 2.2 Choose a reload strategy
1. **The application reads config only at startup**: make a change trigger a rollout. Learnk8s names two common
   ways, a versioned ConfigMap name or a changed annotation on the pod template, so the Deployment creates a
   new ReplicaSet.
2. **The application reloads files while running**: mount the config as files and make sure the watcher copes
   with Kubernetes volume updates (§2.1 point 3).
3. **The config must never change**: use an immutable ConfigMap or Secret and create a new object per
   change (Learnk8s).
4. **Or run a controller that does it.** Stakater Reloader watches ConfigMaps and Secrets and triggers a rollout
   of the workloads that reference them when they change. A workload opts in with an annotation such as
   `reloader.stakater.com/auto: "true"`. Its default strategy adds an environment variable to the
   containers; the alternative writes an annotation on the pod template, which its README recommends for
   GitOps tools so they do not see drift. The README says the project's `master` branch is feature-frozen and
   active development is on a `v2` branch, so check which line you install.
5. **A GitOps tool that owns the Deployment can revert** what such a controller writes; choose the strategy with
   that in mind (this follows from the README's own note on drift).
6. **Several resources changing together** can cause repeated restarts; the Reloader README describes a
   pause-period annotation on Deployments for that case.

## 2.3 Secrets
1. **Prefer mounted files to environment variables for credentials.** Environment variables can leak: debug
   output, process listings and crash dumps (Learnk8s). kube-linter's check `read-secret-from-env-var` cites a
   benchmark item that says the same, and its default check `env-var-secret` flags raw secret values in
   environment variables, suggesting a mounted file or a `secretKeyRef`.
2. **Mounted Secret files can be updated in a running pod**; environment variables do not update after start
   (Learnk8s).
3. **A rotated secret reaches the process only if something reloads it**: the file watcher of §2.1, or a
   restart from §2.2. Rotating the Secret object alone proves nothing.
4. **Duplicate environment variable names** in one container are a bug the linters check for by default
   (kube-score; kube-linter).

## 2.4 Verify
Change the ConfigMap or Secret in a test namespace and check what the running pod reports: the environment
variable stays old, a mounted file changes after a delay, a `subPath` file never does. Confirm the rollout
that your strategy promises actually happens.
