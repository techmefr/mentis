# solid-ownership-pitfalls: origin and source stamps

> Provenance of `skills/solid-ownership-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real application by us. No Solid code
was built or run while writing it.

**Overlap note.** A broader Solid conventions block now exists as `skills/solid-conventions`. This block was written standalone, with a name that cannot collide, to hold the gaps found in a comparison against it. Overlaps with `skills/solid-conventions` (2026-10-19); cross-referenced, not merged.

## Version scope
**Solid 1.x.** The package registry read on 2026-10-08 showed the stable tag on a 1.9 release, a beta on 1.10
and the `next` tag on a 2.0 release candidate. The lint plugin documentation describes 2.0 behaviour for several
rules; those 2.0-only rules (renamed lifecycle and batching functions, the two-argument effect, writes in owned
scopes, the removed class-list prop, the module move of the web package) were **not** written, because 2.0 is
not the current release. The attribute and module-scope rules apply to both lines per the plugin documentation.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The official Solid documentation: Show, children, stores, createStore, createRoot, JSX attribute namespaces, testing guide, component basics | official docs, read 2026-10-08 | Keyed Show, children helper, reconcile, root ownership and disposal, `prop:`, test rendering with a function, `renderHook`, `findBy`, portal queries, `testEffect` |
| The eslint-plugin-solid rule documentation (module-scope primitive, boolean enumerated attribute, rule-confidence policy, 2.0 removal rules) | MIT, read 2026-10-08 | §2.2 module scope, §2.3 enumerated attributes and ARIA tristate behaviour, the version scoping above |
| One MIT Solid best-practices rule set (about 15 of 67 rules read) | MIT (holder named only "Community"), read 2026-10-08 | Component-as-function, keyed children, stable mount, primitives in reactive contexts, store function wrapper, deproxy, page-boundary cleanup, test arrow, roots, async and timer rules, innerHTML, storage isolation |

The MIT rule set has no real author named, so nothing is copied and every rule is rewritten.

## Re-read 2026-10-20 (verification pass)
Official Solid pages opened that day (site terms not read; facts only, nothing copied; read through a fetch tool
that summarises): the Show reference (unkeyed re-renders only when truthiness changes and gives an accessor;
keyed re-renders on any change and gives the value), the children helper (memoised accessor, reads reuse the
resolved result), reconcile (diffs into the store, key defaulting to the id, merge option), createRoot (disposed
only through the dispose function; a root without a dispose parameter is unowned and may leak; runs once,
untracked), the testing guide (render takes a function; renderHook returns result, cleanup and owner; testEffect
for asynchronous effects; findBy rejects after one second; user-event takes the fake-timer advance function;
portal content through the screen queries), the prop namespace page (client-only, no server output) and the
store guide (function values are updaters; unwrap gives a non-reactive snapshot). These now source §1.2.1-1.2.2,
§1.3.1, §1.1.4, §2.1.1, §2.1.2 (the updater half), §2.4.2, §3.1.1, §3.2.2, §3.3.1-3.3.3 and resolve open
points 3 and 4 of the list below (the testing guide does mention the fake-timer option; it does not mention
`createRoot` in tests, but the createRoot page's own example is a test). Corrections: §3.3.1 gains the one-second
rejection; §2.4.2 gains the point that the prefix is not always needed. Still unsourced: calling a component as a
function and the same component in several branches (open points 1), the wrapper form for a stored function
(point 2, the consequence only), the `on:` namespace for custom events (point 5), the enumerated-attribute and
ARIA tristate rules of §2.3 (from the lint plugin docs, not re-opened), module-scope signals under server
rendering (§2.2, plugin docs), the split-pane cleanup (§1.1.5), innerHTML and the IndexedDB isolation notes.

## Rewrite notes
Rules are re-explained principle first. The verification lists are ours.

## Not verified
1. **Calling a component as a function** and **the same component in several branches**: the behaviour is from
   the MIT rule set only; the official component documentation read does not address either.
2. **A function stored in a store needs a wrapper**: from the MIT rule set only; the official store pages read
   describe updater functions but do not say how to store a function.
3. **`advanceTimers` for fake timers** is from the MIT rule set only; the official testing page read does not
   mention it.
4. **`createRoot` in tests**: the official root page shows a test example; the testing guide read mentions
   `testEffect` and `renderHook` but not `createRoot`.
5. **`on:` for custom events** was taken from an example in the MIT rule set; the official attribute page read
   gave no detail on it.
6. **Nothing here was run.**
7. **Dropped from the review's list:** the Solid 2.0 migration section (2.0 is a release candidate, not the
   current release), and the lint-policy meta-rule (P3, a statement about one plugin's design).
8. **Written by us, not sourced:** the verification lists and the output/checkpoint paragraph of `SKILL.md`.

## Related blocks
`accessibility`, `security-hardening`, `testing-anti-patterns`, `typescript-patterns`.
Independent verification 2026-10-21: 17 checked, 17 matched, 0 corrected, 0 unverified (Solid docs and eslint-plugin-solid)
