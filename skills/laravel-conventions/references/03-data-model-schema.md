# laravel-conventions §3 — Data model and schema

> Section 3 of `skills/laravel-conventions`. Read it when a migration, a column, an enum, a soft delete. The other sections and the guardrails stay in `SKILL.md`.

1. **No DB-level ENUM column.** Use a string column, with a PHP enum as the single source of truth, cast on
   the model, and validated through the framework's enum rule. Five reasons, and the first is the one that
   bites: **every value change is an `ALTER TABLE`** — adding one status to a 50-million-row table is a long
   migration that may lock it. Then: the type is inconsistent across engines (native enum here, a created type
   with its own alter semantics there); the DB constraint and the PHP list are **two sources of truth that will
   drift**; renaming a value becomes a multi-step data-plus-schema-plus-code migration; and a value set that
   depends on the tenant or that an admin can extend is simply impossible.
2. **Don't tune the column length to the longest value**, and **don't skip the cast** — without it the column
   comes back as a raw string and the enum bought nothing. A `CHECK (status IN (...))` constraint is the same
   mistake wearing a lighter costume: same migration friction, same duplication.
3. **A set that changes at runtime isn't an enum at all.** An admin-configurable category, a per-plan status
   list, a feature parameter — those belong in a table, not in code. The test is who changes it: a developer
   with a deploy (enum) or a user at runtime (table). A boolean column beats a two-value enum outright.
4. **An enum with per-case data puts the value on the enum as a method**, not in a `match` scattered across
   callers. A `match` on an enum case returning a rate, a label or a threshold is behaviour that belongs to
   the enum — otherwise the day a case is added, the compiler helps you in one file and not in the other six.
5. **No cascade delete at the database level.** The DB deletes rows behind the ORM's back, so nothing fires
   on the children. What silently stops happening: no audit entry for the deleted child, the child stays in
   the search index, its cache is never invalidated, it stays in the CRM/billing/ERP because no
   `child.deleted` listener ran, the cancellation email is never sent, and denormalised counters on siblings
   stay wrong. None of that fails loudly.
6. **Keep the foreign key, drop only the cascade.** Removing the constraint to dodge the rule is worse — you
   trade silent-wrong-behaviour for silent-orphan-rows.
7. **Cascade through a listener class**, registered explicitly — not a closure in a model hook. A class is
   testable on its own, keeps the model thin, and can be queued when the cascade is heavy. Inside it, stream
   the children (a cursor, or chunk-by-id when you need to dispatch between chunks); reading the relation as a
   property loads every child row into memory first, which is exactly the case you were worried about.
8. **Never both.** A DB cascade *and* a listener means the listener deletes children the DB has already
   removed, and the same domain must not mix the two strategies per parent/child pair.
9. **Debugging tip worth its own line: when a lifecycle listener "isn't firing", check the parent's foreign
   key for a cascade first.** That's the most common root cause, and it looks like a broken listener.
10. **Where a DB cascade is genuinely fine**: a pure pivot table with no columns and no business meaning; a
    deliberate data-destruction purge at scale, where firing per-row notifications is the thing you don't
    want; and an append-only log table whose only consumer is its parent's lifecycle.
11. **Decide all of this at the ERD/plan stage, not at code review.** A plan sentence like "delete the user
    and cascade to orders and sessions" has already chosen the mechanism, and a verbal answer to "should
    deleting a company remove its invoices?" is the same decision made without noticing.
12. **Don't factorise two concepts into one table, model or abstraction** just because they look alike or
   share columns today. The shared table is cheap now and is the thing you can't unpick later, when one
   side grows a rule the other can't have. Factorisation is earned by **shared meaning and shared
   change** — the two play the same role in the domain and will evolve together — never by shared *shape*
   (similar columns right now) or shared *screen* (a designer drew them on one page). A mockup listing two
   kinds of thing in one table is a layout decision, and reading it as a schema decision is the most common
   way this one gets made.
13. Every model using soft deletes also carries a **pruning policy** with a retention window. Soft deletes
   without pruning is an unbounded table that silently becomes the biggest one in the database.
