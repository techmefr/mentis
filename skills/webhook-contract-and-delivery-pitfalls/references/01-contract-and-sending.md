# webhook-contract-and-delivery-pitfalls §1 — Contract and sending

> Part 1 of `skills/webhook-contract-and-delivery-pitfalls`. Read it when webhooks are designed or changed on the
> sending side. Facts come from the Standard Webhooks specification 1.0.0 (Apache-2.0), read 2026-10-20; sentences
> marked "own guidance" are ours. The spec's numbers (a retry table, a timeout range, a size hint) are the
> authors' suggestions and are not carried: re-read the spec before relying on one.

1. **The envelope has three stable pieces: a type, an event time and the data.** The type names the event and
   fixes the schema of the data; the event time says when the thing happened, not when it was delivered. Symptom
   of mixing them up: a consumer orders events by the time of the last retry and applies an old state over a new
   one. Fix: send the event time in the body and the attempt time in a header, and say which is which in the
   documentation.
2. **Two identities, two lifetimes.** The event (or message) id is created once and stays the same on every retry;
   the attempt timestamp changes on every retry. The spec uses the id as the consumer's idempotency key and the
   attempt timestamp as the replay guard. Symptom of a single combined value: either duplicates cannot be
   detected (new id per retry) or a legitimate retry is rejected as stale (old timestamp reused). Keep both.
3. **Name event types as a hierarchy with one schema each.** Dot-separated, a limited character set, the same
   schema every time for a given type, like one URL path returning one shape. Add a display string for humans
   separately. Own guidance: a changed field is a new type (`invoice.paid.v2`) dispatched beside the old one for a
   stated deprecation window, never a silent reshape.
4. **Let the consumer choose types per endpoint and filter at the sender.** Sending every event to every endpoint
   makes the receiver pay for traffic it ignores and widens what it can see. Fix: a subscription list on each
   endpoint, evaluated before delivery, with the default being nothing rather than everything (own guidance).
5. **Thin or full payload is a trade-off, decide it on purpose.** Full: the consumer has the data without a call.
   Thin (identifiers plus the change): cheaper to build, easier to extend later (a thin payload can grow, a full
   one cannot shrink), and every read goes through the API where access can be authorised and audited. Mixed is
   fine (identifiers plus the one field everybody needs). Own guidance: when the data is personal or confidential,
   default to thin, because a full payload is pushed to every listening endpoint and cannot be recalled. Keep
   payloads small; large assets go by link.
6. **Sign the message id, the timestamp and the body together.** The spec signs the string
   `id.timestamp.body` with an HMAC under a per-endpoint secret, and carries the id, the timestamp and one or more
   versioned signatures in three prefixed headers. Reasons it signs the metadata too: the timestamp stops replay of
   a captured request and the id fixes the identity. Rules that follow: the id and the timestamp must not be
   user-controlled or must not contain a dot (the separator), and the bytes signed must be exactly the bytes sent
   (serialise once, sign that string, send that string). Store the body as text, not as a re-encoded structure.
7. **One secret per endpoint, never shared across customers.** A shared secret lets one customer forge another's
   events. Random secret of adequate length, shown once, stored encrypted, and given a recognisable prefix so
   that a leaked value is easy to spot in a scan (the spec defines prefixes). Asymmetric signatures are the
   spec's preferred option when the sender does not control the receiver's security: the consumer holds only a
   public key, so a leak at the consumer forges nothing. The consumer must keep a list of trusted keys and schemes
   and never trust a key delivered in the same request.
8. **Rotate with overlap, send every valid signature.** The signature header is a space-separated list so that,
   during a rotation window, a message is signed with the new secret and the old one and either verifies.
   Procedure: create the new secret, start dual signing, tell the consumer to switch, wait until the consumer has
   switched or the window has elapsed, stop signing with the old one. Signing with an extra, even compromised, key
   does not weaken the scheme, because the consumer still needs one valid signature. For a leaked secret, cut the
   old one at once and accept breakage (own guidance), then tell the consumer through another channel.
