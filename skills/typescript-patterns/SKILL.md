---
name: typescript-patterns
description: Use when writing or reviewing pure TypeScript/JavaScript, whatever the framework (not Nuxt, not React, not NestJS, those are vue-nuxt-vuetify-conventions/react-nextjs-conventions/nestjs-node-conventions), advanced types, async patterns, closures, immutability. Real production experience on the operator's side with this language.
---

# typescript-patterns

Step 6 of the pipeline (`WORKFLOW.md`), upstream of the framework blocks: the language itself,
before the Nuxt/React/NestJS layer that stacks on top.

## When
As soon as TS/JS is written or reviewed, on any stack: this block is the common base, the framework
conventions apply on top of it, not instead of it.

## Steps

### 1. Typing: avoid the fake-typed
1. `any` never used to avoid thinking about the real type: `unknown` + narrowing if the type really
   is unknown at that point in the code.
2. Type assertion (`as`) only when TypeScript structurally cannot infer (e.g. the result of
   `JSON.parse`), never to silence a legitimate type error.
3. Derived types (`ReturnType`, `Parameters`, `Pick`/`Omit`, mapped types) rather than duplicating a
   data shape already declared elsewhere: a duplicated type diverges silently from the first one at
   the first refactor.
4. `interface` for an extensible shape (object, public contract), `type` for a
   union/intersection/alias: no rule that opposes them out of dogma, but no random choice either.
5. Discriminated unions (`{ type: 'a', ... } | { type: 'b', ... }`) rather than one object with all
   fields optional and nullable to represent mutually exclusive states.

### 2. Async: the number one source of silent bugs
1. A `Promise` never left dangling without an `await` or an explicit `.catch`; a rejected promise
   that isn't handled is a silent crash or an unhandled rejection.
2. `Promise.all` for independent operations, never a serial `await` in a loop out of reflex when
   parallelism is possible and safe (no dependency between them).
3. `async` on a function that does nothing asynchronous is a signal to remove, not a neutral style.
4. The classic race condition: two `await`s modifying the same shared state with no logical lock
   (e.g. two calls that read then write the same variable): check the real execution order, not the
   apparent order in the code.

### 3. Immutability and closures
1. `const` by default, `let` only if reassignment is genuinely necessary: never `var`.
2. A closure inside a loop captures the reference, not the value at creation time: a classic trap
   with `var`, less so with `let`/`const` but worth checking if an array of callbacks is built
   dynamically.
3. Mutating an object/array received as a parameter = a side effect invisible to the caller: return a
   copy (spread, `structuredClone`) if the contract isn't explicitly "I mutate in place".
4. Native TS `enum` avoided in favour of an `as const` object + a derived type
   (`typeof X[keyof typeof X]`): the native enum generates superfluous runtime JS and behaves
   differently under `isolatedModules`.

## Output / checkpoint
Code compliant with the three sections above, checked on top of the applicable framework conventions
(`vue-nuxt-vuetify-conventions`/`react-nextjs-conventions`/`nestjs-node-conventions`) through `gate`
(7) and `review` (8).

## Guardrails
No comments in the code produced. Don't impose a typing style stricter than what the project's
`tsconfig.json` already requires (`strict`, `noImplicitAny`): align on the real config, not on a
theoretical ideal the repo doesn't apply.

## Origin
Internal synthesis based on the operator's real production experience (long-standing JS/TS, see
`frodo`/`legolas`) and established TypeScript recommendations (official handbook on discriminated
unions, `as const`). No single external repo retained: this is a language block, not a framework one,
so there's no "expert X" source to credit as with the market-sourced framework conventions.
