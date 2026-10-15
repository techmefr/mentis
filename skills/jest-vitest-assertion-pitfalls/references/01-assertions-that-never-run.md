# jest-vitest-assertion-pitfalls §1 — Assertions that never run

Jest and Vitest consider a test failed when something throws. Everything that stops the throw from happening,
or from being awaited, leaves the test green. The rule pages cited here are those of `eslint-plugin-jest` and
`eslint-plugin-vitest`.

## 1.1 Async assertions must be awaited or returned
1. **`expect(promise).resolves...` without `await` or `return` is flagged** by the Jest rule, which also flags an
   `expect` that is never followed by a matcher, a matcher that is named but not called (`expect(true).toBeDefined;`),
   and `expect()` with no argument (`valid-expect`, eslint-plugin-jest). Its `alwaysAwait` option requires `await`
   over `return` inside blocks. The Vitest rule of the same name checks the argument count and, only with its
   `alwaysAwait` option (off by default), the `await` (`valid-expect`, eslint-plugin-vitest).
2. **A promise chain that holds an `expect` is covered too**: a `.then` callback whose promise is not awaited or
   returned is flagged, including one of several promises where only some are collected
   (`valid-expect-in-promise`, both plugins). `Promise.all` and `Promise.allSettled` count as handled when
   they are awaited or returned.
3. **Vitest `expect.poll` and `expect.element` return promises that need the same handling**
   (`require-awaited-expect-poll`, eslint-plugin-vitest). The Playwright equivalent is in
   `playwright-e2e-pitfalls` §1.5.
4. **With type information, a promise passed to `expect` without `resolves` or `rejects` is flagged, and so is the
   opposite**: `resolves` on a value that is not a promise (`valid-expect-with-promise`, eslint-plugin-jest; it
   needs typed linting).
5. **Verify** by deleting one `await` on purpose and checking that the lint step flags it.

```js
test('rejects an unknown id', async () => {
  await expect(findOrder('missing')).rejects.toThrow('order not found');
});
```

## 1.2 An `expect` that can be skipped
1. **Jest only considers a test failed if it throws**, so an `expect` in an `if`, after `&&`, in a `catch` block or
   in a callback of a function named `catch` can be skipped while the test passes
   (`no-conditional-expect`, eslint-plugin-jest; the Playwright plugin has the same rule).
2. **The classic shape is `try` around the call and the `expect` in `catch`**: if the call does not throw, nothing
   is asserted. Goldberg's guide (section 1.10) describes the same shape and its result: a test report that only
   says a value was null, not that an exception was missing.
3. **To assert on the properties of a thrown error**, wrap the call in a helper that returns the error and throws
   a distinct "no error was thrown" error, then assert that the result is not that error and check the property
   (`no-conditional-expect` page). `expect.assertions` and `expect.hasAssertions` can force a count, but combined
   with conditionals they add complexity.
4. **Conditional logic inside a test is a sign it covers too much**: give each branch its own test
   (`no-conditional-in-test`, eslint-plugin-jest). Conditional logic in a helper or a hook is not reported.
5. **A test that is itself defined inside an `if`** is a different finding (`no-conditional-tests`,
   eslint-plugin-vitest).

## 1.3 No assertion, or an assertion outside a test
1. **A test with no `expect` call proves nothing** (`expect-expect`, both plugins). A project's own assertion
   helpers are declared to the rule by name or wildcard, so calling `assertTotal(...)` counts and a bare helper
   that asserts nothing does not.
2. **Vitest type tests that only contain `expectTypeOf` need the plugin's typecheck setting**, or the rule reports
   them as having no assertion (`expect-expect`, eslint-plugin-vitest).
3. **An `expect` inside `describe` but outside a test, or outside any `describe`, never runs**
   (`no-standalone-expect`, eslint-plugin-jest). An `expect` in a helper that a test calls is fine; a helper that
   nothing calls is not reported by this rule, so rely on an unused-variable check.
4. **`expect.hasAssertions()` in a `beforeEach` is accepted**, because it runs as part of each test
   (`no-standalone-expect`).

## 1.4 The `done` callback
1. **`done` makes every assertion's failure depend on careful wiring.** Without a `try`/`catch` the test times out
   instead of failing, and with one, forgetting to pass the caught error to `done` makes the runner believe the
   test passed (`no-done-callback`, eslint-plugin-jest).
2. **Use `async`/`await`, or return the promise**: when a test or hook returns a promise, Jest waits for it and
   fails on rejection (`no-done-callback`).

## 1.5 Thrown errors
1. **`toThrow()` with no message passes for any thrown error**, so state the message, or an error type
   (`require-to-throw-message`, eslint-plugin-jest). Goldberg's guide (section 1.10) adds that the error should carry
   a property that tells its type, otherwise the application cannot do more than show a generic message.
2. **`toEqual` and `toStrictEqual` on an error compare only its `message`**, so two errors of different types pass
   (`no-error-equal`, eslint-plugin-jest; needs typed linting). `toThrow` checks the type along with the message.
3. **Do not catch errors to assert them; expect them**: the one-line `toThrow` or `rejects.toThrow` form is
   shorter, clearer and fails when nothing is thrown (Goldberg's guide, section 1.10).
