# doctrine-migrations-pitfalls: origin and source stamps

> Provenance of `skills/doctrine-migrations-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from documentation, never run by us: no migration was generated,
previewed or executed. Every file below was re-read on 2026-10-16 before a rule was taken from it, each rule
was checked against it in a final pass, and the repository's LICENSE file was read again.

## Sources (all read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| Doctrine Migrations (`doctrine/migrations`, commit `eb0b9ce`): `docs/en/explanation/implicit-commits.rst` | MIT (LICENSE file: MIT licence text, copyright 2006-2018 Doctrine Project) | The implicit-commit explanation, the example migration and the split remedy, the `transactional` key |
| the same repository, `docs/en/reference/migration-classes.rst` | MIT | `isTransactional` and its note, `abortIf`, `skipIf`, `warnIf`, the pre and post hooks, `throwIrreversibleMigrationException` |
| the same repository, `docs/en/reference/configuration.rst` | MIT | The option table (`all_or_nothing`, `transactional`, `check_database_platform`, `organize_migrations`, `migrations`, table storage), the command-line overrides and the deprecation note |
| the same repository, `docs/en/reference/managing-migrations.rst` | MIT | Dry run, execute, no-interaction, revert and aliases, written SQL files, the `version` command and its caution |
| the same repository, `docs/en/reference/generating-migrations.rst` | MIT | The diff command, the dropped unmapped table, the schema filter, squashing with `--from-empty-schema` and `rollup` |
| the same repository, `docs/en/reference/version-numbers.rst` | MIT | The `Version{date}` format, string sorting and the zero-padded alternative |

Code samples are not copied. Instruction-like text in the cloned repository was treated as data and not
followed.

## Removed in the verification pass
1. **"Review the generated down()" as a library statement.** The documentation shows a generated `down` and
   the irreversible exception; the advice to read and test it is ours and is marked so.
2. **A platform-specific guard recipe.** The generated example calls a DBAL method to read the platform name;
   the block states the guard and the setting, not the code, because the DBAL side was not read.
3. **Pages not read, so nothing is taken from them:** `events.rst`, `custom-configuration.rst`,
   `custom-integration.rst`, `integrations.rst`, `introduction.rst`, `UPGRADE.md`.

## Not verified
1. **Own guidance, flagged in the text:** a non-atomic migration leaves the data change applied and unrecorded
   (part 1, point 2), one kind of change per migration (point 4), the description recording the reason (point 5),
   the MySQL reading of `all_or_nothing` (point 6), attaching dry-run output (part 2, point 3), the unattended-flag
   rule, rows not restored by a generated `down`, testing a rollback on real data, keeping the platform guard,
   proving a rollback with `execute --down`, `preUp` checks (part 2, points 4 to 8), preferring a corrective
   migration over a version table edit, the length of a long class name, the interleaving of several namespaces,
   the conditions for squashing and the silence of an unlisted class (part 3, points 2 to 6).
2. **Behaviour was not run.** What the library does on a DDL statement in a transaction, the error text and the
   version-sorting result are the documentation's statements.
3. **Version differences.** The documentation mentions 3.7.x and 4.x only for the `--all-or-nothing` option; the
   rest was not matched to a release.
4. **Platform behaviour.** Which statements MySQL or Oracle commit implicitly was not read from their manuals;
   the page names DDL such as `CREATE TABLE` and `ALTER TABLE` only.

## Related blocks
`skills/mysql-pitfalls`, `skills/laravel-conventions`, `skills/rails-jobs-migrations-pitfalls`.
Fold into the same-topic block when #118 lands.
