# kubernetes-availability-config-pitfalls §3 — Manifest correctness before the cluster

A manifest can be syntactically valid YAML and still point at nothing, target the wrong pods, or use an API the
next cluster upgrade removes. These are cheap to catch before apply.

## 3.1 Selectors and references that match nothing
1. **A Deployment's selector must match its pod template labels.** kube-score and kube-linter both check it
   (`mismatching-selector`); the same applies to a StatefulSet in kube-score.
2. **A Service must select a pod, an Ingress must target a Service, an HPA must target an existing object.**
   kube-score and kube-linter check each (`service-targets-pod`, `ingress-targets-service`,
   `dangling-service`, the dangling HPA check). A mismatch is silent: the object exists and does nothing.
3. **A NetworkPolicy that selects no pod does nothing** (kube-score `networkpolicy-targets-pod`; kube-linter
   dangling checks). The policies themselves belong to a different topic.
4. **Port names must follow the specification**, which kube-linter checks by default for deployments and
   services.
5. **Name the namespace.** The Niessen skill notes a manifest with no namespace deploys wherever the current
   context points, and kube-linter has an optional check against the `default` namespace, citing a CIS item.
6. **Label meaningfully.** Kubernetes recommends the `app.kubernetes.io/*` set (name, instance, version,
   component, part-of, managed-by) on top-level resources and on the pod template, so tools and people can
   identify them. Using them is optional (Learnk8s).

## 3.2 API versions
1. **A manifest that works today can fail after a cluster upgrade** if it uses an API version that has been
   deprecated and then removed. The API server uses `apiVersion` and `kind` to decode, validate, admit and
   store the object, and can reject it before the application starts (Learnk8s).
2. **It also affects Helm**: stored release metadata can still carry old API versions, so a live release can be
   the problem, not only the chart (Learnk8s). Learnk8s names Pluto, kube-no-trouble and KubePug for scanning
   manifests, charts and releases, and `helm-mapkubeapis` for releases that already carry removed versions; none
   of those four was read for this block.
3. **Compare against the official deprecation guide** for the versions you run now and the ones you plan to
   upgrade to (Learnk8s). kube-score (`stable-version`) and kube-linter (`no-extensions-v1beta`) flag some old
   versions.
4. **Pin the field names too**: kube-linter flags the deprecated `serviceAccount` field in favour of
   `serviceAccountName`, and a pod that names a service account that does not exist.

## 3.3 Validate in CI
1. **Run a manifest linter on every change.** The sources name kube-score and kube-linter, and kube-linter's
   optional `schema-validation` check validates against the Kubernetes API schemas using kubeconform. Which
   one you pick is a tooling choice; this block lists the checks, not the commands.
2. **A linter is not a cluster.** It cannot tell you what your PDB allows right now or whether a node has the
   topology label; the verification steps in §1 and §2 still apply.
3. **Decide which checks block the pipeline.** kube-linter enables only some of its checks by default and
   marks the rest optional; kube-score does the same (default and optional columns). Write the choice down.

## 3.4 Verify
Run the chosen linter in CI against the rendered manifests (the output of Helm or Kustomize, not only the
templates), and make a deliberate mistake once, such as a selector typo, to confirm the pipeline fails.
