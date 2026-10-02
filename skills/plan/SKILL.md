---
name: plan
description: Use when the architecture is set, before writing tests or code, break the feature into atomic testable tasks.
---

# plan

Step 4 of the pipeline (`WORKFLOW.md`). Turn the target architecture into deliverable
increments.

## When
After `archi`, before `tdd`.

## Steps
1. Break into **atomic** increments: each one testable and deliverable independently.
2. Order by dependency (whatever unblocks the rest comes first).
3. Record **one tracked item per increment**, wherever the task's trail lives (a todo list, the ticket, a
   local orchestrator if there is one). The tracking must exist; the tool is not prescribed.
4. **What a step contains**: the minimum that lets the implementer write exactly one reasonable thing.
   A test step has the test name and its assertions with the spec's exact values; a code step has the file,
   the signature and the values the spec pins, and the body only for an algorithm the signature and tests
   do not determine; a verification step has the command and the output that means pass; a reference to
   another task points at that task's interface rather than repeating its code.
5. **Review Focus**: list at most five failure modes or inputs the spec implies but no task's tests
   exercise, most likely first, each pinned to a test in the task that owns the code. An empty list means
   the check was done and found none.
6. **Proportion check**: a plan several times longer than its spec has transcribed the code. Bring it back
   to signatures and assertions. A line that decides nothing ("handle edge cases") is the opposite fault.
7. **A reviewer of a plan adds phases; they never rewrite the original plan.** The author's phases stay as
   written and the added ones are marked as the reviewer's.

## Output / checkpoint
`plan_done` + one tracked item per increment, in dependency order.

## Guardrails
No automatic execution of the whole plan (**no `/build auto`**: see `WORKFLOW.md`, auto-mode
was removed on purpose). The dev validates and moves forward step by step.

## Origin
Native / a market generalist dev skill catalogue (planning-and-task-breakdown), rewritten our
way.

Steps 4 to 6 rewritten from the `writing-plans` skill of `superpowers` (MIT, 6.4.x), read 2026-10-02. Step 7 comes from the cross-model plan-review workflow in `claude-code-best-practice` (MIT), same date.
