---
name: serverless-edge-worker-pitfalls
description: "Use when writing or reviewing code that runs as a serverless or edge function (Cloudflare Workers first, the same traps on Lambda-style platforms): runtime configuration and bindings, state shared between requests, promises that outlive the response, memory and CPU limits, queues and at-least-once delivery, service-to-service calls, database connections and durable state."
---

# serverless-edge-worker-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for functions that the platform starts, reuses and kills for you. The
premise: **the handler looks like an ordinary request function, but the process around it is shared, short-lived
and limited**: a module variable leaks one user's data to the next, a promise nobody awaited dies with the
response, a body read whole exhausts memory, a queue delivers the same message twice. Long-lived servers are
in `nestjs-reliability` and `queue-worker-runtime-pitfalls`; infrastructure as code is in `terraform-conventions`.

## When
- A function is written for an edge or serverless platform, or its configuration file changes.
- Work is done after the response is sent, or moved to a queue or a workflow.
- A function talks to a database, another function, or a durable stateful object.
- A reviewer asks why a function behaves differently in production than in a local run.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Compatibility date, bindings and generated types, secrets, logs, tests in the real runtime | a function or its configuration file is created or changed | [`01-configuration-and-bindings.md`](./references/01-configuration-and-bindings.md) |
| 2 | Shared state, promise lifetime, memory and CPU limits, streaming, fail-open error handling, secret comparison | a handler is written or reviewed | [`02-request-lifetime-and-state.md`](./references/02-request-lifetime-and-state.md) |
| 3 | Queues and workflows, service calls, database connections, durable objects, serialization, other platforms | work leaves the request, or the function calls something else | [`03-async-work-and-integration.md`](./references/03-async-work-and-integration.md) |

## Output / checkpoint
Each section ends with its own checks. For a change touching this block: no module-level mutable request state,
every promise is awaited, returned or attached to the platform's background hook, large bodies stream, each
queue consumer is idempotent, and the function's types come from the platform's generator, not from hand.

## Guardrails
- Pass request state as arguments (§2.1). Never keep it in a module variable.
- Await, return or hand off every promise (§2.2). Never leave one floating.
- Stream or bound any body that can be large (§2.3). Never read it whole.
- Make every consumer safe to run twice (§3.1). Never rely on exactly-once delivery.
- Put secrets in the platform's secret store, never in configuration or source (§1.4).
- Limits and prices are the platform's; re-read them for the plan in use before relying on a number (🟡, nothing here was deployed).

## Origin
Rewritten from the `cloudflare/skills` repository (Apache-2.0, commit 86505e4), read 2026-10-20. The non-Cloudflare
points are our own guidance and are labelled. See [`references/origin.md`](./references/origin.md).
