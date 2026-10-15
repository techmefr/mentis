# airflow-dag-authoring-pitfalls: origin and source stamps

> Provenance of `skills/airflow-dag-authoring-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us against an Airflow deployment. No DAG was parsed or
run, no scheduler was started.

## Sources (all read in full 2026-10-15, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| apache/airflow at commit 868d791 (2026-10-15), `airflow-core/docs/best-practices.rst` (1,242 lines, read in three passes). `airflow-core/pyproject.toml` at that commit shows version 3.4.0 | Apache-2.0 (`LICENSE` re-read 2026-10-15, Apache License Version 2.0 text; the page carries the ASF header) | Task as transaction, partitions, `now()`, communication between tasks, top-level code, Variables, timetables, complexity, loader and unit tests, staging, mocking, upgrade steps, ruff `AIR` rules |
| astronomer/agents at commit 486ee63 (2026-10-07), `skills/authoring-dags/reference/best-practices.md` (466 lines) | Apache-2.0 (`LICENSE` re-read 2026-10-15, Apache License Version 2.0 text) | Claim check, sensor modes, deferrable operators, dynamic task mapping, pools, Airflow 3 imports, the anti-pattern list |

## Version bounds stated in the sources
- The Airflow page is the documentation of the main branch at the stamped commit (airflow-core 3.4.0 in
  `pyproject.toml`); its examples use `from airflow.sdk import ...` and spell DAG as "Dag". It states two
  version facts itself: `TaskInstance.run()` and `render_templates()` removed in Airflow 3.2, and the removals and
  moves in 3.0 listed in its ruff example output.
- The Astronomer file states Airflow 2.x and 3.x import forms and says Airflow 2 imports are deprecated on
  Airflow 3 with `AIR31x` warnings.
- `use_job_schedule`, the `[scheduler]` and `dag_processor` option names are quoted as the page names them; no
  option was checked against the configuration reference.

## Removed (in the sources, not carried)
- The Astronomer example that reads an API key with `Variable.get` and presents it as correct: the Airflow page
  recommends a secrets backend for sensitive values, so the example is dropped. Also the review's decision on
  the Astronomer `testing-dags` rule "trigger first, no pre-flight": not read for this block and not carried.
- The Astronomer statement that DAG files are parsed every 30 seconds: the Airflow page gives a configurable
  minimum interval instead.
- The Astronomer statement that Airflow 3 serialises DataFrames natively, and its XCom object storage settings:
  the Airflow page does not confirm them.
- The sections of the Airflow page on custom operators, Ruff installation versions, the `ExternalPythonOperator`,
  `PythonVirtualenvOperator`, Docker, Kubernetes and Celery-queue strategies, cluster policies, the watcher
  pattern and static type checking: outside the review item.
- Astronomer's TaskFlow, provider operators, setup and teardown, data quality operators and Assets sections.
- Instructions found in the cloned files, including the Stop hook in the frontmatter of the Astronomer
  `authoring-dags` skill, which was not read and is not a source.

## Not verified
1. **Vendor points.** Sensor modes, deferrable operators, dynamic task mapping, pools, the Airflow 3 metadata
   database restriction, `execution_date` and SubDAG replacement come from the Astronomer file alone and are
   marked (Astronomer) in the text. The Airflow page does not state them in the pages read.
2. **Executor behaviour** ("different servers with the Kubernetes or Celery executor") is quoted from the page.
3. **Own guidance, labelled in the text:** every "Checks" section.
4. **The ruff version** pinned in the page's install line was not repeated.
5. **Airflow 2 behaviour** was not separately checked: where the page says "Dag" and shows `airflow.sdk`
   imports, Airflow 2 users should expect the older import paths of the Astronomer file.

## Related blocks
`data-pipeline-conventions` §1 (idempotence of a whole run), §2 (data quality), `background-jobs-conventions` §1
to §5, `source-freshness`.
