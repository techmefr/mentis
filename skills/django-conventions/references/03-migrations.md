# § 3 — Migrations

> Section 3 of `skills/django-conventions`. Read it when a model change needs a migration, when data is changed
> by a migration, when a migration touches another app, or when CI is set up to guard the migration state. Read
> 2026-10-02 from the Django migrations topic and the `django-admin` reference (development docs) and from the
> PostgreSQL documentation for `CREATE INDEX`.

1. **Migrations are generated from the models, named, and read.** `makemigrations` writes them; give a
   migration a meaningful name with `--name` when the generated one says nothing; read the SQL a migration
   will run with `sqlmigrate` before it reaches a database someone else guards. Committing the migration with
   the model change keeps the two from drifting.
2. **CI fails when the state is inconsistent.** `makemigrations --check` exits non-zero when model changes have no
   migration (it implies a dry run); `migrate --check` exits non-zero when migrations are unapplied; and
   `check --deploy` against the production settings module is the deployment checklist as a command (§4.1),
   with `--fail-level` to choose the severity that breaks the build. These are three cheap jobs that replace
   three kinds of review.
3. **In a data migration, use the historical models, never the real ones.** The function given to `RunPython`
   receives an app registry holding the models as they were at that point in the history; fetch them with
   `apps.get_model`. Importing the real model works today and fails the day a new installation replays the
   whole history on a model that has since changed, which is the day nobody remembers writing it. The same
   holds for database-router `allow_migrate` code.
4. **Data migrations are separate migrations from schema migrations,** written by hand (`makemigrations
   --empty`), and reversible: give `RunPython` a second callable for the backward direction, otherwise
   migrating backwards raises. A migration that cannot be reversed says so by omitting it, on purpose.
5. **A migration that reads another app's models depends on that app's latest migration,** or the model lookup
   fails with `LookupError: No installed app with label ...` at run time. Dependencies are the only ordering
   the framework knows; an inconsistent history (a migration applied whose dependencies are not) makes the
   framework refuse to migrate at all, which is the correct response and a sign the dependency is wrong.
6. **Atomic by default, non-atomic by declaration.** On databases with transactional DDL each migration runs in
   a transaction. A migration containing an operation the database refuses inside a transaction (building a
   PostgreSQL index concurrently is one) sets `atomic = False`, and then is not atomic: a failure half-way
   leaves the first part applied, so keep it to that one operation. A failed concurrent index build leaves an
   invalid index behind that must be dropped before retrying. Use `atomic()` inside the non-atomic migration
   for the parts that should still be all-or-nothing.
7. **Squash when the count gets unwieldy, not before.** Migrations are cheap and Django copes with hundreds;
   squashing replaces a run of them with one that represents the same changes, and then the old files and
   the stale rows (`migrate --prune`) are removed together.
8. **Old migrations keep importing what the project later deletes.** A validator function, a custom field class
   or a manager referenced from a migration must stay importable as long as the migration exists. When a
   custom field is removed from the project, leave a stub of it (it needs only to subclass what it did and
   report its internal type) until the migrations that reference it are squashed away; and a manager that must
   exist inside `RunPython` declares `use_in_migrations = True`.
