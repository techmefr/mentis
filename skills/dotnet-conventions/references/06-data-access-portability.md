# § 6 — Data access and portability

> Section 6 of `skills/dotnet-conventions`. Read it when an EF Core query or migration is written, when
> the middleware pipeline is changed, or when a path, a clock or a culture is involved.

1. `AsNoTracking()` on every read-only EF Core query: without it there's a measured cost (~2x slower at
   scale) and unwanted state tracking. Tracking is what produces bugs rather than slowness: a tracked
   entity modified anywhere in the request is saved by the next `SaveChanges`, including one called by
   unrelated code further down the pipeline.
2. Middleware order checked by eye (`UseRouting`/`UseAuthentication`/`UseAuthorization`): no analyzer
   covers it, and getting it wrong fails open — the attributes are all present, the checks never run, and
   nothing looks wrong (§3.11).
3. Cross-platform APIs by default even on a single-OS target today: `Path.Combine` over hardcoded
   separators, the framework's folder-path API over an absolute `C:\…`, a hosted `BackgroundService` over
   a Windows-only service host, the configuration abstraction over the registry. The port is cheap now and
   expensive later; it is forced rarely by a decision to change OS but by a container, a CI runner or a
   developer's machine, when the assumptions already span dozens of files.
4. **Never read the ambient clock in business logic.** The local-time properties answer by the host's
   timezone and DST state, so the same code gives one result on a developer's box and another in a UTC
   container — a correctness bug, not style. A class built by the container takes the platform's time
   abstraction as a dependency, which also makes "expires in 30 days" testable without waiting. The
   platform ships that abstraction and a controllable fake, so the rule costs one constructor parameter, not
   an interface of your own — and the fake turns cases nobody reaches by waiting (a month boundary, a DST
   hour, a leap day) into ordinary tests. A timer created through it is disposed like any resource (§5.9).
5. **State the culture and the comparison instead of inheriting the ambient one.** Two halves of one
   boundary: machine-facing text — identifiers, keys, wire and file formats — parses and formats with the
   invariant culture and compares **ordinally**; human-facing text parses, formats and sorts with the
   current culture, chosen deliberately rather than by omission. The invariant-culture *comparison* is
   never the answer to either: it is linguistic collation with a frozen locale, not ordinal.
6. **A query inside a loop is N+1, and the fix is stated in the query, not the loop.** Loading a thousand
   orders and reading `order.Customer.Name` issues a thousand round trips — each fast, the page slow. Load
   the relations the code will read, or project straight to the shape the caller needs, which is better
   because it also reads only the columns involved.
7. **Know which half of the query runs on the server.** An expression EF Core cannot translate is either
   refused or evaluated on the client depending on the construct, and the second case silently loads the
   table before filtering it. A filter calling a local method looks like every other filter and behaves
   like a full scan; check what was generated rather than assuming.
8. **A migration is code and is reviewed like code.** A generated migration can contain a column drop, a
   type change that truncates, or a rename expressed as drop-plus-add — none visible in the model diff that
   produced it, all data loss on the way to production. Read the generated file, every time, before it is
   committed.
9. **A `DbContext` is scoped and is not thread-safe.** Two awaits running in parallel on one instance
   corrupt its change tracker, and the exception is about a concurrent operation rather than the code that
   started them. Parallel work gets a scope each (§2.4), which is also what §2.3's captive-dependency rule
   protects.
10. **`SaveChanges` is the transaction boundary, so two calls are two transactions.** Writing a parent,
    saving, then writing children and saving again can leave the parent committed and the children
    missing. One call per business operation, or an explicit transaction around the whole thing — the same
    rule as `skills/design-patterns` §4.7, including side effects going after the commit rather than
    inside it.
11. **Enabling connection resiliency changes what a manual transaction may do.** A retrying execution
    strategy cannot replay a user-initiated transaction on its own, so code opening one must go through the
    strategy explicitly. The failure is not subtle — it throws — but appears only once retries are switched
    on, usually long after the code was written.
12. **A moment in time crosses the storage boundary with its offset or not at all.** Storing a local
    `DateTime` loses which offset it was local to, so it cannot be converted back correctly, and rows
    written either side of a DST change are no longer comparable. Store the instant — a `DateTimeOffset`,
    or UTC by an enforced convention — and keep the display conversion at the edge (point 4).
