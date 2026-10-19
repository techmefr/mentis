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

**Reasoning of ours, not a source statement:** §1 points 5, 6 (system-level framing), 8, 10; §2 points 5 (partition
change), 7 (pause advice), 10 (design), 12; §3 point 4.
