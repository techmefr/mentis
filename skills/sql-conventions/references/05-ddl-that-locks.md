# § 5 — DDL that locks

> Section 5 of `skills/sql-conventions`. Read it when an `ALTER`, an index build or a new constraint is
> written against a table that is in use. This is the statement-level half; the deployment-order half (two
> versions of the code on one schema, backfills, the way back) is `skills/devops-conventions` §6, and this
> file does not repeat it.

1. **Find out which lock the statement takes before you run it.** On PostgreSQL an `ALTER TABLE` takes the
   strongest table lock unless its form is documented otherwise, and when several subcommands are combined the
   strictest one applies. That lock blocks reads and writes for as long as it is held, and everything queued
   behind it waits too. The lock level of each form is in the manual's `ALTER TABLE` page; read it for the form
   you use, do not infer it from "it is only a small change".
2. **Set a lock timeout on the session that runs the migration, and retry.** A statement that needs a strong
   lock waits for every older transaction touching the table, and while it waits it blocks the new ones. A
   lock-timeout setting makes the statement give up instead of freezing the table's traffic; the migration
   then retries later, ideally with a short pause and some randomness between attempts. Scope the setting to
   the migration (the session or the transaction), never the server-wide file, where it would also hit
   ordinary sessions. Run migrations as a role that has these timeouts and that the application's role does not
   share.
3. **Build indexes without blocking writes.** On PostgreSQL a plain index build blocks writes for its whole
   duration; the concurrent form does not, at the price of two table scans, a wait for older transactions, and
   more total work. It cannot run inside a transaction block, so its migration file holds that statement alone.
   If it fails (a deadlock, a uniqueness violation) it leaves an index marked invalid that is ignored by
   queries yet still costs on every write: drop it and retry, or rebuild it concurrently. On MySQL/InnoDB, state
   the algorithm and lock in the statement (§5.5).
4. **Add constraints in two steps on a live table.** A new foreign key or check constraint normally scans the
   table to verify existing rows while holding a lock. Add it as not-yet-validated (it is enforced for new
   writes at once), then validate in a separate statement, which scans without the strong lock. The not-null
   case follows the same idea on current PostgreSQL versions; confirm on the deployed one. A new foreign key
   also takes a lock on the referenced table, so mind the parent.
5. **On MySQL/InnoDB, ask for the algorithm and the lock you expect.** Writing the `ALGORITHM` and `LOCK`
   clauses makes the statement fail if the operation cannot be done that way, instead of silently falling back
   to a blocking table copy. Even an online change takes a brief exclusive metadata lock at start and end, and
   waits for transactions that hold a metadata lock on the table, so a long transaction blocks it exactly as
   in §5.2. For tables too large or too busy for that, a shadow-table tool does the change with a controlled
   cutover, at the cost of triggers or binary-log requirements.
6. **Know which changes rewrite the table.** On PostgreSQL, adding a column with a constant default is a
   metadata change and fast; adding one with a volatile default (a function called per row), a stored generated
   column or an identity column rewrites the table and its indexes under the strong lock. Changing a column's
   type usually rewrites too. Do these as add-new-column, backfill in batches, switch, drop-old, per
   `devops-conventions` §6.
7. **Order the drops.** Remove the constraints and indexes that depend on a column, then the column; drop the
   code's use of it first. A function replaced with a different argument list is a new overload, not a
   replacement, so drop the old one when you mean to replace it.
8. **PostgreSQL DDL is transactional; use it to test, not to hide risk.** Most schema changes can be run in a
   transaction and rolled back, which makes a rehearsal safe on a copy. It does not make a lock cheaper: the
   lock is held until the transaction ends, so keep the transaction as short as the change.
9. **When the table is not yet serving traffic, the simple forms are correct.** If the migration runs before
   the new version starts and the table has no live readers (a new table, a deploy window), the plain
   statement is fine and the machinery above is unnecessary. State which case you are in; do not apply the live
   case's caution by reflex, and do not apply the empty case's simplicity to a table that is in use.

**Sources:** the PostgreSQL manual (`ALTER TABLE` locks, `NOT VALID` and `VALIDATE CONSTRAINT`, table
rewrites, `CREATE INDEX` and building indexes concurrently, client connection settings for lock timeouts) and
the MySQL manual (InnoDB online DDL: algorithm and lock clauses, metadata locks), read 2026-10-02.
Version-bound: the not-null two-step and the identity-column rewrite note describe the manual read on that date
(PostgreSQL current at the time); confirm on the deployed major version. Points 2 (retry detail), 7 and 9 are
reasoning of ours, as is the claim in point 2 that a waiting strong lock blocks the requests that arrive after
it: the manual documents that queueing for MySQL metadata locks, and for PostgreSQL it is a consequence of
how lock requests are ordered, not a quotation.
