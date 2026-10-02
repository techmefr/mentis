# svelte-conventions §4 — Tests

> Section 4 of `skills/svelte-conventions`. Read it when a Svelte unit, component or end-to-end test is
> written. Doctrine is `skills/tdd` and `skills/testing-anti-patterns`; the layer map is
> `skills/frontend-testing`. Only what is specific to the framework is here.

1. **The framework picks no runner.** When the project builds with Vite (including SvelteKit), the documented
   choice for unit and component tests is Vitest. A project that already has a runner keeps it.
2. **Runes work in test files whose name contains `.svelte`** (`counter.svelte.test.ts`), because the same
   compiler step processes them. A test of code that creates effects wraps its body in `$effect.root`, since an
   effect needs a parent scope.
3. **Test logic as logic.** Before writing a component test, ask whether the thing under test is the component
   or the logic inside it; if the logic, extract it into a function or a `.svelte.ts` module and test it
   without rendering.
4. **A component test runs in a simulated or real browser DOM.** The simulated one (a DOM emulation library
   through the Vite config) is fast; layout, focus and scroll need a real browser. Calling the mount API by
   hand is brittle, because it is coupled to the component's structure: use a testing library that queries by
   role and text.
5. **Bindings, context and snippet props are tested through a wrapper component** written for that test, and
   the wrapper is what gets mounted. For a component that reads context, the mount API also accepts a context
   map (5.49+); the context applies to that mounted tree only.
6. **Stories can double as component tests.** With Storybook, a story's play function drives interactions with
   the testing library and the runner's assertions in a real browser (`skills/frontend-testing`).
7. **End-to-end tests do not know about Svelte.** They drive the DOM through the browser; the choice of tool
   is the project's (`skills/frontend-testing` for the rules that hold in any of them). Start the application
   on a known port from the runner's configuration.
8. **A form action is tested at both ends**: a unit test of the action function with a constructed request
   (valid, invalid, unauthenticated), and one end-to-end journey with JavaScript on and one with it off, since
   the form is meant to work either way (§3.6).

## Mechanical checks

```
find src -name "*.test.*" -o -name "*.spec.*" | grep -v "\.svelte\." | xargs grep -ln "\\\$state\|\\\$derived"
grep -rnE "\\\$effect" src --include=*.test.ts --include=*.spec.ts | grep -v "effect.root"
grep -rnE "mount\(|render\(" src --include=*.test.ts --include=*.spec.ts
```

- A rune used in a test file without `.svelte` in its name fails to compile; the first command finds the ones
  that will.
