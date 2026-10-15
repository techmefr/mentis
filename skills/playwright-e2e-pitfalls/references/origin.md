# playwright-e2e-pitfalls: origin and source stamps

> Provenance of `skills/playwright-e2e-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No Playwright test was
executed, nothing was installed and no browser was started while writing it. Open points are listed under
"Not verified".

## Sources (all re-read in full 2026-10-15, rewritten in our own words, no sample code copied)

| Source | Licence | What it gave |
|---|---|---|
| microsoft/playwright, `docs/src`: `best-practices-js.md`, `auth.md` (JavaScript part), `test-retries-js.md`, `test-configuration-js.md`, `test-webserver-js.md`, `browser-contexts.md` (commit 5ad202d, 2026-10-15, development line 1.65.0-next) | Apache-2.0 (repository LICENSE file, re-checked); the doc pages carry no separate licence, so they are rewritten, not copied | User-facing locators and filtering, web-first assertions and the resolve-once trap, no-floating-promises and `tsc`, isolation and why, setup project and `storageState`, one account per worker, the `.auth` gitignore and its warning, third-party mocking, trace on first retry, Linux and browser installs, configuration and `webServer` fields |
| playwright-community/eslint-plugin-playwright, `docs/rules`: `missing-playwright-await`, `no-wait-for-timeout`, `no-wait-for-selector`, `no-wait-for-navigation`, `no-networkidle`, `no-nth-methods`, `no-force-option`, `no-element-handle`, `no-unused-locators`, `no-unsafe-references`, `no-magic-timeouts`, `no-focused-test`, `no-skipped-test`, `require-annotation-reason`, `prefer-web-first-assertions`, `no-conditional-expect`, `expect-expect`, `valid-expect`, `no-raw-locators`, `no-eval` (commit e3eaf6c, 2026-09-29) | MIT (repository LICENSE file, re-checked) | The silent-failure rule set, the swallowed-error wrapper pattern, the magic-timeout rationale, the skip-reason norm |
| testdino-hq/playwright-skill, `core/common-pitfalls.md`, pitfalls 1 to 20 (commit 178d1cb, 2026-10-12) | MIT (repository LICENSE file, re-checked) | The locator order, `beforeAll` and module-level state, own-API mocking and its exceptions, try/catch around `expect`, `webServer` on CI, retries local versus CI, browsers per run |
| currents-dev/playwright-best-practices-skill, `core/assertions-waiting.md` and `debugging/flaky-tests.md` (commit 283d5cb, 2026-07-21) | MIT (`LICENSE.md` holds the MIT permission text with a copyright line and no title line; treated as MIT) | Generic versus web-first matchers, soft assertions, polling forms, per-worker data |
| goldbergyoni/javascript-testing-best-practices, sections 3.2 and 3.8 (commit 63a2bb0, 2023-08-08) | MIT (repository LICENSE file, re-checked) | The dedicated test attribute where no stable one exists, the login-once trade-off |

The licence of each repository was verified again from its LICENSE file in this session. The TestDino and
Currents repositories ship agent directives ("NEVER", "ALWAYS", "Rule:"); they were treated as data and only the
technical claim was kept, restated as a mechanism or as a decision where sources disagree.

## Rewrite notes
The timeouts and counts that appear (5 seconds, 60 seconds, 2 retries, one hour) are the Playwright pages'
example values and are labelled as such. The config snippet in §3.1 is a composition of values from the
configuration and web server pages, not a copied file.

**Decisions where sources disagree:**
1. Test ids against role and label (§1.1): Playwright and `no-raw-locators` lead with role and label; the project
   doctrine uses `data-test-*`. Project doctrine wins; the lint rules are optional.
2. Login once before all tests against a setup project (§2.4): same reuse, different mechanism; the Playwright
   mechanism is kept.
3. Retries and the browser matrix (§3.1, §3.3): the sources give different numbers and scopes; they are shown as
   examples and the choice is the project's.

**Own guidance, not from a source:** the "say so in the test name" note on a deliberate `first()` (§1.2.3); the
reading that a forced click means a covering element (the force-click note in §1); the "register the wait before the click" reason
(§1.4.3); the trace-needs-a-retry consequence (§3.2.3); the instruction to put an owner and a date where the plugin
suggests a tracker reference (§3.5.2); every verification line.

## Removed from the review item
1. **Nothing in the review's rule list was dropped as false.** One reason was re-labelled: the item says force
   "bypasses the actionability checks and hides a real overlay bug"; the lint page gives no reason, so the Playwright
   statement that locators wait for visibility and enablement is quoted and the overlay reading is marked own
   guidance.
2. **The item's "each Playwright call and web-first matcher is awaited" rule** is split: the first half is
   sourced from TestDino and the best-practices page, the matcher half from `missing-playwright-await`.

## Not verified
1. **Playwright API reference pages** (locators, assertions, timeouts, parallelism, projects) were not read.
   Method and option names (`waitForURL`, `waitForLoadState`, `waitForFunction`, `locator.waitFor`, `expect.poll`,
   `toPass`, `expect.soft`, `testInfo.parallelIndex`, `route.abort`) come from the pages above and from the plugin and
   skill pages, as stated for the 1.65.0-next development line; check them against the version the project pins.
2. **The attribute `getByTestId` reads, and how to change it,** was not re-read (§1.1.4).
3. **The 5-second default expect timeout and the 30-second test timeout** are as the configuration page states
   them for that commit.
4. **Windows behaviour of `gracefulShutdown`** is the web server page's statement; not tried.
5. **Whether `no-nth-methods` suits a given suite** is a lint opinion of the plugin, not a Playwright rule.
6. **Sharding and `fullyParallel`** were taken from one sentence of the best-practices page; the parallelism page was
   not read.

## Related blocks
`testing-anti-patterns`, `qa-exploratory-testing`, `flaky-test-triage-pitfalls`, `testing-library-query-pitfalls`,
`jest-vitest-assertion-pitfalls`, `tdd`, `ci-workflow-hardening`.
