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
handling guide (nuxt.com/docs/getting-started/error-handling), filling a real gap: §11.10 only covered the
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

**Depth pass, §11, §12, §8, §1 and §5, 2026-09-08 (third pass, same day).** The five remaining thin
sections, taken by ascending thickness as recorded in `CATALOG.md` §2. Same method throughout: originals
kept, mechanism and consequence added, new points only where the section was silent rather than wrong.
§11 9 → 16 points, §12 8 → 17, §8 7 → 14, §1 12 → 17, §5 6 → 15.

What is genuinely new, as opposed to deepened. §11 gained the reactivity mechanics the linter-derived
list had skipped — a `computed` must be pure, watching an object versus a getter (and what `deep: true`
actually costs), a `v-for` key that is the array index reusing the wrong DOM node so a typed value moves
to another row, `v-if` and `v-for` on one element — plus three server-side security points in the same
family as the existing ones: never reading a user's identity from something the client can set
(horizontal privilege escalation), never building a redirect target from user input (open redirect), and
capping an unbounded collection at the boundary. §12 gained the field patterns that were observed but
never written down: a pending flag not reset on the failing branch, an optimistic update that never
reconciles, server-side pagination mixed with client-side sorting, a search index whose result count is
a cap rather than a total, a watcher chain whose update order is emergent, a `catch` that logs and
continues, and a component test asserting on CSS classes. It also gained the one that belongs beside a
permission check: **hiding is not authorising**.

§8 gained the wrapper discipline (don't wrap just in case; a wrapper that does exist forwards attrs and
slots explicitly), theme tokens over a hex, the prohibition on `:deep()` into generated class names since
those are not API, reading the docs for the *installed* version rather than the latest, not defeating the
accessibility the component already carries, and the server-side/client-side data-table contract. §1
gained the template-holds-shape-not-reasoning rule, no prop mutation in a child, `v-model` as a declared
pair rather than a hand-rolled `value`/`input`, the props-explosion signal, and `defineExpose` as a
deliberate act rather than a habit. §5 gained enforcement of the layer boundary by the toolchain rather
than by prose, alias resolution verified in the linter *and* the type checker before migrating, the
`shared/`-as-boundary-not-bucket threshold, circular imports, the server boundary kept physical rather
than commented, environment variables read in one place, checking the platform before adding a dependency
for one helper, and the lockfile as part of the change.

**A defect fixed in passing**: §5 had two points numbered 6 and no 7, and the second one cited "point 5
above" for a source that was actually point 6's. Renumbered and the citation corrected.

**Depth pass, §4, §9 and §13 — the block is complete, 2026-09-08.** These three were already the deepest
sections, so this pass added only what was missing and deliberately padded nothing. §4 8 → 16 points,
§9 9 → 15, §13 6 → 12; the block's thirteen sections plus its router now stand at 12,443 words against
the org catalogue's 19,869 for the same stack, **x1.6**, from x3.6 this morning. That figure deliberately
excludes this file: provenance is not depth, the catalogue being compared against has no equivalent of
it, and counting the ~1,700 words these stamps added today would have reported x1.34 for work that did
not happen in the rules. `CATALOG.md` §2 records the convention change.

§4 covered casing, BEM and auto-imports thoroughly and said nothing about what makes a name good. Added:
a name states the subject rather than the plumbing or the type (`data`, `payload`, and the `Utils`/
`Manager`/`Helper` bag-names at file level); a name numbered to dodge a collision is a name that gave up,
and a renamed symbol renames its file; abbreviate only in the domain's own words; **an emitted event says
what happened, not what the parent should do** — the reuse test being that a second parent can react
differently to `saved` and cannot to `refreshTable`; name the positive, since a negative boolean
double-negates at every call site; a translation key never leaks into an identifier; in a codebase that
already chose, consistency beats correctness and a convention changes in its own pass; and if a name needs
a comment, the name is wrong — which is why this block bans comments rather than merely discouraging them.

