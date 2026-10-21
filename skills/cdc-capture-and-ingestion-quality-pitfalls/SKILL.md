---
name: cdc-capture-and-ingestion-quality-pitfalls
description: "Use when changes are streamed out of a database log into another system (change data capture), when a table is snapshotted or back-filled alongside live changes, or when ingested data is checked for quality: replication slots that hold the log, heartbeats on quiet databases, missing before-images and unchanged large values, deletes and tombstones, the outbox table instead of capturing business tables, keys and ordering, lag and reconciliation against the source, and validation suites that run on each batch."
---

# cdc-capture-and-ingestion-quality-pitfalls

A defensive block for pipelines fed from a database's change log rather than from queries. Premise: **a log-based
capture looks like a stream of rows but behaves like a contract with the source database: it pins disk, hides
values it did not need to log, replays after a restart, and reports a delete as two messages**. Generic pipeline
rules (idempotence, quality dimensions, raw layer) are `skills/data-pipeline-conventions` §1 and §2; contracts at
the producer boundary are `skills/data-contract-quality-rules-pitfalls`; delivery guarantees and compaction on
Kafka are `skills/kafka-delivery-semantics-pitfalls`; writing an event and its row in one step (outbox and inbox)
is `skills/nestjs-reliability`; keeping a search index in step with a database is `skills/search-index-sync-pitfalls`;
PostgreSQL server operation is `skills/postgres-operations-and-exposed-api-pitfalls`; a one-off move between
systems is outside this block.

## When
- A connector, an engine or a script reads a write-ahead or binary log to feed a warehouse, a cache, a search
  index or another service.
- The source database's disk grows, a replication slot lags, or a table was added and needs its history.
- Consumers see an update with missing columns, a delete they cannot key, or an old value after a new one.
- Data validation is added to ingestion, or a quality failure blocks a run nobody knows how to unblock.

## Steps

**Read only the section the task meets.** §1 is the entry point for a source-side incident.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Source-side setup and risks: slots and retained log, heartbeats, replica identity, large unchanged values, DDL, special values, snapshot restarts | a capture is set up, the source disk grows, or events lack columns | [`01-source-side.md`](./references/01-source-side.md) |
| 2 | Snapshots, deletes, keys and the outbox: incremental snapshot, collisions, tombstones, event shape, capturing an outbox table | history is back-filled, deletes are consumed, or a service publishes events | [`02-snapshots-deletes-outbox.md`](./references/02-snapshots-deletes-outbox.md) |
| 3 | Quality at ingestion: lag, reconciliation, batch validation suites, row conditions, failing rows, who is told | a pipeline gets checks, or a check fails | [`03-quality-at-ingestion.md`](./references/03-quality-at-ingestion.md) |

## Output / checkpoint
No pipeline checkpoint. A reviewed capture owes: for the source, what retains log and how that is watched (§1);
for each captured table, its key and what an update and a delete carry (§1, §2); how a back-fill runs next to live
changes (§2); the lag measure and a reconciliation of target against source (§3); and who is told when a check
fails and what unblocks it (§3).

## Guardrails
- Watch the retained log and the slot's lag on the source, and drop a slot you stop using. Never leave an idle
  slot, because the source keeps the log it would have sent (§1).
- Check what an update and a delete carry for each table before consumers rely on them. Never assume the old
  values or the key of a deleted row arrive (§1).
- Back-fill beside live capture with a method that resolves collisions. Never stop the stream, copy the table and
  hope nothing changed meanwhile (§2).
- Capture an outbox table for service events. Never publish an event by capturing business tables and reverse
  engineering intent from row changes (§2).
- Compare counts and keys against the source on a schedule. Never treat "no error" from the pipeline as proof of
  completeness (§3).
- Fail a batch or quarantine rows with a count and an owner. Never let a failed check pass quietly (§3).
- This block restates the Debezium and Great Expectations documentation at idea level plus marked own guidance;
  nothing was run. Defaults and numbers are not given (see [`references/origin.md`](./references/origin.md)).

## Origin
Rewritten from the Debezium documentation (Apache-2.0) and the Great Expectations documentation (Apache-2.0), read
2026-10-20, with own guidance marked in the references. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
