---
name: rabbitmq-delivery-pitfalls
description: "Use when writing or reviewing code that consumes from or publishes to RabbitMQ: when to ack, prefetch and manual acknowledgement, redelivery and idempotent handlers, publisher confirms and persistence, the mandatory flag, dead letter exchanges and their silent-drop cases, and connection, channel and heartbeat practice."
---

# rabbitmq-delivery-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the application side of RabbitMQ delivery. The premise: **a
broker that "accepted" a message has not necessarily kept it, and a message that was "delivered" has not
necessarily been processed**. Each side has its own acknowledgement and neither knows about the other. The
generic rules (at-least-once, idempotent jobs, dead letter handling) are in `background-jobs-conventions`
§1 to §5; the outbox in `nestjs-reliability` §3; this block holds the engine-specific traps. Broker
operation (memory and disk alarms, clustering, storage) is not covered.

## When
- A consumer is written or its acknowledgement mode, prefetch or error handling changes.
- A publisher must not lose a message when the broker or the network fails.
- A queue gets a dead letter exchange, a TTL, a length limit or a delivery limit.
- A client opens connections or channels, or sets a heartbeat.

## Steps

**Read only the section the task meets.** §1 and §2 are the two halves of one delivery; §3 starts where §1
rejects a message.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Ack timing, auto-ack, prefetch, double ack, redelivery | a consumer is written or reviewed | [`01-consumer-acks.md`](./references/01-consumer-acks.md) |
| 2 | Publisher confirms, persistence, the `mandatory` flag | a publisher must not lose messages | [`02-publisher-confirms.md`](./references/02-publisher-confirms.md) |
| 3 | Dead lettering: triggers, configuration, silent drops, cycles | a queue gets a DLX, TTL, length limit or delivery limit | [`03-dead-lettering.md`](./references/03-dead-lettering.md) |
| 4 | Connection churn, separate connections, heartbeats, channels, polling | a client is created or its connection handling changes | [`04-connections-and-channels.md`](./references/04-connections-and-channels.md) |

## Output / checkpoint
Each section ends with checks. For a change touching this block: the ack comes after the work, the prefetch
is set with manual acks, the handler survives a second delivery, the publisher runs in confirm mode and
republishes what is unconfirmed, every queue that must not lose messages has a dead letter exchange that
exists, and connections and channels stay flat under steady load.

## Guardrails
- Never acknowledge before the work is done, and never use automatic acknowledgement for data that matters
  (§1.1).
- Never acknowledge on a channel other than the one that received the delivery (§1.3).
- Never publish persistent data without confirms and call it safe (§2.2).
- Never rely on a dead letter exchange that has not been created, or on the default republish being
  confirmed (§3.3).
- Never open a connection per message (§4.1).
- Replaying or purging a dead letter queue re-executes real side effects: a human decision.
- The documentation pages carry no version of their own; behaviour is stated as at the stamped commit (see
  `references/origin.md`). Nothing was run against a broker (🟡).

## Origin
Rewritten from the RabbitMQ documentation (rabbitmq-website, dual-licensed Apache-2.0 OR MPL-2.0, phrased
under Apache-2.0; commit db23826), read 2026-10-15. Open points and own guidance are in
[`references/origin.md`](./references/origin.md).
