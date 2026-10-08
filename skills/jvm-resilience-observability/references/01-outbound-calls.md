# jvm-resilience-observability §1 — Outbound calls

Resilience4j 2.2 user guide and Spring Boot 4.1 documentation. Each rule says what happens to the caller
when it is missing. A retried call runs the operation more than once, so the effect has to be safe to repeat
(see `background-jobs-conventions` §1).

## 1.1 Timeouts first
1. **Every outbound call has an explicit timeout, set by you.** Do not rely on a client library's default
   for connect or read time. Spring Boot exposes `spring.http.clients.connect-timeout` and
   `spring.http.clients.read-timeout` for the HTTP clients it configures, and per-client groups can override
   them; custom builders take the same values in code.
2. **The connection pool wait is a timeout too.** In HikariCP the maximum wait for a connection from the pool
   is `connectionTimeout`, 30 seconds by default with a lowest accepted value of 250 ms; past it the caller
   gets an exception. Set it to what the caller can afford to wait, not to the default.
3. **Time limiter for asynchronous calls.** Resilience4j's `TimeLimiter` limits the execution time of a
   `Future` or `CompletionStage`: it has a timeout duration and a flag deciding whether the running future is
   cancelled when time is up. The blocking variant is equivalent to `future.get(timeout, ...)`.

## 1.2 Retry
1. **A retry has a bounded number of attempts.** In Resilience4j `maxAttempts` counts the initial call, and
   the default is 3, with a fixed wait of 500 ms between attempts.
2. **Wait longer each time.** The default interval is constant; an `IntervalFunction` factory gives
   exponential backoff, and another a randomised interval so many callers do not retry in step. Pick one
   on purpose.
3. **Say which failures are worth retrying.** `retryExceptions` lists the ones to retry (with subtypes),
   `ignoreExceptions` lists the ones that must not be retried, and predicates can decide on the result.
   A business outcome (not found, validation failed) is not a retryable failure. If you use checked
   exceptions the call must be wrapped as a checked supplier.
4. **Retrying a failing dependency without a breaker is a load multiplier.** Three attempts is three times
   the traffic at the moment it can least take it; combine it with §1.3.

## 1.3 Circuit breaker
1. **A breaker wraps one dependency,** so that when it fails repeatedly callers fail fast instead of
   waiting. It moves from closed to open when the failure rate, or the slow-call rate, reaches a threshold
   over a sliding window of recent calls, then to half-open after a wait to let a limited number of calls
   test recovery.
2. **Know the defaults before trusting it.** In the guide the failure rate threshold is 50 %, the sliding
   window is the last 100 calls, and `minimumNumberOfCalls` is also 100, so no failure rate is computed
   until 100 calls have been recorded; a low-traffic service therefore never trips with defaults. Open state
   lasts 60 seconds, and 10 calls are permitted when half-open. Tune the window and the minimum to your
   traffic.
3. **Say what counts as a failure.** `recordExceptions` and `ignoreExceptions` decide; an ignored exception
   counts as neither success nor failure. A call rejected by an open breaker raises
   `CallNotPermittedException`.
4. **A sliding window is not a concurrency limit.** The guide's example: 20 concurrent callers are all
   allowed through a closed breaker even if the window holds 15 calls. To cap concurrency, add a bulkhead.

## 1.4 Bulkhead
1. **Limit concurrent calls per dependency** so one slow dependency cannot take every thread. The
   semaphore bulkhead has `maxConcurrentCalls` (default 25) and `maxWaitDuration` (default 0, the longest a
   caller is blocked when it is full). The thread-pool bulkhead uses a bounded queue and a fixed pool.
2. **The semaphore bulkhead has no thread pool of its own,** so the pool you call from must still be
   sized to be consistent with it; the guide says so explicitly.

## 1.5 Fallbacks
1. **A fallback is a real degraded answer,** a cached value or a smaller response, and not a swallowed
   error. In the Spring starter it works like a catch block, selected by the most specific matching
   exception, is executed regardless of the breaker's state, and must be in the same class with the same
   signature plus one exception parameter.
2. **No fallback is better than a wrong one.** If there is no honest degraded answer, let the error
   propagate to a handler that turns it into a clear response.

## 1.6 Order of the wrappers
1. **Know the order the starter applies.** The Spring Boot starter's aspects apply as
   `Retry( CircuitBreaker( RateLimiter( TimeLimiter( Bulkhead( function ) ) ) ) )`, so the retry is the
   outermost and each attempt goes through the breaker. To change it, use the functional decoration style
   or the aspect-order properties of each module (a higher value is a higher priority).
2. **Write the order in the code or the configuration once,** next to the call, so a reader does not have
   to infer it from annotations on different methods.

## 1.7 Make it visible
1. **Breaker, retry, rate limiter, bulkhead and time limiter metrics are published to the actuator
   metrics endpoint** and to a Micrometer registry once one is configured; the breaker's state is
   mapped to health (closed up, open down, half-open unknown). Alert on the breaker staying open, not on a
   single open event (see `observability-instrumentation` §3 for metric rules).
2. **Do not let a dependency's breaker state decide your liveness** (§2.3).

## 1.8 Checks
- Slow the dependency to twice its timeout in a test: the call fails near the timeout, not later.
- Fail the dependency 100 times: the breaker opens, calls fail fast, the metric shows it, and it recovers.
- With a retry configured, count the calls the dependency received for one failing request.
- Search for HTTP client construction with no timeout, and for `catch` blocks that return a default.
