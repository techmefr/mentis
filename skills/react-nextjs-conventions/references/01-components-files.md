# react-nextjs-conventions §1 — Components and files

> Section 1 of `skills/react-nextjs-conventions`. Read it when a component is created or split. The other sections and the guardrails stay in `SKILL.md`.

1. **One component per file**, the file named after the component it exports. A helper sub-component added
   inline is invisible to search and untestable on its own — and it is the one that grows, because adding to
   a component nobody can find costs nothing in review.
2. **Never define a component inside another component's body**: it recreates the type on every render and
   unmounts/remounts the whole subtree, losing state and focus. This is also why a `React.memo` "doesn't
   work" and why effects re-run every render. Move it to module level. The symptom people report is an input
   that clears itself while typing, which is chased in the input rather than in the parent that redefines it.
3. **Named exports only**, never `export default`: a default export is renamed freely at each import site,
   so the same component ends up under three names and greps for none of them. It also breaks the rename
   refactor — the tool updates the declaration and leaves every import alone, silently. **Exception, not a
   choice: the App Router's file-convention modules** (`page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`,
   `not-found.tsx`, `template.tsx`, `global-error.tsx`) — the router requires a default export on these
   specific files and there is no named-export alternative (confirmed by building one: `next build` doesn't
   pick up a named export there). The rule still holds for every component that isn't one of these files,
   including one rendered *by* a page — only the file the router itself loads by convention is exempt. This
   is the mirror image of §7.10 (`route.ts` handlers take named exports only, no default) — the two file
   kinds sit in the same folder tree with opposite export rules, which is worth stating plainly rather than
   discovering from a build error.
4. **Separate the container from the presentation**: a component that fetches, holds business logic and
   renders a full UI does three jobs. The data/logic side goes in a hook or a container; the JSX side stays a
   presentational component that takes props. The practical payoff is testing: a presentational component is
   exercised by passing props, while the same markup behind a query hook needs the network faked before a
   single assertion about layout can be made.
5. Extract shared **knowledge** into a hook or utility, and shared **meaningful** JSX into a component — but
   don't over-extract trivial layout markup: a `<div className="flex">` wrapper is not a component. The
   over-extracted version costs more than it saves, because every reader now has to open a file to learn
   that it contains nothing.
6. **Prop drilling past two layers is a structure problem, not a naming one.** A prop threaded unchanged
   through a component that never reads it, just to reach a grandchild, means that middle component takes on
   a dependency it doesn't have — composition (pass the element itself as a child/slot) or a scoped context
   fixes the layer that doesn't need to know, without reaching for a global store.
7. Props typed through a named props type, destructured in the signature rather than reached through
   `props.x` — the destructuring is the component's documented input list, so a prop that stops being used
   shows up in the diff instead of lingering as a `props.` access three screens down.
8. **A component's imports declare which layer it is in.** A presentational component that imports a query
   hook has become a container without anyone deciding it should, and the split of point 4 is gone while the
   folder still claims it holds. This is the check worth running on a diff: not "is the file in the right
   place" but "does what it imports match where it lives".
9. **Prefer a slot to a prop per part.** `headerTitle`, `headerIcon` and `headerAction` are three props that
   will become five; a `header` slot taking an element lets the caller compose whatever it needs and stops
   the component from having to anticipate. The same reasoning caps prop count: a signature with a dozen
   props is usually two components sharing a name.
10. **A `variant` prop added per consumer is a refusal to split.** Each new caller widens the component's
    contract, every branch has to keep working for every other screen, and the file becomes the place where
    unrelated requirements meet. Two components that share their genuinely common parts are cheaper than
    one that serves both (§8.8).
11. **Colocate the component with its test and its styles.** A parallel test tree makes deleting a feature a
    two-place operation, which means it becomes a one-place operation and the orphaned test either fails
    for nobody or passes forever against nothing.
12. **The deletion test is the structure test.** If removing a feature means editing files in five folders,
    the folders are organised by technical kind rather than by feature, and every change to that feature
    will pay the same tax. A top-level `components/` `hooks/` `utils/` split reads tidy and scatters each
    feature across all three.
13. **A barrel that re-exports everything is not a public surface.** It defeats tree-shaking, so importing
    one helper pulls the folder; it creates import cycles that are easy to add and hard to see; and it hides
    which of the folder's contents were meant to be used from outside. Export deliberately, or import from
    the file.
14. **A circular import between components fails at render, not at build.** The symptom is a component type
    that is `undefined` — React reports an invalid element type and names nothing useful — so the cause is
    diagnosed from the import graph rather than from the stack trace. It is almost always a barrel (point
    13) or a component reaching back up to its parent.
15. **Split on reasons to change, not on line count.** A three-hundred-line component that changes for one
    reason is fine; an eighty-line one that changes whenever either the API or the design moves is already
    two components. Line count is a symptom that gets treated as the diagnosis, and the resulting split
    puts the seam in the wrong place.
16. **The server/client boundary is a file-level architectural decision.** Where `'use client'` sits decides
    what ships to the browser (§10.14) and what may cross as a prop (§7.9), so it is chosen when the
    component tree is designed rather than added to the file that happened to need a hook.
