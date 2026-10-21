# laravel-conventions §4 — Queries

> Section 4 of `skills/laravel-conventions`. Read it when an Eloquent query, a relation load, or anything inside a loop. The other sections and the guardrails stay in `SKILL.md`.

1. **No query inside a loop.** A lazy-loaded relation accessed per iteration, an aggregate per row, a
   `find()` in a `foreach` — all N+1. Eager-load or aggregate before iterating. This includes a loop inside
   a view, the variant that survives review: the controller looks clean, and the template pulls a
   relation per row. It also includes the accessor that loads something — an N+1 can hide behind an
   attribute that reads like a field.
2. **Read the relation accessor**, never re-fetch a related model by hand from a foreign-key attribute: the
   accessor uses the loaded relation when present and is what eager-loading can optimise. A hand-rolled
   `Model::find($row->model_id)` is invisible to eager loading, so it cannot be fixed later by adding a
   `with()` — it has to be found and rewritten first.
3. **Prefer the `OrFail` fetch** (`findOrFail`, `firstOrFail`) over a fetch plus a null check that aborts
   404: one line, and the not-found path can't be forgotten. Distrust a fetch whose null case is handled
   *sometimes* — the second caller is where the null-pointer lands.
4. Push filtering, sorting and pagination into the query, not into a collection loaded whole and filtered in
   PHP. Not only speed: a page computed after filtering in PHP has a wrong total, so pagination lies before
   it gets slow.
5. **Count and aggregate in the database.** `withCount()` and a relation's own `->count()` issue an
   aggregate; `count($model->relation)` hydrates every row to reach a number, and the two read almost
   identically. Same for a sum, an average or a max computed by looping a collection. And an aggregate is
   not a filter: totals computed in PHP over an already-paginated set give the total of the page, the bug
   that looks like a rounding error.
6. **Filter on the key you already have, not through a relation you don't need.** A nested existence check
   across two hops generates correlated subqueries the planner cannot help with, and is usually
   unnecessary: when the discriminating foreign key is already a column on the row being filtered, filter on
   the column. Use the relation-existence check when the condition genuinely lives on the far side — and
   then keep it to one hop and index the join key.
7. **A search-index query is a different engine, and it fails quietly.** The field the index stores is not
   always the field the database stores — an index holding a label where the table holds an id will
   accept a filter on the id, match nothing, and return an empty list rather than an error. A filter's
   contract is the index mapping, read before the filter is written. Two consequences: an index-backed
   list has a result ceiling and truncates past it *silently*, so anything exhaustive (an export, a bulk
   action, a reconciliation) goes to the database; and a test that mocks the engine has to stub everything
   the calling code touches, or the mock fails somewhere unrelated and reads like a flake.
8. **Bulk work is chunked, and chunking has an ordering trap.** Never load an unbounded set with `get()`;
   chunk it, or stream it with a cursor when each row is handled independently. But a chunked read whose
   rows are mutated so they no longer match the query skips rows, because the next page is computed
   against a table that moved — iterate by primary key, or select the ids first and work from the list.
9. **Every application table is reached through its model**, pivot tables included. The raw query-builder
   facade looks equivalent and is not: it returns unhydrated rows and silently skips the casts, accessors,
   global scopes and lifecycle events, surfacing later as a date that is a string, a soft-deleted
   row that came back, or a listener that never ran. A table with no model yet is the signal to declare
   one — a pivot model for a pivot. Genuine raw SQL for a
   reporting query or a bulk operation stays a named, deliberate exception, and never carries domain writes.
10. **When raw SQL is the exception, bind the values.** Interpolating into the string is an injection
    surface, and even for a trusted value an escaping problem: a class name or a Windows path in a string
    literal carries backslashes the engine consumes, so the value stored is not the value written.
    Bindings sidestep both. A raw *fragment* naming only columns and operators is fine.
11. **Two writes that must both land are a transaction, not a sequence** — decided per
    `skills/design-patterns` §4.7, including the part people skip: a queued job or a notification dispatched
    inside the transaction fires against state that may roll back, so dispatch it after commit.
12. **`chaperone()` on a `hasMany` fixes the specific N+1 point 2 names — a child reaching back for its own
    parent — without a query per child.** Declared on the relationship (or opted into at the call site),
    the parent already loaded by the eager load is hydrated onto every child; the child's inverse
    `belongsTo` accessor finds it there instead of issuing point 1's per-row query. It only helps the
    reverse direction — a child needing a *sibling* is a different relation and fix.
