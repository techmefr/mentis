---
name: react-nextjs-conventions
description: Use when writing a component, a hook, a Redux slice or a screen on the colleagues' React/Next.js stack, applies the rendering/perf patterns, the Redux Toolkit structuring and shadcn/ui composition. Merges the three convention families of the same stack into a single block of the code step, counterpart of vue-nuxt-vuetify-conventions.
---

# react-nextjs-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing of code on the front-end colleagues' React
18/19 + Next.js + Redux Toolkit + shadcn/ui stack. Three families of rules that overlap because it's
always the same stack and the same step: a single block rather than three that step on each other.
Complementary to `legolas` (the diff review agent): here we write the code, legolas re-reads it
afterwards.

## When
As soon as a `.tsx` component, a Next.js route, a hook, a Redux Toolkit slice is written or modified, or a
shadcn/ui component is composed, during `code` (6) or `tdd` (5).

## Steps

### 1. Rendering and perf
1. Parallelise independent fetches with `Promise.all` (Server Components) rather than chaining them in
   sequence: one `await` after another creates a network waterfall that's invisible when reading the
   component.
2. Derive state at render time rather than a redundant `useEffect` + `setState`. If a value is computed
   from existing props/state, it's a local variable or a `useMemo`, never an effect that resynchronises a
   parallel state.
3. Never define a component inside a component (a function declared in the body of another component): it
   recreates the type on every render and unmounts/remounts the whole subtree, losing state and focus with
   it. Move the component out to module level.
4. Functional `setState` (`setCount(c => c + 1)`) as soon as the new value depends on the old one,
   especially in a handler that can be called several times before the next render (fast event, effect,
   async callback).
5. `next/dynamic` for any heavy component not needed for the first paint (rich editor, chart, complex
   modal): with `ssr: false` if the component depends on the DOM/window.

### 2. Redux Toolkit: structuring
1. One slice = a typed `createSlice`: explicitly typed `initialState`, reducers with `PayloadAction<T>`,
   never an `any` state or action.