13. **Invariant globalization is a project-wide switch, and it makes point 5's second half throw.** Turning
    it on — commonly for container size, trimming or an AOT build, often by whoever chose the base image
    rather than whoever wrote the code — makes naming any culture raise `CultureNotFoundException` at run
    time. The human-facing half of point 5 stops being a wrong result and becomes an exception, and a test
    of culture-dependent formatting cannot be written. Read the switch before assuming a locale exists; a
    project with it on has decided there is one culture, a decision worth stating rather than discovering.
14. **Two collection includes in one query multiply the rows, and the fix has its own cost.** Loading a
    parent with two child collections in one statement returns every combination — ten and ten come back
    as a hundred rows carrying the parent's columns a hundred times, a cost of bandwidth and
    materialisation rather than query plan. Splitting the query is the answer for two or more collections
    and stays wrong for one; splitting means several round trips with no transaction between them, so the
    halves can disagree, and any paging must be ordered deterministically or pages are drawn from different
    orderings of the same rows.
15. **A bulk update or delete statement bypasses everything the rest of the code relies on.** Translating
    the change into one SQL statement instead of loading entities is right for a large set, and skips the
    change tracker — with it the interceptors, the domain events, the audit columns and the **global query
    filters**, soft delete included. A bulk delete reaches rows the application considers already deleted,
    and nothing near it says so. Use it deliberately, on a query whose filter restates by hand whatever the
    global filter did.
16. **Raw SQL has two forms and only one is a query.** The interpolated form turns every hole into a
    parameter; the plain-string form concatenates, so a value from a request becomes part of the statement.
    They differ by one character at the call site and a vulnerability class in production — and the plain
    form is what internet examples use, because it is shorter.
17. **A pooled `DbContext` factory reuses the instance, and what the context accumulated on the last
    request is still there on the next.** `AddDbContextPool` cuts construction cost under load by resetting
    the context's own state, not any state a class built on it added — a field cached on a custom context
    subclass, a static-feeling value captured at construction, survives the reset and leaks from one
    caller's request to the next. A pooled context stays a thin wrapper over the generated one, or pooling
    becomes a cross-request data bug.
18. **Split-query behaviour is a per-query decision as often as a global default.** Setting
    `UseQueryTrackingBehavior`-style split queries globally treats every query with more than one included
    collection alike, but point 14's trade — several round trips, no shared transaction — is worth paying
    only where row multiplication is large. `AsSplitQuery()` and `AsSingleQuery()` at the call site
    override the default for the one query that needs it: a decision made where the data's shape is
    known, not a blanket policy.
19. **A `SaveChangesInterceptor` is the one place a cross-cutting write concern belongs, not copied into
    every place that calls `SaveChanges`.** Stamping an audit column, rejecting a save that violates an
    invariant no single entity can express, or turning a soft-delete flag into the update it is — each done
    once in an interceptor runs for every write path including ones added later, where logic pasted at each
    call site is out of sync the day a new call site forgets it.
20. **A filtered or ordered include changes what a collection navigation returns, and doing it in the
    query is why it exists.** `Include(x => x.Children.Where(...).OrderBy(...))` (filtered-include syntax)
    applies the filter and order in the generated SQL — one query producing exactly the rows needed.
    Loading the full collection and filtering in memory defeats point 6, paying for every row the filter
    discards.
21. **A compiled model trades a startup cost for a per-request one, and pays off only once the model is
    genuinely large.** EF Core builds the model mapping entities to the schema once at startup by
    reflecting over every entity type; a compiled model (generated ahead of time via
    `dotnet ef dbcontext optimize`) skips that reflection and can work where dynamic model building can't,
    as under trimming or Native AOT (§9). It is generated code that must be regenerated whenever the mapped
    model changes — worth carrying when startup time matters for a large model, not a default for every
    project.
