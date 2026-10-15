# rabbitmq-delivery-pitfalls §1 — Consumer acknowledgements, prefetch and redelivery

Sources: the RabbitMQ documentation (rabbitmq/rabbitmq-website at db23826): `docs/reliability.md`, `docs/confirms.md` and `docs/consumer-prefetch.md`, read 2026-10-15. Phrased under the Apache-2.0 option of the dual licence.

## 1.1 When to acknowledge
1. **An acknowledgement is a transfer of ownership.** The source says a consumer must not acknowledge a delivery until it has done what it needs with it: stored it in a data store, forwarded it, or performed whatever other operation the message stands for. After the ack the broker is free to delete the delivery.
2. **Acknowledgements give at-least-once delivery.** Without them the source says message loss is possible on publish and consume, and only at-most-once is guaranteed.
3. **Automatic acknowledgement is unsafe.** The broker counts a message as delivered as soon as it is written to the socket, so a closed connection or channel loses every delivery in flight. The source says to consider the mode unsafe and unsuitable for all workloads, and recommends it only for consumers that process deliveries efficiently and at a steady rate.
4. **Automatic acknowledgement also has no prefetch bound.** A fast producer can pile a backlog into the consumer's memory until it runs out of heap or the operating system ends the process. Some clients apply TCP back pressure.
5. **`basic.reject` and `basic.nack` are the negative acknowledgements.** `basic.nack` is a RabbitMQ extension that adds the `multiple` field; `basic.reject` has no such field. With `requeue` false the message goes to a dead letter exchange if one is configured and is discarded otherwise (§3).

## 1.2 Prefetch
1. **With manual acknowledgements, bound the unacknowledged deliveries with a prefetch count (`basic.qos`).** When the count is reached the broker stops delivering on the channel until an outstanding delivery is acknowledged. A value of 0 means no limit.
2. **RabbitMQ applies the count per consumer, where the AMQP 0-9-1 specification shares it across the channel.** Two consumers on one channel each get their own window unless the global flag is also used, in which case both limits apply and the global one is slower because the channel and the queues must coordinate.
3. **Unlimited prefetch still meets other limits:** the source states that quorum queues cap consumer prefetch at 2,000 to limit Raft log growth.
4. **Trade-off in the source:** a higher prefetch raises delivery rate and consumer memory; values from 100 to 300 usually give good throughput without overwhelming consumers, and a prefetch of 1 is the most conservative and cuts throughput, especially on high-latency links. The source calls finding the right value trial and error per workload.
5. **Changing the prefetch while deliveries are in flight can briefly exceed it** because deliveries and acknowledgements are asynchronous.
6. **`basic.get` ignores the prefetch setting, even with manual acknowledgements.** The source tells applications to avoid polling consumers in most cases (§4).
7. **A broker-wide default exists** as `default_consumer_prefetch` in the advanced configuration file, applied when the consumer sets none.

## 1.3 Acknowledging correctly
1. **Acknowledge on the channel that received the delivery.** Delivery tags are scoped per channel, so an acknowledgement on another channel raises an "unknown delivery tag" error and closes the channel.
2. **A second ack of the same tag, or an unknown tag, raises `PRECONDITION_FAILED - unknown delivery tag` and closes the channel.** Own guidance: give each delivery one owner, so that a retry path cannot acknowledge it a second time.
3. **`multiple: true` acknowledges every outstanding tag up to and including the given one,** on that channel only; it reduces network traffic. With `multiple` false the lower tags stay unacknowledged.

## 1.4 Redelivery
1. **Unacknowledged deliveries are requeued automatically when the channel or connection closes,** including client crashes and channel-level errors. Detection of a dead client takes time (heartbeats).
2. **A consumer must expect to see a message more than once and be idempotent.** The source prefers idempotent handlers to explicit deduplication, and notes that a message can reach a different consumer than the first one.
3. **The `redelivered` flag is a hint, in one direction only.** When set, the consumer may have seen the message before (the original delivery might never have reached any consumer); when not set, the source says it is guaranteed the message has not been seen before. A consumer for which a duplicate check is expensive can restrict it to redelivered messages.
4. **If every consumer requeues on a transient condition they create a requeue and redelivery loop,** costly in bandwidth and CPU. The source suggests tracking the number of redeliveries and either rejecting the message for good or scheduling requeueing after a delay. For quorum queues the delivery limit dead-letters poison messages (§3.1).
5. **A consumer whose queue is deleted receives a cancel notification** and must recover, by consuming from another queue or by redeclaring the original one when that is safe.

## 1.5 Checks (own guidance)
1. Search the consumer for the point where the ack is sent: it comes after the write or the forward, never before.
2. The prefetch is set explicitly, and the acknowledgement mode is manual.
3. The handler is run twice on the same message in a test, and the second run changes nothing.
