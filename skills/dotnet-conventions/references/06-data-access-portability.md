# § 6 — Data access and portability

> Section 6 of `skills/dotnet-conventions`. Read it when an EF Core query or migration is written, when
> the middleware pipeline is changed, or when a path, a clock or a culture is involved.

1. `AsNoTracking()` on every read-only EF Core query: without it there's a measured cost (~2x slower at
   scale) and unwanted state tracking. The tracking is the part that produces bugs rather than slowness: a
   tracked entity modified anywhere in the request is saved by the next `SaveChanges`, including one called
   by unrelated code further down the pipeline.
2. Middleware order checked by eye (`UseRouting`/`UseAuthentication`/`UseAuthorization`): no analyzer covers
   it, and getting it wrong fails open. Failing open is the whole reason this is in the block: the
   attributes are all present, the checks never run, and nothing in the code looks wrong (§3.11).
3. Cross-platform APIs by default even on a single-OS target today: `Path.Combine` over hardcoded
   separators, the framework's folder-path API over an absolute `C:\…`, a hosted `BackgroundService` over a
   Windows-only service host, the configuration abstraction over the registry. The port is cheap now and
   expensive later. The move that forces it is rarely a decision to change OS — it is a container, a CI
   runner or a developer's machine, and by then the assumptions are spread over dozens of files.
4. **Never read the ambient clock in business logic.** The local-time properties answer according to the
   host machine's timezone and DST state, so the same code gives one result on a developer's box and another
   in a UTC container — a correctness bug, not a style point. A class built by the container takes the
   platform's time abstraction as a dependency; that is also what makes "expires in 30 days" testable
   without waiting. The platform ships that abstraction and a controllable fake for tests, so this rule
   costs one constructor parameter rather than an interface of your own — and the fake is what makes the
   cases nobody reaches by waiting (a month boundary, a DST hour, a leap day) into ordinary tests. A timer
   created through it is disposed like any other resource (§5.9).
5. **State the culture and the comparison instead of inheriting the ambient one.** Two halves of one
   boundary, not a rule with a footnote: machine-facing text — identifiers, keys, wire and file formats —
   parses and formats with the invariant culture and compares **ordinally**; human-facing text parses,
   formats and sorts with the current culture, chosen deliberately rather than by omission. The
   invariant-culture *comparison* is never the answer to either: it is linguistic collation with a frozen
   locale, which is not ordinal.
6. **A query inside a loop is N+1, and the fix is stated in the query, not in the loop.** Loading a
   thousand orders and reading `order.Customer.Name` issues a thousand round trips — each fast, and the
   page slow. Load the relations the code will read, or project straight to the shape the caller needs,
   which is the better answer because it also reads only the columns involved.
7. **Know which half of the query runs on the server.** An expression EF Core cannot translate is either
   refused outright or evaluated on the client depending on the construct, and the second case silently
   loads the table before filtering it. So a filter that calls a local method looks like every other filter
   and behaves like a full scan; check what was generated rather than assuming.
8. **A migration is code and is reviewed like code.** A generated migration can contain a column drop, a
   type change that truncates, or a rename expressed as drop-plus-add — none of which is visible in the
   model diff that produced it, and all of which are data loss on the way to production. Read the generated
   file, every time, before it is committed.
9. **A `DbContext` is scoped and is not thread-safe.** Two awaits running in parallel on the same instance
   corrupt its change tracker, and the exception it throws is about a concurrent operation rather than
   about the code that started them. Parallel work gets a scope each (§2.4), which is also what §2.3's
   captive-dependency rule is protecting.
10. **`SaveChanges` is the transaction boundary, so two calls are two transactions.** An operation that
    writes a parent, saves, then writes children and saves again can leave the parent committed and the
    children missing. One call per business operation, or an explicit transaction around the whole thing —
    the same rule as `skills/design-patterns` §4.7, including the part about side effects going after the
    commit rather than inside it.
11. **Enabling connection resiliency changes what a manual transaction may do.** A retrying execution
    strategy cannot replay a user-initiated transaction on its own, so code that opens one has to go
    through the strategy explicitly. The failure is not subtle — it throws — but it appears only once
    retries are switched on, which is usually long after the code was written.
12. **A moment in time crosses the storage boundary with its offset or not at all.** Storing a local
    `DateTime` loses which offset it was local to, so the value cannot be converted back correctly, and
    two rows written either side of a DST change are no longer comparable. Store the instant — a
    `DateTimeOffset`, or UTC by an enforced convention — and keep the display conversion at the edge
    (point 4).
