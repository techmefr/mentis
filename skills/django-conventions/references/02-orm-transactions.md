# § 2 — The ORM and transactions

> Section 2 of `skills/django-conventions`. Read it when a queryset, a loop over related objects, a bulk write, a
> lock, a transaction or an action that must follow a commit is written. Read 2026-10-02 from the Django
> database-optimization topic, the QuerySet reference and the transactions topic (development docs, 6.2
> alpha; the fetch-mode rule is newer than the LTS releases).

1. **Profile before and after.** Look at what queries run and what they cost (the queryset `explain()`, a
   debug toolbar, or the database's own monitor) before changing anything, and again afterwards: every
   suggestion below can be neutral or reversed in your case, and an optimisation that costs readability must
   buy a measurable gain. Index on evidence: an index speeds the lookups that use it and its upkeep can outweigh the gain.
2. **Querysets are lazy and cache their result; attributes cache too, callables do not.** `entry.blog` is fetched
   once and reused; `entry.authors.all()` is a new query every time it is evaluated. A template silently calls
   callables, so a query hides behind a dotted name; read template code with that in mind. Store a queryset in a
   variable when you will iterate, test and count it, so the one result cache serves all three; calling
   `.exists()`, `.count()` and `.contains()` on top of a queryset you are about to load anyway costs extra
   queries.
3. **Related objects in a loop are N+1 queries.** Load them with the query: `select_related` joins
   single-valued relations (foreign key, one-to-one) into the same `SELECT`; `prefetch_related` does one extra
   query per relation and joins in Python, and is the only choice for many-to-many and reverse foreign keys.
   Where the project's Django version offers a fetch mode that bulk-loads on first access, enabling it through
   a custom manager removes the need to predict which relations a code path will touch; it is newer than the
   LTS line, so check the pinned version. Be aware that related-object access goes through the base manager,
   not the default one.
4. **Ask only for what you use.** `values()` / `values_list()` when you need dicts or tuples rather than model
   objects; `defer()` / `only()` only to avoid large text or expensive-to-convert columns, because a deferred
   field read later is another query and the database reads most of a row anyway; `count()` when you need only
   the number, `exists()` when you need only the answer; use the foreign key value already on the object
   (`entry.blog_id`) instead of loading the related row to read its id. Do not order a result you do not
   consume in order.
5. **Fetch a single object by an indexed, unique column.** `get()` on a column that is not unique may match many
   rows and scan the table; a unique constraint guarantees the lookup can never return more than one.
6. **Do the work in the database.** `filter` and `exclude`, `F()` expressions for comparisons between columns,
   `annotate` for aggregation; `RawSQL` or raw queries only when the ORM cannot say it. Raw SQL takes its
   values through the `params` argument and its placeholders are never quoted or interpolated: a quoted
   placeholder or an f-string is an injection (`skills/security-hardening`).
7. **Bulk statements skip per-object behaviour.** `QuerySet.update()` and `delete()` run one statement and do not
   call `save()` or `delete()` on instances; `bulk_create` and `bulk_update` do not call `save()` and do not
   send the save signals either. A rule that lives in `save()` or a signal is therefore not applied on those
   paths (§1.5); either the rule belongs in a constraint or a service, or the bulk path calls the service.
8. **Large result sets stream.** `iterator()` skips the result cache and keeps memory flat when a loop touches
   each row once.
9. **`get_or_create` and `update_or_create` are only atomic if the database enforces uniqueness** on the
   lookup fields. Without a unique constraint, concurrent calls insert duplicates; the constraint is part of
   the call.
10. **Lock rows with `select_for_update()` inside `atomic`, and say how to wait.** It locks the selected rows (and
    the rows of any `select_related` relation, unless `of=` narrows it) until the end of the transaction; by
    default a conflicting transaction blocks. `nowait=True` raises instead; `skip_locked=True` ignores locked
    rows. Support differs by backend, and it cannot be applied to the
    nullable side of an outer join.
11. **Autocommit is the default; a transaction is a decision.** Each statement commits on its own unless inside
    `atomic`. Wrap a multi-statement change in `transaction.atomic()` at the service (§1.1), not in the view. A
    per-request transaction (`ATOMIC_REQUESTS`) is simple and costs under load, covers only the view and not
    middleware or template rendering, and does not suit streaming responses; prefer the explicit block.
12. **Never catch a database error inside the `atomic` block it broke.** After an `IntegrityError` the
    transaction is unusable and a further query raises `TransactionManagementError`; the correct shape is
    `try: with atomic(): ... except IntegrityError:` so the failing part rolls back to a savepoint and the
    outer transaction continues. Nested `atomic` blocks are savepoints, and an inner success can still be
    rolled back by the outer block. An in-memory model is not rolled back with the database: restore its
    fields by hand.
13. **Side effects that must follow the data go through `transaction.on_commit`.** A mail, a task, a cache
    invalidation, a webhook registered with `on_commit` runs after the outermost commit, is discarded on
    rollback (including a savepoint rolled back), and runs at once when there is no transaction. Bind
    arguments with `functools.partial`. A failure in the callback does not roll the transaction back; a follow-up whose failure should
    undo the change does not belong in a callback. `robust=True` lets later
    callbacks run when one fails. Test with `captureOnCommitCallbacks`.
14. **Use `durable=True` for a block that must be the outermost transaction,** so that a caller wrapping it in
    another `atomic` fails loudly instead of deferring the commit it relied on.
