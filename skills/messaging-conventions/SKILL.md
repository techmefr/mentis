---
name: messaging-conventions
description: "Use when configuring or writing producers and consumers for a message broker (Kafka, RabbitMQ): delivery guarantees, acknowledgement and offset commit order, ordering, retries and dead-lettering, durability settings. Broker-independent job rules stay in background-jobs-conventions; this block is the per-broker half."
---

# messaging-conventions

Step 6 of the pipeline (`WORKFLOW.md`). `background-jobs-conventions` states what holds for any asynchronous
work, whatever carries it: assume it runs more than once, design the failure path, do not assume order. This
block is the half that is specific to a broker: which settings turn those rules into behaviour, and which
defaults and old advice no longer hold. Every rule holds in a repo with nothing installed (`CONVENTIONS.md`,
rule A).

**Special status.** New block, no in-house production experience: the content comes from the brokers' own
published documentation and source, read on 2026-10-02. A base to confront with the first real system, not
proven doctrine. Defaults and removed features are tied to broker versions and marked; confirm the deployed one.

## When
A producer, a consumer, a queue, a topic, an exchange or a retry/dead-letter policy is created or changed, or a
message is lost, duplicated, reordered or stuck.

## Steps

**Read §1 first, every time,** then the section for the broker in use.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | What a delivery guarantee actually promises, and who has to do the rest | always, before choosing settings | [`01-guarantees-and-the-consumer-side.md`](./references/01-guarantees-and-the-consumer-side.md) |
| 2 | Kafka: producer durability, idempotence, offsets, ordering, transactions | the broker is Kafka | [`02-kafka.md`](./references/02-kafka.md) |
| 3 | RabbitMQ: queue type, confirms, acknowledgements, prefetch, requeue loops, dead letters | the broker is RabbitMQ | [`03-rabbitmq.md`](./references/03-rabbitmq.md) |

## Output / checkpoint
For each flow, the guarantee it needs is written down (§1.1), the producer setting that provides it and the
consumer behaviour that completes it are named, and a replay or duplicate has been thought through (§1.3).
Nothing here writes a pipeline checkpoint.

## Guardrails
- Never acknowledge or commit an offset before the work the message asks for is done and recorded (§1.2).
- Never claim "exactly once" for a flow without naming the mechanism and its boundary (§1.4).
- Never rely on an old default from memory: read the configuration reference of the deployed version.
- A dead-letter or parking destination nobody reads is a failure that was hidden, not handled
  (`background-jobs-conventions` §2.3).
- No comments in the code produced.

## Origin
The brokers' own documentation and client configuration source (both Apache-2.0), read 2026-10-02 and
rewritten. Provenance, licences and the version stamps are in [`references/origin.md`](./references/origin.md).