13. **Invariant globalization is a project-wide switch, and it makes point 5's second half throw.**
    Turning it on — commonly for container size, trimming or an AOT build, and often by whoever chose the
    base image rather than by whoever wrote the code — makes naming any culture raise
    `CultureNotFoundException` at run time. So the human-facing half of point 5 stops being a wrong
    result and becomes an exception, and a test that checks culture-dependent formatting cannot be
    written at all. Read the switch before assuming a locale is available; a project that has it on has
    decided there is only one culture, which is a decision worth stating rather than discovering.
14. **Two collection includes in one query multiply the rows, and the fix has its own cost.** Loading a
    parent with two child collections in a single statement returns every combination of the two — ten and
    ten come back as a hundred rows carrying the parent's columns a hundred times, which is bandwidth and
    materialisation rather than a slow query plan. Splitting the query is the answer for two or more
    collections and stays wrong for one; and splitting means several round trips with no transaction
    between them, so the halves can disagree, and any paging has to be ordered deterministically or the
    pages are drawn from different orderings of the same rows.
15. **A bulk update or delete statement bypasses everything the rest of the code relies on.** Translating
    the change into one SQL statement instead of loading the entities is the right call for a large set, and
    it skips the change tracker — and with it the interceptors, the domain events, the audit columns and the
    **global query filters**, soft delete included. So a bulk delete reaches rows the application considers
    already deleted, and nothing in the code near it says so. Use it deliberately, on a query whose filter
    restates by hand whatever the global filter was doing.
16. **Raw SQL has two forms and only one of them is a query.** The interpolated form turns every hole into a
    parameter; the plain-string form concatenates, so a value that came from a request is now part of the
    statement. They differ by one character at the call site and by a vulnerability class in production —
    and the plain form is what an example on the internet uses, because it is shorter.
17. **A pooled `DbContext` factory reuses the instance, and anything the context accumulated on the last
    request is still there on the next one.** `AddDbContextPool` exists to cut construction cost under
    load, but it works by resetting the context's own state, not any state a class built on top of it added
    — a field cached on a custom context subclass, a static-feeling value captured at construction, survives
    the reset and leaks from one caller's request into the next caller's. A pooled context stays a thin
    wrapper over the generated one, or the pooling that was meant to save allocation cost becomes a
    cross-request data bug instead.
18. **Split-query behaviour is a per-query decision as often as it is a global default.** Setting
    `UseQueryTrackingBehavior`-style split queries globally treats every query with more than one included
    collection the same way, but point 14's trade — several round trips with no shared transaction — is
    only worth paying where the row multiplication is actually large. `AsSplitQuery()` and
    `AsSingleQuery()` at the call site override the global default for the one query that needs it, which
    is the difference between a blanket policy and a decision made where the shape of the data is actually
    known.
19. **A `SaveChangesInterceptor` is the one place a cross-cutting write concern belongs, instead of copied
    into every place that calls `SaveChanges`.** Stamping an audit column, rejecting a save that violates an
    invariant no single entity can express, or turning a soft-delete flag into the update it actually is —
    each done once in an interceptor runs for every write path including the ones added after the
    interceptor was written, where the same logic pasted at each call site is a rule that's already out of
    sync the day a new call site forgets to paste it.
20. **A filtered or ordered include changes what a collection navigation returns, and doing it in the query
    is why it exists.** `Include(x => x.Children.Where(...).OrderBy(...))` (via the filtered-include syntax)
    applies the filter and the order in the generated SQL, which is one query producing exactly the rows
    the caller needs — loading the full collection and filtering it in memory after the fact defeats
    point 6's whole point, paying for every row the filter was about to discard.
21. **A compiled model trades a startup cost for a per-request one, and only pays off once the model is
    genuinely large.** EF Core builds the model that maps entities to the schema once, at startup, by
    reflecting over every entity type; a compiled model (generated ahead of time via
    `dotnet ef dbcontext optimize`) skips that reflection and can also work where dynamic model building
    can't, as under trimming or Native AOT (§9). It is generated code that has to be regenerated whenever
    the mapped model changes, which is a real cost of its own — worth carrying for a model large enough
    that startup time matters, not a default reached for on every project.
22. **A concurrency token (`[Timestamp]`/`RowVersion`, or a plain column mapped with
    `IsConcurrencyToken()`) is how a lost update is turned into a `DbUpdateConcurrencyException` instead of a
    silent overwrite.** Two requests loading the same row, editing different fields and saving in sequence
    otherwise both succeed — the second `SaveChanges` simply writes over the first's change, with no error
    anywhere naming what was lost. The token makes the second save fail loudly, at the point where the
    caller can still decide what "the row changed underneath you" should mean for this operation.
