# clickhouse-conventions: origin and source stamps

> Provenance of `skills/clickhouse-conventions`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No ClickHouse server was used while
writing it. A new engine block with no same-topic block. Overlaps with `skills/sql-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| ClickHouse documentation, markdown view of the pages: choosing a primary key, choosing a partitioning key, select data types, `LowCardinality(T)` | Licence of the rendered pages not re-read in this pass: facts only, nothing copied | Ordering key defined at creation, projections as the only added ordering, filter-first ordering, partition as data management, low-cardinality partition key and the too-many-parts error, Nullable overhead, LowCardinality thresholds, narrow numeric types |
| ClickHouse documentation: selecting an insert strategy, asynchronous inserts | Same: facts only | Batch sizes, one insert per second, retry with identical batches, `async_insert` and `wait_for_async_insert` semantics, flush conditions and defaults, flush-time rejection |
| ClickHouse documentation: avoid mutations, `ALTER TABLE ... UPDATE`, `DELETE` (lightweight), `ReplacingMergeTree`, avoid `OPTIMIZE FINAL`, use data skipping indices where appropriate | Same: facts only | Mutation rewrite cost and behaviour, key-column update limit, lightweight delete behaviour and settings, deduplication only on merge, `OPTIMIZE FINAL` effects, `FINAL` in queries, skipping-index limits |
| ClickHouse/agent-skills, best-practices rules `schema-pk-cardinality-order`, `schema-pk-filter-on-orderby`, `schema-types-lowcardinality` (LICENSE re-read, Apache-2.0), commit `356a8c1` of 2026-09-28 | Apache-2.0 | Low-to-high cardinality ordering statement and the leading-prefix claim (both stated in the text as the agent skills' claims) |

## Re-read 2026-10-20 (verification pass)
Every ClickHouse page of the table above was opened again on that day (facts only; the pages' licence was
not read; read through a fetch tool that summarises), plus the `LowCardinality` type page and the
`ReplacingMergeTree` and lightweight `DELETE` reference pages. Confirmed point by point: ordering key fixed at
creation and projections as the only added ordering, the filter-first and correlation rules with four or five keys,
the low-cardinality-first example (an 8-valued type column), the `EXPLAIN indexes = 1` check and the full-scan
cost of `ORDER BY tuple()` (about 59.8 million rows read against about 197 thousand with a key); partitioning as
data management, no merge across partitions, fewer than about 100 to 1,000 values, start without partitioning;
Nullable's separate mask column, the 10,000 and 100,000 distinct-value statements of the `LowCardinality`
page (which also advises it over `Enum` for strings), the narrow numeric example; batch sizes and one insert
per second, async insert pair and fire-and-forget risks, flush defaults (100 MiB, 200 ms or 1,000 ms on
Cloud, 450 queries; the page also says the timeout adapts since 24.2), flush-time rejection of the whole query,
no visibility before the flush; the mutation rewrite cost, persistence through restarts, monitoring and the
alternatives; `OPTIMIZE FINAL` and the 150 GB limit and `FINAL` in queries; the skipping-index conditions;
lightweight delete's hidden mask, merge-time removal, sync setting and forced-merge setting, and no stated
version. Additions: 2.1.3 (idempotent retry), 3.2.2 (compact parts), 3.2.3 (version and deleted-flag columns).
No correction was needed; the claim on the agent skills' leading-prefix wording stays flagged below.
## Removed in the verification pass (no page supporting them)
Version numbers for lightweight `DELETE` (23.3 and 25.7 in the earlier review): the page read states no
version, so the rule tells the reader to check the server. "`ORDER BY` is effectively immutable" narrowed to
what the page says (the key must be defined at creation and cannot be added; projections add orderings). "Avoid
`FINAL`" narrowed to `OPTIMIZE ... FINAL`: the documentation says `FINAL` in a query is sometimes needed and is
fine when the query filters on the key columns. The "avoid Nullable columns" page of the best-practices set was
not reachable (404 on the markdown view), so the rule rests on the select-data-types page.

## Not verified
1. **Own guidance (unchanged on 2026-10-20):** none beyond the order in which rules are applied; the numbers (1,000, 10,000 to 100,000,
   one insert per second, fewer than 100 to 1,000 partitions, 10,000 distinct values) are the documentation's.
2. **Versions:** the documentation read was current on 2026-10-08 and does not tie these rules to server
   versions; the `ALTER ... MODIFY ORDER BY` restrictions, projections and materialised views were not read.
3. **Skipping prefix key columns prevents index use** is the agent skills' wording and is likely stronger than
   the engine's behaviour; it is flagged in the text, not relied on.
4. **ClickHouse Cloud defaults** (for example the 1,000 ms async flush timeout) are quoted as the page gives
   them and not checked on a self-managed server.

## Related blocks
`data-pipeline-conventions`, `sql-server-tsql-types-and-queries`, `mysql-pitfalls`, `mongodb-conventions`.
Independent verification 2026-10-21: 28 checked, 28 matched, 0 corrected, 0 unverified (ClickHouse docs; the agent-skills pin 356a8c1 is older than the head of that day, 69a8354, the text is valid for the pin)
