# kafka-delivery-semantics-pitfalls §3 — Transactions and exactly-once between Kafka topics

Sources: the Apache Kafka documentation, "Design" page of the 4.3 documentation (apache/kafka-site at e6cbeb5, `content/en/43/design/design.md`: sections "Message Delivery Semantics", "Using Transactions" and the start of "The Share Consumer"), read 2026-10-15.

## 3.1 What is transactional
1. **Only the producer is transactional.** The consumer and producer are separate; the producer makes transactional updates of the consumer's position (the "committed offset"), and that is what gives the overall exactly-once behaviour.
2. **The consumer position is stored as a message in an internal topic,** so it can be written in the same transaction as the output records. When a transaction aborts, the stored position reverts to its old value and the produced records are not visible to other consumers, depending on their isolation level.
3. **Exactly once is documented for reading, processing and writing within Kafka topics** (Kafka Streams, or the transactional producer with a `read_committed` consumer). For other destinations it needs the cooperation of the destination (§1.4).

## 3.2 The three requirements and the settings
1. **The consumer must be the only consumer of each partition in its group at the time,** which partition assignment provides.
2. **The producer's records, and the offsets it updates for the consumer, are written atomically in one transaction.**
3. **Use one producer instance per consumer instance** to handle transactions together with rebalancing. The page says more efficient schemes exist at the price of more complexity.
4. **Consumer settings: `isolation.level=read_committed` and `enable.auto.commit=false`.** The default isolation level is `read_uncommitted`, where all messages are visible even from aborted transactions. Strictly, the consumer need not use `read_committed`, but without it the page says it sees records from aborted and from still-open transactions.
5. **Producer setting: `transactional.id`.** It makes the producer transactional, and ensures that a restarted application aborts any in-flight transaction from the previous instance. Only the producer has this setting.

## 3.3 After an abort
1. **Transaction markers are written when a transaction commits or aborts;** that is how a `read_committed` consumer skips aborted records.
2. **The application must reset its state and the consumer position explicitly after an abort,** so that it reprocesses the records of the aborted transaction.
3. **The simple policy in the page: discard and recreate the producer and the consumer.** The consumer group then rebalances and the consumer fetches the last committed offset, which rewinds it to before the aborted transaction. A more elaborate application can read the committed offset and `seek` instead.
4. **Exception categories (the page says they were standardised, in the 4.3 documentation):** retriable and refresh-retriable exceptions are retried inside the client and do not reach the application; an abortable exception must be handled by aborting the transaction and resetting the consumer position; an application-recoverable exception requires an application recovery strategy that includes restarting the producer; an invalid-configuration exception reaches the application, which may or may not restart the producer; other Kafka exceptions go to the application.

## 3.4 Share groups are another model
1. **A share group is a different kind of group** with records acknowledged individually, partitions possibly assigned to several consumers, and an acquisition lock with a default duration of 30 seconds (`share.record.lock.duration.ms`). The rules above are about consumer groups; share groups are not covered by this block.

## 3.5 Checks (own guidance)
1. The consumer configuration is read from the code: `read_committed` and no auto commit.
2. Each consumer instance has its own transactional producer, configured with a `transactional.id`.
3. A test aborts a transaction on purpose and shows that the consumer reprocesses the records and the output topic shows them only once.
