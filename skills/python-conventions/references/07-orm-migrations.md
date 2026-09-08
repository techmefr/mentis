# python-conventions §7 — ORM and migrations

> Section 7 of `skills/python-conventions`. Read it when a model, a relationship, a query or a migration is written. The other sections and the guardrails stay in `SKILL.md`.

1. **No DB-side cascade delete** (`ondelete="CASCADE"`): the database bypasses the ORM, so delete events and
   registered listeners never fire on child rows. Cascade in the ORM layer, where the hooks live. The
   consequence is not only a missed event: search indexes, audit trails, file cleanup and outbound
   notifications all hang off those hooks, so the rows vanish and everything derived from them does not.
2. **Python-side defaults over server-side defaults**: a Python default is visible at the call site, testable
   without a database, and applies whether the row came from the ORM or a raw insert. A server default is
   also invisible to the in-memory object — the attribute is `None` until the row is reloaded, so code that
   creates and immediately reads it sees a value that is not what the table holds.
3. **No implicit lazy loading in an async ORM**: declare relationships non-loading (or raising) so the caller
   states what it needs. Implicit lazy loading is both a runtime failure in async contexts and the root cause
   of N+1 queries. Configuring the relationship to *raise* is the version that turns a silent performance
   problem into an immediate, local error.
4. A query inside a loop is an N+1: load what you need in one query before iterating. It is invisible in
   development against twenty rows and linear in production, so the same code is fine in review and an
   incident at scale — which is why the shape is the thing to recognise, not the timing.
5. **A relationship accessed after the session closes raises**, and that is the same rule as point 3 seen
   from the caller's end: an object returned out of a request scope is detached, so an attribute that was
   never loaded is unavailable rather than merely slow. Load what the caller needs before handing the object
   over, or hand over a plain data structure instead.
6. **A query returning entities when it needs three columns loads everything.** Selecting the columns is
   both less data over the wire and less to instantiate — and it removes the temptation to touch an
   unloaded relationship on the way past.
7. **Anything unbounded needs a limit.** A query with no cap is fine on today's table and a memory
   exhaustion on next year's, and the version that hurts most is an export or a report: written once, run
   monthly, and never revisited until it takes the process down.
8. Transactions go through one entry point (a single transaction/session facade), with after-commit work
   registered explicitly rather than run inside the transaction and hoped to be atomic with it. A mail, a
   queued job or an outbound call dispatched inside the transaction fires even when the transaction rolls
   back — and a rollback cannot recall an email.
9. **Inside a transaction, a raise is the rollback.** Catching and continuing in there commits the
   half-finished unit of work the transaction existed to prevent, which is the failure that leaves the
   database in a state no code path expects.
10. **A transaction held open across an external call is a lock held for the network's duration.** The rows
    stay locked while a payment provider takes four seconds, so unrelated requests queue behind it and the
    outage looks like a database problem. Do the external work outside, and keep the transaction to the
    writes.
11. **Nested transaction blocks are not nested transactions.** Most stacks join the outer one, so an inner
    "commit" commits nothing and an inner rollback discards the outer work — the behaviour depends on
    whether a savepoint is used, and assuming either without checking is how a partial write survives.
12. **A migration runs against real data, so it is tested that way.** The fresh-install path always passes,
    which proves nothing about the rows already there; a migration that fails halfway on a released version
    is also the hardest thing to recover, because what it needed is what it broke.
13. **A migration adding a non-null column to a populated table needs a default or a backfill**, in that
    order: add nullable, backfill, then constrain. Done in one step it fails on any table that is not empty
    — and if it succeeds in staging, that only means staging has no data.
14. **A schema change on a large table locks it.** An index built without the concurrent option, a column
    type change, a rewrite: each blocks writes for as long as it runs, which on production volume is an
    outage scheduled by whoever wrote the migration. Know which operations are cheap in the specific
    database before assuming.
15. **The model and the migration are one change.** A field added to the model without the migration works
    locally against a database somebody already migrated by hand, and fails everywhere else with a
    missing-column error — and the reverse, a migration with no model change, leaves a column nothing reads.
16. **A migration is reversible or says why it is not.** A destructive step — a dropped column, a
    transformation that loses information — cannot be undone by a downgrade, so the honest version fails
    loudly on the way back rather than pretending to restore something.
