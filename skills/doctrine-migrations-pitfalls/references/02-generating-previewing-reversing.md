# doctrine-migrations-pitfalls §2 — Generating, previewing and reversing

> Part 2 of `skills/doctrine-migrations-pitfalls`. Read it when a migration is generated, reviewed or rolled
> back. Sourced from the Doctrine Migrations documentation (commit `eb0b9ce`):
> `docs/en/reference/generating-migrations.rst`, `managing-migrations.rst`, `migration-classes.rst` and
> `configuration.rst`, read 2026-10-16. Names are the library's. Sentences marked "own guidance" are ours.

1. **A diff migration drops what Doctrine does not know about.** The `diff` command compares the database
   with the mapping and writes the SQL for the difference. The documentation's own example output contains a
   `DROP TABLE` for a table that was created by an earlier migration and is not mapped, and a note explaining
   that the command detects the unmapped table and generates SQL to drop it. Read every generated statement
   before running it.
2. **Tell the tool about tables it does not manage.** The page says that for custom tables not managed by
   Doctrine, every `diff` will try to drop them unless a schema filter is set: a callback on the connection's
   configuration (`setSchemaAssetsFilter`) that returns false for names to ignore, its example excluding names
   prefixed `t_`. The page says a Symfony bundle exposes a `schema_filter` option for the same purpose.
3. **Preview before executing.** `migrate --dry-run` prints the SQL that would run without sending it. The
   `--write-sql` option writes the statements, including the insert into the version table, to a file instead
   of executing them from PHP (a file path, a directory, or nothing for the default name). The page's reason:
   capture the SQL, perhaps adjust it, and deploy it later across several database servers. Own guidance:
   attach the output to the change that adds the migration, so the review is of the SQL and not the class.
4. **Know the prompts.** Without `--no-interaction`, `migrate` and `execute` warn that the run could change the
   schema and lose data and ask to continue; with it the run is unattended. Own guidance: use the flag only
   where the SQL has already been previewed.
5. **Read the generated `down` and make an irreversible one say so.** A generated `down` for a dropped table
   recreates the table definition; own guidance: that restores structure, not the rows. For a migration that
   cannot be reversed the library provides `throwIrreversibleMigrationException()`, with an optional message,
   for the `down` method. Never leave a `down` empty or auto-generated and unread; test a rollback on a copy
   of real data before the change is released.
6. **Guard against the wrong platform.** Generated migrations start with an `abortIf` that refuses to run
   unless the database platform is the one the SQL was written for; the `check_database_platform` setting
   (default true) controls whether this check is added to generated code. `abortIf` aborts, `skipIf` skips the
   migration and `warnIf` only warns. Own guidance: keep the guard on any migration that contains
   platform-specific SQL.
7. **Run one migration, forwards or backwards, to test it.** The `execute` command with `--up` or `--down` runs
   a single migration class, and the generator prints the exact command. `migrate first` reverts all of them,
   and the aliases `prev`, `next` and `latest` move one step or to the end. Own guidance: use `execute --down`
   to prove a rollback before relying on it.
8. **Pre and post hooks exist.** `preUp`, `postUp`, `preDown` and `postDown` run around the main method. Own
   guidance: keep checks of the data a migration depends on in `preUp` with `abortIf`, so a migration refuses
   before it has changed anything.
