---
name: nestjs-integration-patterns
description: "Use when a NestJS service wires itself to the outside: microservice transports (RpcException, request-response versus events, client timeouts, hybrid apps), WebSocket gateways and Server-Sent Events (exceptions, guards, scaling, teardown), URI/header versioning and the OpenAPI document (types, plugin limits, deprecation headers), dynamic modules, discovery and lazy loading, signed outgoing and incoming webhooks, queue job retention and stalled jobs, rate-limiter storage failure policy, search-index dual writes, and structured request logging with pino."
---

# nestjs-integration-patterns

Step 6 of the pipeline (`WORKFLOW.md`), for the edges of a NestJS service that the module-and-DTO basics do
not cover. The sections are independent. They share one premise: **each edge has its own error channel,
its own lifecycle and its own idea of "done", and the HTTP defaults of Nest do not carry over**. A filter
written for HTTP is skipped by a message handler; a request that ends does not end the work started for it;
a global setting does not reach a connected microservice. Every section states the principle, then the Nest
mapping. It extends `nestjs-node-conventions` (layout, DTOs), `nestjs-reliability` (idempotency, outbox,
resilience), `nestjs-di-traps` (injection) and `api-design` (contract rules).

## When
- A handler is reached by a broker, a socket, an event stream or a webhook rather than an HTTP request.
- The API gets a second version, an OpenAPI document, or an endpoint is being retired.
- A reusable module takes options, scans providers for metadata, or loads on demand.
- A queue, a limiter, or a search index is added and its failure behaviour has not been decided.
- Request logs have to carry an id across the service.

## Steps

**Read only the sections the task meets.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Microservice transports, WebSocket gateways, Server-Sent Events | a handler is not an HTTP route | [`01-transports.md`](./references/01-transports.md) |
| 2 | Versioning, OpenAPI document and types, CLI plugin limits, deprecation signals | the API surface or its documentation changes | [`02-http-surface.md`](./references/02-http-surface.md) |
| 3 | Dynamic modules, discovery, lazy loading | a module takes options, scans metadata or loads late | [`03-module-composition.md`](./references/03-module-composition.md) |
| 4 | Outgoing and incoming webhooks | a service sends or receives signed callbacks | [`04-webhooks.md`](./references/04-webhooks.md) |
| 5 | Queue retention and stalls, limiter failure policy, search-index dual write | a queue, a rate limit or an index is introduced | [`05-queues-limits-indexes.md`](./references/05-queues-limits-indexes.md) |
| 6 | Structured logging with request context | logs must be correlated and safe | [`06-request-logging.md`](./references/06-request-logging.md) |

## Output / checkpoint
Each rule's edge was exercised, not read: a handler error was thrown on each channel and the caller saw the
intended answer (§1), the generated document was read after a change (§2), the module was built once with
sync and once with async options (§3), a signature was verified against a body altered by one byte and a
delivery was replayed (§4), a job was left to finish and to fail and the Redis footprint checked (§5), and a
request's id appeared on every line it produced (§6). A diff verified only through the happy HTTP path is
not verified.

## Guardrails
- Never throw an HTTP exception from a transport handler and expect the caller to see it: use the
  channel's own exception (§1.1, §1.4).
- Never verify a webhook signature on a re-serialised body (§4.5).
- Never leave finished queue jobs to the default retention in a long-lived service (§5.1).
- Never let a limiter's storage failure decide your availability by accident: choose open or closed per
  route, on purpose (§5.3).
- Never log request payloads by default; redact (§6.4).
- The Nest packages for webhooks and outbox are described from the documentation only, and their minimum
  versions and release status were not verified; check before relying on a mapping. Nothing here was
  installed or run.
- Dependencies named here are named, not installed: whoever adds one runs the install, with the project's
  package manager.
- Shutting an endpoint down, rotating a signing secret, replaying deliveries and purging a queue act on
  other people's systems or in shared state: a human decision.

## Origin
Rewritten from the NestJS documentation repository (MIT, the Nest 12 docs; the microservices, WebSockets,
SSE, versioning, OpenAPI, dynamic-module, discovery, lazy-loading, rate-limiting, queues and webhooks
chapters, each read in full before use), the BullMQ documentation, the nestjs-pino README (MIT), the
Standard Webhooks signing scheme as the Nest webhooks chapter describes it, and one API-guidelines chapter on
deprecation (CC BY 4.0, attribution in `references/origin.md`). 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
