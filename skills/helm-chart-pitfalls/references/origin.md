# helm-chart-pitfalls: origin and source stamps

> Provenance of `skills/helm-chart-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us: no chart was created, linted or rendered while
writing it. Every file below was re-read in full on 2026-10-16 before a rule was taken from it, and the
repository's LICENSE file was read again.

## Sources (all read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| helm/helm-www (commit `2364a04`), `docs/chart_best_practices/conventions.md` | MIT (LICENSE file: MIT licence text, copyright Microsoft Corporation 2017) | Chart name rules and `helm lint`, SemVer and the `+` to `_` label convention, two-space indent, namespace in templates |
| the same repository, `docs/chart_best_practices/values.md` | MIT | Value naming, dashed keys and `index`, flat versus nested, type coercion and quoting, `--set` friendly structure, documenting values |
| the same repository, `docs/chart_best_practices/templates.md` | MIT | `templates/` layout, namespaced `define` names, YAML versus template comments and the `required` case |
| the same repository, `docs/chart_best_practices/pods.md` | MIT | Fixed image tags, `imagePullPolicy` default, PodTemplate selectors |

The pages are in a documentation website repository whose licence file is the repository's MIT text; no
separate licence for the documentation content is stated, so the pages were rewritten, not copied. The
code samples are small adaptations with placeholder names and no comments.

## Removed in the verification pass
1. **"Quote all strings, store large integers as strings"** was kept, but the review's wording on big
   integers ("become scientific notation") was narrowed to the page's "in some cases".
2. **Style-only points were left out on purpose**: whitespace chomping and brace spacing, blank lines in
   generated output, the JSON-in-templates section, the "Helm versus helm" capitalisation.
3. **Pages not read, so nothing is taken from them**: `labels.md`, `rbac.md`, `custom_resource_definitions.md`,
   `dependencies.mdx`, `index.mdx` of the same directory.

## Not verified
1. **Which Helm version the guide describes** was not checked; the page mentions Helm 2.4 and 2.5 only for
   the `--set` list syntax, and that sentence is kept as history.
2. **`helm lint` coverage** beyond the chart-name check was not read; the page states only that the name
   is validated.
3. **Written by us, not sourced:** the verification paragraphs, the `helm template` check for a hard-coded
   namespace (§1.2), the helper for the `+` replacement (§1.3), the reasoning that the template engine
   runs before YAML is read (§3.3), the rule to switch off a template line by removal or a template
   comment (§3.3), the link between a fixed tag and `IfNotPresent` (§3.4), and the rule that only constant
   labels belong in a selector (§3.5).
4. **chart-testing, helm-unittest and kubeconform** were not read; the block says nothing about testing
   a chart beyond `helm lint` and `helm template`.

## Related blocks
`kubernetes-workload-pitfalls`, `kubernetes-availability-config-pitfalls`, `dockerfile-build-pitfalls`,
`docker-compose-file-pitfalls`, `devops-conventions`.
