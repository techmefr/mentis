# vue-test-utils-pitfalls §3 — Stubs, teleport, transitions, server rendering, router and time

> Part 3 of `skills/vue-test-utils-pitfalls`. Read it when a child, a directive, a portal, a transition, the
> router or the clock is replaced in a test. Sourced from the Vue Test Utils guide pages on stubs and shallow
> mounting, teleport, transitions, server-side rendering, Vue Router and the FAQ (commit `f472a50`), read
> 2026-10-16. Sentences marked "own guidance" are ours.

## 3.1 Stubs and `shallow`
1. **`global.stubs` replaces a component everywhere in the render tree**, at any depth, with a dummy. `true`
   gives the default stub (rendered as `<name-stub>`); a component definition with a `template` gives your own
   markup. The key can be the registered key or the component's name, and the key wins when both are given.
2. **`shallow: true` stubs every child component.** It is the same as the older `shallowMount`. To keep one
   child real, list it with `false`: `stubs: { Child: false }`.
3. **The more you stub, the less production-like the test.** The page's rule of thumb is that tests resembling
   real use give more confidence; with one or two irrelevant children, prefer `mount` with a few `stubs` over
   `shallow`, and keep asserting on inputs and outputs (part 1.5).
4. **A stub does not render its slots.** Under `shallow` a stubbed `CustomButton` renders no slot content, so a
   test of the text a parent puts in the slot cannot pass. `config.global.renderStubDefaultSlot = true`
   renders the default slot of stubs, and only the default slot.
5. **That setting is global.** Set it in `beforeAll` and reset it in `afterAll`, or in a shared setup file on
   purpose; leaving it on silently changes later tests.
6. **A stubbed child cannot be asserted on.** Own guidance: when a test needs a child's text or events, leave
   that child real and stub the others.
7. **Prop names that clash with DOM `Element` properties** (the FAQ names `attributes`, `children` and
   `prefix`) produce a "failed setting prop" warning on stubs. The page's options: use `mount` instead of
   `shallowMount`, silence the warning, or rename the prop.

## 3.2 Stubbing an async component
1. **By the registered key**, the component is stubbed before it resolves and the test needs no `await`.
2. **By the component's own name**, the real component must resolve first, so `await flushPromises()` before
   asserting; and the component must define a `name`.

## 3.3 Stubbing a directive
1. **Stub with a name in the `vFoo` form.** `stubs: { vTooltip: true }` skips the directive's code, useful
   when it measures nodes and jsdom cannot. A stub object with hooks (for example `beforeMount`) replaces it
   with a minimal implementation when the code depends on a side effect such as a class it adds.
2. **This does not work for functional components or `<script setup>`**, because the directive name is not
   known to `withDirectives` there. The page says to mock the directive module through the test framework
   instead.

## 3.4 Teleport
1. **Create the target element before mounting**, for example a `div` with the id the component teleports to,
   appended to `document.body`; otherwise Vue warns that the target was not found. Remove it after each test
   (the page clears `document.body`), because some runners do not reset the DOM.
2. **`wrapper.find` cannot see teleported markup.** The wrapper's own HTML shows only the teleport comments.
3. **Use `findComponent` or `getComponent`**, which work on the virtual DOM, then `get`, `setValue` and
   `trigger` on the returned wrapper, and read its `emitted()`.
4. **To ignore teleport, stub it:** `global: { stubs: { teleport: true } }`.

## 3.5 Transitions
1. **VTU stubs `transition` and `transition-group` by default**, so after an action the element is there or
   gone and can be asserted without waiting for animation.
2. **The stub is simple.** JavaScript hooks are not supported and may produce Vue warnings. The page's
   options: turn off the automatic stubbing through global stubs, write your own stub that handles the hooks,
   or spy on the warning. With the stub off, JavaScript hooks may also need `requestAnimationFrame` mocked
   to run its callback straight away.

## 3.6 Server rendering and the router
1. **`renderToString` renders a component to a string** with the same arguments as `mount`; it is async. Use
   it to test what `onServerPrefetch` produced; the page's test awaits the string and compares the whole
   markup.
2. **VTU has no special router helpers.** Pick one of two approaches. A **mocked router** keeps the test on
   your logic: pass `$route` and `$router` through `global.mocks` for the Options API, or mock the `vue-router`
   module for `useRoute` and `useRouter`, and assert that `push` was called with the expected location.
3. **A real router** is a plugin: add it with `global.plugins`. Mounting without it warns that `router-link`
   and `router-view` cannot be resolved. The router starts asynchronously, so `router.push('/')` then
   `await router.isReady()` before mounting, and `await flushPromises()` after a click that navigates.
4. **Build a new router in every test**, from the exported route list, so state does not leak between
   tests. The page does it in `beforeEach`.
5. **The page's own verdict:** the real router takes a lot of setup, which is why mocking is common in unit
   tests; end-to-end tests in a browser are the place to prove real navigation. Router behaviour itself is in
   `skills/vue-router-pitfalls`.

## 3.7 Fake system time
1. **Mount after `vi.setSystemTime`.** The FAQ says Vue's scheduler depends on the system time, and mounting
   before the call may break reactivity. Own guidance: call it in `beforeEach`, mount inside the test, and
   restore real timers in `afterEach`.

## 3.8 Verify
Print the wrapper's HTML for one stubbed test and see the stub tags; for a teleport, check that `find` fails
and `getComponent` succeeds; for the router, run the test file twice in a different order.
