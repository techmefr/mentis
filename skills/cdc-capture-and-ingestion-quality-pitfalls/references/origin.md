# cdc-capture-and-ingestion-quality-pitfalls: origin and source stamps

> Provenance of `skills/cdc-capture-and-ingestion-quality-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from project documentation and craft knowledge. No database, connector or
validation suite was set up or run while writing it.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| debezium/debezium at commit 8d6ccc1, `documentation/` pages: PostgreSQL connector (slot, retained log, heartbeats, replica identity, large values, special values, limits), incremental snapshot concept, event flattening, outbox event router and Quarkus outbox extension; LICENSE file read | Apache-2.0 (`LICENSE.txt`) | Source-side risks and settings at idea level, snapshot method, delete and tombstone handling, outbox pattern |
| great-expectations/great_expectations at commit 3be49de, `docs/docusaurus/docs/core/` pages: suites, row conditions, result format, validation definitions, checkpoints with actions, retrieving unexpected rows; LICENSE file read | Apache-2.0 (LICENSE file) | Batch and suite model, restricting a check to rows, result detail levels, actions on results |

## Left out on purpose
- Every configuration property name and default, chunk size, time-to-live, version and connector class.
- Other engines' connectors (MySQL, SQL Server, Oracle, MongoDB), schema history topics, Kafka Connect deployment,
  monitoring metrics and managed-database setup steps: not read or not used.
- Great Expectations code samples, the cloud product, data docs and the expectation gallery.
- The generic quality rules, already in `data-pipeline-conventions`.

## Not verified
1. **Behaviour was read, not run.** Replica identity effects, placeholder values, heartbeat requirements, tombstone
   handling and the failing-rows cap are the documentation's statements at the commits; re-read before relying.
2. **Debezium for engines other than PostgreSQL** was not read; §1 is explicitly PostgreSQL-shaped.
3. **Own guidance, not sourced** (marked in the text): per-key ordering, key changes as delete plus insert, clean-up
   of the outbox table, reconciliation schedules and credentials, alert design, batch design of suites, and all
   "Checks" lines.
4. **Agent instruction files:** the repositories were read only under their documentation folders; any agent
   instruction file they hold was not opened and nothing in it was followed.

## Related blocks
`data-pipeline-conventions`, `data-contract-quality-rules-pitfalls`, `kafka-delivery-semantics-pitfalls`,
`nestjs-reliability`, `search-index-sync-pitfalls`, `postgres-operations-and-exposed-api-pitfalls`,
`dbt-cli-and-model-versioning-pitfalls`, `source-freshness`.
