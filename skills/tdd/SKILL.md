---
name: tdd
description: Use during the tests step, before the code, write the tests first (test-casebook doctrine) and turn every acceptance criterion into a contract line that fails by default.
---

# tdd

Step 5 of the pipeline (`WORKFLOW.md`). Tests first, and a **default-FAIL contract** that will
make the GATE (step 7) mechanical.

**Where the doctrine lives.** The testing doctrine itself — `data-test-*` selectors, the `task-test.md`
plan, the permission/persona matrix, the coverage floor, the per-stack guides — is owned by the
`test-casebook` package (MIT, `techmefr/test-casebook`), which also ships its own executing agents and a
plan-before-tests hook. **Where it's installed, it is the authority and this block defers to it**; install
it in the project (`npm i -D test-casebook`, pinned) rather than restating its rules here. What stays ours
is the **default-FAIL contract** and its link to the gate — that has to hold in a repo with no package
installed at all.

## When
After `plan`, before writing the implementation.

## Steps
1. For **every acceptance criterion** in the spec, create a line in `test-results.json`
   initialised to `{ "passes": false }` (the contract starts as a failure).
2. Write the matching test following **test-casebook** (`data-test-*` selectors, exhaustive,
   persona matrix, target coverage ≥ 90%).
3. Run the suite: **everything is red**, that's the expected result at this step.
4. **Read each failure**: red has to mean the assertion failed, not that the test file crashed on a
   broken import or an incomplete mock. A setup error satisfies the contract while proving nothing,
   and it turns green later for reasons unrelated to the behaviour.

Delegate the writing to `dozer` (tests only, never implementation) when you want that separation
enforced rather than relied on.

## Output / checkpoint
`tests_written` + `test-results.json` (every line `{ passes: false }`).

## Guardrails
No test bypassed, hidden or disabled. The default contract is **failure**: nothing is
"passing" until the GATE has proven it. Never loosen an assertion or lower a coverage threshold to
close a gap: a test that can't fail reports safety that isn't there.

## Origin
`test-casebook` (MIT, `techmefr/test-casebook`) for the doctrine, plus market long-running agent patterns
for the default-FAIL contract, rewritten. **Aligned with test-casebook `package.json` 1.0.10** (its
CHANGELOG carries a 1.1.0 section and npm publishes 1.0.4 — three different numbers, so treat the doctrine
as "as fresh as the copy installed in the project", not as a version this block can claim). Re-verify
against the installed package rather than from memory (`skills/source-freshness`). Stamped 2026-08-06.
