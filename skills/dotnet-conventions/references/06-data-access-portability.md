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
   without waiting.
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
