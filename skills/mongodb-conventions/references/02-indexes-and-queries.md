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
4. **The first key of the index should appear in the filter or the sort.** The MongoDB agent skills state this
   as a compound index guideline; it was not checked on a manual page.

```javascript
db.orders.createIndex({ status: 1, createdAt: -1, total: 1 });
db.orders.find({ status: "open", total: { $gt: 100 } }).sort({ createdAt: -1 });
```

## 2.2 Sort and collation
1. **Sort on an index key or index prefix, or the server sorts in memory.** If the sort keys match the index
   keys or a prefix of them, the index supplies the order. An index on one field serves the ascending sort and,
   by reverse traversal, the descending one.
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
3. **Index only for queries that run.** Every extra index slows writes and uses memory; confirm with the plan
   that the index is chosen (own guidance).

```javascript
db.movies.find({ rated: "PG", title: /^T/ }, { title: 1, _id: 0 });
```
