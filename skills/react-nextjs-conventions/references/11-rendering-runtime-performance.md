# react-nextjs-conventions §11 — Rendering and runtime performance

> Section 11 of `skills/react-nextjs-conventions`. Read it when a list grows, an interaction feels heavy, a scroll or input handler is added, or a component re-renders more than it should. The other sections and the guardrails stay in `SKILL.md`. Measure first (`skills/webperf`): every point below is a candidate cause, not a routine pass.

1. **A state update that is not urgent goes in a transition.** Typing in a search box and filtering ten thousand
   rows from it are two updates of different priority; putting both in plain `setState` makes the keystroke wait
   for the list, so the input visibly lags behind the keyboard. `startTransition` (or `useTransition`) marks the
   list update as interruptible, and React keeps the input responsive and abandons the stale list render when
   the next key arrives.
2. **`useDeferredValue` when the value arrives from above and cannot be wrapped.** A prop or a context value
   cannot be put in a transition by the component that receives it; deferring it renders the expensive subtree
   with the previous value until the urgent work has finished. Pair it with a memoised child, otherwise the
   deferred render recomputes everything anyway and the deferral buys nothing.
3. **A value that changes often and is not displayed lives in a ref, not in state.** A scroll offset, a timer
   id, the last pointer position, a previous prop: each `setState` re-renders the component for a value no
   pixel depends on, and the symptom is a component that re-renders sixty times a second while looking
   unchanged. Read it in the handler that needs it.
4. **Subscribe to the derived boolean, not to the raw value.** A component that needs "is the window narrow"
   and subscribes to the window width re-renders on every pixel of a resize; subscribing to the comparison
   re-renders when the answer changes. The same applies to a store selector (§6): select the field, not the
   object that contains it.
5. **Read state at the point of use when it is only used in a callback.** Reading `searchParams` or a store
   value in the render body to use it once inside a click handler subscribes the whole component to a value
   it never displays. Read it inside the handler, and the component stops re-rendering for changes that do not
   affect what it shows.
6. **Functional `setState` when the next value depends on the previous one.** A callback closed over `count`
   captures the value from the render it was created in, so two updates in the same event both start from the
   same number and one is lost — and the callback then needs `count` in its dependencies, which recreates it
   on every change. `setCount(c => c + 1)` is correct in both cases.
7. **Lazy initial state for anything that is not free to compute.** `useState(parse(storage))` runs the parse
   on every render and throws the result away after the first; `useState(() => parse(storage))` runs it once.
   The cost is invisible on a small input and shows up as a slow keystroke once the input grows.
8. **A default non-primitive prop value is a new reference on every render.** `({ items = [] })` or
   `({ onChange = () => {} })` on a memoised component defeats the memo: the default is a fresh object each
   time, so the comparison always fails and the component re-renders as though it were not memoised. Hoist the
   default to a module constant.
9. **Do not memoise a primitive-returning expression that is cheaper than the memo.** `useMemo(() => a && b, …)`
   costs a closure, a dependency array and a comparison to save one boolean operation. Memoisation earns its
   keep on a result that is expensive to build or whose identity matters to a dependency (point 4 of §5), not
   on an expression that returns a boolean or a number.
10. **Narrow effect dependencies to the primitives actually read.** An effect that depends on a whole `user`
    object re-runs when any field of it changes, including the ones it never uses; depending on `user.id`
    re-runs it when the answer to its question changes. A depended-on object that is rebuilt every render
    re-runs the effect every render, which is the form of this that reaches production as a request storm.
11. **Put interaction logic in the event handler, not in an effect that watches state.** "When `submitted`
    becomes true, post the form" runs a render late, runs again if anything it reads changes, and cannot tell
    a user action from a state restore. The handler runs exactly once per interaction and knows which one it is.
12. **Split a hook that computes several unrelated things from different inputs.** One `useMemo` returning three
    values from three dependency sets recomputes all three when any input changes. Three memos, or three small
    hooks, recompute only the one whose input moved.
13. **Hoist static JSX out of the component.** An element tree that depends on nothing (an empty-state
    illustration, a fixed icon row) is rebuilt on every render for no reason; a module constant is built once
    and reused. It matters most for large static SVG, where the recreated tree is also reconciled each time.
14. **`content-visibility: auto` for a long list or a long page of independent blocks.** The browser skips
    layout and paint for blocks outside the viewport, which on a few hundred rows is the difference between a
    slow first render and a normal one, with no JavaScript. Give the block a `contain-intrinsic-size` close to
    its real height, otherwise the scrollbar jumps as blocks are measured. Past a few thousand items, virtualise
    instead (`skills/webperf` §2.4): this property skips rendering work, it does not remove DOM nodes.
