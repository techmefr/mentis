# doctrine-migrations-pitfalls §3 — Versions and the version table

> Part 3 of `skills/doctrine-migrations-pitfalls`. Read it when a version name is custom, a migration has to be
> marked applied, or history is squashed. Sourced from the Doctrine Migrations documentation (commit
> `eb0b9ce`): `docs/en/reference/version-numbers.rst`, `managing-migrations.rst`, `generating-migrations.rst`
> and `configuration.rst`, read 2026-10-16. Names are the library's. Sentences marked "own guidance" are ours.

1. **Keep the generated `Version{date}` name.** Generated classes are named `Version` plus a `YmdHis` date, and
   the page says this format is important because it lets migrations be ordered correctly. Since version 1.5
   the library sorts the version names as strings, so custom names such as `Version1`, `Version2` and
   `Version10` end up in the order 1, 10, 2, which the page says may cause damage to a database. It strongly
   recommends the generated format. If a custom number is unavoidable, it should be as long as the date format
   and left-padded with zeros (the page's example is `Version00000000000010`, 21 characters in total, the same
   as a generated name). Moving to that format after migrations have been applied may need manual changes to
   the version table, the page warns.
2. **Editing the version table changes what runs next.** The `version` command with `--add` or `--delete`
   marks a migration as applied or not without executing anything. The page's caution: delete a version and
   run `migrate`, and that migration runs again. Own guidance: after a failed run on MySQL (part 1), find out
   which statements took effect first, and prefer a corrective migration to a hand edit; record any manual
   edit in the change that made it.
3. **Check the table configuration before relying on it.** The version table's name and columns are settings
   (`table_storage`): the default table is `doctrine_migration_versions`, the version column holds up to 191
   characters by default, and executed time and duration are stored in their own columns. Own guidance:
   a long namespace-and-class name must fit the configured length.
4. **Several namespaces are a feature, with a catch.** `migrations_paths` maps a PHP namespace to a directory,
   and more than one pair is allowed, as the page's example shows. The `organize_migrations` setting can put
   classes under year or year-and-month subdirectories. Own guidance: because versions sort as strings across all
   paths, a second component's migrations interleave with the first by date, so decide who owns the schema
   before adding a path.
5. **Squash with a fresh diff, then roll up.** To replace many historical migrations with one, the page says
   to delete or archive the old files, run `diff` with `--from-empty-schema` to generate one migration that
   builds the whole schema as if the database were empty, and use the `rollup` command to synchronise the
   version table of a database that is already up to date. Own guidance: do it only when every database that
   matters is at the latest version, and test the squashed migration on an empty database and the rollup on a
   copy of a real one.
6. **Pin migrations by hand only on purpose.** The `migrations` setting lists classes explicitly instead of
   having them discovered. Own guidance: a class left off that list is never run, and nothing warns.
