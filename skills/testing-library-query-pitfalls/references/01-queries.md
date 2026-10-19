# testing-library-query-pitfalls §1 — Queries

A Testing Library test is worth what it proves about a user reaching a control. A query that bypasses the
accessible surface proves only that a node exists.

## 1.1 Query from `screen`, by what a user perceives
1. **`screen` holds every query**, which helps autocomplete and keeps each test simpler; destructuring queries
   from the `render` result is flagged (`prefer-screen-queries`, eslint-plugin-testing-library). Use the
   `render` result for what `screen` lacks: `rerender`, `unmount`, `asFragment`, `container` and `baseElement`.
2. **Scope with `within(subtree)`** rather than passing a subtree as the first argument of a top-level query
   (`prefer-screen-queries`). The same page lists the exceptions: queries chained to `within`, custom queries, and
   a custom `container` or `baseElement`.
3. **Do not query through `container`** (`container.querySelector('.btn-primary')`): the test loses the
   confidence that a user can reach the control, reads worse and breaks more often (`no-container`).
4. **Do not reach through nodes** with `closest`, `lastChild`, indexes into a list of nodes, or call `click()`
   or `select()` on a node: use queries and `userEvent` instead (`no-node-access`). `focus()` and `blur()` are
   not reported, because calling them on the element is recommended over firing the focus events, and an element
   that cannot take focus then fails the assertion (`no-node-access`).
5. **Verify** by moving the control to a different element or class and re-running: a role or label query still
   passes, a selector query does not.

## 1.2 Test ids: a decision
1. **The plugin's `no-test-id-queries` rule bans every `*ByTestId` query**, because a test id couples the test to
   an implementation detail instead of to how the control is used, and points to `getByRole` and
   `getByLabelText`. Playwright's own guide leads with role and label as well (`playwright-e2e-pitfalls` §1.1).
2. **The project's doctrine uses `data-test-*` attributes as the stable selector** (`tdd`, which points at the
   test-casebook contract). Goldberg's guide (section 3.2) says to query by attributes unlikely to change, such as a
   form label, and to add a dedicated test attribute when the element has none.
3. **Decision: the project doctrine wins.** Query by role or label where the control has an accessible name;
   use the `data-test-*` attribute where it has none or its text is dynamic. Keep `no-test-id-queries` off, or
   scoped to the folders where it fits, so the lint does not fight the doctrine.
4. **A dedicated attribute needs Testing Library to read it.** The plugin's `consistent-data-testid` page notes
   that the queried attribute can be overridden in the Testing Library configuration and exposes a
   `testIdAttribute` option for it. That rule validates the attribute's values against a pattern you supply and,
   per its page, is available for the React flavour only. The configuration call itself was not re-read.

## 1.3 `get`, `query` and `find` each mean something
1. **`getBy*` throws when the element is missing, so use it to assert presence**: the error is descriptive.
   **`queryBy*` returns `null` (or an empty array for `queryAllBy*`), so use it to assert absence**: the test does not
   fail before the assertion can run (`prefer-presence-queries`).
2. **The two mistakes are symmetrical**: a `queryBy*` in a presence assertion gives less information than the
   `getBy*` error would, and a `getBy*` in an absence assertion throws before the assertion executes
   (`prefer-presence-queries`).
3. **`findBy*` is `getBy*` plus `waitFor`**, and takes the `waitFor` options as its last argument. To wait for an
   element, use `findBy*` rather than `waitFor` around a single `getBy*` (`prefer-find-by`).
4. **A `waitFor` with a code block, or around a custom function, is not the same case** and stays a `waitFor`; the
   rule only rewrites the one-query arrow form (`prefer-find-by`).
5. **To wait for disappearance, pass a `queryBy*` to `waitForElementToBeRemoved`.** A `getBy*` throws if the
   element is already gone, and the helper requires that the element exists before it waits for removal
   (`prefer-query-by-disappearance`).
6. **Do not `await` the synchronous variants**: `getBy*`, `getAllBy*`, `queryBy*` and `queryAllBy*`
   (`no-await-sync-queries`). **Do `await` `findBy*` and `findAllBy*`**, or return the promise; an unhandled
   one asserts nothing (`await-async-queries`).
7. **Never pass a `findBy*` promise to `fireEvent`**: it expects a DOM element and fails. Await the query first
   (`no-promise-in-fire-event`).

## 1.4 A global regexp keeps state
1. **A regexp with the `/g` flag holds `lastIndex` state**, which can produce false results when it is used to
   query for an element (`no-global-regexp-flag-in-query`). Write `/hello/i`, not `/hello/gi`; the plugin can fix
   it automatically.
2. **Verify** by searching the tests for a regexp literal ending in `g` inside a query call.
