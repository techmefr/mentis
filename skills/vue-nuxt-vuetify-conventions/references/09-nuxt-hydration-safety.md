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
   Nuxt 3 goes silently stale under Nuxt 4; replace the object with a fresh spread, or reach for
   `useState`/a store when nested mutation is genuinely needed. [Nuxt 4 upgrade guide,
   nuxt.com/docs/4.x/getting-started/upgrade, read 2026-08-10.]
6. `routeRules` (`nuxt.config`) to arbitrate rendering per route (`ssr: false`, `prerender`, `swr`, cache)
   rather than conditionals in every page.
7. Lazy hydration (`<Lazy...>`, `hydrate-on-visible`/`hydrate-on-interaction`) for any heavy component
   outside the initial viewport.
8. **Client-side error handling has its own toolkit, distinct from the server-side `createError()` in
   §11.10**: `error.vue` at the app root replaces the page for a fatal/unhandled error;
   `NuxtErrorBoundary` wraps a section of the tree so one widget failing doesn't take down the whole page
   (a dashboard with independent cards is the textbook case); `useError()` reads the current global error
   reactively; `showError()`/`clearError()` set/clear it programmatically; `onErrorCaptured` (component
   tree) and the `vue:error` hook (anything that reaches the top) are the two places to intercept before
   Nuxt's default handling takes over. A `useFetch`/`useAsyncData` call that never reads its `error`
   return value is swallowing a real failure state silently rather than handling it.
   [nuxt.com/docs/getting-started/error-handling, read 2026-08-10.]
9. **"It looks fine" is not evidence of hydration safety.** Vue reconciles some divergences without
   telling the user, and the ones it cannot reconcile it patches at a cost, so a mismatch routinely ships
   looking correct and surfaces later as a wrong attribute, a lost event listener or a flicker on one
   browser. The dev-mode warning is the actual signal — read the console on the page you changed rather
   than concluding from the screenshot.
10. **`<ClientOnly>` is a hole in the server render, not a free escape hatch.** The subtree is absent from
    the HTML, so the user gets a gap and then a pop-in, and any content inside it is invisible to a
    crawler. Give it a `fallback` sized like the real thing, and wrap the smallest possible part — a whole
    page inside `<ClientOnly>` is a single-page app with an SSR bill attached.
11. **Everything a server-side fetch returns is serialised into the HTML payload.** The `data` a page
    fetched during SSR is embedded in the page source, so a query that selects more than the template
    renders ships those fields to the browser in plain sight — including the ones authorisation was
    supposed to keep out — and inflates the document for every visitor. Select what the screen needs, on
    the server side.
12. **`useFetch` runs on the server and again on the client unless the payload is reused.** The dedup and
    the key are what make it one request (point 4); a hand-rolled guard around a fetch is the usual sign
    that the primitive is being fought rather than configured, and it trades a double request for a page
    that renders empty on the server.
13. **A server-side call to your own API is anonymous unless the request context is forwarded.** Cookies
    and headers do not travel automatically, so the same endpoint answers 200 in the browser and 401
    during SSR — which reads as a flaky backend. That is what `useRequestFetch` is for (point 3), and the
    choice is worth stating explicitly at the call site.
14. **The server has no browser locale or timezone.** A date or number formatted during SSR uses the
    server's settings, so it renders one way in the HTML and another after hydration — visibly, on the
    first paint. Decide whose timezone the value is in (§6.10) and format on the side that knows it.
15. **Checklist before merging a page/component**: no non-deterministic value outside a client hook; the
    fetch primitive matches the need; an explicit key on every `useFetch`/`useAsyncData`; no nested
    mutation relied on for reactivity on a Nuxt 4 fetch result; no data leaking between requests through
    module-level state; nothing in the SSR payload the template does not render; `routeRules` set if the
    page needs a non-default rendering mode; a fetch's `error` state read and handled, not just its
    `data`; and the dev console clean of hydration warnings on the page you touched.
