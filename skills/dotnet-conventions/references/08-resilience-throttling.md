# § 8 — Resilience and throttling at the boundary

> Section 8 of `skills/dotnet-conventions`. Read it when an outbound HTTP client is configured, a retry or a
> timeout is added, or a limit is placed on our own API. The generic rules live once, in
> `skills/code-baseline` §4 (an external call fails five ways; retry only what is retryable, with backoff
> and a cap) and `skills/background-jobs-conventions` (an effect delivered twice, and the idempotency key
> that makes it survivable); this section is the half specific to this platform's own handlers, whose
> defaults decide the behaviour you get when nobody chose one.

1. **A retry is a duplication decision, not a reliability setting.** The platform's standard resilience
   handler retries **every** HTTP method unless told otherwise, so a `POST` that inserts a row inserts it
   twice the first time an attempt times out after the server already committed. Retry what is idempotent
   by definition, or make the call idempotent with a key the receiver deduplicates on
   (`skills/background-jobs-conventions` §1.2) — and write down which of the two you did, because the next
   reader cannot tell a deliberate retry-everything from a default nobody looked at.
2. **Timeouts nest, and their budgets have to be arithmetic rather than round numbers.** The standard
   pipeline is a total timeout around a retry around a circuit breaker around a per-attempt timeout: a
   per-attempt timeout longer than the total budget means the second attempt never happens, and the caller
   gets one slow failure where the configuration reads like three fast ones. State the sum next to the
   registration.
3. **Backoff without jitter synchronises the herd it exists to spread.** A thousand clients retrying a
   recovering dependency at the same delay arrive together and knock it over again; the platform's own
   handler adds jitter, a hand-rolled loop with a doubling delay does not, and that is the usual reason a
   dependency comes back three times before it stays up.
4. **A circuit breaker converts a dependency outage into a fast local failure, and into silence.** Once the
   circuit is open nothing calls out, so the errors that were filling the log stop — the incident looks like
   our own error rate improving. Log and count the open/close transitions, or the stability has been bought
   at the price of not knowing (`skills/observability-instrumentation`).
5. **Limiting what our own API accepts is a different mechanism, and reaching for the outbound one is the
   common mistake.** Inbound throttling is middleware, not a resilience strategy on a client. Where it sits
   in the pipeline decides what a limit even means: placed before authentication every request is
   anonymous, so the partition can only be the address, and one office behind one NAT is one client (§6.2
   on order).
6. **A rejection has to be machine-readable, and the default is not.** The limiter answers 503 unless it is
   configured to answer 429 with a retry-after — and a client that cannot tell "too fast" from "broken"
   retries exactly the way point 1 describes, which turns our own limit into the load that justified it.
7. **A health endpoint is called on a schedule for ever, so what it does is a design decision.** One that
   queries the database on every probe is a load generator with a reassuring name. And liveness and
   readiness answer different questions: readiness failing on a degraded dependency takes the instance out
   of the pool, while the same check wired as liveness restarts the process instead — losing the in-flight
   requests and fixing nothing, since the dependency was the problem.
8. **One resilience pipeline per client, not several stacked.** Attaching more than one resilience handler
   to the same outbound call multiplies retries against retries and timeouts against timeouts in a way
   nobody reading the registration can add up from the call site — the total behaviour lives in whichever
   handler ran last, invisibly. One named pipeline, read top to bottom, is what point 2's arithmetic
   actually describes.
9. **Rate-limiting a call you make is a different problem from rate-limiting a call you receive**, and it
   needs its own strategy, not a repurposed inbound limiter. A token-bucket style limiter in front of an
   outbound client tolerates a natural burst while still capping the average rate against a dependency that
   has its own ceiling — a fixed-window limiter on the same traffic either starves a legitimate burst or
   lets one straddle the window boundary and double the instantaneous rate.
