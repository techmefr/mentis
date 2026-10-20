# task-tracker-app-build-pitfalls: origin and source stamps

> Provenance of `skills/task-tracker-app-build-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against one open-source tracker's source code. Never run by us: no application was built and no test was executed.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: applicability gate (no feature means analogy only), one place for the transition table with a writer-count check and from-state guards, repair migrations as evidence.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | Kanboard (`kanboard/kanboard`, commit `ba34221`): `app/Model/TaskPositionModel.php`, `TransitionModel.php`, `TaskStatusModel.php`, `TaskLinkModel.php`, `UserNotificationModel.php`, `UserNotificationFilterModel.php` | MIT: file `LICENSE` read | Dense integer positions rewritten on every move with an id tie-break, transition rows with user, source, destination, time and time spent, close and reopen behaviour and completion time, subtasks closed with the parent, links stored per direction with a unique index and no cycle check found, notification filters and recipient exclusion |

Neighbouring blocks of this repository were read to avoid duplication: `skills/laravel-recognise-state-machine-or-pipeline`,
`skills/crm-app-build-pitfalls` (pipeline statuses and merge), `skills/support-queue-design-pitfalls`,
`skills/laravel-mail-via-notifications`, `skills/data-table-ui-pitfalls`, `skills/filters-search-and-saved-views-pitfalls`
and `skills/csv-xlsx-import-export-pitfalls`. The overlap check found no block that covers building a task or
project tracker. Kanban, calendar and upload screens are written by a sibling lot as UI-component blocks, so
this block covers the data model only and does not describe those screens.

## Verified
1. §1 points 3, 4, 6, 9 and 10 (partly) and §2 point 1 (partly): source 1, as the points now say.

## Corrected
1. §1 point 6 now says that the reference tracker uses dense integers and rewrites the list, so the sparse key is a
   deliberate alternative and not an observed practice; the precision-limit marker is kept.
2. §1 point 9: the cycle check is flagged as not present in the code read.

## Removed
1. **Every numeric threshold, nesting limit, digest window and precision figure.** None is stated; set them by
   policy and test them.
2. **Named tracker products and ordering libraries:** not used.

## Not verified
1. **Still our own guidance:** workflow per project with status categories (§1 point 2), priority and type enumerations
   (point 5), the move operation that changes status and position together (point 7), assignee and watchers
   (point 8), date-only versus instant (point 11), conflict detection on edit (point 12), archive and activity history
   (points 13 and 14), tenants (point 16), and in §2 notification coalescing, reassignment, visibility, roles,
   recurrence, reminders, imports, search, time tracking, build order and v2 regrets.
2. **The sparse-key ordering precision** depends on the database type and was not tested; re-read before relying.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed. Only a few model files of the
   tracker were read, not the whole code base, and its separate documentation was not read.
4. **Framework pointers** (Laravel, Nuxt) are short and were not checked against a current release; re-read
   before relying.

## Related blocks
`skills/laravel-recognise-state-machine-or-pipeline`, `skills/laravel-no-cascade-delete`, `skills/laravel-idempotent-jobs`,
`skills/crm-app-build-pitfalls`, `skills/admin-back-office-pitfalls`.
