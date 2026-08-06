---
name: debug
description: Use as soon as a bug, an unexpected test failure or a repeated error shows up during the code step, understand the cause before proposing a fix.
---

# debug

Support block for step 6 (`code`). Find the **root cause**, not the symptom.

## When
During `code` / `/BUILD`, at the first unexpected error or the second identical failure.

## Steps
1. Reproduce reliably (command + minimal input).
2. Isolate: state a single hypothesis, verify it (targeted log/test), before changing it.
3. Fix the **cause**, not the symptom; add/adjust a test that captures the case.
4. Still looping after more than 2 attempts with no progress → `escalate`.

## Output / checkpoint
No checkpoint of its own: resumes `code`.

## Guardrails
No "random" fixes and no retry loops. One hypothesis at a time.

## Origin
Native / internal `systematic-debugging`, rewritten our way.
