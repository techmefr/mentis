---
name: code
description: Use when the build step starts and the tests are written, implement in increments until they pass, one task_item at a time.
---

# code

Step 6 of the pipeline (`WORKFLOW.md`). Build the minimum that makes each test pass.

## When
After `tdd` (red tests written), during `/BUILD`.

## Steps
1. Take **one** `task_item`, write the minimum code that makes its test pass.
2. `toggle_task_item` when the increment is done, commit.
3. Blocked / unexpected error → invoke the **`debug`** block before proposing a fix.
4. Repeat until the `task_items` are exhausted.

## Output / checkpoint
`build_done`.

## Guardrails
**No comments in the code.** **Never** mark a test `passes: true` by hand, the **GATE**
(step 7) decides, on evidence. We don't validate ourselves.

## Origin
Native Claude Code + internal, rewritten.
