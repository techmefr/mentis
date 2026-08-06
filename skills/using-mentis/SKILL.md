---
name: using-mentis
description: Use when starting any task in a Xefi project, establishes the mentis pipeline (task → brainstorm → spec → archi → plan → TDD → code → review → MR → merge → finish) and how the skills plug into starfleet.
---

# using-mentis

Entry point of the Xefi method layer. To be read at the start of every task.

## The rule

**Before any action** (including a clarifying question or exploring the repo), identify the
mentis skill that applies and invoke it. Announce "I'm using [skill] for [goal]" then follow
it. If a checklist exists, one todo per item.

## The pipeline (order)

Every step writes its checkpoint in starfleet (`update_checkpoint`). All blocks follow the
**single template** (`mentis/CONVENTIONS.md`) and are rewritten our way:

1. **start-feature**: creates the isolated worktree (starfleet `create_task` + `launch_worktree`).
2. **brainstorm**: explore the intent before any code.
3. **spec**: lock down scope + out-of-scope; `CONTEXT.md` + ADR → `spec_done`.
4. **archi**: target architecture via graphify (anti-duplication), written (`set_arch_node`) → `arch_done`.
5. **plan**: break into atomic tasks → `plan_done`.
6. **tdd**: tests first (**test-casebook**) + `{passes:false}` contract → `tests_written`.
7. **code**: build in increments (`debug` in support) → `build_done`.
8. **gate**: mechanical lock: mandatory evidence + clean-context evaluator → `verified`.
9. **review**: 2 parallel axes (Standards + Spec) + Xefi agents + `/code-review`/`/security-review`.
10. **simplify**: quality pass at identical behaviour → `simplified`.
11. **ship**: push + **draft** MR (dev + 2 colleagues) → `mr_draft_pushed`, `awaiting_human`. **The agent stops.**
12. **finish**: after the human merge: `finish_task` (server, worktree, integration base).

## The seam with starfleet

A mentis skill **does not reinvent orchestration**: it calls starfleet's MCP tools
(create_task, launch_worktree, update_checkpoint, set_arch_node, escalate, finish_task) and
lets the dashboard reflect the state. Method ≠ state: mentis decides *what/how*, starfleet
holds *where/state*.

## Guardrails

- The **2 human approvals** and the **merge** are outside agent scope, we stop at the draft MR
  and hand back.
- Blocked and it keeps happening? `escalate` rather than loop.
- "I already know how to do this" ≠ "I followed the skill". Invoke it.
