---
name: laravel-no-cascade-delete
description: "Use when adding or reviewing a foreign key, or a delete on a model with children: never a database-level cascade delete."
---

# laravel-no-cascade-delete

Narrow trigger extracted from `skills/laravel-conventions` §3.5–§3.10, so a migration or a delete
path routes here directly instead of only through the whole Laravel block.

## When
A migration adds a foreign key and reaches for `->cascadeOnDelete()` (or the raw SQL equivalent),
or a review is looking at why deleting a parent row also removed its children with no listener
having run.

## Steps
1. **No cascade delete at the database level.** The DB deletes children behind the ORM's back, so
   no lifecycle event fires: no audit entry, the child stays in the search index, its cache is
   never invalidated, no cancellation email, denormalised counters on siblings stay wrong — none of
   it fails loudly.
2. **Keep the foreign key, drop only the cascade.** Removing the constraint entirely trades
   silent-wrong-behaviour for silent-orphan-rows, which is worse.
3. **Cascade through an explicit listener class**, not a closure in the model's `boot()`. Stream
   the children (a cursor or chunk-by-id); reading the relation as a property loads every child
   into memory first.
4. **Never both.** A DB cascade and a listener means the listener deletes children the database has
   already removed.

## Output / checkpoint
The foreign key exists with no `cascadeOnDelete`; deletion of the parent's children, if any, goes
through a registered listener class that can be read, tested and queued on its own.

## Guardrails
- If a lifecycle listener "isn't firing", check the parent's foreign key for a leftover cascade
  first — the most common root cause, and it looks like a broken listener.
- Three narrow exceptions exist (a pure pivot table with no business meaning, a deliberate
  data-destruction purge at scale, an append-only log whose only consumer is its parent) — read
  `skills/laravel-conventions` §3.10 before claiming one, not after.

## Origin
No external source: this is `skills/laravel-conventions` §3.5–§3.10 extracted to its own trigger.
The reasoning and the five-consequence list stay in the parent block. Written 2026-09-09, same
pilot as `laravel-no-db-enums`.
