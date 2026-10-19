# svelte-conventions §2 — Components, templates, shared state and styling

> Section 2 of `skills/svelte-conventions`. Read it when markup, snippets, each blocks, raw HTML, context, a
> shared module or CSS is written. The other sections and the guardrails stay in `SKILL.md`.

1. **Reuse markup with snippets, not slots.** `{#snippet name(args)}` declares and `{@render name(args)}`
   instantiates; a snippet can be passed as a prop (`children` is the implicit one). A top-level snippet that
   touches no component state can be exported from a `<script module>` for other components.
2. **Key every `{#each}` that can reorder or change.** The key must uniquely identify the item, and the index is
   not a key. Keyed blocks let the framework insert and remove surgically instead of rewriting the DOM of
   existing rows. Do not destructure the item in the head when the body mutates it (`bind:value={item.count}`).
3. **`{@html}` is a raw sink.** Escape the string or populate it only with values you control; never render
   unsanitised content. Content injected this way does not receive scoped styles, so style it with `:global`
   under a scoped wrapper element.
4. **Dynamic components are plain.** Use the component variable directly (`<DynamicComponent />`) and the
   component's own file for recursion (`import Self from './ThisComponent.svelte'`).
5. **Pass a script value to CSS with a custom property.** Set it with the `style:` directive
   (`style:--columns={columns}`) and read `var(--columns)` in the component's `<style>`.
6. **Style a child through custom properties.** Scoped CSS stops at the component boundary; a parent
   controls a child by setting custom properties that the child's styles read. Use `:global` to reach into a
   third-party child only when it offers no such hook.
7. **Use `class` with clsx-style arrays and objects**, not many `class:` directives.
8. **Prefer context to a shared module for state that belongs to part of the app.** Context scopes the state to
   the component subtree and, on the server, cannot leak between requests; a module-level `$state` is one
   instance for every user of a long-lived server process. Use `createContext` (5.40+) for a typed
   getter/setter pair; below that version use `setContext` / `getContext` with a key. To keep reactivity,
   store an object you update or pass getters, never a value you reassign (reassigning breaks the link, and the
   framework warns).
9. **Module state is acceptable when there is no server rendering** and never will be. Say so where the module
   is declared in the review; "never will be" is a decision, not a default.
10. **Use `$props.id()` for generated ids**, not a random value, so server and client agree.
11. **Async in components (await expressions, `hydratable`) is experimental** and needs an opt-in option at the
    pinned version. Do not use it in a project that has not turned it on deliberately.
12. **Accessibility lives in the template**: the compiler warns for many mistakes, so treat accessibility
    warnings as errors in CI, and follow `skills/accessibility` for what it cannot see.

## Mechanical checks

```
grep -rnE "\{#each [^}]*\}" src --include=*.svelte | grep -v "("
grep -rnE "\{@html" src --include=*.svelte
grep -rnE "export (const|let) [a-zA-Z_]+ *= *\\\$state" src --include=*.svelte.ts --include=*.svelte.js
grep -rnE "class:[a-z-]+=" src --include=*.svelte
grep -rnE "setContext\(|getContext\(" src
```

- An unkeyed each is read for whether the list can reorder; a static list is fine.
- Every `{@html` hit gets the question "who controls this string".
- A module-level exported `$state` in an app that renders on the server is a finding (rule 8).
