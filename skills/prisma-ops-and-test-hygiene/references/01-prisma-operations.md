# prisma-ops-and-test-hygiene §1 — Prisma operations

An ORM client is a connection pool, a query generator and a migration tool. Each has a default that suits a
laptop. Rules carry the Prisma major version they hold for; check yours first.

## 1.1 The connection pool
1. **Know the size.** Prisma 6 sizes the pool as the number of physical CPUs times two plus one. Prisma 7
   with driver adapters uses the driver's own default, 10 in the adapters documented (`max` for the
   Postgres driver, `connectionLimit` for MySQL, `pool.max` for SQL Server). Set it explicitly.
2. **The pool cannot exceed what the database allows**, and every replica has its own pool. Replicas times
   pool size must stay under the server's connection limit with room for migrations and admin sessions.
3. **Serverless multiplies it**: each short-lived instance opens its own pool. Put an external pooler
   (PgBouncer or the provider's) in front and keep the in-process pool small.
4. **Create one client per process**, share it through DI (see `nestjs-di-traps`), and disconnect it in the
   shutdown hook; one client per request or per test file exhausts the server.
5. **Observe it**: connections in use on the database side during a load test, not only the setting.

## 1.2 Seeing the queries
1. **Log queries as events**, not to stdout in production: configure the client to emit the `query` level as
   an event and subscribe with `$on('query', ...)`, which gives the SQL, parameters and duration. This is
   documented for Prisma 7; check the older major's logging section before using it there.
2. **Record the duration** as a metric and log only the slow ones (a threshold you pick); parameters can hold
   personal data, so do not ship them to a log by default.
3. **Look for N+1 first**: many identical short queries in one request is the usual cause of a slow endpoint.
   Use relation loading in one query, or batch by id (see `nestjs-node-conventions`).

## 1.3 Middleware is gone: use extensions
1. **The client middleware API (`$use`) was removed in Prisma 7.** Code that used it for logging, timing,
   soft delete or tenant filtering has to move to client extensions.
2. **Query extensions** (`$extends` with `query: { $allModels: { $allOperations ... } }`) wrap every
   operation the way middleware did, with typed arguments. Keep cross-cutting rules (tenant filter,
   soft-delete filter) here once, not repeated at call sites.
3. **An extended client is a new object.** Provide the extended instance through DI, not the base one, or the
   rule is silently skipped.
4. **Other version-7 changes that affect operations**: driver adapters are required; the datasource URL
   and shadow database URL live in the Prisma config file; the separate direct-connection URL setting is
   removed; automatic seeding after migrate is removed; several CLI flags (`--skip-generate`, `--skip-seed`,
   `--schema`, `--url`) are removed. Scripts and CI that pass them break.

## 1.4 Read the migration before it runs
This is the workflow for Prisma up to 7: the tool generates a SQL file from the schema diff. Prisma ORM 8's
documentation describes a different, TypeScript-based migration workflow; if you are on 8, apply the same
review to what that workflow produces (its plan and the operations it will run) and treat the statements
below as the risk list. The statements and their behaviour were not checked against the newest major.
1. **A rename may be generated as a drop and an add.** Renaming a field looks like a rename in the schema
   and arrives as `DROP COLUMN` plus `ADD COLUMN`: the data is gone. Generate with the create-only option,
   then edit the SQL to a real `RENAME COLUMN` before applying.
2. **Optional to required adds `SET NOT NULL` with no backfill.** It fails on any null row or, worse,
   succeeds on a table that happened to have none in the test database. Add the column nullable, backfill,
   then enforce, in separate migrations.
3. **Enum changes can recreate the type**, rewriting or locking columns that use it.
4. **Risk list to scan for in every migration**: `DROP COLUMN`, `DROP TABLE`, `ALTER COLUMN ... TYPE`,
   `SET NOT NULL`, a new `UNIQUE` constraint (fails on duplicates), a default added to an existing column on
   an old PostgreSQL (pre-11 rewrites the table), a foreign key without a supporting index, and
   `CREATE INDEX` on a large table.
5. **Build large indexes concurrently** (`CREATE INDEX CONCURRENTLY` in PostgreSQL), which cannot run inside a
   transaction block, so that migration must be run without a transaction wrapper.
6. **Expand and contract** for any change an old and a new application version must both survive during a
   rolling deploy: expand (add the new column or table, write to both), migrate data, switch reads, then
   contract (drop the old) in a later release. Never drop what the previous release still reads.
7. **Index foreign keys**: the database does not do it for you, and joins and cascades scan without it.
8. **Pre-apply checklist**: backup or restore point exists, the SQL was read, risky statements were named,
   the migration was rehearsed on a copy with realistic row counts, the previous application version still
   works against the new schema.
9. **Apply from CI or a release job**, with the production-safe command (apply pending, never the
   development one that can reset), not from a developer machine.

## 1.5 Verification
- Connections on the database during a load test are below the server limit with margin.
- A slow query was found from the event log, not guessed.
- The SQL of the last migration was read and every risky statement from §1.4.4 was named in the review.
- The migration ran on a copy with production-sized data and its duration was recorded.

## 1.6 Nest mapping
Provide the (extended) client through a module and disconnect it in `onModuleDestroy`; see
`nestjs-di-traps` for the injection mistakes and `nestjs-reliability` §3 for writing a message with the
same transaction as the data change.