14. **Pruning is deleting, and a sweep fires the same per-row events as a delete.** A mass-prune trait,
   event suppression, a quiet delete, a table truncate and a hand-rolled `DELETE … WHERE created_at <`
   cron are the same bypass as point 5's database cascade arriving from the other direction: the rows
   leave and nothing downstream hears. "This data is never deleted, only pruned" is a contradiction — if a
   row can be purged after eighteen months then it is deletable, and the retention window only says when.
   A summary event carrying a class name and a count is not a substitute, because nothing can audit,
   archive, re-index or sync from a number: it says how many rows vanished, never which. Where the volume
   genuinely makes per-row events untenable, that is point 10's deliberate purge — an explicit decision
   with the lost listeners named, not a trait chosen to keep the log quiet.
15. Column defaults: prefer the application-side default, visible at the call site and testable without a
    database.
16. **A generated column (`virtualAs`/`storedAs`) is for a value that has to be filtered, sorted or
    indexed by the database, never for one only PHP ever reads.** An accessor already covers the second
    case, computed on read and free to change without a migration; the generated column exists specifically
    because an accessor's result cannot appear in a `WHERE`, an `ORDER BY` or an index, so reaching for one
    on a value nothing ever queries by adds a schema-migration cost point 1 already warns about, for a
    feature the code never uses.
17. **A custom cast class (`implements CastsAttributes`) is for a transformation the built-in casts don't cover**
    — a money value stored as an integer of cents and read as a value object, a JSON blob decoded into a typed
    DTO, an encrypted field decoded on read. Reaching for one to wrap a value the built-in `decimal`, `boolean`
    or `array` cast already produces is an indirection with nothing behind it: the reader has to open the cast
    class to learn what a native cast name would already have told them.
18. **`Attribute::make(get: ..., set: ...)` replaces the accessor/mutator pair, and it's one declaration instead
    of two methods that drift.** A `getNameAttribute()`/`setNameAttribute()` pair can be edited on one side and
    not the other — the combined `Attribute` return value keeps get and set next to each other, and marking it
    `->shouldCache()` is the explicit opt-in for an accessor expensive enough to need it, rather than every
    accessor silently re-running on every access.
19. **A composite index is ordered for the queries that use it, not for the column order in the migration.** An
    index on `(tenant_id, status)` serves a filter on `tenant_id` alone and on both columns together, but not a
    filter on `status` alone — the leftmost-prefix rule, not intuition about which columns "belong together",
    decides the order. A unique constraint spanning several columns is the same index doing double duty as a
    business rule, and it belongs in the schema precisely because a uniqueness check in PHP loses the race
    point 4.11 already describes for two writes that must both land.
20. **A foreign key's `onDelete` action is a decision about the child's fate, not a default to leave alone.**
    `cascade` is point 5's forbidden default; `restrict` (the safer default) blocks the parent's delete until the
    child is handled explicitly; `set null` silently detaches the child from a parent that no longer exists,
    which is only correct when "orphaned" is a valid, expected state for that child — picking one without asking
    which state the child should be in after the parent is gone is the same decision skipped that point 11
    already flags for cascade itself.
21. **A JSON column is queryable through `->` path operators, but it is not indexed like a real column unless a
    generated column is built on top of it (point 16).** A `WHERE json_col->'$.status' = ?` filter table-scans
    every row past a small table, silently, because nothing about the query looks unindexed at the code level —
    a value filtered or sorted often enough to matter belongs promoted to its own column, and the JSON column
    stays for data that is genuinely read as a document and never filtered on individually.
22. **`foreignId()->constrained()` is the shorthand and the constraint is not implied by the column alone.**
    `foreignId('user_id')` only creates an unsigned big-integer column shaped like a foreign key; without the
    chained `constrained()` (or an explicit `foreign()`) nothing at the database level stops it pointing at a
    row that no longer exists, and the column reads as a relationship in the migration while behaving as a
    plain integer in the schema. Point 20's `onDelete` decision only exists once this chain is complete.
    [Laravel migrations docs, laravel.com/docs/12.x/migrations, read 2026-09-10.]
23. **Renaming a table needs its foreign keys named first, or the rename detaches them.** Laravel names a
    constraint from the table and column at creation time by convention; renaming the table does not rename
    the constraint to match, so a later migration hunting for "the foreign key on this table" by the old
    convention finds nothing, and a rollback that drops constraints by their expected name silently no-ops.
    Give a foreign key an explicit name in the migration that creates it, and a rename stays a rename instead
    of an accidental un-linking. [Laravel migrations docs, laravel.com/docs/12.x/migrations, read 2026-09-10.]
