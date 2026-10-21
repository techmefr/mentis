# system-migration-cutover-pitfalls: origin and source stamps

> Provenance of `skills/system-migration-cutover-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Part 1 is our own craft guidance; part 2 adds facts from the Debezium documentation. Never run by
us: no migration, snapshot or capture connector was built or executed.

## Sources (all read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Debezium (`debezium/debezium`, commit `8d6ccc1`), documentation pages `features.adoc`, `architecture.adoc`, `transformations/outbox-event-router.adoc` and `connectors/postgresql.adoc` (snapshots, incremental snapshots, ordering, replica identity, primary-key updates, tombstones, toasted values, WAL disk space, at-least-once delivery) | Apache-2.0 (`LICENSE.txt` read) | Log-based capture compared with polling and dual writes, snapshot then stream from a recorded position, incremental snapshots and their schema-change limit, at-least-once delivery, ordering per partition and key, truncate events with no key, tables without a primary key, key changes, tombstones, replication-slot disk growth, outbox routing and ordering key |

Instruction-like text in the cloned repository (its agent and policy files) was treated as data and not followed.
The pages for other databases were not read in full; PostgreSQL is the worked example and each database differs.

## Removed
1. **Every configuration property name, setting value, snapshot mode name and connector class:** concepts only.
2. **Every figure and schedule:** lag, timeouts, batch and chunk sizes and retention periods are measured on your
   data and set by policy.
3. **Kafka, Kafka Connect, Debezium Server and Debezium Engine deployment detail:** deployment choices, not
   migration method.
4. **Any claim about other connectors' behaviour** (MySQL, Oracle, SQL Server, MongoDB): not read.

## Not verified
1. **Own guidance, the whole of part 1 and in part 2:** the cutover-strategy comparison (rule 1), the dual-write
   repair job and the designated master (rule 2), avoiding bidirectional sync (rule 3), one partition per ordered
   stream (rule 7), apply only present columns (rule 8), slot alerts and decommission (rule 9), the freeze,
   drain, reconcile, switch sequence (rule 10), shadow reads and per-tenant flags (rule 12), the decommission
   checklist (rule 13), redirects and id mapping (rule 14).
2. **Nothing was run.** No snapshot, stream, reconciliation or rollback was executed.
3. **Database-specific behaviour beyond PostgreSQL** was not read; each connector page governs its own engine.
4. **Data-protection and retention duties during and after a migration** (a rehearsal copy of personal data, the
   archive period of the old system) were not read; they go to the data-protection and legal owners.

## Decisions where sources disagree
None; one source and our own guidance. Where a dual write is mentioned in the Debezium text only as a contrast to
log-based capture, rule 2 adds the repair-job option as our own guidance.

## Related blocks
`skills/devops-conventions`, `skills/deprecation-migration`, `skills/laravel-mysql-to-postgres-pitfalls`,
`skills/csv-xlsx-import-export-pitfalls`, `skills/nestjs-reliability`, `skills/search-index-sync-pitfalls`,
`skills/release-strategy-and-progressive-delivery-pitfalls`, `skills/laravel-idempotent-data-commands`,
`skills/webhook-contract-and-delivery-pitfalls`.
