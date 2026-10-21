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

**Re-read 2026-10-20 (verification pass).** The official pages were opened again (facts only, wording not
compared sentence by sentence; the three licences are as recorded above). TanStack Query: important defaults
(stale at once is implied rather than stated; five-minute discard; three retries with exponential backoff;
structural sharing for JSON-compatible data; `'static'` is an optional stale time that blocks even manual
invalidation), query functions (resolve or throw; undefined is treated as failed, use null; the fetch API does not
throw on HTTP errors; the abort signal is in the context), disabling queries (pending and idle state, `isLoading`
is pending and fetching, skip token cannot refetch, a disabled query ignores invalidation), advanced rendering (a
client per request, dehydration of successful queries by default, pending queries opt-in, a stale time above zero),
mutations (no default retry, parallel by default, scope id to serialise, callbacks on the trigger call only while
mounted and only for the last call), optimistic updates (the two approaches and their rollback steps),
invalidation (marks stale regardless of stale time, prefix, exact, predicate; returning the promise from the
success handler keeps the mutation pending), render optimisations (select identity, tracked properties and rest
destructuring, unstable result object) and testing (retries off, fresh client per test, Jest garbage-collection
warning). Redux style guide (essential, strongly recommended and recommended tiers match §1.5, §3.2-3.16 and its
priorities). Pinia core concepts (set-up stores must return all state, destructuring breaks reactivity and the
refs helper fixes it, actions can be destructured).

Corrected: §2.8 (a disabled query ignores invalidation: added), §2.9 (the list of types a framework serialiser
cannot carry is not on the page read; softened), §3.1 (the "single tree is over-read" sentence was not on the style
guide). Still unsourced: the `queryOptions` helper advice of §2.2 (not on the query-functions page; it exists in
the clone docs read 2026-10-02), the five-minute discard figure's exact option name, the lint-plugin remark of
§2.1, the pnpm and grep recipes (ours), SSR hydration drift in §2.10, and the `retry` per error class advice of
§2.7 (the testing page confirms the default only).

**Not read, a stated gap.** SWR, Apollo, RTK Query internals, framework-native loaders (Next, Nuxt, SvelteKit
data functions, Angular resources), Zustand, Jotai, Valtio and NgRx; persisted-store versioning beyond what
`skills/react-nextjs-conventions` §6 already states. A project on one of those applies §1 and translates §2-3.

**Refresh protocol.** Re-read the important-defaults and the server-rendering pages of the next TanStack Query
major and the Pinia usage-outside-component page; give each pinned fact above a verdict
(`skills/source-freshness` §3); stamp the date even when nothing changed.
