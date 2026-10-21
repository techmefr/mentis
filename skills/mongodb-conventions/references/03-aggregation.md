# mongodb-conventions §3 — Aggregation

Rules hold for the current MongoDB manual (read 2026-10-08). The disk-spill default needs MongoDB 6.0.

## 3.1 `$lookup` has a price
1. **Index the foreign field.** The agent skills' aggregation and excessive-lookups references (re-read
   2026-10-20) call it the most important `$lookup` optimisation, since each lookup runs a find on the joined
   collection, and suggest `explain("executionStats")` with the documents examined in the lookup stage. The manual says `$lookup` performance depends on whether the foreign field is
   indexed, and that unindexed or correlated-subquery lookups on large collections can slow down queries.
2. **Prefer an embedded model for data that is always read together.** The same page suggests it to cut
   reliance on `$lookup`; a pipeline with a lookup on the hot path is a design smell (§1.1).
3. **Pipeline-form `$lookup` uses an index only for comparisons with constants.** `$eq`, `$lt`, `$lte`, `$gt`
   and `$gte` inside `$expr` can use an index on the joined collection, but only between a field and a
   constant, and multikey, partial and sparse indexes are not used there.

## 3.2 Order and position of stages
1. **Put `$match` (and `$sort`) first so an index can be used.** An aggregation can use the input
   collection's indexes at the start of the pipeline; the optimizer also moves a `$match` filter that does not
   depend on a computed field ahead of projection stages, which lets it use an index on that field.
2. **Do not add `$project` early to "shrink" documents.** The manual says a `$project` at the start or middle
   of a pipeline to reduce fields is unlikely to help because the engine already does that, and that
   `$project` should typically be the last stage, used to choose the fields returned. Use it at the end.
3. **Put a limit right after a sort.** The agent skills' aggregation reference (Apache-2.0, re-read 2026-10-20)
   says the engine then keeps only the top N values instead of sorting everything, which uses far less memory.
4. **Read the optimised plan with `explain`.** Optimisations can change between releases, so inspect the
   plan rather than relying on a remembered rewrite.

## 3.3 Memory and disk
1. **Stages that need more than 100 MB of memory spill to temporary files by default** from MongoDB 6.0
   (`allowDiskUseByDefault`), unless the command sets `allowDiskUse: false`; a command can also set
   `allowDiskUse` itself to override the server setting either way. The Apache-2.0 agent skills say the same
   about spilling by default (`allowDiskUse` defaults to true) but give no version; the 6.0 start and the
   parameter name are unverified (2026-10-21).
2. **A spill is a signal.** The profiler and diagnostic logs include a `usedDisk` indicator when a stage wrote
   temporary files; treat repeated spills as a query or index to fix, not as normal.
3. **A sort that cannot use an index gets the same treatment.** Over 100 MB it also writes temporary files
   unless the query sets `allowDiskUse: false`; the fix is an index whose keys give the order (§2.2).
