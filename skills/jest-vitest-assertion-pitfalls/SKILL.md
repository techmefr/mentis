---
name: jest-vitest-assertion-pitfalls
description: "Use when Jest or Vitest tests are written or reviewed for assertions that never run or prove nothing: async expect not awaited, expect.poll and promise chains, expect inside if or catch, a test with no expect, expect outside a test, the done callback, toThrow without a message, toEqual on errors, focused and disabled tests, identical titles, exporting from a test file, strict equality, bare toHaveBeenCalled, snapshot size and interpolation, concurrent snapshots, Vitest hoisting and typed mocks, Jest v30 removed aliases."
---

# jest-vitest-assertion-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`) for unit and component tests in Jest or Vitest. The three sections share one
premise: **in these runners a test fails only when something throws, so an assertion that is skipped, not awaited
or never called leaves a green test that checked nothing**. Mock theatre, incomplete mocks and timing guesses are in
`testing-anti-patterns`; test hygiene for Node services and the five outcomes to assert are in
`prisma-ops-and-test-hygiene` §2; neither is repeated. Component queries are in `testing-library-query-pitfalls`
and browser tests in `playwright-e2e-pitfalls`.

## When
- Writing or reviewing a Jest or Vitest test, or setting up the lint rules for them.
- A test passes although the code is wrong, a focused or skipped test shrank the run, or a snapshot diff is
  unreadable.
- Moving between Jest versions, or between Jest and Vitest.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Assertions that never run: async, conditional, missing, outside a test, `done`, thrown errors | a test is async, catches an error, or has no clear assertion | [`01-assertions-that-never-run.md`](./references/01-assertions-that-never-run.md) |
| 2 | Focus, skip, titles and test files | a `.only` or `.skip` appears, or a test file is imported | [`02-focus-skip-and-files.md`](./references/02-focus-skip-and-files.md) |
| 3 | Equality, called-with, snapshots, hoisted mocks, Jest v30 | a matcher, snapshot or `vi.mock` is chosen | [`03-matchers-snapshots-and-mocks.md`](./references/03-matchers-snapshots-and-mocks.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: an `await` was removed from an async assertion on purpose and
the lint rule flagged it (§1.1), a `try`/`catch` test whose function stopped throwing was shown to pass and then
rewritten so it failed (§1.2), a test with its `expect` deleted was flagged (§1.3), and a committed `.only` failed
the lint step (§2.1). A test that was only read is not verified.

## Guardrails
- Never leave an async assertion, `expect.poll` or a promise chain holding an `expect` without `await` or `return` (§1.1).
- Never put an `expect` inside a `catch` or behind an `if` (§1.2).
- Never accept a test body with no `expect` or an `expect` that is not followed by a matcher call (§1.3).
- Never use the `done` callback in a new test (§1.4).
- Never merge a `.only`, `fit` or `fdescribe` (§2.1).
- Never write a `.skip` or an empty-bodied test without a reason, an owner and a date (§2.2).
- Never export from, or import, a test file (§2.4).
- This block states the rules as the lint plugin pages state them, at the plugin commits in
  [`references/origin.md`](./references/origin.md); the Jest and Vitest documentation themselves were not read.
  Version-bound facts name their version. Nothing was run while writing it.

## Origin
Rewritten from the `eslint-plugin-jest` and `eslint-plugin-vitest` rule pages (MIT) and sections 1.8 and 1.10 of
Goldberg's JavaScript testing best-practices guide (MIT), read 2026-10-15. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