24. **`upsert()` is one round trip for "insert the new ones, update the changed ones," and it still needs a
    real unique or primary key to decide which rows collide.** Its second argument names the columns Laravel
    checks for an existing match, and its third names which columns to update on a match — passed a column
    with no unique constraint behind it, the database has no way to detect the collision and every call
    inserts again, which reads as `upsert()` "not updating" when the real fault is the missing constraint
    point 19 already covers. [Laravel query builder docs, laravel.com/docs/12.x/queries, read 2026-09-10.]
25. **A composite primary key needs `$primaryKey` and `$incrementing` set explicitly on the model, because
    Eloquent's default assumes a single auto-incrementing `id`.** A pivot-shaped table promoted to a real
    model with a `(parent_id, child_id)` primary key still saves through `save()`/`update()` looking up by
    the model's *assumed* `id` column unless both are overridden — the model appears to work until the first
    update targets the wrong row, or every row, because the `WHERE` clause it builds silently used the wrong
    key.
26. **A column that is a foreign key is not automatically a good index for every filter on that table.** The
    constraint guarantees referential integrity; it does not by itself make `(tenant_id, status)` — point
    19's example — exist unless that composite is declared separately. A schema with foreign keys everywhere
    and no composite indexes reads as "indexed" at a glance and still table-scans every filtered list query
    that touches more than the key column alone.
27. **A migration that back-fills existing rows before adding a `NOT NULL` constraint has an ordering
    dependency the migration file itself has to enforce, not the deploy pipeline.** Adding the column
    nullable, populating every existing row, then a second migration tightening it to `NOT NULL` is three
    steps that must run in that order on every environment including one already carrying production data —
    collapsing them into one migration that adds a `NOT NULL` column with no default fails outright on a
    populated table, which is the difference between this working in CI (empty database) and failing in
    staging (real one).
28. **A `timestamp` column that must survive a server timezone change is stored as UTC and converted at the
    edges, not stored in local time because that's what the reads use.** Casting a datetime column through
    Carbon already normalises reads to the application's configured timezone; storing local time in the
    column instead removes the one property that makes cross-timezone comparison and DST correctness possible
    at the database level, and the bug it produces — an hour off, once or twice a year — is exactly the kind
    that a project without stored UTC discovers on the day clocks change rather than in review.
29. **`HasUuids`/`HasUlids` change the primary key's *generation strategy*, and that choice has an index-locality
    consequence an autoincrementing id never raised.** A UUID v4 is random, so each insert lands at an
    arbitrary point in the primary key's index rather than at the end, fragmenting it on a large,
    high-write table; a ULID is time-ordered like the id it replaces, keeping inserts append-like — the
    same "ordered for the queries that use it" reasoning point 19 applies to a composite index applies here
    to the primary key itself, and it is the reason to default to ULIDs unless the id must be
    unguessable *and* unordered.
30. **A polymorphic relation's `*_type` column should store a short alias from an explicit morph map, not
    the model's fully-qualified class name.** `Relation::enforceMorphMap([...])` in a service provider is
    what makes a later namespace move — a model relocated into an OSDD package per `skills/laravel-conventions`
    §10 point 5 — safe: every row already written keeps resolving through the map, where a stored FQCN
    silently orphans every polymorphic row the moment the class it names no longer exists at that path.
31. **A model's date attributes default to *mutable* Carbon instances, which a caller can change in place
    without meaning to.** Casting to `immutable_datetime` (or enabling immutable dates application-wide)
    means a method that receives `$invoice->due_at` and calls `->addDays(3)` on it for a local calculation
    gets a new instance back instead of silently mutating the one every other reader of that model still
    holds a reference to in the same request — the object-identity twin of the UTC-storage discipline point
    28 already asks for on the way the value is read.
