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
10. **A retry that succeeds on the second attempt still tells no one it needed a second attempt**, unless
    the pipeline is told to. The standard resilience handler raises an event on every retry, break and
    timeout; wiring it to the same telemetry as the rest of the request (§8's own guardrail is
    `skills/observability-instrumentation`) is what turns "the dependency is fine, we retried once" into a
    visible signal instead of a number that only shows up once the retries stop working and requests start
    failing outright.
11. **An inbound limit and an outbound one answer to different partitions, and using the wrong partition
    key makes either one meaningless.** Partitioning by the caller's identity protects one tenant from
    starving another on a shared dependency; partitioning by the remote endpoint instead caps total load
    on that endpoint regardless of who asked. A single limiter configured with one partition key is quietly
    solving only one of those two problems, and the symptom is a limit that "isn't working" for the case it
    was never built to cover.
12. **A load-shedding limiter and a queueing one fail two different ways under the same overload**, and the
    choice is not neutral. A queue-processing limiter holds excess requests up to a bound and serves them
    once capacity frees up, trading latency for throughput; a limiter with no queue rejects immediately,
    trading a fast, clear failure for one that a client can retry (point 6) rather than one that waits and
    times out anyway further up the stack. Which one is correct depends on whether a late answer is still
    useful to the caller — for a synchronous user-facing request it usually is not, and a queue only adds
    the wait before the same rejection.
13. **A fallback strategy is the last resilience layer, not a replacement for fixing the call underneath
    it.** Returning a cached or default value when every retry, timeout and circuit-breaker layer has
    already failed keeps the caller from seeing an exception, at the cost of an answer that is stale or
    empty and looks the same as a correct one in the response. It belongs where a degraded answer is
    genuinely acceptable to the caller — and it needs its own signal (point 4's logging point again) so a
    fallback silently masking a dead dependency isn't mistaken for the dependency being healthy.
14. **A resilience pipeline that has never seen the failure it's meant to survive is a configuration, not a
    tested behaviour.** Fault injection — a chaos strategy that deliberately delays, fails or aborts a
    fraction of calls through the same pipeline abstraction the retry and circuit-breaker strategies use —
    is what turns "the timeout budget in point 2 adds up" from arithmetic on paper into an observed
    outcome: the caller actually times out where the sum says it should, the breaker actually opens after
    the configured count, and the fallback in point 13 actually fires when everything above it has failed.
    Run it against a lower environment behind a flag, never against production traffic by accident.
15. **The built-in rate limiter tracks its counters in the process's own memory, and scaling out is exactly
    what breaks that assumption.** Three replicas behind a load balancer each enforce the configured limit
    independently, so a caller throttled at "100 requests per minute" actually gets up to 300 across the
    fleet before anything rejects it — the policy reads correctly and the behaviour it produces is a
    multiple of what was written down. A limit that has to hold across instances needs a shared store (a
    Redis-backed limiter implementing the same partitioned abstraction) rather than the in-memory default
    scaled up and hoped about.
16. **The partition key decides who shares a bucket, and reading it from unvalidated input turns the
    limiter into the load problem it exists to prevent.** Each distinct partition key allocates and caches
    its own limiter state; partitioning on a caller-supplied value with no bound on its cardinality (a raw
    query string, an arbitrary header) lets an attacker manufacture unbounded partitions and exhaust memory
    with requests that individually look throttled and compliant. Partition on the authenticated identity
    (point 11's "who" answer) or another bounded, server-controlled value — never on a client-chosen string
    taken at face value.
17. **`SocketsHttpHandler.PooledConnectionLifetime` is what makes a long-lived pooled connection notice a
    DNS change, and its absence is invisible until the endpoint it points to moves.** A connection is
    reused for as long as it stays healthy, and neither `HttpClient` nor the factory re-resolves the name
    behind it while the connection lives — after a failover or a DNS cutover the pool keeps talking to the
    old address until something closes the connection first. Setting a pooled connection lifetime (a few
    minutes, not tuned to zero) bounds how stale that resolution can get; `HttpClientFactory`'s named and
    typed clients set this by default from .NET 9 on, which is a reason to know whether the client in
    question actually goes through the factory or was constructed by hand.
18. **A hedging strategy sends a second request before the first has failed, which trades load for tail
    latency and is not the same trade as a retry.** Where a retry waits for a definite failure and then
    tries again, a hedging strategy fires a second attempt after a delay if the first is merely slow,
    keeping whichever answer comes back first — the same duplication hazard as point 1 applies with a
    shorter fuse, since the first attempt may still complete server-side after the second one already did.
    It belongs on calls that are cheap to duplicate and where tail latency matters more than the extra
    load, never layered onto the same call as an ordinary retry without doing the arithmetic in point 2
    for both together.
19. **A concurrency limiter (bulkhead) caps how many calls are in flight to one dependency at once,
    independent of how fast or slow each one is.** Where a rate limiter bounds calls per unit of time, a
    concurrency limiter bounds calls happening simultaneously — the distinction matters because a slow
    dependency can stay under any reasonable per-second rate while still holding every available connection
    or thread open, starving every other caller of that same dependency. Isolating each downstream
    dependency behind its own concurrency limit keeps one degraded dependency from consuming the capacity
    that a healthy one needs, which a shared, undifferentiated pool cannot do.
20. **Graceful shutdown is resilience from the server's own side of the boundary, and skipping it turns
    every in-flight request into the failure this section spends nineteen points preventing on the client
    side.** `IHostApplicationLifetime`'s stopping notification, honoured by the host's shutdown timeout,
    gives in-flight requests a window to finish and lets a load balancer stop sending new ones before the
    process actually exits — a container orchestrator that sends `SIGKILL` on its own schedule, with no
    drain period the application requested, turns a routine deploy into exactly the abrupt failure a client
    retry or circuit breaker further up is left to absorb.