23. **A complex type or owned type maps a value object into the owner's own table without giving it an
    identity the rest of the schema can reference.** `ComplexProperty` (or `OwnsOne` for the entity-shaped
    predecessor) is how an address or a money amount stays a real .NET type with its own equality instead of
    flattening back into loose columns on the parent — reach for it whenever a value object (§4.12) would
    otherwise be represented as three or four separate scalar properties the mapping quietly re-groups by
    naming convention alone.
24. **A `ValueConverter` translates between the .NET type the domain wants and the column type the store
    actually has, and belongs in the model configuration, not in a property getter that runs the conversion
    by hand on every read.** An enum stored as its display string, a value object stored as its wrapped
    primitive, a `DateOnly` mapped where the provider still expects `DateTime` — configuring the conversion
    once means every query, projection and migration agrees on it, where a getter that converts on read still
    leaves `Where` clauses and raw column access seeing the untranslated stored value.
25. **Keyset pagination (`WHERE Id > @lastId ORDER BY Id LIMIT @n`) replaces offset-based paging
    (`Skip`/`Take`) once a table is large enough that `Skip` has to walk past everything it discards.** An
    OFFSET is not an index seek — the database still scans and discards every skipped row to find where the
    page starts, so page 500 costs proportionally more than page 1 even though both return the same number
    of rows; keyset paging seeks directly to the last-seen key, which is the same trade point 6 makes for a
    query in a loop, restated for the shape of a paged list rather than a relation.
26. **A configuration source's connection string is never the literal secret checked into `appsettings.json`
    — a placeholder is, and the real value comes from an environment variable, a secret store or user-secrets
    in development.** `appsettings.json` ships inside the published artefact and is readable by anyone who
    can open it, so a credential committed there is a credential leaked the moment the repository or the
    image is shared, independent of whatever access control the running service itself enforces.
27. **A keyless entity type (`HasNoKey()`, or a type mapped from a raw SQL view with no natural key) can
    never be tracked and is only ever read, never updated through the change tracker.** It exists for a
    database view, a stored-procedure result shape, or a report projection that has no single-row identity
    to track — reaching for it on a table that does have a key just to skip defining one removes the ability
    to update that entity through EF Core at all, which is a permanent limitation on that mapping, not a
    shortcut around modeling the key.
28. **A compiled query (`EF.CompileQuery`/`EF.CompileAsyncQuery`) is a different optimisation from the
    compiled model in point 21, and confusing the two means reaching for the wrong one.** The compiled model
    skips reflecting over the *schema* at startup; a compiled query instead caches the translation of one
    specific LINQ expression to SQL so that exact shape of query skips re-translation on every call — worth
    it for a query executed often enough that repeated translation shows up in a profile, and a second thing
    to keep in sync by hand: the compiled delegate captures the expression tree as written, so a query
    changed at the call site without touching the compiled declaration keeps running the old translation.
