# nuxt-no-hydration-nondeterminism: origin and source stamps

> Provenance of `skills/nuxt-no-hydration-nondeterminism`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

Independent verification 2026-10-21: 17 checked, 16 matched, 1 corrected, 0 unverified

**Status: 🟡 never dogfooded.** Written from documentation, never run by us: no server render was made and
no hydration warning was reproduced. The documents below were read on 2026-10-20 and each rule was checked
against them. The `[src N]` marks in `SKILL.md` point to the numbered rows.

## Sources (all read 2026-10-20, restated in our own words, no text copied)

| N | Source | Licence | What it gave |
|---|---|---|---|
| 1 | nuxt/nuxt (shallow clone), `docs/4.api/1.components/*client-only.md` | MIT (LICENSE file read: MIT, copyright 2016-present Nuxt Team) | `ClientOnly` drops its default slot from the server build, the `#fallback` slot and fallback props |
| 2 | vuejs/docs (shallow clone), `src/guide/scaling-up/ssr.md` | CC BY 4.0 (LICENSE file read: CC BY 4.0 for everything but images, copyright Yuxi (Evan) You and Vue documentation contributors) | Browser globals throw on the server, `onMounted` not called in SSR, cleanup-needing side effects in `setup()`, hydration mismatch causes (invalid nesting, random values, time zones), automatic recovery and its cost, `data-allow-mismatch` from 3.5 |
| 3 | nuxt/nuxt, `docs/3.guide/2.best-practices/hydration.md` | MIT | Consequences of a mismatch, `useCookie`, `useState`, `NuxtTime`, CSS media queries, iOS Safari link wrapping, tag managers, `onMounted` |
| 4 | nuxt/nuxt, `docs/4.api/6.advanced/2.import-meta.md` (commit `fe9ca5b` of nuxt/nuxt; vuejs/docs at `40aa88a`) | MIT | `import.meta.client` is a Nuxt build flag |

The documentation sits inside repositories under the licences above, with no separate licence for the pages
except the Vue one; Vue's is creditable under CC BY 4.0, Nuxt's pages were rewritten, not copied. Instruction-like
text in the cloned repositories was treated as data and not followed.

## Verified in this pass
Steps 1, 3, 4, 5, 6, 7 and the guardrails on cost and suppression are each backed by a row above. The
original block said "Origin: none"; its three claims (globals absent on the server, divergence of
non-deterministic values, isolation in `onMounted` / `import.meta.client` / `ClientOnly`) are confirmed.
Added from the sources: `useState`, `useCookie`, `NuxtTime`, time zones, markup rewritten by the browser, iOS
link detection, tag managers and the cleanup rule.

## Corrected
0. **`useState` (independent check 2026-10-21).** The text said `useState` computes a value once on the server and the client reuses it; neither page states that outright (the hydration guide shows only the initialiser pattern, the useState page says the state is serialised to JSON). Reworded as an inference.
1. **`import.meta.client` in `setup()`.** The Nuxt hydration guide (row 3) treats a guarded dynamic import and init inside `setup()` as still able to alter the DOM before or during hydration, and moves it to `onMounted`. Step 3 no longer offers the guard as an equal alternative for such code.

## Not verified
1. **"A `computed` is evaluated server-side."** No page says it. The Vue page says only that reactivity is
   disabled on the server; the step is worded as what follows from a server render reading the value.
2. **Nothing was run.** Whether a given read mismatches depends on the markup it reaches.
3. **Nuxt version:** the pages are the main branch as cloned on the read date; no version was pinned.

## Related blocks
`skills/vue-nuxt-vuetify-conventions`, `skills/vue-router-pitfalls`.
