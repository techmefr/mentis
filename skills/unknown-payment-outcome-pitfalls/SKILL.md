---
name: unknown-payment-outcome-pitfalls
description: "Use when code calls a payment processor or bank and the call can time out or return an ambiguous transport error: treating a timeout as unknown rather than failed, never failing over on a timeout, recording an unknown attempt outcome, resolving it only on evidence (webhook, lookup by the stored key, settlement report), one attempt row per execution, a database constraint against two successes, idempotency scope and request fingerprints, in-progress answers for concurrent duplicates, and client-generated ids reused on every retry."
---

# unknown-payment-outcome-pitfalls

A defensive block for the one moment a payment integration cannot answer "did the money move": the call went out
and nothing usable came back. The tempting answers (mark it failed, retry elsewhere, assume success) each have a
way to charge a customer twice or to record an outcome nobody observed. The sources are two public engineering
write-ups, and one of them (payments-platform) is a reference implementation that its own README says has never
processed real money, so its rules are one author's design, not an industry standard. The engineering invariants
for money code in general (idempotency keys, webhook verification and dedup, reconciliation as a job) are in
`business/fintech-compliance` part 4; this block does not repeat them and goes deep on the ambiguous outcome.
Idempotent background work that is not about payments is in `skills/laravel-idempotent-jobs` and
`skills/nestjs-reliability`.

## When
- A diff calls a payment processor, acquirer, bank API or any service that moves money, and handles a timeout,
  a dropped connection or a 5xx.
- A status such as "failed" is assigned from elapsed time, a retry count or a cleanup job.
- A payment can be retried or sent to a second processor.
- An endpoint accepts an idempotency key, or a client submits a payment and may retry it.

## Steps

**Read the part before changing the handling of an unknown outcome.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Unknown outcome and idempotent submission: the unknown state, no timer and no failover, the attempt record, resolution by evidence, the database constraint, idempotency scope, fingerprints, concurrent duplicates, client ids | any code path can end a payment call without a definitive answer, or an idempotency key is designed | [`01-unknown-outcome-and-idempotent-submission.md`](./references/01-unknown-outcome-and-idempotent-submission.md) |

## Output / checkpoint
For each call that moves money: the states the payment can be in when the call returns nothing usable, who or
what is allowed to leave that state and on what evidence, where the attempt and its key are stored before the
call, which constraint makes a second success impossible, and what the client is told in the meantime. Evidence
is a test (or a drill against a processor stub) that accepts a request, drops the response, and shows one
attempt in the unknown outcome, the payment still processing, no second attempt created, and the lookup path
resolving it. Nothing here was run by us.

## Guardrails
- This block does not replace a chartered accountant, an auditor, a legal, compliance or payments-regulation
  adviser, or a financial adviser. It is engineering method, not accounting, legal or investment advice.
- Never mark a payment failed because time passed, and never leave a cleanup job able to do it (part 1, rules 2
  and 3).
- Never fail over to another processor on a timeout; a failover follows a definitive negative answer only
  (part 1, rule 4).
- Never mutate an old attempt to retry; create a new one, and write it before the call (part 1, rules 5 and 6).
- Never rely on application care alone against a double charge; put the constraint in the database (part 1,
  rule 9).
- Never report "failed" for a payment that may have succeeded (part 1, rule 14).
- Do not copy a schedule, window or size from the sources; they are the authors' numbers. Set them from the
  processor's own documented limits and your policy.
- Do not paste a real card number, token or processor secret into a prompt, a fixture or a log.

## Origin
Rewritten from the payments-platform README and its timeout decision record (Apache-2.0) and from the
TigerBeetle documentation pages on reliable submission and data modelling (Apache-2.0), read 2026-10-16. The
full provenance, what was removed and what is our own guidance are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
