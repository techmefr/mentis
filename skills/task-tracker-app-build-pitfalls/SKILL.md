---
name: task-tracker-app-build-pitfalls
description: "Use when a project or task tracker application is designed or built: project, task, subtask and assignee model, statuses as per-project workflows with defined transitions and a category that reports read, manual ordering that survives concurrent drags, dependencies without cycles, assignment and watchers, due dates and time zones, comments and activity history, notification volume and digests, archive versus delete, and what to split first and what gets regretted at v2. Data model only; board, calendar and upload screens are separate blocks."
---

# task-tracker-app-build-pitfalls

A defensive block for building the application that tracks work, not for running projects with it. A tracker
built in a hurry fails in familiar ways: every team wants its own statuses and reports break, a reordered column
is overwritten by the next drag, a dependency loop freezes two tasks forever, a reassigned task keeps notifying
its old owner, and a busy project sends forty emails an hour until everyone mutes them. The content is craft
knowledge with no external source read (see `references/origin.md`). Board, calendar and file-upload screens are
UI components covered by their own blocks; this block covers the data behind them. State-machine design is in
`skills/laravel-recognise-state-machine-or-pipeline`, tenant boundaries in `skills/laravel-tenant-context-by-default`,
roles in `skills/laravel-permissions-not-roles`, notifications in `skills/laravel-mail-via-notifications`, tables
and filters in `skills/data-table-ui-pitfalls` and `skills/filters-search-and-saved-views-pitfalls`, stored
files in `skills/document-file-management-pitfalls`, audit of staff actions in `skills/admin-back-office-pitfalls`.

## When
- A new task tracker, issue board, to-do app or project module is specified or its schema is drafted.
- An existing tool gains custom statuses, drag ordering, dependencies, recurring tasks or notifications.
- A feature touches assignment, due dates, ordering or deletion of tasks.

## Steps

**Read the part you need before the schema or the migration is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Model, workflows, ordering, dependencies, assignment, dates, history | a schema or a write path is designed | [`01-model-workflows-and-ordering.md`](./references/01-model-workflows-and-ordering.md) |
| 2 | Notifications, roles and visibility, recurrence, integrations, split order, v2 regrets, framework pointers | notifications, permissions, an import or the first release are planned | [`02-notifications-roles-and-v2.md`](./references/02-notifications-roles-and-v2.md) |

## Output / checkpoint
Before building: the entity list with an owner for each, the workflow per project with status categories and
allowed transitions, the ordering scheme and its conflict behaviour, the dependency rules (cycle check, what a
blocked task may do), the assignment and watcher rules, and the notification matrix by event and recipient.
Evidence is a test that an invalid transition is refused, two concurrent reorders that both survive, a cycle
attempt that is rejected, a reassignment that moves notifications, and a test that a user outside a project
cannot read its tasks through the list, the search and the notification link. Nothing here was run by us.

## Guardrails
- Never let a status be free text, and never let the reports read the status label; map each status to a fixed
  category (§1, point 2).
- Never store position as a dense integer rewritten for every row on each drag; use a sparse key and rebalance
  rarely (§1, point 6).
- Never accept a dependency edge without a cycle check in the same transaction (§1, point 9).
- Never overwrite a task edit silently when two people save; detect the conflict (§1, point 12).
- Never hard-delete a task that has history; archive it (§1, point 13, and `skills/laravel-no-cascade-delete`).
- Never notify per field change; coalesce into one event or a digest (§2, point 2).
- Never filter visibility in the screen only; enforce it in the query, the search index and the notification
  link (§2, point 4).
- Never store due dates without deciding date-only versus instant and the time zone rule (§1, point 11).

## Origin
Written from craft knowledge of building task and project trackers; no open-source tracker documentation was
read, so no source is credited and no text was taken. See [`references/origin.md`](./references/origin.md).
🟡: never run by us.
