# testing-library-query-pitfalls: origin and source stamps

> Provenance of `skills/testing-library-query-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from rule documentation and reading, never run by us. No test was executed and nothing
was installed while writing it. The Testing Library documentation site was not read: every rule below is stated
as the lint plugin's pages state it.

## Sources (all re-read in full 2026-10-15, rewritten in our own words, no sample code copied)

| Source | Licence | What it gave |
|---|---|---|
| testing-library/eslint-plugin-testing-library, `docs/rules`: `prefer-screen-queries`, `no-container`, `no-node-access`, `no-test-id-queries`, `consistent-data-testid`, `prefer-presence-queries`, `prefer-find-by`, `prefer-query-by-disappearance`, `await-async-queries`, `no-await-sync-queries`, `no-promise-in-fire-event`, `no-global-regexp-flag-in-query`, `no-wait-for-side-effects`, `no-wait-for-multiple-assertions`, `no-wait-for-snapshot`, `prefer-user-event`, `prefer-user-event-setup`, `await-async-events`, `no-await-sync-events`, `no-unnecessary-act`, `no-manual-cleanup`, `no-render-in-lifecycle` (commit 6f5c603, 2026-10-05) | MIT (repository LICENSE file, re-checked) | Every query, wait, event, act and cleanup rule and its stated reason; the flavours each rule applies to; the user-event v14 split |
| goldbergyoni/javascript-testing-best-practices, `readme.md` sections 3.1, 3.2, 3.3 and 3.4 (commit 63a2bb0, 2023-08-08) | MIT (repository LICENSE file, re-checked) | Separate UI from logic, the dedicated test attribute, fully rendered components and their size limit, do not sleep |

The licence of each repository was verified again from its LICENSE file in this session.

## Rewrite notes
Every rule is attributed to its plugin page in the text. The two version-bound facts are stated with their
version as the pages state it: user-event v14 (`setup()` recommended before render, all methods asynchronous) and
earlier versions (synchronous, except `type` and `keyboard` with `delay`); and `fireEvent` being asynchronous only
in the Vue and Marko packages, with Svelte noted on the page as asynchronous but not yet supported by the plugin.

**Decision where sources disagree:** test ids (§1.2). The plugin's `no-test-id-queries` and Playwright's guide lead
with role and label; the project doctrine uses `data-test-*`; Goldberg's guide recommends a dedicated attribute
when no stable one exists. Project doctrine wins; the lint rule is left off.

**Own guidance, not from a source:** the verification lines, the break-it check in §3.1, the instruction to read an
`act` warning before acting (§2.3.5), the advice to disable `prefer-user-event-setup` when the setup lives in a
shared utility file (the page says to disable it; the wording is ours), and the decision to keep
`no-test-id-queries` off.

## Removed from the review item
1. **Kept, each re-read:** `getBy*` for presence and `queryBy*` for absence, `findBy*` as `getBy*` plus `waitFor`, one
   `waitFor` per async target, no side effect in `waitFor`, user-event v14, `fireEvent` async only in Vue and
   Marko, no act wrapping, no manual cleanup, no render in `beforeEach`, no `/g` flag, full rendering.
2. **Softened:** the item says a `queryBy*` in a presence assertion "gives a useless null message". The page says a
   `getBy*` offers better information than the other queries, so the text uses that wording (§1.3.2).
3. **Re-written, not dropped:** the item's "separate UI from logic so logic is tested without the DOM". The guide
   warns that skipping rendering gives tests that do not resemble reality, so the rule reads "extract the data
   from the markup, do not skip rendering" (§3.2).
4. **Added from the pages, not in the item:** the unawaited `findBy*` promise, awaiting a synchronous query,
   a promise passed to `fireEvent`, and a snapshot inside `waitFor`.

## Not verified
1. **The Testing Library documentation site** (query priority, `configure`, `testIdAttribute` setup, user-event
   options) was not read; the page describing the role-first priority is not cited.
2. **How to configure `testIdAttribute`** was not re-read (§1.2.4); only the plugin's note that it can be overridden.
3. **Behaviour of `waitFor` timeouts and intervals** (defaults) is not stated here; no page read gives them.
4. **Whether `userEvent.setup()` must precede `render`** is as `prefer-user-event-setup` states it ("recommends
   calling setup() before rendering"); the user-event documentation was not read.
5. **Svelte `fireEvent` behaviour** is as the plugin notes it, not confirmed against the Svelte package.
6. **Plugin rules not read:** `prefer-explicit-assert`, `prefer-implicit-assert`, `prefer-query-matchers`,
   `render-result-naming-convention`, `no-debugging-utils`, `no-dom-import`, `await-async-utils`.

## Related blocks
`testing-anti-patterns`, `playwright-e2e-pitfalls`, `jest-vitest-assertion-pitfalls`, `flaky-test-triage-pitfalls`,
`tdd`, `accessibility`.
