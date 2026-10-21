---
name: webhook-contract-and-delivery-pitfalls
description: "Use when a service sends webhooks to customers or partners, or receives them from a provider, in any stack: the event envelope and type names, thin versus full payloads, signing what was sent, secret rotation with overlap, retry and disable policy, delivery log and replay for the consumer, then on the receiving side raw-body verification, a replay window, deduplication, acknowledging before slow work, events arriving out of order or twice with different ids, unknown event types, outage recovery by reconciliation, and the usual reasons a signature check fails. Method only; mechanics of one framework are in its own block."
---

# webhook-contract-and-delivery-pitfalls

A defensive block for the HTTP callback between two systems that cannot see each other. A webhook looks like one
POST; in practice it is a delivery contract (what is promised, how often, in what order) and a trust boundary (who
is calling). Failures are familiar: a handler parses the body before checking the signature, an event is processed
twice, an update arrives before its create, a rotated secret breaks every consumer for an hour, a provider outage
leaves the receiver silently behind. The facts below come from the Standard Webhooks specification (version 1.0.0,
Apache-2.0) and are restated in our words; the rest is our own craft guidance and is marked as such.

Mechanics already written for one stack are not repeated: signed sending, inbox and outbox, and the NestJS wiring
are in `skills/nestjs-integration-patterns` §4 and `skills/nestjs-reliability` §3. Webhooks from a payment
processor, and the unknown payment outcome, are in `skills/unknown-payment-outcome-pitfalls` and
`skills/invoicing-app-build-pitfalls` §2 point 3. Request-forgery defence for an outbound URL is in
`skills/security-hardening`. This block is the stack-neutral contract and the receiving discipline around them.

## When
- A product starts sending webhooks, or an endpoint registered by a customer is added, changed or disabled.
- A handler for a provider's webhooks is written, reviewed or debugged.
- A signature check fails, an event is applied twice, or state drifts after a provider outage.
- A secret is rotated, or an older home-made signing scheme is replaced.

## Steps

**Read the part for the side you are on; a design review reads both.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The contract and the sending side: envelope, event types, thin versus full payloads, signing, rotation, retries, disable policy, delivery log, replay, migrating an old scheme | webhooks are designed or changed on the sending side | [`01-contract-and-sending.md`](./references/01-contract-and-sending.md) |
| 2 | The receiving side: verify, acknowledge, deduplicate, ordering, same change twice, unknown types, recovery, why verification fails | a handler is written, reviewed or debugged | [`02-receiving-ordering-and-recovery.md`](./references/02-receiving-ordering-and-recovery.md) |

## Output / checkpoint
For the sending side: the envelope fields and which of them stay stable across retries, the signed string, the
rotation procedure, the retry and disable policy, and what the consumer can see and replay. For the receiving
side: the order of operations in the handler (raw body, verify, window, dedupe, persist, acknowledge), the stored
identity of an event, how out-of-order and duplicate events are neutralised, and the reconciliation that closes
a gap. Evidence is a test where a body altered by one byte, a stale timestamp and a missing header are each
rejected, the same delivery sent twice changes state once, an update delivered before its create does not break
the handler, and a stub that returns a server error is retried while a gone answer disables the endpoint.
Nothing here was run by us.

## Guardrails
- Verify the signature over the exact bytes received, before parsing. Never re-serialise a parsed body and sign or
  verify that (part 2, rule 1).
- Give every event one identifier that stays the same across retries, and use it, with the object, to deduplicate.
  Never use the delivery time to decide whether an event is new (part 1, rule 2; part 2, rules 4 and 5).
- Treat delivery as at least once and unordered. Never rely on arrival order; carry an event time and an object
  version, or read the current state (part 2, rules 6 and 7).
- Rotate with an overlap that sends and accepts two signatures, and rotate with no overlap only after a leak.
  Never cut a secret over in one step (part 1, rule 8; part 2, rule 10).
- Acknowledge only after the event is stored, and do the slow work afterwards. Never return success first and then
  lose the event (part 2, rule 3).
- Close a gap by reconciling with the provider's own listing. Never assume a webhook was the only copy of the
  truth (part 2, rule 11).
- Do not copy a retry schedule, timeout or window from a source; take them from the provider's documentation or
  set them by policy and write them down.
- Do not paste a real signing secret into a prompt, a fixture, a log or a ticket.

## Origin
Rewritten from the Standard Webhooks specification (`standard-webhooks/standard-webhooks`, Apache-2.0, LICENSE
file read), read 2026-10-20, plus our own craft guidance, flagged in the text. The full provenance, what was
removed and what is not verified are in [`references/origin.md`](./references/origin.md). 🟡: never run by us.
