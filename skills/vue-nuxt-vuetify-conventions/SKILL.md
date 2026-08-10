---
name: vue-nuxt-vuetify-conventions
description: Use when writing or reviewing anything on the Vue 3/Nuxt stack, the SFC shape, the composable and store discipline, typing, naming, i18n, layered structure, CSS naming, accessibility in templates, the UI-toolkit-first rule, hydration safety, the choice of data primitive, realtime events, and the correctness/security rules derived from the vue-doctor/nuxt-doctor linters. Self-contained, it assumes no plugin or catalogue installed.
---

# vue-nuxt-vuetify-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing of frontend code on the Vue 3 + Nuxt stack with a
component library. Every rule below holds in a repo with **nothing installed** — that's the point of the
block (`CONVENTIONS.md`, rule A).

**Relation to an org skill catalogue.** Where a company ships its own versioned catalogue for this stack, it
is the authority on **its** house style — its package list, its named internal libraries, its file
layout — and it overrides this block on any point where the two differ. This block is the generic default,
not a competitor: it states the rule and the reason, so an agent can apply it on a project that has no
catalogue at all, and can recognise a house override as an override rather than as a contradiction.

## When
As soon as a `.vue` component, a Nuxt page, a composable, a store or a server route is written or modified,
during `code` (6) or `tdd` (5).

## Steps

### 1. The shape of a component
1. `<script setup lang="ts">`, always. Never the Options API, never untyped JS, never a `<script>` without
   `setup`.
2. Block order fixed across the codebase (`<template>` → `<script setup>` → `<style scoped>`) so a reviewer
   reads every file the same way. `<style>` always scoped; global styles live in a project-level stylesheet.
3. One component per file. A child component declared inside another file's script is invisible to search
   and impossible to test on its own.
4. Never ship an empty `<script setup>` or an empty `<style>` block: an empty block reads as logic deleted
   halfway, and says nothing about the component's intent. Omit it.
5. **A component renders, a composable thinks.** Logic — every `ref`, watcher, handler body, fetch and
   lifecycle hook — belongs in a composable, not inline in `<script setup>`. This is the most-broken rule of
   the set, so treat extraction as the default reflex rather than something to justify.
6. Past a soft size limit (the project's, ~150–200 lines of template), split rather than scroll.
7. Use the shorthand when the prop name matches the variable being passed.
8. Props/emits/model typed at the boundary. Which form — the generic macro or the runtime/validator form —
   is a project decision, applied consistently; what is never acceptable is an untyped prop.
9. Never destructure a reactive `props` object directly (`const { foo } = props` breaks reactivity). Read
   `props.foo`, or go through `toRefs(props)` / a `computed`.
10. `shallowRef` for non-primitive state (objects, arrays, heavy DOM refs) unless the nested reactivity is
    genuinely consumed.
11. A composable returns `ref`s/`computed`s, never raw values. A parameter that may be a value or a ref is
    read with `toValue()`, never `unref()` alone (no getter support).

### 2. Composables and stores
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

### 3. Typing
1. `any` is banned; `unknown` keeps the value opaque and forces the narrowing you needed anyway. The two
   narrow exceptions — an untyped third-party lib with no shim available, and a generic parameter defaulting
   for backwards-compatible inference — stay confined to one file.
2. `import type` for type-only symbols, so the build can erase them.
3. Business types live in one predictable place per module rather than next to whichever component first
   needed them, and the project's prefix/casing convention is applied uniformly (a mixed codebase is worse
   than either convention).
4. A mapped type (`Record<K, V>`) rather than an interface with an index signature.
5. Annotate explicitly by default; fall back to inference only where the explicit type would be genuinely
   unreadable.
6. No type assertion (`as`) where a narrowing check would do: an assertion is a claim the compiler can't
   check.

### 4. Naming and style
1. Casing fixed per artefact kind (files, components, composables, stores, types, constants) and applied
   without exception.
2. Booleans prefixed `is`/`has`/`can`/`should`. `loading` is ambiguous — a boolean? a promise? a count?
   `isLoading` isn't.
3. A callback parameter is the full singular word of the collection it iterates (`post` in `posts.map`),
   never `p` or `u`. A `reduce` accumulator is named for what it accumulates (`runningTotal`, `byId`),
   never `acc`.
4. Functions declared as arrow functions assigned to a `const`, consistently — the point is one shape
   across the codebase, not a claim that `function` is broken.
