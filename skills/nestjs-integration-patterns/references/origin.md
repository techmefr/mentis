# nestjs-integration-patterns: origin and source stamps

> Provenance of `skills/nestjs-integration-patterns`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real service by us.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The NestJS documentation repository (Nest 12 docs): microservices (pipes, guards, exception filters, pre-request hooks, clients), WebSockets (gateways, pipes, exception filters, adapters, rate limiting), SSE, versioning, OpenAPI, dynamic modules, discovery, lazy loading, rate limiting, queues, hybrid applications, raw body, webhooks chapters | MIT | §1 to §5 mechanisms and mappings |
| The BullMQ documentation: auto-removal of jobs, stalled jobs, retries | MIT (`LICENSE` of the repository re-read 2026-10-20: BullForce Labs AB and contributors) | retention strategies, lazy removal, stall defaults, backoff formulas |
| The nestjs-pino README | MIT | §6 setup, context, flush, redaction, version requirements |
| One API-guidelines chapter on deprecation | CC BY 4.0 | §2.5. Attribution: the Zalando RESTful API and Event Guidelines, chapter on deprecation, used under CC BY 4.0; reworded and shortened |
| One MIT agent-skill on search integration | MIT, copyright line generic | §5.4: the dual-write anti-pattern, the real-engine test rule |

The ideas-only repositories in the sourcing review were not used for any phrasing.

## Verification pass 2026-10-20
Re-opened, each against the exact page: the Nest documentation repository (MIT, `LICENSE` re-read) pages for
microservice basics, exception filters, pipes, guards, pre-request hooks, hybrid applications, WebSocket gateways,
exception filters, guards and adapters, server-sent events, versioning, the OpenAPI introduction, types and CLI
plugin pages, dynamic modules, discovery, lazy loading, webhooks (both halves), queues, rate limiting and
lifecycle events; the BullMQ pages on auto-removal, stalled jobs and retries; the nestjs-pino README (MIT,
`LICENSE` re-read: iamolegga); the deprecation chapter of the Zalando guidelines (repository `LICENSE` re-read:
CC BY 4.0).

Confirmed: §1.1 (RpcException, object passthrough, the Observable-returning filter, guard-false message, the
HttpException-becomes-internal-error statement on the pipes page), §1.2.1, §1.2.3 to §1.2.7, §1.3.1 to §1.3.3,
§1.4.1 to §1.4.5, §1.4.7 to §1.4.10 (§1.4.6 not re-read), §1.5.1 to §1.5.3, §2.1.1 to §2.1.4, §2.2.1 to §2.2.4, §2.2.6, §2.3, §2.4.1, §2.4.2, §2.4.4,
§2.5 (the Zalando rules: consent is a MUST, usage monitoring a MUST, the two headers a SHOULD; the guideline
text names the deprecation RFC as 9745 in prose and links it as 9754: the header names are what the block
uses), §3.1, §3.3.1 to §3.3.5, §4.1 to §4.5 as far as the chapter states them (defaults of 10 attempts, a 5 s
start with factor 4 capped at one day, 15 s timeout, five days to disable, 24 h overlap, 5 minute tolerance,
HTTPS-only and private-address blocking with a pinned resolved address, 410 disables, redirects never
followed, 4096 bytes of response kept, pruning not scheduled), §5.1.1 to §5.1.3, §5.1.5, §5.1.6, §5.2.1,
§5.3.1 to §5.3.3, §6.1, §6.2, §6.3.4, request-logging point 5 (version from the pino readme).
Corrected: §1.2.2 (only the message decorator is documented as controller-only), §2.4.3 (the plugin page says SWC
needs type checking and Jest applies no plugin by default; it does not name transpile-only runners), §5.1.4
(the BullMQ page does not say a removed job frees its id), request-logging point 5 (the shutdown option and the 11.1.10 version
are in the pino readme, not in the core lifecycle page), "Standard Webhooks" in §4.2.1 was wrongly labelled absent in that pass: the Nest webhooks chapter names it (fixed 2026-10-21).
Now labelled ours in the text, not on any page read: the discovery timing and scope remarks (§3.2.3,
§3.2.5), the lazy-loading note on injected loggers (§3.3.6 states it comes from the pino readme), the SSE
idle-timeout remark (§1.5.4), the payload-logging rationale (§6.4.1).
Moved out of "Not verified": the BullMQ defaults (30 second stall check, stall count 1) and the Nest webhooks
defaults, both read this pass; and the Nest 12.1.1 note on client listeners (stated for the TCP transporter).
Still unverified: the TCP transport limits and `tlsOptions` of §1.3.4, the `@nestjs/outbox` package and the
minimum version and release status of `@nestjs/webhooks` (the chapter gives neither), §2.2.5 (docs in
production, our judgement), the Throttler behaviour when its storage fails (the rate-limiting page says
nothing, §5.3.4 stays our policy), §5.2.2 and §5.2.4 (alternatives to blocking work, the older queue package
being in maintenance), §5.4 (the index dual write), §6.3.1 to §6.3.3, §6.4.2 and §6.4.3 (redaction
setup and the log-once rule; the readme only mentions the redact option in passing).

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

Independent verification 2026-10-21: 34 checked, 30 matched, 4 corrected, 0 unverified. Corrected in 04-webhooks.md, all four under-credited: the chapter does name Standard Webhooks (§4.2.1), states the body is stored as text (§4.2.2), states the 32-byte whsec_ secret (§4.2.3) and states the endpoint pause on 429, 502, 503 or 504 (§4.3.2). Re-checked the Nest 12 request-scoped gateway statement and the BullMQ 30 second stall check: correct
