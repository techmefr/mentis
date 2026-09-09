---
name: laravel-no-db-enums
description: "Use when adding or reviewing a database column that holds a fixed set of values (a status, a type, a category): never a DB-level ENUM column."
---

# laravel-no-db-enums

Narrow trigger extracted from `skills/laravel-conventions` §3.1–§3.3, so a migration adding a
closed-set column routes here directly instead of only through the whole Laravel block.

## When
A migration adds a column whose value is one of a fixed, known set — a status, a type, a category,
a role. Also fires on a review comment proposing `enum(...)` or a `CHECK (... IN (...))`
constraint as "simpler than a cast".

## Steps
1. **Never a DB-level `ENUM` column, and never a `CHECK` constraint standing in for one.** Use a
   string column, a PHP backed enum as the single source of truth, cast on the model, validated
   through the framework's enum rule.
2. **Before writing the migration, ask who changes this set.** A developer with a deploy → enum.
   A user or an admin at runtime → a table, not an enum at all (`laravel-conventions` §3.3).
3. **Don't tune the column length to the longest current value, and don't skip the cast.** A
   column with no cast is a raw string that happened to work by convention, not an enum.

## Output / checkpoint
The migration declares a plain string column; the model casts it to a backed PHP enum; nothing in
the schema enforces the value set at the database level.

## Guardrails
- Never rename an enum's backing value to "tidy it up" — it is stored data, read by every existing
  row, payload and cache (`laravel-conventions` §3, backing-value point).
- The full five-reason argument (locking a large table on `ALTER`, cross-engine inconsistency, two
  sources of truth drifting, a multi-step rename, an impossible runtime-configurable set) lives in
  `skills/laravel-conventions` §3 — read it before arguing the exception case, not after.

## Origin
No external source: this is `skills/laravel-conventions` §3.1–§3.3 extracted to its own trigger, the
same way an org skill catalogue exposes this exact rule as its own file rather than one point among
fifteen. The reasoning and the mechanism stay in the parent block; this file only narrows *when* it
fires. Written 2026-09-09 as a pilot for the "narrow-trigger + pointer" restructuring proposed after
comparing mentis's `laravel-conventions` against a market catalogue's per-rule granularity.
