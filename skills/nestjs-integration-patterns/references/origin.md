# nestjs-integration-patterns: origin and source stamps

> Provenance of `skills/nestjs-integration-patterns`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real service by us.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The NestJS documentation repository (Nest 12 docs): microservices (pipes, guards, exception filters, pre-request hooks, clients), WebSockets (gateways, pipes, exception filters, adapters, rate limiting), SSE, versioning, OpenAPI, dynamic modules, discovery, lazy loading, rate limiting, queues, hybrid applications, raw body, webhooks chapters | MIT | §1 to §5 mechanisms and mappings |
| The BullMQ documentation: auto-removal of jobs, stalled jobs, retries | official docs | retention strategies, lazy removal, stall defaults, backoff formulas |
| The nestjs-pino README | MIT | §6 setup, context, flush, redaction, version requirements |
| One API-guidelines chapter on deprecation | CC BY 4.0 | §2.5. Attribution: the Zalando RESTful API and Event Guidelines, chapter on deprecation, used under CC BY 4.0; reworded and shortened |
| One MIT agent-skill on search integration | MIT, copyright line generic | §5.4: the dual-write anti-pattern, the real-engine test rule |

The ideas-only repositories in the sourcing review were not used for any phrasing.

## Rewrite notes
Examples and listings were dropped; rules are re-explained principle first. Items 5.3.4, 2.2.5 (docs in
production), 6.3.2 (untrusted request id) and 5.1.5 are our own judgement and labelled as such.

## Not verified
1. **Package availability.** `@nestjs/webhooks` and `@nestjs/outbox` are described from the docs only;
   minimum core versions and release status unknown.
2. **Throttler storage errors.** The chapter says nothing about storage failure; the guard's behaviour when
   storage throws was not checked. §5.3.4 is our policy.
3. **Version notes** (Nest 12.1.1 client listeners, 11.1.10 shutdown option, pino integration requirements)
   come from the Nest docs and the nestjs-pino README, not from running them.
4. **Dropped claims**: "idle polling" cost for queues and an "HTTP/2 connection limit" for SSE were in the
   sourcing review and in neither source read; they are not in this block.
5. **Standard Schema support in OpenAPI** (§2.2.6) depends on the Swagger package and library versions.
6. **BullMQ defaults** (30 s stall interval, stall count 1) and the Nest webhooks defaults (10 attempts,
   15 s timeout, 5-day disable, 24 h rotation overlap, 5-minute tolerance) are quoted from docs.
7. **RFC numbers** for the deprecation and sunset headers (9745, 8594) come from the guideline chapter and
   are not written in the block text; the header names are.
8. **Written by us:** all verification lists, the open/closed split by route, and the SSE keep-alive note.

## Related blocks
`nestjs-reliability` (outbox, inbox, idempotency, outbound policy), `nestjs-di-traps`, `api-design`,
`background-jobs-conventions`, `security-hardening`, `observability-instrumentation`, `node-container-runtime`.
