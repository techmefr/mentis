# slo-design: origin and source stamps

> Provenance of `skills/slo-design`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from published sources, never run on a real service by us.

## Sources (read 2026-10-19, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Google SRE Workbook, "Implementing SLOs", https://sre.google/workbook/implementing-slos/ | Published online by Google; idea only | Specification versus implementation, three measurement methods and their trade-offs, SLI kinds per system type, multiple latency thresholds, why not perfect, product owner owns the target, three agreeing parties, rolling versus calendar windows, budget as one minus the target, policy contents and actions, dependency-caused misses, review rhythm |
| Google SRE Workbook, "Alerting on SLOs", https://sre.google/workbook/alerting-on-slos/ | same | Precision, recall, detection and reset time; why error-rate threshold, long window and duration fail; burn rate; multiple burn rates; short plus long window; low-traffic options; extreme targets; one parameter set and request classes |
| alirezarezvani/claude-skills, skill `slo-architect` (SKILL.md and its principles, SLI and budget references, read in full; commit 19392f7a08264ed00486a251f5b2098321771f94; LICENSE file re-read: MIT, Alireza Rezvani 2025) | MIT | Structure of the method: indicator test "would a user notice", four mistakes, owner per objective, quarterly review, composition with ramps and chaos; used as a checklist, rewritten |

## Removed
1. **Every figure**: targets, window lengths, the Workbook's example numbers and its burn-rate and window
   tables, budget tables, "reality check" target ranges and the source skill's thresholds. They are one example
   or one author's tuning, and the chapter's own tables must be re-read before use.
2. **The source skill's "target equals the median of the last month"**: an unsourced heuristic by its author;
   the Workbook starts from current performance but only as a provisional start (§2 point 4).
3. **The source skill's four-state budget table (healthy, caution, critical, violated)**: not in the Workbook
   chapter read; the policy actions here are the chapter's.
4. **Scripts, query snippets, YAML and policy templates**: a runtime, not a method.

## Not verified
1. Both chapters were read through a fetch tool's summary, not page by page. The tables and worked numbers were
   deliberately not carried; any figure must be re-read at the source.
2. The Workbook's chapter on SLO engagement, on error budget policies in full and the example policy appendix
   were not read.
3. The claim that the internal objective should be tighter than the customer promise is the source skill's
   own and is phrased here as guidance, not as a Workbook rule.
4. No monitoring product's alert syntax was checked.

## Related blocks
`skills/observability-instrumentation`, `skills/failure-classification-before-retry`,
`skills/spend-guard-fail-closed`, `skills/feature-flag-lifecycle`, `skills/chaos-experiment`,
`skills/source-freshness`.
