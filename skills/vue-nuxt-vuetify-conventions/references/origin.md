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
Nuxt 4 stable release. The layer-convention override note names the `nuxt-osdd` package directly
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

**Bodies pass on the org catalogue, 2026-09-07.** The 2026-08-06 stamp above mined that catalogue's 21
skills from their **descriptions**; this pass read the bodies, which is where the thresholds, the
anti-pattern lists and the runtime gotchas live. Four real gaps, all of them mechanism rather than house
policy: §4.5 gained BEM's three out-of-scheme shapes (grandchild, bare modifier, camel case), §4.6 the
static/dynamic split with its extract-to-`computed` threshold and the reactive-CSS-in-the-style-block
preference, §4.7 the opt-a-folder-into-the-scan rule, and **§13 is new** — the typed-client layer, which the
descriptions pass had reduced to "go through the model" and whose real weight is the hydration-typing trap,
the shared applied state between two handles on one record, and the foreign-ORM muscle memory. The house
client's own name, decorators and config stay out (rule C); `lomkit/laravel-rest-api` is named in §13.2
under the same carve-out as elsewhere in the repo, as a public package. The 17 other skills were already
covered by §1–§12 and are unchanged.

**Depth pass, §10, §2 and §3, 2026-09-08.** Not a source refresh: no new source, no rule reversed. The
three thinnest sections of the block (113, 211 and 174 words) were the ones stating a rule without the
failure it prevents, which is what makes a rule unenforceable in review — an agent can agree with "no
`any`" and still not know what it costs. Each is now written the way §9 and §13 already were: one
numbered point per real failure mode, the mechanism named, and the consequence stated in terms of what
the user or the next reader actually sees. §10 goes to 12 points (transport-to-event, one connection
owner, the scoped subscription including `keepalive`, the untrusted payload, message-as-hint rather than
snapshot, duplicates and out-of-order delivery, the missed-while-disconnected resync, no socket during
SSR, server-side channel authorisation, channel-scoped rather than client-filtered subscriptions, not
moving the UI under the user, and the don't-build-it test). §2 goes to 16 (shared-versus-per-caller state
named deliberately, module-scope state leaking across SSR requests, the synchronous-`setup` requirement,
in-flight deduplication, one reset, no async in a getter, watcher scope ownership, store cycles, and
URL-owned state). §3 goes to 16 (type-only `defineProps`/`defineEmits`, the `undefined` inside an empty
`ref`, deriving API types instead of copying them, boundary validation, discriminated unions over
optional bags, ids that must not be swapped, `as const`, typed slot props, and the annotated store
surface). The pre-existing points were kept verbatim and renumbered only where new material was
interleaved.

Two of these are corrections rather than additions, and worth naming as such: §2's module-scope-state
point closes a real cross-account leak the block never mentioned (SSR shares a module across visitors,
not across a visitor's requests), and §10's server-side-channel-authorisation point closes the case where
a private channel is "authorised" by a name the client itself composes. Both were absent, not wrong.

**Depth pass, §7 and §6, 2026-09-08 (same day, second pass).** Same method, next two thinnest sections.
§7 goes from 172 to 899 words and 9 to 17 points; §6 from 199 to 877 and 6 to 15. Both were checklists —
true, terse, and impossible to argue from in a review, because a reviewer who is told "every icon-only
control gets an accessible name" cannot answer "why does it matter here" without the mechanism.

§7's nine original points are kept and each now carries the failure it prevents; the eight added are the
ones a template review actually keeps catching: a placeholder used as a label, an error message not
programmatically attached to its field, required/invalid carried by colour or an asterisk alone (which
generalises to status chips and chart series), a focus outline removed and not replaced, a row action
that only exists on hover, an image alt left as the filename and a chart with no textual equivalent, a
missing page language, and the closing point that automated checkers pass pages nobody can use — tab
through it and zoom to 200% instead. Point 4 also gained the voice-control consequence: an accessible
name that does not contain the visible text makes the control unusable by voice, which is the one
accessible-name failure that is invisible to a screen-reader-only test. This section is where the RGAA
expectation lands in practice, and it is stated as mechanism rather than as a criterion number, because
the block has to hold on a project with no compliance target at all.

§6's six original points are kept; the nine added are the internationalisation mistakes that are correct
in the source language and wrong everywhere else — a `n > 1` ternary standing in for a plural rule
(Russian and Polish have three forms, Arabic six, several treat zero separately), a sentence built by
concatenation, a translation rendered as HTML (an injection surface fed by a file edited outside code
review), dates and numbers formatted by hand, the ~30% expansion German applies to a button sized for
French, a missing key falling back to an empty string instead of loudly, one key reused for two meanings
because the English words coincide, text baked into an image, and the locale file being part of the same
commit as the code since nothing builds to catch its absence.
