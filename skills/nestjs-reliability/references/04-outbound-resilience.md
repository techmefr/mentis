# nestjs-reliability §4 — Outbound resilience policy and unknown outcomes

Every call to another system will meet it slow or down. Without a plan, a slow dependency ties up your
handlers, your clients wait until their own timeouts fire, and retries from every layer add load to the
service that is already struggling. This section is the policy: how long to wait, whether to repeat, when to
stop calling, how to cap the damage, what to answer instead, and what to do when you do not know whether
the call worked. The principle holds for any Node service; the Nest mapping is at the end.

## 4.1 The time budget
1. **Every outbound call has a per-attempt timeout.** The platform's `fetch` has no timeout of its own
   beyond the HTTP client's very long connection limits (minutes); without one, a hung dependency holds the
   handler, a connection and a pool slot until someone upstream gives up.
2. **Budget end to end.** Time per attempt times number of attempts, plus backoff, must fit inside the
   caller's timeout *and* the load balancer's. Two attempts of 1.5 seconds plus up to 200 ms of backoff is
   about 3.2 seconds: if the caller waits 3, it gives up while you are still working, and the work you
   finish is unseen. A per-attempt timeout does not bound the whole call; add a **total deadline** as an
   abort signal (a timeout signal combined with the caller's own with `AbortSignal.any`) when the whole
   call needs a bound.
3. **A timeout bounds how long you wait, not what happens.** Passing a cancellation signal to every I/O call is
   what makes the underlying work stop. If the code ignores the signal, a timed-out call keeps running in
   the background, outside the bulkhead's count (§4.5) and its result is dropped. A race against a timer only
   settles the race.
4. **Timeouts and 408.** Answer an upstream that did not respond in time with `504`, not `408`: a `408`
   claims the *client* was too slow to send its request, and some clients and proxies repeat `408`s
   automatically, even for `POST`.

## 4.2 Retry only what is safe, at one layer
1. **Retry safe and idempotent methods by default** (GET, HEAD, OPTIONS; PUT and DELETE are idempotent by
   HTTP's definition and some clients retry them too; know which yours does). **POST and PATCH are not
   retried** unless the receiver deduplicates: send an idempotency key derived from the operation (the
   same key on every attempt) and opt that call in. A POST retried without one creates two shipments.
2. **Never retry a deterministic client error** (4xx: the same request gets the same answer); `408` and
   `429` are the exceptions, because they mean the upstream is pushing back. A failure of unknown
   cause is not transient by default.
3. **Use exponential backoff with full jitter**, a cap (30 seconds is a ceiling, not a target), and honour
   `Retry-After`: it replaces the computed wait; when it asks for more than the cap, return the `429` or
   `503` at once rather than waiting.
4. **A request whose body is a stream is never retried**: the first attempt consumed it.
5. **Retry amplification.** Three attempts at each of three hops is up to 27 calls to a dependency that is
   already failing. **Retry at one layer**, usually the service that talks to the external dependency;
   turn retries off in SDKs and HTTP clients beneath it, and on clients that call your own services. A
   retry hidden inside a service method cannot be seen at the call site, which is why a policy applied at
   the entry point or an explicit policy object is preferable to a library default.
6. **Message and event handlers never retry unless declared repeat-safe.** There is no method to inspect,
   so a retry preset reused from an HTTP route must not silently re-run a handler with side effects.
7. **A server-side retry inside one request and a client's retry of the whole request are two different
   problems.** The first lets the server repeat the handler within one request (safe only when the handler
   is repeat-safe); the second is deduplicated by an idempotency key (§1). Use both for a retried write, and
   order the layers so a replay or an "in flight" answer is given **before** any retry, breaker or timeout
   runs: then all retries of one request happen under a single claimed key, a booking that already
   succeeded replays even while the breaker is open, and a `503` or `504` releases the key (§1.7).

## 4.3 The circuit breaker
1. **A breaker opens on a failure rate over a sliding window**, with a minimum number of calls so two
   errors at night do not open it. It counts timeouts and 5xx; it ignores client errors (4xx) because the
   dependency is not down, except `408` and `429`, which count. Tune `recordIf` for anything else that is
   not an outage.
2. **Open means fail fast**: calls are rejected without touching the dependency, and the answer is `503`
   with `Retry-After` set to the seconds until the next probe. After the open duration the breaker is
   half-open and lets one probe through; success closes it with an empty window, failure reopens it. Set
   the open duration near how long the dependency usually takes to recover.
3. **The retry wraps the breaker**, so a rejection by an open breaker is never retried (retrying it would
   be a loop that does nothing).
4. **Give every breaker a timeout.** A breaker only learns from calls that finish. A call that hangs is
   never counted, and a hanging probe keeps a half-open breaker rejecting everything else.
5. **One dependency, one breaker, shared by every call site** (a route, a background job, a message
   handler). What a reader sees when each has its own: the background job keeps spending a timeout per item
   on a carrier that checkout already knows is down, and checkout keeps waiting for timeouts before it
   serves its fallback. Shared state means each side teaches the other.
6. **State is per process.** With several replicas each has its own breakers, bulkhead limits and outbound
   rate limits, a restart starts them fresh, each breaker opens on its own, and a "limit per second" is a
   limit per replica. Do not describe a per-process breaker as a global one in a runbook.
7. **Alert on transitions** (a breaker opening, a bulkhead rejecting), not on individual failures.

## 4.4 Fallbacks
1. **The fallback is the outermost stage** (it also sees the breaker's rejections) and should be **narrow**:
   served only for the condition it was designed for (the breaker is open), not for every error. A flat
   shipping rate that costs money on heavy parcels is a last resort, so a single slow answer still returns
   `504`.
2. **A fallback must be cheap and independent**: it never calls the dependency it stands in for, and it
   preserves authorisation, billing, consistency and freshness. A fallback that answers "paid" for an
   unreachable payment provider is a bug, not resilience.

## 4.5 Bulkheads: cap the expensive work
1. **A bulkhead caps concurrent runs of work that is heavy on a shared resource**, with a bounded queue
   and a queue timeout: two CSV exports at a time, up to three waiting for at most ten seconds, the next
   one refused at once. Twenty at once would slow the checkout for everyone.
2. **A full bulkhead answers `503`**, not `429`: `429` blames the client's request rate, while here the
   server is at capacity for everyone. No `Retry-After`, because nobody knows when a slot frees up.
3. **A slot is held until the handler finishes or the attempt times out.** A handler that ignores its
   signal keeps running outside the count, so pass the signal everywhere (§4.1.3).
4. A bulkhead without a name belongs to its handler; give a name to share one pool of slots across handlers.

## 4.6 Mapping upstream failures to your own answers
1. **Upstream non-2xx, connection failure, malformed body: `502 Bad Gateway`. Upstream timeout: `504`.** Do
   not return `500` for a failing dependency: it hides which side failed.
2. **Do not forward the upstream's body by default**; it may describe the upstream's internals. Forward
   chosen statuses (a `422` whose body tells the caller what to fix) deliberately.
3. **Log the 5xx you map.** The framework's default exception filter does not log an HTTP exception
   (it considers it an intended answer), so a mapped `502` or `504` leaves no trace unless the mapping logs
   it. Log method, origin and path without the query string (query strings carry personal data and keys).
4. **Outbound requests carry credentials, so a URL taken from user input or from an upstream response must
   not receive them.** A client with a base URL should send only to that origin, refuse a redirect to
   another host, refuse credentials embedded in the URL, URI-encode path parameters (a `..` value must
   throw, not move the request to another endpoint), and keep response bodies and query values out of error
   messages and logs.
5. **Validate responses from APIs you do not control**: a type argument describes the data, nothing checks it.

## 4.7 Unknown outcome: after a timeout on a possible write
A timeout, a reset connection or a cancelled call on a write **does not mean the write failed**. The
provider may have charged the card, created the shipment, sent the email; the answer was lost. The state
is "unknown", and treating it as "failed" produces either a duplicate (retried blind) or a customer told
the payment failed when it did not.
1. **Do not retry a write blindly, and do not report it as definitively failed.** Return an answer that
   says the result is pending, and resolve it.
2. **Prefer an operation identity the provider deduplicates on.** Send a key that is deterministic for
   the business operation, derived from stable identifiers (the order id, or the user id plus the client's
   key from §1.7, since the client's key alone can collide across users), and **identical on every
   attempt**. A provider that "returns the existing resource when it has seen the reference before" makes
   a retry safe by construction.
3. **When the provider has no idempotency support, reconcile before retrying**: look the operation up by your
   own reference (a read by reference, a list filtered by your id) and only create it if it is absent.
   Where neither exists, the operation is not safely retriable and a person or a reconciliation job decides.
4. **Write the intent down before calling.** Record "payment for order X, attempt Y, state: calling" durably
   first, then call, then record the outcome. A crash in the middle leaves a trail a reconciler can
   resolve; without it, a crash during the call leaves nothing and the order is silently stuck or silently
   duplicated.
5. **A timeout after a possible write is also the case for the outbox (§3)** when the follow-up (the
   event, the email) must agree with the local state, and **the 5xx-after-effect gap of §1.7** when the
   unknown comes from your own handler failing after the provider answered.
6. **Cancellation does not prove the effect did not happen** either: an aborted `fetch` can have been
   processed by the other side. Reconcile by key whatever the cause of the lost answer: local timeout,
   caller cancellation, shutdown drain.
7. Distinguish in logs and metrics: caller cancellation, local timeout, dependency timeout, and shutdown
   drain, so a "timeout" count is not a mix of unrelated causes.

## 4.8 Verification
1. **A hanging dependency**: make the fake client's call end only when its signal aborts. Assert: the
   response is `504` after the budgeted time; the dependency saw every attempt cancelled (the signal is
   aborted); the number of calls equals the number of attempts.
2. **Fake only the clock functions** (timers and `Date`) so the HTTP server and the test client keep real
   I/O; advance time past each attempt and the backoff, and wait until the request has reached the fake
   before advancing, or there are no timers to advance.
3. **An open breaker**: trip it directly, assert the fallback answers without calling the dependency, advance
   past the open duration, assert the next call is a probe and the breaker closes. Do not produce ten
   failures to test it.
4. **A write that times out**: assert the retry sends the same operation key, or that the code looked the
   operation up before creating it, and that two attempts produced one effect at the fake provider.
5. **A bulkhead**: send more than slots plus queue concurrently; assert the overflow is refused at once
   and the queued ones time out.
6. **A retry on a POST with no key**: assert it is not retried.
7. **State is fresh per test application**; one test's open breaker must not leak into the next.

## 4.9 Nest mapping
- `@nestjs/resilience` (Nest 12 docs): decorators for retry, timeout, circuit breaker, bulkhead, fallback and a
  named `@Resilience(preset)`; `@Signal()` injects the current attempt's abort signal. They apply to
  **entry points** (controllers, resolvers, message handlers, gateways) through one global interceptor and map
  failures to the transport's native error (HTTP `504` for a timeout, `503` with `Retry-After` for an open
  breaker, `503` for a full bulkhead). On a provider method the decorators do nothing and bootstrap warns;
  inside services use a **policy object** (preset or created), which shares the breaker with the routes by
  name. A policy object always applies its retry, so wrap only repeat-safe calls.
- On HTTP, retries apply only to safe methods; on GraphQL to queries; a `POST` or mutation needs an explicit
  `idempotent: true` on the decorator, and **only a decorator can say it** (a preset cannot declare every
  handler repeat-safe). On message, event and WebSocket handlers only a retry set on the handler itself
  turns retries on.
- Import the idempotency module **before** the resilience module so the idempotency layer is outermost
  (§4.2.7); in a hybrid application connect the microservice with the app's configuration inherited, or the
  global interceptor will not reach its handlers.
- Configuration is checked at bootstrap: an unknown preset, an invalid duration or a `NaN` from an unset
  variable, a missing fallback method, or one breaker name configured two ways fails the boot.
- Events for retry, timeout, breaker transitions and bulkhead rejection are an observable stream and are
  published on diagnostics channels.
- `@nestjs/http-client` (Nest 12 docs, built on `fetch`): per-attempt `timeout` (default `0`, none), a
  `signal` option combined with the timeout, retries **on by default** (three attempts, GET, HEAD, OPTIONS,
  PUT and DELETE; connection errors, timeouts, `408`, `429`, `500`, `502`, `503`, `504`; full jitter, `Retry-After`
  honoured, a stream body never retried). `POST` and `PATCH` are not retried unless the call opts in with a
  method list and sends an idempotency key. The `methods` and `status codes` lists **replace** the defaults.
  `toHttpException()` maps the errors to `502`/`504` and logs the 5xx; a client with a base URL sends only to
  its origin. Set retries off on clients that call your own services, and do not stack them with a resilience
  decorator on the same call.
