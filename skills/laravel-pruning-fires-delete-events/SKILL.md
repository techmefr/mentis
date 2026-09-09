---
name: laravel-pruning-fires-delete-events
description: "Use when writing or reviewing a pruning/retention sweep on a soft-deleted model: never a mass-prune trait, event suppression, a quiet delete, or a raw DELETE — pruning is deleting, it fires the same per-row events."
---

# laravel-pruning-fires-delete-events

Narrow trigger extracted from `skills/laravel-conventions` §3.13–§3.14, so a retention/pruning sweep
routes here directly instead of only through the whole Laravel block.

## When
Writing or reviewing a scheduled sweep, a `Prunable`-style mass deletion, or any code purging rows
past a retention window on a model that uses soft deletes.

## Steps
1. **Every model using soft deletes also carries a pruning policy with a retention window.** Soft
   deletes without pruning is an unbounded table silently becoming the biggest one in the database.
2. **Pruning is deleting, and a sweep fires the same per-row events as a delete.** A mass-prune trait,
   event suppression, a quiet delete, a table truncate, or a hand-rolled `DELETE ... WHERE created_at
   <` cron all bypass those events.
3. **"This data is never deleted, only pruned" is a contradiction.** If a row can be purged after a
   retention window, it is deletable — the window only says when.

## Output / checkpoint
The sweep goes through the model's normal delete path (row by row, or a mechanism that still fires
per-row lifecycle events), never a bulk statement or a suppressed-event mass delete.

## Guardrails
- This is the retention-side twin of `laravel-no-cascade-delete` — the same bypass (rows leave, no
  event fires, nothing downstream hears) arriving from the scheduled-sweep direction instead of the
  foreign-key direction.
- The full schema section, including why "shared shape" or "shared screen" is never the reason two
  concepts merge into one model, lives in `skills/laravel-conventions` §3.

## Origin
No external source: this is `skills/laravel-conventions` §3.13–§3.14 extracted to its own trigger.
Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
