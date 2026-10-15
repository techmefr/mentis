# kafka-delivery-semantics-pitfalls §2 — Durability: in-sync replicas, acks and leader election

Sources: the Apache Kafka documentation, "Design" page of the 4.3 documentation (apache/kafka-site at e6cbeb5, `content/en/43/design/design.md`: sections "Replication", "Unclean leader election" and "Availability and Durability Guarantees"), read 2026-10-15.

## 2.1 What "committed" means
1. **A message is committed only when all the replicas in the in-sync set (ISR) have applied it to their log.** Once committed, it is not lost as long as one broker that replicates the partition stays alive; the page's stated guarantee is that a committed message is not lost as long as at least one in-sync replica is alive, at all times.
2. **Consumers only receive committed messages,** so a consumer never sees a message that could be lost on a leader failure.
3. **A replica leaves the ISR** when its broker loses its session with the controller, or when it falls too far behind the leader (`replica.lag.time.max.ms`). Replication follows a fail/recover model; Byzantine failures are not handled.

## 2.2 `acks` does not mean all replicas
1. **`acks=all` means all the current in-sync replicas, not all assigned replicas.** The page's example: a topic with two replicas of which one has failed, so one replica is in sync; a write with `acks=all` succeeds, and can be lost if the remaining replica also fails.
2. **`acks=0` and `acks=1` commit more weakly:** asynchronously across the ISR for 0, synchronously on the leader only for 1. Regardless of `acks`, messages are not visible to consumers until they are replicated to all in-sync replicas and the ISR is no smaller than `min.insync.replicas`.
3. **To prefer durability over availability, the page names two topic settings:** disable unclean leader election (a partition whose replicas are all down stays unavailable until the most recent leader returns), and set a minimum ISR size with `min.insync.replicas`.
4. **`min.insync.replicas` only takes effect when the producer uses `acks=all`.** It guarantees the acknowledgement by at least that many in-sync replicas, and the partition rejects writes while the ISR is smaller. A higher value gives better consistency and lower availability.

## 2.3 Unclean leader election
1. **When every replica of a partition is dead, the guarantee no longer holds.** Two behaviours exist: wait for a replica from the ISR to return and make it leader, or make the first replica that returns the leader even if it is not in the ISR, in which case its log becomes the source of truth although it may lack committed messages.
2. **Since 0.11.0.0 Kafka's default is to wait for an in-sync replica,** and `unclean.leader.election.enable` changes that for cases where uptime matters more than consistency.

## 2.4 Checks (own guidance)
1. For each topic that must not lose data, write down the replication factor, `min.insync.replicas`, and the producer's `acks`, and check that the last is `all`.
2. The topic has a replication factor above the `min.insync.replicas` value, so that one broker can fail without making the partition reject writes (own reading of the availability trade-off in 2.2.4).
3. `unclean.leader.election.enable` is read from the topic or broker configuration and is not assumed.
