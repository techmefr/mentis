# react-nextjs-conventions §4 — Control flow

> Section 4 of `skills/react-nextjs-conventions`. Read it when conditional rendering, lists, early returns. The other sections and the guardrails stay in `SKILL.md`.

1. **Early returns** for guards: check null/undefined/invalid at the top and return, rather than wrapping the
   entire body in one `if` and burying the happy path under an indent. The gain is not cosmetic: with the
   guards at the top, every line below them reads under a precondition that has already been established, so
   whoever adds code there does not have to re-derive what can still be missing. A body wrapped in a single
   `if` also invites the next branch to be nested inside it, and nesting compounds — three guards written
   that way put the actual render four indents deep, where nobody reads it as the main path any more.
2. **In a component, the early return comes after every hook call**, never between them. This is the one
   place where the guard-first habit collides with §5.1: `if (!user) return null` placed above a `useEffect`
   changes how many hooks run on that render, and React matches hooks by call order rather than by name, so
   the state of one hook is handed to another. Compute the condition early and return late, or move the
   guarded part into its own component and let the parent decide whether to render it at all — that second
   form is usually the clearer one, because the guard then reads as a composition decision.
3. Never a short-circuit (`condition && sideEffect()`) purely for control flow: `if` states the intent, and
   an expression whose value is discarded reads like a mistake. The next reader cannot tell whether the
   author meant to branch or meant to compute something and then forgot to use the result, so the line
   survives every review that was looking for something else.
4. In JSX, `&&` only on a real boolean. `array.length && <List/>` renders a literal `0` when the array is
   empty — the classic stray zero on screen. Compare explicitly (`array.length > 0`). The rule generalises:
   React skips `false`, `null`, `undefined` and `''`, and renders everything else, so a numeric left-hand
   side leaks `0` and a computed one leaks `NaN` into the layout it was supposed to suppress. Both look like
   a data bug rather than a rendering one, which is why they get chased in the wrong file.
5. **A condition with no other branch leaves a hole, and a hole is unreadable.** `{isLoading && <Spinner/>}`
   with nothing for the loaded case is fine because the content sits next to it; `{hasAccess && <Panel/>}`
   alone means the reader cannot tell whether an empty area is the intended answer for someone without
   access or a forgotten message. Render the alternative explicitly, even if it is `null` behind a named
   variable, so the absence is a decision on the page rather than an inference.
6. **No ternary inside a ternary in JSX.** Two levels already require holding a truth table in the head while
   also parsing tags, and the diff of a change to the middle branch is unreadable. Three or more states are a
   lookup — an object keyed by the state, or a small function with early returns — and the moment the states
   come from a union, that function is also where §3.9's discriminated union pays off.
7. **A `switch` over a union closes with a `never` default.** Assigning the scrutinee to a `never`-typed
   variable in the default branch makes adding a variant to the union a compile error at every switch that
   handles it, instead of a silent fall-through that renders nothing. Without it, the new status ships as an
   empty region on a screen nobody thought to open.
8. **Guard the shape, not the truthiness.** `if (!items)` does not cover the empty array, `if (!count)`
   rejects a legitimate `0`, and `if (user)` is satisfied by `{}`. Each is the same mistake in a different
   direction: a falsy test standing in for a question about content. Ask the question that is actually being
   asked — `items.length === 0`, `count === undefined`, a field the object must have.
9. **Changing which element wraps a subtree unmounts the subtree.** `cond ? <Card><Form/></Card> : <Form/>`
   is not "the same form with an optional card": React compares by position and type, so flipping `cond`
   destroys the form and everything it held — typed input, scroll position, focus. Keep one branch and make
   the wrapper itself conditional (a component that renders `children` bare or wrapped), or accept the reset
   knowingly.
10. **The mirror of point 9 is a tool**: giving an element a `key` derived from what it represents resets it
    on purpose, which is the honest way to clear a form when the record it edits changes. Reaching instead
    for an effect that resynchronises every field is the derived-state anti-pattern of §5.2 wearing a
    different hat.
11. **Optional chaining is not an error branch.** `data?.items?.map(...)` renders an empty list identically
    for "still loading", "loaded and empty" and "the request failed", so the user gets a blank panel and no
    way to tell which. The chain silences the crash that would otherwise have told you a state was missing;
    render the three states explicitly (§5.6) and keep the chain for genuinely optional fields.
12. **No mutating array method during render.** `items.sort()` and `items.reverse()` sort in place, so a
    component that sorts a prop before mapping it rewrites its parent's data as a side effect of drawing —
    the parent's order changes, other consumers see it, and nothing in the component announces that it
    happened. Copy first (`[...items].sort()`, or `toSorted`), which is the same rule as §5.3 applied to the
    render body rather than to an update.
13. **`forEach` cannot stop.** A callback that needs to abort early wants `some`, `find`, `every` or a plain
    `for...of`; a `return` inside `forEach` only ends that iteration, so the loop keeps running and any work
    after the intended break still happens. It reads as an early exit and behaves as a filter.
