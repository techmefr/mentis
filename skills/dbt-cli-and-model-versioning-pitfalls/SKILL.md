---
name: dbt-cli-and-model-versioning-pitfalls
description: "Use when running dbt commands, introducing a breaking change to a contracted model, or reviewing a dbt project: build against run, selectors and the selector-typo guard, defer, model versions and the latest version pointer (1.12 beta, post-hook on 1.11 and earlier), contracts, access and groups, unit test mechanics and project-evaluator DAG checks."
---

# dbt-cli-and-model-versioning-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the dbt traps that a generic data-quality rule does not name. The
premise: **a dbt command that selects nothing succeeds, and a version bump is a release to every consumer who
queries the unsuffixed name**. The generic rules (unit test against schema test, contracts as a promise, data
contracts at the producer and consumer boundary) are already in `data-pipeline-conventions` §2; this block
holds only what is specific to dbt and does not repeat them. Warehouse tuning, orchestration and dbt Cloud are
not covered.

## When
- A dbt command is written into a script, a CI job or a habit.
- A contracted or public model must change shape.
- Unit tests are added to a model, or a project is reviewed for structure.

## Steps

**Read only the section the task meets.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | `build` against `run`, selectors, `--quiet` guard, defer, CLI flavors, Fusion | a command is typed or scripted | [`01-cli-mechanics.md`](./references/01-cli-mechanics.md) |
| 2 | Versioning criteria, pointer by dbt version, two-deploy migration, deprecation | a breaking change is needed | [`02-model-versions.md`](./references/02-model-versions.md) |
| 3 | Contract scope and materializations, constraints, access, groups, `config:` nesting | a model becomes public or contracted | [`03-contracts-and-access.md`](./references/03-contracts-and-access.md) |
| 4 | Unit test mechanics and limits, `--empty`, evaluator checks on the DAG | tests are written, or the project structure is reviewed | [`04-unit-tests-and-dag-checks.md`](./references/04-unit-tests-and-dag-checks.md) |

## Output / checkpoint
Each section ends with checks. For a change touching this block: every command names a selector, a breaking
change ships as a new version while `latest_version` stays on the old one, and `dbt show` against the
unsuffixed relation still returns the old columns before the bump.

## Guardrails
- Never run a command without a selector, and never read "no nodes selected" as success (§1).
- Never promote a new version to `latest_version` in the same change that introduces it (§2).
- Never nest `contract`, `access` or `group` as top-level model properties: put them under `config:` (§3).
- Never expect `access` to control database permissions (§3).
- Versions: the pointer is `latest_version_pointer` (beta) on 1.12 and later and a post-hook on 1.11 and
  earlier; Fusion differences are quoted where the sources state them. Nothing was run (🟡).
- This block does not repeat `data-pipeline-conventions` §2 points on schema against unit tests and contracts.

## Origin
Rewritten from the `dbt-labs/dbt-agent-skills` skills and the `dbt-labs/dbt-project-evaluator` rule pages
(both Apache-2.0), read 2026-10-15. Commits, open points and own guidance are in
[`references/origin.md`](./references/origin.md).
