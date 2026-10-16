---
name: react-jsx-and-promise-lint-pitfalls
description: "Use when React code is written, reviewed or linted for the mistakes a rule can catch mechanically: a button without a type inside a form, children passed as a prop, fragments that wrap nothing, a controlled checkbox with no change handler or with both checked and defaultChecked, components defined inside components (state lost on every render, render props, memoized copies), the value and setter naming of useState, and promises that nobody handles (floating statements, async functions passed to void-returning handlers and JSX attributes, async callbacks in forEach and map)."
---

# react-jsx-and-promise-lint-pitfalls

A defensive block for the small React mistakes that look correct in review and that a lint rule finds in a
second. The three parts share one premise: **these are not style points; each one changes behaviour** (a form
submits and the page reloads, a child component loses its state on every parent render, a rejected promise
vanishes) **and the rule that detects it is only useful if the team knows what the failure is when it
turns the rule off**. Hook ordering, state and effects, keys, leaked `&&` renders and the rest of the React
conventions are in `skills/react-nextjs-conventions`; query and event traps in tests are in
`skills/testing-library-query-pitfalls`; accessibility of the markup is in `skills/accessibility`.

## When
- A button, an input, a fragment or a `children` prop is written or reviewed in a component.
- A component is declared inside another component, or a function that returns JSX is passed as a prop.
- An `async` function is passed as an event handler, a callback to `forEach` or `map`, or a value that is
  expected to return nothing.
- A lint rule from the React or typescript-eslint plugins is switched off, downgraded to a warning, or added
  to a project.

## Steps

**Read only the part the diff touches.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Button type, children prop, useless fragments, controlled and uncontrolled checkboxes | JSX markup is written or a markup rule fires | [`01-markup-traps.md`](./references/01-markup-traps.md) |
| 2 | Components inside components, render props, memoized copies, state and setter naming | a component or a render function is defined inside another, or state is declared | [`02-component-identity-and-state-naming.md`](./references/02-component-identity-and-state-naming.md) |
| 3 | Floating and misused promises at the JSX boundary, async callbacks, enabling the typed rules | an async function reaches a handler or an array method, or a promise is dropped | [`03-promises-at-the-jsx-boundary.md`](./references/03-promises-at-the-jsx-boundary.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a form with an untyped button was submitted from that button
(part 1.1), a child defined inside its parent lost its input text when the parent re-rendered and kept it once
moved out (part 2.1), a rejected promise inside an `async` click handler was made visible in the console and
then handled (part 3.2), and the typed lint rules ran on the project with the parser option that gives them
type information (part 3.5). A rule that was only read about, or turned on without type information, is not
verified.

## Guardrails
- Never leave a `button` inside a form without an explicit `type` (part 1.1).
- Never pass children through a `children` prop when they can be nested between the tags (part 1.2).
- Never give a controlled `checked` input without `onChange` or `readOnly`, and never `checked` together with
  `defaultChecked` (part 1.4).
- Never define a component inside another component's body (part 2.1).
- Never pass an `async` function to a callback that expects nothing back without a handler for its rejection
  (part 3.2, part 3.3).
- Never mark a promise with `void` and call it handled; the rejection is still unhandled (part 3.1).
- Never use the typed promise rules without type information configured (part 3.5).
- This block states the rule documentation of the two plugins as of the commits read on the date in
  [`references/origin.md`](./references/origin.md); the plugin versions the pages describe were not checked,
  and nothing was run while writing the block.

## Origin
Rewritten from the rule documentation of eslint-plugin-react (MIT) and typescript-eslint (MIT), read
2026-10-16. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
