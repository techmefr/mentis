# airflow-dag-authoring-pitfalls §3 — Passing data, credentials, waiting and fan-out

Sources: the Airflow documentation page `airflow-core/docs/best-practices.rst` (apache/airflow at 868d791, airflow-core 3.4.0 in its `pyproject.toml`), section "Communication"; and the Astronomer `reference/best-practices.md` (astronomer/agents at 486ee63), sections "Handle Large Data (XCom Limits)", "Never Hard-Code Credentials", "Use Dynamic Task Mapping", "Configure Retries and Scaling" and "Sensor Modes and Deferrable Operators". Read in full 2026-10-15. Points taken from the Astronomer file only are marked (Astronomer).

## 3.1 Passing data between tasks
1. **Do not hand a file from one task to the next through the local filesystem.** With the Kubernetes or Celery executor the tasks of a Dag run on different servers, so the downstream task is likely to run where the file does not exist; the page's example is a task that downloads the file the next task processes. With the local executor a file on disk can still make retries harder, for example a config file deleted by another task.
2. **Use XCom for small messages, and remote storage (S3, HDFS) for larger data,** passing the path through XCom: the task that stores the processed data pushes the path, the downstream tasks pull it and read the data. (Astronomer) The same idea is called the claim-check pattern, and the file warns that a large return value may exceed XCom limits.
3. **(Astronomer) For automatic offloading the file names the object storage XCom backend of the `common-io` provider,** with a size threshold. Its settings were not checked against the provider documentation and are not relied on.

## 3.2 Credentials
1. **A task must not store passwords or tokens inside itself.** The page says to use Connections, kept in the Airflow backend and fetched by a unique connection id.
2. **Do not hard-code a connection string with a password.** (Astronomer) The same file shows reading a connection through the Connection API, or a templated variable, as the alternatives. Its third example stores an API key in a Variable; that example is not carried, since the Airflow page recommends a secrets backend for sensitive values (§2.2).

## 3.3 Waiting
1. **(Astronomer) A sensor in `poke` mode, which is the default, holds a worker slot for the whole wait.** The file says to prefer `deferrable=True` when the operator offers it, to otherwise use `mode="reschedule"` for waits longer than a few minutes, and to keep `poke` for checks shorter than a minute.
2. **(Astronomer) `deferrable=True` hands the wait to the triggerer,** which the file calls the most efficient option.

## 3.4 Fan-out and limits
1. **(Astronomer) Use dynamic task mapping instead of looping inside one task:** `expand` over a list returned by an upstream task, with `partial` for constant parameters. The file's reasons: the loop is sequential and one failure fails all, whereas mapped instances run in parallel.
2. **(Astronomer) Cap concurrency and use pools for resource-limited work:** `max_active_runs`, `max_active_tasks`, and `pool="..."` on tasks that hit a constrained resource. The retry settings it shows (3 retries, 5 minute delay, exponential backoff) are sample values.

## 3.5 Checks (own guidance)
1. No task reads a file written by another task unless it lives in remote storage whose path was passed through XCom.
2. No sensor with a wait longer than a few minutes runs in the default mode.
3. No credential appears in a Dag file, a task body or a default argument.
