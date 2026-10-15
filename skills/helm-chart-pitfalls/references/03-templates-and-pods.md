# helm-chart-pitfalls §3 — Templates and pod templates

Templates are where a chart meets other charts (through shared helper names), the debugging output (through
comments), and the cluster (through the pod template).

## 3.1 Layout of `templates/`
1. **File extension**: `.yaml` for files that produce YAML, `.tpl` for files that produce no formatted
   content (Helm's templates page).
2. **File names use dashes, not camelCase** (`my-example-configmap.yaml`).
3. **One resource definition per template file**, and the file name reflects the kind (`foo-pod.yaml`,
   `bar-svc.yaml`).

## 3.2 Names of defined templates
1. **A `define`d template is global.** A chart and all its subcharts can call every template created with
   `define`, so two charts defining the same name silently share, or overwrite, one helper.
2. **Prefix every defined name with the chart name**: `nginx.fullname`, not `fullname`.
3. **`helm create` generates names in this form**, which is why the page recommends starting new charts
   with it.

## 3.3 Comments, and `required`
Helm templates have two comment markers with different effects. A YAML comment (`#`) stays in the output; a
template comment (`{{- /* ... */ -}}`) does not.
1. **Use a template comment to document a template or a `define`.** It is never rendered.
2. **A YAML comment inside a template is visible with `helm install --debug`**, which is occasionally what
   you want for the user who is debugging.
3. **A `#` on a line that contains a template action does not stop the action from running.** The page's
   example: a commented-out `memory` line that calls `required` on `maxMem` still fails the render with
   `maxMem must be set` when `maxMem` is unset, (own reasoning for why: the template engine runs before
   the YAML is read, so a `#` hides nothing from it). Putting that whole block inside a template comment, so that it is not
   rendered, avoids the error.
4. **Own guidance, not from the page:** when a template line is disabled, remove it or move it inside a
   template comment; never rely on `#` to switch off a line with a template action on it.

## 3.4 Images
1. **Use a fixed tag or an image SHA in a pod template.** Do not use `latest`, `head`, `canary` or any other
   tag designed to float (Helm's pods page). The resource list is not exhaustive: Deployment,
   ReplicationController, ReplicaSet, DaemonSet and StatefulSet all contain pod templates.
2. **Images may come from `values.yaml`** so they are easy to swap, either as one field (`image`) or as
   image and tag in two fields.
3. **`imagePullPolicy` defaults to `IfNotPresent`**: `helm create` sets it that way through a value
   (`image.pullPolicy`), and Kubernetes itself defaults to `IfNotPresent` when the field is absent. To use
   another value, change it in `values.yaml` rather than in the template. Own guidance, not from the page: a fixed tag is
   what makes `IfNotPresent` safe (workload-level reasoning is in `kubernetes-workload-pitfalls` §4).

## 3.5 Selectors
1. **Every PodTemplate section declares a selector** matching the pod template labels, which makes the
   relationship between the set and its pods explicit:

```yaml
selector:
  matchLabels:
    app.kubernetes.io/name: my-app
template:
  metadata:
    labels:
      app.kubernetes.io/name: my-app
```

2. **It matters most for a Deployment.** Without a selector the whole set of labels is used to select the
   matching pods, so the selection breaks as soon as a label that changes, such as a version or a release
   date, is among them.
3. **Use only labels that stay constant for the life of the release in the selector.** This follows from the
   previous point and the page's example; the page itself does not state it as a separate rule.

## 3.6 Verify
Render the chart with `helm template` once with all `required` values set and once with one of them unset:
the second render must fail with the message you wrote. Search the output for `latest` and for pod
templates without a `selector`.
