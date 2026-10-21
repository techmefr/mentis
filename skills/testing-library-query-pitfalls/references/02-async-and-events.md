# testing-library-query-pitfalls §2 — Async and events

Waiting and acting are where a component test turns flaky: the callback of `waitFor` runs an unpredictable
number of times, an event method returns a promise that nobody awaits, and a warning gets silenced instead of
read.

## 2.1 What goes inside `waitFor`
1. **`waitFor` is for things with a non-deterministic delay between your action and the assertion passing.** Its
   callback is called, or checked for errors, an unpredictable number of times at an unpredictable rate
   (`no-wait-for-side-effects`, eslint-plugin-testing-library).
2. **Never put a side effect in it**: `fireEvent`, `userEvent` or `render` inside the callback runs again on every
   attempt and repeats the action (`no-wait-for-side-effects`). Act first, then wait for the result.
3. **One `waitFor` per asynchronous target.** Several assertions on the same async target inside one callback
   can delay the failure until the timeout, which is slow; assertions on different async targets, such as two
   independent state updates, are fine in one callback (`no-wait-for-multiple-assertions`).
4. **Never take a snapshot inside `waitFor` or another async utility.** The callback loops, so a snapshot is
   generated per loop, the number of loops differs between a laptop and CI, and a local `jest -u` writes snapshots
   that fail in CI (`no-wait-for-snapshot`).
5. **Prefer `findBy*` when the wait is for one element** (§1.3).
6. **Know what the callback must do.** It is retried only when it throws, so a callback that returns a false value
   passes at once; put the assertion inside it (Testing Library, async methods page). The documented defaults are a
   1000 ms timeout and a 50 ms interval, with the first run immediate and a rerun on DOM changes in the container;
   a callback that returns a promise is not called again until that promise rejects.
7. **Verify** by running the test many times in a row, and by checking that no action sits inside a waiting
   helper.

## 2.2 user-event v14: set up, then await
1. **From v14 the library recommends calling `userEvent.setup()` before rendering and using the returned instance
   for every interaction**, so the event system is initialised and events fire in the right order
   (`prefer-user-event-setup`). The user-event introduction says the same and discourages rendering or using
   `userEvent` in a before or after hook; its direct API on the default export calls `setup` internally and exists to
   ease the move to v14. A helper that returns the instance together with the render result keeps this to
   one line per test. The rule cannot follow a `setup()` call made in another file, so a project that wraps it in
   shared test utilities disables the rule rather than suppressing it per test (`prefer-user-event-setup`).
2. **Every v14 event method returns a promise; `await` it** (`await-async-events`). Without the await the test
   moves on before the interaction happened.
3. **Before v14 the methods were synchronous**, except `type` and `keyboard` when a `delay` option is given;
   awaiting a synchronous method is flagged (`no-await-sync-events`). The two rules cover opposite versions: check
   the installed user-event version before enabling either, and enable only the one that matches.
4. **Prefer `userEvent` to `fireEvent`.** `userEvent` adds the related browser events around an action and is
   more realistic, while `fireEvent` is the low-level API (`prefer-user-event`). Events that `userEvent` does not
   cover, such as `cut`, still use `fireEvent`.
5. **`fireEvent` is asynchronous only in a few flavours**: the Vue and Marko packages are supported by the
   plugin's async-event rule, and the page notes Svelte as async too but not yet supported by the plugin
   (`await-async-events`). In the other flavours it is synchronous; do not await it.
6. **Keep the test's promise handling visible**: an event or query promise is handled when awaited, passed to
   `Promise.all` or `Promise.allSettled`, chained with `then`, or returned (`await-async-events`,
   `await-async-queries`).

## 2.3 `act` is not a mute button
1. **Every Testing Library utility is already wrapped in `act`.** An "not wrapped in act" warning is usually the
   test telling you something unexpected happens, so wrapping the call to silence it hides the finding
   (`no-unnecessary-act`).
2. **An empty `act` callback is also wrong**, and so is wrapping `render`, `waitFor` or events in it
   (`no-unnecessary-act`).
3. **`act` stays correct around code that does not use Testing Library**, such as a direct state update from
   your own module. The rule's `isStrict` option, on by default, also reports an `act` that
   mixes both kinds of calls (`no-unnecessary-act`).
4. **`act` exists only in some flavours**: the React and Marko packages are supported by the plugin
   (`no-unnecessary-act`).
5. **Read the warning first**: find which update happens after the test finished or outside a wait, and make the
   test wait for it with a query or `waitFor`. The React Testing Library FAQ says the warning is usually an async
   operation updating after the test ended, prefers waiting for the result with an async utility, and offers mocking
   the operation as the other way.

## 2.4 Cleanup and where `render` goes
1. **Cleanup runs automatically when the runner exposes the `afterEach` global**, as Mocha, Jest and Jasmine do.
   Do not import or call `cleanup` yourself, unless auto-cleanup was switched off with an environment variable
   such as `RTL_SKIP_AUTO_CLEANUP` (`no-manual-cleanup`). The React setup page names the same condition. Vitest does
   not expose those globals by default, so there the automatic cleanup needs `globals: true` or a top-level
   `afterEach` that calls `cleanup` (same page); symptom of a missing one: "Found multiple elements" in a later test.
2. **Do not call `render` in `beforeEach` or `beforeAll`.** Moving it next to the assertions reduces variable
   mutation and nesting, which makes the tests easier to maintain; render in each test or in a `setup()` function
   that each test calls (`no-render-in-lifecycle`).
3. **The exception**: when auto-cleanup is skipped, the plugin's `allowTestingFrameworkSetupHook` option permits
   `render` in one named hook (`no-render-in-lifecycle`).
