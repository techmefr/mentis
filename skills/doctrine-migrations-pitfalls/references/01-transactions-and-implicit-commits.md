# doctrine-migrations-pitfalls §1 — Transactions and implicit commits

> Part 1 of `skills/doctrine-migrations-pitfalls`. Read it when a migration mixes DDL and data changes, or a
> failed run left the database half changed. Sourced from the Doctrine Migrations documentation (commit
> `eb0b9ce`): `docs/en/explanation/implicit-commits.rst`, `docs/en/reference/migration-classes.rst` and
> `docs/en/reference/configuration.rst`, read 2026-10-16. Names are the library's. Sentences marked "own
> guidance" are ours.

1. **By default each migration is wrapped in a transaction.** The configuration reference lists
   `transactional` (default true) as wrapping migrations in a transaction, and `all_or_nothing` (default
   false) as wrapping multiple migrations run together in a single one, so that if one fails they are all
   rolled back. A migration class can opt out with `isTransactional()` returning false.
2. **On MySQL and Oracle a DDL statement commits the transaction first.** The explanation page says these
   platforms do not support DDL in transactions: `CREATE TABLE`, `ALTER TABLE` and the like end the
   transaction that was open, before they run. The documentation's own example puts several `UPDATE`
   statements and then a `CREATE TABLE` in one migration: the updates are committed on their own, the table is
   created outside any transaction, and the library then tries to commit a transaction that no longer exists.
   Own guidance: such a migration is not atomic, so a failure after the DDL leaves the data change applied and
   the migration unrecorded.
3. **The "no active transaction" error is this problem, made visible.** The page says that since PHP 8 a driver
   such as PDO for MySQL reports an error that was silent before: `There is no active transaction`. It says the
   library currently checks for an active transaction before committing, so the error should not appear, but
   that this will not hold in the next major version and projects should prepare. Own guidance: if you see
   the message, the cause is a DDL statement in a transactional migration, not the library.
4. **Split data changes from DDL.** The page's remedy for keeping the data statements in a transaction: two
   migrations, the first with the `UPDATE` statements and the second with the `CREATE TABLE` and an
   `isTransactional()` that returns false. Own guidance: one migration, one kind of change, so a failure
   names which kind was left behind.
5. **Say so when a migration is not transactional.** Set `transactional` to false and new migrations are
   generated with the override, making them non-transactional by default (the page's words). The page also
   cautions that `isTransactional()` does not guarantee that statements run in one transaction on these
   platforms and tells you to read your platform's manual. Own guidance: put the reason in the migration's
   `getDescription()` so a reviewer sees that atomicity was given up on purpose.
6. **`all_or_nothing` only helps where DDL is transactional.** The configuration page notes it works only if the
   database supports transactions for DDL statements. Overrides on the command line are `--all-or-nothing` and
   `--no-all-or-nothing`; the page says passing a value to the first is deprecated from 3.7.x and not allowed
   in 4.x. Own guidance: on MySQL, treat it as no protection against a failure after DDL, and plan the
   recovery of a half-applied run in advance (part 2, point 3).
