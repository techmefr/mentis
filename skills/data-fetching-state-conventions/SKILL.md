---
name: data-fetching-state-conventions
description: "Use when deciding where a piece of state lives or how data is fetched, cached, mutated and shared on a frontend, whatever the framework: server state against client state against URL and form state, a query cache's staleness, keys and invalidation, optimistic updates, server-rendered hydration, and the rules for a client store."
paths: "**/queries/**, **/api/**, **/stores/**, **/store/**, **/*.store.ts, **/*.slice.ts, **/use*Query*.ts, **/use*Mutation*.ts"
---

# data-fetching-state-conventions

Step 6 of the pipeline (`WORKFLOW.md`), framework-neutral: the decision layer above `skills/react-nextjs-conventions`
§6, `skills/vue-nuxt-vuetify-conventions` §2 and §13, `skills/angular-conventions` §3 and
`skills/svelte-conventions` §2-3. Those blocks say how a given framework spells these rules (hooks, composables,
signals, runes). This block says **which kind of state a value is and what that kind owes**, using three
primary sources whose libraries exist for several frameworks: the query-cache library TanStack Query (v5), the
Redux style guide with Redux Toolkit, and Pinia. **Status: a base to confront with real work**, same status as
`go-conventions`. Pinned to TanStack Query 5.104 (read 2026-10-02). A project on another cache library
(SWR, RTK Query, Apollo, a framework's own loaders) applies §1 unchanged and translates §2.

## When
As soon as a value is stored, fetched, cached, shared between components, written back to a server, put in the URL
or in a form, during `code` (6); and in `review` (8) for a store, a hook that fetches, or a mutation.

## Steps

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The four kinds of state and where each lives | a value needs a home, or a store is about to receive a server response | [`01-kinds-of-state.md`](./references/01-kinds-of-state.md) |
| 2 | Server state: cache, keys, staleness, invalidation, mutations, server rendering | data is fetched, cached, refreshed, mutated or prefetched | [`02-server-state.md`](./references/02-server-state.md) |
| 3 | Client stores: Redux-style and Pinia-style | a store, a slice or a reducer is written or reviewed | [`03-client-stores.md`](./references/03-client-stores.md) |

## Output / checkpoint
For a change touching state: each new value named with its kind (§1) and owner, and for fetched data its staleness
decision and its invalidation trigger written next to the fetch. No dedicated checkpoint: `gate` (7), `review` (8).

## Guardrails
No comments in the code produced. Never an install: name the library, the person runs `pnpm add -D <package>`
(`CONVENTIONS.md`). Never copy a server response into a client store. Never leave staleness at the default by
accident: the default is a decision someone else made for a different screen. Do not introduce a second state
mechanism when the project has one for that kind; extend it.

## Origin
Rewritten from the TanStack Query documentation (MIT), the Redux style guide (MIT) and the Pinia documentation
(MIT), read 2026-10-02. Provenance, pins and refresh protocol are in
[`references/origin.md`](./references/origin.md). Read it when checking freshness, not when applying a rule.
