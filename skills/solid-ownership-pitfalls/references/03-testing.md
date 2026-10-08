# solid-ownership-pitfalls §3 — Testing Solid code

Solid tests fail by passing: a component rendered outside its reactive scope shows its first output and never
updates, and the assertion still holds. These rules keep the test inside the scope the code runs in. They
assume the Solid testing library and a browser-like test environment.

## 3.1 Rendering
1. **Pass `render` a function.** `render(() => <Counter />)`. The testing library requires a function; passing
   JSX directly runs the component in the caller's scope, outside the library's root, so the output is static
   and a test that clicks and then checks the old value can pass while reactivity is broken.
2. **Assert after the interaction, on a value that must change.** A test that checks only the initial render
   cannot see the missing reactive scope.

## 3.2 Primitives
1. **Test signals, effects and memos inside an owner.** Top-level test code has none, so `createEffect` never
   runs and a memo is never disposed. Wrap the test in `createRoot` (calling `dispose` at the end) or use
   `renderHook`, which simulates a component without rendering anything.
2. **For asynchronous effects** the testing library provides `testEffect`.

## 3.3 Async behaviour
1. **Use `findBy` queries for anything that resolves later:** a resource, a lazy component, a router
   transition. `getBy` immediately after the trigger fails because the DOM has not updated.
2. **Fake timers need the user-event delay hook.** With `vi.useFakeTimers()`, create the user-event instance
   with an `advanceTimers` option wired to the timer library, or typing waits on internal delays that never
   elapse and the test hangs.
3. **Query portal content through `screen`,** not through the container returned by `render`: a portal renders
   outside the container.

## 3.4 Isolation
1. **Keep logic tests separate from UI tests.** Test a primitive or store directly, and test the component for
   what the user sees.
2. **In a real-browser test mode, clear storage between tests.** IndexedDB and `localStorage` persist across
   tests in one session, and leaked state shows up as an order-dependent failure. An IndexedDB database cannot
   be deleted while a connection to it is open, so close the connection first or the delete blocks silently.
3. **Prefer accessible queries** (role, label) to test ids: they fail when the markup stops being accessible.
   Wider testing guidance is in `testing-anti-patterns`.

## Verification
- Change the code under test so the behaviour is wrong and confirm the test fails (§3).
- Run the test file alone and in the full suite, in two orders (§3).
