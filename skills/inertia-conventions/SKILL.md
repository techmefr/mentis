---
name: inertia-conventions
description: Use when writing or reviewing a Laravel + Inertia.js app (Vue, React or Svelte pages rendered from Laravel controllers with no separate REST API) — controller-returns-a-page-with-props instead of JSON, shared data via HandleInertiaRequests, useForm for submissions and validation errors, partial/lazy/deferred reloads, and why laravel-conventions' REST/lomkit assumptions and the Nuxt-runtime parts of vue-nuxt-vuetify-conventions or react-nextjs-conventions' App Router parts don't apply here. Self-contained, it assumes no plugin or catalogue installed.
---

# inertia-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames a Laravel + Inertia.js app: **one monolith, no separate
API**. A Laravel controller returns a page component name and its props directly; Inertia hands them to
a Vue/React/Svelte component and swaps it in without a full page reload. There is no JSON contract
between two deployed apps, because there's only one app.

**This is the one place laravel-conventions and the Vue/React frontend blocks genuinely disagree with
Inertia, not just with each other** — see §4, read it before applying either block wholesale to an
Inertia repo.

## When
As soon as an Inertia page component, a controller returning `Inertia::render(...)`, the
`HandleInertiaRequests` middleware, or a `useForm`/page-props usage is written or modified.

## Steps

### 1. The controller owns the page, not an API endpoint
1. **A controller action returns `Inertia::render('Page/Name', [...])`**, not a JSON resource. The
   second argument is exactly the page component's props — there is no separate serialisation layer to
   design, and no REST resource class needed for a page's own data.
2. **Never build a JSON API endpoint whose only consumer is the page itself.** If a component's data
   comes from `Inertia::render`'s props, adding a `fetch`/`axios` call to a matching API route duplicates
   the same data through two paths that can now disagree. An endpoint is only justified when something
   genuinely needs to poll or be called from outside a full Inertia visit (e.g. a live search-as-you-type
   suggestion list, a webhook).
3. **Routing is Laravel's, entirely.** No client-side router (`vue-router`, `react-router`) — Inertia
   intercepts `<Link>` clicks and `router.visit()` calls and asks Laravel's own router for the next
   page. A route that exists on the frontend but not in `routes/web.php` doesn't exist.

### 2. Shared data and page props
1. **Data every page needs (the authenticated user, flash messages, feature flags) goes through
   `HandleInertiaRequests::share()`**, once, not repeated in every controller's props array. A prop
   duplicated across twenty controllers because nobody centralised it is the tell that it belongs in
   `share()`.
2. **Props are the page's contract with its controller — type them.** Generate the frontend type from
   the same Laravel Data DTO/resource the controller returns rather than hand-writing a parallel
   interface that can drift from what the backend actually sends.
3. **Partial reloads (`only`/`except`) for a page that re-visits itself with unchanged sections** (a
   filtered table re-requesting only the table's data, not the whole page's props again) — cheaper than
   a full prop payload, and the reason to reach for it is a measured or obvious cost, not a default on
   every visit.
4. **A prop that's expensive to compute and not needed for the first paint is `Inertia::lazy()`/deferred**
   rather than computed eagerly on every request that touches the page, including ones that never scroll
   to where it's used.

### 3. Forms, validation and errors
1. **`useForm` owns a form's state, submission and error display** — not a hand-rolled `ref`/`useState`
   plus a manual `axios.post` plus manually reading a caught error's response body. `useForm` already
   wires the request, the pending/processing flag, and the validation-errors bag together.
2. **Validation stays server-side, in a FormRequest, the same as any other Laravel controller** — a
   thrown `ValidationException` arrives back as the page's `errors` prop automatically; there's no
   separate error-shape contract to invent for Inertia.
3. **Real-time (as-you-type) validation feedback, where the UX genuinely needs it, uses Laravel's own
   precognition mechanism** rather than a hand-rolled debounced validation endpoint — it reuses the same
   FormRequest rules the real submission will run, so the two can't drift apart.

