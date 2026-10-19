# § 1 — What a delivery guarantee promises

> Section 1 of `skills/messaging-conventions`. Read it before choosing any broker setting. The broker owns
> half of every guarantee; the other half is code you write, and the half people forget is the consumer's.

1. **Decide the guarantee per flow and write it down.** Three exist. *At most once*: a message may be lost but
   is never redelivered (fire and forget, acknowledge or commit before processing). *At least once*: a message
   is never lost but may arrive more than once (acknowledge or commit after processing). *Exactly once*: each
   message is processed once and only once, which is not a switch but a property of a whole path (§1.4). A
   flow that carries money, orders or state changes is at least once with an idempotent consumer. A flow that
   carries a metric sample or a cache hint may be at most once. The choice is a product decision with a cost.
2. **Acknowledge or commit after the work, never before.** Both brokers read the same way: an acknowledgement
   (or a committed offset) transfers responsibility to the system that gave it. Doing it first means a crash
   between the acknowledgement and the work loses the message; doing it after means a crash between the work and
   the acknowledgement repeats the work. The second failure is recoverable and the first is not, so the order is
   work, then record the result, then acknowledge. Automatic acknowledgement (acknowledge on send) is the
   at-most-once mode and is only appropriate for consumers that can process at a steady rate and tolerate loss.
3. **A producer that retries creates duplicates, and a consumer that is redelivered repeats work, so the
   consumer must be idempotent.** A publish whose confirmation was lost is sent again, and the broker may already
   hold the first copy; a consumer that died before acknowledging gets the message again. Both brokers' guides say
   to prefer an idempotent consumer to explicit deduplication. Give the effect a stable key (the entity and the
   intended transition, or a message id carried in the payload) and enforce it where the effect is stored, with a
   unique constraint or a check inside the transaction (`skills/sql-conventions` §4.10;
   `background-jobs-conventions` §1.2). A "redelivered" flag, where the broker sets one, is a hint that lets you
   skip the check on first deliveries; its absence is a guarantee, its presence is only a suspicion.
4. **Exactly once has a boundary, and it is the broker's.** Kafka can make a read-process-write cycle that stays
   inside Kafka atomic, by committing the output records and the consumer's position in one transaction. The
   moment the output goes to another system (a database, an email, an HTTP call) the guarantee needs that system's
   cooperation: store the position in the same place as the output, or make the effect idempotent. A statement
   "we have exactly-once" without naming that boundary is the misleading claim the Kafka documentation itself
   warns about.
5. **Writing to the database and publishing a message is two systems, so it is a race.** Commit then publish
   loses the message if the process dies between them; publish then commit announces something that may not have
   happened. Write the message into a table in the same transaction as the state change, and let a separate relay
   publish from that table and mark the row (a transactional outbox); consumers are idempotent anyway (§1.3).
6. **Order is a property of one partition or one queue, not of the system.** A single Kafka partition, or a
   single RabbitMQ queue with a single consumer and no requeue, preserves order; parallel consumers, retries and
   requeues do not. If two messages must be applied in order, give them the same key so they land in the same
   partition, or carry a version/sequence number and let the consumer reject a stale one; never assume dispatch
   order (`background-jobs-conventions` §3.1).
7. **Bound the retries and give failures a destination you read.** An unprocessable message that is requeued
   forever blocks the line and burns CPU; one that is dropped silently is data loss. Retry transient errors a
   bounded number of times with a growing delay, treat a malformed or invalid message as terminal at once, and
   route terminal messages to a dead-letter or parking destination with the original payload, the reason and the
   attempt count, plus an alert on its depth and a documented way to replay (`background-jobs-conventions` §2).
8. **The payload is a contract between deploys.** A rolling deploy runs two versions of the producer and the
   consumer against the same queue; add fields rather than rename or remove, version the message type, and let a
   consumer ignore what it does not know (`background-jobs-conventions` §4.1).
9. **Size the backlog and the speed difference on purpose.** A queue absorbs a slow consumer until memory or disk
   runs out. Bound the work in flight per consumer (the prefetch or the poll batch), set a maximum queue length
   or retention with a stated overflow behaviour, and alert on backlog age rather than on depth alone.
10. **Secrets, access and data classification apply to the broker too.** Messages can carry personal data
    (`business/data-protection`), so retention and who can consume a topic or bind a queue are access decisions,
    not defaults; use a per-application account with the narrow permissions it needs, and TLS to the broker.

**Sources:** the delivery-semantics sections of the Kafka design documentation and the RabbitMQ reliability and
confirms guides (both Apache-2.0), read 2026-10-02. Points 5, 6 (the system-level framing), 8 and 10 are
reasoning of ours; the transactional-outbox shape is a widely used pattern, not a quotation of either guide.
