# vue-nuxt-vuetify-conventions §2 — Composables and stores

> Section 2 of `skills/vue-nuxt-vuetify-conventions`. Read it when logic moves out of a component, or a store is touched. The other sections and the guardrails stay in `SKILL.md`.

1. **A composable owns exactly one domain**, and a function lives in the composable whose subject it
   matches — a contract-sync function belongs in the contract composable, never in the contract-line one.
   The name is a promise about what's inside; "I was already in this file" is how that promise breaks.
2. **No namespace stutter**: a member reached through something that already names its domain doesn't repeat
   it. `useContract().sync()`, not `useContract().syncContract()`.
3. A store (Pinia or equivalent) is for state genuinely shared across **unrelated** components or pages.
   Everything else stays a composable, a `ref`, or an SSR-safe shared state primitive — a store used as a
   convenient global is how state becomes untraceable.
4. `defineStore()` is called once at module level, never inside a `setup()`/composable/function body:
   otherwise each call recreates a store definition instead of reusing the shared singleton.
5. Async loading and error state belong to whatever owns the fetch, exposed explicitly (`data`, `pending`,
   `error`), never inferred by the caller from a null check.
6. A data-fetching composable carries its own fetch and returns `data`/`refresh`.
