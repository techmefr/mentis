# § 2 — Kafka

> Section 2 of `skills/messaging-conventions`. Read it when the broker is Kafka. Defaults below are those of the
> client source read on 2026-10-02 (the main branch); older clients had different ones, and several pieces of
> advice written for them are now wrong. Check the version of the client and of the broker in use.

1. **A committed message is one every in-sync replica has.** The producer's acknowledgement setting says how long
   it waits: none, the leader only, or all in-sync replicas. With the leader only, a leader that fails right after
   acknowledging loses the record. Use the "all" setting for anything you cannot lose; in the client source read it
   is the default, but write it explicitly so a change of default or a copied configuration cannot weaken it.
2. **"All" is only as strong as the minimum in-sync size.** The "all" acknowledgement means all replicas currently
   in sync, which can be just the leader if the others have fallen out. Set the topic's minimum in-sync-replica
   count (for a replication factor of three, the usual choice is two) so a write is refused rather than accepted
   on a single copy, and accept that writes then stop when too few replicas are in sync. That is the documented
   trade between consistency and availability. Also leave unclean leader election off (the default since 0.11) so
   an out-of-date replica never becomes leader; turn it on only for data where staying up beats being complete.
3. **Turn idempotence on, and don't fight it.** The idempotent producer attaches a producer id and a sequence
   number so the broker discards a retried duplicate and preserves order across retries. It requires the "all"
   acknowledgement, retries above zero, and no more than five requests in flight per connection; it is enabled by
   default in the client read when no conflicting setting is present, and silently disabled if a conflicting one
   is set without enabling it explicitly. Enable it explicitly so a conflict raises an error instead of
   quietly dropping the protection.
4. **Control retries with the delivery timeout, not a retry count.** The client documents that users should leave
   the retry count alone and bound the whole send with the delivery timeout. Without idempotence, retries with more
   than one request in flight can reorder records; with it they cannot.
5. **Ordering is per partition, and the key picks the partition.** The producer hashes the key to a partition, so
   all records for one entity (a user, an order) with the same key arrive in order at the same consumer. Choose a
   key that matches the unit that needs ordering and spreads load; a key with a few hot values creates a hot
   partition. Changing the partition count later changes where keys land, so records for one key can end up split
   across partitions over the change; decide the count with growth in mind.
6. **Commit the offset after processing, and turn off the background auto-commit when correctness depends on it.**
   The consumer's position is the record of what is done. Committing before processing is at most once; after is
   at least once. The auto-commit default is on and commits periodically in the background, independent of
   whether your processing finished, so for a flow that must not lose work, commit manually after the work has been
   recorded (and design the handler to be idempotent, §1.3). Commit the offset of the next record to read (the last
   processed offset plus one), which the consumer's own documentation requires.
7. **Keep the poll loop alive.** A consumer that does not call poll again within the maximum poll interval is
   removed from the group and its partitions are reassigned, causing duplicate processing and a rebalance. Bound
   the work done per poll (the batch size) so it fits, or hand long work to another thread while still polling and
   pausing partitions, and handle the callback for revoked partitions by committing what is done.
8. **Choose where a new consumer group starts, deliberately.** With no committed offset, the reset policy decides:
   from the beginning, from the end, or fail. "From the end" silently skips everything produced before the first
   start; "from the beginning" may replay a very large history. State the choice for each group, and use failure
   where neither is acceptable.
9. **Exactly once across topics uses transactions, and the reader must read committed.** A transactional producer
   can write output records and the consumer's offsets atomically; a consumer must use the read-committed
   isolation level, because the default (read uncommitted) also returns records of aborted transactions. In
   read-committed mode a consumer reads only up to the last stable offset, so one long-open transaction holds back
   everything after it. Use one producer instance per consumer instance for the transactional case. Writing to an
   external system is outside this guarantee (§1.4). The streams library applies the pattern for you.
10. **Dead-letter handling is yours to build.** The broker has no built-in dead-letter queue for a consumer
    group: a failing record either blocks the partition (retrying forever) or is skipped. Decide per error class:
    retry in place a bounded number of times, then publish the record with its error to a retry or dead-letter topic
    and commit past it, so one bad record does not stall the partition (`background-jobs-conventions` §2).
11. **Compaction keeps the last value per key, not a history.** A compacted topic suits changelogs and current
    state; a record with a null value (a tombstone) marks a key for deletion. Do not use a compacted topic where
    each record is an event that must be seen.
12. **Secure and size it.** Require authentication and TLS, give each application its own principal with
    permission only on its topics and groups, and set retention from the replay window you need and the storage you
    have (watch consumer lag, in time as well as in offsets: `skills/observability-instrumentation` §3).

**Sources:** the Kafka design documentation (message delivery semantics, transactions, replication, availability
and durability, unclean election, partitioning by key, consumer position) and the producer and consumer
configuration source of the main branch (acks, idempotence and its requirements, in-flight limit, retries and the
delivery timeout, auto-commit, offset reset, isolation level), Apache-2.0, read 2026-10-02. Point 7 follows the shared client
configuration's poll-interval description. Points 5 (partition change), 7 (the pause advice), 10 (design) and 12
are reasoning of ours; the usual replication-three/minimum-two choice in point 2 is
common practice, not a documented requirement.
