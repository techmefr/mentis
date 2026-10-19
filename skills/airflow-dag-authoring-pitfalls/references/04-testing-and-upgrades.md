# airflow-dag-authoring-pitfalls §4 — Testing, staging, upgrades and Airflow 3

Sources: the Airflow documentation page `airflow-core/docs/best-practices.rst` (apache/airflow at 868d791, airflow-core 3.4.0 in its `pyproject.toml`), sections "Testing a Dag", "Dag Loader Test", "Unit tests", "Staging environment", "Mocking variables and connections", "Metadata DB maintenance", "Upgrades and downgrades" and "Code Quality and Linting"; and the Astronomer `reference/best-practices.md` (astronomer/agents at 486ee63), sections "Import Compatibility" and "Anti-Patterns". Read in full 2026-10-15. Points taken from the Astronomer file only are marked (Astronomer).

## 4.1 Tests
1. **The loader test is `python your-dag-file.py`.** It catches missing dependencies and syntax errors, and must run in an environment that matches the scheduler's: the same dependencies, environment variables and shared code.
2. **The same command times Dag loading.** The page times it with `time`, runs it several times in a row to account for caching, compares before and after in the same conditions, and subtracts the interpreter start-up time measured with `time python -c ''`.
3. **Unit tests can load the Dags and check them:** a `DagBag` with `import_errors == {}`, the Dag found by id, the number of tasks, and for code-generated Dags the task dependencies against an expected dictionary.
4. **Unit test an operator by calling `execute()` with the context keys the code reads,** and a sensor by calling `poke()`. No Dag run, Dag or metadata database is needed. Render templated fields with `render_template_fields` before asserting on them. For a deferrable operator, assert that it raises `TaskDeferred` with the expected trigger, then call the method the trigger resumes into.
5. **`TaskInstance.run()` and `TaskInstance.render_templates()` were removed in Airflow 3.2,** according to the page; replace them with `op.execute(context)` and `op.render_template_fields(context)`.
6. **`dag.test()` is an integration test:** it needs a metadata database and a serialisable Dag, and does not replace unit tests.

## 4.2 Staging and mocking
1. **Keep a staging environment where possible, and parameterise the Dag** (the output path of an S3 operation, the database holding the configuration) with environment variables, instead of hard-coding values and editing them by hand per environment.
2. **Mock variables and connections with environment variables:** `AIRFLOW_VAR_<KEY>` for a variable, `AIRFLOW_CONN_<CONN_ID>` with a connection URI for a connection, patched in with `unittest.mock.patch.dict` on `os.environ`. The page says this avoids the time cost of writing them to the database.

## 4.3 Upgrades
1. **Back up the metadata database before any operation that modifies it.**
2. **Pause the Dags rather than relying on `use_job_schedule`.** The page calls pausing the better way: run `airflow dags list` first and store the list of unpaused Dags, pause them before the maintenance and unpause from that list afterwards.
3. **Add a few "integration test" Dags that use the services you depend on with test or dev accounts,** and unpause them first after an upgrade: if they fail it does not matter and you can revert to the backup; if they pass, the cluster can run tasks against your libraries and services. The page's examples: a task that retrieves a connection from the external secrets backend, one that runs a short command in a Kubernetes pod, one that writes to S3, one that runs `select 1`.
4. **Prune old metadata before a large upgrade with `airflow db clean`,** since some migrations are slow on a large database. The page says to use it with caution. It also names `db clean` for general purging as the metadata database grows with Dag runs, task runs and event logs.

## 4.4 Airflow 3
1. **Use the Task SDK imports in new Airflow 3 code:** `from airflow.sdk import DAG, task, Variable, Connection`. The Airflow page's own examples use `airflow.sdk`; (Astronomer) the Astronomer file says the Airflow 2 imports still work on Airflow 3 but are deprecated and raise `AIR31x` warnings.
2. **Ruff has Airflow-specific rules (`AIR`) that flag deprecated patterns.** The page installs `ruff` and runs `ruff check dags/ --select AIR3`; its example output reports a Dag without an explicit schedule, `schedule_interval` removed in Airflow 3.0, `airflow.datasets.Dataset` removed in Airflow 3.0, and `FileSensor` moved into the `standard` provider in Airflow 3.0. The ruff version pinned in the page's install line is a snapshot and is not repeated here.
3. **(Astronomer) Do not query the metadata database from a task.** The file says that opening a session and querying a model fails on Airflow 3.
4. **(Astronomer) Replace `execution_date` with the run's `logical_date` or with `data_interval_start`, and replace SubDAGs with task groups.** The file also replaces the deprecated dummy operator import with the `EmptyOperator` of the standard provider.

## 4.5 Checks (own guidance)
1. The loader test runs in CI in an image that matches the scheduler's.
2. Before an upgrade, the paused-Dag list is saved to a file, not kept in a head.
3. On an Airflow 3 target, `ruff check --select AIR3` runs clean on the Dag folder.
