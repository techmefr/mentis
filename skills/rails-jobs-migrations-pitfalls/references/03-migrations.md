# rails-jobs-migrations-pitfalls §3 — Migrations

Source: the strong_migrations README (2.8.0, MIT), read 2026-10-08. The rules are for PostgreSQL unless stated;
the README has separate MySQL and MariaDB sections that were not mapped. The generic expand and contract
discipline for live schema changes is `deprecation-migration` §3; this section only maps it to Rails calls.

## 3.1 Columns and constraints
1. **Remove a column in two deploys.** First ignore it in the model (`self.ignored_columns += ["name"]`) and deploy,
   because Active Record caches attributes; then drop it in a migration wrapped in `safety_assured`.
2. **Add a foreign key or a check constraint without validating,** `add_foreign_key ..., validate: false` or
   `add_check_constraint ..., validate: false`, then validate in a separate migration with `validate_foreign_key` or
   `validate_check_constraint`.
3. **Set `NOT NULL` through a check constraint.** `change_column_null` on an existing column blocks reads and writes
   while every row is checked. Add `IS NOT NULL` as an unvalidated check, validate it in a second migration, then set
   `NOT NULL` and drop the check in the same migration as the validation.
4. **Use `jsonb`, not `json`,** for new columns; the README says to use `jsonb` instead.
5. **Add a volatile default in two steps.** A volatile default on an existing table rewrites the whole table and
   blocks reads and writes. Add the column without a default, change the default, then backfill the existing rows.
6. **`force: true` on `create_table` can drop an existing table.** Do not use it in a migration.

## 3.2 Indexes and references
1. **Add an index concurrently:** `algorithm: :concurrently` with `disable_ddl_transaction!` at the top of the
   migration. Without the latter the migration fails. Indexes on tables created in the same migration need neither.
2. **`add_reference` creates an index too,** so it needs the concurrent form,
   `add_reference :users, :city, index: {algorithm: :concurrently}`, under the same `disable_ddl_transaction!`.

## 3.3 Backfills and timeouts
1. **Never backfill in the migration that alters the table.** Active Record wraps a migration in a transaction, so
   the table stays locked for the length of the backfill. Backfill in batches, throttled, outside a transaction (a
   separate migration with `disable_ddl_transaction!`, or the console). The README says the tool does not detect
   dangerous backfills, so review them by hand.
2. **Set lock and statement timeouts for migrations** (`StrongMigrations.lock_timeout`, `statement_timeout`) or on
   the database role that runs them. **Behind a connection pooler in transaction mode the timeouts must be set on
   the database user,** as the README states.
3. **Set timeouts for the application too** in `database.yml` (`connect_timeout`, and under `variables`
   `statement_timeout` and `lock_timeout`), so a hung query does not hold a connection. The same pooler caveat
   applies.
4. **`safety_assured` marks a step as reviewed; it does not make it safe.** The README says to wrap a step in it
   only after the safe steps above. Treat every use as a question for the reviewer (own guidance on review).
