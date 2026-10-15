# dbt-cli-and-model-versioning-pitfalls §1 — CLI mechanics

Sources: `skills/dbt/skills/running-dbt-commands/SKILL.md` (dbt-labs/dbt-agent-skills at 7c7b5fa), read in full 2026-10-15. Points that depend on the Fusion engine are marked (Fusion).

## 1.1 Which command
1. **Prefer `dbt build` to `dbt run` while developing.** `build` is `run` plus `test` in one step, so a data quality problem shows up immediately. The skill calls `run` alone almost never the right answer during development.
2. **`dbt test` does not refresh a model.** After a model changes, running `test` checks the old relation; use `build`.
3. **Know which executable `dbt` is.** Three CLIs exist: dbt Core (a Python environment), dbt Fusion and the dbt Cloud CLI. With Core in a virtual environment and Fusion installed elsewhere, typing `dbt` runs Core. If unsure which one is in use, find out before reasoning about behaviour.

## 1.2 Selectors
1. **Always pass `--select`.** A command with no selector runs the whole project.
2. **Graph operators:** `model+` (downstream), `+model` (upstream), `+model+` (both), `model+N` (N levels downstream). A space is a union and a comma is an intersection (`tag:x,config.mat:y`). `--exclude` removes from the selection.
3. **Preview a complex selector with `dbt list --select ... --resource-type model`** before running it. `dbt list --output json` accepts `--output-keys`, and the skill lists `group`, `access` and `version` among the keys.

## 1.3 Guarding against a selector that matches nothing
1. **Pair `--quiet` with `--warn-error-options '{"error": ["NoNodesForSelectionCriteria"]}'`.** The quiet flag reduces output, and the second option turns a selection that matches no node into an error, which catches selector typos. Using `--quiet` without it hides the typo.

## 1.4 Show, variables, results
1. **`dbt show --limit N`, not a SQL `LIMIT` clause.** `--inline` runs arbitrary SQL.
2. **Pass `--vars` as a string:** `'my_var: value'` for one, a JSON object for several. The skill says to avoid special characters such as a backslash or a newline.
3. **`target/run_results.json` holds the outcome of the last command:** per node `status` (success, error, fail, skipped, warn) and `execution_time`; `compiled_code` and `adapter_response` are listed too.

## 1.5 Defer
1. **`--defer --state <path>` builds one model against production artifacts instead of building its upstream first.** `--favor-state` prefers the node definitions in the state even when they exist locally.

## 1.6 Fusion
1. **(Fusion) `--resource-type` is not supported with `dbt test`.** The skill points to dbt-fusion issue 1628 and says to use `dbt build --select <model>` or `dbt build --select <unit test name>`, and `dbt list --resource-type unit_test` to find the names.
2. **(Fusion) `--static-analysis=off` or `unsafe` overrides SQL analysis** for models with dynamic SQL or unrecognised UDFs.
3. **(Fusion) After changing files, a schema error can come from a stale schema cache:** the skill says to run `dbt clean` and re-run.

## 1.7 Checks (own guidance)
1. No script or CI step contains a dbt command without `--select`, except where a full run is the point and is written down.
2. A CI step that selects by name or tag fails when the selection is empty.
3. The script states whether it expects Core or Fusion and fails if the other is on the path.
