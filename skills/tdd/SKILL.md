---
name: tdd
description: Use during the tests step, before the code, write the tests first (test-casebook doctrine) and turn every acceptance criterion into a contract line that fails by default.
---

# tdd

Step 5 of the pipeline (`WORKFLOW.md`). Tests first, and a **default-FAIL contract** that will
make the GATE (step 7) mechanical.

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
Xefi `test-casebook` + market long-running agent patterns (default-FAIL contract), rewritten.
