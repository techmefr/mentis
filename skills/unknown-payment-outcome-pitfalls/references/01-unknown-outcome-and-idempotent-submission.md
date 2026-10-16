# unknown-payment-outcome-pitfalls §1 — Unknown outcome and idempotent submission

> Part 1 of `skills/unknown-payment-outcome-pitfalls`. Read it when a call that moves money can end without a
> definitive answer, or an idempotency key is being designed. Sourced from the payments-platform README (decisions
> 1 to 3) and its timeout record (`docs/adr/ADR-013-timeout-leaves-payment-processing.md`), commit `576d6da`, and
> from the TigerBeetle pages `docs/coding/reliable-transaction-submission.md` and `docs/coding/data-modeling.md`,
> commit `0450c32`, all read 2026-10-16. payments-platform is a reference implementation that its README says has
> not processed real money: read its rules as one author's design. Sentences marked "own guidance" are ours.

1. **A timeout is the absence of information, not a failure.** When nothing comes back, three worlds fit the
   observation: the request never arrived, it arrived and was declined, or it arrived, was approved and the
   reply was lost. Your side cannot tell them apart, and the customer may already be charged. Design the state
   model so it can say "unknown" out loud.
2. **Record the attempt as unknown and keep the payment in processing.** The attempt gets its own outcome value
   (the source calls it a timeout-unknown outcome), the payment stays in a non-terminal state, and the
   synchronous answer to the caller says "processing" with no terminal outcome and no decline reason. The caller
   then polls or waits for a webhook. The source notes this is a harder client contract: checkout screens and
   merchant integrations must handle a non-terminal answer, and the documentation has to say so plainly.
3. **No timer, scheduler or request-path code may fail a payment because time elapsed.** In the source the
   transition to failed requires an evidence argument (a processor response or a lookup result) in the domain
   API, so there is no zero-argument way to fail a payment, and a test asserts that no scheduled job holds that
   capability. The risk the source names is the tidy-up job ("clean up old processing rows") that quietly brings
   the false failure back. Own guidance: grep for any job or cron that updates payment status by age.
4. **Never fail over to another processor on a timeout.** "Timeout, mark failed, retry elsewhere" is described
   in the source as the most common cause of double charges: the first attempt succeeded silently, the second
   succeeds visibly. The source rejects the variant "fail after a wait, no failover" too, because the merchant,
   believing it failed, asks the customer to pay again and the double charge arrives one layer up, with a false
   outcome written to the ledger. Failing over is legitimate after a definitive negative answer from the first
   processor; an unknown is not one.
5. **One attempt row per execution, and failover creates a new one.** A payment is the intent; an attempt is one
   execution of it against one processor. A retry to the same processor reuses the same attempt and key; a move
   to another processor is a new attempt (a new authorisation) and never edits the old one. The source also
   says an unknown attempt is never retried automatically and never produces a failover.
6. **Write the attempt, with its key, before the call.** The row and its processor-side idempotency key exist in
   the database before the request leaves, so an unknown attempt is always durable and always resolvable. The
   source derives the key deterministically from the attempt id with a keyed hash and a per-processor secret, so
   a transport retry reuses it while a different processor gets a different one. Own guidance: whatever the
   derivation, the property that matters is "same attempt, same key; new attempt, new key", and the key is
   stored, not recomputed from state that may have changed.
7. **Resolve only on positive evidence, fastest first.** In the source: a processor webhook; then a reconciler
   polling the processor's lookup call with the stored key; then the settlement report as the slow backstop.
   Polling backs off with jitter and is bounded by the processor's own authorisation lifetime. The lookup call is
   required of every processor at integration time, because without it the second path does not exist; reject a
   processor that cannot support it before production, not during an incident. Alert when an attempt enters the
   unknown outcome. The source's own schedule and window figures are its choices and are not carried; take the
   lifetime from the processor's documentation.
8. **Expiry is not failure.** The source lets a payment become expired only on evidence that the authorisation
   window closed (a processor confirmation, or the documented lifetime having elapsed and a lookup returning
   not-found), and the reconciler makes the move and records the evidence; a clock firing does not.
9. **Make a second success impossible in the database.** The source's invariant is at most one successful attempt
   per payment, enforced by a partial unique index over the payment id restricted to successful attempts, so a
   buggy orchestrator, a duplicated message or a replayed event cannot move money twice because the database
   refuses the second row. When the tables are range-partitioned, the source derives the partition from the
   payment (not from each attempt) so that all attempts of one payment share a partition and the unique index
   constrains the full set. Own guidance: after any partitioning or sharding change, re-test that two successes
   for one payment are still refused.
10. **Idempotency scope is more than the key.** The source scopes a claim to tenant, merchant, method, route
    template and the key, and claims it with an insert that does nothing on conflict against a unique index. A
    key alone is shared by unrelated callers and routes; the scope makes "same key" mean "same request".
11. **Fingerprint the request to catch one key used for two payments.** The source hashes the canonicalised body
    together with the scope and rejects a reused key whose fingerprint differs, with a distinct error from a
    plain replay. A replay returns the stored result; a reuse with a different body is the client's bug and is
    refused, never silently served the first payment's answer.
12. **A concurrent duplicate gets "in progress", not a blocked thread.** While a first request is still being
    processed, a second request with the same key receives an in-progress answer with a hint to retry later; it
    does not wait on a lease held elsewhere, because blocked request threads are how a retry storm exhausts a
    pool. An expired claim is reclaimed atomically.
13. **The database is authoritative; the cache is an accelerator.** The source mirrors completed records in a
    cache only for latency: a miss, a stale entry or a full outage costs speed and never correctness, because
    the unique index decides. That is what allows the cache to be flushed, resized or lost. Own guidance: if a
    cache outage changes what a request does, the cache has become the source of truth and needs the same
    durability and constraints.
14. **Never report failed for a payment that may have succeeded.** The source calls this the worst of the three
    wrong outcomes (double charge, stuck forever, false failed), because the merchant then charges the customer
    on purpose. Its detection idea is worth keeping: a new payment for the same instrument and amount created
    shortly after a payment still processing is a recognisable signature.
15. **Processing is not allowed to last forever.** Resolution has to be guaranteed and bounded. The source adds a
    human escalation for an attempt still unresolved after a bounded window, as a backstop and not the primary
    mechanism, plus the ambiguity rate per processor as a monitored figure and a scorecard item. Own guidance:
    name the window and the owner in your policy; do not copy the source's number.
16. **The client generates the id, saves it, then submits, and reuses it on every retry.** TigerBeetle's page: the
    app or browser (not the API) creates the transfer id, persists it locally before submission, and sends the
    same id on each retry, so a lost request, a lost reply and a client restart all converge on one transfer; a
    repeat is answered "exists" instead of creating a second. An id generated server-side per request defeats
    this, because a retry gets a new one.
17. **Time-ordered ids, no central counter.** TigerBeetle recommends identifiers that need no central oracle
    (an auto-increment is a bottleneck), are time-ordered, and are unlikely to collide; it says random ids give
    that engine lower throughput. That is a statement about its storage engine; apply it as "do not depend on a
    central counter to mint ids" and check your own database's behaviour before adopting the rest. Keep the two
    uses of a key distinct: the id that makes your own ledger write idempotent is not the key you send to the
    processor, which can be derived per attempt as in rule 6.
