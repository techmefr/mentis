# angular-conventions §6 — Tests

> Section 6 of `skills/angular-conventions`. Read it when any Angular test is written or reviewed. The test
> doctrine itself is `skills/tdd` and `skills/testing-anti-patterns`; the layer to defect map is
> `skills/frontend-testing`. This section is only what is specific to the framework.

1. **A unit test sits next to the code it tests and ends in `.spec.ts`** (§1.2, §1.6).
2. **A new project's runner is Vitest, in a Node environment with `jsdom`** (`ng test` builds in watch mode and
   runs it); a project migrating from Karma follows the framework's migration guide and keeps one runner during
   the move. Switch to a real browser through the browser provider option only for a test that needs layout,
   focus or scroll; the default is faster. On CI, `ng test` detects `CI=true` and runs once without watch;
   force it with the no-watch flag when the variable is missing.
3. **Test in a zoneless environment: act, wait, assert.** Change state or perform the action, `await
   fixture.whenStable()`, then assert. Do not call `fixture.detectChanges()` to push the view: it forces a
   check Angular would not have scheduled, so a component that forgets to notify passes the test and fails in
   production. Keep waiting rare: use a controllable clock where the project provides one, and a real `async`
   test with an explicit timeout only when time is the behaviour.
4. **An existing suite built on `detectChanges()` is not worth converting wholesale.** The test bed still
   enforces `OnPush` compatibility and throws `ExpressionChangedAfterItHasBeenCheckedError` for an update made
   without a notification. Fix such an error in the component (a signal, or `markForCheck`), not in the test; a
   test-only wrapper component may call `markForCheck` on its own change detector reference.
5. **The test bed rethrows application errors by default.** Keep it that way. Disable it
   (`rethrowApplicationErrors: false`) only in a test whose purpose is that the application survives an error,
   and say so in the test name.
6. **Create the component through the test bed and mock the providers, not the unit under test.** Global test
   providers (the HTTP testing provider, for example) go in a shared providers file that is listed in the test
   TypeScript configuration, so the test build can see it.
7. **Interact through component harnesses for shared widgets.** A harness exposes what a user does and hides the
   DOM structure and CSS classes, so a markup refactor does not break every test, and the same harness serves
   unit and end-to-end tests. For an application-specific page, test through the template's visible text and
   the project's `data-test-*` attributes (`skills/tdd`).
8. **HTTP is tested against the testing backend, not a hand-made fake of the client.** Provide the client with
   its features (interceptors) first and the testing provider after it, because the testing provider overwrites
   parts of the first. Trigger the call, `expectOne` the request (it fails on more than one match; use `match`
   for duplicates and `expectNone` for "must not happen"), assert on method, full URL with query, headers and
   body, flush a response or an error, and verify in `afterEach` that no request is left outstanding. Test the
   failure paths as well as the success. An interceptor is tested through the client, since its order and its
   use of `clone` are the behaviour.
9. **A deferred block is tested through the test bed's defer APIs**, which can hold the block in each state
   (placeholder, loading, error, complete); by default it plays through like a real one.
10. **Test a guard by its navigation outcome**: mock the services it depends on, navigate through the router
    testing harness, and assert where the user ended up (the redirect), not that a function returned a value.
    Test a routed component the same way, so route parameters come from a real navigation.

## Mechanical checks

```
grep -rnE "detectChanges\(\)" src --include=*.spec.ts
grep -rnE "rethrowApplicationErrors" src
grep -rnE "provideHttpClientTesting|HttpTestingController" src
grep -rnE "verify\(\)" src --include=*.spec.ts
grep -rnE "setTimeout|waitForAsync|fakeAsync" src --include=*.spec.ts
```

- A `HttpTestingController` import without a matching `verify()` is rule 8.
- `detectChanges` hits are counted, not condemned: rule 4 allows them in a legacy suite and forbids new ones.