22. **A concurrency token (`[Timestamp]`/`RowVersion`, or a plain column mapped with
    `IsConcurrencyToken()`) turns a lost update into a `DbUpdateConcurrencyException` instead of a silent
    overwrite.** Two requests loading the same row, editing different fields and saving in sequence
    otherwise both succeed — the second `SaveChanges` writes over the first's change, with no error naming
    what was lost. The token makes the second save fail loudly, where the caller can still decide what "the
    row changed underneath you" means for this operation.
23. **A complex type or owned type maps a value object into the owner's own table without an identity the
    rest of the schema can reference.** `ComplexProperty` (or `OwnsOne`, its entity-shaped predecessor)
    keeps an address or money amount a real .NET type with its own equality instead of flattening into
    loose columns on the parent — use it whenever a value object (§4.12) would otherwise be three or four
    scalar properties the mapping re-groups by naming convention alone.
24. **A `ValueConverter` translates between the .NET type the domain wants and the column type the store
    has, and belongs in the model configuration, not a property getter converting by hand on every read.**
    An enum stored as its display string, a value object stored as its wrapped primitive, a `DateOnly`
    mapped where the provider expects `DateTime` — configured once, every query, projection and migration
    agrees, where a converting getter still leaves `Where` clauses and raw column access seeing the
    untranslated stored value.
25. **Keyset pagination (`WHERE Id > @lastId ORDER BY Id LIMIT @n`) replaces offset paging (`Skip`/`Take`)
    once a table is large enough that `Skip` must walk past everything it discards.** An OFFSET is not an
    index seek — the database scans and discards every skipped row to find the page start, so page 500
    costs more than page 1 though both return the same number of rows; keyset paging seeks to the last-seen
    key, the same trade point 6 makes for a query in a loop, restated for a paged list.
26. **A connection string is never the literal secret checked into `appsettings.json` — a placeholder is,
    and the real value comes from an environment variable, a secret store or user-secrets in
    development.** `appsettings.json` ships inside the published artefact and is readable by anyone who can
    open it, so a credential committed there is leaked the moment the repository or image is shared,
    whatever access control the running service enforces.
27. **A keyless entity type (`HasNoKey()`, or a type mapped from a raw SQL view with no natural key) can
    never be tracked and is only read, never updated through the change tracker.** It exists for a view, a
    stored-procedure result shape or a report projection with no single-row identity — using it on a table
    that has a key just to skip defining one removes the ability to update that entity through EF Core, a
    permanent limitation of the mapping, not a shortcut around modelling the key.
28. **A compiled query (`EF.CompileQuery`/`EF.CompileAsyncQuery`) is a different optimisation from point
    21's compiled model; confusing them means reaching for the wrong one.** The compiled model skips
    reflecting over the *schema* at startup; a compiled query caches the translation of one specific LINQ
    expression to SQL so that shape skips re-translation per call — worth it for a query run often enough
    that repeated translation shows in a profile, and a second thing to keep in sync by hand: the compiled
    delegate captures the expression tree as written, so a query changed at the call site without touching
    the compiled declaration keeps running the old translation.
29. **Table splitting maps two or more entity types onto one table, and loading one without the other is a
    decision the mapping makes, not the query.** A large, rarely-read column group (a document's full text,
    a blob) split into its own entity sharing the parent's primary key lets a parent query skip that column
    by not including the split entity — but only if it is genuinely optional to load, meaning every read
    path must know whether it needs the second half or silently pays a second round trip for it.
30. **A shadow property tracked by EF Core but absent from the CLR type is invisible to code reading the
    entity directly, including a debugger.** A foreign key EF Core infers from a navigation, or a column
    deliberately excluded from the class and configured through the fluent API only, still participates in
    queries, migrations and change tracking — but `object.Property` doesn't see it. It is the right tool
    for a column the domain has no business exposing, and a source of "where did this column come from"
    the day someone reads the entity class expecting the schema fully described there.
31. **A global query filter applies to every query against that entity type, including one reached through
    a navigation the calling code never mentions.** Point 15 covers a bulk statement bypassing the filter;
    the opposite failure is a query including it unexpectedly — an owned or table-split type sharing the
    parent's filter, or a self-referencing navigation silently dropping soft-deleted children from a
    parent's own collection with no `Where` naming it. `IgnoreQueryFilters()` exists for the one query that
    legitimately needs the full set, and carries the review weight of any bypass of a rule the codebase
    assumes is always on.
