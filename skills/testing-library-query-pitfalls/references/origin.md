# testing-library-query-pitfalls: origin and source stamps

> Provenance of `skills/testing-library-query-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from rule documentation and reading, never run by us. No test was executed and nothing
was installed while writing it. The Testing Library documentation site was first not read; on 2026-10-20 the
documentation repository was read for the points listed under the added table, and every other rule below is
stated as the lint plugin's pages state it.

## Sources (all re-read in full 2026-10-15, rewritten in our own words, no sample code copied)

| Source | Licence | What it gave |
|---|---|---|
| testing-library/eslint-plugin-testing-library, `docs/rules`: `prefer-screen-queries`, `no-container`, `no-node-access`, `no-test-id-queries`, `consistent-data-testid`, `prefer-presence-queries`, `prefer-find-by`, `prefer-query-by-disappearance`, `await-async-queries`, `no-await-sync-queries`, `no-promise-in-fire-event`, `no-global-regexp-flag-in-query`, `no-wait-for-side-effects`, `no-wait-for-multiple-assertions`, `no-wait-for-snapshot`, `prefer-user-event`, `prefer-user-event-setup`, `await-async-events`, `no-await-sync-events`, `no-unnecessary-act`, `no-manual-cleanup`, `no-render-in-lifecycle` (commit 6f5c603, 2026-10-05) | MIT (repository LICENSE file, re-checked) | Every query, wait, event, act and cleanup rule and its stated reason; the flavours each rule applies to; the user-event v14 split |
| goldbergyoni/javascript-testing-best-practices, `readme.md` sections 3.1, 3.2, 3.3 and 3.4 (commit 63a2bb0, 2023-08-08) | MIT (repository LICENSE file, re-checked) | Separate UI from logic, the dedicated test attribute, fully rendered components and their size limit, do not sleep |

The licence of each repository was verified again from its LICENSE file in this session.

**Added 2026-10-20:** the Testing Library documentation repository (`testing-library/testing-library-docs`, `docs/`,
main branch, read on 2026-10-20). Its licence was read through the repository's licence file: **MIT**. The pages
used, facts only and rewritten:

| Page | What it gave |
|---|---|
| queries, About (priority section) | the order of priority and the last-resort status of test ids (§1.2) |
| DOM Testing Library, async methods | `findBy` as `getBy` plus `waitFor`, the throw-to-retry rule, 1000 ms and 50 ms defaults, promise callbacks (§2.1, §1.3) |
| DOM Testing Library, configuration | `configure` with `testIdAttribute` (§1.2.4) |
| DOM Testing Library, FAQ and appearance guide | `container` queries shown as a fallback; `queryBy` for absence (§1.1, §1.3) |
| user-event, introduction and setup | `setup()` before render, no use in hooks, direct API (§2.2) |
| React Testing Library, setup and API, FAQ | auto cleanup condition and the Vitest globals note, the `act` warning advice (§2.3, §2.4) |

## Rewrite notes
Every rule is attributed to its plugin page in the text. The two version-bound facts are stated with their
version as the pages state it: user-event v14 (`setup()` recommended before render, all methods asynchronous) and
earlier versions (synchronous, except `type` and `keyboard` with `delay`); and `fireEvent` being asynchronous only
in the Vue and Marko packages, with Svelte noted on the page as asynchronous but not yet supported by the plugin.

**Decision where sources disagree:** test ids (§1.2). The plugin's `no-test-id-queries` and Playwright's guide lead
with role and label; the project doctrine uses `data-test-*`; Goldberg's guide recommends a dedicated attribute
when no stable one exists. Project doctrine wins; the lint rule is left off.

**Own guidance, not from a source:** the verification lines, the break-it check in §3.1, the advice to disable `prefer-user-event-setup` when the setup lives in a
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
1. **Verified 2026-10-20 against the documentation:** query priority (§1.2), `testIdAttribute` configuration
   (§1.2.4), `waitFor` defaults and retry rule (§2.1.6), `setup()` before render (§2.2.1), `act` warning advice
   (§2.3.5), auto cleanup and the Vitest globals requirement (§2.4.1). The user-event options page and the full
   query pages (`*ByRole` options, `hidden`) were not read.
2. **Not found in the documentation read:** a statement banning `container` queries (the FAQ shows them); that
   rule is the plugin's.
3. **The Testing Library documentation does not cover the flavour-specific points** (`fireEvent` async in Vue and
   Marko, `act` in some flavours): they stay as the plugin pages state them.
4. **A dedicated per-flavour check** of the lint configurations was not done.
4. **Svelte `fireEvent` behaviour** is as the plugin notes it, not confirmed against the Svelte package.
5. **Plugin rules not read:** `prefer-explicit-assert`, `prefer-implicit-assert`, `prefer-query-matchers`,
   `render-result-naming-convention`, `no-debugging-utils`, `no-dom-import`, `await-async-utils`.

## Related blocks
`testing-anti-patterns`, `playwright-e2e-pitfalls`, `jest-vitest-assertion-pitfalls`, `flaky-test-triage-pitfalls`,
`tdd`, `accessibility`.
