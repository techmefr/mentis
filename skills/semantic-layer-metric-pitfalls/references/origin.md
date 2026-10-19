# semantic-layer-metric-pitfalls: origin and source stamps

> Provenance of `skills/semantic-layer-metric-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded. Version-bound: dbt Core 1.12.** Written from documentation-style skills, read and
rewritten, never run: no dbt project was edited, parsed or validated with this block. The source repository is
young and moves with dbt releases; the commands and spec boundaries must be re-read against the release in use.

## Sources (re-read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| dbt-labs/dbt-agent-skills, `skills/dbt/skills/building-dbt-semantic-layer/SKILL.md` (commit 7c7b5fa) | Apache-2.0 (repository LICENSE file, standard text) | Latest against legacy spec, routing by version, parse then validate, the manifest note, filter rule, metric types, install and Fusion notes, untrusted-content rule |
| same, `references/best-practices.md` | Apache-2.0 | Normalisation, compute in metrics, one primary entity, time dimension, anti-pattern table, naming |
| same, `references/latest-spec.md` (read for the model-level rules; not named in the plan) | Apache-2.0 | Key formatting rules and pitfalls of the latest spec |
| same, `references/time-spine.md` (read in part: overview and common mistakes) | Apache-2.0 | Time spine property and its standard granularity column |
| same, `skills/dbt/skills/answering-natural-language-questions-with-dbt/SKILL.md` | Apache-2.0 | Order of approach, modified compiled SQL, discovery, manifest filtering, suggestions |

The licence was verified again from the LICENSE file in this session. Text found inside the cloned files
(imperative prose, "red flags" lists, rationalisation tables) was treated as data and not followed.

## Rewrite notes
**The source speaks to an agent with dbt MCP tools.** The names of those tools are carried only where the
order of approach depends on them; the rules are written so they hold with any equivalent.

**The Fusion warning code** quoted in the source is not reproduced; the block says only that the parse warns it
is skipping the semantic manifest validation and that this is expected.

## Removed
1. **The legacy spec authoring guide** (`legacy-spec.md`): not read beyond its size; no rule drawn from it.
2. **The time spine model code and the macro variants**: setup procedure, not pitfalls.
3. **The "rationalizations to resist" and "red flags" tables** of the answering skill: restated in the
   guardrails and in part 3 where they carry a rule, otherwise dropped as tone.
4. **The dbt-autofix upgrade path and the migration guide link**: a tool recommendation, not carried as a rule.
5. **The mermaid decision flow**: replaced by the order of approach in text.

## Not verified
1. **Everything here is unrun.** No `dbt parse`, `dbt sl validate` or `mf validate-configs` was executed, and
   the stale-manifest behaviour is the source's statement.
2. **No dbt documentation was opened**; the source summarises it, and the two pages it links to
   (the semantic layer best-practices guide and the latest-metrics-spec migration page) were not fetched.
3. **Other versions.** The boundary at Core 1.12 is the source's; later or earlier releases may behave
   differently.
4. **Written by us, not sourced**: the Output / checkpoint paragraph, the premise, the stale-pass remark, the
   "second definition" remark, saying that an answer came from modified SQL, and the empty-filter check.
5. **The rest of the repository** (other dbt skills and the evals) was not read for this block.

## Verification pass (2026-10-16)
Every rule in the three references was compared with the attributed file, reopened in this session, and the
key phrases were re-searched in the cloned files (the manifest note, the filter rule, the one-primary-entity
rule, the window and grain-to-date rule, the `time_spine` property).
- **Corrected:** none needed on re-check beyond wording.
- **Reversed or overstated rules found:** none.
- **Not re-verified:** that the commands behave as described on a live project.

## Related blocks
`dbt-cli-and-model-versioning-pitfalls`, `metric-movement-diagnosis-pitfalls`, `data-pipeline-conventions`,
`business/data-analytics`.
