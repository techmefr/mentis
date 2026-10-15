---
name: helm-chart-pitfalls
description: "Use when a Helm chart is authored or reviewed: the chart name (DNS-1123, helm lint), a namespace written into templates (and GitOps tools that render the chart as-is), values naming and layout (lowerCamelCase, dashed keys and index, flat versus nested, quoting strings and big integers, maps instead of lists so --set works), defined template names shared across subcharts, a YAML comment on a template line that calls required, one resource per template file, and pod templates (fixed image tag, imagePullPolicy, selectors that match changing labels)."
---

# helm-chart-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the chart as a deliverable. The three sections share one premise:
**a chart is rendered by tools you do not control, from values written by people who never read the
template, so every convention is about what still works when someone else renders it**. The workload fields
the chart ends up producing (probes, resources, rollout) are in `kubernetes-workload-pitfalls`; config reload
and manifest validation are in `kubernetes-availability-config-pitfalls`.

## When
- Creating a chart, or reviewing a change to `Chart.yaml`, `values.yaml` or `templates/`.
- A chart installs with Helm but fails or lands in the wrong namespace under another tool.
- A value set with `--set` does not reach the template, or arrives with the wrong type.
- Two charts, or a chart and its subchart, break each other through a shared helper name.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Chart name, namespace in templates, version numbers, YAML indentation | a chart is created or renamed, or a template pins a namespace | [`01-chart-identity.md`](./references/01-chart-identity.md) |
| 2 | Values: names, dashed keys, flat versus nested, types, layout for `--set` | `values.yaml` is designed or a value does not arrive as written | [`02-values.md`](./references/02-values.md) |
| 3 | Templates and pods: file layout, defined names, comments and `required`, images, selectors | a template file or a `define` is added, or a pod template is written | [`03-templates-and-pods.md`](./references/03-templates-and-pods.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: `helm lint` ran clean on the final chart (§1.1), the chart was
rendered with `helm template` and with the namespace given only on the command line (§1.2), a value was
overridden with `--set` and the rendered manifest changed (§2.4), and the chart was rendered once with every
`required` value unset to see the failure (§3.3). A chart that was only read is not verified.

## Guardrails
- Never write `metadata.namespace` in a template (§1.2).
- Never use a dashed or capitalised key in your own values (§2.1).
- Never leave a string unquoted in a template when the value could be read as another type (§2.3).
- Never name a `define`d template without the chart name prefix (§3.2).
- Never put a `#` YAML comment on a template line that calls `required` (§3.3).
- Never use a floating image tag in a pod template (§3.4).
- This block states Helm documentation as of the repository read on the date in
  [`references/origin.md`](./references/origin.md). The page is the Helm project's own best-practices guide,
  but the Helm version it describes was not checked, and nothing was run while writing the block.

## Origin
Rewritten from the Helm project's chart best-practices pages for conventions, values, templates and pods
(helm/helm-www, MIT), read 2026-10-16. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
