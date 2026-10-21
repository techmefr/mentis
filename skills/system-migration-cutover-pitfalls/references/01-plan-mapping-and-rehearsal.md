# system-migration-cutover-pitfalls §1 — Plan, mapping and rehearsal

> Part 1 of `skills/system-migration-cutover-pitfalls`. Read it before the first load and before every rehearsal.
> This part is our own craft guidance (no source was needed for it); the Debezium facts are in part 2. Every
> sentence is "own guidance", and none was run by us.

1. **Inventory first: what moves, what stays, who reads it.** List each entity with its volume, its owner, the age
   after which it is archived rather than moved, and every consumer of it (reports, integrations, exports,
   scheduled jobs, other systems). Symptom of skipping it: a nightly export that read the old database keeps
   running against a frozen copy for weeks. Fix: the consumer list is a checklist at cutover, one line per
   consumer with a new source and an owner.
2. **A decision for every source field.** The mapping document has one row per source field: target field,
   transformation, rule for empty and unknown values, whether it loses information, and the person who approved
   it. Fields that are deliberately not moved are listed with the reason. Enumerations get an explicit value
   table, and the table says what happens to a value that is in the data but not in the table. Symptom: a status
   that exists in the old system with no equivalent is silently turned into a default and nobody notices.
3. **Identity: keep the old key and map it.** Store the source identifier on every migrated row (or in a mapping
   table) so a load can be rerun without duplicates, a person can find a record by its old number, and external
   references (links in sent emails, ids quoted by customers, third-party systems) can be resolved. Decide what
   happens when one source record becomes two (a split) or two become one (a merge) before loading, because the
   mapping table, not the loader, has to carry it.
4. **The loader is a program, not a script run by hand.** In version control, idempotent (a rerun converges to the
   same state), resumable (a batch fails and the next run continues), batched, and parameterised by a run id.
   Rejected rows go to a quarantine table with the source key, the reason and the run id; a rejected row is never
   skipped without a record. Report counts per entity: read, created, updated, unchanged, quarantined.
5. **Side effects are off during the load.** Importing a row can send an email, fire a webhook, enqueue a job,
   write to a search index, bump a counter or create an audit entry. Switch each of them off for the migration
   path (a flag the loader sets, not a global switch someone forgets to restore), and switch on deliberately
   afterwards what is wanted (a rebuilt search index, recomputed counters). Reset id sequences after a bulk load
   (see `skills/laravel-mysql-to-postgres-pitfalls` §1 point 4).
6. **Profile the source and rehearse on a copy, with the real procedure, timed.** Profiling finds duplicates,
   orphans (a child with no parent), mixed encodings, dates with no time zone, money stored as text or with
   different precision, soft-deleted rows, free-text values in what should be a list. Then run the full procedure
   on a copy of production at least twice: first to fix the loader, then to prove it. Time every step. The
   cutover window comes from the measured duration plus the rollback time, not from the data volume. The copy
   holds real personal data and gets production-grade access control; masking is acceptable only if the
   reconciliation still works on the masked data.
7. **Reconcile on three levels.** Structural: row counts per entity against the source minus the quarantine.
   Numeric: sums of money and quantity columns per period, per tenant, per status (an open-invoice total is a
   good one). Content: a sampled or hashed comparison of rows by source key, including the oldest and newest
   records and the ugly edge cases from the profiling. Add referential checks on the target (no orphans, no
   duplicate natural keys). The thresholds for "matches" are set by the data owner before the run, and the report
   is stored. Symptom of counts only: every table has the right number of rows and half of them have a wrong
   currency.
8. **Design the rollback before the cutover, including its point of no return.** Write what returns to the old
   system if you back out at each step; list data written only in the new system after the switch and how it
   comes back (or that it is lost, and who accepted that). Keep the old system intact and read-only. Rehearse the
   rollback once, with the same timing discipline as the load. After the point of no return the plan is
   roll-forward, and that should be said out loud in the runbook.
9. **Acceptance is the data owner's, not the developer's.** The people who know the records (accounting for the
   ledger, support for the tickets) review sampled records and the reconciliation, and sign. Give them a list of
   known differences (dropped fields, changed formats) so that a difference is not a surprise.
10. **Freeze and communicate.** Decide what is frozen (new records, edits, schema changes, deployments) and for
    how long, tell the people affected, and keep an incident channel and an owner for each runbook step. A
    migration that depends on one person being awake is a plan to fix.
11. **A runbook with go or no-go criteria.** Numbered steps, owner, expected duration, the check after each step,
    and the criterion that stops the cutover. The runbook is rehearsed as written; a step discovered during the real
    run is a defect of the rehearsal.
12. **Small and reversible beats one large move.** If the data can be moved per tenant, per region or per entity
    type, plan it that way; each step then has its own reconciliation and rollback, and the first one teaches
    something cheaply.
