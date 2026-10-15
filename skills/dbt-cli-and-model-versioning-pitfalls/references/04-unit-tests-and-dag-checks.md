# dbt-cli-and-model-versioning-pitfalls §4 — Unit test mechanics and DAG checks

Sources: `skills/dbt/skills/adding-dbt-unit-test/SKILL.md` and `references/special-cases-ephemeral-dependency.md` (dbt-labs/dbt-agent-skills at 7c7b5fa), and `docs/rules/modeling.md` and `docs/rules/performance.md` (dbt-labs/dbt-project-evaluator at fb3b3bcb68a473d61f8f4c0da55f962080c48f14), read in full 2026-10-15. Why a unit test and a schema test are both needed is in `data-pipeline-conventions` §2 and is not repeated.

## 4.1 What a unit test can and cannot cover
1. **Supported:** SQL models of the current project. **Not supported:** Python models, snapshots, seeds, sources and analyses as the tested node, models from packages or other projects, `materialized view` models, recursive SQL, introspective queries.
2. **No `expect` for the final table of an incremental model,** only for what will be inserted or merged.
3. **Worth testing:** regex, date math, window functions, many-branch `case`, complex joins, past bugs, edge cases not yet in the data, refactors, public or contracted models. **Not worth testing:** warehouse built-ins such as `min()`.
4. **If any unit test of a model fails, dbt does not materialise that model.**

## 4.2 Writing one
1. **Give every `ref` and `source` of the model an `input`,** or compilation fails with "node not found". Use `rows: []` for a dependency whose values do not matter, but beware of a join that would then drop every row.
2. **`dict` is the default format and needs only the relevant columns.** `csv` is similar. `sql` needs all columns and is the only format that works for an ephemeral input, with `format: sql` on that input. No format supports Jinja.
3. **Alias table names inside the model,** which the source says is needed to unit test join logic.
4. **A seed input defaults to the seed's CSV,** replaced by an explicit input.
5. **Fixtures live under a `fixtures` folder in `test-paths`** (`tests/fixtures` by default); unit tests live in YAML under `model-paths`.
6. **A failure prints "actual differs from expected" with a diff.** The source says it takes judgement to tell a wrong test from a model bug.
7. **`dbt show` helps to find realistic inputs;** sanitise sample data of sensitive values before it becomes a fixture.

## 4.3 Running them
1. **Direct parents must exist in the warehouse** for `dbt test` alone. `dbt build --select <model>` handles the whole chain and is the source's recommendation.
2. **`--empty` builds schema-only relations** by limiting `ref` and `source` to zero rows. The source warns it overwrites an existing model with a zero-row version, so use it only when the model does not exist or its schema must change.
3. **Run unit tests in development and CI, not production:** the inputs are static, and the source names `--exclude-resource-type` and `DBT_EXCLUDE_RESOURCE_TYPES` to exclude them. On Fusion see §1 (Fusion points).
4. **To switch one off,** set `config: enabled: false`.

## 4.4 Project-evaluator checks on the DAG
These are the rule pages' findings, each flagged by a model the package builds. They are heuristics with documented exceptions.
1. **Staging is one model per source table.** Flagged: a model joining a source and a model, a mart or intermediate reading a source directly, a staging model reading another staging model or a downstream model, one source with several children, several sources in one model. Exceptions named: identical sources unioned once, heavily nested data split into several base models.
2. **Use `ref` and `source`, not a hard-coded relation.** The page says they let dbt infer dependencies, detect cycles and read from the right environment. A model with no parent usually hides one; a calendar built from `date_spine` is the named exception.
3. **A model with more than 3 leaf children, or 7 joins, is flagged** by default, thresholds set by `models_fanout_threshold` and `too_many_joins_threshold`. The page suggests 4 to 6 entities per join step.
4. **A model between a parent and a child that nothing else reads is a "rejoining" finding.** The page suggests a CTE instead, except when a function such as `dbt_utils.star` needs a relation.
5. **Duplicate and unused sources are cruft:** two source nodes on the same table give a wrong lineage, and a source with no child should be removed.
6. **A chain of 4 or more views or ephemerals triggers a warning** (`chained_views_threshold`). The page suggests a table or incremental for views used by many models or doing heavy work.
7. **Exposures should depend on `table` or `incremental` models,** not on sources or lighter materializations.

## 4.5 Checks (own guidance)
1. Every unit test has an input for every `ref` and `source`, and its model's logic is non-trivial.
2. CI runs unit tests, production does not.
3. Evaluator findings are triaged against the named exceptions, not fixed mechanically.
