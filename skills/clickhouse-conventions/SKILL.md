---
name: clickhouse-conventions
description: "Use when designing or reviewing a ClickHouse MergeTree table or the code that writes to it: choosing ORDER BY (the ordering key), PARTITION BY and its cardinality, avoiding Nullable, LowCardinality and narrow numeric types, batch size and async_insert for inserts, the too-many-parts error, why ALTER TABLE UPDATE and DELETE mutations hurt, lightweight DELETE, ReplacingMergeTree duplicates, OPTIMIZE FINAL, and data skipping indexes."
---

# clickhouse-conventions

Step 6 of the pipeline (`WORKFLOW.md`), for ClickHouse tables and the writers that feed them. The premise:
**ClickHouse is built for large, immutable, sorted parts, so the ordering key is fixed at creation, every insert
makes a part, and every update rewrites parts**. A habit from a row-oriented database (a surrogate key first, a
row per insert, an update in place) works against the engine instead of failing loudly.

## When
- A MergeTree table is created, or its `ORDER BY`, `PARTITION BY` or column types are chosen.
- An application inserts rows, often in small batches, or the server reports "too many parts".
- Rows must be corrected, deduplicated or deleted.
- A query is slow and a skipping index, `FINAL` or `OPTIMIZE` is proposed.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Schema: ordering key, partitioning, Nullable, LowCardinality, numeric width | a table is created or its key, partition or types change | [`01-schema.md`](./references/01-schema.md) |
| 2 | Inserts: batch size, async inserts, retries | a writer is built, or "too many parts" appears | [`02-inserts.md`](./references/02-inserts.md) |
| 3 | Mutations and merges: updates, deletes, ReplacingMergeTree, OPTIMIZE FINAL, skipping indexes | rows must change or disappear, or a query is tuned | [`03-mutations-and-merges.md`](./references/03-mutations-and-merges.md) |

## Output / checkpoint
Each rule was exercised on the target server version: the ordering key was chosen from the real `WHERE` clauses
and the rows read were compared with `EXPLAIN indexes = 1` (§1.1), a load test inserted at the intended rate
and the part count stayed bounded (§2.1), and a delete or correction path was run and observed in
`system.mutations` (§3.1). A rule checked by reading documentation only is not verified.

## Guardrails
- Never create a MergeTree table without deciding the ordering key from the queries; `ORDER BY tuple()` means
  full scans (§1.1).
- Never use a high-cardinality partition key, and never partition to speed up queries (§1.2).
- Never insert row by row; batch on the client or use asynchronous inserts that wait for the flush (§2.1, §2.2).
- Never run frequent `ALTER TABLE ... UPDATE` or `DELETE` as part of normal writes (§3.1).
- Never schedule `OPTIMIZE ... FINAL` (§3.3).
- Versions: each rule names its version where one is stated; the documentation read was current at 2026-10-08.
  Nothing was run while writing this block.

## Origin
Rewritten from the ClickHouse documentation (facts only, no text copied) and the ClickHouse agent skills
(Apache-2.0), read 2026-10-08. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md). A new engine block with no same-topic block on main; it is
meant to sit beside the general SQL conventions block (`sql-conventions`), which exists only on the unmerged
branch `feat/antislop-lot` (PR 118), and to be linked from it when PR 118 lands. Pipeline-level ingestion
design is in `data-pipeline-conventions`.
