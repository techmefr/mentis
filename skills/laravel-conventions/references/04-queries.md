# laravel-conventions §4 — Queries

> Section 4 of `skills/laravel-conventions`. Read it when an Eloquent query, a relation load, or anything inside a loop. The other sections and the guardrails stay in `SKILL.md`.

1. **No query inside a loop.** A lazy-loaded relation accessed per iteration, an aggregate per row, a
   `find()` in a `foreach` — all N+1. Eager-load or aggregate before iterating. This includes a loop inside
   a view, which is the variant that survives review: the controller looks clean, and the template pulls a
   relation per row. It also includes the accessor that loads something — an N+1 can hide behind an
   attribute that reads like a field.
2. **Read the relation accessor**, never re-fetch a related model by hand from a foreign-key attribute: the
   accessor uses the loaded relation when it's there and is the thing eager-loading can optimise. A
   hand-rolled `Model::find($row->model_id)` is invisible to eager loading by construction, so it cannot be
   fixed later by adding a `with()` — it has to be found and rewritten first.
3. **Prefer the `OrFail` fetch** (`findOrFail`, `firstOrFail`) over a fetch plus a null check that aborts
   404: one line, and the not-found path can't be forgotten. The version to distrust is a fetch whose null
   case is handled *sometimes* — the second caller is where the null-pointer lands.
4. Push filtering, sorting and pagination into the query, not into a collection loaded whole and filtered in
   PHP. The failure is not only speed: a page computed after filtering in PHP has a wrong total, so the
   pagination lies before it gets slow.
5. **Count and aggregate in the database.** `withCount()` and a relation's own `->count()` issue an
   aggregate; `count($model->relation)` hydrates every row to reach a number, and the two read almost
   identically at the call site. Same for a sum, an average or a max computed by looping a collection. And
   an aggregate is not a filter: computing totals in PHP over an already-paginated set gives the total of
   the page, which is the bug that looks like a rounding error.
6. **Filter on the key you already have, not through a relation you don't need.** A nested existence check
   across two hops generates correlated subqueries the planner cannot help with, and it is usually
   unnecessary: when the discriminating foreign key is already a column on the row being filtered, filter on
   the column. Reach for the relation-existence check when the condition genuinely lives on the far side —
   and when it does, keep it to one hop and index the join key.
7. **A search-index query is a different engine, and it fails quietly.** The field the index stores is not
   always the field the database stores — an index that holds a label where the table holds an id will
   accept a filter on the id, match nothing, and return an empty list rather than an error. So a filter's
   contract is the index mapping, read before the filter is written, not inferred from the model. Two
   consequences: an index-backed list has a result ceiling and truncates past it *silently*, so anything
   that must be exhaustive (an export, a bulk action, a reconciliation) goes to the database instead; and a
   test that mocks the engine has to stub everything the calling code touches, or the mock fails somewhere
   unrelated and reads like a flake.
8. **Bulk work is chunked, and chunking has an ordering trap.** Never load an unbounded set with `get()`;
   chunk it, or stream it with a cursor when each row is handled independently. But a chunked read whose
   rows are mutated so they no longer match the query will skip rows, because the next page is computed
   against a table that moved — iterate by primary key for that case, or select the ids first and work from
   the list.
9. **Every application table is reached through its model**, pivot tables included. The raw query-builder
   facade looks equivalent and is not: it returns unhydrated rows and silently skips the casts, the
   accessors, the global scopes and the lifecycle events the model applies, so the difference surfaces later
   as a date that is a string, a soft-deleted row that came back, or a listener that never ran. A table with
   no model yet is the signal to declare one — a pivot model for a pivot — not a licence to reach past it.
   Genuine raw SQL for a reporting query or a bulk operation stays a named, deliberate exception, and it
   never carries domain writes.
