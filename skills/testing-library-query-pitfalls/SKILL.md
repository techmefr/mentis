---
name: testing-library-query-pitfalls
description: "Use when a component test written with Testing Library (DOM, React, Vue, Angular, Svelte, Marko flavours) is written or reviewed: querying with screen and by role, label or text instead of container or node access, getBy versus queryBy versus findBy, the test id decision, waitFor traps (side effects, several assertions, snapshots), user-event v14 setup and awaiting, fireEvent, act, cleanup and render in beforeEach, the global regexp flag, and rendering the component fully."
---

# testing-library-query-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`) for component and DOM tests written with Testing Library. The three
sections share one premise: **a test that reaches into the DOM instead of acting like a user, or that waits the
wrong way, stays green while the control is unreachable or the wait is a coin flip**. Mock rules and the generic
timing rule are in `testing-anti-patterns` §3 and are not repeated; locator ideas for real-browser tests are in
`playwright-e2e-pitfalls`; assertion traps shared with Jest and Vitest are in `jest-vitest-assertion-pitfalls`.

## When
- Writing or reviewing a component test that uses `render`, `screen`, `userEvent` or `fireEvent`.
- A component test passes but the control is not reachable by a user, flakes on a wait, or prints an `act`
  warning.
- Choosing between `getBy`, `queryBy` and `findBy`, or deciding whether a test id is acceptable.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Queries: `screen`, role and label, container and node access, test ids, `get` versus `query` versus `find`, regexps | a query is written, or a test breaks after a markup change | [`01-queries.md`](./references/01-queries.md) |
| 2 | Async and events: `waitFor` traps, user-event v14, `fireEvent`, `act`, cleanup, render placement | a test waits, clicks or types, or warns about `act` | [`02-async-and-events.md`](./references/02-async-and-events.md) |
| 3 | Structure: full rendering, UI versus logic, sleeping, the lint set | a component is large, or the lint plugin is set up | [`03-structure-and-lint.md`](./references/03-structure-and-lint.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a control was moved to another element and the role-based test
still passed (§1.1), a component that stopped rendering made a `queryBy` presence check fail with a useful
message (§1.3), a click placed inside `waitFor` was moved out and the test stayed green over repeated runs (§2.1),
and the lint plugin flagged a deliberate violation of each rule enabled in §3.4. A test that was only read is not
verified.

## Guardrails
- Never query through `container` or reach for nodes with `closest`, `parentElement` or child indexes (§1.1).
- Never use `getBy` to prove absence or `queryBy` to prove presence (§1.3).
- Never put a click, a typed key or a render inside `waitFor` (§2.1).
- Never call a user-event method without `await` (§2.2).
- Never wrap Testing Library calls in `act` to silence a warning (§2.3).
- Never use the `/g` flag in a query regexp (§1.4).
- Where this block and the project's `data-test-*` doctrine differ on selectors, the project doctrine wins (§1.2).
- This block states the behaviour described by the plugin pages at the commit in
  [`references/origin.md`](./references/origin.md); the Testing Library documentation (MIT) was read on 2026-10-20 for the points it
  covers (query priority, `waitFor`, user-event setup, cleanup, `act`).
  Version-bound facts name their version (user-event v14). Nothing was run while writing it.

## Origin
Rewritten from the `eslint-plugin-testing-library` rule pages (MIT) and sections 3.1 to 3.4 of Goldberg's JavaScript
testing best-practices guide (MIT), read 2026-10-15, and cross-checked on 2026-10-20 against the Testing Library
documentation (MIT). 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
