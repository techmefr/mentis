---
name: polly-resilience-pitfalls
description: "Use when writing or reviewing Polly v8 resilience code in .NET: retry, circuit breaker, fallback and timeout strategies, resilience pipelines registered with dependency injection, sharing data between strategies, handling failures without exceptions, and the misuses such as varying retry delay by breaker state, using retry as a scheduler or as a fallback, throwing a replacement exception from a fallback callback, or building a service provider inside a pipeline builder."
---

# polly-resilience-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for Polly v8 resilience pipelines. The premise: **a strategy does
one narrow job, and using it for a neighbouring job produces a system that looks resilient and is not**.
The broad resilience rules (timeouts, retry budgets, handler stacking) are in `dotnet-conventions` §8; this
block holds the named misuses and how to register pipelines correctly.

## When
- Adding or changing a retry, circuit breaker, fallback, timeout or hedging strategy.
- Registering a pipeline with `AddResiliencePipeline` or `AddResilienceHandler`.
- A breaker stays open, a call runs twice, a callback throws, or memory is held for hours.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Strategy misuse: breaker and retry anti-patterns, fallback callbacks, exception cost | a strategy is chosen or a callback is written | [`01-strategy-misuse.md`](./references/01-strategy-misuse.md) |
| 2 | Registration: service provider, resilience context, keyed pipelines | a pipeline is registered or shares data | [`02-registration-context.md`](./references/02-registration-context.md) |

## Output / checkpoint
The pipeline was driven by a fault-injecting stub: the breaker opened and closed as documented
(§1), the fallback ran once per failure (§1), and the pipeline resolved its services from the container
without building a second provider (§2). A pipeline that was only read is not verified.

## Guardrails
- Never pick a retry delay from the breaker state, and never wrap each endpoint in its own breaker (§1.1).
- Never throw a replacement exception from OnFallback (§1.4).
- Never build a service provider inside a pipeline builder (§2.1).
- Versions: this block targets Polly v8 (`ResiliencePipeline`); the v7 policy API differs. Nothing was run
  while writing it.

## Origin
Rewritten from the Polly documentation (BSD-3-Clause) read 2026-10-08. 🟡: never run by us; open points
are in [`references/origin.md`](./references/origin.md). It is meant to be folded into the resilience
section of `dotnet-conventions` when the branch `feat/antislop-lot` (PR 118) lands.
