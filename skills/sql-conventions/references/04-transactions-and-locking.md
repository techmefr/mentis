# § 4 — Transactions, isolation, and locking

> Section 4 of `skills/sql-conventions`. Read it when two writers can reach the same rows, when a job claims
> work from a table, or when a deadlock or lock timeout shows up. Concurrency bugs pass every single-user
> test; the habit that protects you is to ask, for each read-then-write, what happens when a second copy of
> the code runs at the same moment.

1. **Know the default isolation level of the engine you are on.** PostgreSQL defaults to read committed: each
   statement sees what was committed before it began, so two statements in one transaction can see different
   data. MySQL/InnoDB defaults to repeatable read: a snapshot taken at the first read. Reasoning written for
   one engine's default silently breaks on the other, which is why step zero of the router fixes the engine first.
2. **A read followed by a write on the strength of that read is a race.** "Check there is room, then insert"
   fails when two transactions both see room. Fix it at the level where it can be made true: a constraint
   (§2.7), a single conditional statement that checks and writes at once, a lock on the row that arbitrates
   (§4.4), or a stricter isolation level with a retry (§4.3).
3. **The stricter levels require a retry loop.** On PostgreSQL, repeatable read and serializable can abort a
   transaction with a serialization failure; the manual says the application must be ready to retry the whole
   transaction from the start. The same holds for a deadlock victim on MySQL. A retry re-runs the entire unit,
   including the reads, and is safe only if the transaction has no side effect outside the database (a mail
   sent, a call made) or those effects are made idempotent (`skills/background-jobs-conventions`).
4. **Take the narrowest lock that serialises the conflict.** Locking the one parent row with `SELECT ... FOR
   UPDATE` serialises all writers of that aggregate without locking tables. Use the lock only when a
   constraint cannot express the rule, keep it for as short a time as possible, and do not mix locking and
   non-locking reads of the same data in one transaction on a snapshot-based engine, because they can observe
   different states.
5. **Claim work from a table with the skip-locked clause.** A worker that selects a batch of rows `FOR UPDATE
   SKIP LOCKED` takes rows nobody else holds, so parallel workers do not block each other. The manual notes
   the result is an inconsistent view of the data, which is exactly right for a queue and wrong for any report.
   The claim and the status change commit in the same transaction, and the job is still processed
   idempotently, because a worker can die after the work and before the commit.
6. **Avoid deadlocks by ordering, and expect the rest.** Deadlocks come from two transactions taking the same
   locks in opposite order, and from statements without a usable index that lock far more rows than they
   change. Access rows in one consistent order (by primary key) in every code path, keep transactions short,
   and index the columns of every `UPDATE` and `DELETE` predicate. A deadlock is detected and one transaction
   is rolled back; treat it as a normal event that costs a retry (§4.3), not as a bug to eliminate to zero.
7. **Keep transactions short and do no waiting inside them.** No network call, no file operation, no user
   interaction between `BEGIN` and `COMMIT`. A long transaction holds its locks, and on PostgreSQL an idle open
   transaction also blocks the cleanup of dead rows, which grows tables. Set the idle-in-transaction timeout so
   a client that crashes mid-transaction is disconnected, and set a statement timeout for the role that serves
   requests; do not set either in the server-wide file where it also hits maintenance sessions.
8. **A connection pooler changes what session state exists.** In transaction-pooling mode the connection a
   client gets changes between transactions, so session-level state does not survive: setting a session
   variable, listening for notifications, preparing a statement by hand, holding a session-level advisory lock
   and keeping preserved temp tables all fail or behave wrongly, per the pooler's own feature table. Use
   transaction-scoped forms (`SET LOCAL`, transaction-level advisory locks), or a session-pooling mode for the
   code that needs the rest, and test through the pooler that production uses.
9. **Advisory locks are application-defined and outside the transaction's rollback in their session form.** A
   session-level advisory lock taken in a transaction that rolls back is still held. Prefer the
   transaction-level form, and take care with a lock call inside a query that has a `LIMIT`, since the number
   of locks taken depends on evaluation order.
10. **Isolation is not durability and not idempotency.** A committed transaction can still be applied twice
    if the caller retries after a lost acknowledgement; give the operation a natural idempotency key enforced
    by a unique constraint (`skills/laravel-post-may-run-twice` for the HTTP-side statement).

**Sources:** the PostgreSQL manual (transaction isolation, explicit locking and deadlocks, SELECT locking
clauses including SKIP LOCKED, client connection defaults for the timeouts), the MySQL manual (InnoDB
isolation levels) and the vendor's published MySQL guidance (deadlocks, gap locks, retry), and the connection
pooler's documented feature table by pooling mode, read 2026-10-02. Points 2, 4, 7 (first half) and 10 are
reasoning of ours.