10. **When raw SQL is the exception, bind the values.** Interpolating into the string is an injection
    surface, and even where the value is trusted it is an escaping problem: a class name or a Windows path
    in a string literal carries backslashes that the engine consumes, so the value stored is not the value
    written. Bindings sidestep both. A raw *fragment* that names only columns and operators is a different
    thing and is fine.
11. **Two writes that must both land are a transaction, not a sequence** — and where that gets decided is
    `skills/design-patterns` §4.7, including the part people skip: a queued job or a notification dispatched
    inside the transaction fires against state that may roll back, so it is dispatched after commit.
12. **`chaperone()` on a `hasMany` fixes the specific N+1 point 2 already names — a child reaching back for
    its own parent — without a query for each child.** Declared on the relationship (or opted into at the
    call site), the parent already loaded by the eager load is hydrated onto every child directly; the
    child's own inverse `belongsTo` accessor then finds it there instead of issuing point 1's per-row query.
    It only helps the reverse direction — a child that needs a *sibling*, not its own parent, is a different
    relation and a different fix.
13. **`lazy()`/`cursor()` stream one row at a time and both answer point 8's chunking need, but they are not
    interchangeable.** `cursor()` reads a single unbuffered database cursor and is the cheaper of the two on
    memory, but a query that visits a Collection-only method (`groupBy`, a collection macro) forces it back
    into a full collection anyway; `lazy()` keeps chunking under the hood, so it accepts those methods
    without that trade and is the safer default when the code between fetch and use is not already known
    to be row-by-row.
14. **`Model::shouldBeStrict()` turns point 1's N+1 rule into a thrown exception instead of a review
    checkpoint.** It also refuses a silently-discarded mass-assignment field and a read of a missing
    attribute — the same family of bug as point 1, all three failing loudly the moment they happen rather
    than at the point a slow query or a wrong value is noticed later. The trade is environment-specific: on
    in a local/CI environment so the violation is caught before merge, off in production so an edge case
    the tests missed degrades instead of 500ing for every affected user — a project running it everywhere
    has usually not thought about that half.
15. **A constrained eager load (`with(['relation' => fn ($query) => ...])`) filters or orders the *loaded*
    relation, and that is a different question from filtering the *parent* rows.** `whereHas` (point 6) decides
    which parents come back; the constrained closure decides which children come back for a parent that's
    already in the result. Using one to answer the other's question either drops parents that have no matching
    child at all, or loads every child and expects the parent list to have narrowed.
16. **A polymorphic `morphTo` needs `morphWith()` to eager-load type-specific relations, because a plain
    `with('commentable')` cannot know in advance which concrete model each row will resolve to.** Without it,
    loading the commentable's own relations falls back to point 1's per-row query once per polymorphic type
    encountered — the fix is declaring, per morph type, which of *that* type's relations to load alongside it.
