# playwright-e2e-pitfalls §2 — Isolation, authentication and data

A browser test shares a lot by accident: the account, the database rows, the worker, a module variable. Each
shared thing is a way for one test to change the result of another, and parallel runs make it visible.

## 2.1 One test, one clean browser context
1. **Playwright gives every test its own browser context** with its own cookies, local storage and session
   storage, like an incognito profile; creating one is fast and cheap (Playwright isolation page).
2. **Why it matters**: a failure does not carry over, a single test can be run as many times as wanted, and
   order does not matter under parallel runs or sharding (Playwright isolation page).
3. **Starting from scratch beats cleaning up between tests**: cleanup is easy to forget and some state cannot be
   cleaned, such as visited links (Playwright isolation page).
4. **Do not rely on another test's data or order.** A test that needs a signed-in page uses a `beforeEach` hook,
   a fixture or saved authentication state, not the previous test (Playwright best practices). A little
   duplication is fine when it keeps a simple test readable.
5. **Serial mode groups dependent tests and retries them together**, and the Playwright page says it is usually
   better to make tests independent so they run and retry on their own (Playwright retries page).
6. **Verify**: run the suite with `--workers=1` and with several workers, and a single test many times with
   `--repeat-each`. A test that passes alone and fails in the suite is a data or order dependency; the triage is in
   `flaky-test-triage-pitfalls` §1.

## 2.2 Per-test setup does not belong in `beforeAll`
1. **`beforeAll` state is shared by every test in the file**: one test changes it and the next fails
   (TestDino).
2. **A failing test discards the worker, and a new worker runs `beforeAll` again** (Playwright retries page),
   so a `beforeAll` that creates server data runs once per worker restart, not once per file.
3. **Use `beforeEach`, or a test-scoped fixture when the setup needs teardown**; a fixture's code after
   `use()` runs even when the test failed (TestDino; Currents).
4. **Module-level mutable variables are shared between tests** and between parallel tests of the same worker
   process; a variable assigned in one test and read in another makes order a hidden input (TestDino).

## 2.3 Data each test owns
1. **Build the data inside the test or in a test-scoped fixture, with a value that is unique per test** (an
   email or name carrying a unique suffix), and delete it afterwards (TestDino; Currents).
2. **Tests that run in parallel against one backend collide on shared rows**: "duplicate key" errors and failures
   that vanish when run alone are the signature (TestDino).
3. **When working with a database, control the data**: test against an environment that does not change under
   the test (Playwright best practices). For visual comparisons the operating system and browser versions must
   be the same.

## 2.4 Authentication
1. **Authenticate once in a `setup` project and reuse the saved state** through `storageState`, declaring the
   setup project as a dependency of the testing projects. This is Playwright's recommended approach when tests
   do not change server-side state, that is, when you can picture all tests running at once with the same account
   (Playwright authentication page).
2. **When tests change server-side state, use one account per parallel worker.** Override the `storageState`
   fixture with a worker-scoped fixture keyed on the worker's parallel index, so each worker signs in once with
   its own account; accounts must be unique so that several people can run the suite at the same time
   (Playwright authentication page).
3. **Sign in inside that fixture from a clean context** (`storageState: undefined`), so an existing state does
   not leak into the login (Playwright authentication page).
4. **Wait for the final signed-in state before saving it.** A login that redirects several times sets its
   cookies along the way, so wait for the final URL or a signed-in element (Playwright authentication page).
5. **The saved state file holds live cookies and headers.** Create the `playwright/.auth` directory, add it to
   `.gitignore`, and never commit it, in a private or a public repository (Playwright authentication page).
6. **Delete the saved state when it expires**, or write it under the project's output directory, which is
   cleaned before every run (Playwright authentication page). UI mode does not run the setup project by
   default, so run the setup file by hand when the state has expired.
7. **Decision: a login in a "before all" hook against the setup-project mechanism.** Goldberg's JavaScript
   testing best-practices guide (section 3.8) logs in once before all tests and reuses the token, trading autonomy for
   speed, and says tests should still create their own records. Playwright reaches the same reuse through a setup
   project and `storageState`. Keep the Playwright mechanism, and keep the guide's second half: reused
   credentials, not shared records (§2.3).

## 2.5 Mock only what you do not own
1. **Do not test third-party sites or servers you do not control**: their content, cookie banners and overlays
   can fail your test. Fulfil the call with `page.route` and guarantee the response you need (Playwright best
   practices).
2. **Do not mock your own API by default.** A test that fulfils its own backend's responses passes when that
   backend is broken, and the mocks drift from the real contract (TestDino). Run the real backend through the
   `webServer` option (§3.1).
3. **Mocking your own API is right for states that are hard to produce**: an error status, a timeout, an edge case
   (TestDino). Say in the test name that the response is simulated.
4. **Block what is not part of the test**, such as analytics and ad requests, with `route.abort()` (TestDino).
5. **Several users in one test** use several contexts from `browser.newContext()`, one per user, not one page
   that signs in and out (Playwright isolation page).
