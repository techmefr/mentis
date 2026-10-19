---
name: mongodb-conventions
description: "Use when designing or reviewing a MongoDB schema, query or aggregation pipeline: choosing between embedding and referencing, unbounded arrays and the 16 MiB document limit, $jsonSchema validation levels and actions, a schemaVersion field for gradual migrations, compound index key order (equality, sort, range), index collation, covered queries and the _id projection, $lookup performance, $project placement, and memory limits that spill pipeline stages to disk."
---

# mongodb-conventions

Step 6 of the pipeline (`WORKFLOW.md`), for MongoDB application code and schema. The premise: **a flexible
schema moves the contract from the database to the application, so the contract has to be written down
(validation, a version field, bounded arrays) and the indexes have to be shaped by the queries, not by the
fields**. SQL-engine rules for the same ideas are in `sql-server-tsql-types-and-queries`,
`mysql-pitfalls` and the ORM blocks (`jpa-hibernate-pitfalls`, `prisma-ops-and-test-hygiene`).

## When
- A collection or document shape is designed or changed.
- A query is slow, an index is added, or a sort or aggregation reports memory or disk use.
- Data from two collections is combined with `$lookup`, or an array field is allowed to grow.
- A validation rule or a new field version is introduced on a live collection.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Schema: embed or reference, bounded arrays, validation, schema versions | a document shape, a relationship or a validation rule changes | [`01-schema.md`](./references/01-schema.md) |
| 2 | Indexes and queries: compound key order, collation, sort, covered queries | an index is added, or a query scans, sorts in memory or should be covered | [`02-indexes-and-queries.md`](./references/02-indexes-and-queries.md) |
| 3 | Aggregation: `$lookup`, `$project` placement, `$match` position, disk use | a pipeline is written or is slow | [`03-aggregation.md`](./references/03-aggregation.md) |

## Output / checkpoint
Each rule was exercised on the target server version: the winning plan of the query was read with `explain`
before and after (§2.1), a validator was tried with an invalid document at each action level (§1.3), and an
array's growth was bounded by a test that inserts past the intended limit (§1.2). A rule checked by reading
documentation only is not verified.

## Guardrails
- Never let an array grow without a stated bound (§1.2).
- Never switch a populated collection to rejecting writes before the logged violations have been read (§1.3).
- Never reorder compound index keys by habit: equality, then sort, then range, unless the range is the
  selective part (§2.1).
- Never assume a projection of indexed fields covers a query: the `_id` field is included unless excluded (§2.3).
- Versions: each rule names the MongoDB version it needs; the manual read is the current one, with 6.0 as the
  version where pipeline stages began spilling to disk by default. Nothing was run while writing this block.
- Operational concerns (backups, sharding, access control) are outside this block; `security-hardening` covers
  injection through operators.

## Origin
Rewritten from the MongoDB manual (facts only, no text copied) and from the MongoDB agent skills (Apache-2.0),
read 2026-10-08. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md). A new engine block with no same-topic block. Overlaps with `skills/sql-conventions` (2026-10-19); cross-referenced, not merged.
