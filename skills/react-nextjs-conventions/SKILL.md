---
name: react-nextjs-conventions
description: Use when writing or reviewing anything on the React/Next.js stack, component and file structure, naming, typing, hooks discipline, immutability, memo discipline, server-state library conventions (TanStack Query, Zustand, RTK), validation at boundaries, Next.js App Router rules, component-library composition, and the effects/security/a11y correctness rules derived from the react-doctor linter. Self-contained, it assumes no plugin or catalogue installed.
---

# react-nextjs-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing of code on the React 18/19 + Next.js stack. Every
rule below holds in a repo with **nothing installed** (`CONVENTIONS.md`, rule A). Complementary to `legolas`
(the diff review agent): here we write the code, legolas re-reads it afterwards.

**Relation to an org skill catalogue.** Where a company ships its own versioned catalogue for this stack, it
is the authority on **its** house style and overrides this block wherever the two differ. This block is the
generic default. Two house conventions in particular genuinely split across real codebases — `type` vs
`interface` for object shapes, and where tests live — and this block says "pick one and apply it uniformly"
rather than pretending there's a universal answer.

**On a Laravel + Inertia.js app with React pages, there is no Next.js runtime** (no App Router, no
Next data fetching) — a page there is a plain component wired by Inertia. This block's Next-specific
sections don't have an equivalent in that architecture; see `skills/inertia-conventions` §4 before
flagging an Inertia repo against them.

## When
As soon as a `.tsx` component, a Next.js route, a hook, a store slice or a query hook is written or modified,
during `code` (6) or `tdd` (5).

## Steps

### 1. Components and files
1. **One component per file**, the file named after the component it exports. A helper sub-component added
   inline is invisible to search and untestable on its own.
2. **Never define a component inside another component's body**: it recreates the type on every render and
   unmounts/remounts the whole subtree, losing state and focus. This is also why a `React.memo` "doesn't
   work" and why effects re-run every render. Move it to module level.
3. **Named exports only**, never `export default`: a default export is renamed freely at each import site,
   so the same component ends up under three names and greps for none of them.
4. **Separate the container from the presentation**: a component that fetches, holds business logic and
   renders a full UI does three jobs. The data/logic side goes in a hook or a container; the JSX side stays a
   presentational component that takes props.
5. Extract shared **knowledge** into a hook or utility, and shared **meaningful** JSX into a component — but
   don't over-extract trivial layout markup: a `<div className="flex">` wrapper is not a component.
6. **Prop drilling past two layers is a structure problem, not a naming one.** A prop threaded unchanged
   through a component that never reads it, just to reach a grandchild, means that middle component takes on
   a dependency it doesn't have — composition (pass the element itself as a child/slot) or a scoped context
   fixes the layer that doesn't need to know, without reaching for a global store.
7. Props typed through a named props type, destructured in the signature rather than reached through
   `props.x` — the destructuring is the component's documented input list.

### 2. Naming
1. Functions declared as arrow functions assigned to a `const`, consistently.
2. **No abbreviations** in identifiers: `expense` not `exp`, `index` not `idx`, `error` not `err`,
   `button` not `btn`, `previous` not `prev`, `event` not `e`. The keystrokes saved cost every future reader
   a guess.
3. A function name **starts with an action verb**: `formatAmount`, not `amount`; `fetchBills`, not `bills`.
   A noun-named function reads like a value at the call site.
4. Booleans prefixed `is`/`has`/`can`/`should`, including boolean props and JSX flags.
5. **Callback prop vs handler**: the prop is `onSomething`, the function implementing it is
   `handleSomething`. Swapping them makes it impossible to tell an incoming contract from a local
   implementation.
6. A hook wrapping a server query is `use` + Resource + `Query`; a hook wrapping a mutation is `use` + verb +
   Subject + `Mutation`. `useBill`, `fetchBills` and `createClientVatMutation` each break it in a different
   way.
