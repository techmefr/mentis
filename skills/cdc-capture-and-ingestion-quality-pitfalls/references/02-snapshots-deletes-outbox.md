# cdc-capture-and-ingestion-quality-pitfalls §2 — Snapshots, deletes, keys and the outbox

Sources: the incremental-snapshot concept page, the event-flattening transformation page and the outbox event router and Quarkus outbox extension pages of the Debezium documentation at commit 8d6ccc1, read 2026-10-20. "Own guidance" marks craft knowledge.

## 2.1 Back-filling beside the live stream
1. **An initial snapshot postpones streaming; an incremental one runs next to it.** Debezium's supplementary snapshot reads a table in chunks, sorted by key, while change capture continues, and can be resumed after an interruption and repeated on demand (for example after adding a table to the include list). Symptom of the alternative (stop, copy, restart): a gap or a long outage. Fix: use the incremental method where the engine has it, and run it on a quiet hour (own guidance on timing).
2. **A snapshot row is a "read" event, not an insert.** Symptom: a consumer that handles only inserts, updates and deletes drops back-filled rows. Fix: map reads like inserts in the target merge.
3. **A change made during the snapshot may arrive before the snapshot's own copy of that row.** The page describes a buffer that resolves collisions between snapshot reads and streamed changes by key, so the final state is the logical one. Consumers should still merge by key with a source position, because their own ordering can differ (own guidance).
4. **The chunk size trades load against speed.** The page gives a default and says it is configurable; measure on your source rather than copying a value.
5. **Ask for the table list per run,** and record who started a snapshot and why (own guidance), because a snapshot reloads the targets.

## 2.2 Deletes and tombstones
1. **One delete in the source can become two messages,** a change event with the old row and a tombstone with the same key and an empty value (the flattening page). The tombstone marks the key for compaction on a log-compacted topic. Symptom: a consumer crashes on an empty value, or a warehouse row never disappears. Check: consume a delete on a test table and see both messages.
2. **Decide the delete representation for each target.** The flattening transformation can drop deletes, keep them, or rewrite them as a record with the old values plus a deleted marker field; it can also keep or drop tombstones. A warehouse that keeps history wants the marker; a cache wants the removal. Compaction behaviour is `skills/kafka-delivery-semantics-pitfalls`.
3. **Soft deletes in the source are updates, not deletes.** A "deleted at" column produces an update event; do not wait for a delete message (own guidance).
4. **Mapping a delete needs the key.** See §1.2: without the key the target cannot find the row.

## 2.3 Keys and ordering
1. **Order is per key, not global** (own guidance, standard for partitioned logs). Symptom: an update of one row before its insert, because two partitions were read independently. Fix: key events by the row's primary key so one row stays in one partition, and merge with the source position, not arrival time.
2. **A change of the key itself is a delete and an insert.** Symptom: the old row stays in the target. Check by changing a key in a test (own guidance).
3. **Record the source position and timestamp with each event** and keep them in the target for audit and for the lag measure (§3.1).

## 2.4 The outbox instead of capturing business tables
1. **Capturing business tables publishes how rows changed, not what happened.** Symptom: consumers depend on column names, and a refactoring of the source breaks them. The outbox pattern writes an event row in the same transaction as the business change and captures only that table, so the event and the data cannot disagree. The Debezium router transformation turns outbox rows into events; its page says a connector using it should capture the outbox table only, and that several outbox tables must share one structure.
2. **The Quarkus extension's page makes every event of one application share the same column types,** because they share one table (a build error otherwise). A general lesson: one outbox table, one shape.
3. **The event row carries an aggregate identifier, a type and a payload,** and the identifier becomes the message key so one entity's events stay ordered (the pattern; own guidance on the key choice).
4. **Clean the outbox table.** Captured rows are in the log and need not stay in the table (own guidance, as the page implies). Delete them after a delay longer than any consumer lag you accept.
5. **The consumer is still idempotent** (`skills/nestjs-reliability`, inbox side): the pattern gives at-least-once delivery, not exactly-once.
6. **A different engine has its own router.** The page notes the MongoDB connector needs a separate transformation.

## 2.5 Checks (own guidance)
1. Run a snapshot on a copy while writing to the table; compare the target with the source by key and count.
2. Delete, update the key, and update a large column in a test table; read all three event shapes.
