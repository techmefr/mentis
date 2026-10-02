# nestjs-node-conventions §3 — Cross-cutting type-safe contracts (Zod and tRPC)

> Section 3 of `skills/nestjs-node-conventions`. Read it when a shared contract, a response union or a tRPC router is written. The other sections and the guardrails stay in `SKILL.md`.

1. At the boundaries where the contract has to be shared with a type-safe client (tRPC), derive the type
   from the validation schema with `z.infer<typeof schema>` rather than maintaining a TypeScript interface
   alongside the Zod schema: a single source of truth, never two definitions that can diverge.
2. Heterogeneous API responses (success/error, several result variants) modelled as a discriminated union
   (`{ status: 'ok', data } | { status: 'error', message }`) with an explicit discriminant field, never an
   object with optional fields the caller has to guess at.
3. tRPC tree organised by business domain, symmetric to the Nest modules: one router per domain
   (`usersRouter`, `ordersRouter`), composed into a root `appRouter`; each procedure (`query`/`mutation`)
   validates its input with a Zod schema passed to `.input()`.
4. The procedure's Zod schema and the equivalent REST controller's `class-validator` DTO describe the same
   data shape: when a single use case is exposed twice (REST + tRPC), check they don't diverge silently
   rather than letting them evolve independently.
