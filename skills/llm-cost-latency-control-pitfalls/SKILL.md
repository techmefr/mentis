---
name: llm-cost-latency-control-pitfalls
description: "Use when an application's model calls are too slow or too expensive, or when one is designed with that in mind: prompt layout and caching of repeated prefixes (and the cache that silently never hits), token budgets on input and output, routing easy work to a smaller model and its failure modes, streaming and batching, and timeouts, retries and concurrency that multiply cost under load instead of absorbing it."
---

# llm-cost-latency-control-pitfalls

A defensive block for the moment a bill or a response time is called "too high". The two sections share one
premise: **cost and latency are properties of the call path, not of the model, so measure per stage and per
request class before choosing a lever, and check that every lever is still working after the next prompt
edit**. The fail-closed spend cap itself is in `spend-guard-fail-closed`; picking a model for a task is in
`choose-model`; versioning the prompt that gets longer is in `prompt-versioning-and-change-gating-pitfalls`;
what to do after a failure is in `failure-classification-before-retry`; run caps for agent loops are in
`agent-run-limits-and-guardrail-pitfalls`; measuring the effect of a change is in `llm-eval-regression-pitfalls`.

## When
- The monthly bill or latency percentile moved and nobody knows which feature did it.
- A prompt grew (instructions, examples, retrieved context) and cost followed.
- A cheaper model or a cache is proposed to save money.
- A timeout, retry or concurrency setting is chosen for a model-backed endpoint.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Spend levers: measurement per request class, prefix caching, token budgets, routing, batching | the bill is too high or a lever is proposed | [`01-spend-levers.md`](./references/01-spend-levers.md) |
| 2 | Latency and load: first-token versus total time, streaming, timeouts, retries, concurrency, rate limits | responses are slow, time out or storm under load | [`02-latency-and-load.md`](./references/02-latency-and-load.md) |

## Output / checkpoint
Cost and latency are broken down per request class (feature, prompt version, model) with input tokens, output
tokens, cached share, retries and failures, before any lever is pulled (§1.1). Each lever that was pulled has a
metric proving it works (a cache hit share, a routed share with its quality result) and a test that fails when
it stops (§1.2, §1.4). Timeouts, retry counts and concurrency are written down as one budget that holds under a
provider slowdown (§2.3). A saving with no quality check beside it is a regression waiting for a complaint.

## Guardrails
- Never optimise from the invoice total; split by request class first (§1).
- Never route to a smaller model without running the same cases on both and reading the failures (§1.4).
- Never stack retry layers without multiplying them out; instead set one retry budget per user request (§2).
- Never put a per-user value or a timestamp ahead of a long shared prefix you want cached (§1).
- Never treat a cost figure from a dashboard as the bill; see `spend-guard-fail-closed` (§1).
- This block is idea-level guidance from the sources in [`references/origin.md`](./references/origin.md), read on the
  date there. No call was made and no price or limit of any provider is stated.

## Origin
promptfoo documentation (MIT) on response caching, rate limits and cost and latency assertions, plus craft
knowledge marked "own guidance", read 2026-10-20. Provider caching, batching, rate-limit, streaming and error documentation (Anthropic, OpenAI) and the Azure circuit-breaker
pattern page were re-read on 2026-10-20 for the credited points (facts only); no price, limit or lifetime figure is stated. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
