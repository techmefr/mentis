---
name: vue-router-pitfalls
description: "Use when code navigates or configures Vue Router: router.push with params and paths, awaiting a navigation and reading its failure (aborted, cancelled, duplicated, redirected), routes added at runtime, navigation guards (return values, redirect loops, the legacy next callback, beforeEnter limits, beforeResolve versus beforeEach), route components reused when params change, lazy-loaded route components, catch-all and history-mode fallbacks, scroll behaviour, and typed routes."
---

# vue-router-pitfalls

A defensive block for the router layer of a Vue 3 app, written for plain Vue Router. The four parts share one
premise: **a navigation is asynchronous and can end without the user arriving, in several different ways,
and most router bugs come from code that assumes it simply succeeded** (a menu closed, a toast shown, a fetch fired for a page the user never
reached). Component conventions, stores and Vuetify are in `skills/vue-nuxt-vuetify-conventions`; Nuxt's own
file-based routing and its route middleware were not read for this block and are out of scope; testing a
component that uses the router is in `skills/vue-test-utils-pitfalls`.

## When
- A call to `router.push`, `router.replace` or a `RouterLink` `to` carries params, a path built from user text,
  or code that runs after the navigation.
- A guard is written, or a login redirect loops, or a guard seems not to run when only a param changed.
- A page does not refresh when going from one id to another, or a fetch fires twice.
- Route components are imported, split into chunks, or wrapped as async components.
- Scroll position is wrong after navigating, or links to anchors land under a fixed header.
- Routes are added after start-up, or the router is given typed route names.

## Steps

**Read only the part the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Locations (name versus path, params, encoding), awaiting a navigation, failure types, redirects, runtime routes | code navigates or reacts to the result of a navigation | [`01-locations-and-navigation-results.md`](./references/01-locations-and-navigation-results.md) |
| 2 | Guards: return values, loops, `next`, order, per-route and in-component limits, resolve guard, after hooks | a guard or a redirect rule is written or breaks | [`02-guards.md`](./references/02-guards.md) |
| 3 | Reused components, watching params, lazy loading, async components, 404 and history fallback, memory history | a page shows stale data, chunks are split, or a deep link gives 404 | [`03-route-components-and-history.md`](./references/03-route-components-and-history.md) |
| 4 | Scroll behaviour and typed routes | scroll restoration or anchors misbehave, or route names and params should be checked by the compiler | [`04-scroll-and-typed-routes.md`](./references/04-scroll-and-typed-routes.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a navigation was awaited and a guard that returns `false`
produced a failure value (part 1.2), a guard was triggered by a param-only change to see that a per-route guard
does not run (part 2.4), a component was navigated from one id to the next and the fetch ran again (part 3.1), a
deep link was requested from the server that serves the built app (part 3.4), and a navigation to a missing
route name failed the type check (part 4.4). A router configuration that was only read is not verified.

## Guardrails
- Never act on `await router.push(...)` as if it meant "arrived": test the resolved value (part 1.2).
- Never pass `params` together with `path`; use a route name, or encode each segment yourself (part 1.1).
- Never return a redirect from a guard without a condition that stops it on the target (part 2.2).
- Never call the legacy `next` twice on one path through a guard (part 2.3).
- Never rely on `beforeEnter` for a rule that must hold when only the param, query or hash changes (part 2.4).
- Never watch the whole `route` object; watch the property you read (part 3.2).
- Never wrap a route component in `defineAsyncComponent`; give the route a function that imports it (part 3.3).
- This block states the Vue Router documentation as of the commit read on the date in
  [`references/origin.md`](./references/origin.md); the router version the pages describe was not checked, and
  nothing was run while writing the block.

## Origin
Rewritten from the Vue Router documentation (vuejs/router, MIT), read 2026-10-16. 🟡: never run by us; open
points are in [`references/origin.md`](./references/origin.md).
