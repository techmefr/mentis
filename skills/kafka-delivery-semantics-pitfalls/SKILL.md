---
name: kafka-delivery-semantics-pitfalls
description: "Use when writing or reviewing Kafka producers and consumers where loss or duplicates matter: when to commit the consumer offset, the idempotent producer, acks=all and min.insync.replicas, unclean leader election, transactions with read_committed for Kafka-to-Kafka exactly-once, storing offsets with the output of an external sink, and compaction tombstones."
---

# kafka-delivery-semantics-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for what Kafka guarantees between a producer, the log and a consumer,
and where the guarantee ends. The premise: **"exactly once" is a property of a specific path, not of Kafka**,
and a write acknowledged by "all" replicas may have been acknowledged by one. The generic rules (idempotent
consumers, retries, dead letters) are in `background-jobs-conventions` §1 to §5 and the outbox in
`nestjs-reliability` §3. Broker operation, security and share groups are not covered.

## When
- A consumer commits offsets, or a producer retries.
- A topic must not lose data when a broker fails, or `acks`, `min.insync.replicas` or replication change.
- A pipeline is meant to be exactly once, between Kafka topics or into another system.
- A compacted topic carries deletes.

## Steps

**Read only the section the task meets.** §1 applies to every consumer; §3 builds on §1 and §2.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Offset commit order, idempotent producer, external sinks | any consumer or producer is written | [`01-delivery-semantics.md`](./references/01-delivery-semantics.md) |
| 2 | ISR, `acks`, `min.insync.replicas`, unclean leader election | a topic must survive a broker failure | [`02-durability.md`](./references/02-durability.md) |
| 3 | Transactional producer, `read_committed`, aborts, exception categories | exactly-once between Kafka topics is claimed | [`03-transactions.md`](./references/03-transactions.md) |
| 4 | Compaction, tombstones, delete retention | a topic is compacted or carries deletes | [`04-compaction-deletes.md`](./references/04-compaction-deletes.md) |

## Output / checkpoint
Each section ends with checks. For a change touching this block: where the offset is committed relative to
the sink write is written down, the durability settings of the topic are listed (replication factor,
`min.insync.replicas`, `acks`), and any exactly-once claim names its path and its isolation level.

## Guardrails
- Never commit the offset before the processing unless losing messages is acceptable (§1.2).
- Never describe `acks=all` as "written to all replicas" (§2.2).
- Never claim exactly-once for a path that leaves Kafka without naming how the sink agrees with the offset
  (§1.4, §3.1).
- Never use auto commit with a transactional pipeline (§3.2).
- Never rely on a consumer seeing every tombstone if it can lag past the delete retention (§4.2).
- Versions: the page read is the Kafka 4.3 documentation; 0.11.0.0 marks (idempotent producer, transactions,
  unclean election default) are quoted from it. Nothing was run against a cluster (🟡).

## Origin
Rewritten from the Apache Kafka documentation, "Design" page of the 4.3 docs (Apache-2.0, apache/kafka-site
commit e6cbeb5), read 2026-10-15; the Kafka rules rest on that one source. Open points and own guidance are in
[`references/origin.md`](./references/origin.md).