32. **The command timeout and the connection timeout answer different questions, and a slow query fails
    against whichever was configured.** The connection timeout bounds establishing a connection; the
    command timeout bounds one executed command once connected — a provider's default command timeout (30
    seconds for the SQL Server provider) is a per-command ceiling a legitimately long report query hits
    however fast the connection opened, and raising the wrong one leaves the real limit where it was.
33. **A relational database's own feature (a JSON column, a computed column, an ignore-case collation) is
    provider-specific, and treating it as the default mapping makes a second provider a rewrite instead of
    a config change.** Mapping a property `ToJson()` in the relational sense, or relying on a
    server-computed column's exact type, ties the model to the provider implementing that mapping; a
    codebase that has only run on one provider and mixes provider-specific mapping into the ordinary model
    has spent point 3's portability budget without a decision to spend it.
34. **`SaveChanges` batches pending inserts, updates and deletes into as few round trips as the provider
    allows, and disabling batching is a real trade, not a free safety switch.** Turning batching off (or a
    provider defaulting to a small batch size) trades round trips for a smaller blast radius per statement,
    which matters where a very large single statement risks a timeout or a lock held longer than smaller
    ones — reached for as a default rather than a response to a measured problem, it pays point 6's
    per-round-trip cost on every `SaveChanges` for a save that was already one transaction (point 10).
35. **`AsNoTrackingWithIdentityResolution()` and a JSON-mapped collection navigation don't combine safely,
    and the platform now refuses the combination rather than return a silently wrong result.** Identity
    resolution gives every row mapping to the same key the same object instance without the full change
    tracker; a JSON column's nested collection is materialised inside its parent's document with no
    row-per-child identity to key on, so the combination used to produce a corrupted graph or an opaque
    deserialisation error. Know the combination is restricted rather than chase the parse exception as if
    the query were malformed — a JSON-owning entity gets an ordinary `AsNoTracking()`.
36. **`ExecuteUpdateAsync` can now target a property nested inside a JSON column, where the whole document
    previously had to be read back and rewritten through `SaveChanges`.** Point 15's trade-off applies
    exactly as to an ordinary column: right for changing one field across many rows without loading them,
    and still no interceptor, domain event or soft-delete filter runs for the write, so point 15's
    deliberate, filter-restated-by-hand discipline is not optional because the target is JSON.
37. **`ExecuteUpdateAsync` accepting a plain lambda, not only an expression tree the provider must parse,
    changes what a conditional or dynamically-built update looks like.** A property/value set decided at
    run time — which columns to touch depends on which fields a caller sent — used to force building the
    setter expression tree by hand, one `SetProperty` reflected together; a plain lambda is ordinary C# the
    method evaluates directly, simpler where the update shape is the variable part, and it doesn't change
    point 8's "check what runs on the server" caution for the `Where` selecting the rows.
38. **A complex type mapped onto the owner's table (point 23) can collide with another property's column
    name, and column uniquification turns that collision into two distinct columns instead of one property
    overwriting another's storage.** Two properties from different complex types (or a complex type and a
    scalar) that would map to the same column name are now disambiguated by an appended number rather than
    merged — worth knowing because the old behaviour was no error: both wrote to one column and the last
    saved silently won, reading as two independent fields until the data is inspected sideways.
39. **A compiled model (point 21) no longer needs its own `UseModel` call in the context's configuration
    when it sits in the same project as the `DbContext` using it — the provider detects and applies it.**
    The model still has to be regenerated by hand whenever the mapped model changes (point 21's caveat
    stands), but the wiring cost that made it feel like a separate opt-in path is gone for the common case,
    removing one reason a large-model project defers adoption past the point startup time matters.
40. **Querying directly into a JSON column's nested structure — filtering or projecting a field inside the
    document without loading and deserialising the whole column — arrived in the relational JSON mapping
    after point 33 was written, and is as provider-specific as that point says.** A `Where` reaching into a
    JSON property translates to the provider's own JSON path syntax, so point 33's portability budget is
    spent a second time once a query, not just a mapping, depends on one provider's JSON functions.
