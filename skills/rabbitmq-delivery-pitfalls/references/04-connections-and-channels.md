# rabbitmq-delivery-pitfalls §4 — Connections, channels and recovery

Sources: the RabbitMQ documentation (rabbitmq/rabbitmq-website at db23826): `docs/production-checklist.md` (the "Application Considerations" section), `docs/reliability.md` and `docs/confirms.md`, read 2026-10-15. Phrased under the Apache-2.0 option of the dual licence.

## 4.1 Connections
1. **Keep connections long-lived.** The source says messaging protocols assume them. An application that opens connections and never closes them exhausts the nodes' file descriptors, after which no new connection is accepted. One that opens a connection to publish a single message and closes it causes connection churn, and nodes under high churn must be tuned to release TCP connections faster than kernel defaults or they run out of file handles or memory.
2. **When a few long-lived connections are not possible, pool them** to reduce peak resource use.
3. **Use separate connections for publishing and consuming.** Flow control applied to a publishing connection can otherwise delay the consumer's manual acknowledgements. Separately, the source says resource alarms throttle publishers when consumers do not keep up.
4. **Do not set the heartbeat timeout below 5 seconds:** the source says it can produce false positives under network congestion or high load.

## 4.2 Recovery
1. **When a connection fails, its channels are closed with it** and must be opened again; the client is told through an exception or similar.
2. **Use the client's automatic connection recovery when it exists** (the source names the Java, .NET and Ruby clients) instead of writing your own. The Go and Pika clients do not have it as a feature and ship examples of how to recover.
3. **A connection failure can lose messages in transit** (being encoded or decoded, in TCP buffers or on the wire). Acknowledgements and confirms are what tell each side when to retransmit (§1, §2).

## 4.3 Channels
1. **Minimise the number of channels and close those no longer needed.** Channels cost resources on both client and server and are meant to be long-lived. Closing a connection closes all its channels.
2. **A channel closed by a protocol error can come from a double ack or an unknown delivery tag (§1.3).** Own guidance: fix the code that acknowledges rather than reopening the channel in a loop.

## 4.4 Observation
1. **Leaks show up only in monitoring:** the source names channel leaks and a growing count of file descriptors from poor connection management as the trends to watch, and describes a slow connection leak as a failure that goes unnoticed for a long time.

## 4.5 Polling
1. **Avoid `basic.get` in most cases.** Polling is inherently inefficient, and the prefetch limit does not apply to it (§1.2).

## 4.6 Checks (own guidance)
1. Count connections and channels on the broker under load: both stay flat when the load is steady.
2. The publisher and the consumer use different connections.
3. Heartbeats are not set below 5 seconds, and automatic recovery is on where the client provides it.
