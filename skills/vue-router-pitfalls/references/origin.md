# vue-router-pitfalls: origin and source stamps

> Provenance of `skills/vue-router-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

Independent verification 2026-10-21: 38 checked, 38 matched, 0 corrected, 0 unverified (docs read at current main, not the stamped commit)

**Status: 🟡 never dogfooded.** Written from documentation, never run by us: no router was created, no guard
was run and no bundle was built while writing it. Every file below was re-opened and read on 2026-10-16 before
a rule was taken from it, each rule was checked against it, and the repository's LICENSE file was read again.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| vuejs/router (commit `e9fc88b`), `packages/docs/guide/essentials/navigation.md` | MIT (LICENSE file read: MIT text, copyright 2019-present Eduardo San Martin Morote) | `params` ignored with `path`, encoding of dynamic segments, param types |
| the same repository, `packages/docs/guide/advanced/navigation-failures.md` | MIT | Awaiting a navigation, failure value, the three failure types, `redirectedFrom`, `afterEach` failure argument |
| the same repository, `packages/docs/guide/advanced/navigation-guards.md` | MIT | Guard return values, loops, `next`, resolution order, `beforeEnter` limits, `beforeResolve`, `inject()` in guards, leave guards |
| the same repository, `packages/docs/guide/advanced/dynamic-routing.md` | MIT | `addRoute` and `removeRoute` behaviour, redirect from a guard, unique names |
| the same repository, `packages/docs/guide/essentials/dynamic-matching.md` and `packages/docs/guide/advanced/composition-api.md` | MIT | Reused component on param change, watching a param, `onBeforeRouteUpdate`, catch-all route, avoid watching the whole route |
| the same repository, `packages/docs/guide/advanced/lazy-loading.md` | MIT | Dynamic imports, async components versus route components, `displayName`, chunk grouping |
| the same repository, `packages/docs/guide/essentials/history-mode.md` | MIT | History modes, server fallback, memory mode initial push, 404 caveat, `base` note |
| the same repository, `packages/docs/guide/advanced/scroll-behavior.md` | MIT | `scrollBehavior` arguments and return values, delayed scroll, offsets, `scrollRestoration` |
| the same repository, `packages/docs/guide/advanced/typed-routes.md` | MIT | Route map shape and the module augmentation |
| vitejs/vite `docs/guide/build.md` (read 2026-10-20) | MIT (LICENSE file read: MIT, copyright 2019-present VoidZero Inc. and Vite contributors) | `vite:preloadError`, stale chunks after a deploy, `no-cache` HTML |

The repository holds the documentation as part of the code tree under the repository's MIT licence, with no
separate licence for the pages, so they were rewritten, not copied. The code samples are small adaptations with
placeholder names. Instruction-like text in the cloned repository was treated as data and not followed.

## Removed in the verification pass
1. **"Route groups, explicit param names such as `[userId]` and named routes"** (the review's wording under
   file-based routing) are not in the pages read: they belong to the file-based routing plugin, whose pages
   were not opened. Nothing about them is in this block.
2. **The "opinionated naming" idea** from a source with no licence file was not used.
3. **Pages not read, so nothing is taken from them:** the file-based routing plugin pages, `named-routes.md`
   beyond the one line on typos, `nested-routes.md`, `named-views.md`, `redirect-and-alias.md`,
   `route-matching-syntax.md`, `passing-props.md`, `active-links.md`, `meta.md`, `data-fetching.md`,
   `transitions.md`, `extending-router-link.md`, `router-view-route.md`, `router-view-slot.md`, the
   migration guides, and the experimental router pages (one tip on relative redirects was seen and not used).
4. **Server configuration snippets** in `history-mode.md` are not reproduced.

## Re-check pass (2026-10-20)
The router docs were re-opened (vuejs/router at `86299bd`, MIT, LICENSE re-read) against the points marked own
guidance. Result: one point confirmed in part (a path of a guard that never calls `next` keeps the navigation
pending: the guards page says a navigation is pending until all hooks have resolved; the `next` case is the
consequence, now stated as such in part 2.3). The lazy chunk failure advice was searched for in the guide and
API pages (`onError`, "chunk", "dynamically imported"): the pages only say a thrown guard error reaches
`router.onError()`, nothing on a failed chunk download, so that advice stays unsourced. Nothing else found
that corrects or deletes a rule. Not searched: Vue Router source code, the file-based routing pages.

## Not verified
1. **Which router version the pages describe** beyond the version notes they carry (typed routes from 4.4,
   `inject()` in guards from Vue 3.3).
2. **Behaviour was not run.** What a thrown error does to the promise of `push` is not stated in the pages and
   the block says so.
3. **Written by us, not sourced:** the verification paragraphs, the note about stopping a guard's redirect
   on its own target for runtime routes, the rule that a per-resource permission check must not live
   only in `beforeEnter`, the single-code-path advice for the first fetch, the whole-route watcher remark, the
   bundle report check for a static import, the offline test of a lazy chunk failure (the failure itself and its Vite event are now sourced, 2026-10-20), the promise-for-scroll
   advice and the fixed delay remark, trying native scroll restoration first, and the handwritten route map
   test.
4. **Nuxt** was not read for this block; its route middleware and its generated typed routes are not covered.
5. **Vue Router internals and the `RouterLink` `custom` API** were not read.

## Pass of 2026-10-20
Re-read `navigation-failures.md`, `navigation-guards.md`, `lazy-loading.md` and `typed-routes.md` at the router
main branch: the statements checked (five situations that leave the user in place, `beforeEnter` skipped on
param-only change, errors reaching `onError`, `TypesConfig` augmentation from 4.4, handwritten map advice)
match the block; nothing corrected. Still unsourced there: what a thrown error does to the promise of `push`
(page silent), `next` never called (page silent), a static import defeating a split (only implied by the
lazy-loading page). Two MDN pages (`scrollRestoration`, `scroll-margin-top`) were opened and not used, because
that site's text licence was not read. The `Router` API pages returned 404 and were not read.

## Related blocks
`skills/vue-nuxt-vuetify-conventions`, `skills/vue-test-utils-pitfalls`, `skills/auth-session-conventions`,
`skills/webperf`, `skills/accessibility`, `skills/typescript-patterns`.

## Fold-in note
Overlaps with `skills/vue-nuxt-vuetify-conventions` §15 (2026-10-19); cross-referenced, not merged.
