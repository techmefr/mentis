# § 2 — Keys, constraints, and NULL

> Section 2 of `skills/sql-conventions`. Read it when a key, a constraint, a foreign key or a nullable column
> is written. The database is the last place an invariant can be enforced for every writer at once; a rule
> that lives only in application code is a rule that the next script, import or second service will not follow.

1. **Put the invariant in the database when more than one writer exists or ever will.** Not-null, unique,
   check, foreign key and exclusion constraints cost almost nothing and hold against every path in. The
   application validates for the user's benefit (a readable message); the constraint is for the data's
   benefit. A race that "can't happen because the code checks first" is exactly what a unique constraint
   catches.
2. **Declare not-null by default and make nullable the exception that has a meaning.** Null means "unknown or
   absent", and every nullable column forces every reader to handle three-valued logic. Give common values a
   default.
3. **Know what null does to a check and to uniqueness.** A check constraint passes when its expression is
   true *or null*, so `CHECK (price > 0)` allows a null price; pair it with not-null. A unique constraint
   treats nulls as distinct by default, so two rows with the same key and a null in one column both pass.
   PostgreSQL 15 added the option to treat nulls as equal in a unique constraint; on other engines and
   versions a unique index over an expression or a partial unique index achieves it. State which behaviour you
   want.
4. **Index the referencing side of a foreign key yourself, on PostgreSQL.** The referenced columns always have
   an index (they are a key); the referencing columns do not get one automatically. Without it, a delete or a
   key update in the parent scans the child table for matches. MySQL/InnoDB creates the index for you when none
   exists (§7.1).
5. **Choose the foreign-key action on purpose, and prefer refusing.** Restricting the parent's delete is the
   safe default. Cascading delete turns one statement into an unbounded cascade across tables, bypasses every
   application hook and audit, and surprises whoever runs a clean-up (`skills/laravel-no-cascade-delete` is the
   stack-level statement). Setting null or a default is a modelling decision that needs the column to allow it.
6. **A key is chosen for stability, not meaning.** A surrogate key never changes; a natural key (an email, a
   code) changes when the business does and drags every reference with it. Keep the natural key as a unique
   constraint next to the surrogate. A pure join table's primary key is the pair of its two ids, which also
   forbids duplicates.
7. **An overlap or exclusivity rule is an exclusion constraint, not a check-then-insert.** A booking that must
   not overlap another, or a period that must not overlap its sibling, is expressed once in the schema on
   engines that support it (PostgreSQL's exclusion constraints). Elsewhere, serialise the writers on a parent
   row (§4.4) rather than trusting a read.
8. **Normalise first and denormalise for a measured reason.** Redundant copies create update anomalies; a
   copy is justified by a read path you have measured, and it has an owner who keeps it in sync. A computed
   value that must stay consistent with its inputs is a generated column, not a hand-maintained one.
9. **Soft deletion is a design with consequences.** Every unique constraint, every query and every join must
   account for the deleted rows, or a "deleted" email blocks a new sign-up. If rows must be retained, a partial
   unique index over the live rows keeps uniqueness meaningful; if they need not be, delete them
   (`skills/laravel-pruning-fires-delete-events` for retention on the Laravel side).

**Sources:** the PostgreSQL manual (constraints: check, not-null, unique and its null handling, foreign keys
and the note on indexing the referencing columns), read 2026-10-02; the MySQL manual for the InnoDB foreign
key index behaviour; vendor-published schema guidance (Apache-2.0, MIT). Points 1, 5 (reasoning part), 6 and 9
are reasoning of ours.
