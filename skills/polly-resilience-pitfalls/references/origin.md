# polly-resilience-pitfalls: origin and source stamps

> Provenance of `skills/polly-resilience-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us.

This block is meant to be folded into the resilience section of `dotnet-conventions` when the branch
`feat/antislop-lot` (PR 118) lands.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The Polly documentation: retry, circuit breaker and fallback strategy pages (their Anti-patterns sections), performance and resilience context pages, dependency injection page | BSD-3-Clause, read 2026-10-08 | The anti-pattern list per strategy, `ExecuteOutcomeAsync` with the context pool, the provider overload and the service collection anti-pattern, keyed registration, reloads |

The copyright notice of the BSD licence is kept in the licence file of the Polly repository; no text was
copied here.

## Corrections to the earlier review
The "never gate a call on the breaker state, it stays open" rule was not supported: the circuit breaker page
lists varying retry delay by breaker state and per-endpoint breakers as the anti-patterns, so the block says
that instead. The breaker-inside-retry rule was removed; the block states only that order matters.

## Removed in the verification pass (no page supporting them)
"Breaker leaves open only on a call", "breaker inside retry", "fallback exception is not handled by later
strategies" (reworded to what the page says), and "a pipeline is thread-safe".

## Not verified
1. **Own guidance, flagged as such in the text:** idempotent retries, a fallback calling the same dependency
   is a second retry, no shared mutable closures, one pipeline per key reused.
2. **Anti-pattern titles for the circuit breaker, and the fallback "nesting ExecuteAsync" item,** were read
   by section title; their full examples were not re-read in this pass.
3. **Exact API names** were read from the docs, not compiled.

## Related blocks
`dotnet-conventions` §8, `dotnet-aspnet-efcore-pitfalls`, `observability-instrumentation`,
`background-jobs-conventions`.