5. CSS class names follow a single naming scheme, BEM by default (`.block`, `.block__element`,
   `.block--modifier`) — this is about naming, not about the preprocessor, and applies identically to plain
   CSS.
6. Class and style bindings expressed through the framework's binding syntax rather than string
   concatenation built by hand.
7. Don't hand-import what the framework auto-imports (in Nuxt: composables, components, stores, utils, and
   your own project types). A manual import line for an auto-imported symbol is noise that drifts out of
   date; the fix is usually deleting the import, not aliasing it.
8. Prefer an import alias over a relative path across folders, once the architecture linter resolves it.

### 5. Structure and dependencies
1. Separate code by **technical concern** vs **functional/business concern** (the layered/OSDD split), and
   `technical/` never imports `functional/`: if a value is missing, the caller passes it as a parameter.
2. Tests and stories sit where the project decided — a dedicated folder mirroring the source tree, or
   co-located — but the decision is uniform. Half a codebase each way costs more than either choice.
3. One package manager per project, and a curated list of approved dependencies. A new dependency is a
   decision (licence, maintenance, bundle weight), not a reflex; check what's already there first.
4. Declarative config in a `config/` folder as soon as N near-identical entities are being wired by hand
   with duplicated watchers and hardcoded arrays.
5. Look for an existing nearby component/composable before writing a new one.
6. **`runtimeConfig` vs `app.config` is a security boundary, not a style choice.** `runtimeConfig`'s
   top-level keys are server-only by default and read from `NUXT_*` environment variables (a secret goes
   here, unnested, never under `public`); only `runtimeConfig.public`/`runtimeConfig.app` cross to the
   client, and a value placed there is as exposed as if it were hardcoded in the bundle. `app.config.ts` is
   for static, non-secret, build-time values (theme tokens, feature toggles) that need hot-reload during
   dev, and **cannot** read an environment variable at all — reaching for it to keep a secret out of the
   bundle is the opposite of what it does. In a layered/OSDD project each layer's own `nuxt.config.ts`
   carries its own `runtimeConfig`, not a single root one. [nuxt.com/docs/4.x/getting-started/configuration,
   nuxt.com/docs/4.x/guide/going-further/runtime-config, read 2026-08-10.]
