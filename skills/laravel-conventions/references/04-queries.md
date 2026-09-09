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
