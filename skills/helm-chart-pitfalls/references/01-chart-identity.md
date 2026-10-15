# helm-chart-pitfalls §1 — Chart name, namespace and versions

Three things are fixed when a chart is created and are hard to change once other tools reference them: its
name, the namespace it deploys to, and how it is versioned.

## 1.1 Chart names
1. **A chart name follows DNS-1123 label rules**: only lowercase letters, digits and dashes, a lowercase
   letter or digit at both ends, at most 63 characters (Helm's conventions page).
2. **These names are invalid**: uppercase letters (`MyChart`), underscores (`my_chart`), dots (`my.chart`), a
   leading dash, a trailing dash, and anything over 63 characters. Valid ones look like `drupal`,
   `nginx-lego`, `aws-cluster-autoscaler`.
3. **`helm lint` checks the name against these rules**, so the check costs one command; run it when the
   chart is created and again whenever it is renamed.
4. **`Chart.yaml` keeps its capital C**: the file name is case sensitive (the same page). The page also says
   "chart" is not a proper noun and "Helm" is the project; that is wording, not behaviour.

## 1.2 No namespace in the templates
1. **Do not define `metadata.namespace` in the templates of a chart.** The namespace belongs in the call to
   the Kubernetes client, with a flag such as `--namespace`.
2. **Why it breaks**: Helm renders the templates as they are and hands them to a client, which may be Helm
   itself or another program (the page names kubectl, flux and spinnaker). A namespace baked into the
   template overrides the one the caller chose.
3. **A chart that installs correctly with Helm only proves one of those clients.** Own guidance, not from
   the page: render the chart once with `helm template --namespace` set to a value that appears nowhere in
   the chart and search the output for namespaces.

## 1.3 Version numbers
1. **Helm uses SemVer 2 wherever it can**; Docker image tags are called an unfortunate exception because
   they do not necessarily follow it (Helm's conventions page).
2. **A SemVer version stored as a Kubernetes label value has its `+` replaced by `_`**, because labels do
   not allow `+`. Own guidance, not from the page: do the replacement in one helper rather than at each label.

## 1.4 YAML formatting
1. **Indent YAML with two spaces, never tabs** (the conventions page).

## 1.5 Verify
Run `helm lint`, then render with `helm template` and the namespace on the command line only: no object in
the output may carry a namespace you did not pass.
