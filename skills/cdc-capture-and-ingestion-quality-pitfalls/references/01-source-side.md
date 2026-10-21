# cdc-capture-and-ingestion-quality-pitfalls §1 — Source-side setup and risks

Sources: the PostgreSQL connector page of the Debezium documentation at commit 8d6ccc1, read 2026-10-20. Written for PostgreSQL logical decoding; the other engines have the same shape with different names, which were not read (own guidance). "Own guidance" marks craft knowledge.

## 1.1 The slot holds the log
1. **A replication slot makes the source keep the log until the reader confirms it.** Symptom: the source's disk fills although the data did not grow. Cause: the connector is stopped, slow or no longer wanted, and the slot still demands retention. Check: on the source, compare the slot's confirmed position with its restart position and the log size the slot pins (the connector page names both columns of the slot view). Fix: restart or fix the reader, or drop the slot you no longer use.
2. **Quiet tables behind busy databases starve the confirmation.** The page names two cases: many writes in the database but few in the captured tables, and several databases on one server where the busy one is not captured. The reader is not invoked, so it never confirms, and the shared log grows. Fix: enable the connector's periodic heartbeat, and where needed a regular small write to a heartbeat table added to the publication; the page says the heartbeat table must be in the publication or the heartbeat is not seen.
3. **An idle managed instance can also hide writes from clients on a schedule,** which the page says looks like the quiet-table case; regular events solve it. Re-read the provider's documentation (own guidance on generalising).
4. **A new connector creates its slot if it can; production setups usually create it by hand.** The page says both are possible. Decide who owns the slot and where its name is recorded (own guidance).
5. **Several connectors on one source need their own slots,** and each is its own retention risk. List them with their owners (own guidance).

## 1.2 What an event carries
1. **The old row image depends on the table's replica identity.** With the default setting an update carries only the key columns of the old row, and a delete carries only the key. Setting the table to full identity adds the entire old row, at the cost of more log per change. Symptom: a consumer needs "what changed" and gets only the new row, or a delete event cannot be matched. Check: read one real update and one real delete per table. Fix: choose the identity per table, deliberately.
2. **A table without a primary key cannot give a keyed delete unless its identity is full.** The page says a delete on such a table has no old image under the default or the "nothing" setting. Fix: add a key, or set full identity.
3. **Large values stored out of line are not repeated when unchanged.** The page says an update that did not touch them leaves them out and the connector emits a placeholder value you configure. Symptom: a long text or document column suddenly equals a placeholder string in the warehouse. Fix: treat the placeholder as "not changed" when merging, never as data (own guidance on the merge), or set full identity for that table.
4. **Generated columns may be missing with the common output plug-in** (the page states it). Check each generated column in the target.
5. **Special values need a decision.** Infinite dates and timestamps cannot be a normal date; the connector uses a structured form or a sentinel depending on the precision mode. Check what your target type does with it.
6. **Schema changes are not in the log stream for this engine** (the page lists DDL among the logical-decoding limits). Symptom: a new column appears in events before the target has it, or never. Fix: change the target first and the source second, and test the order on a staging copy (own guidance).

## 1.3 Commit, visibility and restarts
1. **Events can reach the consumer before the same data is readable on a replica.** The page warns that changes are published at commit and a consumer can be told about a row it cannot yet read through another connection. Fix: when the consumer looks the row up again, read from the primary or tolerate "not found, retry" (own guidance).
2. **After a crash the reader continues from its recorded position,** so events can be seen twice (the page says it records the position per event and resumes from there). Fix: the consumer is idempotent, keyed on the row key and a source sequence (`skills/kafka-delivery-semantics-pitfalls`).
3. **If the reader stops during its first snapshot, it takes a new snapshot at restart** (the page states it). Plan the snapshot's duration against the source's load and restart risk before starting.
4. **A starting position that is no longer in the log cannot be recovered by streaming.** The page notes a connector can only start from the log when you know the data of interest is still in it. Otherwise a snapshot is needed.

## 1.4 Checks (own guidance)
1. A table: source table, key, replica identity, large columns, generated columns, target key, merge rule, sample of an update and a delete event.
2. The source team can name the slots, their owners and the alert on retained log.