13. **`lazy()` and `cursor()` both stream rows and answer point 8's chunking need, but they are not
    interchangeable.** `cursor()` runs a single query and hydrates one model at a time, so it cannot eager
    load relationships, and the docs add that it can still run out of memory because the PDO driver buffers
    the raw results; `lazy()` chunks under the hood, so it can eager load and is the one the docs recommend
    for very large sets. Both return a lazy collection. [Laravel Eloquent docs 12.x, "Cursors", read
    2026-10-21.]
14. **`Model::shouldBeStrict()` turns point 1's N+1 rule into a thrown exception instead of a review
    checkpoint.** In the 12.x source it switches on three guards together: lazy-loading prevention, an
    exception when an unfillable attribute is filled, and an exception when a missing attribute is read.
    The docs show the first two as separate calls guarded by a non-production check, which is the shape to
    copy: on in local and CI so the violation is caught before merge, off in production so an edge case the
    tests missed degrades instead of failing every affected user. [Laravel Eloquent docs 12.x, "Configuring
    Eloquent Strictness"; framework source `Model.php` (12.x), read 2026-10-21.]
15. **A constrained eager load (`with(['relation' => fn ($query) => ...])`) filters or orders the *loaded*
    relation, a different question from filtering the *parent* rows.** `whereHas` (point 6) decides
    which parents come back; the constrained closure decides which children come back for a parent already
    in the result. Using one for the other's question either drops parents with no matching child, or
    loads every child while the parent list stays wide.
16. **A polymorphic `morphTo` needs `morphWith()` to eager-load type-specific relations, because a plain
    `with('commentable')` cannot know which concrete model each row will resolve to.** Without it, loading
    the commentable's own relations falls back to point 1's per-row query once per polymorphic type — declare,
    per morph type, which of *that* type's relations to load.
17. **A correlated value pulled alongside a list (a child's latest row, a running count) is a subquery select
    (`addSelect`/`selectSub`, or the `latestOfMany`/`oldestOfMany` relation shortcut), not a loop reaching back
    per row.** The loop version is point 1's N+1 as "just one more field," and survives review because the
    field looks like a plain column.
18. **`whereHas` and a direct join both answer "parents with a matching child," and they are not interchangeable
    at scale.** `whereHas` compiles to a correlated subquery and composes safely with further
    `orWhereHas`/nested conditions; a join can be faster on a large table but silently duplicates the parent
    once per matching child unless the query is made distinct or the join constrained to at most one row.
    Reach for the join once `whereHas`'s cost shows up in a slow-query log, not by default.
19. **A transaction that can deadlock needs a retry count, because `DB::transaction()` takes one as its
    second argument for exactly that** (the docs write it as `attempts: 5`). A deadlock is a
    database-detected condition, not a bug in the callback, and once the attempts are used up the exception
    is thrown. Retrying is safe only because point 11 keeps side effects out of the callback until commit;
    one that emails would email once per retry. [Laravel database docs 12.x, "Handling Deadlocks", read
    2026-10-21.]
20. **`upsert()` replaces a manual "find, then create-or-update" round trip, but the columns it checks for a
    collision have to carry a unique or primary index.** Its second argument names the columns that identify
    an existing row, its third the columns to overwrite on a match; the docs say all databases except SQL
    Server require that index, and that MySQL and MariaDB ignore the second argument and use the table's own
    indexes. Without it nothing stops two concurrent calls both deciding "no match" and both inserting.
    [Laravel query builder docs 12.x, "Upserts", read 2026-10-21.]
21. **`chunkById` is point 8's ordering trap solved by construction, not merely a faster `chunk`.** The docs
    say that updating records while chunking can change the chunk results in unexpected ways, and that
    `chunkById` instead paginates on the primary key; it also adds its own where conditions, so the docs
    advise grouping your own conditions in a closure. Plain `chunk()` pages by offset in the framework
    source, so a row updated or deleted between pages can shift later pages. Use `chunkById` for any chunked
    update and keep plain `chunk()` for a read-only pass (`lazyById` is the streaming twin). [Laravel query
    builder docs 12.x, "Chunking Results", read 2026-10-21.]
22. **`joinSub`/`leftJoinSub` and a `whereHas` subquery (point 18) solve different shapes of the same
    problem, and reaching for a join when the real need is an aggregate produces duplicate rows instead of a
    slow query.** A subquery join pulls a *value* alongside each parent row — a per-tenant running total, a
    latest related timestamp — point 17's `addSelect`/`selectSub` with an explicit alias, useful once the
    subquery needs its own filtering or grouping. It answers "what value", not "which parents", which stays
    `whereHas`'s question. [Laravel query
    builder docs, laravel.com/docs/12.x/queries, read 2026-09-10.]
23. **`withExists()` answers "does at least one match" as a boolean attribute on each parent.** The docs list it
    next to `withCount`, `withMin`, `withMax`, `withAvg` and `withSum`; each adds an attribute to the
    resulting models. Own guidance: prefer it to `withCount()` followed by a comparison with zero when only
    existence matters; the saving on a large child table was not measured. [Laravel Eloquent relationships
    docs 12.x, "Aggregating Related Models", read 2026-10-21.]
24. **A `WHERE` clause built from a value the caller controls needs a column allow-list, not just a bound
    parameter.** Bindings (point 10) stop a value being interpreted as SQL; they do nothing when the
    column name itself is taken from input — `orderBy($request->sort)` lets the caller order by a column
    never meant to be exposed, or trigger an error probing for one that doesn't exist. Validate the column
    name against a known list before it reaches the query builder, as `skills/laravel-conventions` §6
    point 9 requires for query parameters generally.
25. **A soft-deleted row still counts toward a unique constraint unless the index itself is scoped to
    exclude it.** `SoftDeletes` filters a soft-deleted row out of ordinary queries, but a `UNIQUE` index has
    no concept of the deleted flag — re-creating a record with the same unique value after "deleting" the
    old one fails at the database, because the old row is still physically present. The fix is a
    partial/conditional unique index (or a unique constraint over `(value, deleted_at)`) at the schema level,
    not a uniqueness check in PHP that loses the race `skills/laravel-conventions` §3 point 19 warns about.
26. **A model event fired inside a query executed via `insert()`/`update()`/`delete()` on the query builder
    does not fire at all, the gap point 9 names from a different angle.** Point 9 covers casts, accessors
    and global scopes skipped by the query builder; lifecycle events are on the same list — a bulk
    `Model::query()->where(...)->update([...])` changes rows without a single `updated` event, so a
    listener relying on it to invalidate a cache or reindex a search document never runs, though the call
    looks identical to a per-model `->update()`.
27. **`doesntHave`/`whereDoesntHave` is `whereHas`'s negative, and it carries the same correlated-subquery
    cost point 18 names — it is not cheaper because the answer is "none."** A `leftJoin ... whereNull` is the
    join-based alternative point 18 describes, with the same duplicate-row risk once the join is
    one-to-many; the trade-off is the same, evaluated for "no match."
28. **`firstOr(fn () => ...)` is a third option between point 3's `firstOrFail` and a fetch-then-null-check,
    for the case where "not found" isn't an error but a different value to compute.** A fallback to a default object, an unpersisted model or a cached value reads cleaner as
    `firstOr(...)` than fetch, null check and branch — point 3 still holds when the missing case is a 404.
29. **A global scope applied automatically to every query on a model needs an explicit `withoutGlobalScope()`
    (or `withoutGlobalScopes()`) at the one call site that legitimately needs to see past it, not a model-wide
    toggle.** A soft-delete scope, a tenant scope, a "published only" scope all filter silently by design; the
    traps are forgetting a scope exists (an audit report quietly excluding soft-deleted rows) or removing it
    too broadly (a report query disabling the tenant scope for the whole request instead of its own query) —
    scope the removal to the query, as the filtering was.
30. **`whereBelongsTo($model)` replaces a hand-written `where('model_id', $model->id)` with the foreign key
    read from the relationship definition itself, more than a shorthand once the relation's key name
    diverges from the table's default.** A `belongsTo` with a custom foreign key or owner key means the
    hand-written version must repeat that customisation at every call site; `whereBelongsTo` reads it from
    the relationship once, so a later column rename changes only the relationship definition.
31. **`simplePaginate()` skips the `COUNT` query `paginate()` runs to compute a total, and `cursorPaginate()`
    skips it too while also avoiding the offset.** The docs say `paginate` counts the matching records first
    so it knows the page count, that `simplePaginate` suits a UI with only "Next" and "Previous" links, and
    that cursor pagination builds where clauses instead of an offset, which they call the most efficient of
    the three; it needs an order by clause on columns that belong to the table being paginated. A numbered
    page control needs the total, so it needs `paginate()`. [Laravel pagination docs 12.x, read 2026-10-21.]
32. **`when($condition, fn ($query) => ...)` and `unless()` build a query's optional clauses inline, without a
    chain of `if` statements reassigning the query in each branch.** A filter applying only when a request
    parameter is present reads as `$query->when($request->filled('status'), fn
    ($q) => $q->where('status', $request->string('status')))` rather than an `if` around a `$query =
    $query->where(...)` reassignment — the parameter having been validated against an allow-list first, as
    point 9 of `skills/laravel-conventions` §6 asks, `when()` is where the validated value gets applied
    conditionally.
33. **`Model::withoutTimestamps()` and a mass `update()` that bypasses `updated_at` are two ways a bulk write
    can leave the timestamp lying about when it last changed, and only one is deliberate.** Wrapping a
    backfill in `withoutTimestamps()` states that this write shouldn't disturb the column a
    cache-invalidation or "recently modified" query relies on; a bulk query-builder `update()` (point 26)
    skips it implicitly and silently — one is a decision, the other point 26's gap seen through the timestamp.
34. **`firstOrCreate()`/`updateOrCreate()` run a select then, conditionally, an insert as two separate
    statements — and between them a second concurrent call can also see no match.** Both requests decide
    "no row exists" and both insert; the second duplicates a row a unique index would have caught (point
    25's database-level check is the same category) or fails outright — the fix is a unique constraint
    backing the lookup columns so the race fails loudly instead of duplicating silently, or the whole
    read-then-write in `DB::transaction()` with `lockForUpdate()` (point 36) so the second call waits.
    [Laravel race-condition guidance and Eloquent docs, read 2026-09-10.]
35. **`whereAny([...], $operator, $value)` and `whereAll([...], $operator, $value)` apply one condition across
    several columns at once, replacing a chain of `orWhere()`/`where()` calls whose parentheses must be right
    by hand.** `whereAny(['title', 'body'], 'like', "%{$term}%")` satisfies point 24's column allow-list by
    construction — the columns are named once in an array literal, not built from request input — and reads
    as one intent instead of a chain a later edit can silently unbalance.
36. **`lockForUpdate()` and `sharedLock()` are pessimistic locks meant to be held until the transaction ends,
    so use them inside `DB::transaction()`.** The docs: a shared lock stops the selected rows from being
    modified until your transaction commits; a for-update lock stops them from being modified or selected
    with another shared lock. Own guidance: outside a transaction there is nothing to hold the lock across
    the following statements, which reads like the race it was meant to close. Point 11 from the other
    direction: the lock makes the read, as the transaction's first statement, trustworthy for the write
    after it. [Laravel query builder docs 12.x, "Pessimistic Locking", read 2026-10-21.]
37. **`Builder::clone()` (or PHP's own `clone`) is what lets a base query be reused for two different results
    — a paginated list and its unfiltered total, say — without the second use inheriting constraints added
    while building the first.** An Eloquent builder is mutable: `->where()` on a query object already assigned
    elsewhere in the method changes that other reference too, since both names point at one builder; clone
    before branching, or point 4's "filtering belongs in the query" yields two queries sharing a growing
    set of constraints neither branch expected.
38. **`Model::preventAccessingMissingAttributes()` is `shouldBeStrict()` (point 14) split into its own toggle**,
    for a project that wants the missing-attribute guard without making every N+1 access throw. A project
    mid-migration on N+1s can turn missing-attribute and mass-assignment strictness on immediately while
    triaging lazy-loading violations separately.
39. **Select only the columns the operation needs, but only when it buys something.** Leaving out large text,
    binary or JSON columns on a list is a real saving; narrowing every query is noise. When you do narrow, keep
    every key Eloquent matches on: for a `belongsTo`, the foreign key on the parent query and the owner key on the
    related one; the parent's local key and the related foreign key for a `hasMany`, otherwise the eager
    load silently returns nothing.
40. **`toQuery()` on a non-empty Eloquent collection of one model type builds a bulk query from the loaded
    models, and a bulk update through it fires no per-model events**, as any other bulk update. It is the
    tidy replacement for a hand-built `whereIn($collection->modelKeys())`, and the wrong tool when a listener,
    an audit trail or a cache invalidation hangs on the model's own update event (`skills/laravel-pruning-fires-delete-events`
    makes the same point for deletion).
