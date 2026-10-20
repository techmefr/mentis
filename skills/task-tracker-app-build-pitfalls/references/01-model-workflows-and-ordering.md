# task-tracker-app-build-pitfalls §1 — Model, workflows, ordering and dependencies

> Part 1 of `skills/task-tracker-app-build-pitfalls`. Read it when a schema or a write path is designed. Craft
> knowledge, no external source read. Each point gives the symptom, the check and the fix.

1. **Minimal model, each entity with one owner.** Workspace or tenant, project (a container with members and a
   workflow), task (a unit of work in one project), subtask (a task with a parent, one level or a bounded
   depth), user, membership (user in project with a role), comment, attachment reference, label. Give each task
   a creator and an optional assignee. Symptom of skipping membership: access is decided by a flag on the user
   and a contractor sees every project.
2. **A workflow per project, a category per status.** Symptom: one team adds "In QA", another "Review", and the
   burndown, the overdue list and the "done this week" report each disagree about what finished. Check: add a
   custom status and run every report. Fix: statuses are rows owned by the project's workflow, each mapped to a
   fixed category (not started, active, done, and optionally cancelled) that all reports read; reports never
   match on label. Renaming a status changes the label, never the id or the category. Deleting a status
   requires moving its open tasks to another status first.
3. **Transitions are defined, not free.** Symptom: a task jumps from "Backlog" to "Done" with no assignee and
   no estimate. Fix: a transition table (from, to, optional guard), checked in one place (see
   `skills/laravel-recognise-state-machine-or-pipeline`), with guards that are data checks (assignee present,
   blockers done, required field filled), and a default of "any to any" only where the team wants it, stated
   openly. Stage history is rows (task, from, to, actor, time), never an overwritten column.
    Check on an existing code base: grep every statement that updates the status column, in application code and in
    migrations, and count the writers. More than one is the symptom: each writer must go through the one transition
    function, and each update must carry a from-state guard (update only where the current status is an allowed
    source), otherwise a repeat call re-runs side effects or overwrites a later state. Fix: route every writer
    through that function and add the guard.
    A repair migration (an update that moves rows stuck in a status) in the history is evidence of missing
    transitions or missing guards: read it, name the path that stranded them, and close the path before adding
    another repair. Repair migrations are one-off and idempotent, never the mechanism.
4. **Done and reopen are explicit.** Symptom: a reopened task keeps its old completion date and shows as both
   done and active. Fix: set completion time on entry to a done category, clear it on reopen while keeping the
   history row, and let reports use the history for "completed in period".
5. **Priority and type are small enumerations with stable ids.** Same rule as statuses: a renamed label must not
   rewrite history, and sorting by priority sorts by an order column, not alphabetically.
6. **Manual ordering uses a sparse key.** Symptom: dragging a card rewrites the position of every row below it,
   two users dragging at once overwrite each other, and a long list makes each drag slow. Check: reorder the
   same column from two sessions at once and reload. Fix: store a sortable key between neighbours (a fractional
   number, or a short lexicographic string) so a move writes one row; compute the new key from the two
   neighbours the client saw; when keys get too close or too long, rebalance that list in one background
   job; resolve ties by id so order is deterministic. Order is per list (project backlog, a status column, a
   saved view), so keep the list identity in the key's scope. Re-read before relying: the exact precision limit
   depends on the database type; test it.
7. **A move changes status and position together.** Symptom: a card dropped into another column keeps its old
   status until a refresh, or lands but is refused later. Fix: one server operation takes target status and
   neighbours, validates the transition (point 3), writes status, position and history in one transaction, and
   returns the authoritative state for the client to reconcile. The drag screen itself is covered by the board
   UI block, not here.
8. **Assignment has one assignee and many watchers, or an explicit multi-assignee decision.** Symptom: two
   assignees each assume the other is doing it, or reports count a task twice. Fix: decide it at the start;
   default to one accountable assignee plus watchers or collaborators as a separate relation; a reassignment
   is a history row and moves the task from one person's workload to another's in the same transaction; an
   unassigned task is a valid, visible state with a queue, not an error.
9. **Dependencies are a graph with a cycle check.** Symptom: A blocks B and B blocks A, and neither can ever
   start; or a parent is done while a child is not. Check: try to create a loop through three tasks. Fix: a
   dependency table (blocker, blocked, type), a uniqueness rule, a self-edge ban, a cycle check on insert that
   walks the existing edges in the same transaction (lock the affected rows to stop two concurrent inserts
   forming a loop), and a clear rule for what a blocked task may do (may start but cannot close, or may not
   start). Cross-project edges need the permission of both projects. Deleting or archiving a blocker releases
   its dependants with a history row, not silently.
10. **Parent and child completion has a rule.** Symptom: a parent shows 100 percent while a subtask is open, or
    the reverse. Fix: choose one rule (parent derived from children, or parent closed manually with a guard that
    children are done), store derived progress as a computed value rather than a second editable field, and
    cap nesting depth.
11. **Dates: decide date-only versus instant, and the time zone.** Symptom: a task due "Friday" shows overdue
    on Thursday evening for a colleague in another zone, or a daylight-saving change moves a reminder. Fix: a
    date-only due date is stored as a date with no zone and compared in the viewer's or project's zone by a
    stated rule; an instant (a meeting, a deadline at an hour) is stored in UTC with the zone it was meant in;
    "overdue" uses one function reused by screen, filter and notification (see
    `skills/locale-value-formatting-pitfalls`).
12. **Edits detect conflicts.** Symptom: two people edit the description and the later save erases the earlier
    one without a word. Fix: a version number or updated-at token sent back with the save; on mismatch, refuse
    and show the newer state with a merge choice; comments are inserts, not edits of a shared field.
13. **Archive is the default; delete is a controlled job.** Symptom: deleting a project removes tasks, comments
    and time history, and totals shift retroactively. Fix: an archived timestamp hidden by default and
    restorable, restrict foreign keys instead of cascading (see `skills/laravel-no-cascade-delete`), and a
    separate audited purge for erasure that keeps non-personal work records. Soft delete alone is not erasure.
    What law requires is for the data-protection owner, not legal advice.
14. **Activity history is append-only.** Symptom: nobody can say who moved the task or changed the date. Fix:
    history rows for status, assignee, dates, priority and parent changes with actor, old and new value and
    time; comments are separate and can be edited with an "edited" marker and a kept previous version when the
    team needs it. Staff-level audit is in `skills/admin-back-office-pitfalls`.
15. **Status history records from and to.** Symptom: a log line says "validated" but not from which state, so a stuck item cannot be traced. Fix: one history row per transition with from, to, actor and time (point 14), written by the same function as point 3.
16. **Every row belongs to a tenant from the first migration.** Tenant column on all tables including join
    tables, one default scope (see `skills/laravel-tenant-context-by-default`), and a test per path (list,
    search, notification link, attachment URL).
