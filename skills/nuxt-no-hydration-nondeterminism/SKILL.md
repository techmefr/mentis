---
name: nuxt-no-hydration-nondeterminism
description: "Use when a synchronous setup() or a computed reads Date.now(), Math.random(), or window/document/navigator/localStorage: never — isolate it in onMounted, import.meta.client, or ClientOnly."
---

# nuxt-no-hydration-nondeterminism

Narrow trigger extracted from `skills/vue-nuxt-vuetify-conventions` §9.1–§9.2, so a
non-deterministic or client-only read routes here directly instead of only through the whole
Nuxt/Vue block.

## When
Writing or reviewing code that reads `Date.now()`, `Math.random()`, or `window`/`document`/
`navigator`/`localStorage` at the level of a synchronous `setup()` or inside a `computed` getter.

## Steps
1. **Never call these at the level of synchronous `setup()`**: those globals don't exist server-side,
   and a non-deterministic value diverges between the server render and the client render — a
   hydration mismatch.
2. **The same rule applies inside a `computed` getter** — a `computed` is evaluated server-side too,
   so it is not a safe place to reach for these either.
3. **Isolate the read** in `onMounted` (runs client-only, after hydration), behind
   `import.meta.client`, or inside `<ClientOnly>`.

## Output / checkpoint
No direct `Date.now()`/`Math.random()`/`window.`/`document.`/`navigator.`/`localStorage.` call sits
at the top level of `setup()` or inside a `computed` getter — every such read is wrapped in
`onMounted`, guarded by `import.meta.client`, or moved inside `<ClientOnly>`.

## Guardrails
- The failure this produces is a hydration mismatch, not a crash — it can look like flicker or a
  console warning rather than a clear error, which is why it survives review.
- The choice of data primitive (`useFetch`/`useAsyncData`/`$fetch`/`useState`/`useCookie`) for actual
  async or shared state lives in `skills/vue-nuxt-vuetify-conventions` §9.3 — read it once the
  nondeterminism is isolated and the question becomes "where does this state live".

## Origin
No external source: this is `skills/vue-nuxt-vuetify-conventions` §9.1–§9.2 extracted to its own
trigger. Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
