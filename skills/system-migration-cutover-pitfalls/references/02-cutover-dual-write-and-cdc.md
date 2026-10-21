# system-migration-cutover-pitfalls §2 — Cutover, dual write and change data capture

> Part 2 of `skills/system-migration-cutover-pitfalls`. Read it when the old and the new system must stay in step
> or the switch is being scheduled. Facts about log-based capture come from the Debezium documentation (features,
> architecture, outbox event router, PostgreSQL connector; Apache-2.0, repository commit `8d6ccc1`), read
> 2026-10-20. Behaviour differs per database and per connector: re-read the page for yours. Sentences marked "own
> guidance" are ours.

1. **Pick the cutover strategy by tolerance, not habit.** Big bang with a freeze: simplest to reason about, longest
   outage, one rollback. Phased by tenant, region or entity type: each step is small and reversible, but the
   systems coexist longer. Parallel run (both process the same input and the outputs are compared before the
   switch): the strongest proof, the highest cost, and the old system must not act on external effects twice.
   Own guidance: choose by how long you can be down and how long you can tolerate two truths.
2. **Application dual write is the weakest way to keep two stores in step.** Two writes are not one transaction:
   the second can fail, the two can interleave differently under concurrency, and the stores drift with no
   alarm. The CDC documentation lists dual writes next to polling as the approaches that log-based capture
   improves on. Fix, in order of preference: one system of record that the other follows through its log or an
   outbox; or, if the application must write both, one is designated master, the other is repaired by a compare
   job, and failures of the second write are recorded, not swallowed (own guidance).
3. **Name one system of record at every moment, and one direction of copy.** Bidirectional sync needs a conflict
   rule decided in advance (last writer by time, source priority, merge by field) and a loop breaker so a change
   copied one way is not copied back. Own guidance: avoid it; if the rollback needs the reverse direction, build
   it as a separate, time-boxed path rather than a symmetric one.
4. **Log-based capture reads what the database already wrote.** Benefits the source states: it captures every
   change including deletes, with a delay measured in milliseconds for the main open-source databases, no polling
   load, no change to the data model (no "last updated" column), and optionally the old row state and transaction
   metadata, depending on the database's settings. Cost: an operated component, database-side configuration and
   privileges (use a dedicated replication user, not a superuser), and the problems in rules 5 to 9.
5. **A snapshot then a stream, from a recorded position.** On first start the connector takes a consistent snapshot
   of current rows and then continues from the log position it read when the snapshot began, so nothing between
   them is missed. If it stops during the snapshot, it starts the snapshot again. After the snapshot, a restart
   resumes from the saved offset. Snapshot rows are emitted as read events, not as inserts: the target must treat
   them as upserts. The snapshot mode is a setting; one that skips the snapshot is safe only when the log still
   holds all the data of interest.
6. **Backfill while streaming uses incremental snapshots.** A chunked, signalled snapshot can run beside the live
   stream, using watermarks to reconcile a chunk with changes that arrive meanwhile; it can be triggered and
   stopped at run time, restricted by a condition, and, for the read-only variant, run without a signal table.
   The PostgreSQL documentation warns that schema changes are not supported while one runs: freeze the schema
   for its duration. Re-reading a window can emit duplicates; this is consistent with rule 7.
7. **Delivery is at least once, so the apply side is idempotent.** After a crash the same change events can be
   delivered again. Apply by primary key with an upsert, or compare the position or version before applying, so a
   repeat changes nothing. Ordering is guaranteed within a key and a partition; the documentation notes that a
   table-truncate event has no key, so across partitions there is no ordering between it and row events. Own
   guidance: use one partition per ordered stream during a cutover, or accept and design for reordering.
8. **Table shape decides what you receive.** In PostgreSQL's default replica identity, update and delete events
   carry only the primary key of the old row; a table with no primary key emits only creates for new rows and no
   updates or deletes (change the table or its replica identity). Changing a primary key arrives as a delete and a
   create, with headers linking the two, and a delete is followed by a tombstone with a null value so a compacted
   topic can drop the key. Large values stored out of line and unchanged are left out of an update message unless
   they are part of the identity, so an apply that writes the missing field as null destroys data: apply only the
   columns present (own guidance for the apply side). Check each table for these before relying on the stream.
9. **An unconsumed replication slot fills the source's disk.** The database must keep the log for a slot whatever
   the consumer does, so a stopped or slow connector makes log files accumulate until the disk is full. The
   documentation tells you to monitor slot lag and size, and to cap retained log size where the database allows it.
   Own guidance: alert on slot lag before cutover week, and drop the slot as part of the decommission checklist,
   not whenever somebody notices.
10. **Measure lag, and cut over only at near zero and reconciled.** Compare the source timestamp and the processing
    timestamp in each event for lag; lag spikes at snapshot time, on a bulk update and after a pause. The
    cutover step is: stop writes to the old system (freeze), let the stream drain to zero lag, run the final
    reconciliation (part 1, rule 7), switch writers, keep the old system read-only (own guidance).
11. **Events: write them with the change.** If the new system must publish events, write the event row in the same
    transaction as the state change (an outbox) and let the capture component route it. The outbox router in the
    documentation takes the event key from a chosen column to keep the order inside a partition, can place chosen
    columns in the message, ignores deletes on the outbox table so that cleaning it up does not emit events, and
    leaves the event id for consumers to deduplicate. Cross-link `skills/nestjs-reliability` §3 and
    `skills/webhook-contract-and-delivery-pitfalls`.
12. **Move reads before writes, with a comparison.** Own guidance: shadow reads (serve from the old system, query
    the new one in the background, log differences) find mapping defects with no user impact; then switch reads
    per tenant behind a flag; switch writes last, per tenant. A difference rate that does not fall is a mapping
    defect, not noise.
13. **Decommission is a checklist, after a quiet period.** Keep the old system read-only for a period set by
    policy, then archive what retention requires, drop the replication slot and the connector, revoke the
    credentials, stop scheduled jobs on the old system (so nothing sends twice), remove old DNS and redirects when
    traffic is gone, and record where the final backup is. Own guidance: never delete the source on the day of the
    switch; the rollback plan from part 1, rule 8 needs it.
14. **External references outlive the cutover.** Links in sent emails, ids quoted by customers, third-party
    webhooks and API keys that point to the old system: keep redirects and the id mapping from part 1, rule 3, and
    announce changes to partners in advance.
