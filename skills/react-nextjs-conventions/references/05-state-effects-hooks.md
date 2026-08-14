# react-nextjs-conventions §5 — State, effects, hooks

> Section 5 of `skills/react-nextjs-conventions`. Read it when a hook is written, or an effect added. The other sections and the guardrails stay in `SKILL.md`.

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
