# dbt-cli-and-model-versioning-pitfalls: origin and source stamps

> Provenance of `skills/dbt-cli-and-model-versioning-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from skill files and rule pages, never run by us against a dbt project. No command was
executed, no macro was compiled.

## Sources (all read in full 2026-10-15, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| dbt-labs/dbt-agent-skills at commit 7c7b5fa, `skills/dbt/skills/running-dbt-commands/SKILL.md`, `adding-dbt-unit-test/SKILL.md` and `references/special-cases-ephemeral-dependency.md`, `working-with-dbt-mesh/references/model-versions.md`, `model-contracts.md`, `groups-and-access.md` | Apache-2.0 (`LICENSE` re-read 2026-10-15, Apache License Version 2.0 text) | Build against run, selectors, selector guard, defer, Fusion notes, versions and the pointer, contracts, constraints, access, groups, unit test mechanics |
| dbt-labs/dbt-project-evaluator at commit fb3b3bcb68a473d61f8f4c0da55f962080c48f14, `docs/rules/modeling.md` and `docs/rules/performance.md` | Apache-2.0 (`LICENSE` re-read 2026-10-15, Apache License Version 2.0 text) | DAG structure checks and performance checks with their documented exceptions |

## Version bounds stated in the sources
- `latest_version_pointer` is built in from dbt Core 1.12 and Fusion and is described in the source as currently
  beta in dbt's documentation; dbt Core 1.11 and earlier use the `create_latest_version_view` post-hook. The
  source says to confirm the feature for the exact version.
- Removal of a contracted model counts as a breaking change from dbt 1.9 (contracts file).
- The Fusion points (`--resource-type` with `dbt test`, `--static-analysis`, `dbt clean`, top-level `config`
  properties) are quoted as the sources state them; none was checked against Fusion.
- The evaluator thresholds (3 leaf children, 7 joins, chain of 4) are the defaults named on the rule pages at the
  stamped commit.

## Removed (in the sources, not carried)
- The `running-dbt-commands` preference to use MCP tools and its assumptions about file locations of the CLI
  binaries: environment specific.
- The warehouse data type and caveat files of the unit test skill, `spec.md`, `examples.md` and the incremental,
  overrides and versioned-model special cases: not read in full for this block.
- The evaluator rule pages on documentation, testing, structure and governance: outside the review item.
- Instructions directed at agents in the cloned files, including `CLAUDE.md` of the skills repository, which is
  not a source.

## Not verified
1. **The pointer macro and the post-hook** were not compiled or run, and the `create view` syntax is platform
   dependent according to the source.
2. **The constraint enforcement table** is quoted from the contracts file and not checked against warehouse
   documentation.
3. **The `--empty` flag** is described as the unit test skill describes it; no dbt documentation page was read.
4. **Own guidance, labelled in the text:** every "Checks" section.

## Related blocks
`data-pipeline-conventions` §2 (schema and unit tests, contracts, data contracts), `source-freshness`.
