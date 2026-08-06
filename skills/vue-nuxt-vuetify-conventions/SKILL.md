---
name: vue-nuxt-vuetify-conventions
description: Use when writing a component, a page or a composable on the Vue 3/Nuxt/Vuetify stack, applies the pure Composition API conventions, the Nuxt hydration patterns, the Vuetify patterns (utilities, component catalogue), the vue-doctor/nuxt-doctor style reactivity/security correctness, and the recurring Xefi review patterns. Merges these convention families of the same stack into a single block of the code step.
---

# vue-nuxt-vuetify-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing of frontend code on the Vue 3 + Nuxt + Vuetify
stack: three families of rules (Vue, Nuxt, Vuetify) that overlap because it's always the same stack and the
same step: a single block rather than three that step on each other.

## When
As soon as a `.vue` component, a Nuxt page or a composable is written or modified, or a Vuetify component is
chosen for a UI need, during `code` (6) or `tdd` (5).

## Steps

### 1. Vue 3: pure Composition API
1. `<script setup lang="ts">` mandatory. Never the Options API, never untyped JS.
2. Props/emits/model through macros only: `defineProps<T>()`, `defineEmits<T>()`, `defineModel<T>()`. No
   runtime `props: {}` object if the typing is enough.
3. `shallowRef` by default for any non-primitive state (objects, arrays, heavy DOM refs). A deep `ref` only
   if the nested reactivity is genuinely consumed.
4. Never destructure a reactive `props` object directly (`const { foo } = props` breaks reactivity). Access
   through `props.foo`, or go through `toRefs(props)` / a `computed`.
5. A composable returns `ref`s/`computed`s, never raw values. If it takes a parameter that can be a value or
   a ref, read it with `toValue()`: never `unref()` alone (no getter support).

### 2. Nuxt: hydration safety and fetch choice
1. **Never** `Date.now()`, `Math.random()`, or any direct `window`/`document` access at the level of the
   synchronous `setup()`: it diverges between the server render and the client render (hydration mismatch).
   Isolate that kind of value in `onMounted`, behind `import.meta.client`, or in `<ClientOnly>`.
2. Choice of data primitive according to the need:
   - `useFetch`: a simple call tied to the component's lifecycle, automatic cache/dedup.
   - `useAsyncData`: transformation/aggregation logic before returning, or several sources combined.
   - `$fetch`: an imperative call outside the render cycle (form submit, user action).
   - `useState`: SSR-safe shared state between components (not a classic global `ref`).
   - `useCookie`: state that has to survive a reload and be readable server-side.
   - `useRequestFetch`: a server call that has to forward the incoming request's headers/cookies (SSR to an
     authenticated internal API).
3. `routeRules` (`nuxt.config`) to arbitrate rendering per route (`ssr: false`, `prerender`, `swr`, cache)
   rather than conditionals in every page.
4. Lazy hydration (`<Lazy...>` or `hydrate-on-visible`/`hydrate-on-interaction` when Nuxt exposes them) for
   any heavy component outside the initial viewport.
5. **Review checklist before merging a Nuxt page/component**:
   - [ ] no non-deterministic value generated outside a client hook
   - [ ] the fetch primitive chosen matches the need (not `useFetch` everywhere out of reflex)
   - [ ] no data leaking between requests through shared module-level state
   - [ ] `routeRules` set if the page needs a rendering mode different from the default

### 3. Vuetify: the component that matches the need, and utility classes
1. Need → component table (go to the most specific one, never a custom `<div>` if Vuetify already has the
   component):

   | Need | Vuetify component |
   |---|---|
   | Sortable/filterable list of rows | `VDataTable` (server-side if pagination is on the backend) |
   | Form + validation | `VForm` + `VTextField`/`VSelect` + rules |
   | One-off confirmation/edit | `VDialog` |
   | Contextual side panel | `VNavigationDrawer` |
   | Transient notification | `VSnackbar` |
   | Status/label | `VChip` |
   | Metric at a glance | `VCard` + `VSparkline`/`VProgressLinear` |