7. The result of a mutation hook is stored as the **whole result object** under a derived name, not
   destructured into bare `mutate`/`isPending` — two mutations in one component collide immediately
   otherwise.
8. **Named constants** instead of inline literals: a numeric threshold in a condition, a status code, a
   timeout, a string used as an identifier. A magic value whose meaning isn't obvious from context is a
   comment waiting to be needed.
9. Query keys in one casing, camelCase by default, across every key segment — a mismatched key silently
   fails to invalidate, which looks like a caching bug.

### 3. Typing
1. `any` is banned, including in a `catch` clause: `unknown` plus narrowing. `catch (e: unknown)` and a type
   guard, not `catch (e: any)`.
2. **No type assertions** (`as`, and the non-null `!`), except `as const`. An assertion is a claim the
   compiler cannot check; a narrowing check is one it can.
3. **Derive types rather than re-listing fields**: `Pick`/`Omit`/`Partial` off the source type, or inferred
   from the validation schema. A hand-copied subset drifts the day a field is added.
4. A **string union** rather than an `enum` for a fixed set of string values: it needs no runtime object, it
   narrows properly, and it serialises as itself.
5. `type` or `interface` for object shapes: **pick one per project and apply it uniformly**. Both are
   defensible; a codebase using both for the same kind of shape is not.
6. **Validate at every untrusted boundary** (API response, `localStorage`/`sessionStorage`, URL query
   params, `postMessage`) with a schema, and derive the type from the schema. This is the correct
   replacement for `as SomeResponse` on a fetch result: the assertion claims a shape, the schema checks it.

### 4. Control flow
1. **Early returns** for guards: check null/undefined/invalid at the top and return, rather than wrapping the
   entire body in one `if` and burying the happy path under an indent.
2. Never a short-circuit (`condition && sideEffect()`) purely for control flow: `if` states the intent, and
   an expression whose value is discarded reads like a mistake.
3. In JSX, `&&` only on a real boolean. `array.length && <List/>` renders a literal `0` when the array is
   empty — the classic stray zero on screen. Compare explicitly (`array.length > 0`).

### 5. State, effects, hooks
1. **Rules of hooks**: never after a conditional return, never inside an `if`/loop/`try`. A hook called
   conditionally desynchronises React's internal order from the code's.
2. **Never derive state in an effect**: a value computed from props or other state is a local variable or a
   `useMemo`, never a `useState` resynchronised by a `useEffect` — that pattern renders twice and holds a
   stale copy in between.
3. **Immutable updates**: never `obj.field = value`, never `push`/`pop`/`splice`/`sort` on a value in state
   or received as a prop. Build a new object/array. A reducer returns new state, never mutates in place.
4. **Never memoise on suspicion.** `useMemo`/`useCallback`/`React.memo` are answers to a measured problem;
   added "just in case" they cost a dependency array to keep correct and buy nothing. Profile first. The
   exception is correctness, not speed: a value used as a dependency or passed to a memoised child has to be
   stable, and there the memo is load-bearing.
5. **Let the library own its state**: no `useState(false)` next to a query or a form library that already
   exposes `isLoading`/`isError`/`isSubmitting`. Duplicated state is state that disagrees.
6. **Render every state a query has**: loading, empty, and error, before mapping over the data. A component
   that calls a query hook then immediately maps the result crashes on the first slow network or empty
   result set.
7. **Stable list keys**: the item's own id. `key={index}` reuses the wrong element after a sort or filter —
   the symptom is a row showing another row's data, or state stuck on the wrong item.
8. **Effect cleanup removes exactly what was added** (`addEventListener`, `observer.disconnect()`,
   `clearInterval`/`clearTimeout`, `unsubscribe()`) — never an inline function recreated on each render, or
   nothing is actually removed.
9. Never a prop callback, a ref mutation, a context/store creation, or a navigation **during render**: that
   goes in a handler or an effect. A context/store is created at module level.
