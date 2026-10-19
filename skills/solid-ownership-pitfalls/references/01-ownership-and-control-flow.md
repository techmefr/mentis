# solid-ownership-pitfalls §1 — Ownership and control flow

A Solid component function runs once, when it is first rendered. Everything reactive that it creates is owned
by the owner active at that moment and is disposed with it. These rules keep ownership where you meant it.

## 1.1 Component calls and owners
1. **Render a component with JSX, never as a plain call.** JSX compiles to `createComponent`, which gives the
   component its own reactive owner. Calling `MyComp(props)` runs the body inside the caller's owner. The
   component appears to work, then silently resets its state each time the caller re-runs, and its signal reads
   become the caller's dependencies.
2. **For a dynamic component use `Dynamic` or capture the reference first.** `<Dynamic component={x} />`, or
   assign the component to a variable and render it inside a `Show` that hands it back as a function.
3. **Do not create primitives inside effects, memos or computeds.** Anything created there (`createSignal`,
   `createMemo`, a router match hook, a query hook) is created again on every run and disposed on the next, so
   the state and subscriptions are lost. Call hooks once at component level and derive with `createMemo`.
4. **Creating a root detaches ownership.** `createRoot` makes a new owned context and its computations live
   until the supplied `dispose` is called. A root created without a `dispose` parameter is unowned and its
   computations are not managed, which can leak. Use it for module-level state you mean to keep.
5. **Do not clear shared state on navigation alone.** In a split-pane layout several routed pages can be
   mounted at once, so a reset triggered by a path change clears state owned by a pane that did not unmount.
   Clean up with `onCleanup` in the page or resource owner that actually unmounts, and test narrow and wide
   layouts, whose mounting differs.

## 1.2 Show, Switch and Match
1. **`Show` and `Match` are keyed by truthiness unless told otherwise.** Replacing one truthy value with another
   truthy value does not recreate the child. Going from record A to record B leaves the child mounted with
   record A's internal state and shows wrong data without an error.
2. **Add `keyed` when the child holds state that belongs to one value.** With `keyed`, a change of the `when`
   value (compared by reference) renders the child again, giving a full remount for a form or editor.
3. **Do not render the same component in two branches.** A component placed in both a `Switch` fallback and a
   `Match`, or in several `Show` branches, is unmounted when the branch changes and a new instance mounts in
   the other one. Local state, focus and scroll position are lost, and mount and cleanup run again.
4. **Keep it in one place and change the layout around it.** Place the component outside the branching
   element, toggle a class for the layout, and put only the differing parts inside the conditional. If it must be
   hidden but alive, use CSS rather than unmounting.

## 1.3 Children
1. **Use the `children` helper before reading `props.children`.** It resolves and memoises the children, so
   repeated reads use the resolved result instead of recreating the child structure. Reading `props.children`
   twice (once in a preview, once in the body) can create the children twice.
2. **Resolve once, then use the accessor** wherever the children appear or are inspected, instead of iterating
   `props.children` yourself.

## Verification
- Make the parent re-run (change a signal it reads) and confirm the child's local state survived (§1).
- Switch a `keyed` `Show` between two records and confirm the child shows the second record's data (§1).
- Switch a layout branch and confirm focus and scroll position in the shared component are unchanged (§1).
