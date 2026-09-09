---
name: laravel-seed-new-features
description: "Use when a change introduces or changes persisted data (a new model, an extended enum, a new column): ship its seed data in the same change, not three weeks later."
---

# laravel-seed-new-features

Narrow trigger extracted from `skills/laravel-conventions` §9.11, so a schema or data change routes
here directly instead of only through the whole Laravel block.

## When
A migration adds a model, extends an enum with new cases, or adds a column — anything that changes
what a fresh `migrate` produces.

## Steps
1. **A change that introduces or changes persisted data ships its seed data in the same change.** The
   bar is a fresh migrate-and-seed showing the new feature populated with realistic, varied data,
   without anyone touching their database by hand.
2. **A new model gets its seeder registered.** An extended enum gets rows for the new cases. A new
   column gets values that are not all the default.
3. A feature whose data only exists on the author's machine is a feature the next person cannot see
   — and the seeder written three weeks later is written against a schema that has already moved.

## Output / checkpoint
`php artisan migrate:fresh --seed` (or the project's equivalent) produces the new feature already
populated with realistic, varied data — no manual database edit required to see it working.

## Guardrails
- The seed data added here follows `laravel-idempotent-seeders`'s upsert-by-natural-key rule, same as
  every other seeder.
- This is a checkpoint on the change itself, not a separate ticket — "seed data later" is the failure
  mode this rule exists to name.

## Origin
No external source: this is `skills/laravel-conventions` §9.11 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
