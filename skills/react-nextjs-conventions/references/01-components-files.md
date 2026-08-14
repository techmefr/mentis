# react-nextjs-conventions §1 — Components and files

> Section 1 of `skills/react-nextjs-conventions`. Read it when a component is created or split. The other sections and the guardrails stay in `SKILL.md`.

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
