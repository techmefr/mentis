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
17. **A project with a database and no ORM still owes points 8 to 11.** The transaction rules are about
    the database, not about the mapper: one entry point that commits or rolls back, a raise being the
    rollback, no transaction held across a network call, and no assumption that a nested block is a
    nested transaction. Everything above point 8 is mapper-shaped and does not apply; those four do, and
    a hand-written data layer is where they are most often absent, because there is no session facade to
    inherit them from.
18. **Hand-written DDL is a schema with no migration history, and that has to be said out loud.** A
    create-if-not-absent script sets up a fresh database correctly and silently never changes an existing
    one, so a column added to the script is present for every new install and missing everywhere the
    software already ran — the same failure as point 15, arriving through the absence of a tool rather
    than through a forgotten file. Either a real migration mechanism exists, or the script records which
    version it produces and the gap is a known one.
19. **Read the database's own defaults rather than assuming them.** Referential integrity that is off
    unless enabled per connection, a type system that accepts what it documents as another type, an
    upsert that needs its conflict target named explicitly: each is a property of the specific engine,
    each is invisible in code that looks correct, and each is what a mapper would have handled. Found by
    dogfooding 2026-09-08 against a hand-written `sqlite3` layer.
20. **A pool without a liveness check hands out dead connections.** `pool_pre_ping` pings a connection on
    checkout and transparently reconnects if it was dropped by the database side or a middlebox — but it
    does not cover a connection that dies mid-transaction, so a long-running unit of work still needs its
    own retry or a bounded transaction lifetime (point 10) rather than relying on the pool alone.
21. **Autogenerate proposes a migration, it does not write one.** A diff-based tool compares the model
    metadata against a reflected schema and is explicit about what it cannot see: a check constraint's own
    expression is never diffed once it exists, so an edited constraint with an unchanged name is silently
    treated as unchanged, and the same is true of some server-side computed defaults and of most
    data-only changes. The generated file is a draft to read, not a commit to trust.
22. **Every constraint the migration tool manages needs a naming convention, or it manages some of them
    silently by accident.** A check constraint or index left to the database's own default name is a
    naming convention of one, invisible until two databases pick different defaults, or until autogenerate
    treats an unnamed constraint as absent from the model side entirely and proposes to drop it.
23. **A migration that reorders on top of another developer's unmerged one produces two branch heads.**
    A linear migration history is an assumption, not a guarantee, once two people add a revision from the
    same parent; the merge step is explicit (a merge revision, not silently picking one), because applying
    either branch alone on top of the other leaves a database that matches neither model.
24. **A bulk write and an ORM write are a deliberate choice, not an implementation detail.** A single
    bulk `UPDATE`/`INSERT` skips the ORM's per-row identity map, event hooks and cascade rules for every
    row it touches — correct for a genuine bulk operation where those hooks would not fire anyway (point 1
    already assumes cascades run through them), wrong the moment the code silently expects row-level hooks
    that a bulk statement never invokes.
25. **A mutable value inside a JSON/JSONB column does not notify the session by being mutated in place.**
    Appending to a list or setting a key on a dict loaded from such a column changes the Python object
    without marking the attribute dirty, so the change is silently absent from the next flush unless the
    column is wrapped in a change-tracking type or the attribute is reassigned wholesale.
26. **An index proposed by autogenerate on a large existing table is still a locking operation (point 14)
    even though the tool wrote it.** Autogenerate does not know which of its proposed operations are cheap
    on the target engine and which one locks a production table for the duration of the build; that
    judgment stays with whoever applies the migration, not with whoever generated it.
