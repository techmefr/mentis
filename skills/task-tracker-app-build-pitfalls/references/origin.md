# task-tracker-app-build-pitfalls: origin and source stamps

> Provenance of `skills/task-tracker-app-build-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: applicability gate (no feature means analogy only), one place for the transition table with a writer-count check and from-state guards, repair migrations as evidence.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of building task and project trackers. No open-source tracker or ordering-library documentation was opened; no LICENSE file was read because no source was used. |

Neighbouring blocks of this repository were read to avoid duplication: `skills/laravel-recognise-state-machine-or-pipeline`,
`skills/crm-app-build-pitfalls` (pipeline statuses and merge), `skills/support-queue-design-pitfalls`,
`skills/laravel-mail-via-notifications`, `skills/data-table-ui-pitfalls`, `skills/filters-search-and-saved-views-pitfalls`
and `skills/csv-xlsx-import-export-pitfalls`. The overlap check found no block that covers building a task or
project tracker. Kanban, calendar and upload screens are written by a sibling lot as UI-component blocks, so
this block covers the data model only and does not describe those screens.

## Removed
1. **Every numeric threshold, nesting limit, digest window and precision figure.** None is stated; set them by
   policy and test them.
2. **Named tracker products and ordering libraries:** not used.

## Not verified
1. **All points are our own guidance** and were not compared with any open-source tracker schema.
2. **The sparse-key ordering precision** depends on the database type and was not tested; re-read before relying.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** (Laravel, Nuxt) are short and were not checked against a current release; re-read
   before relying.

## Related blocks
`skills/laravel-recognise-state-machine-or-pipeline`, `skills/laravel-no-cascade-delete`, `skills/laravel-idempotent-jobs`,
`skills/crm-app-build-pitfalls`, `skills/admin-back-office-pitfalls`.
