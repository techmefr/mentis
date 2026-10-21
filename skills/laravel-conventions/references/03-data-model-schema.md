# laravel-conventions §3 — Data model and schema

> Section 3 of `skills/laravel-conventions`. Read it when a migration, a column, an enum, a soft delete. The other sections and the guardrails stay in `SKILL.md`.

1. **No DB-level ENUM column.** Use a string column, with a PHP enum as the single source of truth, cast on
   the model, and validated through the framework's enum rule. Five reasons, and the first is the one that
   bites: **every value change is an `ALTER TABLE`** — adding one status to a 50-million-row table is a long
   migration that may lock it. Then: the type differs across engines (native enum here, a created type
   with its own alter semantics there); the DB constraint and the PHP list are **two sources of truth that
   will drift**; renaming a value becomes a multi-step data-plus-schema-plus-code migration; and a value
   set that depends on the tenant or that an admin can extend is impossible.
2. **Don't tune the column length to the longest value**, and **don't skip the cast** — without it the column
   comes back as a raw string and the enum bought nothing. A `CHECK (status IN (...))` constraint is the same
   mistake in a lighter costume: same migration friction, same duplication.
3. **A set that changes at runtime isn't an enum at all.** An admin-configurable category, a per-plan status
   list, a feature parameter — those belong in a table, not in code. The test is who changes it: a developer
   with a deploy (enum) or a user at runtime (table). A boolean column beats a two-value enum outright.
4. **An enum with per-case data puts the value on the enum as a method**, not in a `match` scattered across
   callers. A `match` on an enum case returning a rate, a label or a threshold is behaviour that belongs to
   the enum — otherwise the day a case is added, the compiler helps in one file and not in the other six.
5. **No cascade delete at the database level.** The DB deletes rows behind the ORM's back, so nothing fires
   on the children. Silently skipped: the audit entry, search-index removal, cache invalidation, the
   `child.deleted` sync to CRM/billing/ERP, the cancellation email, and denormalised sibling counters.
   Nothing fails loudly.
6. **Keep the foreign key, drop only the cascade.** Removing the constraint to dodge the rule is worse — you
   trade silent-wrong-behaviour for silent-orphan-rows.
7. **Cascade through a listener class**, registered explicitly — not a closure in a model hook. A class is
   testable on its own, keeps the model thin, and can be queued when the cascade is heavy. Inside it, stream
   the children (a cursor, or chunk-by-id when dispatching between chunks); reading the relation as a
   property loads every child row into memory first.
8. **Never both.** A DB cascade *and* a listener means the listener deletes children the DB has already
   removed, and the same domain must not mix the two strategies per parent/child pair.
9. **Debugging tip worth its own line: when a lifecycle listener "isn't firing", check the parent's foreign
   key for a cascade first.** Most common root cause; it looks like a broken listener.
10. **Where a DB cascade is genuinely fine**: a pure pivot table with no columns and no business meaning; a
    deliberate data-destruction purge at scale, where firing per-row notifications is the thing you don't
    want; and an append-only log table whose only consumer is its parent's lifecycle.
11. **Decide all of this at the ERD/plan stage, not at code review.** A plan sentence like "delete the user
    and cascade to orders and sessions" has already chosen the mechanism, as has a verbal answer to "should
    deleting a company remove its invoices?"
12. **Don't factorise two concepts into one table, model or abstraction** just because they look alike or
   share columns today. The shared table is cheap now and can't be unpicked once one side grows a rule the
   other can't have. Factorisation is earned by **shared meaning and shared change** — the two
   play the same role in the domain and will evolve together — never by shared *shape* (similar columns
   now) or shared *screen* (a designer drew them on one page). A mockup listing two kinds of thing in one
   table is a layout decision, not a schema one.
13. Every model using soft deletes also carries a **pruning policy** with a retention window. Soft deletes
   without pruning is an unbounded table that silently becomes the biggest one in the database.