17. **A correlated value pulled alongside a list (a child's latest row, a running count) is a subquery select
    (`addSelect`/`selectSub`, or the `latestOfMany`/`oldestOfMany` relation shortcut), not a loop reaching back
    per row.** The database computes it once per row inside the same query plan; the loop version is point 1's
    N+1 wearing the clothes of "just one more field," and it is the version that survives review because the
    field looks like a plain column at the call site.
18. **`whereHas` and a direct join both answer "parents with a matching child," and they are not interchangeable
    at scale.** `whereHas` compiles to a correlated subquery re-executed conceptually per parent row and composes
    safely with further `orWhereHas`/nested conditions; a join can be faster on a large table but silently
    duplicates the parent once per matching child unless the query is made distinct or the join is constrained
    to at most one row. Reach for the join once `whereHas`'s cost shows up in a slow-query log, not by default.
19. **A transaction that can deadlock needs a retry count, because `DB::transaction($callback, $attempts)`'s
    third argument is exactly for that** — a deadlock is a database-detected condition, not a bug in the
    callback, and MySQL/Postgres both expect the losing transaction to retry rather than surface the error to
    the caller. Retrying is only safe because point 11 already requires the callback to be the transaction's own
    unit of work with no side effect dispatched before commit — a callback that emails on every attempt would
    email once per retry.
20. **`upsert()` replaces a manual "find, then create-or-update" round trip, but the columns it checks for a
    collision have to be a real unique key, not just the columns that happen to be equal.** Its second
    argument names which columns identify an existing row and its third names which columns to overwrite when
    one matches — without a unique or primary constraint backing those columns at the database level, nothing
    stops two concurrent calls both deciding "no match" and both inserting, the same race point 11's
    transaction guidance exists to close. [Laravel query builder docs, laravel.com/docs/12.x/queries, read
    2026-09-10.]
21. **`chunkById` is point 8's ordering trap solved by construction, not merely a faster `chunk`.** Plain
    `chunk()` re-runs the query with an offset for every page, so a row updated (or deleted) between pages
    shifts every later page by one and skips a row; `chunkById` instead re-runs the query filtered on "id
    greater than the last one seen," which stays correct as long as the id itself is never reassigned to a
    different row mid-run. Reach for it by default on any chunked update, and reserve plain `chunk()` for a
    read-only pass. [Laravel query builder docs, laravel.com/docs/12.x/queries, read 2026-09-10.]
22. **`joinSub`/`leftJoinSub` and a `whereHas` subquery (point 18) solve different shapes of the same
    problem, and reaching for a join when the real need is an aggregate produces duplicate rows instead of a
    slow query.** A subquery join is for pulling a *value* alongside each parent row — a per-tenant running
    total, a latest related timestamp — computed once and joined in; it is point 17's `addSelect`/`selectSub`
    with an explicit alias instead of a scalar subquery, useful once the subquery itself needs its own
    filtering or grouping that a scalar subquery can't express. It answers "what value", not "which parents",
    which stays `whereHas`'s question. [Laravel query builder docs, laravel.com/docs/12.x/queries, read
    2026-09-10.]
23. **`withExists()` answers "does at least one match" without the `COUNT` a naïve `withCount() > 0` computes
    and discards.** A relation existence check compiled through `COUNT` counts every matching row before the
    call site throws the number away for a boolean; `withExists()` compiles a boolean-shaped subquery instead,
    which is the difference that shows up once the child table is large enough for the count itself to be the
    expensive part of the query.
24. **A `WHERE` clause built from a value the caller controls needs a column allow-list, not just a bound
    parameter.** Bindings (point 10) stop a value from being interpreted as SQL; they do nothing to stop a
    caller naming an arbitrary *column* to sort or filter by when the column name itself is taken from input
    and interpolated into the query — a sort parameter passed straight to `orderBy($request->sort)` lets the
    caller order by a column that was never meant to be exposed, or trigger an error probing for one that
    doesn't exist. The column name is validated against a known list before it ever reaches the query builder,
    the same validation point 9 of `skills/laravel-conventions` §6 already requires for query parameters
    generally.
25. **A soft-deleted row still counts toward a unique constraint unless the index itself is scoped to
    exclude it.** `SoftDeletes` filters a soft-deleted row out of ordinary queries, but a `UNIQUE` index at
    the database level has no concept of the deleted flag — re-creating a record with the same unique value
    after "deleting" the old one fails at the database, not in application code, because the old row is still
    physically present. The fix is a partial/conditional unique index (or a unique constraint over
    `(value, deleted_at)`) declared at the schema level, not a uniqueness check in PHP that loses the race
    `skills/laravel-conventions` §3 point 19 already warns about.
26. **A model event fired inside a query executed via `insert()`/`update()`/`delete()` on the query builder
    does not fire at all, and this is the same gap point 9 already names from a different angle.** Point 9
    covers casts, accessors and global scopes silently skipped by the query builder; lifecycle events are the
    same list — a bulk `Model::query()->where(...)->update([...])` changes rows without a single `updated`
    event firing for any of them, so a listener relying on that event to invalidate a cache or reindex a
    search document simply never runs for a bulk operation, which is exactly the kind of change that looks
    identical to a per-model `->update()` at the call site and behaves nothing like it.
