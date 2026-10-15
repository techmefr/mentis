---
name: playwright-e2e-pitfalls
description: "Use when a Playwright end-to-end test or its config is written or reviewed: locators (role and label first, positional methods, the test id decision), web-first assertions versus resolve-once reads, fixed waits, missing await and swallowed failures, force clicks, element handles, test isolation (fresh context, beforeAll, shared data, one account per worker, storageState and its gitignore), mocking only what you do not own, and CI settings (forbidOnly, retries, webServer, trace, browser matrix, lint rules)."
---

# playwright-e2e-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`) for browser tests written with Playwright Test. The three sections share
one premise: **an end-to-end test that passes before its assertion ran, or only on the machine that wrote it,
reports a safety nobody has**. The generic timing rule is in `testing-anti-patterns` §3 and driving a browser by
hand to explore is in `qa-exploratory-testing` §4; neither is repeated. Retries, quarantine and flake triage are
in `flaky-test-triage-pitfalls`; Testing Library queries for component tests are in
`testing-library-query-pitfalls`; assertion traps shared with Jest and Vitest are in
`jest-vitest-assertion-pitfalls`.

## When
- Writing, reviewing or debugging a Playwright test, a fixture, a setup project or `playwright.config`.
- A test passes locally and fails in CI, passes when it should fail, or fails only when run in parallel.
- Choosing how tests authenticate, what they mock, or what CI runs.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Locators, web-first assertions, fixed waits, awaiting, swallowed failures, force, handles | a test is written or flaky, or a locator breaks after a UI change | [`01-locators-and-assertions.md`](./references/01-locators-and-assertions.md) |
| 2 | Isolation, hooks, test data, authentication, what to mock | tests collide in parallel, depend on order, or log in | [`02-isolation-auth-and-data.md`](./references/02-isolation-auth-and-data.md) |
| 3 | Config, CI, trace, browsers, lint rules that catch silent failures | the config is written or CI behaves differently from local | [`03-ci-config-and-lint.md`](./references/03-ci-config-and-lint.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a test whose `await` was removed on purpose was caught by the
linter or the type check (§1.5), the suite was run in parallel and with `--repeat-each` and stayed green
(§2.1), a second run authenticated from the saved state without the login steps (§2.4), and a `test.only`
committed on a scratch branch failed the CI run (§3.1). A test that was only read is not verified.

## Guardrails
- Never use `waitForTimeout`, `waitForSelector`, `waitForNavigation` or `networkidle` in a test (§1.4).
- Never assert on a value read once (`isVisible()`, `textContent()`) when a web-first assertion exists (§1.3).
- Never leave a Playwright call or an async matcher without `await` (§1.5).
- Never put an `expect` inside a `catch` or behind an `if` (§1.6).
- Never commit the authenticated state directory (§2.4).
- Never let one test depend on data or order created by another (§2.1, §2.3).
- Where this block and the project's `data-test-*` doctrine differ on selectors, the project doctrine wins (§1.1).
- This block states Playwright behaviour as of the repository commit in
  [`references/origin.md`](./references/origin.md) (docs of the 1.65.0-next development line). Check an API name
  or default against the Playwright version the project pins. Nothing was run while writing it.

## Origin
Rewritten from the Playwright documentation pages on best practices, isolation, authentication, retries,
configuration and web server (Apache-2.0), the community `eslint-plugin-playwright` rule pages (MIT), the TestDino
common-pitfalls page (MIT) and the Currents assertions page (MIT), read 2026-10-15. 🟡: never run by us; open
points are in [`references/origin.md`](./references/origin.md).
