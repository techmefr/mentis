# nestjs-integration-patterns §4 — Webhooks

A webhook is a promise between two systems that cannot see each other: the sender promises to keep trying,
the receiver promises to check who is calling and to tolerate repeats. The principle: **at-least-once
delivery, signed bodies, no ordering, and an endpoint the sender can stop calling**. Both halves reuse
`nestjs-reliability` (§3 outbox and inbox, §1 idempotency).

## 4.1 Sending: write first, deliver after commit
1. **Record the event in the same transaction as the change** that caused it (an outbox, see
   `nestjs-reliability` §3). Never call the subscriber from the request path: its slowness becomes yours
   and a rollback leaves a callback for something that did not happen.
2. **Fan out after commit**: one delivery per message and endpoint, unique on that pair, so a retry of the
   relay does not duplicate it.
3. **Treat delivery as at-least-once.** A worker that dies after sending produces a repeat with the same
   message id; subscribers deduplicate on it. There is no ordering guarantee: put a timestamp in the body so
   a subscriber can ignore a stale event.

## 4.2 Sending: signing
1. **Sign `id.timestamp.body`** with HMAC-SHA256 under a per-endpoint secret and send three headers
   (`webhook-id`, `webhook-timestamp`, `webhook-signature` with a version prefix such as `v1,` and the
   base64 digest), the layout of the Standard Webhooks specification.
2. **Sign the exact bytes sent.** Store the body as text, not as a parsed JSON column, so replays and
   verification see the same bytes.
3. **Secrets are random (32 bytes), shown once, and sealed at rest.** Rotation overlaps the old and new secret
   for a window (24 hours in the Nest chapter) and sends two signatures; for a leaked secret, rotate with no
   overlap.

## 4.3 Sending: retry, backoff, stop
1. **Default schedule in the Nest chapter**: 10 attempts, backoff starting at 5 seconds, multiplied by 4,
   capped at one day, with jitter, so about two days in total.
2. **Honour `Retry-After`.** A `429`, `502`, `503` or `504` pauses the endpoint, not only the message. A `410
   Gone` ends the delivery and disables the endpoint. Never follow redirects.
3. **Disable an endpoint after a long run of failure** (5 days in the chapter) and tell its owner; alert on
   the disable event.
4. **Set a delivery timeout shorter than the lease** that guards the worker (15 s timeout inside a
   one-minute lease), or a slow endpoint lets a second worker pick up the same delivery.
5. **Keep a delivery log** of every attempt (status, the first few KB of the response), and offer replay that
   re-sends the same id and body. The log needs pruning; nothing schedules that for you.

## 4.4 Sending: do not become a proxy
Delivering to a customer-supplied URL is a server-side request forgery vector. Accept only public https
destinations, block private, link-local and cloud-metadata addresses, resolve the name yourself and connect
to the checked address (so the name cannot resolve differently at connect time), and alert on blocked
destinations. See `security-hardening`.

## 4.5 Receiving: verify before parsing
1. **Get the raw body.** Enable the raw body option on the app and read it from the request; verify the
   signature over those bytes, never over a re-serialised object (key order and whitespace change). Do not
   disable the built-in body parser, or the raw body is not kept. Default body limits are 100 kB on Express
   and 1 MiB on Fastify; raise them for this route only if the provider's payloads need it.
2. **Check the headers exist and have the right shape** before computing anything.
3. **Compare in constant time.** Never `===` on a signature.
4. **Check the timestamp** against a tolerance (5 minutes in the chapter), both directions, so an old valid
   capture cannot be replayed.
5. **Answer failures with `401` and a generic message**; send the reason to an event or log, not to the
   caller.
6. **Some providers sign no id and no timestamp** (GitHub signs the body only). Then deduplicate on a hash of
   the signed body and accept that replay protection is weaker.

## 4.6 Receiving: deduplicate and be idempotent
1. **Record the webhook id in an inbox only after the handler succeeded** (see `nestjs-reliability` §3), so
   a failed handling is retried and a successful one is not repeated.
2. **For an exactly-once state change**, run the state change and the inbox write in one transaction.
3. **Keep the handler idempotent anyway**: the inbox does not cover a crash between effect and record.
4. **Prune the inbox on a window longer than any provider's full retry schedule.**
5. **Acknowledge fast** (`2xx` once persisted) and do slow work after; a provider that waits times out and
   retries.

## 4.7 Operating
- Run the delivery worker on a few instances, not on every pod.
- Alert on delivery lag and on endpoint-disabled events.
- **Version payloads**: add fields, never rename or remove; for a breaking change add a `type.v2` event and
  dispatch both for a deprecation window (see `02-http-surface.md` §2.5).

## 4.8 Verification
- A body altered by one byte, a missing header, and a stale timestamp are each rejected with `401`.
- The same delivery sent twice changes state once.
- An endpoint answering `410` and one answering `503` with `Retry-After` behave differently.
- A destination resolving to a private address is refused.

## 4.9 Nest mapping
The documentation describes `@nestjs/webhooks`, built on `@nestjs/outbox`: dispatch inside the business
transaction, a relay that fans out, a delivery log, the signing scheme above. The package, its minimum core
version and its release status were not verified; the receiving side needs only the raw-body option and a
guard or service that verifies, and works without the package. Reading them is documentation-level only.
