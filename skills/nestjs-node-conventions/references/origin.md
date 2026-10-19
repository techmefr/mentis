# nestjs-node-conventions — origin and source stamps

> Provenance of `skills/nestjs-node-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

## Extension of 2026-10-02 (sections 5, 6, 7 and the additions to 2 and 4)

Primary source, read on 2026-10-02 from a shallow clone of the framework's documentation repository
(`nestjs/docs.nestjs.com`, `content/`, MIT licence), at the **NestJS 12** content (its migration guide moves from
11 to 12): the request lifecycle FAQ, the lifecycle events page, injection scopes, configuration, exception
filters, pipes, guards, interceptors, middleware, validation, serialization, the file upload and streaming page,
unit and end-to-end testing, the Prisma chapter (including the transactions and connection lifecycle sections),
the keep-alive connections FAQ, the standalone applications page, the logger, and the async-local-storage
recipe. Mechanisms and defaults are the framework's; the grouping, numbering, wording and mechanical checks are
ours. No text was copied.

What is ours, with no external source: the read-only audit method and its six passes (`07-testing-audit.md`),
the rule that an end-to-end test applies the entry point's global set-up, the real-database rule for data tests,
and the "deny by default, mark the public routes" framing (the framework's authentication chapter shows the
pattern).

**Facts that move, with their pin (NestJS 12).** The Standard Schema pipe and interceptor (new in 12), the
Prisma ORM 7 specifics (driver adapter required, config file name, no `beforeExit`, the `latest`-tag warning),
the shutdown-hook and signal behaviour, the request-scoped cost figure (about 5%), the force-close-connections
option per adapter.

**Not read, a stated gap.** Microservices, GraphQL and WebSocket pipelines, the CQRS and queues chapters, the
OpenAPI chapter, the authentication and authorization chapters beyond the public-route pattern, dynamic modules,
the discovery service, versioning, and the Prisma documentation itself (only the framework's chapter was read).
tRPC and Zod (sections 3) were not re-read in this pass.

**Refresh protocol.** Re-read the migration guide, the lifecycle events and request lifecycle pages and the
Prisma chapter of the next major; give each pinned fact above a verdict (`skills/source-freshness` section 3);
stamp the date even when nothing changed.

## Original sources and dogfood record (sections 1 to 4)

Ideas taken from: a market NestJS skill catalogue (skills/nestjs-expert/SKILL.md) for the
module/controller/service architecture, constructor DI, `class-validator` DTOs, HTTP exceptions and
`Test.createTestingModule` tests; an advanced market TypeScript skill for the Zod/`z.infer` contracts,
discriminated unions and mapped types/type guards on Prisma models; a market React/Node skill catalogue
(prisma-development/SKILL.md for the schema/migrations/type-safe operations, trpc/SKILL.md for the
routers/procedures tree, zod-schema-validation/SKILL.md for validation at the boundaries). Mechanisms
rewritten, no copied text.

Dogfooded, 2026-09-10: first real dogfood, a small standalone NestJS 12 project (`UsersModule` with
controller/service/repository, a `CreateUserDto` validated with `class-validator`, a global
`ValidationPipe`, a simulated `WelcomeEmailQueue` job, `Test.createTestingModule` unit tests). Build,
lint and tests all pass; the module/DI/DTO/exception rules in §1-2 held with no rewrite needed. Two real
gaps found by practice and folded into §1.6 above: the current Nest CLI scaffold is ESM and needs `.js`
extensions on relative imports, and `isolatedModules` + `emitDecoratorMetadata` force `import type` for
any interface/type-alias used in a decorated signature (else `TS1272`). §3 (Zod/tRPC) and §4 (Prisma)
were not dogfooded here (no tRPC router, no Prisma schema in this small project) and still need a real
pass.

Dogfooded again, 2026-09-10 (agent `trinity`, its first real dispatch): built a `NotificationsModule`
(paginated query DTO, service, controller, in-memory repository, unit tests) on the same standalone
project. Build/lint/test all passed. One real gap found and folded into §2.2 above: a paginated query
DTO needs `ValidationPipe({ transform: true })` globally, not just `whitelist`/`forbidNonWhitelisted`,
or `@IsInt()` on a query param never passes since Express hands it in as a string.
