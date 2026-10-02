# data-fetching-state-conventions — origin and source stamps

> Provenance of `skills/data-fetching-state-conventions`. Read it when a rule has to be traced back to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Written 2026-10-02, new block, never run on real work (🟡, base to confront with a real project).**

Sources, all primary, read on 2026-10-02 from shallow clones of the projects' documentation:
- TanStack Query (`TanStack/query`, `docs/`, MIT), at **5.104**: important defaults, query keys and functions,
  query options, dependent queries, mutations, invalidation, optimistic updates, server rendering and
  hydration, render optimisations, testing, and the comparison page. Feeds §1 and §2.
- Redux style guide and Redux Toolkit documentation (`reduxjs/redux`, `docs/`, MIT): the three priority tiers,
  state ownership, derived data, events versus setters, where state should live, form state. Feeds §1.5-1.8
  and §3.
- Pinia (`vuejs/pinia`, `packages/docs`, MIT): defining stores, set-up store return rule, destructuring,
  state, actions, usage outside components, server rendering. Feeds §3.17-3.22.

**Licence.** All three are MIT: mechanisms were rewritten in our own words, no sentence or example is copied.
The ordering, the four-kind taxonomy of §1, the mechanical checks and the cross-references to the stack blocks
are ours.

**Facts that move, with their pin.**
- Cache defaults in §2.6 (stale at once, five-minute discard, three retries) and the `'static'` stale time:
  v5.104 values.
- Dehydration defaults and the serialisation limits in §2.9: v5.104.
- The `enabled` / skip-token behaviour in §2.8: v5.104.
- Pinia set-up store and usage-outside-component rules in §3.17-3.18: the documentation at the clone date.
- Redux Toolkit names (`createSlice`, `createSelector`, query layer): the documentation at the clone date.

**Not read, a stated gap.** SWR, Apollo, RTK Query internals, framework-native loaders (Next, Nuxt, SvelteKit
data functions, Angular resources), Zustand, Jotai, Valtio and NgRx; persisted-store versioning beyond what
`skills/react-nextjs-conventions` §6 already states. A project on one of those applies §1 and translates §2-3.

**Refresh protocol.** Re-read the important-defaults and the server-rendering pages of the next TanStack Query
major and the Pinia usage-outside-component page; give each pinned fact above a verdict
(`skills/source-freshness` §3); stamp the date even when nothing changed.
