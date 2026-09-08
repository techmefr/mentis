# § 4 — Where this overrides laravel-conventions and the frontend blocks

> Section 4 of `skills/inertia-conventions`. Read it before applying `laravel-conventions` §6 or either
> frontend block wholesale to an Inertia repo, and whenever a review flags an Inertia app for missing a
> REST API or a meta-framework pattern. This is the one section of this block that is ours rather than
> the framework's, and it exists because the case it resolves has already been got wrong in production.

1. **`laravel-conventions` §6's REST/resource-routing and lomkit-filters guidance is written for an API
   backend serving a separately deployed frontend.** An Inertia app has no such boundary: a page's data
   is passed as props, not filtered through a REST resource collection, so there's no lomkit-vs-custom
   endpoint decision to make for page data at all. `laravel-conventions`' other sections (thin models,
   events over observers, action classes, config/env discipline, testing tiers) still apply unchanged —
   only the HTTP-surface-as-a-REST-API assumption doesn't. Read the override narrowly: it removes one
   assumption, it does not put the block's Laravel rules aside, and a diff that drops action classes or
   the testing tiers "because it's Inertia" is not applying this section.
2. **The Nuxt-specific parts of `vue-nuxt-vuetify-conventions`** (Nuxt's file-based routing, auto-imports,
   `useFetch`/`useAsyncData`, the Nuxt directory layout, Nuxt's own SSR runtime) **don't apply**: there is
   no Nuxt app, no Nuxt server, no Nuxt-owned routing. An Inertia+Vue page is a plain Vue 3 SFC wired by
   Inertia, so that block's language- and component-level Vue guidance (SFC shape, composables that
   aren't Nuxt-specific, typing, naming, accessibility in templates) still applies; its Nuxt-runtime
   sections don't have an equivalent here. The half that still applies is the larger half — reactivity,
   component boundaries, accessibility, template discipline — so treating the whole block as inapplicable
   loses far more than it saves.
3. **The Next.js-App-Router-specific parts of `react-nextjs-conventions`** don't apply for the same
   reason when the frontend is React: no Next.js server, no App Router, no Next data-fetching primitives
   — Inertia is the data-fetching and routing layer instead. That block's plain React/component-level
   guidance still applies. Its server/client boundary rules are the ones with no equivalent: an Inertia
   page has no server components, and the boundary that matters here is the props payload (§2.6), which
   is a different mechanism with the same consequence — what crosses it is readable by the reader.
4. **When a reviewer (human or an agent) flags an Inertia app for "missing a REST API" or "not using
   Nuxt/Next conventions," that's this conflict surfacing** — point them here rather than adding either
   layer on top of Inertia; a Laravel+Inertia app doesn't need a REST API or a meta-framework runtime
   to be conventional, it needs Inertia's own conventions applied consistently. Adding the missing layer
   to satisfy the review is the expensive outcome: a REST surface nobody consumes still has to be
   authorized, versioned and tested, and it becomes a second path to the same data (§1.2).
5. **Inertia and a REST package (`lomkit/laravel-rest-api` or equivalent) are not mutually exclusive in
   the same project — they can genuinely coexist**, because they serve different surfaces: Inertia
   renders the app's own pages (`routes/web.php`, `Inertia::render(...)`), a REST package serves a real
   JSON API for a consumer that isn't the Inertia frontend (a mobile app, a partner integration, a
   versioned public API, usually under `routes/api.php`). Checking only "is the package a dependency" is
   too coarse once both are in the same project — the package being installed says nothing about which
   specific controller a mandate should apply to.
6. **Before applying any "CRUD goes through the REST package" mandate — this repo's or an installed
   house catalogue's — to a *specific* controller, check what that controller actually returns and where
   it's routed**, not just whether the package is a project dependency:
   - Returns `Inertia::render(...)`, routed under the app's own web routes → it's a page. The mandate
     doesn't apply, regardless of whether the package is installed and used elsewhere in the same
     project.
   - Returns JSON for a consumer other than the Inertia frontend (mobile, a partner, a versioned public
     API), typically under `routes/api.php` → a real REST endpoint. Where the package is installed, the
     mandate applies normally.
   - Genuinely ambiguous which of the two a given controller is → ask rather than guess; don't default
     to forcing the mandate because the package happens to be present in the project.
   This resolves the case a purely project-level dependency check gets wrong: a project using **both**
   Inertia for its pages and a REST package for a separate, real API surface — the mandate still governs
   that real API, it just never reaches the page controllers. Two checks are worth stating because they
   are the ones that look sufficient and aren't: the method name (`index`, `store`, `update` are the same
   names a page controller uses) and the package's presence in `composer.json`. Neither distinguishes the
   two surfaces; only the return value and the route file do.
7. **This whole section resolves the case, so apply it and keep going — don't tell a non-technical
   stakeholder "there's a conflict between mentis and the house rules."** That framing reads as broken,
   and a CdP with no way to judge it themselves has already responded to exactly that framing by
   deleting the whole setup and starting over. There's a resolution stated above; use it silently. The
   distinction to hold on to: a **resolved** case is applied without narration, and only a case where no
   rule anywhere decides the answer is worth raising — as one specific named question, never as a general
   alarm about two rule sets disagreeing.
8. **An installed house catalogue wins on its own subject, and this section is not a subject it covers.**
   Where a company ships its own versioned catalogue for Laravel or for the frontend framework, that
   catalogue is the authority on its house style and overrides this block wherever the two differ (§4.6
   is about how to *scope* one of its mandates, not about outranking it). But a catalogue written for a
   REST backend and a separately deployed frontend has no rule about Inertia at all: the gap this section
   fills is a gap, not a disagreement, and filling it does not put the catalogue aside anywhere else.
