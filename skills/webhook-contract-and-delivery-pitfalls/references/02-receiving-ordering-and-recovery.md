# webhook-contract-and-delivery-pitfalls §2 — Receiving, ordering and recovery

> Part 2 of `skills/webhook-contract-and-delivery-pitfalls`. Read it when a handler for someone else's webhooks is
> written, reviewed or debugged. Facts come from the Standard Webhooks specification 1.0.0 and its receiving
> guidance (Apache-2.0), read 2026-10-20; sentences marked "own guidance" are ours. Header names, secret formats and
> windows differ by provider: confirm each against the provider's own documentation.

1. **Verify before you parse, over the raw bytes.** The signature covers the exact body sent. A framework that
   parses JSON and serialises it again changes key order or whitespace and breaks the check. Symptom: every
   request fails in production but a hand-built test passes. Fix: read the raw body for this route, verify first,
   then parse. Check that the three headers exist and have the expected shape before computing anything.
2. **Compare in constant time, and reject with a generic answer.** A plain equality check leaks timing. Return a
   client error with no detail to the caller and send the reason to your own log (own guidance).
3. **Acknowledge only after the event is stored, then work.** Persist the raw event (or enqueue it) and return a
   success status quickly; slow work happens in a worker. Symptom of the opposite: the provider times out, retries,
   and you process the same event twice, or you return success and lose the event when the process dies before
   the write. Rule: a failure to store is a server error so the provider retries. Redirects count as failures for
   most senders.
4. **Check the timestamp window, both directions.** Reject a message whose timestamp is too far from now so a
   captured request cannot be replayed later. The window is a policy; the spec's guidance uses a few minutes
   (re-read before relying). Symptom of a false rejection: clock skew on your server, a proxy delaying delivery, or
   a retry from days ago that carries a fresh attempt time (it should pass). Keep servers on synchronised time.
5. **Deduplicate on the event id, and keep the record longer than the retry span.** Store ids of processed events
   and ignore a seen one. Keep them for longer than the sender's whole retry schedule, not for a few minutes: a
   schedule that lasts days with a dedupe record that lasts minutes lets the late retry through. Record the id as
   part of the same transaction as the effect (or make the effect idempotent), because a crash between effect and
   record otherwise repeats it. Where a provider sends no id (some sign the body only), deduplicate on a hash of the
   body and accept weaker protection (own guidance).
6. **Do not rely on arrival order.** Delivery is unordered and retries make old events arrive late. Never order by
   the time you received an event or by the attempt timestamp. Order by the event's own time when it has one, or
   by an object version, and ignore an event that is older than the state you hold. Symptom: a customer shown as
   active after cancelling, because the cancel arrived first and the earlier update second.
7. **Prefer "fetch the current state" over "apply this payload" for money and access.** Own guidance: treat the
   webhook as a notification that something changed, then read the object from the provider's API and set your
   state from that read. This makes duplicates harmless and order irrelevant, at the cost of one call and a
   dependency on the provider being up. Do it for anything that grants access or moves money; applying the payload
   directly is acceptable for low-stakes display data.
8. **Make state transitions one-way where the domain is one-way.** A paid invoice does not go back to open because
   an old event arrives; an out-of-order event that would move backwards is recorded and ignored. Write the legal
   transitions down (own guidance) and test the reverse ones.
9. **An update before its create is normal.** Symptom: the handler fails with "not found" and the retry sequence
   keeps failing. Fix: on a missing parent, fetch it from the provider, or park the event and retry later with a
   limit, then alert when the limit is hit.
10. **Rotate your own secret with overlap.** During the sender's rotation window the header carries more than one
    signature: verify against each configured secret and accept if any matches. Remove the old secret from your
    configuration only after the window ends. Never log a secret while debugging a rotation.
11. **Recovery after an outage: reconcile, do not hope.** When your endpoint was down for longer than the retry
    schedule, events are gone. Use the provider's replay by range if it offers one, and otherwise list the
    objects changed since the last known good time through the provider's API and run them through the same
    handler. A webhook is a notification, not a ledger: keep a periodic reconciliation job as the backstop (own
    guidance). Payments add a stricter rule in `skills/unknown-payment-outcome-pitfalls`.
12. **Two different events can describe one change.** Some providers emit several events for one thing (a created
    and an updated for the same object). Deduplicate on the object and the transition as well as on the event id,
    so a state change is applied once whichever event arrives first.
13. **Unknown event types are acknowledged and ignored.** The sender may add types without telling you. Returning
    an error for an unfamiliar type triggers retries and can get the endpoint disabled. Log it, count it, review the
    count (own guidance).
14. **Poison events get a limit.** An event that always fails is retried until the sender gives up. Own guidance:
    store the failure, return success to stop the retry storm once your retry budget is spent, and alert so a human
    looks. Never let one bad event keep an endpoint in a failing state until it is disabled.
15. **A failing signature check, in the order to try.** (a) The body was parsed or modified before verification
    (a middleware, a gateway, a body-size limit). (b) The secret is for another endpoint or environment (test
    against live). (c) The secret has a format prefix or an encoding that must be removed or decoded first. (d) A
    reverse proxy stripped or renamed the signature headers. (e) Clock skew rejects a valid timestamp. (f) A
    captured payload was replayed by hand after the window; trigger a fresh delivery from the provider instead.
16. **Test as the sender would break you.** Altered body, missing header, stale timestamp, the same event twice,
    two events out of order, an unknown type, a delayed retry after the dedupe record would have expired, a
    secret mid-rotation, and a storage failure that must give a server error.