2. Spacing and visibility: always the Vuetify utility classes (`ma-*`, `pa-*`, `d-*`, `bg-*`,
   `cursor-not-allowed`, `opacity-0`…`opacity-100`) rather than a custom scoped `<style>`. A scoped style for
   a simple padding/margin/background colour is a review signal.
3. Inside an `#item` slot of `VDataTable`/`VAutocomplete`/`VSelect`, the object exposed is the internal
   `ListItem`: always read the data through `item.raw`, never `item` directly.
4. Mini-catalogue of assembly patterns:
   - **Dashboard**: a grid of `VCard`s (one metric per card) + a shared filter area above, every counter
     scoped on the same active filter.
   - **CRUD + dialog**: `VDataTable` (the list) + a single `VDialog` reused for create/edit, a
     `mode: 'create' | 'edit'` state driven by a composable.
   - **List**: a server-side `VDataTable` as soon as pagination/sorting has to hit the backend; `v-for` +
     `VCard` only for a short unpaginated list.
   - **Form-detail**: a `VForm` in read-only mode toggled into editing (not two separate components),
     validation before `submit`.
   - **Login**: `VForm` + a password-type `VTextField` with a visibility toggle, errors inline under the
     field concerned (not a `VSnackbar` for a field error).

### 4. Reactivity/hydration correctness and security (vue-doctor/nuxt-doctor)
Deterministic rules taken from a market scanner (the `oxlint-plugin-vue-doctor` / `oxlint-plugin-nuxt-doctor`
packages, itself explicitly inspired by its React equivalent but locked to Vue 3 + Nuxt 4: so directly
applicable to this stack, with no niche-framework filtering to do as on the React side).

**Reactivity and composition, the most frequent mistake**:
1. `defineStore()` is called once at module level, never inside a `setup()`/composable/function body:
   otherwise each call recreates a store definition instead of reusing the shared singleton. The
   `useXxxStore()` it returns is called normally inside `setup()`.
2. Never invoke a prop callback (`props.onXxx()`) during the body of `setup()` or inside a `computed` getter:
   that's a side effect on the render path, replayed on every re-evaluation and during SSR. Where it goes:
   an event handler, a `watch`, or a lifecycle hook.
3. A `watch`/`watchEffect` that registers a listener/timer/observer (`addEventListener`,
   `setInterval`/`setTimeout`, `IntersectionObserver`/`MutationObserver`/`ResizeObserver`,
   `WebSocket`/`EventSource`/`BroadcastChannel`) must have its exact cleanup returned or done through
   `onWatcherCleanup`: the same rule as on the React side (the corresponding section of
   `react-nextjs-conventions`): whatever is added must be explicitly removed.

