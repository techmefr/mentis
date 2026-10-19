# airflow-dag-authoring-pitfalls §2 — DAG parsing: top-level code, variables and file layout

Sources: the Airflow documentation page `airflow-core/docs/best-practices.rst` (apache/airflow at 868d791, airflow-core 3.4.0 in its `pyproject.toml`), sections "Top level Python Code", "How to check if my code is top-level code", "Dynamic Dag Generation", "Airflow Variables", "Timetables", "Triggering Dags after changes" and "Reducing Dag complexity"; and the Astronomer `reference/best-practices.md` (astronomer/agents at 486ee63), section "Avoid Top-Level Code". Read in full 2026-10-15.

## 2.1 Why top-level code is expensive
1. **The Dag processor executes everything outside the operators' `execute` methods repeatedly,** at a minimum interval set by `min_file_process_interval` (a configuration option; the Astronomer file says about every 30 seconds, a figure the Airflow page does not give and that is not relied on here). The scheduler continuously makes sure that what is in the Dags is reflected in the scheduled tasks.
2. **So the top level may only create operators and build their dependencies.** The page says to run no database access, no heavy computation and no network operation there.
3. **The page's example:** a Dag with a top-level `expensive_api_call()` takes an additional 1,000 seconds to parse compared with the functionally equivalent Dag that calls it inside a task. Moving the call into the task means it runs only when the task runs.
4. **Imports are top-level code too.** Expensive imports (the page names `pandas`, `torch` and `tensorflow`) should be local imports inside the callables, and a module that executes code at import time hurts the scheduler the same way.
5. **Top-level code also includes the code that computes default values of arguments.**
6. **To check whether a piece of code is top-level, add a print statement and run `python <my_dag_file>.py`:** what prints is executed at parse time. In the page's example the function called to compute a `task_id` prints, the callable passed as `python_callable` does not.

## 2.2 Airflow Variables
1. **`Variable.get()` at the top level makes a request on every parse of the Dag file** unless caching is enabled; the page says this gives suboptimal performance and can make the file time out before it is fully parsed.
2. **Read variables where they are cheap:** inside an operator's `execute()`, inside a task, or through a Jinja template (`{{ var.value.<name> }}`, or `{{ var.json.<name> }}` to deserialize JSON), which delays the read until the task runs.
3. **If a Variable must be read in top-level code,** the page says its cost can be reduced by enabling the experimental secrets cache with a sensible TTL.
4. **For a variable that holds sensitive data, use a secrets backend.** The page recommends it for any such variable.

## 2.3 Timetables
1. **Do not read Variables, Connections or the Airflow database in timetable code:** not at module level, not in `__init__`, not in scheduling methods such as `next_dagrun_info`. The scheduler and the Dag processor rebuild the timetable from the serialised Dag by calling `deserialize`, which calls `__init__` again, so the lookup runs on every load, and if it fails (for example the Variable does not exist) the timetable cannot be loaded.
2. **Pass configuration as plain arguments and store it with `serialize` and `deserialize`.** If the value comes from a Variable, read it in the Dag file and pass it to the timetable; it is then serialised with it and refreshed whenever the file is parsed.

## 2.4 File layout and generated Dags
1. **A Dag file is parsed by one file processor,** so many Dags generated from one file make changes slow to appear. The page says to consider splitting them when the delay is observed.
2. **Do not copy near-identical Dag files:** the page says it causes repeated imports of the same resources, and prefers dynamic generation that minimises repeated code.
3. **Dynamic generation makes the top-level rules matter more.** The page lists three sources: environment variables (not Airflow Variables), generated Python code in the Dag folder, and a generated configuration file in the Dag folder.
4. **A simpler structure schedules faster:** the page says a linear chain has fewer scheduling delays than a deeply nested tree with exponentially growing dependants. It also says no metric exists for Dag complexity and that making the Dag load faster has the biggest effect on scheduler performance.

## 2.5 After a change
1. **Do not trigger a Dag immediately after changing it or its accompanying files.** The files have to reach the Dag processor, be parsed and stored, which the page says takes from seconds to many minutes. Wait for the Dag to appear in the UI.
2. **The options named for long delays:** `scheduler_idle_sleep_time`, `dag_processor` `min_file_process_interval`, `refresh_interval`, `parsing_processes` and `file_parsing_sort_mode`.

## 2.6 Checks (own guidance)
1. Run `python <dag file>` with a timer and with print statements in anything that is not a task body: nothing may print or wait.
2. Search the Dag files for `Variable.get` (including inside f-strings and operator `env` dictionaries, the page's three bad examples), database hooks and HTTP calls outside a task.
3. The check is made in an environment with the scheduler's dependencies and environment variables (§4.1).
