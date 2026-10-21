---
name: laravel-idempotent-seeders
description: "Use when writing or reviewing a seeder that carries reference data: upsert by a natural key, never insert — a seeder that duplicates rows on the second run makes a fresh environment unreproducible."
---

# laravel-idempotent-seeders

Narrow trigger extracted from `skills/laravel-conventions` §7.12 and §9.10, so a reference-data
seeder routes here directly instead of only through the whole Laravel block.

## When
Writing or reviewing a seeder (or a migration inserting reference data) whose rows represent
application reference data — statuses, roles, categories, plan tiers.

## Steps
1. **A seeder carries the reference data the application needs to run, and it is idempotent.**
   Upsert by a natural key rather than inserting.
2. **Reference data inserted by a migration or a seeder must run again on the next environment**
   without erroring or duplicating — that's the entire point of committing it.
3. A seeder that duplicates its rows on the second run makes a fresh environment unreproducible: the
   row count depends on how many times the seeder happened to be run. The framework's own seeding page shows a
   plain insert, so idempotence is a house rule here, not a framework requirement.
4. **`upsert` needs a unique index to do its job.** Eloquent's `upsert(values, uniqueBy, update)` is one atomic
   operation, but every database except SQL Server requires the `uniqueBy` columns to carry a primary or unique
   index, and MySQL and MariaDB ignore that argument and use the table's own primary and unique indexes. A
   natural key with no index upserts nothing: it inserts again. Add the unique index in the migration first.
5. **`firstOrCreate` is idempotent but not atomic**: it looks the row up and inserts if absent (the documentation
   describes exactly that and says nothing about atomicity), so, by our own reasoning, two concurrent runs can
   both insert unless the key is unique at the database level.
6. **The seeder may run often.** Tests can run the default seeder before each test through the base test
   class's seed property, and the seeding command is the one operators rerun (it asks for confirmation in
   production unless forced). A seeder that is safe only once breaks both.

## Output / checkpoint
Running the seeder (or migration) twice on the same database leaves the same rows, not duplicates —
verified by seeding twice locally, not by inspection.

## Guardrails
- This is the reference-data half of `laravel-conventions` §9's seed-data coverage — a *feature's*
  new seed data (as opposed to static reference rows) is `laravel-seed-new-features`'s concern.
- Factories are the opposite case (deliberately non-idempotent, a fresh row per call) — don't apply
  this rule to test factories, only to reference-data seeders and migrations.

## Origin
Extracted from `skills/laravel-conventions` §7.12 and §9.10 (2026-09-09). Steps 4 to 6 added on 2026-10-20 from
the framework's documentation, 12.x (read for facts, our words): Eloquent, Retrieving or Creating Models and
Upserts; Database: Seeding (Writing Seeders, Running Seeders, forcing in production); Database Testing (Running
Seeders: the seed property). Independent verification 2026-10-21: 8 checked, 7 matched, 1 corrected (step 5's atomicity statement is our reasoning, not a documented fact), 0 unverified.
Not in any source and therefore our policy: the idempotence rule itself and the
reference-data scope. Mechanisms only, rewritten in our words.