**Nuxt: hydration, the second most frequent mistake**:
4. No direct access to `window`/`document`/`navigator`/`localStorage`/`sessionStorage` at the root level of a
   `<script setup>`: it crashes on the server side (those globals don't exist under SSR). Guard with
   `import.meta.client` (or `process.client`) or move it into `onMounted`.
5. The same rule inside a `computed` getter: a `computed` is also evaluated on the server side, so reading a
   browser global inside it crashes or produces a hydration mismatch instead of waiting for the client mount.
6. `useAsyncData`/`useFetch` called in a loop without an explicit string key as the first argument cause
   duplicated requests and cache fragmentation; always a unique key passed explicitly inside a loop.

**Security, never negotiable**:
7. Never an auth token/secret in `localStorage`/`sessionStorage`: exposed to any XSS payload. A cookie that's
   `HttpOnly`, `Secure`, `SameSite` and set server-side is the only sane option.
8. `eval()`, `new Function()`, and `setTimeout`/`setInterval` with a string argument are XSS/RCE vectors:
   replace them with explicit logic, `JSON.parse` for data.
9. Assigning `innerHTML`/`outerHTML` injects unsanitised markup (a direct DOM XSS sink); `textContent` for
   text, or go through DOMPurify before assigning if HTML really is necessary.

**Nuxt server routes (h3/Nuxt 4)**:
10. `throw new Error()` in a server handler leaks the stack trace and internal details; `throw createError()`
    (h3) for a clean HTTP error with no stack leak.
11. `readBody()` is the legacy h3 reader; under Nuxt 4/h3 v2, `readValidatedBody()` parses and validates the
    request body in a single step: no manual validation afterwards.
12. The `event` parameter of a `defineEventHandler` must be typed explicitly
    (`defineEventHandler<H3Event>(...)` or a direct annotation); an untyped handler loses autocompletion and
    the type guardrails on `event.context`/`event.node`.

### 5. Recurring Xefi review patterns (quality debt observed in the field)
A short checklist, findings repeated in frontend reviews on this stack.

1. Boolean prefixed with `is`/`has`/`can`/`should`, always.
2. Check that a Vuetify prop really exists (the project's version) before passing it.
3. An i18n label in a list/config = `computed(() => [...])`, never frozen at `setup()` time.
4. A data-fetching composable = it carries its own `useAsyncData`/`useFetch`, returns `data`/`refresh`.
5. Response/DTO interface in the module's `types/index.ts`, prefixed with `I`, not local.
6. No pre-emptive chunking/retry without a verified backend constraint. A notification in a loop = only once.
7. Look for an existing nearby component/composable before writing a new one.
8. An import alias rather than a relative path across folders (if the architecture linter resolves it).
9. Declarative config in `config/` as soon as N near-identical entities are wired by hand.
10. A summary card above a table: the total recomputed on the table's active filters.
11. Table filter: read the backend Resource/Model (id/name/slug) before writing the `whereIn`/sort.
12. Endpoint response: a status/type + a human message, not just an HTTP code.
13. `.client.vue`: DOM ref through `watch(..., { immediate: true, flush: 'post' })`; API exposed through
    `emit('ready', api)`, not `defineExpose`.
14. Dark/light switch: cut the CSS transitions during the change (a temporary class, a double
    `requestAnimationFrame`, an SSR guard) to avoid the flash on refresh.
15. An icon-only button with no visible label = a mandatory `aria-label`. An open modal = focus placed on it
    and trapped inside, returned to the trigger on close.
16. A default import from an icon lib (the whole lib instead of one icon) or a heavy module loaded at the
    level of a rarely visited route = bloats the bundle for nothing: named import / lazy component.

## Output / checkpoint
Code compliant with the five sections above. No dedicated checkpoint: compliance is checked by `gate` (7) and
`review` (8), like the rest of the code produced at the `code`/`tdd` step.

## Guardrails
No comments in the code produced. Don't reinvent a component Vuetify already provides. Don't duplicate an
existing composable before checking that no nearby composable already covers the need. `technical/` never
imports `functional/`; if a value is missing, it's passed as a parameter from the caller. When in doubt about
a Nuxt/Vuetify rule not covered here, escalate rather than guess.

## Origin
Ideas taken from: a market Vue skill catalogue (skills/vue/, SKILL.md, script-setup-macros.md,
core-new-apis.md, advanced-patterns.md) for the Vue section; a market Nuxt skill catalogue
(skills/nuxt4-patterns/SKILL.md) and another market Nuxt skill catalogue
(skills/nuxt/references/nuxt-composables.md, an extract limited to the useState/useCookie/useRequestFetch
discipline) for the Nuxt section; a market Vuetify skill catalogue (.deprecated/vuetify-4/SKILL.md +
references/patterns/) for the Vuetify section; a market linter (the
`oxlint-plugin-vue-doctor`/`oxlint-plugin-nuxt-doctor` packages, itself inspired by its React equivalent,
locked to Vue 3 + Nuxt 4) for the correctness/security section; internal Xefi review feedback (recurring
quality debt observed across several frontend projects on the same stack, generalised and de-identified) for
the review patterns section; a market open source TypeScript project (the `typescript-review` skill,
accessibility/bundle-weight blind spots) for items 15-16 of that same section. Mechanisms rewritten, no copied
text.