14. **Pruning is deleting, and a sweep fires the same per-row events as a delete.** A mass-prune trait,
   event suppression, a quiet delete, a table truncate and a hand-rolled `DELETE … WHERE created_at <`
   cron are point 5's database cascade from the other direction: the rows leave and nothing downstream
   hears. "This data is never deleted, only pruned" is a contradiction — if a row can be purged after
   eighteen months it is deletable, and the retention window only says when. A summary event with a
   class name and a count is no substitute: nothing can audit, archive, re-index or sync from a number.
   Where volume genuinely makes per-row events untenable, that is point 10's deliberate purge — an
   explicit decision with the lost listeners named, not a trait chosen to keep the log quiet.
15. Column defaults: prefer the application-side default, visible at the call site and testable without a
    database.
16. **A generated column (`virtualAs`/`storedAs`) is for a value that has to be filtered, sorted or
    indexed by the database, never for one only PHP ever reads.** An accessor covers the second case,
    computed on read and free to change without a migration; the generated column exists because an
    accessor's result cannot appear in a `WHERE`, an `ORDER BY` or an index, so one on a value nothing
    queries by adds a schema-migration cost point 1 warns about, for a feature the code never uses.
17. **A custom cast class (`implements CastsAttributes`) is for a transformation the built-in casts don't cover**
    — a money value stored as an integer of cents and read as a value object, a JSON blob decoded into a typed
    DTO, an encrypted field decoded on read. One wrapping a value the built-in `decimal`, `boolean` or
    `array` cast already produces is indirection with nothing behind it.
18. **`Attribute::make(get: ..., set: ...)` replaces the accessor/mutator pair, and it's one declaration instead
    of two methods that drift.** A `getNameAttribute()`/`setNameAttribute()` pair can be edited on one side only — the
    combined `Attribute` keeps them together, and `->shouldCache()` is the explicit opt-in for an
    expensive accessor.
19. **A composite index is ordered for the queries that use it, not for the column order in the migration.** An
    index on `(tenant_id, status)` serves a filter on `tenant_id` alone and on both columns together, but not a
    filter on `status` alone — the leftmost-prefix rule, not which columns "belong together", decides the order. A
    multi-column unique constraint is the same index doing double duty as a business rule, and belongs in
    the schema because a uniqueness check in PHP loses the race §4 point 11 describes.
20. **A foreign key's `onDelete` action is a decision about the child's fate, not a default to leave alone.**
    `cascade` is point 5's forbidden default; `restrict` (the safer default) blocks the parent's delete until the
    child is handled explicitly; `set null` silently detaches the child from a parent that no longer exists,
    correct only when "orphaned" is a valid state for that child — pick one by asking which state the
    child should be in after the parent is gone (point 11).
21. **A JSON column is queryable through `->` path operators, but it is not indexed like a real column unless a
    generated column is built on top of it (point 16).** A `WHERE json_col->'$.status' = ?` filter table-scans
    every row past a small table, silently, because nothing in the code looks unindexed — a value filtered
    or sorted often enough to matter belongs promoted to its own column; the JSON column stays for data
    read as a document and never filtered on individually.
22. **`foreignId()->constrained()` is the shorthand and the constraint is not implied by the column alone.**
    `foreignId('user_id')` only creates an unsigned big-integer column shaped like a foreign key; without the
    chained `constrained()` (or an explicit `foreign()`) nothing at the database level stops it pointing at a
    row that no longer exists — a relationship on paper, a plain integer in the schema. Point 20's
    `onDelete` decision only exists once this chain is complete.
    [Laravel migrations docs, laravel.com/docs/12.x/migrations, read 2026-09-10.]
23. **Name a foreign key explicitly before the table is renamed.** The docs warn that, before renaming a
    table, any foreign key constraint on it should have an explicit name in the migration instead of the
    convention-based name, otherwise the constraint name still refers to the old table name. Give a foreign
    key an explicit name in the migration that creates it, and a rename stays a rename. [Laravel migrations
    docs 12.x, "Renaming Tables With Foreign Keys", read 2026-10-21.]