6. **Nuxt 4's default directory layout, on a plain repo with no layer/OSDD convention installed**:
   `srcDir` defaults to `app/` (components/composables/layouts/middleware/pages/plugins/utils/app.vue all
   move under it, and `~` now resolves to `app/` instead of the project root); `serverDir` moves the other
   way, to `<rootDir>/server` regardless of `srcDir`; `layers/`, `modules/`, `public/` stay resolved from
   `<rootDir>`; and a new `shared/` directory (`shared/utils/`, `shared/types/`) is auto-imported into both
   the Vue app and the Nitro server for code that's genuinely neither. [Same source as point 5 above,
   read 2026-08-10.] **Where `nuxt-osdd` (nuxt-osdd.xefi.com) is installed, it overrides this**: each layer
   already carries its own self-contained `app/` subtree (see that package's own structure), and this
   generic default only applies where no such layer package is installed.

### 6. i18n
1. Locale files flat, no nested objects: nesting makes a key impossible to grep and invites two keys for one
   string.
2. Keys are the full source sentence in the source language, lowercase — in the source-language file, key
   and value are identical. A key like `err.42` tells a translator nothing.
3. Domain-specific strings live with the domain that owns them (its own `lang/` folder, merged at runtime);
   only genuinely transverse strings — navigation, shared buttons, generic errors used by more than one
   feature — go in the central file.
4. An i18n label inside a list/config = `computed(() => [...])`, never frozen at `setup()` time: a label
   frozen at setup doesn't follow a locale change.
5. Page title/subtitle metadata is translated too. A `definePageMeta`-style title left as a raw string is
   the page that stays in the wrong language.
6. No user-visible text hardcoded in a component. Where a project has no i18n layer at all, the text still
   comes from one place, not from wherever it was first typed.

### 7. Accessibility in templates
1. Native semantic element (or the toolkit's wrapper for it) first — never a clickable `div`/`span`.
2. Heading order respected, no skipping levels.
3. Page shell wrapped in landmark elements.
4. Every icon-only control gets an accessible name (`aria-label`).
5. Every toggleable / expandable / selectable / checked / current state exposed through the matching ARIA
   attribute, not through a CSS class alone.
6. An icon sitting next to visible text is decorative: hide it from assistive tech rather than having it
   read twice.
7. Async UI feedback (toasts, status messages, form error summaries) announced through a live region.
8. An open modal: focus placed on it, trapped inside, returned to the trigger on close.
9. Never block paste on an authentication field, never disable viewport zoom. If the layout breaks at 200%,
   the layout is the problem.

### 8. The component library
1. **Toolkit first**: if the chosen UI library ships a component, composable, directive or utility class for
   the need, use it rather than pulling another package or hand-rolling a `<div>`. Mixing a second UI library
   splits both the visual language and the mental model.
2. Go to the most specific component available (a data table for a sortable/filterable list of rows, a
   dialog for a one-off confirmation, a chip for a status) rather than assembling one from primitives.
3. Spacing, visibility and state utilities come from the toolkit's own classes (`ma-*`, `pa-*`, `d-*`,
   cursor and opacity helpers) rather than a custom scoped `<style>`. A scoped style for a simple
   padding/margin/background is a review signal.
4. Check a prop really exists in the project's version of the toolkit before passing it. A prop that
   silently does nothing (a `:show-select="false"` on a wrapped data table) is the recurring shape of this
   mistake, and it survives review because nothing errors.
5. Inside an item slot of a data table / autocomplete / select, the object exposed is often the library's
   internal wrapper: read the data through its raw payload (`item.raw`), not through `item` directly.
6. A carve-out from rule 1 is legitimate — many projects route notifications to a dedicated toast library
   rather than the toolkit's snackbar, and date handling to a dedicated date lib. Read the project's
   decision instead of assuming either way.
7. Extend a generated/vendored component through a wrapper, never by editing the generated file in place.

### 9. Nuxt: hydration safety and the choice of data primitive
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
4. `useAsyncData`/`useFetch` called in a loop without an explicit string key cause duplicated requests and
   cache fragmentation: always a unique key passed explicitly inside a loop.
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

### 10. Realtime events
1. An incoming realtime/websocket message is **translated into an application-level hook or event**, not
   consumed inline in the component that happens to be mounted. A component subscribing directly couples
   the transport to the view and leaks a listener the moment it unmounts.
2. One place owns the connection and its lifecycle (connect, reconnect, teardown); components subscribe to
   the application event, not to the socket.
3. A payload arriving from the wire is untrusted input: validate it at the boundary like any other.

### 11. Reactivity and security correctness (linter-derived)
1. Never invoke a prop callback (`props.onXxx()`) during the body of `setup()` or inside a `computed`
   getter: that's a side effect on the render path, replayed on every re-evaluation and during SSR. It goes
   in an event handler, a `watch`, or a lifecycle hook.
2. A `watch`/`watchEffect` that registers a listener/timer/observer (`addEventListener`,
   `setInterval`/`setTimeout`, `IntersectionObserver`/`MutationObserver`/`ResizeObserver`,
   `WebSocket`/`EventSource`/`BroadcastChannel`) must have its **exact** cleanup returned or done through
   `onWatcherCleanup`: whatever is added is explicitly removed.
3. Never an auth token/secret in `localStorage`/`sessionStorage`: exposed to any XSS payload. A cookie
   that's `HttpOnly`, `Secure`, `SameSite` and set server-side is the only sane option.
4. `eval()`, `new Function()`, and `setTimeout`/`setInterval` with a string argument are XSS/RCE vectors:
   explicit logic, `JSON.parse` for data.
5. Assigning `innerHTML`/`outerHTML` injects unsanitised markup (a direct DOM XSS sink): `textContent` for
   text, or sanitise before assigning if HTML really is necessary.
6. Server routes (h3): `throw createError()`, never `throw new Error()` — the latter leaks the stack trace
   and internal details.
7. `readValidatedBody()` parses and validates the request body in one step; `readBody()` leaves you to
   remember the validation.
8. The `event` parameter of a `defineEventHandler` is typed explicitly; an untyped handler loses the
   guardrails on `event.context`/`event.node`.
9. No mutable module-level state on the server side, shared between concurrent requests.

### 12. Recurring review patterns (quality debt observed in the field)
1. No pre-emptive chunking/retry without a verified backend constraint. A notification in a loop = once.
2. A summary card above a table: the total recomputed on the table's **active filters**, not on the user's
   full scope.
3. Table filter: read the backend Resource/Model (does the field take an id, a name, a slug?) before writing
   the `whereIn`/sort. A 422 from a live request is not a specification.
4. Endpoint response: a status/type **and** a human-readable message, not just an HTTP code — the front has
   to display something.
5. A client-only component: DOM ref through `watch(..., { immediate: true, flush: 'post' })`; API exposed
   through `emit('ready', api)`, not `defineExpose` (a client-only wrapper doesn't relay it).
6. Dark/light switch: cut the CSS transitions during the change (a temporary class, a double
   `requestAnimationFrame`, an SSR guard) to avoid the flash on refresh.
7. A default import from an icon lib (the whole lib instead of one icon), or a heavy module loaded at the
   level of a rarely visited route, bloats the bundle for nothing: named import / lazy component.
8. Check the permission name against the backend before wiring a menu entry or a guard on it: a plausible
   name that doesn't exist fails open or hides the entry for everyone.

## Output / checkpoint
Code compliant with the sections above. No dedicated checkpoint: compliance is checked by `gate` (7) and
`review` (8), like the rest of the code produced at the `code`/`tdd` step.

## Guardrails
No comments in the code produced. Don't reinvent a component the UI toolkit already provides. Don't duplicate
an existing composable before checking that no nearby one covers the need. `technical/` never imports
`functional/`. Where an org catalogue is installed and disagrees with a rule here, **it wins** — say so
explicitly rather than silently applying either one. When in doubt about a rule covered by neither, escalate
rather than guess.

## Origin
Ideas taken from: a market Vue skill catalogue (script-setup macros, core APIs, advanced patterns) and a
market Nuxt catalogue (`nuxt4-patterns`, plus a `nuxt-composables` extract limited to the
`useState`/`useCookie`/`useRequestFetch` discipline) for sections 1 and 9; a market Vuetify catalogue for
section 8; a market linter (the `oxlint-plugin-vue-doctor`/`oxlint-plugin-nuxt-doctor` packages, itself
inspired by its React equivalent, locked to Vue 3 + Nuxt 4) for section 11; a market open source TypeScript
project (the `typescript-review` skill) for the accessibility/bundle-weight blind spots; **an org skill
catalogue for this stack (21 skills: SFC shape, composable cohesion, namespace stutter, typing, naming,
callback naming, arrow functions, auto-imports, BEM, class binding, i18n conventions and domain placement,
layered structure, package management, store management, test placement, template ARIA and semantics,
toolkit-first, realtime)** — rules extracted, de-identified and rewritten generically, with everything
naming an internal library, package list or project deliberately left out (rule C). Internal review feedback
(recurring quality debt across several projects on this stack, generalised) for section 12. Mechanisms
rewritten, no copied text. Stamped 2026-08-06.

Section 9 point 5 and section 5 point 6 (the `shallowRef` reactivity change and the Nuxt 4 directory
defaults) refreshed against the official Nuxt 4 upgrade guide (nuxt.com/docs/4.x/getting-started/upgrade),
read 2026-08-10 — supersedes the `nuxt4-patterns` extract above on this specific point, which predated the
Nuxt 4 stable release. The layer-convention override note names `nuxt-osdd` (nuxt-osdd.xefi.com) directly
rather than de-identified: it's the company's own published open-source package, publicly readable outside
the company like `test-casebook` — rule C's generic-citation default is for internal/private facts, not for
a real tool the company itself ships publicly (`CONVENTIONS.md` rule C). Confirmed against its own docs,
read 2026-08-10: each layer keeps its own `app/` subtree, which is why the Nuxt 4 root-level default
doesn't compete with it.

Section 9 point 8 (client-side error handling: `error.vue`, `NuxtErrorBoundary`, `useError`,
`showError`/`clearError`, `onErrorCaptured` vs `vue:error`) added 2026-08-10 from the official Nuxt error
handling guide (nuxt.com/docs/getting-started/error-handling), filling a real gap: §11.6 only covered the
server-side `createError()` half, nothing on the client side was documented at all.

Section 5 point 6 (`runtimeConfig` vs `app.config` as a security boundary) added the same day from the
official Nuxt configuration and runtime-config guides (nuxt.com/docs/4.x/getting-started/configuration,
nuxt.com/docs/4.x/guide/going-further/runtime-config): filled a real gap, the skill had no rule at all on
where a secret is allowed to live versus where a value becomes client-exposed. Cross-checked against
`nuxt-osdd`'s real per-layer `runtimeConfig` usage (each layer's own `nuxt.config.ts`, `public.*` correctly
scoped) rather than asserted from the docs alone.