29. **Table splitting maps two or more entity types onto the same table, and loading one without the other
    is a decision the mapping makes for you, not a decision the query makes.** A large, rarely-read column
    group (a document's full text, a blob) split into its own entity sharing the parent's primary key lets a
    query for the parent skip that column by simply not including the split entity — but only if the split
    entity is genuinely optional to load, which means every read path has to know whether it needs the
    second half or is silently paying for a second round trip to get it when it turns out to.
30. **A shadow property tracked by EF Core but absent from the CLR type is invisible to any code that reads
    the entity directly, including a debugger inspecting the instance.** A foreign key EF Core infers from a
    navigation, or a column deliberately excluded from the class and configured through the fluent API only,
    still participates in queries, migrations and change tracking — but `object.Property` access doesn't see
    it, so a shadow property is the right tool for a column the domain genuinely has no business exposing and
    a source of "where did this column come from" the day someone reads the entity class expecting the
    schema to be fully described there.
31. **A global query filter applies to every query against that entity type, including one reached through
    a navigation the calling code never mentions.** Point 15 already covers a bulk statement bypassing the
    filter entirely; the filter's opposite failure is a query that includes it when the caller didn't expect
    to — an owned or table-split type sharing the parent's filter, or a self-referencing navigation that
    silently drops soft-deleted children out of a parent's own collection with no `Where` clause anywhere
    naming that behaviour. `IgnoreQueryFilters()` exists for the one query that legitimately needs the full
    set, and reaching for it has the same review weight as any other bypass of a rule the rest of the
    codebase assumes is always on.
32. **The command timeout and the connection timeout answer different questions, and a slow query fails
    against whichever one was actually configured.** The connection timeout bounds how long establishing a
    connection to the server may take; the command timeout bounds how long one executed command may run once
    connected — a provider's default command timeout (30 seconds for the SQL Server provider) is a
    per-command ceiling that a legitimately long report query hits regardless of how fast the connection
    itself opened, and raising the wrong one of the two leaves the real limit exactly where it was.
33. **A relational database's own feature (a JSON column, a computed column, an ignore-case collation) is
    provider-specific, and treating it as the default mapping is what makes a second provider a rewrite
    instead of a config change.** Mapping a property `ToJson()` in the relational sense, or relying on a
    server-computed column's exact type, ties the model to whichever provider actually implements that
    mapping; a codebase that has only ever run against one provider and mixes provider-specific mapping in
    with the ordinary model has already spent point 3's portability budget without a decision anyone made
    on purpose to spend it.
34. **`SaveChanges` batches multiple pending inserts, updates and deletes into as few round trips as the
    provider allows, and disabling batching is a real trade, not a free safety switch.** Turning batching off
    (or a provider defaulting to a small batch size) trades round trips for a smaller blast radius per
    statement sent, which matters where a very large single statement risks a timeout or a lock held longer
    than the equivalent set of smaller ones — reached for as a default rather than a response to a measured
    problem, it pays point 6's per-round-trip cost on every `SaveChanges` call for a save that was already
    one transaction (point 10) regardless of how many statements make it up.
35. **`AsNoTrackingWithIdentityResolution()` and a JSON-mapped collection navigation don't combine safely, and
    the platform now refuses the combination rather than returning a silently wrong result.** Identity
    resolution works by giving every row that maps to the same key the same object instance without the full
    change tracker behind it — a JSON column's nested collection is materialised as part of its parent's own
    document, with no independent row-per-child identity for the resolution logic to key on, so the two
    features used together used to produce a corrupted graph or an opaque deserialisation error depending on
    the shape. The fix is knowing the combination is restricted, not chasing the parse exception as though the
    query itself were malformed — a JSON-owning entity gets an ordinary `AsNoTracking()` instead.
36. **`ExecuteUpdateAsync` can now target a property nested inside a JSON column, where before the whole
    document had to be read back and rewritten through `SaveChanges` to change one field inside it.**
    Point 15's trade-off — a bulk statement bypasses the change tracker and everything wired to it — applies
    exactly the same way to a JSON-nested update as to an ordinary column: it's the right tool for changing
    one field across many rows without loading them, and it still means no interceptor, no domain event and
    no soft-delete filter runs for the write, so the same deliberate, filter-restated-by-hand discipline point
    15 asks for is not optional just because the target happens to be JSON instead of a column.
37. **`ExecuteUpdateAsync` accepting a plain lambda, not only an expression tree the query provider has to
    parse, changes what a conditional or a dynamically-built update can look like.** A set of property/value
    pairs decided at run time — which columns to touch depends on which fields a caller actually sent — used
    to force building the setter expression tree by hand, one `SetProperty` call reflected together; a plain
    lambda is ordinary C# the method evaluates directly, which is simpler exactly where the update shape
    itself is the variable part and not where the query being updated is, so it doesn't change point 8's
    "check what runs on the server" caution for the `Where` clause selecting which rows are touched.
38. **A complex type mapped onto the owner's table (point 23) can silently collide with another property's
    column name, and column uniquification is what turns that collision into two distinct columns instead of
    one property quietly overwriting another's storage.** Two properties from different complex types (or a
    complex type and an ordinary scalar) that would otherwise map to the same column name are now
    disambiguated by an appended number rather than merged — worth knowing precisely because the old
    behaviour was not an error: it wrote both properties to one column and the one saved last silently won,
    a bug that reads as two independent fields until the data is inspected sideways.
39. **A compiled model (point 21) no longer needs its own `UseModel` call wired into the context's
    configuration when the compiled model sits in the same project as the `DbContext` that uses it — the
    provider detects and applies it automatically.** The generated model still has to be regenerated by hand
    whenever the mapped model changes (point 21's own caveat stands), but the wiring cost that used to make a
    compiled model feel like a separate opt-in configuration path is gone for the common case, which removes
    one more reason a large-model project defers adopting it past the point startup time actually matters.
40. **Querying directly into a JSON column's nested structure — filtering or projecting a field inside the
    document without first loading and deserialising the whole column — is a capability the relational
    JSON mapping only grew after point 33 was written, and it is still exactly as provider-specific as the
    rest of that point describes.** A `Where` clause reaching into a JSON property translates to the
    provider's own JSON path syntax, which means the portability budget point 33 already warns about is spent
    a second time the moment a query — not just a mapping — depends on one provider's JSON functions being
    present.
