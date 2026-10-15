# grafana-dashboard-pitfalls §2 — Variables, panels and exceptions

A dashboard is portable only if everything environment-specific is a variable, and reviewable only if the exceptions
are written down next to it. The linter's rules are small and each one stands for one of those two ideas.

## 2.1 The datasource variable
1. **Have exactly one template variable for the data source**, named `datasource`, with the label "Data Source", of
   the Prometheus or Loki kind (dashboard-linter).
2. **Panels use that variable, not a named data source.** The panel rule checks that each panel uses the templated
   data source; it covers panels of type singlestat, graph, table and timeseries at the commit read, so a panel of
   another type is not covered by the check (dashboard-linter).
3. **Dashboards with another kind of data source, or with more than one, are the documented exception.** The rule
   says it will be updated for several data sources in future; until then write an exclusion with the reason rather
   than adding a second variable that the rule flags (dashboard-linter; the choice of an exclusion is the source's
   advice for related rules, applied here by us).

## 2.2 The job and instance variables
1. **Define `job` and `instance` variables that meet the same list** (dashboard-linter): the variable exists, is
   named and labelled `job` (or `instance`), uses the `$datasource` variable as its data source, finds its values
   with a Prometheus query, is multi-select, and has an all-value of `.+`.
2. **The `.+` all-value is what makes "All" a valid matcher.** With "All" selected and a matcher such as
   `job=~"$job"`, an all-value of `.+` matches every value instead of an empty string (our own reading of the
   all-value rule; the source states the value and not the reason).
3. **Reload the variables on time change.** The rule checks that template variables refresh when the time range
   changes, which avoids errors when telemetry was just set up and the dashboard is opened afterwards. The linter's
   `--fix` option can fix this one (dashboard-linter).
4. **Keep the queries of the variables valid PromQL**, since the linter parses them (§1.3).

## 2.3 Panels: title, description, unit
1. **Every panel has a title and a description.** The title says what the panel is for; the description is the longer
   text shown as the panel's tooltip. The rule covers panel types stat, singlestat, graph, table, timeseries and
   gauge at the commit read (dashboard-linter).
2. **A panel whose title and visualization are descriptive enough may skip the description**, with a lint
   exclusion that says so (dashboard-linter).
3. **Every panel has a unit, and it must be a valid one from Grafana's list.** The list is in the Grafana source,
   which was not read. The rule is excluded automatically when value mappings are set, and when a stat panel shows
   non-numeric values, for example a label's value. A panel that shows something with no predefined unit, or whose
   title makes the unit obvious, may use an exclusion (dashboard-linter).
4. **A panel with no targets is a defect**, from the linter's one-line description of its no-targets rule, whose page
   was not read (dashboard-linter, index line).

## 2.4 Dashboards as code
1. **Make the dashboard non-editable in the UI.** The linter checks that it cannot be edited, because a dashboard
   declared as code has that code as its source of truth, and a UI edit is lost or drifts at the next deployment
   (dashboard-linter; the consequence is our reading of its stated reason).
2. **The linter's scope is narrow.** At the commit read it states that its capabilities focus exclusively on
   dashboards that use a Prometheus data source, and describes itself as early and a work in progress
   (dashboard-linter).

## 2.5 Exceptions and CI
1. **Write an exclusion in a `.lint` file next to the dashboard**, listing the rule under `exclusions` (or under
   `warnings` to downgrade it). Always add a `reason` so the next maintainer can tell a decision from an oversight
   (dashboard-linter).
2. **Exclude the narrow case, not the rule.** Give the rule's entries by dashboard and panel, and by target index
   where a panel has several targets, so the same violation in another panel or dashboard is still reported
   (dashboard-linter).

```yaml
exclusions:
  target-rate-interval-rule:
    reason: The top 10 panels show the selected range on purpose.
    entries:
      - dashboard: Service overview
        panel: Top 10 request rate
  target-instance-rule:
    reason: The total is across all instances.
    entries:
      - panel: Requests per second
        targetIdx: 2
```

3. **Lint in CI with a pinned version and `--strict`.** The README publishes release binaries and a container image
   and recommends pinning a version and using `--strict` to fail the pipeline on warnings; `lint` also takes
   `--stdin` and `--fix`. The container runs as an unprivileged user and cannot write to a mounted directory, so
   `--fix` needs it to run as your own user (dashboard-linter).
4. **A rule downgraded to a warning blocks nothing without `--strict`.** The flag makes the run fail upon an error or
   a warning, according to the command's help text; read together with the `warnings` list, a downgraded rule only
   gates the pipeline when `--strict` is on (dashboard-linter; the second half is our reading).
5. **A lint pass is not a review.** The rules check structure and names; they do not know whether a panel answers a
   question (our own guidance, and the reason `observability-instrumentation` §1 comes first).
