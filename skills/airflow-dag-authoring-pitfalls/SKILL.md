---
name: airflow-dag-authoring-pitfalls
description: "Use when writing, testing or upgrading Apache Airflow DAGs: re-runnable tasks (upsert, data interval partitions, no now()), top-level code and Variable.get at parse time, passing data between tasks, credentials, sensor modes, dynamic task mapping, the loader test, mocking variables and connections, upgrade steps and Airflow 3 import and API changes."
---

# airflow-dag-authoring-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the Airflow traps that a generic pipeline rule does not name. The
premise: **a DAG file is code that the scheduler's Dag processor executes over and over, and a task is code
Airflow will run again after a failure**. Generic idempotence, data quality and cost rules are in
`data-pipeline-conventions`; this block holds what is specific to Airflow's execution model. Deployment,
executors and Astro-specific tooling are not covered.

## When
- A DAG file, task or operator is written or changed.
- A DAG parses slowly, times out, or a value read at parse time is wrong or costly.
- Tasks exchange data, wait on external events, or are fanned out.
- An Airflow upgrade, or a move from Airflow 2 to Airflow 3, is planned.

## Steps

**Read only the section the task meets.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Task as a transaction, upsert, data interval partitions, no `now()`, deleting a task | a task writes data or is retried | [`01-rerunnable-tasks.md`](./references/01-rerunnable-tasks.md) |
| 2 | Top-level code, imports, Variables, timetables, file layout, waiting after a change | a DAG file is slow to parse, or reads a Variable | [`02-dag-parsing.md`](./references/02-dag-parsing.md) |
| 3 | Files between tasks, XCom, credentials, sensor modes, mapping, pools | tasks exchange data, wait, or fan out | [`03-communication-and-waiting.md`](./references/03-communication-and-waiting.md) |
| 4 | Loader test, unit tests, mocking, staging, upgrade steps, Airflow 3 changes | tests are written, or an upgrade is planned | [`04-testing-and-upgrades.md`](./references/04-testing-and-upgrades.md) |

## Output / checkpoint
Each section ends with checks. For a change touching this block: the task run twice for the same interval
leaves the destination unchanged, `python <dag file>` in the scheduler's environment prints nothing outside the
task bodies and loads quickly, and no credential, local file hand-off or default-mode long sensor remains.

## Guardrails
- Never read or write "the latest data" or call `now()` for a critical computation inside a task (§1.2).
- Never run a database call, network call or heavy import at the top level of a DAG file (§2.1).
- Never call `Variable.get()` at the top level without caching, and never put sensitive values in plain
  Variables (§2.2).
- Never pass a file between tasks through the local filesystem (§3.1).
- Never store a credential in a task or a DAG file (§3.2).
- Versions: the Airflow page read is that of the main branch at the stamped commit (airflow-core 3.4.0); the
  Astronomer file is a vendor reference and its points are marked. Nothing was run (🟡).
- The "trigger it first, no pre-flight" testing rule of one Astronomer skill is not carried: it is unsafe
  against a real environment.

## Origin
Rewritten from the Airflow `best-practices.rst` page (Apache-2.0, apache/airflow commit 868d791) and the
Astronomer `authoring-dags` best-practices reference (Apache-2.0, astronomer/agents commit 486ee63), read
2026-10-15. Open points and own guidance are in [`references/origin.md`](./references/origin.md).
