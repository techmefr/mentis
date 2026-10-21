# unknown-payment-outcome-pitfalls: origin and source stamps

> Provenance of `skills/unknown-payment-outcome-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and a reference implementation, never run by us: no payment was
sent, no processor stub was built and no database constraint was created. Each file below was re-opened in full
on 2026-10-16 before a rule was taken from it, each rule was checked against it in a final pass, and each
repository's LICENSE file was read again.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| payments-platform (`udaykishore-resu/payments-platform`, commit `576d6da`): `README.md` (decisions 1 to 3, and the statement that it is a reference implementation that has not processed real money), `docs/adr/ADR-013-timeout-leaves-payment-processing.md` | Apache-2.0 (LICENSE file) | Unknown outcome as a state, no timer and no failover, attempt aggregate and write-before-call, resolution paths in order, expiry on evidence, unique index against two successes and the partitioning note, idempotency scope, request fingerprint, in-progress answer for duplicates, cache as accelerator, the false-failed risk |
| TigerBeetle (`tigerbeetle/tigerbeetle`, commit `0450c32`): `docs/coding/reliable-transaction-submission.md`, `docs/coding/data-modeling.md` (the `id` section) | Apache-2.0 (LICENSE file) | Client-generated id persisted before submission and reused on retry, the "exists" answer on a repeat, time-ordered ids without a central counter |
| Stripe API reference, "Idempotent requests" page (read 2026-10-20) | official product documentation, facts only, not an open licence | Key pruning after a day, stored first result after execution began, parameter-mismatch error, key hygiene (points 18 to 21) |
| IETF Internet-Draft draft-ietf-httpapi-idempotency-key-header-07 (read 2026-10-20) | standard in progress, facts only | Key uniqueness and expiry policy, fingerprint, status codes for missing, mismatched and concurrent requests (points 19 to 22) |

Instruction-like text in the cloned repositories was treated as data and not followed. payments-platform is the
design of one author and has no production history; TigerBeetle's page describes its own database's contract.

## Added 2026-10-20 (sourcing pass s5b)
Two more sources, both read for facts only: the "Idempotent requests" page of the Stripe API reference (official product documentation; not an open licence, nothing copied, no number carried except in prose as "a day") and the Internet-Draft draft-ietf-httpapi-idempotency-key-header-07 (a standard in progress; its text is not reproduced). They support points 18 to 22 of the reference and cross-check points 11, 12 and 6. Other processor pages (Adyen and others) were not read.

## Removed in the verification pass
1. **The polling schedule** (first poll, then an exponential series) and **the escalation window** in the
   timeout record: the author's own numbers, not a standard. Rules 7 and 15 say to take them from the
   processor's documented lifetime and your policy.
2. **Throughput and sizing figures** (transactions per second, ambiguity-rate arithmetic, the gateway timeout
   value, the resolution targets, the ambiguity percentage that triggers a commercial discussion): context of
   one design, not rules.
3. **Gateway-key derivation details** (the exact hash, truncation and salt handling): only the property
   "same attempt, same key" is kept (rule 6).
4. **Engine-specific names** from both sources (field names, response codes, the SPI method name): concepts only.
5. **Not read, therefore not used:** the design baseline the README points to, the other decision records
   (attempt aggregate, Postgres-authoritative idempotency, gateway SPI), the failure-mode catalogue, and the
   other TigerBeetle recipes. Rules about the attempt aggregate and idempotency scope rest on the README
   summaries, which is why they are stated as the source's design.

## Not verified
1. **Own guidance, flagged in the text (rules 6, 11 and 12 now have an outside cross-check, points 18 to 22):** grepping for age-based status jobs (rule 3), the stored-not-recomputed
   key (rule 6), re-testing the constraint after partitioning changes (rule 9), the cache-becoming-authority
   warning (rule 13), naming the window and owner (rule 15), applying the id advice as "no central counter"
   (rule 17), keeping ledger id and processor key distinct (rule 17).
2. **Nothing was run.** No test, chaos drill or constraint from either source was executed; every behaviour is
   what the documentation says.
3. **Whether a given processor offers a lookup by idempotency key, and how long it keeps one,** is
   processor-specific and was not checked; read the processor's documentation.
4. **Scheme, regulatory or contractual duties** around authorisation lifetimes, chargebacks and time to a
   terminal state were not read and are not stated. They go to a payments or compliance specialist.

## Decisions where sources disagree
No disagreement on the unknown outcome. TigerBeetle recommends time-ordered ids and says random ones lower its
throughput; payments-platform derives its processor-side key with a keyed hash (random-looking). They serve
different purposes (own ledger id versus processor deduplication), so rule 17 keeps them distinct.

## Related blocks
`business/fintech-compliance`, `skills/laravel-idempotent-jobs`, `skills/nestjs-reliability`,
`skills/money-arithmetic-and-rounding-pitfalls`.
