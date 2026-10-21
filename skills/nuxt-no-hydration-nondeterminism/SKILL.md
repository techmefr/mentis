---
name: nuxt-no-hydration-nondeterminism
description: "Use when a synchronous setup() or a computed reads Date.now(), Math.random(), or window/document/navigator/localStorage: never — isolate it in onMounted, import.meta.client, or ClientOnly."
---

# nuxt-no-hydration-nondeterminism

Narrow trigger extracted from `skills/vue-nuxt-vuetify-conventions` section 9 (9.1 and 9.2), so a
non-deterministic or client-only read routes here directly instead of only through the whole
Nuxt/Vue block.

## When
Writing or reviewing code that reads `Date.now()`, `Math.random()`, `new Date()`, the time zone, or
`window`/`document`/`navigator`/`localStorage` at the level of a synchronous `setup()` or inside a
`computed` getter.

## Steps
Source marks `[src N]` are the rows of the table in [`references/origin.md`](./references/origin.md).
1. **Never call these at the level of synchronous `setup()`**: the browser globals don't exist
   server-side (they throw there), and a non-deterministic value diverges between the server render
   and the client render, which is a hydration mismatch. [src 1,2]
2. **The same rule applies inside a `computed` getter**: a render on the server reads it too, so it
   is not a safe place to reach for these either. (The Vue page says reactivity is switched off on the
   server; it does not say computed values are skipped, and a value read by the template is
   evaluated once there.) [src 2]
3. **Isolate the read** in `onMounted` (never called during server rendering) or inside `<ClientOnly>`
   (its default slot is dropped from the server build; give it a `#fallback` for the server markup).
   An `import.meta.client` guard keeps a server-unsafe call from running, but it is not enough in
   `setup()` for a library that edits the DOM: the Nuxt guide moves that to `onMounted`. [src 1,3,4]
4. **Prefer a value both sides agree on over hiding it.** For a stored preference, `useCookie` is
   readable on the server; for a random or time-based value that must be shown in the first paint,
   `useState` computes it once on the server and the client reuses it; `NuxtTime` renders dates
   consistently; for layout switches use CSS media queries instead of reading `window.innerWidth`. [src 3]
5. **Time zones are a source too.** A timestamp turned into the user's local time differs when the
   server and the browser sit in different zones: do the conversion client-only. [src 2]
6. **Other mismatch causes to rule out when the warning persists:** HTML the browser rewrites
   (`<div>` inside `<p>`), phone numbers and dates that iOS Safari wraps in links before hydration
   (disable detection with a `format-detection` meta tag, and wrap a number you want tappable in a
   `tel:` link in the server markup), and third-party scripts such as tag managers that edit the DOM
   (initialise them in `onMounted`). [src 2,3]
7. **Keep cleanup-needing side effects out of `setup()`.** `onUnmounted` never runs on the server, so
   a timer started at the top level leaks there; start it in `onMounted`. [src 2]

## Output / checkpoint
No direct `Date.now()`/`Math.random()`/`new Date()`/`window.`/`document.`/`navigator.`/`localStorage.`
call sits at the top level of `setup()` or inside a `computed` getter: every such read is wrapped in
`onMounted`, moved inside `<ClientOnly>`, or replaced by `useState`/`useCookie`/`NuxtTime`.

## Guardrails
- The failure is a hydration mismatch, not a crash: in development a console warning, in production
  Vue patches the DOM to match the client, which costs rendering time and can show flicker; the Nuxt
  page also lists dead event listeners and diverging state as possible consequences. Treat the warning
  as a bug, not noise. [src 3]
- Suppressing a mismatch (`data-allow-mismatch`, Vue 3.5+) is for unavoidable cases only; it does
  not fix a divergent value. [src 2]
- The choice of data primitive (`useFetch`/`useAsyncData`/`$fetch`/`useState`/`useCookie`) for actual
  async or shared state lives in `skills/vue-nuxt-vuetify-conventions` section 9.3: read it once the
  nondeterminism is isolated and the question becomes "where does this state live".

## Origin
`skills/vue-nuxt-vuetify-conventions` section 9.1 and 9.2 extracted to its own trigger (2026-09-09), then checked
against the Nuxt and Vue documentation on 2026-10-20 (MIT and CC BY 4.0), rewritten in our own words.
🟡 never run. Details and the open points: [`references/origin.md`](./references/origin.md).
