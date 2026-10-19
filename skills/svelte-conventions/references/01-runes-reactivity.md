# svelte-conventions §1 — Runes: state, derived, effects, props

> Section 1 of `skills/svelte-conventions`. Read it when any reactive value is declared, derived or
> synchronised, or a prop is read. The other sections and the guardrails stay in `SKILL.md`.

1. **New code is runes mode.** Use `$state`, `$derived`, `$effect`, `$props`; avoid the legacy forms that have a
   replacement: implicit reactivity, `$:` statements, `export let`, `$$props`, `$$restProps`, `on:click`,
   `<slot>`, `<svelte:component>`, `<svelte:self>`, `use:action`, `class:` directives, and stores for sharing
   reactivity (a class with `$state` fields replaces a store).
2. **`$state` only for values that must cause an update.** Anything that no effect, derived or template reads is
   a plain variable.
3. **Deep state is a proxy, and the proxy costs.** `$state({...})` and `$state([...])` are made deeply reactive
   and so are proxied; mutation triggers updates. For a large object that is only ever reassigned, use
   `$state.raw`, which cannot be mutated, only replaced. Class instances are not proxied: put `$state` on the
   class fields. Use the reactive built-ins (`Set`, `Map`, `Date`, `URL`) from `svelte/reactivity`, not the
   plain ones, when their contents drive the view.
4. **Destructuring a reactive value breaks the link.** The extracted variables are the values at that moment,
   as in plain JavaScript. The exception is `$derived` and `$props`, whose destructured variables stay reactive.
5. **Passing state to a function passes its current value.** If the callee must see later values, pass a
   function (a getter) or an object whose property is read at use. Applies to context, closures and module
   exports alike.
6. **A module's `$state` cannot be exported if it is reassigned.** The compiler works one file at a time, so
   another file cannot be told to wrap reads. Either do not reassign it (mutate a property), or export
   accessor functions instead of the variable.
7. **Compute from state with `$derived`, never with an effect that writes state.** `$derived(expr)` takes an
   expression; use `$derived.by(() => …)` for a body. Its expression is side-effect free, and the compiler
   rejects state changes inside it. A derived can be reassigned (since 5.25), which is the way to do optimistic
   UI from a server value. A derived that returns an object or array is not made deeply reactive.
8. **`$effect` is an escape hatch, not a data-flow tool.** It runs only in the browser, after mount, batched in
   a microtask, and reads only what it touches synchronously (reads after an `await` or inside a timer are not
   tracked). Do not update state in an effect: it makes cycles and obscures flow. Alternatives, in order:
   a derived; an event handler or a function binding for a reaction to a user action (two inputs that must stay
   in sync use `oninput` callbacks or function bindings, never two effects); an `{@attach …}` to sync with a
   library such as a chart; `$inspect` for debugging; `createSubscriber` to observe something external.
9. **An effect that starts something returns its teardown.** The returned function runs before every re-run
   and on destroy. Never wrap an effect body in `if (browser)`: effects do not run on the server.
10. **If an effect must write and read the same state, `untrack` the read.** That is the repair for a loop; the
    better repair is rule 7 or 8.
11. **Treat props as changing.** A value that depends on a prop is a `$derived`, not a one-time copy, because a
    component body runs once. Destructure `$props()` with defaults, and use `$props.id()` for ids that link
    labels and controls (stable between server and client).
12. **Never mutate a prop you do not own.** Reassigning a prop is allowed for temporary local state; mutating a
    regular object has no effect, and mutating a state proxy owned elsewhere triggers an ownership warning.
    Communicate upward with callback props, or declare the prop `$bindable` when parent and child intentionally
    share one object. Use `$bindable` sparingly: it makes data flow harder to follow. A bindable prop with a
    fallback requires the parent to pass a defined value when it binds.
13. **Type props.** Annotate the `$props()` destructure; wrapper components take element attributes from
    `svelte/elements`, and snippet props use the `Snippet` type.
14. **Events are attributes.** `onclick={…}`; listeners on `window` or `document` use `<svelte:window>` and
    `<svelte:document>`, not `onMount` or an effect.

## Mechanical checks

```
grep -rnE "export let |\\\$:|\\\$\\\$props|\\\$\\\$restProps|on:[a-z]+=|<slot|<svelte:(component|self)" src --include=*.svelte
grep -rnE "\\\$effect\(" src
grep -rnE "if \((browser|typeof window)" src --include=*.svelte
grep -rnE "from 'svelte/store'" src
```

- Legacy hits are findings in a new file and migration candidates elsewhere (see `SKILL.md` guardrails).
- Every `$effect(` hit is read against rule 8: if it writes state that could be a derived, rewrite it.
- The Svelte compiler and `svelte-check` already flag several of these; run them before reading by hand.