10. No `ref.current` or `location.pathname` in a dependency array: they don't trigger a re-render, so the
    effect lies about when it runs. Read them in the body.
11. Functional `setState` (`setCount(c => c + 1)`) as soon as the new value depends on the old one — a
    handler can fire several times before the next render.
12. **Several `setState` calls in the same effect or handler for one logical update** is a sign the state
    should be one `useReducer` call, or a value derived instead of stored — each separate `setState` is a
    separate render, and a bug that reads the value between them is straightforward to introduce and hard to
    spot.
13. A handmade `isLoading`/`isPending` boolean gating a transition-worthy update (a tab switch, a filter
    re-render, anything that keeps the current UI interactive while new state computes) is what
    `useTransition`'s `isPending` already gives you, without blocking input on the stale screen.

### 6. Server state and stores
1. Reach for the ecosystem's server-state library (TanStack Query, SWR, RTK Query) rather than
   `useEffect` + `useState` for anything cached, deduped or invalidated. A hand-rolled cache is the part
   that's always subtly wrong.
2. **Query keys through a central factory**, never literal arrays scattered across files: an invalidation
   only matches if the key is built the same way in both places, and a typo silently invalidates nothing.
3. **Split the mutation callbacks by concern**: cache invalidation belongs in the hook (it's part of the data
   contract), UI feedback like a toast belongs in the calling component (it's part of that screen). Toasts
   fired from inside the hook appear on screens that never asked for them.
4. Prefer the callback form (`mutate` with `onSuccess`/`onError`) over `await mutateAsync` wrapped in
   `try`/`catch`: a bare `await mutateAsync` without a catch is an unhandled rejection waiting to happen.
5. Read a store through **atomic selectors**, one value per call, never by destructuring the whole store
   object: destructuring subscribes the component to every field and re-renders on all of them.
6. A store is for state genuinely shared across unrelated components; everything else stays local.
7. Where the project's server-data layer is Redux Toolkit rather than Query/Zustand: one slice = a typed
   `createSlice` (typed `initialState`, `PayloadAction<T>`, never an `any` action); typed
   `useAppDispatch`/`useAppSelector` wrappers, never the raw hooks in components; `createAsyncThunk` with
   `rejectWithValue` so the slice can tell a business rejection from an exception; a memoised
   `createSelector` for anything derived; RTK Query rather than a homemade thunk for standard cached CRUD.

### 7. Next.js
1. Parallelise independent fetches with `Promise.all` in Server Components: one `await` after another
   creates a network waterfall that's invisible when reading the component top to bottom.
2. `next/dynamic` for any heavy component not needed for the first paint (rich editor, chart, complex
   modal), with `ssr: false` if it depends on the DOM/window.
3. `cookies()`/`headers()`/`draftMode()`/`params`/`searchParams`: always `await` (Next 15+).
4. An error boundary is a Client Component (`'use client'`); `global-error.tsx` wraps `<html><body>`.
5. `route.ts` exports **named** handlers (`GET`, `POST`…), never `export default`.
6. `next/head` is ignored in the App Router: go through the `Metadata` API.
7. No mutable module-level state on the server side (`let`/`var` outside a function): it's shared between
   concurrent requests, i.e. between users.
8. **An exported Server Action is a public endpoint**: it is callable by an unauthenticated client and
   checks authorisation itself. Being imported by one protected page proves nothing.
9. A `GET` handler has no side effect — it gets prefetched and preloaded. A mutation is a `POST`.

### 8. The component library
1. A copy-and-own component set (shadcn-style) is generated once and then **owned by the project**: it isn't
   a versioned dependency updated from outside.
2. Extend a generated component through a wrapper composing it, never by editing the generated file in
   place: a regeneration or another consumer inherits the deviation otherwise.
3. One merge point for utility classes (a `cn()`-style `clsx` + `tailwind-merge` helper): never a hand-built
   class string, never two sources of conditional classes on one component.
4. Folder split held: generated primitives in their own folder untouched, business wrappers above them,
   helpers and shared hooks in their own places. No business component living flat among the primitives.

### 9. Security, never negotiable
1. No secret committed. If one is, it's removed **and rotated** — dropping it from the next commit leaves it
   in the history.
2. No hard-coded literal fallback on a secret env variable: fail closed, loudly, at boot.
3. `eval()`/`new Function()` on an untrusted string is forbidden: `JSON.parse` for data.
4. JWT: pin the expected algorithm (`{ algorithms: ['RS256'] }`), never accept `none`.
5. A shell command: never string interpolation, arguments as an array, a strict allowlist.
6. Never an auth token in `localStorage`/`sessionStorage`: an `HttpOnly`, `Secure`, `SameSite` cookie set
   server-side is the only sane option.

### 10. Accessibility and bundle weight
1. An icon-only button with no visible label needs an `aria-label`. Every `<img>` needs an `alt`: the
   description if it carries meaning, `alt=""` (never omitted) if it's purely decorative — a missing `alt`
   reads out the filename to a screen reader.
2. An open modal: focus placed on it, trapped inside, returned to the trigger on close.
3. Native semantic elements over clickable `div`s; heading order without skipped levels.
4. Never block paste on an authentication field (password, one-time code).
5. Never disable viewport zoom: if the layout breaks at 200%, the layout is the problem.
6. A default import from an icon lib, or a heavy module loaded at the level of a rarely visited route,
   bloats the bundle for nothing: named import / `next/dynamic`.

## Output / checkpoint
Code compliant with the sections above. No dedicated checkpoint: compliance is checked by `gate` (7) and by
`legolas` at review time in the `review` step (8).

## Guardrails
No comments in the code produced. Never modify a generated component file in place: always go through a
wrapper. Don't duplicate an existing hook or selector before checking that no nearby one covers the need.
This block writes code, it doesn't review diffs; for the review, that's `legolas`. Where an org catalogue is
installed and disagrees with a rule here, **it wins** — say so explicitly rather than silently applying
either one. When in doubt about a rule covered by neither, escalate rather than guess.

## Origin
Ideas taken from: a market React skill catalogue (perf/rendering/waterfall patterns) for the Next.js
rendering rules; a market React/Node catalogue (`redux-toolkit`) for the RTK paragraph; a market shadcn
catalogue for the component-library section; a market React linter (the `oxlint-plugin-react-doctor` package,
a registry of ~780 deterministic rules, `error`-severity subset filtered for relevance outside niche
frameworks) for the effects/security section; a market open source TypeScript project (the
`typescript-review` skill) for the accessibility/bundle-weight items; **an org skill catalogue for this stack
(36 skills: file and component structure, container/presentational split, naming across identifiers, verbs,
booleans, handlers, query and mutation hooks, typing including derived types, string unions, assertions and
schema validation at boundaries, control flow, hooks discipline, immutability, memo discipline, library-owned
state, query-key factories, mutation callback split, atomic store selectors)** — rules extracted,
de-identified and rewritten generically, with everything naming an internal library or project deliberately
left out (rule C). Mechanisms rewritten, no copied text. Stamped 2026-08-06.

Re-checked directly against the public **React Doctor** tool (react.doctor, the linter this block's
effects/security section already traces to) on 2026-08-10: its documented rule set added three genuine gaps
— prop drilling across component layers (§1.6), several `setState` calls for one logical update belonging
in a `useReducer`/derived value, and a hand-rolled `isLoading` boolean where `useTransition` already applies
(§5.12-13) — plus a missing-`alt` check folded into the existing icon-label rule (§10.1). Everything else it
flags (unnecessary derived-state effects, array-index keys, hardcoded secrets, incorrect hook usage) was
already covered here under a different heading.
