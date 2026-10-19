# jest-vitest-assertion-pitfalls §2 — Focus, skip, titles and test files

A focused test, a skipped test and a duplicated title each make a green run mean less than it seems. A test
file that is imported runs its tests again.

## 2.1 Focused tests
1. **`.only` runs one test and skips the rest.** Jest's `describe.only`, `it.only`, `test.only`, `fdescribe` and
   `fit` all do it; the feature helps while debugging, and `.only` has to come out before the change is committed
   so that every test runs on the build system (`no-focused-tests`, eslint-plugin-jest). Vitest has the same rule
   for `it.only` and `test.only` (`no-focused-tests`, eslint-plugin-vitest).
2. **Edge cases a lint rule cannot see**: an alias such as `const run = describe.only` is not detected
   (`no-focused-tests`, eslint-plugin-jest). A runner-level switch that fails the run when a focused test exists
   is the second layer; Playwright has one (`playwright-e2e-pitfalls` §3.1). Whether Jest and Vitest have an
   equivalent was not read, so check the pinned version before relying on one.
3. **Verify** by committing a `.only` on a scratch branch and confirming that the lint step fails.

## 2.2 Disabled tests
1. **A test is disabled by more than `.skip`**: an `x` prefix (`xit`, `xtest`, `xdescribe`), a title with no
   function body, or a call to `pending()` inside the test (`no-disabled-tests`, eslint-plugin-jest). Vitest
   flags `test.skip` (`no-disabled-tests`, eslint-plugin-vitest).
2. **Disabling is useful while debugging or for a placeholder, and the plugin warns so that all tests are
   running again before the change is committed** (`no-disabled-tests`, eslint-plugin-jest).
3. **Own guidance:** every `.skip` keeps a reason, an owner and a date in the title or the line above, in the form
   the quarantine lifecycle uses (`flaky-test-triage-pitfalls` §3). This repository has no tracker, so a ticket
   reference is not the mechanism.
4. **Not caught by the rule**: a skip hidden behind a variable (`const testSkip = test.skip`) or a renamed `test`
   (`no-disabled-tests`, eslint-plugin-jest).

## 2.3 Titles and structure
1. **Two tests, or two suites, with the same title at the same level make a failure ambiguous**: you cannot tell
   which one failed. A title that repeats a parent's or a sibling suite's is fine
   (`no-identical-title`, eslint-plugin-jest).

## 2.4 Test files and mock files
1. **Do not export from a file that contains tests.** Importing it runs all its tests again in each importing
   file; move shared helpers to a separate non-test file (`no-export`, eslint-plugin-jest).
2. **Do not import from `__mocks__` by hand.** After `jest.mock('./x')`, the code and the test both import
   `./x`; a test that imports `./__mocks__/x` gets a second instance of the mocked module that is not
   referentially equal to the first (`no-mocks-import`, eslint-plugin-jest; eslint-plugin-vitest has the same
   rule).
3. **Vitest: do not import from `node:test`.** The plugin says it is usually imported by accident; its fix
   replaces the import with `vitest` (`no-import-node-test`, eslint-plugin-vitest). Own inference: the `test`
   function then comes from Node's runner, not from Vitest.
