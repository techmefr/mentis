# react-nextjs-conventions §5 — State, effects, hooks

> Section 5 of `skills/react-nextjs-conventions`. Read it when a hook is written, or an effect added. The other sections and the guardrails stay in `SKILL.md`.

1. **Rules of hooks**: never after a conditional return, never inside an `if`/loop/`try`. A hook called
   conditionally desynchronises React's internal order from the code's, so one hook receives another's
   state — the symptom is a value from an unrelated piece of the component, which is why it is rarely
   recognised as a hook-order problem (§4.2 covers where the guard goes instead).
2. **Never derive state in an effect**: a value computed from props or other state is a local variable or a
   `useMemo`, never a `useState` resynchronised by a `useEffect` — that pattern renders twice and holds a
   stale copy in between. Anything that reads the value during that gap sees the previous answer, and the
   two renders make every downstream effect fire twice as well.
3. **Immutable updates**: never `obj.field = value`, never `push`/`pop`/`splice`/`sort` on a value in state
   or received as a prop. Build a new object/array. A reducer returns new state, never mutates in place. The
   mutation does not fail loudly: the reference is unchanged, so React sees no update and the screen keeps
   the old value while the data is already new — and then an unrelated re-render makes it appear, which
   reads as a random delay.
4. **Never memoise on suspicion.** `useMemo`/`useCallback`/`React.memo` are answers to a measured problem;
   added "just in case" they cost a dependency array to keep correct and buy nothing. Profile first. The
   exception is correctness, not speed: a value used as a dependency or passed to a memoised child has to be
   stable, and there the memo is load-bearing.
5. **Let the library own its state**: no `useState(false)` next to a query or a form library that already
   exposes `isLoading`/`isError`/`isSubmitting`. Duplicated state is state that disagrees — and it
   disagrees exactly on the error path, where the library resets its flag and the handmade copy stays true,
   leaving a spinner that never stops.
6. **Render every state a query has**: loading, empty, and error, before mapping over the data. A component
   that calls a query hook then immediately maps the result crashes on the first slow network or empty
   result set. Empty is the one that gets skipped, and it is the one a user meets on their first day, when
   they have no records at all.
7. **Stable list keys**: the item's own id. `key={index}` reuses the wrong element after a sort or filter —
   the symptom is a row showing another row's data, or state stuck on the wrong item. With inputs in the
   rows it is worse than cosmetic: what the user typed moves to a different record, and the save is real.
8. **Effect cleanup removes exactly what was added** (`addEventListener`, `observer.disconnect()`,
   `clearInterval`/`clearTimeout`, `unsubscribe()`) — never an inline function recreated on each render, or
   nothing is actually removed. Listeners then accumulate one per render, so a handler that fires once
   becomes a handler that fires forty times, and the leak looks like a performance problem rather than a
   correctness one.
9. Never a prop callback, a ref mutation, a context/store creation, or a navigation **during render**: that
   goes in a handler or an effect. A context/store is created at module level. Render has to be safe to run
   twice and safe to discard — React does both — so a side effect there happens a number of times the code
   does not state.
10. No `ref.current` or `location.pathname` in a dependency array: they don't trigger a re-render, so the
    effect lies about when it runs. Read them in the body.
11. Functional `setState` (`setCount(c => c + 1)`) as soon as the new value depends on the old one — a
    handler can fire several times before the next render, and two increments each written against the
    captured `count` then produce one.
12. **Several `setState` calls in the same effect or handler for one logical update** is a sign the state
    should be one `useReducer` call, or a value derived instead of stored — each separate `setState` is a
    separate render, and a bug that reads the value between them is straightforward to introduce and hard to
    spot.
13. A handmade `isLoading`/`isPending` boolean gating a transition-worthy update (a tab switch, a filter
    re-render, anything that keeps the current UI interactive while new state computes) is what
    `useTransition`'s `isPending` already gives you, without blocking input on the stale screen.
