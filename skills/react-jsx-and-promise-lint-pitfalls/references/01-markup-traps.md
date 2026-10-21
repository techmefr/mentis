# react-jsx-and-promise-lint-pitfalls §1 — Markup traps

> Part 1 of `skills/react-jsx-and-promise-lint-pitfalls`. Read it when JSX markup is written or a markup rule
> fires. Sourced from the rule pages `button-has-type`, `no-children-prop`, `jsx-no-useless-fragment` and
> `checked-requires-onchange-or-readonly` of eslint-plugin-react (commit `bd381cd`), read 2026-10-16. The
> rule names are the plugin's, written here without the plugin prefix. Sentences marked "own guidance" are
> ours.

## 1.1 A button has a type
1. **The default type of an HTML `button` is `submit`.** Inside a form, a button with no `type` submits the
   form, which the rule page says is often not the desired behaviour and may lead to unexpected page reloads.
   `button-has-type` requires an explicit `type` and checks the value is one of `button`, `submit` or `reset`.
2. **Write `type="button"` for anything that is not a submit control**, such as a toggle, a menu trigger or a
   dialog close button inside a form. `type={condition ? "button" : "submit"}` is accepted; a value taken from a
   variable is not, because the rule cannot know it is valid.
3. **The rule works for `React.createElement` too**, and other elements may carry a `type` attribute freely
   (`span type="foo"` is not reported).
4. **Options can forbid a value.** Passing `false` for `reset` rejects every reset button, for instance. Own
   guidance: forbid `reset` in an application where the reset button has no place in the design, since it
   clears a form without confirmation.
5. **Turn it off only where every button is a submit.** The page's own opt-out wording.
6. **Verify** by clicking a typeless button inside a form in a browser and watching the request or the reload.

## 1.2 Children are nested, not passed as a prop
1. **`children` belongs between the tags.** The rule page says children should always be actual children:
   nested in JSX, or the extra arguments of `React.createElement`. `<MyComponent children={...} />` and
   `{ children: ... }` in a props object are reported.
2. **A function passed as children is the one exception, behind an option.** With `allowFunctions` on, a
   function must be in prop position and not in child position (`<List children={(item) => ...} />`); with the
   default, a function child between the tags is the form that is accepted. Own guidance: pick one form per
   project for render functions, and write it in the lint configuration, because the option reverses which of
   the two is reported.

## 1.3 Fragments that wrap nothing
1. **A fragment is redundant** when it contains one child, or when it is the child of an HTML element, and it
   is not a keyed fragment. `<>{foo}</>`, `<p><>foo</></p>` and an empty `<></>` are reported, as is a ternary
   whose branches are each wrapped in a fragment.
2. **A keyed fragment is not redundant.** `<Fragment key={item.id}>` in a list is the way to give a key to a
   group of siblings, and a fragment with several children is needed.
3. **`allowExpressions` accepts a single expression in a fragment.** It exists because a component whose return
   type is `JSX.Element` cannot return a bare string in TypeScript, and wrapping it is the common workaround.
4. **The rule is autofixable.** Own guidance: remove a redundant fragment in the same change that touches the
   line, and read the diff the fixer produces before committing it.

## 1.4 Controlled and uncontrolled checkboxes and radios
1. **`checked` needs `onChange` or `readOnly`.** The rule page requires one of them for an input with `checked`;
   `checked` with both `onChange` and `readOnly` is also accepted. An input with `checked` and neither is a
   box the user cannot change.
2. **`checked` and `defaultChecked` together are reported.** One makes the input controlled and the other
   uncontrolled; the rule page warns about their combination, and `defaultChecked` alone is correct for an
   uncontrolled input.
3. **Options relax the rule:** `ignoreMissingProperties` and `ignoreExclusiveCheckedAttribute`. The page does
   not describe them in the part read, so own guidance: leave them off and fix the markup.
4. **Verify** by clicking the box in a browser: a controlled input with no handler stays at the
   value of its `checked` prop. The React reference for `input` (CC BY 4.0, read 2026-10-20) says the same: a
   `value` without `onChange` makes typing impossible because the input is forced to the passed value, and
   checkboxes take `checked` or `defaultChecked`.

## 1.5 Rules that this block leaves to the main block
Keys built from an array index, `&&` with a number or a string on the left, and state set inside effects are
in `skills/react-nextjs-conventions`. The rule pages for `no-array-index-key` and `jsx-no-leaked-render` were
read for this block and add nothing that block does not already say, so they are not repeated.
