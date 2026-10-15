# rabbitmq-delivery-pitfalls §2 — Publisher confirms, durability and routing

Sources: the RabbitMQ documentation (rabbitmq/rabbitmq-website at db23826): `docs/confirms.md` and `docs/reliability.md`, read 2026-10-15. Phrased under the Apache-2.0 option of the dual licence.

## 2.1 What a confirm tells the publisher
1. **A message written to a socket is not a message the broker has.** A client cannot assume it reached the server or was processed: networks fail in ways that take time to detect.
2. **Use publisher confirms, not transactions.** The source says transactions are unnecessarily heavy and cut throughput by a factor of 250. A channel put in confirm mode (`confirm.select`) cannot be transactional, and the reverse.
3. **The broker answers each message with a `basic.ack` or, in exceptional cases, a `basic.nack`,** never both. The delivery tag field carries the publish sequence number, counted from the first `confirm.select`, and `multiple` may cover all messages up to it. A `basic.nack` means the broker refuses responsibility and the client may republish; the source says it is sent only on an internal error in the queue's process.
4. **Confirms and consumer acknowledgements are unrelated.** A confirm covers the publisher's relation with the node and the queue leader; it says nothing about any consumer.

## 2.2 When the confirm is sent
1. **For an unroutable message, when the exchange finds that no queue matches.** With the `mandatory` flag the `basic.return` is sent before the `basic.ack`.
2. **For a routable message, when all the queues have accepted it.** For a persistent message on a durable queue that means persisted to disk; for a quorum queue it means a quorum of replicas accepted it.
3. **A persistent message can be lost before it is on disk.** The source's scenario: publish a persistent message to a durable queue without confirms, restart the broker node, and the message is gone. A publisher in confirm mode would not have received an ack for it, which is how it would have known.
4. **Confirm latency under constant load can reach a few hundred milliseconds,** since the message store writes in batches to limit `fsync` calls. The source strongly advises processing confirms asynchronously as a stream, or publishing in batches and waiting for the outstanding confirms.
5. **Do not depend on the order of confirms.** They are emitted asynchronously, can cover one message or a group, and can arrive in a different order than the messages.

## 2.3 After a failure
1. **Retransmit every message that has no confirm after a channel or connection failure.** The source states the consequence: a confirm may have been sent and lost, so the same message can be published twice, and consumers must deduplicate or be idempotent (§1.4).

## 2.4 Durability and routing
1. **Use durable queues, or a replicated queue type, for important data, and publish the messages as persistent.** Both are needed.
2. **Quorum queues pause in-flight delivery during a leader election,** and recover transparently to clients when the election succeeds.
3. **To know that a message reached at least one queue, set the `mandatory` flag on `basic.publish`.** A `basic.return` with a reply code is sent back when no queue was bound. The source adds that for a publish-subscribe system it can be correct for messages to be dropped when nobody is interested.
4. **To route to one known queue, declare it and publish straight to it.**

## 2.5 Checks (own guidance)
1. The publisher runs in confirm mode, tracks the sequence numbers of the unconfirmed messages and republishes those on reconnect.
2. The queue is durable (or replicated) and the message is marked persistent.
3. A test kills the broker node between the publish and the confirm and shows what the application does with the unconfirmed message.