24. **`upsert()` is one round trip for "insert the new ones, update the changed ones," and it still needs a
    real unique or primary key to decide which rows collide.** Its second argument names the columns that
    identify a row, its third the columns to update on a match; the docs say all databases except SQL Server
    require those columns to carry a primary or unique index, and that MySQL and MariaDB ignore the second
    argument and use the table's own indexes. A column with no unique index behind it reads as `upsert()`
    "not updating" when the fault is the missing constraint of point 19. [Laravel query builder docs 12.x,
    "Upserts", read 2026-10-21.]
25. **Eloquent models support one primary key column, not a composite key.** The 12.x docs describe a single
    `$primaryKey` column, and `$incrementing`/`$keyType` for a key that is not an auto-incrementing integer.
    A pivot-shaped table with a `(parent_id, child_id)` primary key promoted to a model cannot be saved or
    updated through `save()` by that pair; use a pivot model, or the query builder with an explicit `where`
    on both columns (own guidance on the alternatives). [Laravel Eloquent docs 12.x, "Primary Keys",
    read 2026-10-21.]
26. **A column that is a foreign key is not automatically a good index for every filter on that table.** The
    constraint guarantees referential integrity; it does not make `(tenant_id, status)` — point 19's
    example — exist unless that composite is declared separately. A schema with foreign keys everywhere and
    no composite indexes reads as "indexed" and still table-scans every filtered list query touching more
    than the key column.
27. **A migration that back-fills existing rows before adding a `NOT NULL` constraint has an ordering
    dependency the migration file itself has to enforce, not the deploy pipeline.** Adding the column
    nullable, populating every existing row, then a second migration tightening it to `NOT NULL` is three
    steps that must run in that order on every environment including one carrying production data —
    one migration adding a `NOT NULL` column with no default fails on a populated table, the difference
    between working in CI (empty database) and failing in staging.
28. **A `timestamp` column that must survive a server timezone change is stored as UTC and converted at the
    edges, not stored in local time because that's what the reads use.** Casting through Carbon already
    normalises reads to the application's timezone; storing local time removes cross-timezone comparison
    and DST correctness at the database level, and the bug — an hour off, once or twice a year — shows up
    the day clocks change, not in review.
29. **`HasUuids`/`HasUlids` change the primary key's *generation strategy*, and that choice has an index-locality
    consequence an autoincrementing id never raised.** A random UUID (version 4) lands at an arbitrary point
    in the primary key's index; the 12.x `HasUuids` trait generates an ordered UUID by default (the framework
    source calls `Str::uuid7()`), and overriding `newUniqueId()` with a v4 generator, as the Eloquent docs'
    own example does, gives that up. A ULID is also lexicographically sortable. Point 19's "ordered for the
    queries that use it" applied to the primary key: keep the ordered default unless the id must be unordered.
    [Laravel Eloquent docs 12.x, "UUID and ULID Keys"; framework source `HasUuids.php` (12.x), read 2026-10-21.]
30. **A polymorphic relation's `*_type` column should store a short alias from an explicit morph map, not
    the model's fully-qualified class name.** `Relation::enforceMorphMap([...])` in a service provider makes
    a later namespace move — a model relocated into an OSDD package per `skills/laravel-conventions`
    §10 point 5 — safe: every row already written keeps resolving through the map, where a stored FQCN
    silently orphans every polymorphic row once the class no longer exists at that path.
31. **A model's date attributes default to *mutable* Carbon instances, which a caller can change in place
    without meaning to.** Casting to `immutable_datetime` (or enabling immutable dates application-wide)
    means a method calling `->addDays(3)` on `$invoice->due_at` for a local calculation gets a new instance
    instead of silently mutating the one every other reader of that model holds in the same request — the
    object-identity twin of point 28's UTC discipline.
