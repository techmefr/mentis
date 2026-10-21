# cdc-capture-and-ingestion-quality-pitfalls §3 — Quality at ingestion

Sources: the Core documentation of Great Expectations at commit 3be49de (expectation suites, row conditions, result formats, validation definitions and checkpoints with actions, retrieving unexpected rows), and the "lag" remark in the Debezium PostgreSQL connector page at 8d6ccc1, read 2026-10-20. The general rules of data quality (dimensions, loud failure, quarantine, counts in and out) are `skills/data-pipeline-conventions` §2 and are not repeated. "Own guidance" marks craft knowledge.

## 3.1 Lag and freshness
1. **Measure end-to-end lag from the source's own timestamp.** The Debezium page says an event carries the time of the change at the source and the time the connector processed it, and that comparing them gives the lag between the database update and the connector. Add the target's load time for the whole path. Symptom of measuring only consumer lag: green dashboards while the connector is hours behind.
2. **Alert on the age of the newest event per table,** not only on the pipeline's heartbeat (own guidance). A quiet table is legitimate; a quiet table during business hours is a question.
3. **Heartbeats prove the reader is alive, not that data is flowing** (§1.1). Show both.

## 3.2 Reconciliation against the source
1. **Compare row counts and key sets between source and target on a schedule,** on a snapshot-consistent view or with a tolerance window for in-flight changes (own guidance). Symptom of skipping it: a silently dropped partition or a failed merge found by a customer. Fix: a count per table per hour, and a sampled key-by-key comparison per day.
2. **Compare aggregates that matter to the business,** such as a sum of amounts per day, not only counts (own guidance).
3. **Deletes are the usual difference.** A target that never applies deletes drifts upward; check that count first (own guidance).
4. **Run reconciliation with different credentials from the pipeline's,** or a shared bug hides itself (`skills/data-pipeline-conventions` §2.8).

## 3.3 Validation suites on a batch
1. **Group the checks that describe one dataset into a suite, and run the suite against each batch.** The Great Expectations documentation says everything validated in production workflows should live in a suite, and that a batch is whatever the batch definition selects, for example a partition by date. Symptom of validating "the table": the whole history is rechecked each run, or only the latest rows are checked and old corruption stays. Fix: batch by load date for the new data and a separate, scheduled full check for the whole table (own guidance on the split).
2. **Restrict a check to the rows it applies to.** The documentation's example: a country-of-origin column must be filled only for imported products, so an unconditioned check fails for local products. It supports a row condition on the expectation. Symptom: a check that fails daily for a legitimate reason and gets disabled. Fix: add the condition, and test both sides of it.
3. **Test a new check on a sample batch before it gates a run.** The documentation has a step for testing one expectation on a sample, used during exploration. A check that was never seen failing is untested (`skills/data-pipeline-conventions` §2.12).
4. **Choose the result detail on purpose.** The documentation lists four levels from a boolean to a complete result, the default being a summary, and says higher levels return a limited number of failing rows for some check types (a cap the page gives at the commit; re-read it). Symptom: an incident where the alert says "check failed" and nobody can see which rows. Fix: use a custom check that can return all failing rows when you need to quarantine, and store them with the run identifier (the documentation has a retrieval method for custom query checks).
5. **A check that runs after the load needs a gate before consumers.** A checkpoint runs one or more validation definitions and then actions based on the results (notify, update a status, call a hook). Decide which actions block the downstream step and which only notify (own guidance on the split).
6. **Alerting actions go to a person or a rota, with the run, the table, the check, the count and an example** (own guidance, same as `skills/data-pipeline-conventions` §2.5).

## 3.4 What to do when a check fails
1. **Stop the downstream step for failures of a set property** (duplicate keys, a total that disagrees); quarantine rows for failures attributable to a row (`skills/data-pipeline-conventions` §2.4).
2. **Name who decides to override** and record it with the run (own guidance).
3. **Keep a way to re-run the failed batch alone** after the source or the rule is fixed, so a failure is not a manual repair (own guidance).

## 3.5 Checks (own guidance)
1. For each table: freshness alert, count reconciliation, one key-set reconciliation, the suite with owners, the action list, and a documented unblock path.
