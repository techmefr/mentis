# mysql-pitfalls §1 — JSON, collation and index key length

Rules hold for MySQL 8.4 (the manual read) with InnoDB and the `DYNAMIC` row format, unless a rule names
another version or format.

## 1.1 JSON operators and indexes
1. **`->` returns a JSON value, so a string comes back quoted and with its escapes.** `column->path` is a
   synonym for `JSON_EXTRACT(column, path)`. The inline operator `->>` returns the unquoted value (it is
   `JSON_UNQUOTE(JSON_EXTRACT(...))`). Use `->>` when the target is text.
2. **Cast before comparing with native types.** `CAST(json AS type)` succeeds only when the JSON is a single
   scalar of that type; otherwise it returns `NULL` with a warning. `BETWEEN`, `IN()`, `GREATEST()` and
   `LEAST()` are not supported with JSON values: the manual's workaround is to cast to a native numeric or
   string type first.
3. **JSON string comparison is case-sensitive.** The manual says JSON strings order like SQL strings with the
   binary collation `utf8mb4_bin`, so comparison is case-sensitive.
4. **A JSON column is not indexed directly.** Create an index on a generated column that extracts one scalar,
   or, for arrays, a multi-valued index (InnoDB): `CAST(... AS ... ARRAY)` in the index definition, queried with
   `MEMBER OF()`, `JSON_CONTAINS()` or `JSON_OVERLAPS()`. Check the plan with `EXPLAIN`; an index that the
   predicate shape cannot use is dead weight.
5. **A functional index over `->>` needs the collation the operator returns.** `JSON_UNQUOTE()`, and so `->>`,
   returns `utf8mb4_bin`, while `CAST(... AS CHAR(n))` returns the server default collation. An index on
   `CAST(data->>'$.name' AS CHAR(30))` is then not used by `WHERE data->>'$.name' = 'James'`; the manual's fix
   is to index `CAST(data->>'$.name' AS CHAR(30)) COLLATE utf8mb4_bin`, which also makes the match case-sensitive.
6. **The size of a JSON document is capped by `max_allowed_packet`.** Storage is roughly that of `LONGBLOB` or
   `LONGTEXT`; keep documents that are read whole small, and keep large blobs out of JSON.

```sql
ALTER TABLE customers
  ADD COLUMN zip INT UNSIGNED GENERATED ALWAYS AS (CAST(profile->>'$.zip' AS UNSIGNED)) VIRTUAL,
  ADD INDEX idx_zip (zip);
```

## 1.2 Index key length and utf8mb4
1. **The InnoDB index key limit is 3,072 bytes for `DYNAMIC` and `COMPRESSED` rows and 767 bytes for
   `REDUNDANT` and `COMPACT`.** A smaller page size lowers it proportionally (1,536 bytes at 8 KB, 768 bytes at
   4 KB). The same limit applies to full-column index keys, and exceeding it is an error.
2. **`utf8mb4` uses up to 4 bytes per character,** so a `VARCHAR(255)` key can be up to 1,020 bytes and the
   767-byte limit is reached at 191 characters. A key of a few long columns together can exceed 3,072 bytes
   even on `DYNAMIC` rows.
3. **Index a prefix when the full value is not needed.** `INDEX (col(N))` gives a prefix length in characters
   for non-binary string types (bytes for binary types); the limit is measured in bytes. Prefixes are required
   for `BLOB` and `TEXT` key parts. Choose a prefix long enough to separate values, then verify the plan.
4. **Prefer a shorter column or a hash or normalised helper column over a long key.** Own guidance: the
   manual states the limits but not this alternative.

## 1.3 Collation and string comparison
1. **The default collation is `utf8mb4_0900_ai_ci`, so non-binary comparisons are case-insensitive by
   default.** `col LIKE 'a%'` matches `A` and `a`. For a case-sensitive comparison make one operand use a
   case-sensitive or binary collation with `COLLATE`.
2. **A binary string is case-sensitive; convert it to compare without case.** Use `CONVERT(x USING utf8mb4)`
   with a case-insensitive `COLLATE`.
3. **Check what a comparison uses with `COLLATION()`.** The manual uses it to show that a function result such
   as `VERSION()` carries a case-insensitive collation, so comparisons with it are case-insensitive.
