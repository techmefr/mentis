---
name: nestjs-node-conventions
description: "Use when writing, testing or reviewing a module, a controller, a service, a pipe, guard, interceptor or filter, the configuration and shutdown, or a tRPC router on the NestJS/Node stack: constructor injection, validated DTOs, the request pipeline order, Zod/tRPC contracts, the Prisma repository and its transactions, end-to-end tests and a read-only audit."
paths: "**/*.module.ts, **/*.controller.ts, **/*.service.ts, **/*.guard.ts, **/*.pipe.ts, **/*.interceptor.ts, **/*.filter.ts, **/*.dto.ts, **/main.ts, **/schema.prisma, **/*.e2e-spec.ts"
---

# nestjs-node-conventions

Step 6 of the pipeline (`WORKFLOW.md`). The mentis block for the Node backend: Nest architecture, validation
contracts, cross-cutting type-safe contracts expected by tRPC, Prisma data access, and, since 2026-10-02, the
request pipeline, configuration and shutdown, scopes, tests and a read-only audit method. One block rather than
one per library, because it is always the same stack and the same step. **Status: a base to confront with real
work**; sections 1 and 2 were dogfooded (see `references/origin.md`), the rest were not. Framework facts are
pinned to **NestJS 12** (documentation read 2026-10-02); the rest of the Node and TypeScript practice lives in
`skills/typescript-patterns`, `skills/api-design` and `skills/security-hardening`.

## When
As soon as a Nest module, a controller, a service, a guard, a pipe, an interceptor, a filter, a DTO, the entry
point or configuration, a tRPC router or procedure, a Prisma repository or a Nest test is written, modified or
audited, during `code` (6), `tdd` (5) or `review` (8).

## Steps

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Module, controller and service architecture; constructor DI; ESM scaffold traps | a module, controller, service or its injection is written | [`01-architecture-di.md`](./references/01-architecture-di.md) |
| 2 | DTOs, global validation, schema validation, typed exceptions | an input shape, a pipe or a typed exception is written | [`02-dtos-validation.md`](./references/02-dtos-validation.md) |
| 3 | Zod and tRPC: one source of truth, unions, routers | a shared contract, a response union or a tRPC router is written | [`03-zod-trpc.md`](./references/03-zod-trpc.md) |
| 4 | Prisma: repositories, migrations, client lifecycle, transactions | a schema, a migration, a repository or a transaction is written | [`04-prisma.md`](./references/04-prisma.md) |
| 5 | Request pipeline: order, which component for which job, filters, serialisation, streams | a middleware, guard, interceptor, pipe or filter is written or bound | [`05-request-pipeline.md`](./references/05-request-pipeline.md) |
| 6 | Configuration, hooks, scopes, shutdown, standalone context | configuration is read, a provider needs set-up or tear-down, or the process must start and stop cleanly | [`06-config-lifecycle.md`](./references/06-config-lifecycle.md) |
| 7 | Tests, mechanical checks, read-only audit | a Nest test is written, or a backend is reviewed without being changed | [`07-testing-audit.md`](./references/07-testing-audit.md) |

## Output / checkpoint
Code compliant with the sections read for the change. No dedicated checkpoint: compliance is checked by `gate`
(7) and `review` (8), like the rest of the code produced at the `code`/`tdd` step. For an audit: the finding list
of `references/07-testing-audit.md`, with the unread areas named.

## Guardrails
No comments in the code produced. Never an install: name the package, the person runs `pnpm add <package>`
(`CONVENTIONS.md`). Never a `new Service()`: DI always goes through the constructor. `forwardRef()` as a last
resort, not as a reflex when facing a circular dependency error. Never business logic in a controller or a tRPC
router. No duplicate type definition where `z.infer` can derive the type from the schema. No `process.env` read
outside the configuration. Don't reimplement a mechanism that Nest, Prisma or tRPC already provide. In an audit,
change nothing. A rule naming a number or a default is the pinned major's; read `package.json` before applying
it to another.

## Origin
Rewritten from the NestJS documentation (`nestjs/docs.nestjs.com`, MIT licence, the version-12 content), read on
2026-10-02, and from the sources listed with the dogfood record in
[`references/origin.md`](./references/origin.md). Read that file when checking freshness, not when applying a
rule.
