---
name: doctrine-migrations-pitfalls
description: "Use when writing, generating or running schema migrations with doctrine/migrations (PHP): migrations that are not atomic because MySQL and Oracle commit DDL implicitly (isTransactional, the transactional and all_or_nothing settings, splitting data changes from DDL), generated diff migrations that drop tables Doctrine does not map, dry runs and written SQL files, platform guards with abortIf, irreversible down methods, version class names that sort wrongly as strings, and the version table commands that can re-run or skip a migration."
---

# doctrine-migrations-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the Doctrine Migrations library on its own, whether it is driven
from its console or from a framework bundle. The three sections share one premise: **a migration tool records
that a migration ran, not that the database changed as the class says**, so every convention here is about
the gap between the two: the transaction that is not one, the diff that decides on its own, the version
string that sorts differently from the date. MySQL behaviour that makes some schema changes copy a table is in `skills/mysql-pitfalls`; Laravel's own
migrations are in `skills/laravel-conventions`.

## When
- Writing or reviewing a migration class, or a `migrate` or `diff` run in a pipeline.
- A migration failed half way and the database is in a state nobody can describe.
- A generated migration contains a statement nobody wrote (a dropped table, a changed column).
- Migration class names are not the generated `Version{date}` form, or a version row is edited by hand.

## Steps

**Read only the section the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Transactions and implicit commits: DDL on MySQL and Oracle, `isTransactional`, `transactional`, `all_or_nothing`, splitting data from DDL | a migration mixes DDL and data changes, or a failed run left a half-applied state | [`01-transactions-and-implicit-commits.md`](./references/01-transactions-and-implicit-commits.md) |
| 2 | Generating, previewing and reversing: the diff command, tables Doctrine does not map, dry run, SQL files, guards, `down` | a migration is generated, reviewed or rolled back | [`02-generating-previewing-reversing.md`](./references/02-generating-previewing-reversing.md) |
| 3 | Versions and the version table: class names and string sorting, the `version` command, merging old migrations | a version name is custom, a migration must be marked applied, or history is squashed | [`03-versions-and-version-table.md`](./references/03-versions-and-version-table.md) |

## Output / checkpoint
For a migration that is going to run against shared data: the SQL it will send was read (`migrate --dry-run` or
a written SQL file), statements that cannot be rolled back were identified (part 1), the `down` method was
read and either works or says so (part 2), and the version table was not edited by hand. Evidence is the
dry-run output attached to the review and a run against a copy of the data that was also run backwards.

## Guardrails
- Never put data changes and DDL that cannot be rolled back in one migration class and expect atomicity
  (part 1, point 2).
- Never run a generated diff migration unread; a table Doctrine does not map is dropped by it (part 2,
  point 1).
- Never rely on `down` that was generated and never run; read it, and make an irreversible one say so (part 2,
  point 5).
- Never use short, unpadded version numbers (part 3, point 1).
- Never delete or add a version row to "fix" a failed run without knowing which statements were applied
  (part 3, point 2).
- This block states the library's documentation at the commit in
  [`references/origin.md`](./references/origin.md). No migration was run while writing it, and the 3.x and
  4.x differences were not checked.

## Origin
Rewritten from the Doctrine Migrations documentation (MIT), read 2026-10-16. 🟡: never run by us; open points
are in [`references/origin.md`](./references/origin.md).
