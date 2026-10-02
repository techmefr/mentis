# § 6 — Safe schema and data migrations

> Section 6 of `skills/devops-conventions`. Read it when a diff adds or edits a database migration,
> alters a large table, backfills data, or plans a deploy that changes a schema while the old code is
> still running. It is a checklist, and each line is here because skipping it has taken a production
> database down. The expand-and-contract strategy itself is in `skills/deprecation-migration`.

A migration runs once, on the data you cannot see, in the minutes when the application is least able to
absorb a surprise. Everything below is about making it small, reversible while it is cheap to reverse, and
tested where it will actually run.

1. **During a deploy, two versions of the code run against one schema.** Old instances are still serving
   while new ones start, so a schema change has to be compatible with both. A change that is correct for
   the new code and breaks the old is an outage for the length of the rollout. That one constraint is why
   the rest of the list exists.
2. **Split the destructive change from the code that stops needing the thing.** Add the new column or
   table first and ship; move the code to it and ship; stop writing the old one and ship; drop the old one
   in a later release, once nothing reads it and a rollback to the previous version would still work. A
   rename is an add, a copy and a later drop, never a single `RENAME` against live traffic.
3. **A new `NOT NULL` column either has a default or arrives in two steps.** Adding the constraint to a
   table that already holds rows fails or rewrites the table. Add the column as nullable (or with a
   constant default that the engine can store as metadata), backfill (point 7), and only then add the
   constraint, checking first that no null remains.
4. **Know what the engine does for your exact statement, in your exact version.** Some `ALTER` forms
   rewrite the whole table and block writers for as long as it takes; others change metadata and finish at
   once. In MySQL, state the algorithm and lock you require (`ALGORITHM=INPLACE` or `INSTANT`,
   `LOCK=NONE`) so the statement *fails* instead of silently choosing a blocking copy, and read the
   documentation table for the operation on your release. In PostgreSQL, check whether the statement takes
   an exclusive lock and for how long, and set a lock timeout so a migration that cannot get its lock
   gives up instead of queueing behind a long query and blocking everything queued behind it. Do not
   assume that a statement which was instant on the version you tested is instant on the one you run.
5. **Build indexes without blocking writes.** On a large table, create the index with the engine's online
   form: `CREATE INDEX CONCURRENTLY` in PostgreSQL (which cannot run inside a transaction, so the migration
   tool must be told not to wrap it, and which leaves an invalid index behind if it fails, to be dropped
   and retried), or the in-place online algorithm in MySQL. Check the time on a copy of production-sized
   data; an index that takes an hour is an hour of added write load.
6. **Foreign keys and unique constraints validate existing rows, so they can lock and they can fail.** Add
   a foreign key or a check in the form that does not scan under a heavy lock (PostgreSQL's `NOT VALID`,
   followed by a separate validation), clean the offending rows first, and expect a unique constraint to
   fail on the duplicate you did not know about. Find the duplicates with a query before the migration,
   not from its error.
7. **Backfill is data work and runs outside the schema change.** A single statement that updates every row
   holds locks and a transaction for its whole length, bloats the log and the replicas, and cannot be
   interrupted. Do it in batches keyed on the primary key, with a pause between them and a measure of
   replica lag, in a job that can be stopped and restarted from where it left off, idempotent so that a
   second run changes nothing. Write the new value on new writes first (dual write), then backfill the
   history, then verify with a count that the old and new representations agree.
8. **Every migration has a defined way back, written before it runs.** For an additive change, the way back
   is the down step. For a destructive one, there is none: the way back is the backup or the point-in-time
   restore, and the migration states which, and that its restore was practised. A down step that drops a
   column loses what was written to it since the up step; say so rather than letting `down` read as a
   guarantee. Forward-fixing with a new migration is usually safer than running a down step against
   production, which is why point 2 keeps each step small.
9. **Test on a copy of production data, at production size.** A migration that takes a second on a seed
   file can take an hour, or fail on one malformed row, on the real table. Run it against a restored copy,
   record the duration and the locks it took, and run the *old* code's test suite and the new one's against
   the migrated schema, since both will meet it.
10. **One concern per migration, and the migration file is never edited after it has run anywhere
    shared.** Changing an applied file makes the environments disagree about what the schema is, and the
    next deploy applies a state nobody tested. Correct a mistake with a new migration. Generated migrations
    are read before they are run: a generated drop-and-recreate for what you meant as a rename is the
    classic way to lose a column.
11. **Do not run schema changes from application start-up on a fleet.** Several instances racing to
    migrate the same schema deadlock or double-apply. Run migrations as a separate, single, ordered step of
    the release, with the credentials that step needs and the application's runtime account not having
    them (`skills/security-hardening` §3).
12. **Say what the migration does to everything downstream.** Read replicas and their lag, change-data
    capture and search indexes fed from the table, exports, caches keyed on the column, and the reporting
    queries that name it. A dropped column that a nightly export still selects is an incident next morning.
13. **Take a recoverable backup before a destructive step, and confirm it restores.** A backup nobody has
    restored is a hope. For a drop or a type change that discards information, take the snapshot
    immediately before, record where it is, and keep it until the new shape has survived a full cycle of
    the workload.
14. **Treat a data-only change like code.** A one-off statement run by hand against production is a
    migration with no review, no test and no record. Put it in a migration or a versioned script, review
    it, give it a `WHERE` that you have first run as a `SELECT` and counted, and run it in a transaction
    where the engine allows (`skills/devops-conventions` §2.1 and the human checkpoint of the guardrails
    apply to it as to any apply on a shared environment).

**Checks, by reading the migration:** is there any statement that rewrites or locks the table, and is that
stated and accepted; is there a nullable-first path for every new constraint; is the index built online;
is the backfill outside the schema change, batched and resumable; what exactly is the way back; was it run
on production-sized data; do both code versions work against the result.

**Sources:** the documentation of the engine and release in use (MySQL online DDL operations table;
PostgreSQL `ALTER TABLE`, explicit locking and `CREATE INDEX`); the expand-and-contract (parallel change)
refactoring pattern; the 12-factor note on admin processes as one-off runs of the release.
