# kafka-delivery-semantics-pitfalls §4 — Compaction, tombstones and what a consumer can miss

Sources: the Apache Kafka documentation, "Design" page of the 4.3 documentation (apache/kafka-site at e6cbeb5, `content/en/43/design/design.md`, section "Log Compaction" and its sub-sections), read 2026-10-15.

## 4.1 What compaction keeps
1. **Compaction keeps at least the last known value for each message key in a partition.** It suits the log of changes to keyed, mutable data (the page's examples: database change subscription, event sourcing, journaling), where time-based retention would lose the current state.
2. **The retention policy is per topic,** so one cluster mixes topics retained by size or time with compacted ones. The page names `log.cleanup.policy=compact` for enabling cleaning and describes it as a broker setting that affects all topics without an override.
3. **Ordering is kept and offsets never change.** Compaction never reorders messages, and a compacted-away offset stays a valid position that reads like the next highest offset.
4. **A consumer that stays within the head of the log sees every message.** `min.compaction.lag.ms` is a lower bound on how long a message stays uncompacted, and `max.compaction.lag.ms` an upper bound on the delay before it becomes eligible. The page adds that the maximum is not a hard guarantee, since it depends on cleaner threads being available.
5. **The active segment is never compacted,** even if all its messages are older than the minimum lag.

## 4.2 Deletes
1. **A record with a key and a null value is a delete marker (tombstone).** It causes prior records with that key to be removed, and is itself cleaned out of the log after a period.
2. **A consumer can miss a tombstone.** The delete markers are guaranteed to be seen only if the consumer reaches the head of the log in less than `delete.retention.ms` (default 24 hours in the page). Since removal happens concurrently with reads, a consumer that lags by more can miss them and keep a deleted record.
3. **The configuration reference confirms the bound**: `delete.retention.ms` (default one day) also limits how long a
   consumer that starts reading from offset 0 has to finish a complete scan, so a slow rebuild can miss
   tombstones. A log is cleaned only once more than half of it is duplicate data (`min.cleanable.dirty.ratio`
   0.5), so a compacted topic holds old values for a long time; do not read the topic as if it were already
   compacted. `cleanup.policy` can combine `compact` and `delete`, and an empty list keeps data forever. Own
   guidance on top: a consumer that rebuilds state from a compacted topic and may lag for longer than the delete retention should rebuild from the start rather than trust its stored state.

## 4.3 Monitoring
1. **The page tells operators to monitor** the `uncleanable-partitions-count`, `max-clean-time-secs` and `max-compaction-delay-secs` metrics when relying on the maximum compaction lag.

## 4.4 Checks (own guidance)
1. Every record written to a compacted topic has a key; a record without a key has no place in one.
2. The delete retention is longer than the longest time a consumer can be down.
