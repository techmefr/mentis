# postgres-operations-and-exposed-api-pitfalls §1 — Maintenance and diagnosis

Sources: the `monitor-vacuum-analyze`, `monitor-pg-stat-statements`, `monitor-explain-analyze` and `schema-partitioning` rules of the `supabase-postgres-best-practices` skill in supabase/agent-skills at c9be0e9, read 2026-10-20.

## 1.1 Statistics and vacuum
1. **The planner chooses plans from table statistics.** After a large load, delete or update, the statistics describe a table that no longer exists, and the symptom is a sequential scan where an index would win. Refresh them for the table (or the columns the filters use) and compare the plan again.
2. **See when each table was last vacuumed and analysed** in the per-table statistics view (the last-vacuum, last-autovacuum, last-analyze and last-autoanalyze columns). A busy table that never shows an automatic run is the lead to follow.
3. **Autovacuum triggers on a fraction of changed rows, so a big table waits for a huge absolute number.** For a high-churn table, lower the scale factors on that table only, not server-wide, and watch the vacuum progress view rather than assuming it ran.
4. **Dead rows are cleaned only if nothing can still see them.** An old open transaction, including an idle one, holds the cleanup back (a row version must stay while any transaction may still see it; PostgreSQL manual, routine vacuuming) and the table grows (`skills/sql-conventions` §4.7 sets the timeout that ends it). Look for the oldest open transaction before tuning autovacuum.
5. **A plain vacuum makes space reusable inside the table; it does not normally shrink the file** (it returns space to the operating system only when the pages at the very end of the table are entirely free and a lock is easily obtained; PostgreSQL manual, routine vacuuming). A table that must give space back needs a rewrite, which locks it: schedule and test it (`skills/devops-conventions` §6).

## 1.2 Finding the costly queries
1. **Enable the statements extension and sort by total execution time first, then by mean time.** A cheap query called millions of times costs more than one slow report, and only the total shows it.
2. **Sort by call count as well** to find the chatty loop (`skills/sql-conventions` §3.11).
3. **Reset the statistics after a fix** so the next reading measures the fix, not history.
4. **The extension must be listed in the server's preload setting (a restart is needed) and created in each database you query it from;** one without the other shows nothing. Query identifier computation must also be on (automatic by default). The reset function with no arguments discards all statistics, and the total and mean execution time columns are in milliseconds (PostgreSQL manual, pg_stat_statements).

## 1.3 Reading a plan
1. **Run the plan with timing and buffer counts, on a copy when the statement writes,** because the analyse option executes it (`skills/sql-conventions` §3.2).
2. **What to look for:** a sequential scan on a large table with many rows removed by the filter (missing or unusable index); estimated rows far from actual rows (statistics, §1.1); reads far above hits in the buffer line (data not cached); a nested loop with a high loop count (join strategy); an external-merge sort (the sort did not fit its memory).
3. **One finding, one change, one new plan.** Several changes at once leave nobody knowing which one helped.

## 1.4 Partitioning
1. **Partitioning pays when queries filter on the partition key and old data is removed in bulk:** dropping a partition is instant where a large delete runs for hours and leaves dead rows behind.
2. **The key must appear in the queries that matter,** or every partition is scanned and the table only gained complexity. The partition key also has to be part of any unique or primary key constraint, and the key cannot be an expression there (PostgreSQL manual, partitioning).
3. **Create future partitions ahead of time, from a schedule.** An insert with no matching partition fails with an error (PostgreSQL manual, partitioning); the fix is a job, not a manual step.
4. **Do not partition on a row count taken from a blog post.** The source gives a rule-of-thumb size; measure scan and vacuum time on your table first.

## 1.5 Checks (own guidance)
1. For a slow query, the report holds: the plan before, the single change, the plan after.
2. For a bloated table: the oldest open transaction, the dead-row count and the last autovacuum time are written down before any setting changes.
3. Before partitioning: the three most frequent queries filter on the intended key.
