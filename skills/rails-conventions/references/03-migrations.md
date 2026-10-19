# § 3 — Migrations and the schema

> Section 3 of `skills/rails-conventions`. Read it when a migration is written, when a column, an index or a
> constraint is added to a table that already holds rows, or when a model validation depends on a column. The
> PostgreSQL index behaviour below is from the PostgreSQL documentation for `CREATE INDEX`; the rest from the
> Rails style guide, the Rails migrations guide and the rubocop-rails cops, as read on 2026-10-02.

1. **The schema file is source.** Keep `schema.rb` (or `structure.sql`) in version control, and initialise an
   empty database from it (`db:schema:load`, or `db:prepare`, which is safe to run repeatedly) instead of
   replaying every migration ever written. Old migrations break as the code around them moves; the schema
   file does not.
2. **Defaults and `NOT NULL` live in the migration, not only in the model.** Most non-trivial databases are
   touched by something other than this application (another service, a script, a console), and a default
   enforced only in Ruby is absent for all of them.
3. **A boolean column has a default and `NOT NULL`.** Without them it is three-valued (true, false, null), and
   SQL's three-valued logic makes `true AND NULL` null, not false: queries return the wrong set without any
   error.
4. **Foreign keys are real constraints, and they are named.** Add them in the migration and give them an
   explicit name rather than leaving it to the generated one, so that the migration that removes them is
   readable and two environments do not diverge on the name.
5. **Use `change` for constructive migrations, and only reversible commands inside it.** When a step cannot be
   reversed automatically, write `up` and `down`, or wrap the step in `reversible`. A migration whose
   rollback raises half-way is worse than one that says it cannot be rolled back.
6. **`add_column` takes no `index:` option, and does not complain when given one.** The index silently never
   exists; add it with `add_index`. Several alterations to one table in one migration are combined into a
   single `ALTER` with `change_table ..., bulk: true` (MySQL, and PostgreSQL since Rails 5.2).
7. **A uniqueness validation gets a unique index in the same change** (§2.9). Without it the validation races
   and duplicates get in, and the validation's `SELECT` scans the table.
8. **Adding a `NOT NULL` column to a table that has rows takes three steps:** add it nullable (or with a
   default), backfill, then add the constraint. Adding it constrained and without a default fails on the
   existing rows. A new table can use `NOT NULL` freely.
9. **A migration does not depend on application models.** If it needs a model, define a minimal class inside
   the migration, so that renaming or changing the real model next year does not break an old migration.
   Never call the real model's validations or callbacks from one.
10. **Writes to a live table are an online operation.** MySQL accepts `algorithm:` and `lock:` options on
    column and index operations (`algorithm: :instant`, `lock: :none`) to avoid blocking reads and writes.
    PostgreSQL builds an index without blocking writes with `algorithm: :concurrently`, which does two scans
    of the table and waits for old transactions; it cannot run inside a transaction block, so such a migration
    declares `disable_ddl_transaction!`; and a failed concurrent build leaves an `INVALID` index behind that
    still costs on every write: drop it and run again (or reindex concurrently). Only one concurrent build can
    run on a table at a time.
11. **A migration with `disable_ddl_transaction!` is not atomic.** If it fails half-way, the parts that
    succeeded stay; write it so that re-running it is safe, and keep it to one operation.
12. **Do not name a column after an Active Record method** (`save`, `saved`, and the like): it shadows the
    method the framework calls. Comments on tables and columns (`comment:`) are worth the line where the name
    cannot carry the meaning.
