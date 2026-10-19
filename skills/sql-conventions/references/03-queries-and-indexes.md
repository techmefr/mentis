# § 3 — Queries and indexes

> Section 3 of `skills/sql-conventions`. Read it when a query is written, an index added or a statement is
> slow. The method is always the same: look at the plan the engine actually chose, on data shaped like
> production, before and after the change.

1. **Read the plan, not the query.** The planner's estimates depend on table statistics, so a plan on an
   empty development table says nothing about production. Ask for the plan on realistic volume, with fresh
   statistics, and compare estimated rows to actual rows: a large gap is the usual cause of a bad plan, and
   the fix is statistics or a different index, not a query hint.
2. **`EXPLAIN ANALYZE` runs the statement.** On PostgreSQL the analyse option executes the query and reports
   real row counts and times (add the buffers option to see reads). For an `UPDATE`, `DELETE` or `INSERT`,
   that means the data changes: wrap it in a transaction you roll back, and not on a production table you
   cannot afford to lock or load.
3. **Keep the indexed column bare in the predicate.** A function or arithmetic applied to the column, an
   implicit type conversion (comparing a text column to a number), or a leading wildcard in a pattern match
   makes a plain index unusable. Rewrite as a range on the bare column (a date column compared to a half-open
   range, not `YEAR(col) = 2024`), match the literal's type to the column's, or create an expression index
   whose expression matches the predicate exactly.
4. **Half-open ranges for anything continuous.** `BETWEEN` includes both ends, so a timestamp range ending at
   midnight double-counts a row stamped exactly then. Use `>= start AND < end`. `BETWEEN` is acceptable for
   discrete values such as integers and dates when you know both ends are included.
5. **Indexes serve queries you actually run.** For a composite index, the order is: equality columns first,
   then the range or sort column; an index on `(a, b)` serves a filter on `a` or on `a` and `b`, not on `b`
   alone, and a range on one column stops the later columns being used for narrowing. A partial index on the
   hot subset (`WHERE status = 'active'`) is smaller and cheaper to maintain. A covering index (extra columns
   carried in the index) lets the engine answer without visiting the table. A pure semi-structured-column
   lookup wants a general inverted index (PostgreSQL's GIN) or a promoted column (§1.9).
6. **Every index costs on every write and in memory.** Add one for a measured query, and remove those that are
   never read: check the engine's usage statistics over a full business cycle before dropping (counters reset
   on restart), and look for an index that is the prefix of another. A unique or primary-key index may be
   unused by queries and still be required.
7. **`NOT IN` with a subquery is a trap; use `NOT EXISTS`.** If the subquery can return a null, `NOT IN`
   returns no rows at all, and the planner cannot turn it into an anti-join, so it can degrade quadratically.
   `NOT IN` with a short constant list is fine unless a parameter in the list can be null.
8. **Page with a cursor, not an offset.** `OFFSET n` reads and discards n rows, so deep pages get slower and
   concurrent inserts shift the pages. Remember the sort key of the last row and ask for the rows after it;
   make the sort key unique (add the id) so ties do not skip or repeat rows.
9. **Select the columns you need.** `SELECT *` defeats covering indexes, sends data the caller discards and
   breaks when a column is added. Count rows with `COUNT(*)`; `COUNT(col)` skips nulls and means something else.
10. **Batch writes.** Send many rows in one multi-row insert or a bulk-load command rather than one statement
    per row; defer non-essential index builds until after a bulk load. A conflict-handling insert (an upsert)
    needs a unique index on exactly the conflict target, and `DO NOTHING` is cheaper than an update that
    changes nothing.
11. **An application-side loop of single-row queries is the same defect as in any ORM.** Fetch the set in one
    statement with a join or an `IN` list (`skills/laravel-no-queries-in-loops` is the stack statement).
12. **Fix a slow query in this order:** the query's shape (§3.3, §3.7, §3.8), then the index that fits it
    (§3.5), then statistics, then the schema, and only then the engine's configuration. Changing a setting
    first moves the problem without explaining it.
13. **Prepared statements and the plan cache.** A parameterised statement may be planned once and reused (a
    generic plan) or planned per call with the actual values; the server picks by estimated cost, and the
    setting that forces one or the other exists for the case where the estimate is badly off. When a query is
    fast with a literal and slow with a parameter, compare the two plans before suspecting the index.

**Sources:** the PostgreSQL manual (using EXPLAIN, EXPLAIN ANALYZE, CREATE INDEX, PREPARE, SELECT) and the
PostgreSQL "don't do this" list (BETWEEN, NOT IN), and the MySQL manual and the vendor's published MySQL
guidance (sargable predicates, cursor pagination, index usage statistics), read 2026-10-02. Point 12's order
and points 9 and 11 are reasoning of ours.