14. **The dependency array is a claim about what the effect reads.** Omitting it entirely runs the effect on
    every render; writing `[]` over an effect that reads props or state freezes the first render's values
    inside it for the lifetime of the component, so a callback registered once keeps calling the original
    version with the original state. The fix is never to silence the linter — it is to make the effect
    depend on less, usually by moving the work into a handler.
15. **Cleanup runs on every dependency change, not only on unmount.** An effect that subscribes and cleans up
    correctly still tears down and re-establishes its subscription each time a dependency moves, which for
    an unstable dependency is every render — a socket that reconnects continuously, or a request fired in a
    loop. This is the case where point 4's memo is load-bearing.
16. **An effect that fetches has to survive going out of date.** The component can unmount before the
    response arrives, and two responses can land out of order, so the later navigation shows the earlier
    record's data. An `AbortController`, or an ignore flag set in the cleanup, is the minimum — and the
    better answer is usually not to hand-roll it at all (§6.1).
17. **An effect synchronises React with something outside React** — the DOM, a timer, a subscription, a
    browser API. If nothing outside is involved, it is the wrong tool: what happens because the user did
    something belongs in the handler that ran, where it happens once and can be read in order, rather than
    after a render, where it happens whenever the dependencies say so.
18. **A context provider's value has to be stable.** A fresh object literal passed as `value` re-renders
    every consumer on every parent render, which is how a context added for convenience becomes the
    application's performance problem. Memoise the value, and split contexts by how often they change: a
    rarely-changing user object and a per-keystroke draft do not belong in the same provider.
19. **State seeded from a browser-only source breaks hydration.** `useState(localStorage.getItem(...))` or
    anything reading `window` runs on the server with a different answer, so the markup React rendered and
    the markup it finds disagree, and it discards the tree. Read it in an effect after mount, and render a
    deliberate initial state until then.
20. **`useLayoutEffect` only for measure-then-paint.** Reading a size and positioning something in a normal
    effect shows the unpositioned frame first, which is the visible jump users report as flicker; the layout
    variant runs before paint. It has no server equivalent, so it warns during SSR — which is the signal
    that the work belongs behind a mount check rather than in the initial render.
21. **A form submission is `useActionState`, not a hand-rolled `isSubmitting` boolean around a `try`/
    `catch`.** It returns `[state, formAction, isPending]` from an `(previousState, formData) => newState`
    function, which is point 12's several-`setState`-for-one-update collapsed into the shape the framework
    already tracks — pending state, the last result and the error all move together, so there is no window
    where they can disagree. A submit button reading that pending state through `useFormStatus` — from a
    child of the `<form>`, not the component holding the state — stays reusable across every form without
    prop-drilling a boolean into it.
22. **`useOptimistic` is for the update the user should see immediately, never for the response you have
    not received yet.** It renders a pending value on top of the real state and reverts to whatever the
    real state settles to — success or failure — so the rollback is automatic and exactly point 6's
    invalidate-don't-hand-write rule applies to it: an optimistic entry is not the source of truth, the
    server's answer still is.
23. **`use()` reads a promise or a context conditionally, which the other hooks cannot.** It is not a
    replacement for `useEffect`+`useState` on a fetch a component owns (§6.1 already answers that); its
    place is reading a promise a Server Component started and passed down, or reading a context after an
    early return — where the rules-of-hooks restriction in point 1 would otherwise force the read above
    a check that makes it pointless.
24. **A compiler that auto-memoises does not repeal point 4, it changes the default answer.** Where the
    project's build has automatic memoisation enabled, a `useMemo`/`useCallback` added "just in case" is
    now genuinely redundant rather than merely unmeasured — the compiler already produces the equivalent
    fewer renders, and hand-written memoisation next to it is dead code that looks load-bearing. Check
    the project's own configuration before assuming either way; the correctness exception in point 4 (a
    dependency that must be referentially stable) still needs a human decision either the compiler or a
    manual memo can express.
