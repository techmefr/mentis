# failure-classification-before-retry §2 — Retry discipline, cool-down and recovery

> Part 2 of `skills/failure-classification-before-retry`. Read it when a retry loop, a cool-down or a breaker
> is written or reviewed. Sources, read 2026-10-19: Google SRE book, "Addressing Cascading Failures"
> (https://sre.google/sre-book/addressing-cascading-failures/) and "Handling Overload"
> (https://sre.google/sre-book/handling-overload/). Own-guidance points are marked. No number from any source
> is carried: the sources' example values are their own illustrations.

1. **Cap retries per request, and per process.** Never retry one request without limit. The cascading-failures
   chapter also suggests a server-wide retry budget that fails requests once spent, and says this can be the
   difference between a small capacity shortfall and a global outage. The overload chapter gives the
   reasoning: with only a per-request limit, an outage multiplies traffic by the per-request attempt count;
   a per-client budget as a fraction of normal traffic keeps the multiplier small. Choose both limits from your
   own traffic and write them in config.
2. **Retry at one layer only.** The chapter shows retries multiplying through a stack of layers (each layer's
   attempts multiply the next one's). Decide which single layer owns retries; the others pass the error up,
   or return "overloaded, do not retry" or a degraded answer.
3. **Randomised exponential backoff.** Without randomness, a blip lines retries up and they hit the dependency
   together. Add jitter. Own guidance: the backoff counter belongs to the thing that failed (a credential, an
   instance), not to the whole caller, and resets on a success.
4. **Honour the dependency's own wait hint.** When a response says how long to wait (the rate-limit hint, see
   §1 point 3), use it instead of your formula, and bound it by your own maximum so a hostile or buggy
   value cannot stall you indefinitely.
5. **Fail fast when the dependency is known down.** The chapter recommends returning an error immediately
   rather than holding resources until a long deadline runs out. A breaker or a cool-down record is how the
   caller knows without trying.
6. **A cool-down is a record with an end, written by the scope that failed.** A credential's cool-down skips
   that credential while others keep serving; a dependency-wide breaker skips the dependency. Both are
   lazy where possible: store the "usable again at" time and test it when the next request arrives, no
   background timer needed (own guidance).
7. **Recover by probing a little, not by flooding.** After a wait, let a single or small number of requests
   through; a success closes the state, a failure re-opens it. A recovering dependency hit with the full queue
   falls over again, which the chapter names as a cascading pattern.
8. **Concurrent failures must not double-count.** Own guidance: when several in-flight requests fail at the
   same moment, they are one event. Count it once or the cool-down stretches and the backoff level jumps
   several steps on a single blip.
9. **Never let a retry change what the call does.** A retried write needs an idempotency key or a lookup of
   the earlier outcome; a retried stream restarts from a known point or not at all. Otherwise the second
   attempt duplicates the first.
10. **Switching is a retry too.** Falling over to another credential or provider consumes the same budget and
    can carry a different price, policy or data location; the switch order is a decision made in advance,
    with the cost side governed by `skills/spend-guard-fail-closed` (own guidance).
11. **Report what you did.** Every retry, skip and switch emits a record with the failure class, the reaction
    and the attempt number, so a rising retry rate shows up as a symptom. The chapter notes that rising
    retries are often a symptom, and that the mitigation can be a code change to retry behaviour or a large
    cut in load.
12. **Test with one injected failure of each class.** For each class in §1 the test asserts the reaction: a
    permanent error is called once; an overload is deferred; a rate limit honours its hint; a terminal state
    is not cleared by time. Assert the number of attempts, not only the final outcome.
