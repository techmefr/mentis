# react-jsx-and-promise-lint-pitfalls §2 — Component identity and state naming

> Part 2 of `skills/react-jsx-and-promise-lint-pitfalls`. Read it when a component or a render function is
> defined inside another, or when state is declared. Sourced from the rule pages
> `no-unstable-nested-components` and `hook-use-state` of eslint-plugin-react (commit `bd381cd`), read
> 2026-10-16. Sentences marked "own guidance" are ours.

## 2.1 A component defined inside a component is a new component every render
1. **React compares element types by reference.** A function component declared in the body of another is a
   new function on every render of the parent, so React sees a different type, throws away the old subtree
   with its state, and builds a new one. The rule page gives this as the reason: the state of the nested
   component is lost on each parent re-render, with extra virtual DOM work.
2. **What the rule reports:** a component function declared in a component's body and rendered as `<Nested />`;
   a function that returns JSX passed in a prop and then rendered as an element by the receiver
   (`footer={() => <div />}` where the receiver writes `<Footer />`); and the same inside a class `render`.
3. **The fix is to move the component out.** Declare it at module level and pass what it needs as props. The
   rule accepts passing an element instead of a function (`footer={<div />}`).
4. **Own guidance, verify:** type into an input inside the nested component, then cause the parent to
   re-render; the text disappears. Move the component out and repeat; the text stays.

## 2.2 Render props are the allowed case, when they are called
1. **A prop whose name starts with `render` may take a function that returns JSX.** The default
   `propNamePattern` is `render*`; the rule page's example calls it, `props.renderFooter()`, in the receiver.
   Another convention can be allowed with a pattern such as `*Renderer`.
2. **The receiver must call it, not render it as an element.** The page says that with `allowAsProps` you must
   make sure the props are called and not used as elements. `props.footer()` is a call; `<Footer />` is a
   component type and brings back the first problem.
3. **Own guidance:** name a function prop by what the receiver does with it. A prop called `renderRow` that
   the receiver uses as `<renderRow />` is the mismatch the rule exists for.

## 2.3 Memoizing does not make it stable enough
1. **A nested component wrapped in `useCallback` or `useMemo` is not reported but should also be avoided.**
   The rule page says it does not detect those.
2. **With no dependencies, move the definition out safely.** With dependencies, the page says to restructure so
   the component can move out of the render function (own guidance: usually by passing the dependency as a
   prop).
3. **If you want the state thrown away on purpose, use a `key`.** The page offers this as the alternative:
   changing the `key` on a component resets its state, deliberately and visibly.
4. **Own guidance:** a memoized nested component with dependencies still gets a new identity whenever the
   dependencies change, which makes the state reset appear at random moments; prefer the explicit `key`.

## 2.4 State and setter naming
1. **Destructure `useState` into a value and a setter named as a pair.** The rule `hook-use-state` reports a
   result that is not destructured (`const result = useState()`) and one whose names do not follow
   `[thing, setThing]` (`[color, updateColor]`). Returning the `useState()` call directly is accepted.
2. **`allowDestructuredState` skips the check on the value name** when the value is destructured further, as in
   `[{ foo, bar }, setFooBar]`.
3. **Own guidance:** the symmetric name is what lets a reader find every writer of a piece of state with one
   search; keep the rule on, and set the option only for destructured objects.

## 2.5 Verify
Search the project for components declared inside functions that render them, for function props rendered as
`<Prop />`, and for `useState` results not destructured as a pair; for each hit, move the component out,
call the prop, or rename.
