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
   row count depends on how many times the seeder happened to be run.

## Output / checkpoint
Running the seeder (or migration) twice on the same database leaves the same rows, not duplicates —
verified by seeding twice locally, not by inspection.

## Guardrails
- This is the reference-data half of `laravel-conventions` §9's seed-data coverage — a *feature's*
  new seed data (as opposed to static reference rows) is `laravel-seed-new-features`'s concern.
- Factories are the opposite case (deliberately non-idempotent, a fresh row per call) — don't apply
  this rule to test factories, only to reference-data seeders and migrations.

## Origin
No external source: this is `skills/laravel-conventions` §7.12 and §9.10 extracted to its own
trigger. Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