### 4. Where this overrides laravel-conventions and the frontend blocks
1. **`laravel-conventions` §6's REST/resource-routing and lomkit-filters guidance is written for an API
   backend serving a separately deployed frontend.** An Inertia app has no such boundary: a page's data
   is passed as props, not filtered through a REST resource collection, so there's no lomkit-vs-custom
   endpoint decision to make for page data at all. `laravel-conventions`' other sections (thin models,
   events over observers, action classes, config/env discipline, testing tiers) still apply unchanged —
   only the HTTP-surface-as-a-REST-API assumption doesn't.
2. **The Nuxt-specific parts of `vue-nuxt-vuetify-conventions`** (Nuxt's file-based routing, auto-imports,
   `useFetch`/`useAsyncData`, the Nuxt directory layout, Nuxt's own SSR runtime) **don't apply**: there is
   no Nuxt app, no Nuxt server, no Nuxt-owned routing. An Inertia+Vue page is a plain Vue 3 SFC wired by
   Inertia, so that block's language- and component-level Vue guidance (SFC shape, composables that
   aren't Nuxt-specific, typing, naming, accessibility in templates) still applies; its Nuxt-runtime
   sections don't have an equivalent here.
3. **The Next.js-App-Router-specific parts of `react-nextjs-conventions`** don't apply for the same
   reason when the frontend is React: no Next.js server, no App Router, no Next data-fetching primitives
   — Inertia is the data-fetching and routing layer instead. That block's plain React/component-level
   guidance still applies.
4. **When a reviewer (human or an agent) flags an Inertia app for "missing a REST API" or "not using
   Nuxt/Next conventions," that's this conflict surfacing** — point them here rather than adding either
   layer on top of Inertia; a Laravel+Inertia app doesn't need a REST API or a meta-framework runtime
   to be conventional, it needs Inertia's own conventions applied consistently.

### 5. Tests
1. **A feature test for an Inertia route asserts the page component name and its props**, not a JSON
   body shape — Laravel's Inertia testing assertions (asserting the component and specific prop values)
   are the equivalent of a JSON-shape assertion on an API endpoint, just aimed at what Inertia actually
   returns.
2. **The two-tier split from `laravel-conventions` §9 still applies**: an Inertia-returning controller
   action is a feature test, the same as any other HTTP endpoint would be.

## Output / checkpoint
Code compliant with the sections above: controllers returning pages with typed props (no shadow JSON
API for page-only data), shared data centralised in `HandleInertiaRequests`, forms on `useForm`, and no
Nuxt/Next-runtime or REST/lomkit expectation applied where §4 says it doesn't hold.

## Guardrails
- Never add a JSON API endpoint whose only purpose is feeding data a controller could pass directly as
  Inertia props.
- Never apply `laravel-conventions` §6's REST-resource/lomkit guidance to an Inertia page's own data —
  that section is for an actual API backend, which an Inertia app isn't.
- Never treat a missing Nuxt/Next-specific pattern (file routing, `useFetch`, the App Router) as a defect
  in an Inertia repo — there's no meta-framework runtime there to begin with.
- Never hand-roll form submission/error-display state where `useForm` already does the job.
- Existing endpoints genuinely consumed by something other than the page itself (a public API, a mobile
  client, a webhook) are a real REST surface and `laravel-conventions` §6 applies to them normally — §4's
  override is scoped to page-only data, not to every endpoint in an Inertia repo.

## Origin
Sourced from the official Inertia.js documentation (shared data via `HandleInertiaRequests`, `useForm`,
partial reloads, lazy/deferred props) and current Laravel+Inertia integration practice (typed props
generated from the same DTO/resource the backend returns, Laravel Precognition for real-time validation
reusing the submission's own FormRequest rules). §4 (the override table against `laravel-conventions` and
the Nuxt/Next-specific blocks) is ours: written after a real conflict surfaced where an Inertia repo was
reviewed against REST/lomkit and Nuxt-runtime expectations that don't hold for that architecture — no
existing skill named the boundary, in this repo or in the installed `xefi-claude-skills` marketplace
(`laravel`/`nuxt` plugins), which don't cover Inertia either. No dedicated in-house Inertia production
experience yet: a solid base from the framework's own documentation, not proven doctrine. Stamped
2026-08-11.
