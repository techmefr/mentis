# rabbitmq-delivery-pitfalls §3 — Dead lettering

Sources: the RabbitMQ documentation (rabbitmq/rabbitmq-website at db23826): `docs/dlx.md`, with `docs/confirms.md` for the negative acknowledgement semantics, read 2026-10-15. Phrased under the Apache-2.0 option of the dual licence.

## 3.1 What triggers it
1. **A message is dead-lettered (republished to an exchange) on four events:** a negative acknowledgement with `requeue` false (`basic.reject` or `basic.nack`, or the AMQP 1.0 `rejected` outcome); expiry through per-message TTL; being dropped because the queue exceeded a length limit; and being returned to a quorum queue more times than its delivery limit.
2. **A queue that itself expires does not dead-letter its messages.**
3. **The reason is recorded in the message** (`rejected`, `expired`, `maxlen`, `delivery_limit`) with the queue and a count, in the `x-death` header for AMQP 0-9-1. Dead-lettering a message can happen several times, and the history is compressed by the pair of queue and reason.

## 3.2 Configuring it
1. **A dead letter exchange is an ordinary exchange.** Set it with a policy (`dead-letter-exchange`, and optionally `dead-letter-routing-key`).
2. **Prefer a policy to the `x-dead-letter-exchange` queue argument.** The source says hard-coded arguments are strongly recommended against because they cannot be changed without redeploying the application and deleting the queue before it is redeclared, while a policy can change at any time. When both exist, the argument overrules the policy.
3. **Without a routing key on the queue, a dead-lettered message keeps all its original routing keys,** including those added by the `CC` and `BCC` headers.
4. **Permissions:** declaring a queue with a dead letter exchange needs read permission on that queue and write permission on the exchange, checked at declaration time.

## 3.3 What goes wrong
1. **A missing dead letter exchange drops messages silently.** The exchange need not exist when the queue is declared, but it must exist when a message has to be dead-lettered.
2. **Dead lettering is publishing, and it can fail.** The source's example is a dead letter target quorum queue without an online quorum: the node logs that it cannot forward dead letters.
3. **By default the republish is done without publisher confirms internally.** In a cluster this is not guaranteed safe, since the message leaves the original queue immediately after publishing, and it can be lost if the target queue is not available. Only quorum queues offer at-least-once dead lettering, republishing with confirms.
4. **A dead-letter cycle with no rejection anywhere in it is detected and the message is dropped.** The source's example is a queue dead-lettering to the default exchange without a routing key. Own guidance: a cycle that does contain a rejection is not covered by that rule, so count the redeliveries yourself (§1.4).

## 3.4 Checks (own guidance)
1. Every queue whose messages must not be lost names a dead letter exchange through a policy, and that exchange and a bound queue exist in the same virtual host.
2. Something reads the dead letter queue: a queue nobody consumes is the same loss with a delay.
3. A test rejects a message with requeue false and shows where it lands and with which `x-death` entries.
