# dotnet-aspnet-efcore-pitfalls §3 — EF Core

The broad data-access rules are in `dotnet-conventions` §6. Version notes are given where the
documentation gives them.

## 3.1 Tracking
1. **Only tracked entities have their changes persisted by `SaveChanges`.** Queries that return entities
   track by default. If you set a no-tracking default for the context, entities you load and edit are not
   persisted: opt in with `AsTracking` on every query that feeds a write, or keep tracking on and use
   `AsNoTracking` on read-only queries.
2. **A no-tracking query can still resolve identity** within its own results (the identity-resolution
   variant), when the same row appears several times.

## 3.2 Migrations at startup
1. **Prefer a separate deploy step to `Migrate` at application start.** The documentation lists the
   trade-offs of applying migrations in the app: elevated schema permissions, no inspection of the SQL,
   manual rollback; it prefers a migration bundle or a SQL script when review or approval is needed.
2. **From EF Core 9, `Migrate` and `MigrateAsync` take a database-wide lock** before applying migrations,
   so concurrent instances no longer apply them at the same time; for earlier versions the documentation
   warns that concurrent instances can fail or corrupt data.
3. **Do not call `EnsureCreated` before `Migrate`.** `EnsureCreated` bypasses migrations, and `Migrate`
   then fails.

## 3.3 Buffering
1. **Avoid `ToList` or `ToArray` when you intend to use another LINQ operator on the result.** It
   needlessly buffers all results in memory; keep operators on the query and enumerate once.
2. **EF buffers internally in two cases:** when a retrying execution strategy is on, and, for a split
   query, for all but the last result set unless MARS is enabled on SQL Server. This buffering is in addition
   to your own `ToList`. Page or stream large reads deliberately.

## 3.4 Indexes
1. **A filter over an expression on a column cannot use a simple index** (the documentation's example is
   `price / 2`). Define a stored computed column for the expression and index that, or compare the raw
   column.
2. **Look at the query plan of a slow query** in the database's own tooling; indexing rules are general
   database knowledge.

## 3.5 Logging, tags and lazy loading
1. **Never leave `EnableSensitiveDataLogging` on in production.** By default EF leaves data values out of
   exception messages because they may be confidential; the option puts them in.
2. **Set the log level on purpose.** EF simple logging includes everything from `Debug` up by default; pass
   a higher minimum level to cut volume.
3. **Tag queries** with `TagWith` (or `TagWithCallSite`) so a slow statement found in the database can be
   traced to its call site.
4. **Lazy-loading proxies make each navigation read a database query.** The performance page treats
   eager loading as the better default when you know what you need; prefer `Include` or a projection.

## Verification
- A write test reloads the entity from a fresh context and asserts the change.
- The deploy runs the bundle against an empty database and against the previous release's schema.
- The generated SQL of the hot queries is read once (`ToQueryString`) and matches an index.