32. **A spatial or geography column type depends on a database extension that has to be enabled per
    environment, and the migration itself does not enable it.** A `point`/`geometry` column created against
    a database where PostGIS (or the engine's equivalent) is already on succeeds locally and in any
    long-lived environment that was set up once by hand, then fails the first time it runs against a fresh
    one — a new CI database, a new developer's machine — because nothing in the migration file itself
    provisioned the extension it depends on.
33. **`Model::preventLazyLoading()` and `preventSilentlyDiscardingAttributes()`, turned on outside
    production, convert two silent defects into loud exceptions during development.** The first throws the
    moment an unloaded relationship is lazy-loaded, catching the N+1 point 21 of §1 asks to be eager-loaded
    at the query site before a profiler ever has to find it; the second throws when a mass-assigned value
    lands on a column absent from `$fillable`, catching the over-broad request point 6 of §2 warns about at
    write time instead of it silently being dropped and the caller never told.
34. **`DB::transaction(callback, $attempts)`'s second argument retries the whole closure on a deadlock**,
    which is the framework's own answer to a deadlock a high-concurrency write path will eventually hit —
    reaching for a hand-written `try { ... } catch (QueryException $e) { if (deadlock) retry(); }` loop
    around the same closure duplicates what the parameter already does, and unlike the built-in version it
    has to get idempotency and the retry count right on its own, the same distinction `skills/laravel-conventions`
    §11 point 10 draws for a retried job.
35. **`foreignIdFor(Model::class)` picks the column type from the referenced model's own key type, which a
    hand-written `foreignId()` call has to get right by hand instead.** A model using `HasUlids` or a
    non-default key type produces a `CHAR(26)`/`CHAR(36)` column through `foreignIdFor()`; the same relation
    written as a plain `$table->foreignId('parent_id')` always emits `UNSIGNED BIGINT` regardless of what the
    parent's primary key actually is, which is silently wrong the moment point 29's ULID choice is made on
    the parent after the child migration was already written from a copy-pasted `foreignId()` line.
    [Laravel migrations documentation, laravel.com/docs/12.x/migrations, read 2026-09-10.]
36. **A unique index that includes a soft-deleted row is enforcing uniqueness against rows the application
    already treats as gone.** `SoftDeletes` leaves the row in the table with `deleted_at` set, so a plain
    unique constraint on `email` still blocks a new signup from reusing an address that belongs to a
    soft-deleted account — the fix is a composite unique index including `deleted_at` (or a partial/filtered
    unique index where the engine supports one), scoped to "unique among the live rows," which is the same
    "the DB enforces what the app actually means" reasoning point 19 already applies to a composite index's
    column order, applied here to what counts as a duplicate in the first place.
37. **SQLite does not enforce foreign key constraints unless a pragma turns them on for the connection, which
    makes a constraint violation that fails loudly in MySQL or Postgres pass silently in a SQLite test
    suite.** `PRAGMA foreign_keys = ON` has to be set per connection — Laravel's own SQLite driver config
    exposes a `foreign_key_constraints` option for exactly this — and a project that runs its test suite
    against SQLite without it is verifying point 22's `constrained()` chain compiles, never that it actually
    rejects an orphaned insert, which is the one thing the constraint exists to do. [Laravel database
    configuration documentation, laravel.com/docs/12.x/database, read 2026-09-10.]
38. **`php artisan schema:dump` squashes a project's full migration history into one SQL file, and a
    project that adopts it stops running the squashed migrations' `up()` methods on a fresh install.** The
    dump plus any migration created after it is what actually runs from then on; a data-only backfill written
    as a step inside an old migration's `up()` — rather than a dedicated seeder or a one-off command — is
    silently skipped for every environment provisioned after the squash, which is a second reason (beside
    point 27's ordering rule) a schema change and a data backfill are kept as separate, explicitly-run steps
    rather than bundled into one migration file. [Laravel migrations documentation,
    laravel.com/docs/12.x/migrations, read 2026-09-10.]
39. **`Model::chunkById()`/`lazyById()` page through a table by its primary key rather than by `OFFSET`, which
    is the version of point 7's "stream, don't load into memory" that stays correct while the table is being
    written to during the same backfill.** An `OFFSET`-based `chunk()` re-reads a shifting window if a row
    already visited is deleted mid-run — the next page's offset now points past a row it never saw — silently
    skipping or double-processing rows on a large table under concurrent writes; `chunkById()` anchors each
    page to "the last id seen," which is unaffected by rows being removed behind it.
40. **A check constraint (`$table->check(...)`) enforces a row-level invariant the database itself refuses to
    violate, which is a stronger guarantee than the same rule written only as a Laravel validation rule.**
    Point 1 already bans a DB-level enum for a value that changes with a deploy; a check constraint is the
    different case — a rule that is not a value set but a relationship between columns on the same row (an
    end date after a start date, a discount that cannot exceed the price) — where validation alone only
    protects rows written through this one application, and a second writer (a script, another service
    sharing the database) can still insert a row that breaks the rule unless the database itself refuses it.
