# playwright-e2e-pitfalls §3 — CI, configuration and lint

The same suite behaves differently on a laptop and on a clean runner: no server is running, a stray `test.only`
is easy to commit, and a retry can turn a real failure green. The config is where those differences are decided.

## 3.1 The configuration that separates CI from local
```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  globalTimeout: 60 * 60 * 1000,
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```
The values come from the Playwright configuration and web server pages; the numbers are the pages' examples, not
measurements for your suite.
1. **`forbidOnly` exits with an error when a test is marked `test.only`**; set it on CI so a focused test cannot
   silently shrink the run (Playwright configuration page). The lint rule `no-focused-test` catches it earlier
   (eslint-plugin-playwright).
2. **Retries on CI only.** The Playwright example uses 2 on CI and 0 elsewhere; zero locally makes flakes visible
   to the person who wrote them (TestDino). What a retry means, and how to track the tests that needed one, is in
   `flaky-test-triage-pitfalls` §2.
3. **`webServer` starts the application so CI does not assume `localhost` is up.** Without it a clean runner
   fails with a refused connection because nothing is listening (TestDino).
4. **`reuseExistingServer: !process.env.CI`**: with `true`, an already-running server on the same url is used;
   with `false`, Playwright throws if a process already listens there (Playwright web server page). Locally you
   keep a dev server running; on CI you want a fresh one.
5. **Give a slow server a larger start-up `timeout`** (60 seconds by default, per the web server page) rather
   than a retry. The readiness `url` is expected to answer with a 2xx, 3xx, 400, 401, 402 or 403 status; the
   `port` option is documented as deprecated in favour of `url`.
6. **Shutting down a Docker container through `webServer` needs `SIGTERM`**: unless `gracefulShutdown` is set the
   process group is killed with `SIGKILL`, and Windows ignores the option (Playwright web server page).
7. **Set `baseURL` and use relative paths**, so the same tests run against local and staging; hard-coded full
   URLs are duplicated everywhere and break when the environment changes (TestDino; Playwright web server
   page). `globalTimeout` stops a hung run with a report instead of waiting for the CI job limit
   (Playwright configuration page).
8. **Verify** by committing a `test.only` and an unreachable `webServer` url on a scratch branch and reading the
   CI result.

## 3.2 Traces, not videos
1. **Debug a CI failure with the trace viewer**, a shareable timeline with DOM snapshots per action, network
   requests and more, rather than videos and screenshots (Playwright best practices).
2. **`trace: 'on-first-retry'` records only when a failed test is retried.** Playwright does not recommend `on`
   for every test because it is heavy; run `--trace on` locally when developing (Playwright best practices).
3. **Consequence of both rules:** a trace on first retry needs a retry, so with zero retries on a branch nothing is
   recorded. Own reasoning: when you turn retries off to hunt a flake, turn the trace on for that run.

## 3.3 What CI runs
1. **Run the tests on every commit and pull request, on Linux**, because it is cheaper; developers can use any
   system locally (Playwright best practices). Consider sharding to make CI faster.
2. **Install only the browsers you use**, for example `playwright install chromium --with-deps`, to save download
   time and disk space (Playwright best practices).
3. **Decision: the browser matrix.** Playwright's guide recommends testing across all browsers so the app works
   for all users, and keeping Playwright up to date to catch failures before a browser release reaches the
   public. TestDino suggests one browser on every pull request and all browsers on a nightly or pre-release job.
   Pick by the product's browser support and record the choice; both readings fit the "run the full matrix on a
   schedule" compromise.
4. **Tests in one file run in order in one worker; tests in different files run in parallel** (Playwright best
   practices). `fullyParallel` and `describe.configure({ mode: 'parallel' })` extend that to tests in a file, which
   is only safe once §2.1 holds.

## 3.4 Lint rules that catch silent failures
Playwright's guide recommends TypeScript and ESLint for tests, with `@typescript-eslint/no-floating-promises`
and `tsc --noEmit` in CI. The community `eslint-plugin-playwright` adds Playwright-aware rules. Enable the ones
below because each stands for a test that passes without proving anything; skip the rules about test names, hook
order, blank lines or `toBe` style, which are taste.

| Rule | Catches | Section |
|---|---|---|
| `missing-playwright-await` | async matchers, `expect.poll`, `test.step`, `waitFor*` without await | §1.5 |
| `no-conditional-expect` | an `expect` in `if`, `catch` or `&&` | §1.6 |
| `expect-expect`, `valid-expect` | a test with no assertion, a matcher never called | §1.6 |
| `prefer-web-first-assertions` | resolve-once reads inside `expect` | §1.3 |
| `no-wait-for-timeout`, `no-wait-for-selector`, `no-wait-for-navigation`, `no-networkidle` | fixed and deprecated waits | §1.4 |
| `no-focused-test`, `no-skipped-test`, `require-annotation-reason` | focused or silently skipped tests | §3.5 |
| `no-force-option`, `no-element-handle`, `no-unused-locators`, `no-unsafe-references` | force, stale handles, dead locators, out-of-scope variables | §1.7 |
| `no-nth-methods`, `no-raw-locators` | position and raw selectors | §1.1, §1.2 |
| `no-magic-timeouts` | inline numeric timeouts that record no reason | §1.4 |

`no-nth-methods` and `no-raw-locators` are a decision, not a default: §1.1 and §1.2 say where the project may
differ.

## 3.5 Skipped and focused tests
1. **A test left on `.only` runs alone and hides the rest**; `no-focused-test` flags the `only` forms of `test`
   and `test.describe` (eslint-plugin-playwright).
2. **`require-annotation-reason` requires a reason on the conditional `skip` and `fixme` calls**, because the
   enforceable norm is rarely "never skip" and usually "never skip silently" (eslint-plugin-playwright). Its
   `pattern` option can require a tracker reference; this repository has no tracker, so write an owner and a
   date in the reason instead, and use the lifecycle in `flaky-test-triage-pitfalls` §3.
3. **The declaration form of `skip` and `fixme` has no description parameter**, so the rule does not check it;
   `no-skipped-test` governs whether the annotation may be used at all (eslint-plugin-playwright).
