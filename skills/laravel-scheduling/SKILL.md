---
name: laravel-scheduling
description: "Use when adding or reviewing a scheduled task in a Laravel app: overlap, running on one server, background runs, environment restrictions, shared constraints and bounding the work inside the task."
---

# laravel-scheduling

Step 6 of the pipeline (`WORKFLOW.md`). A scheduled task runs unattended, on a clock, possibly on several
servers at once. Extends `skills/laravel-conventions` §7 (commands, schedule timezone) and §8 (jobs).

**Special status.** New block, 🟡: written from the rule files the Laravel team ships for its tooling, never
run on real work in house. Re-read the scheduling page of the installed version before relying on a method.

## When
`Schedule::` definitions (or the console routes file), a new command meant to run on a clock, or a report
that a task ran twice, overlapped, or never ran.

## Steps
1. **Overlap is opt-in protection.** `withoutOverlapping()` stops a second run while the previous holds the
   lock. Its argument is the lock's expiry in minutes, not a task timeout; the default is long, a stale lock
   is cleared with the schedule cache-clear command, and an expiry shorter than the real duration allows the
   overlap it was meant to prevent. The task must still survive being retried and partly done.
2. **Several scheduler nodes mean `onOneServer()`.** Every node must use the same default cache store and
   that store must support atomic locks. A scheduled closure needs a name before `onOneServer()`, especially
   the same closure scheduled with different parameters, or the tasks share a lock identity.
3. **`runInBackground()` for long independent commands**, since due tasks otherwise run one after another and
   a slow one delays the rest. It exists only for `command()` and `exec()` tasks, not closures, and a
   background task needs its own logging and failure monitoring because the scheduler no longer waits on it.
4. **`environments([...])` is an operational guard, not authorisation.** It keeps a billing task out of
   staging; it protects nothing from a user.
5. **Shared constraints go in a group** (frequency, server, timezone), only when tasks genuinely share them.
6. **The scheduler cannot stop a task at a deadline.** Bound the work inside the command or job: finite
   chunks, a deadline checked in the loop, or queue jobs with their own timeouts. Hard termination needs
   process-level control.
7. **A task prints what it did.** An unattended command gives the operator a line per item and a summary
   (`skills/laravel-conventions` §7), so a crash at 03:00 names the item.
8. **Test the command, not the clock.** Run the command directly in a test; keep the schedule line a one-line
   registration so there is nothing in it to test.

## Output / checkpoint
Each new scheduled task states its overlap policy, its single-server behaviour if the app runs on more than one
node, and how its work is bounded. Checked at `review` (8).

## Guardrails
No comments in the code produced. New and changed code only (`skills/code-baseline` §0). A stale-lock
cleanup is an operator action, never part of the task.

## Origin
Rewritten from the `scheduling` rule file of Laravel Boost (`laravel/boost`, MIT, cloned 2026-10-02):
overlap expiry semantics, one-server lock requirements and named closures, background-run restriction,
environment guard, groups, bounded work. Mechanisms only, rewritten in our words.
