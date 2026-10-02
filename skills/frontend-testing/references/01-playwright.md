# frontend-testing §1 — End-to-end tests with Playwright (v1.63)

> Reference of `skills/frontend-testing`, step 4. Read it when the project's end-to-end runner is Playwright
> Test, or when one is being set up. The layer doctrine (which defect belongs to which layer) stays in
> `SKILL.md` and is tool-free; this file is the one place where a tool is named, pinned to **Playwright 1.63**
> (documentation read 2026-10-02). Another runner translates the intent of each rule.

## Finding and acting
1. **Locate by what the user perceives, in this order.** Role with its accessible name first
   (`getByRole('button', { name: 'Sign in' })`), then label, placeholder, visible text, alt text, title; the
   dedicated test-id attribute is the contract for what has no stable user-facing handle. CSS and XPath tied
   to the DOM structure break at the next redesign. A role locator that cannot find the element is also an
   accessibility finding (`skills/accessibility`).
2. **Narrow by chaining and filtering**, not by position: a row filtered by its text, then the control inside
   it. A locator that matches several elements fails in strict mode when acted on; do not silence it with
   `.first()` unless "any of them" is the intent.
3. **Do not wait by time; do not check by hand.** Actions wait for the element to be visible, stable (not
   animating), able to receive the event (not covered) and enabled, and `fill` also for editable. Assertions
   on a locator (`toBeVisible`, `toHaveText`, `toHaveURL`) retry until a timeout (5 s by default, test
   timeout 30 s). A one-shot read such as `expect(await locator.isVisible()).toBe(true)` does not wait at all
   and is a flake. For a value that is not a locator, `expect.poll` retries a function.
4. **Await every call.** A missing `await` turns a failure into a pass that ends early. Turn the
   floating-promise lint rule of the TypeScript linter on for the test directory.
5. **Soft assertions** (`expect.soft`) collect several checks in one test without stopping at the first; use
   them for a page of independent facts, not for steps that depend on each other.

## Isolation and state
6. **Every test gets its own browser context**: its own storage, cookies and data. Tests must not depend on
   order or on a sibling's side effects. Shared setup goes in a hook or a fixture, not in an earlier test.
7. **Sign in once, reuse the state.** A `setup` project signs in, writes the browser state to a file
   (`storageState`), and every test project depends on it and loads that file. Wait for the final URL or a
   signed-in element before saving, since a login can set cookies across redirects. Use this only when tests
   can share one account without affecting each other; tests that change server-side state for the account
   need an account each (one per worker).
8. **Keep the state file out of version control** (a `.auth` directory in `.gitignore`): it holds cookies and
   headers that can impersonate the account. Test accounts only, never a real person's.
9. **Fixtures over repeated set-up.** A fixture creates what a test needs and tears it down after, is
   composed from others, and is created only for tests that name it unless declared automatic. A
   worker-scoped fixture is built once per worker and shared by its tests, so it must hold nothing a test
   mutates.

## Boundaries
10. **Mock at the network boundary the app does not control.** Route third-party calls and the API calls a test
    is not about; fulfil, modify or abort them. Do not test the behaviour of someone else's site. For the
    system under test keep the real backend on controlled data (a staging environment or a seeded database
    that does not change underneath the test).
11. **Recorded traffic (HAR) is a fixture that goes stale.** Commit the file next to the tests, re-record on a
    schedule or when the contract moves, and let a contract test (`SKILL.md` step 2) own the drift; a replayed
    recording proves nothing about the current API.
12. **Start the application from the config** (the web-server option: command, URL to wait for, reuse locally
    but not on CI) so a test run needs no manual step.

## Parallelism, retries, evidence
13. **Files run in parallel across workers; tests in a file run in order in one worker** unless the project or
    the describe block is made fully parallel. Workers share nothing: no test may rely on another worker's
    data. Shard across machines when the suite outgrows one.
14. **A failing test discards its worker and its browser**, and its remaining tests restart in a new one, so
    `beforeAll` hooks run again. A retry is a diagnostic: set retries on CI only, and treat a test that passed
    on retry as a flaky test with a deadline (`SKILL.md` step 7), not as green.
15. **Record a trace on the first retry** (`trace: 'on-first-retry'`) or keep traces only for failures
    (`'retain-on-failure'`): the trace has the DOM at each step, the network and the console, and replaces
    guessing about a CI-only failure. Upload it as a CI artifact. Traces and state files may hold personal
    data: scope their retention.
16. **Screenshots depend on the machine.** Rendering differs by operating system, browser version, headless
    mode and hardware, so baselines are named per browser and platform and are compared only where they were
    made (the same container image everywhere). Freeze what moves (data, clock, animation). Updating a baseline
    (`--update-snapshots`) is a review decision, never a reflex.
17. **Install only the browsers a project uses on CI**, run on Linux, and keep the test dependency current so
    the newest browser versions are tested before users have them. Run the accessibility engine on the same
    journeys; its report covers a fraction of the problems, and the manual pass remains
    (`skills/accessibility` §2.12).

## Mechanical checks

```
grep -rnE "waitForTimeout|page\.waitFor\(" tests
grep -rnE "expect\(await [^)]*\.(isVisible|isEnabled|isChecked|textContent|innerText)\(\)" tests
grep -rnE "\.(first|nth|last)\(" tests
grep -rnE "page\.(locator|\\$)\(['\"][.#\[]" tests
grep -nE "retries|trace|fullyParallel|workers|storageState|webServer" playwright.config.*
grep -nE "\.auth" .gitignore
```

- A fixed wait or a one-shot `isVisible` read is a finding. A CSS locator is a finding unless a test-id
  attribute is not available and the reason is recorded.
- The config states retries, the trace policy and the state file; a state file path missing from `.gitignore`
  is a secret in waiting.
