---
name: failure-classification-before-retry
description: "Use when writing or reviewing code or an agent loop that calls an unreliable dependency (an HTTP API, a model provider, a queue, a tool) and decides what to do after a failure: retry, wait, switch to another credential or provider, degrade, or stop. The kind of failure decides the reaction."
---

# failure-classification-before-retry

A stack-neutral method for the step between "the call failed" and "do something about it". The common bug is
a single catch block that retries everything the same way: it hammers a dependency that is already
overloaded, retries a request that can never succeed, and burns a budget on a credential that is dead. The
block sorts a failure first, then picks the reaction. It owns no retry library: the stack blocks own those
(`skills/go-http-resilience-pitfalls`, `skills/polly-resilience-pitfalls`, `skills/jvm-resilience-observability`,
and `skills/dotnet-conventions` §8). Related: `skills/spend-guard-fail-closed` for money,
`skills/observability-instrumentation` for the telemetry the classes need.

## When
- A new outbound call, client wrapper or agent tool gets an error path.
- A retry, fallback or "try the next provider" loop is added or reviewed.
- An incident shows retries amplifying an outage, or a job looping on a request that always fails.

## Steps

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | The classes: what kind of failure it is, and the reaction each one earns | before writing any retry or fallback | [`01-classes-and-reactions.md`](./references/01-classes-and-reactions.md) |
| 2 | Retry discipline: budgets, one layer, backoff with jitter, hints, cool-down and recovery | a retry loop, a cool-down or a breaker is written or reviewed | [`02-retry-discipline-and-cooldown.md`](./references/02-retry-discipline-and-cooldown.md) |

## Output / checkpoint
No pipeline checkpoint. For each call site: the table of failure classes the dependency can return with the
reaction chosen for each, the retry budget and the layer that owns it, and the test that replays one failure
of each class. An unclassified error takes the "stop and report" reaction, never the "retry" one.

## Guardrails
- Never retry on "any error". The default for an unknown failure is to stop and surface it with its raw body.
- Never carry another project's numbers (thresholds, cool-down durations): they are tuning for its traffic.
  Choose yours from measurement and write them where the config lives.
- Never retry a request that is not safe to repeat (a write without an idempotency key) without saying so.
- Never classify by matching message text when the dependency offers a status or an error type.
- Never let a transient failure overwrite a permanent one in recorded state.

## Origin
Google's SRE book chapters "Handling Overload" and "Addressing Cascading Failures", RFC 6585 and an AI vendor's
published error reference, all read 2026-10-19; the account-versus-provider split comes from one open-source
gateway's resilience guide. Provenance, what was removed and not verified:
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