27. **`doesntHave`/`whereDoesntHave` is `whereHas`'s negative, and it carries the same correlated-subquery
    cost point 18 already names for its positive form — it is not a cheaper query just because the answer is
    "none."** Reaching for a `leftJoin ... whereNull` instead is the join-based alternative point 18 describes,
    with the same duplicate-row risk once the join itself is one-to-many; the choice between the two is the
    same trade-off, only evaluated for "no match" instead of "at least one."
28. **`firstOr(fn () => ...)` is a third option between point 3's `firstOrFail` and a fetch-then-null-check,
    for the case where "not found" isn't an error at all but a different value to compute.** A lookup that
    falls back to a default object, a freshly-built (but not persisted) model, or a cached value when no row
    matches reads cleaner as `firstOr(...)` than as a fetch, a null check, and a branch — point 3's rule
    still holds when the missing case genuinely is a 404; this is for when it isn't one.
29. **A global scope applied automatically to every query on a model needs an explicit `withoutGlobalScope()`
    (or `withoutGlobalScopes()`) at the one call site that legitimately needs to see past it, not a model-wide
    toggle.** A soft-delete scope, a tenant scope, a "published only" scope all filter silently by design; the
    trap is either forgetting a scope exists (a query that should see soft-deleted rows for an audit report
    quietly excludes them) or removing it too broadly (a single report query disabling the tenant scope for the
    whole request instead of for its own query) — the removal is scoped to the query, the same way the
    filtering was.
30. **`whereBelongsTo($model)` replaces a hand-written `where('model_id', $model->id)` with the foreign key
    read from the relationship definition itself, and that is more than a shorthand once the relation's key
    name diverges from the table's default.** A `belongsTo` declared with a custom foreign key or owner key
    means the hand-written version has to know and repeat that customisation at every call site; `whereBelongsTo`
    reads it from the relationship once, so a later rename of the foreign key column only has to change the
    relationship definition instead of every place that filtered on it directly.
31. **`simplePaginate()` and `cursorPaginate()` both skip the `COUNT` query `paginate()` runs to compute a
    total, and that is a real cost difference on a large table, not just a smaller response payload.**
    `paginate()`'s total is what a numbered page control needs to render "page 3 of 40"; a "load more" or
    infinite-scroll UI never shows that number, so paying for the count query on every page request buys
    nothing for it — `simplePaginate()` drops the total but keeps offset-based paging (and point 34 of
    `skills/laravel-conventions` §6's ordering trap with it), while `cursorPaginate()` drops both the total
    and the offset instability at once.
32. **`when($condition, fn ($query) => ...)` and `unless()` build a query's optional clauses inline, without a
    chain of `if` statements duplicating the query object being reassigned in each branch.** A filter that
    only applies when a request parameter is present reads as `$query->when($request->filled('status'), fn
    ($q) => $q->where('status', $request->string('status')))` rather than an `if` around a `$query =
    $query->where(...)` reassignment — the same query builder point 9 of `skills/laravel-conventions` §6
    already asks to validate the parameter against an allow-list before it reaches this point, `when()` is
    just where the validated value gets applied conditionally.
33. **`Model::withoutTimestamps()` and a mass `update()` that bypasses `updated_at` are two different ways a
    bulk write can leave the timestamp lying about when it last changed, and only one of them is deliberate.**
    Wrapping a backfill in `withoutTimestamps()` is an explicit statement that this write shouldn't disturb the
    column a cache-invalidation or a "recently modified" query relies on; a bulk `update()` via the query
    builder (point 26) skips it implicitly and silently, which reads identically at the call site but for the
    opposite reason — one is a decision, the other is the same gap point 26 already names, just visible through
    the timestamp instead of a missing event.
