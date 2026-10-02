---
name: typescript-patterns
description: "Use when writing or reviewing pure TypeScript or JavaScript whatever the framework: advanced types, async patterns, closures, immutability, error narrowing, browser platform habits, compiler configuration, trust boundaries and dates. Nuxt, React and NestJS have their own blocks."
---

# typescript-patterns

Step 6 of the pipeline (`WORKFLOW.md`), upstream of the framework blocks: the language itself,
before the Nuxt/React/NestJS layer that stacks on top.

## When
As soon as TS/JS is written or reviewed, on any stack: this block is the common base, the framework
conventions apply on top of it, not instead of it.

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; a section read is a section that has to be applied. If you are reviewing a whole diff,
pick the rows whose trigger the diff meets, not the whole table.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Typing: avoid the fake-typed | a type is written, an `any` or an assertion is tempting, or a union could replace optional fields | [`01-typing.md`](./references/01-typing.md) |
| 2 | Async | a promise is created, awaited or left running | [`02-async.md`](./references/02-async.md) |
| 3 | Immutability and closures | a variable is declared, an argument is modified, a callback is made in a loop, or an enum is considered | [`03-immutability-closures.md`](./references/03-immutability-closures.md) |
| 4 | Errors, narrowing, exhaustiveness | an error is caught, a union is branched on, a type predicate or a branded type is written, absence is modelled | [`04-errors-narrowing-exhaustiveness.md`](./references/04-errors-narrowing-exhaustiveness.md) |
| 5 | JavaScript platform habits in the browser | JSON round-trips, a request from a page, a listener, timer or observer, a URL, DOM writes, internationalised formatting, on-demand loading (the browser-owned side is `skills/browser-runtime`) | [`05-browser-javascript.md`](./references/05-browser-javascript.md) |
| 6 | Compiler configuration and the type-check gate | a `tsconfig` changes, an option is switched off, a build is trusted as a type check | [`06-compiler-configuration.md`](./references/06-compiler-configuration.md) |
| 7 | Trust boundaries, serialisation, dates | data arrives from outside, a value is copied or serialised, a date or time zone is handled | [`07-trust-boundaries-and-dates.md`](./references/07-trust-boundaries-and-dates.md) |
| 8 | Function and type design | a signature, a constant, a generic or a public module boundary is designed | [`08-function-and-type-design.md`](./references/08-function-and-type-design.md) |
| 9 | Node runtime: streams, shutdown, a process that will not exit | code runs on Node and handles a large flow of data, must stop cleanly, or hangs after the work is done | [`09-node-runtime.md`](./references/09-node-runtime.md) |

## Output / checkpoint
Code compliant with the sections above, checked on top of the applicable framework conventions
(`vue-nuxt-vuetify-conventions`/`react-nextjs-conventions`/`nestjs-node-conventions`) through `gate`
(7) and `review` (8).

## Guardrails
No comments in the code produced. Don't impose a typing style stricter than what the project's
`tsconfig.json` already requires (`strict`, `noImplicitAny`): align on the real config, not on a
theoretical ideal the repo doesn't apply. §6 describes a new project's starting point; an existing one
raises strictness as a planned change of its own. The browser section (§5) is platform behaviour and
applies to any code that runs in a page, whichever framework renders it.

## Origin
Internal synthesis based on the operator's real production experience and established TypeScript
recommendations; sections 4 to 7 added 2026-10-02 from the platform and language documentation and a
read of a public rules repository. The full provenance, the source stamps and the refresh log are in
[`references/origin.md`](./references/origin.md). Read it when checking whether a rule is still current,
not when applying one.
