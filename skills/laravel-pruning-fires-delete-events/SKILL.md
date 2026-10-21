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
2. **Pruning is deleting, and a sweep fires the same per-row events as a delete.** The framework's
   per-model prune trait loads the rows in chunks, calls the model's `pruning()` hook, then `delete()` (or
   `forceDelete()` for a soft-deleting model), so the deleting and deleted events fire. Its mass variant runs
   chunked delete queries instead: no `pruning()` hook and no deleting or deleted events (documented). The
   same bypass comes from event muting, a quiet delete, a builder-level `delete()`, a table truncate, or a
   hand-rolled `DELETE ... WHERE created_at <` cron.
3. **"This data is never deleted, only pruned" is a contradiction.** If a row can be purged after a
   retention window, it is deletable — the window only says when.

4. **Pruning a soft-deleting model removes rows for good.** A row matching the prunable query is force
   deleted, trashed or not (documented), which is the point of step 1 and also why the retention window must be
   chosen on purpose. `model:prune --pretend` reports how many rows would go without deleting them.

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
Extracted from `skills/laravel-conventions` §3.13–§3.14 (2026-09-09). Facts checked on 2026-10-20 against the
framework's Eloquent documentation, 12.x (Deleting Models: mass deletes dispatch no model events; Pruning Models,
Mass Pruning; Events, Muting Events; read for facts, our words) and the framework source (MIT, LICENSE read):
`Prunable.php` (`pruneAll`, `prune`) and `MassPrunable.php` (`pruneAll`). Steps 1 and 3 and the house rule
against the mass variant are our own policy, not a framework statement: the framework offers the mass trait and
documents its trade-off.

Independent verification 2026-10-21: 9 checked, 9 matched, 0 corrected, 0 unverified.