15. **Animate a wrapper, not the SVG element.** CSS transforms on an `<svg>` itself do not take the hardware
    path in every browser, so a spinner built that way costs main-thread time on every frame. Wrap it in a
    `div`, animate the wrapper, and the same animation runs on the compositor.
16. **Render conditionally with an explicit boolean, never with a bare number or string.** `{count && <List />}`
    renders a literal `0` when the count is zero, and on React Native crashes outright on a falsy string. Compare
    (`count > 0 &&`) or use a ternary; the bug looks like a stray character on screen, not like a logic error.
17. **`<Activity>` (React 19.2+) to hide a subtree that comes back, instead of unmounting it.** A tab panel or a
    drawer remounted on every open loses its state and re-runs its effects; an Activity boundary keeps the state
    and pauses the effects while it is hidden. Use it where the state is worth keeping, not as the default for
    every conditional.
18. **Avoid a flicker between server and client by rendering the stored value before paint.** Reading
    `localStorage` for a theme in an effect shows the default for a frame and then flips. Either keep the value
    in a cookie the server can read, or inject a tiny synchronous script before the app that sets the attribute
    first; a suppressed hydration warning (`suppressHydrationWarning`) is acceptable only on that exact element
    whose server and client values are expected to differ, never as a blanket (§5).
19. **Event listeners that do not call `preventDefault` are registered `{ passive: true }`.** A non-passive
    `touchstart`, `wheel` or `scroll` listener forces the browser to wait for the handler before it can scroll,
    which is the cause of jank on touch devices that no profiler of the component will show. React's own
    synthetic scroll and touch props are already passive where the platform allows it; the rule is for the
    listeners you attach by hand.
20. **One global listener, shared, not one per component instance.** A `resize` or `keydown` listener added in
    a hook that is used by two hundred rows is two hundred listeners; keep a module-level subscription and a
    set of callbacks. The cost is linear in rows and invisible until the page grows.
21. **Version and minimise what goes in `localStorage`.** Store only the fields read back, under a key that
    carries a schema version, and wrap read and write in `try`/`catch`: a stored shape from last month's release
    parsed by this month's code is a crash on the user's second visit, and the storage can be full, blocked or
    absent in a private window.
22. **Batch DOM reads and writes; never read layout in the render.** Reading `offsetHeight` or
    `getBoundingClientRect()` between writes forces a synchronous layout each time (layout thrashing); read
    everything first, write after, and do it in an effect or an observer rather than in the render body.
    Prefer CSS (flex, grid, `:has`, container queries) to a JavaScript measurement wherever the platform can
    express the layout.
23. **Defer non-critical work to idle time.** Analytics batching, prefetching and cache warming run in
    `requestIdleCallback` (with a `setTimeout` fallback on Safari), so they stop competing with the interaction
    that is happening now.
24. **Preload on intent, not on load.** Starting the import of a heavy module on `pointerenter` or `focus` of
    the control that will need it hides most of the load time behind the user's own movement, without paying
    for it on pages where the control is never used. It complements §7.3 (`next/dynamic`), it does not replace it.
25. **Load third-party scripts after hydration.** Analytics, chat widgets and tag managers do not need to block
    the first paint; load them with `strategy="afterInteractive"` or `lazyOnload`, or `defer`/`async` on a plain
    `<script>`. A blocking third-party script is a first-paint cost the team does not control and cannot
    debug.
26. **Resource hints go through the framework, not hand-written `<link>` in a layout.** `preconnect` to the
    API and CDN origin and `preload` for the one font or hero image that gates first paint, through
    `react-dom`'s `preconnect`/`preload`/`prefetchDNS` or the framework's equivalent, so the hint is
    de-duplicated and sent early. A page that hints everything hints nothing: two or three hints that the
    waterfall shows to be on the critical path.
27. **A navigation or list transition is a View Transition, not a hand-rolled animation.** Wrapping the state
    change in `document.startViewTransition` (or React's `<ViewTransition>` where the project's React version
    ships it) lets the browser snapshot and interpolate the two states, so a shared element moves between
    pages without measuring either one in JavaScript. Give each shared element a unique `view-transition-name`
    — two elements with the same name on the page abort the whole transition — and wrap the call in
    `prefers-reduced-motion` handling (`skills/webperf`, interface rules §1). Where the API is absent the
    state change must still happen, so feature-detect and fall through to the plain update.
