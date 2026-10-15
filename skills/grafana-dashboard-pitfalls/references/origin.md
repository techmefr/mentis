# grafana-dashboard-pitfalls: origin and source stamps

> Provenance of `skills/grafana-dashboard-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No dashboard was opened or
linted and no Grafana instance was started while writing it. The Grafana documentation and every page the linter's
rules link to were not read; every claim rests on the one repository below.

## Sources (all re-read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| grafana/dashboard-linter (commit 9241be1), `docs/index.md`, all 15 pages under `docs/rules/` and `README.md`, each in full | Apache-2.0 (repository LICENSE file, standard Apache-2.0 text) | The rule list and what each rule checks, the best-practice text of the rate-interval, `$__auto`, datasource, job, instance and panel rules, the multi-data-source exception, the exclusion mechanism and its entries, the CI usage |

The licence was verified again from the LICENSE file in this session. The repository carries no instruction aimed at
us in the files read. The YAML sample is our own, built on the shape the exclusion section of `docs/index.md`
documents, with our own dashboard and panel names.

## Rewrite notes
The label "(dashboard-linter)" marks which source states a rule. "At the commit read" marks the panel types and
rule list, which change as the linter does. The block states what the linter checks and why the source says so; it
does not claim that the rules are the Grafana project's complete guidance.

## Removed
Nothing from the review item was dropped for lack of a source: every rule in it was found again in the files above.
Left out as outside the item:
1. The `lint`, `rules` and `completion` command help texts, the build and install instructions of the README and its
   Docker details beyond the pin, `--strict` and unprivileged-user points.
2. The `template-uneditable-rule` detail beyond its stated reason, and the panel-type lists as a rule of their own.
3. The Go implementation under `lint/`, not read.

## Decisions where sources disagree
The files read do not disagree with each other. One tension is resolved by us: the datasource rule asks for exactly
one datasource variable, while the multi-data-source section tells dashboards with several data sources to write an
exclusion. The block says to write the exclusion with a reason (§2.1).

## Not verified
1. **Grafana variables and versions**: `$__rate_interval` and `$__auto` are as the linter's rules describe them. The
   only version the files give is in the address of a linked blog post, which names Grafana 7.2 and was not read; no
   Grafana or Loki version floor is stated. Re-check at writing time.
2. **The list of valid units** is in the Grafana source file the rule links to; not read.
3. **That the rules cover the panel types listed** is the linter's statement at its commit; the Go code was not
   read.
4. **The reasons given for the `.+` all-value and for non-editable dashboards**: the first is our reading, the
   second extends the source's stated reason by one step (§2.2, §2.4).
5. **The no-targets and counter-aggregation rules** appear in the index with one line and have no page; only the
   line was read (§1.3, §2.3).
6. **Written by us, not sourced:** the Output / checkpoint paragraph, the link between `$__rate_interval` and the
   two-sample rule of Prometheus (§1.1), the choice of an exclusion for multiple data sources (§2.1), the reason
   behind the `.+` all-value (§2.2) and the note that a lint pass is not a review (§2.5).

## Related blocks
`prometheus-rules-and-promql-pitfalls`, `observability-instrumentation`, `source-freshness`.