§9 was strong on the primitives and silent on what SSR *exposes*. Added: a hydration mismatch routinely
ships looking correct, so the dev-mode warning is the signal rather than the screenshot; `<ClientOnly>` is
a hole in the server render with a real cost, not a free escape hatch; **everything a server-side fetch
returns is serialised into the HTML payload**, so over-selecting publishes fields the template never
renders and authorisation meant to withhold; `useFetch` runs on both sides unless the payload is reused,
and a hand-rolled client guard is the sign the primitive is being fought; a server-side call to your own
API is anonymous unless the request context is forwarded, which is why one endpoint answers 200 in the
browser and 401 during SSR; and the server has no browser locale or timezone. The closing checklist was
extended to match.

§13 gained the operational half of the typed-client rule: the page size belongs to the model, not to each
screen; a model method is a request and not a cache; extend by wrapping, never by patching the vendor's
prototype; catch the client's own error type, because the per-field validation detail the form needs is
only there; **an absent field is not a null field**, so a payload built from a partially loaded record can
blank columns it never fetched; and the server authorises an include — a relation the builder will happily
request is not one this user may read.

**Two defects fixed in passing.** §9 point 8 pointed at `§11.6` for `createError`, which the §11 pass
moved to point 10 — corrected here and in the 2026-08-10 stamp above that cites it. And a reflow pass had
flattened §9's point 3 sub-list into a paragraph and inserted a space inside its error-handling URL; both
restored. Every intra-block `§N.M` reference was then re-checked against the current numbering, one by
one: fifteen of them, all resolving.

**Widened against Nuxt 4.4's current data-fetching surface, 2026-09-09.** Same method as the other
widenings this week: checked against Nuxt's own current release notes, not the catalogue. §9 gained two
points: two `useFetch`/`useAsyncData` calls sharing a key now share one `data`/`error`/`status` outright, so
a `transform`/`default` passed at the second call site does not rerun for a fetch the first call already
resolved — point 4's explicit-key rule stops an accidental collision, and this is the same sharing invoked
on purpose; and a shared `useFetch` factory wrapping the base URL, error handling and auth header once is
the fix for options repeated at every call site, keeping points 8 and 13 centralised rather than
copy-pasted per page. Nothing here answers the catalogue comparison a second time.

**Widening, 2026-09-10 — pass élargie.** The five thinnest sections by word count (§1, §8, §11, §12, §10)
each gained 5–7 further points, mechanism-plus-consequence in the same voice as the rest of the block.
Sourcing: §1 (defineModel, its `set` transform, generic `<script setup>` components, `useTemplateRef`, the
cost of loose top-level `ref`s, implicit template exposure) against the official Vue.js docs
(vuejs.org/api/sfc-script-setup, vuejs.org/guide/typescript/composition-api,
vuejs.org/guide/essentials/template-refs, vuejs.org/api/composition-api-helpers) — nothing from the
marketplace XEFI. §8 (density scale, dynamic header/item slots vs hand-rolled chrome, slot payload shape,
the toolkit's own selection primitive in table slots, reading migration notes on a major bump, one
declared theme) against the official Vuetify docs (vuetifyjs.com/en/components/data-tables,
vuetifyjs.com/en/concepts/density-and-sizing, vuetifyjs.com/api/VDataTable). §11 (CSRF cookie flags,
conditional composable calls, `markRaw` on foreign instances, dead reactive state) against Vue's reactivity
docs and current Nuxt CSRF/cookie practice (httpOnly/Secure/SameSite, the double-submit pattern). §12
(prop drilling as a state-placement bug, watch-instead-of-computed as the same defect as §11.6, client/server
validation gap mirroring §11.9, a loading flag that doesn't wrap its own transform step, an over-broad
`try`/`catch`) synthesised from the field patterns already generalised in this section plus current
community writing on Composition API anti-patterns (prop drilling, watcher overuse) — no marketplace
content, mechanisms rewritten in this block's own voice. §10 (transport choice by traffic direction, SSE as
still a connection subject to points 1–3 and 8, fan-out cost of a socket per idle viewer, calendar-time
backoff with a visible reconnecting state) against current public writing on WebSockets vs Server-Sent
Events for 2026 real-time architecture. Content word count for the thirteen numbered sections (excluding
this file): 12,625 before this pass, 13,683 after.