9. **Retry for days, with backoff and jitter, and honour the status code.** Delivery counts as success only on a
   2xx. Redirects are failures (fix the URL rather than follow them). A gone answer disables the endpoint. Rate
   limiting and gateway errors slow the endpoint down, and a retry-after hint moves the next attempt. Jitter
   matters because retries can themselves be the load that keeps the receiver down. Set a delivery timeout that
   gives a slow but healthy receiver time to acknowledge. All other statuses and timeouts are failures.
10. **Disable on sustained failure, and tell the owner another way.** After a long run of failures stop sending,
    mark the endpoint disabled, and notify the customer by a channel that does not depend on the broken endpoint
    (email, dashboard banner). Provide a way to re-enable that replays what was missed (see rule 12). Own guidance:
    alert your own team on every disable, because it usually means an outage on either side (the sender in point 17 emits an operator event on every disable).
11. **Keep a delivery log the consumer can read.** Each attempt: time, status, a bounded excerpt of the response,
    next attempt. Customers debug from it. Prune it on a policy; a log nobody prunes becomes the largest table.
12. **Offer replay by message and by range.** The spec treats manual replay of one message or a time range as
    "immensely important" for recovering from long outages. Replays re-send the same message id and the same
    bytes, so the consumer's deduplication still works. Own guidance: a replay is an audited action with an actor
    and a reason.
13. **Enforce HTTPS for payloads that matter.** The signature proves authenticity and integrity, not
    confidentiality. Some customers also need fixed source addresses for their firewall; if you offer them, publish
    the list and a change policy. Delivering to a customer-supplied URL is a request-forgery vector; the defence
    is in `skills/security-hardening` and `skills/nestjs-integration-patterns` §4.4.
14. **Write the event with the change that caused it.** Own guidance: the event row is created in the same
    transaction as the state change (an outbox), then delivered by a worker. Never call the subscriber from the
    request path, and never create the event before commit, or a rollback leaves a callback for something that did
    not happen.
15. **Migrating an older scheme: add, do not replace.** The spec says its headers can be sent beside the legacy
    ones with no change for existing consumers, and the old secret can be reused for the new signature. Payloads
    can migrate three ways: add the new shape to the existing body, add it only for endpoints created after a date,
    or create a new event type per old one. Pick one per audience and publish the date the old form stops.
16. **Test the contract from the consumer's side.** A signature that verifies with an independent implementation,
    a retry that resends the same id, a rotation window where both secrets verify, a disabled endpoint that stops
    receiving. A library from the spec's ecosystem is a reasonable verifier; do not write the check by hand if one
    exists for your language.
17. **What one open-source sender does with failures, as a cross-check of rules 9, 10 and 12.** The Svix server source (MIT) shows these behaviours; they describe one implementation, not a standard, so use them as questions to ask of your own sender:
    - **Disabling needs failures only, for a whole grace period.** The first failure starts a clock; any success clears it; the endpoint is disabled only when the clock has run out with no success in between, and a "disabled" operational event is emitted for the operator. Symptom of the opposite design: an endpoint that fails one minute a day is switched off, or one that fails for a week never is. Check: write down the grace period and what resets it.
    - **A receiver's retry hint is bounded, not obeyed.** The hint can move the next attempt only between the scheduled delay and twice that delay, timeouts and rate-limit answers push the delay to at least a floor, and a random spread is applied to every delay. Consequence for receivers: a very long hint will not park the sender, so shed load with the status code and capacity, not with the hint alone.
    - **A failed manual replay is not retried.** A replay triggered by an operator records its failure and stops, whereas an automatic delivery follows the schedule. Symptom: an operator replays a message, sees "queued", and nothing ever arrives. Fix: show the replay result to the operator and say that it will not retry itself.
    - **The request timeout is configurable inside a bounded range, and an HTTPS-only switch exists** for endpoint URLs. Decide both in policy (rules 9 and 13) rather than inheriting a default.
    Source: `server/svix-server/src/worker.rs` and `cfg.rs` of svix/svix-webhooks (MIT, commit 6e014fd), read 2026-10-20; no number from the source is carried.
