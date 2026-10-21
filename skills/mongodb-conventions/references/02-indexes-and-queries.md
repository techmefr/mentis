# mongodb-conventions §2 — Indexes and queries

Rules hold for the current MongoDB manual (read 2026-10-08). Read the winning plan with `explain` before and
after each change.

## 2.1 Compound index key order
1. **Order keys equality, sort, range (ESR).** The ESR guideline says equality fields go first, which keeps the
   remaining keys in sorted order, and that sort fields before range fields avoid an in-memory sort.
2. **Put a very selective range before the sort when that matters more (ERS).** The guideline says that if the
   range predicate is very selective it can go before the sort fields.
3. **Treat `$in` with fewer than 201 elements as equality.** The manual says such an `$in` is expanded and
   merged in index order, so it behaves like an equality predicate; larger lists behave like a range.
4. **The first key of the index should appear in the filter or the sort.** Stated as a compound index
   guideline in the MongoDB agent skills' indexing reference (Apache-2.0, re-read 2026-10-20), which also
   gives ESR as the most often preferred order, the ERS exception when equality is weakly selective and the
   range strongly so, and 200 or fewer `$in` elements as equality.

```javascript
db.orders.createIndex({ status: 1, createdAt: -1, total: 1 });
db.orders.find({ status: "open", total: { $gt: 100 } }).sort({ createdAt: -1 });
```

## 2.2 Sort and collation
1. **Sort on an index key or index prefix, or the server sorts in memory.** If the sort keys match the index
   keys or a prefix of them, the index supplies the order. An index on one field serves the ascending sort and,
   by reverse traversal, the descending one. On a compound index the exact reverse also works, but a mixed
   direction such as ascending on one key and descending on the next needs an index with that exact pattern
   (agent skills' indexing reference, re-read 2026-10-20).
2. **A sort on a multikey-indexed array field adds an in-memory sort stage** unless the stated boundary
   conditions hold, so check the plan.
3. **The query's collation must match the index's.** To use an index for string comparison, the operation must
   specify the same collation; with a different one the index cannot support string comparisons on the indexed
   fields. Collation-aware index keys can also be larger, and text and 2d indexes do not support collation.

## 2.3 Covered queries
1. **A query is covered when all fields in the query and all returned fields are in one index and no field in
   the query is compared to null.** Such a query reads no documents.
2. **Exclude `_id` explicitly.** Unless `_id` is part of the index the projection must say `_id: 0`; a
   projection of indexed fields alone still returns `_id` and the query is not covered.
3. **Index only for queries that run.** Every extra index slows writes and uses cache memory; the agent
   skills' unnecessary-indexes reference (re-read 2026-10-20) says to read the per-index operation counts, hide
   an index before dropping it and watch performance, and to treat a single-field index as redundant when a
   compound index starts with the same field. Keep indexes for planned queries on new collections, rare critical
   jobs and lifecycle (TTL) indexes. Confirm with the plan that the index is chosen.
4. **What a covered query also needs.** All returned and sort fields must be in the index, the projection must
   be an inclusion projection of indexed fields, and a test for existence or for a null or missing value
   usually defeats coverage. A multikey index can cover a query only when the array field is not returned and
   no element-match operator is used (same reference).

```javascript
db.movies.find({ rated: "PG", title: /^T/ }, { title: 1, _id: 0 });
```
