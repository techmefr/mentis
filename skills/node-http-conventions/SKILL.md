---
name: node-http-conventions
description: "Use when writing or reviewing a Node.js HTTP service on Express or Fastify: async error flow, the error handler, proxy trust, security headers, schema validation and serialization, hooks, deployment shape and tests."
paths: "**/app.{js,ts,mjs,cjs}, **/server.{js,ts,mjs,cjs}, **/routes/**/*.{js,ts}, **/middleware/**/*.{js,ts}, **/plugins/**/*.{js,ts}"
---

# node-http-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of a Node.js HTTP service built on Express
or Fastify, on top of `skills/typescript-patterns` (typing, modules, the toolchain) which stays on the
language. Every rule below holds in a repo with **nothing installed** (`CONVENTIONS.md`, rule A). **Special
status**: like `go-conventions`, no in-house production experience sits behind this block yet. The content comes
from the Express 5.x guides, the Fastify documentation (main branch) and the Helmet README, all read on
2026-10-02; treat it as a base to confront with the first real service, not as proven doctrine. Express is read
at major 5 (async handlers forward rejections); on 4 the async rule in §1.1 does not hold.

## When
As soon as an Express or Fastify handler, middleware, plugin, hook, schema or server bootstrap is written or
modified, during `code` (6) or `tdd` (5).

## Steps

**Read only the section for the framework in use.** One file per section under `references/`.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Express: async errors, error handlers, proxy trust, security headers | an Express route, middleware, error handler or proxy setting is written | [`01-express.md`](./references/01-express.md) |
| 2 | Fastify: schemas, validation errors, hooks, deployment, tests | a Fastify route, schema, hook, plugin or test is written | [`02-fastify.md`](./references/02-fastify.md) |

## Output / checkpoint
Code compliant with the section read; the type check, lint and tests green; every error path reaches the error
handler; the proxy-trust setting named and justified in the diff when touched. Checked by `gate` (7) and
`review` (8). Where the project cannot run its toolchain (no environment), the checkpoint records it rather than
reporting a pass, and nothing is installed to make it run (`CONVENTIONS.md`: a block names a dependency and
stops).

## Guardrails
No comments in the code produced. These rules govern **new** code. Never loosen a validation schema, a header
or the proxy-trust setting to get a diff through. For the error body shape and idempotency,
`skills/api-design`; for authentication and sessions, `skills/auth-session-conventions`; for queues,
`skills/background-jobs-conventions`.

## Origin
Rewritten from the Express documentation, the Fastify documentation and the Helmet README; the full provenance,
licences and the audit of what was left out are in [`references/origin.md`](./references/origin.md). Read it
when checking a rule's freshness, not when applying one.
