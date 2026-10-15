# airflow-dag-authoring-pitfalls §1 — Tasks that can be re-run

Sources: the Airflow documentation page `airflow-core/docs/best-practices.rst` (apache/airflow at 868d791, airflow-core 3.4.0 in its `pyproject.toml`), section "Creating a task", "Deleting a task" and "Self-Checks"; and the Astronomer `skills/authoring-dags/reference/best-practices.md` (astronomer/agents at 486ee63), sections "Ensure Idempotency", "Use Data Intervals" and "Anti-Patterns". Both read in full 2026-10-15. Points taken from the Astronomer file only are marked (Astronomer). The Airflow 3 docs spell DAG as "Dag".

## 1.1 A task is a transaction
1. **Treat a task like a database transaction: it must never leave incomplete results.** The Airflow page's example is not leaving incomplete data in HDFS or S3 at the end of a task.
2. **Airflow can retry a failed task, so a task must produce the same outcome on every re-run.** The page gives three ways to guarantee it, in 1.2.
3. **A self-check task downstream of the write is part of the pattern.** The page's example: after a task that pushes data to S3, a sensor checks that the partition exists, (the example sets `poke_interval=0` and `timeout=0`); the same page suggests checking that a started service is up with an HTTP sensor.

## 1.2 What makes a re-run give the same result
1. **Replace `INSERT` by `UPSERT`.** An `INSERT` during a re-run can produce duplicate rows. (Astronomer) A delete of the interval followed by an insert for the same interval is the other shape shown, using `data_interval_start` and `data_interval_end`.
2. **Read and write a specific partition, and never read the latest available data in a task.** Someone may update the input between re-runs, which gives different outputs. The page's suggestion is `data_interval_start` as the partition, also for the paths written in S3 or HDFS.
3. **Never call `now()` or its equivalents inside a task for critical computation,** since it gives a different result on each run. The page says it is fine for a temporary log line. (Astronomer) Use the context instead: `data_interval_start` and `data_interval_end`, or the `logical_date` of the run.
4. **(Astronomer) In an SQL template, filter on the interval:** `event_time >= '{{ data_interval_start }}'` and `event_time < '{{ data_interval_end }}'`, so every run reads exactly its own slice.
5. **Repeated parameters such as a connection id or a path go in `default_args`** rather than on each task; the page says it avoids typing mistakes and that most connection types have their own parameter name, so one declaration is picked up by every operator of that type.

## 1.3 Deleting a task
1. **Removing a task from a DAG hides it from the Graph and Grid views, so its logs can no longer be reached from the web server.** If that is not wanted, the page says to create a new DAG.

## 1.4 Checks (own guidance)
1. Run the task twice for the same interval in a test and compare the destination: same rows, same counts.
2. Search the task code for `now()`, `today()` and a read of "latest"; each one needs a reason.
3. For the pipeline-wide idempotence rules (run-level side effects, partial runs, backfills) see `data-pipeline-conventions` §1.
