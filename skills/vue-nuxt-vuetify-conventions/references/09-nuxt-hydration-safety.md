# vue-nuxt-vuetify-conventions §9 — Nuxt: hydration safety and the choice of data primitive

> Section 9 of `skills/vue-nuxt-vuetify-conventions`. Read it when SSR, `useFetch`/`useAsyncData`, or a value that only exists client-side. The other sections and the guardrails stay in `SKILL.md`.

1. **Never** `Date.now()`, `Math.random()`, or any direct `window`/`document`/`navigator`/`localStorage`
   access at the level of the synchronous `setup()`: those globals don't exist server-side, and a
   non-deterministic value diverges between the two renders (hydration mismatch). Isolate it in
   `onMounted`, behind `import.meta.client`, or in `<ClientOnly>`.
2. The same rule inside a `computed` getter: a `computed` is evaluated server-side too.
3. Choice of data primitive according to the need:
   - `useFetch`: a simple call tied to the component's lifecycle, automatic cache/dedup.
   - `useAsyncData`: transformation/aggregation before returning, or several sources combined.
   - `$fetch`: an imperative call outside the render cycle (form submit, user action).
   - `useState`: SSR-safe shared state between components (not a classic global `ref`).
   - `useCookie`: state that has to survive a reload and be readable server-side.
   - `useRequestFetch`: a server call that has to forward the incoming request's headers/cookies.
4. **`useAsyncData`/`useFetch` should get an explicit string key by default, not only inside a loop.** The
   auto-derived key is built from the file path and line number: fine for a single static call, but it
   collides or drifts as soon as the call site isn't singular — inside a loop (the classic case, always a
   unique key per iteration), inside a dynamic/conditionally-rendered component, or after a refactor that
   moves the line. An explicit key is the cheap default; relying on the auto-derived one is the exception
   to justify, not the other way round.
5. **Nuxt 4: `useAsyncData`/`useFetch`'s returned `data` is a `shallowRef`, not a deep `ref`.** Mutating a
   nested property (`data.value.items.push(x)`, `data.value.user.name = x`) no longer triggers a
   re-render — only replacing the whole object does. Code that mutated the fetched object in place under
   Nuxt 3 goes silently stale under Nuxt 4; replace the object (`data.value = { ...data.value, items:
   [...] }`) or reach for `useState`/a store when nested mutation is genuinely needed. [Nuxt 4 upgrade
   guide, nuxt.com/docs/4.x/getting-started/upgrade, read 2026-08-10.]
6. `routeRules` (`nuxt.config`) to arbitrate rendering per route (`ssr: false`, `prerender`, `swr`, cache)
   rather than conditionals in every page.
7. Lazy hydration (`<Lazy...>`, `hydrate-on-visible`/`hydrate-on-interaction`) for any heavy component
   outside the initial viewport.
8. **Client-side error handling has its own toolkit, distinct from the server-side `createError()` in
   §11.6**: `error.vue` at the app root replaces the page for a fatal/unhandled error; `NuxtErrorBoundary`
   wraps a section of the tree so one widget failing doesn't take down the whole page (a dashboard with
   independent cards is the textbook case); `useError()` reads the current global error reactively;
   `showError()`/`clearError()` set/clear it programmatically; `onErrorCaptured` (component tree) and the
   `vue:error` hook (anything that reaches the top) are the two places to intercept before Nuxt's default
   handling takes over. A `useFetch`/`useAsyncData` call that never reads its `error` return value is
   swallowing a real failure state silently rather than handling it. [nuxt.com/docs/getting-started/
   error-handling, read 2026-08-10.]
9. **Checklist before merging a page/component**: no non-deterministic value outside a client hook; the
   fetch primitive matches the need; no nested mutation relied on for reactivity on a Nuxt 4 fetch result;
   no data leaking between requests through module-level state; `routeRules` set if the page needs a
   non-default rendering mode; a fetch's `error` state is read and handled, not just its `data`.
