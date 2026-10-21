# messaging-conventions: origin and source stamps

> Provenance of `skills/messaging-conventions`. Read it when tracing a rule to its source or checking freshness
> (`skills/source-freshness`), never to apply a rule.

Written 2026-10-02 from primary sources read that day. Status: **new block, base to confront with a real
system**, no in-house production experience (🟡 in `CATALOG.md`).

| Source | Licence | Treatment |
|---|---|---|
| Apache Kafka repository: design documentation (delivery semantics, transactions, replication, availability and durability, unclean election, partitioning, consumer position) and the producer and consumer configuration source (`ProducerConfig`, `ConsumerConfig`, the shared client configuration, the consumer's own offset-commit note), main branch as of 2026-10-02 | Apache-2.0 | Rewrite with credit; defaults are those of that source and are dated |
| RabbitMQ documentation, read from the project's published documentation repository (reliability, confirms, consumers, prefetch, quorum queues, publishers, alarms, access control, production checklist) | documentation dual-licensed Apache-2.0 or MPL-2.0 (README read) | Rewrite with credit; the Apache option is the one relied on |

**Corrections to common advice, from the sources.** (1) Producer defaults moved: the client read acknowledges
from all in-sync replicas and enables idempotence by default; advice to "set these for safety" is now "set them
explicitly so a copied configuration cannot weaken them". (2) Classic-queue mirroring is gone from RabbitMQ 4.0;
replicated queues mean quorum queues or streams. (3) The "all" acknowledgement is not "all replicas": it is all
in-sync replicas, which the minimum in-sync setting bounds from below.

**Not taken.** Cluster sizing and tuning numbers, broker-version upgrade procedures, Kafka Streams and Connect
details, MQTT/STOMP/AMQP 1.0 protocol particulars, federation and shovel, and managed-service guidance (each a
subject of its own, or infrastructure reality). Numeric defaults of limits and timeouts are deliberately not
recited. The RabbitMQ site was not read directly (it serves a bot challenge to automated readers; the challenge
was not worked around, the repository copy of the same documentation was used instead).

**Version stamps.** Kafka main branch 2026-10-02; RabbitMQ documentation describing a release at or after 4.3.

**Reasoning of ours, not a source statement:** §1 points 5, 6 (system-level framing), 7 (delay and alert), 8, 9, 10; §2 points 5 (partition
change), 9 (open-transaction inference), 10 (design and absence of a dead-letter queue), 12; §3 points 3 (sequence-number map), 4, 6 (memory), 10 (recovery steps), 11 (signals), 12 (partly).

## Verification pass 2026-10-20
Re-opened: Kafka `ProducerConfig`, `ConsumerConfig`, `CommonClientConfigs`, `KafkaConsumer` and the design page (`docs/design/design.md`
on trunk; Apache-2.0 licence re-read), and the RabbitMQ website repository docs: reliability, confirms, consumer prefetch, quorum queues,
alarms and production checklist (documentation licence unchanged). Confirmed: producer defaults (all, idempotence on, retries at the
integer maximum with the delivery-timeout advice, five in flight, key hashing), consumer defaults (auto-commit on at 5000 ms, latest,
read uncommitted, last stable offset), next-offset commit rule, poll interval and the thread-and-pause advice, revoked callback,
delivery-semantics definitions, transactions with offsets and read-committed plus auto-commit off, external-system cooperation,
fine-print remark, compaction and tombstones, ordered partitions with key hashing, quorum queues as default replicated choice,
mirroring removed in 4.0, when-not-to-use list, delivery limit 20 from 4.0 and failed-delivery counting from 4.3, at-most-once
dead-lettering default with the reject-publish requirement for at-least-once, publisher confirm wording, mandatory flag, unsafe automatic
acknowledgement, requeue loops, idempotent consumers, alarms blocking publishers, guest deletion, per-application users, TLS.
Corrected: Kafka 2.3 (a too-large in-flight setting throws even with default idempotence; explicit conflicts throw, implicit ones disable),
2.8 and 2.9 wording, 2.7 pause advice now sourced; RabbitMQ 3.2 (quorum queues cannot be exclusive, not "exclusive queues are never
replicated"), 3.6 (prefetch 1 is conservative, 100 to 300 suggested), 3.3, 3.10 to 3.12 relabelled; 1.3 attributes the
idempotent-over-deduplication advice to RabbitMQ only.
Not found on any page read: a partition-count-change warning, an explicit unclean-election default value (the design page implies it),
queue length and message-age monitoring advice, the memory risk of unbounded prefetch.

Independent verification 2026-10-21: 24 checked, 23 matched, 1 corrected, 0 unverified. Corrected Kafka 2.2: the default of unclean leader election is false in the topic configuration source, but the since-0.11 version is on no page read and was removed. Re-checked the in-flight limit (throws even with default idempotence) and quorum queues cannot be exclusive: correct
