# clickhouse-conventions §1 — Schema

Rules hold for the ClickHouse documentation current on 2026-10-08 (pages modified in mid-2026).

## 1.1 The ordering key
1. **Decide the ordering key (`ORDER BY`) from the queries, before the table exists.** The documentation says
   ordering keys must be defined at table creation and cannot be added later; extra orderings come only from
   projections, which duplicate data. Rewriting the key of a large table means a new table and a copy.
2. **Lead with the columns that filter out the most rows in the common `WHERE` clauses,** then columns
   correlated with other data, which compress and aggregate better. The page says four or five keys are
   typically enough and that the rules can conflict, so apply them in order.
3. **Within that, put low-cardinality columns before high-cardinality ones.** The documentation's example
   leads with an 8-valued type column and a date, not an identifier, and the ClickHouse agent skills state the
   rule as low to high so that the sparse index can skip whole blocks of rows.
4. **Filter on the leading key columns, and verify.** The documentation shows `EXPLAIN indexes = 1` listing the
   `PrimaryKey` condition and a drop in rows read once the query filters on the key; the ClickHouse agent
   skills add that skipping leading columns weakens the index, a claim not checked on a documentation page.
5. **`ORDER BY tuple()` is "no ordering key".** The documentation's example reads the whole table for a
   filtered count because of it.

```sql
CREATE TABLE posts (PostTypeId Enum('Question' = 1, 'Answer' = 2), CreationDate DateTime, Id Int32)
ENGINE = MergeTree
ORDER BY (PostTypeId, toDate(CreationDate));
```

## 1.2 Partitioning is lifecycle, not speed
1. **Partition for data management: retention, moving or dropping whole ranges.** The documentation says
   partitioning is primarily a data management technique, not a query optimisation tool; dropping a partition is
   a metadata operation that is much cheaper than row-level deletes, and it works with TTL and tiered storage.
2. **Choose a low-cardinality key, such as the month.** Parts are never merged across partitions, so a
   high-cardinality key makes many unmerged parts and eventually the "too many parts" error on inserts. The
   page says fewer than about 100 to 1,000 distinct values is usually optimal.
3. **Queries that span partitions can get slower.** More parts are scanned; understand the access pattern
   before relying on partition pruning. If unsure, start without partitioning and add it later for a stated
   lifecycle need (the page's own advice).

## 1.3 Types
1. **Avoid `Nullable` unless "null" must mean something other than empty.** A nullable column keeps a separate
   column for the null mask; the documentation says a default or zero-equivalent value usually suffices.
2. **Use `LowCardinality(String)` for columns with under about 10,000 distinct values.** The type page says
   dictionary encoding helps below 10,000 distinct values and can be worse than plain types above 100,000.
   Prefer it to `Enum` for strings, as the page suggests, unless the built-in validation of an `Enum` is wanted.
3. **Use the narrowest numeric type that fits the range,** for example an unsigned 16-bit integer where values
   are 0 to 65,535 and never negative (the data types page).
