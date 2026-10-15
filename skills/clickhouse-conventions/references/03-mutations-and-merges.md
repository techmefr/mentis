# clickhouse-conventions §3 — Mutations and merges

Rules hold for the ClickHouse documentation current on 2026-10-08. The documentation read does not state the
version in which lightweight `DELETE` appeared; check your server before relying on it.

## 3.1 Mutations are rewrites
1. **Avoid frequent or large `ALTER TABLE ... UPDATE` and `ALTER TABLE ... DELETE`.** A mutation is an
   asynchronous background job that rewrites every part it touches, so even a one-row change can rewrite large
   parts and spike disk I/O. Mutations cannot be rolled back, survive a server restart, and a query running
   during one may read a mix of mutated and unmutated parts. The `UPDATE` page calls it a heavy operation not
   designed for frequent use.
2. **Monitor and cancel.** Watch `system.mutations` and use `KILL MUTATION` for a stuck one.
3. **Updating columns of the primary or partition key is not supported.**

## 3.2 Better ways to change or remove rows
1. **Delete a range by dropping its partition.** Dropping whole parts is efficient and needs a lifecycle-aligned
   partition key (§1.2).
2. **Use lightweight `DELETE` for occasional row deletes.** It marks rows as deleted at once and a later merge
   removes them physically, so for an unspecified time the data is still in storage; the statement waits for the
   marking by default, and `lightweight_deletes_sync` can make it return earlier, at the cost of the rows
   staying visible until the background work ends. If a deletion must be physically complete by a deadline,
   the page points at `min_age_to_force_merge_seconds` or a heavyweight `ALTER TABLE ... DELETE`.
3. **Model corrections as inserts with `ReplacingMergeTree` or `CollapsingMergeTree`.** The mutation page
   recommends them for data corrections. `ReplacingMergeTree` removes rows that share the same sorting key
   (`ORDER BY`, not `PRIMARY KEY`), but only during a background merge at an unknown time: it saves space and
   does not guarantee the absence of duplicates, so queries that need one row per key must handle that, for
   example with `FINAL` (§3.3).

## 3.3 Merges and `FINAL`
1. **Do not run `OPTIMIZE TABLE ... FINAL` on a schedule.** It forces all parts into one, ignoring the usual
   limit of about 150 GB per merged part, which can mean long merges, memory pressure and out-of-memory errors,
   and oversized parts that later merges cannot handle. Background merges are incremental and aware of
   thresholds; leave them alone unless a table is being frozen or exported.
2. **`FINAL` in a `SELECT` is a different thing.** It is sometimes necessary for results without duplicates,
   for example with `ReplacingMergeTree`, and the documentation says it is generally fine when the query
   filters on the same columns as the primary key.

## 3.4 Skipping indexes come last
1. **Add a data skipping index only after the types, the ordering key and materialised views are right.** The
   page says they apply when filtering on non-key columns with a localised distribution and that they can add
   overhead: if even one matching value is in a block, the whole block is read. They work best when the indexed
   column correlates with the ordering key.
2. **Test on real data and measure index size against granularity.** Try index types and granularities with
   realistic queries; a finer granularity filters more but costs index size.
