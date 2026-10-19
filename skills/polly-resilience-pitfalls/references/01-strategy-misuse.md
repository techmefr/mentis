# polly-resilience-pitfalls §1 — Strategy misuse

Each item follows an anti-pattern section in the Polly v8 documentation. The documentation's examples were
read; the wording here is ours.

## 1.1 Circuit breaker
1. **Do not choose the delay between retries from the circuit breaker's state.** The documentation lists
   this as an anti-pattern; let the strategies in the pipeline cooperate instead of a caller reading the
   state and sleeping.
2. **Do not wrap each endpoint with its own circuit breaker.** The documentation lists this as an
   anti-pattern: one breaker per endpoint object splits the failure count and spreads the logic. Define the
   dependency's breaker once in a pipeline.
3. **Know the strategy order.** In a pipeline each strategy wraps the ones added after it; the retry
   documentation shows timeout inside retry (per-attempt) and outside retry (overall) as different designs.
   Decide the order on purpose and test it.

## 1.2 Retry
1. **Retry is not a scheduler.** The documentation lists periodic execution through retry as an
   anti-pattern: use a scheduling tool (it names Quartz.NET and Hangfire) that is more memory-efficient and
   survives machine failures with persistent storage.
2. **Do not add retries per URL in a branching handler.** The documentation lists branching by URL as an
   anti-pattern because the trigger logic spreads across code; consolidate the conditions in the strategy's
   `ShouldHandle` predicate.
3. **Do not use retry as a fallback.** Repeating the same call to the same place is what retry does; to
   call something else when the first fails, use a fallback strategy.
4. **Do not run a method before each attempt through `OnRetry`.** It does not fire before the first
   attempt; group the calls inside the executed callback.
5. **Use one strategy per kind of failure.** The documentation lists a single strategy for several failure
   types (a request and then parsing its response) as an anti-pattern.
6. **Add jitter.** `UseJitter` is false by default; enabling it adds a random factor to the delay so many
   clients do not retry in step.
7. **Retry only what is safe to repeat.** A non-idempotent write retried after a timeout can happen twice.
   This is our own guidance (`dotnet-conventions` §8).

## 1.3 Exceptions as control flow
**In a path where failures are frequent, use `ExecuteOutcomeAsync`.** It returns an `Outcome<T>` that may
carry an exception instance, so strategies handle the failure without the pipeline throwing and the caller
catching. The documentation shows renting a `ResilienceContext` from the shared pool for this call and
returning it afterwards.

## 1.4 Fallback
1. **Do not throw a custom exception from `OnFallback` to replace the original.** The documentation lists
   this as an anti-pattern: throwing from a user-defined delegate disrupts the normal control flow, and the
   fallback telemetry is then not emitted for an unhandled exception from the callback.
2. **Do not use retry in place of fallback** (see §1.2.3), and do not nest `ExecuteAsync` calls inside a
   fallback callback: the documentation lists both as anti-patterns.
3. **A fallback that calls the same dependency is a second retry.** It should return a cached, default or
   degraded result, or call a different dependency. This is our own guidance.

## Verification
- A stub that fails repeatedly: the breaker opens and closes as the documented states describe.
- A fallback test where the secondary also fails returns the intended result without an unobserved
  exception.
