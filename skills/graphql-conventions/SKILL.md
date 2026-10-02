---
name: graphql-conventions
description: "Use when designing or reviewing a GraphQL API: schema naming and nullability, mutation payloads, pagination, evolving the schema without versions, errors, authorization placement, batching and demand control."
paths: "**/*.graphql, **/*.gql, **/schema.*, **/resolvers/**, **/graphql/**"
---

# graphql-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the design and review of a GraphQL API, whatever the server
language; `skills/api-design` stays the block for HTTP and gRPC contracts. Every rule below holds in a repo with
**nothing installed** (`CONVENTIONS.md`, rule A). **Special status**: like `go-conventions`, no in-house
production experience sits behind this block yet. The content comes from the GraphQL project's learning
guides, read on 2026-10-02 on their main branch; the guides themselves say they are conventions, not gospel, and
the GraphQL-over-HTTP specification they cite was still a draft, so treat this as a base to confront with the
first real GraphQL service, not as proven doctrine.

## When
As soon as a schema, a resolver, a mutation, a pagination field or the HTTP serving of a GraphQL endpoint is
designed or modified, during `design` or `code` (6).

## Steps

**Read only the sections the task touches.** One file per section under `references/`.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Schema: naming, nullability, mutations, pagination, evolution | a type, a field, an argument, a mutation or a deprecation is written | [`01-schema-design.md`](./references/01-schema-design.md) |
| 2 | Server: errors, authorization, batching, HTTP, demand control | a resolver, an error path, an authorization check, the endpoint or an abuse limit is written | [`02-server-security.md`](./references/02-server-security.md) |

## Output / checkpoint
A schema and resolvers compliant with the sections read; the project's schema lint and breaking-change check
green where it has them; every list field either paginated or bounded; no authorization decision inside a
resolver body. Checked by `gate` (7) and `review` (8). Where the project cannot run its toolchain (no
environment), the checkpoint records it rather than reporting a pass, and nothing is installed to make it run
(`CONVENTIONS.md`: a block names a dependency and stops).

## Guardrails
No comments in the code produced (schema descriptions are documentation and stay). These rules govern **new**
schema; a published field is never removed or retyped to satisfy a rule, it is deprecated (§1.9). Never loosen a
limit or an authorization rule to get a diff through. For the error body outside GraphQL and for
idempotency, `skills/api-design`; for authentication and sessions, `skills/auth-session-conventions`.

## Origin
Rewritten from the GraphQL project's learning guides; the full provenance, licence and the audit of what was left
out are in [`references/origin.md`](./references/origin.md). Read it when checking a rule's freshness, not when
applying one.
