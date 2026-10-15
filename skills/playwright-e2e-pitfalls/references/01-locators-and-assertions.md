# playwright-e2e-pitfalls §1 — Locators and assertions

Most Playwright tests that pass while the application is broken, or break when the markup changes, fail at
one of five points: how the element is found, how the result is read, how long the test waits, whether the
call is awaited, and whether a failure can be swallowed.

## 1.1 Find elements the way a user would
1. **Prefer user-facing attributes and explicit contracts** over selectors built from CSS classes or DOM
   structure, which break when a designer renames a class (Playwright best practices). TestDino gives an order:
   role with its accessible name, label, placeholder, visible text, test id, and CSS or XPath last.
2. **Codegen picks in the same order**: Playwright's test generator prioritises role, text and test id
   locators and tightens a locator that matches several elements (Playwright best practices).
3. **A lint rule can ban every raw `locator()` call** (`no-raw-locators`, eslint-plugin-playwright); it has an
   allow list for things with no role such as an `iframe`.
4. **Decision: test ids against role and label.** Playwright's guide and the lint rule above lead with role and
   label and treat a test id as a fallback. The project's own doctrine uses `data-test-*` attributes as the
   stable selector (`tdd`, which points at the test-casebook contract). **The project doctrine wins**: use role
   or label where the control has an accessible name, use the `data-test-*` attribute where it has none or its
   text is dynamic, and do not enable `no-raw-locators` as an error where it would fight that doctrine. A
   dedicated test attribute is also what Goldberg's JavaScript testing best-practices guide (section 3.2) recommends when an element has no
   stable attribute such as a label.
   Which attribute name `getByTestId` reads is a configuration point that was not re-read; check the locators
   page of the pinned Playwright version before relying on a name other than the default.

## 1.2 Chain and filter instead of counting
1. **`first()`, `last()` and `nth()` are position, and position changes when the DOM does**
   (`no-nth-methods`, eslint-plugin-playwright).
2. **Narrow with a parent locator and a filter**: a list item filtered by its text, then the button inside it
   (Playwright best practices). The click then follows the row, not its index.
3. **Own guidance:** when the position really is the behaviour under test ("the newest item is first"), say so
   in the test name and keep that one call, rather than banning the method.

## 1.3 Assert with web-first matchers, not with values read once
1. **`await expect(locator).toBeVisible()` retries until the condition holds or the assertion times out**
   (Playwright best practices). The default `expect` timeout is 5 seconds (Playwright configuration page).
2. **`expect(await locator.isVisible()).toBe(true)` reads once and returns at once**: the test does not wait
   a single second, so a message that takes half a second to appear fails it (Playwright best practices).
3. **The same holds for every "resolve once" read**: `isVisible()`, `isEnabled()`, `isChecked()`,
   `textContent()`, `innerHTML()`, `getAttribute()`, `inputValue()`. Use the `expect(locator)` matcher that
   corresponds: `toBeVisible`, `toHaveText`, `toContainText`, `toHaveValue`, `toHaveAttribute` (TestDino;
   `prefer-web-first-assertions`, eslint-plugin-playwright).
4. **Generic matchers (`toBe`, `toEqual`) do not retry** and are for non-UI values (Currents).
5. **`expect.soft` records a failure and lets the test go on**, to list several failures at the end; use it
   for non-critical checks, not as a way to make an assertion optional (Playwright best practices; Currents).

## 1.4 No fixed waits
1. **`page.waitForTimeout`, `page.waitForSelector`, `page.waitForNavigation` and the `networkidle` load state
   are each flagged by their own rule** (eslint-plugin-playwright). The generic reason is in
   `testing-anti-patterns` §3.
2. **Use the signal the application gives**: `expect(locator)` for a visible or changed element,
   `page.waitForURL` or `expect(page).toHaveURL` after a navigation, `page.waitForLoadState`,
   `page.waitForFunction` for an application flag, `locator.waitFor` for a state change (eslint-plugin-playwright;
   TestDino; Currents).
3. **Wait for a response by registering the wait before the action**: create the `waitForResponse` promise,
   click, then await the promise. Registering it after the click can miss a fast response (TestDino shows this
   shape; the "can miss" reason is own reasoning).
4. **Polling has two forms**: `expect.poll(() => ...)` for a value that is read repeatedly, and
   `expect(async () => ...).toPass()` for a block of steps; both take intervals and a timeout (Currents).
5. **An explicit `timeout` is an escape hatch**, and a literal such as `{ timeout: 5000 }` records no reason
   (`no-magic-timeouts`, eslint-plugin-playwright). Put suite-wide values in the config (`timeout`,
   `expect.timeout`, `use.actionTimeout`, `use.navigationTimeout`); where one wait truly needs its own value, name
   the constant after the reason.

## 1.5 Await every call and every async matcher
1. **Every Playwright call is asynchronous**: a missing `await` lets the next line run before the action
   finished, and the symptom is a test that passes unpredictably or reports a detached frame (TestDino).
2. **Two layers catch it**: the `@typescript-eslint/no-floating-promises` rule, and `tsc --noEmit` in CI for
   signatures (Playwright best practices).
3. **`missing-playwright-await` covers what the first rule cannot name**: async matchers, `expect.poll`,
   `test.step` and the `waitFor*` page methods; an option adds `goto`, `click` and locator calls
   (eslint-plugin-playwright). A `waitForResponse` promise that is never awaited does nothing.
4. **Verify by removing one `await` on purpose** and checking that lint or the type check flags it.

## 1.6 A failure that is caught is a test that passes
1. **Playwright fails a test only when something throws.** An `expect` inside a `catch`, behind an `if` or
   after `&&` can be skipped and the test still passes (`no-conditional-expect`, eslint-plugin-playwright).
2. **`try`/`catch` around an `expect` for an "optional" element swallows real failures** (TestDino). The
   alternatives it names: `expect.soft` for non-critical checks, a `.not` assertion to prove absence, or
   `locator.count()` to decide whether to act.
3. **To assert on the properties of a thrown error**, wrap the call in a helper that returns the error and throws
   a distinct "no error was thrown" error, then assert that the result is not that error
   (`no-conditional-expect` page). A test with no `expect` at all is its own finding (`expect-expect`).
4. **`expect(true).toBeDefined` without the call asserts nothing** (`valid-expect`); the same trap is in
   `jest-vitest-assertion-pitfalls` §1.

## 1.7 Force clicks, handles and unused locators
1. **`{ force: true }` is flagged on `click`, `check` and `fill`** (`no-force-option`). Locators wait for the
   element to be visible and enabled before acting (Playwright best practices); forcing skips that wait. The
   following consequence is own guidance: a click that needs `force` usually means something covers the control,
   which is a defect to report, not to click through.
2. **Element handles (`page.$`, `page.$$`) resolve once, can go stale and do not auto-wait**; locators are lazy
   and re-evaluate on every action (`no-element-handle`; TestDino). `page.$eval` has a locator form
   (`locator.evaluate`) (`no-eval`).
3. **A locator that is created and never acted on or asserted does nothing**: `page.getByRole(...)` alone on a
   line is a test step that is missing (`no-unused-locators`).
4. **A variable used inside `page.evaluate` or `addInitScript` is not in scope in the browser**; pass it as an
   argument (`no-unsafe-references`).
5. **Use `evaluate` only where a locator cannot do the job**: reading computed styles, an application hook,
   storage (TestDino).