2. Typed hooks mandatory: `useAppDispatch`/`useAppSelector` (wrappers around `useDispatch`/`useSelector`
   over the store's `RootState`/`AppDispatch`), never the raw RTK hooks in components: otherwise the typing
   gets lost again on every use.
3. Async side effect = `createAsyncThunk` with `rejectWithValue` on the error, never a bare `throw`: the
   slice has to be able to tell a typed business rejection from an unexpected exception in the
   `extraReducers`.
4. Derived selector (filter, sort, aggregate) = a memoised `createSelector`, never a `.filter()`/`.map()`
   recomputed inline in the component on every render.
5. Server data (fetch, cache, invalidation): RTK Query rather than a homemade thunk as soon as the need is
   standard CRUD with caching: a custom thunk + slice is only justified for business logic that goes beyond
   generic caching/invalidation.
6. Data-fetching complement: if the project doesn't have Redux as its server data layer (pure RSC/Next),
   TanStack Query covers the same need: caching, dedup, invalidation, with the same principle as section
   1.2: minimise manual `useEffect`/`useState` for server data, let the lib manage the request's lifecycle.

### 3. shadcn/ui: composition
1. Copy-and-own philosophy: the files in `components/ui` are generated once then owned by the project, not
   a versioned dependency updated from outside.
2. Extend a shadcn component through a wrapper (a new component composing the generated one), never by
   modifying the generated file in `components/ui` directly, otherwise any regeneration or any other use of
   the base component inherits the deviation.
3. `cn()` (the `clsx` + `tailwind-merge` helper) as the single merge point for Tailwind classes: never a
   hand-built class string concatenation, never two different sources of conditional classes on the same
   component.
4. Folder structure: `components/ui` (generated components, not modified in place), `components/` (business
   wrappers on top), `lib/` (`cn()` and utilities), `hooks/` (shared hooks), providers as close to the root
   as possible (`app/providers.tsx` or equivalent): no business component living flat in `components/ui`.

### 4. Effects/state correctness and security (react-doctor)
A short checklist, the `error`-severity subset of the `react-doctor` scanner relevant to this stack
(React/Next core, not Ink/Remotion/R3F/shaders/React Native/React Router).

**Effects and state**:
1. Effect cleanup = the same reference removed as the one added (`addEventListener`,
   `observer.disconnect()`, `clearInterval`/`clearTimeout`, `unsubscribe()`), never an inline function
   recreated.
2. Never a prop callback / ref mutation / `Context`/store creation / navigation during render, that goes in
   a handler or a `useEffect`. A `Context`/store is created at module level.
3. A reducer returns a new object, never mutates its state in place.
4. List key = the item's stable id, never `Math.random()`/`Date.now()`/the index if the order changes.
5. Reactive effect dep: no `ref.current`/`location.pathname` as a dep, read them in the body.
6. An object/array/function recreated on every render and used as a dep/memoised prop → `useMemo`/
   `useCallback`/a module constant.

**Next.js App Router**:
7. `cookies()`/`headers()`/`draftMode()`/`params`/`searchParams`: always `await` (Next 15+).
8. Error boundary = a Client Component (`'use client'`). `global-error.tsx` wraps `<html><body>`.
9. `route.ts` exports named handlers (`GET`, `POST`...), never `export default`.
10. `next/head` is ignored in the App Router: go through the `Metadata` API.
11. No mutable module-level state on the server side (`let`/`var` outside a function), shared between
    concurrent requests.
12. An exported Server Action is callable by an unauthenticated client: it checks auth itself.

**Security, never negotiable**:
13. No secret committed: if one is, it's removed AND rotated, not just dropped from the next commit.
14. No hard-coded literal fallback on a secret env variable: fail closed.
15. `eval()`/`new Function()` on an untrusted string is forbidden: `JSON.parse` for data.
16. JWT: pin the expected algorithm (`{ algorithms: ['RS256'] }`), never accept `none`.
17. Shell command: never interpolation, arguments as an array, a strict allowlist.
18. A `GET` handler has no side effect (it gets preloaded/prefetched): a mutation is a `POST`.

**Accessibility and bundle weight**:
19. Never block paste on an authentication field (password, code).
20. Never disable viewport zoom: if the layout breaks at 200%, the layout is the problem.
21. An icon-only button with no visible label = a mandatory `aria-label`. An open modal = focus placed on
    it and trapped inside, returned to the trigger on close.
22. A default import from an icon lib or a heavy module loaded at the level of a rarely visited route =
    bloats the bundle for nothing: named import / `next/dynamic`.

## Output / checkpoint
Code compliant with the three sections above. No dedicated checkpoint: compliance is checked by `gate` (7)
and by `legolas` at review time in the `review` step (8).

## Guardrails
No comments in the code produced. Never modify a generated file in `components/ui` in place: always go
through a wrapper. Don't duplicate an existing hook or selector before checking that no nearby
hook/selector already covers the need. This block writes code, it doesn't review diffs; for the review,
that's `legolas`. When in doubt about a Redux/shadcn rule not covered here, escalate rather than guess.

## Origin
Ideas taken from: a market React skill catalogue (the react-best-practices skill, AGENTS.md,
perf/rendering/waterfall patterns with before/after examples) for the rendering/perf section; a market
React/Node skill catalogue (redux-toolkit/SKILL.md, typed createSlice, typed hooks, createAsyncThunk,
memoised selectors) for the Redux Toolkit section; a market shadcn skill catalogue (skills/shadcn/SKILL.md,
composition through a wrapper, cn(), folder structure, new-york/sonner/React 19) for the shadcn/ui section;
a market React linter (the `oxlint-plugin-react-doctor` package, a registry of ~780 deterministic rules,
`error`-severity subset filtered for relevance outside niche frameworks) for the correctness/security
section; a market open source TypeScript project (the `typescript-review` skill: accessibility/bundle-weight
blind spots) for items 21-22. Mechanisms rewritten, no copied text.