32. **A spatial or geography column type depends on a database extension that has to be enabled per
    environment, and the migration itself does not enable it.** A `point`/`geometry` column created where
    PostGIS (or the engine's equivalent) is already on succeeds in long-lived environments set up by hand,
    then fails on a fresh one (a new CI database, a new machine) because nothing in the migration
    provisioned the extension.
33. **`Model::preventLazyLoading()` and `preventSilentlyDiscardingAttributes()`, turned on outside
    production, convert two silent defects into loud exceptions during development.** The first throws when
    an unloaded relationship is lazy-loaded, catching the N+1 that point 21 of §1 asks to eager-load at the
    query site before a profiler has to; the second throws when a mass-assigned value lands on a column
    absent from `$fillable`, catching the over-broad request point 6 of §2 warns about at write time
    instead of it being silently dropped.
34. **`DB::transaction(callback, $attempts)`'s second argument retries the whole closure on a deadlock**,
    the framework's own answer to a deadlock a high-concurrency write path will eventually hit — a
    hand-written `try { ... } catch (QueryException $e) { if (deadlock) retry(); }` loop duplicates it and
    must get idempotency and the retry count right on its own (`skills/laravel-conventions` §11 point 10).
35. **`foreignIdFor(Model::class)` picks the column type from the referenced model's own key type, which a
    hand-written `foreignId()` call has to get right by hand instead.** A model using `HasUlids` or a
    non-default key type produces a `CHAR(26)`/`CHAR(36)` column through `foreignIdFor()`; a plain
    `$table->foreignId('parent_id')` always emits `UNSIGNED BIGINT`, silently wrong once point 29's ULID
    choice is made on the parent after the child migration was written. [Laravel migrations documentation,
    laravel.com/docs/12.x/migrations, read 2026-09-10.]
36. **A unique index that includes a soft-deleted row is enforcing uniqueness against rows the application
    already treats as gone.** `SoftDeletes` leaves the row in the table with `deleted_at` set, so a plain
    unique constraint on `email` still blocks a new signup from reusing an address that belongs to a
    soft-deleted account — the fix is a composite unique index including `deleted_at` (or a partial/filtered
    unique index where the engine supports one), "unique among the live rows".
37. **SQLite foreign key enforcement depends on a connection option, so a suite that runs on a different
    engine than production can accept an orphaned insert that production refuses.** The 12.x database docs
    say foreign key constraints are enabled by default for SQLite connections and are switched off with
    `DB_FOREIGN_KEYS=false`; in the framework source the connector issues `pragma foreign_keys` only when the
    connection's `foreign_key_constraints` option is set. A project that sets it off, or a custom connection
    defined without it, verifies only that point 22's `constrained()` chain compiles, never that it rejects an
    orphan. [Laravel database docs 12.x, "SQLite Configuration"; framework source `SQLiteConnector.php`, read
    2026-10-21.]
38. **`php artisan schema:dump` squashes a project's full migration history into one SQL file, and a
    project that adopts it stops running the squashed migrations' `up()` methods on a fresh install.** The
    dump plus any later migration is what runs from then on; a data-only backfill written as a step inside
    an old migration's `up()` — rather than a dedicated seeder or a one-off command — is silently skipped
    for every environment provisioned after the squash, a second reason (beside point 27) to keep a schema
    change and a data backfill as separate, explicitly-run steps. [Laravel migrations documentation,
    laravel.com/docs/12.x/migrations, read 2026-09-10.]
39. **`Model::chunkById()`/`lazyById()` page through a table by its primary key rather than by `OFFSET`, which
    is point 7's "stream, don't load into memory" kept correct while the table is written to during the same
    backfill.** An `OFFSET`-based `chunk()` shifts its window if an already-visited row is deleted
    mid-run, silently skipping or double-processing rows under concurrent writes; `chunkById()` anchors
    each page to "the last id seen."
40. **A check constraint enforces a row-level invariant the database itself refuses to violate, a stronger
    guarantee than the same rule written only as a Laravel validation rule.** Point 1 bans a DB-level enum
    for a value that changes with a deploy; a check constraint is the different case, a relationship between
    columns on the same row (an end date after a start date, a discount that cannot exceed the price).
    Validation alone protects only rows written through this application; a second writer (a script,
    another service) can still break the rule unless the database refuses it. The 12.x migrations docs list
    no check-constraint helper, so write it as a raw statement per engine (own guidance, not sourced).
