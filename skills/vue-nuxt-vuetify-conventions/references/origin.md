# vue-nuxt-vuetify-conventions — origin and source stamps

> Provenance of `skills/vue-nuxt-vuetify-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

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

Re-checked directly against the public **vue.doctor**/**nuxt.doctor** tools (the-doctor.report, the linter
section 11 already traces to) on 2026-08-10: its two named custom rules that weren't already covered here —
never importing a compiler macro (`defineProps`/`defineEmits`/etc.) from `'vue'` (§1.10), and an explicit
`useAsyncData`/`useFetch` key as the default rather than only inside a loop (§9.4, widened) — are now
closed. Its other named rules (props destructuring breaking reactivity) were already §1.9.
