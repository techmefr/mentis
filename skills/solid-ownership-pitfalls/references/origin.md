# solid-ownership-pitfalls: origin and source stamps

> Provenance of `skills/solid-ownership-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real application by us. No Solid code
was built or run while writing it.

**Merge intent.** A broader Solid conventions block exists only on the unmerged branch of the frontend sourcing
pull request (118). This block was written standalone, with a name that cannot collide, to hold the gaps found
in a comparison against it. It is meant to be merged into the same-named framework block when that pull request
lands, section by section, and then removed.

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
