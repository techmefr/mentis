---
name: laravel-api-breaking-changes
description: "Use when removing a field, renaming one, or narrowing a type on an HTTP API: it's breaking even when every in-repo caller is updated — go through the additive-then-remove path, never one commit."
---

# laravel-api-breaking-changes

Narrow trigger extracted from `skills/laravel-conventions` §6.14, so a change to an API Resource or
response shape routes here directly instead of only through the whole Laravel block.

## When
Removing a field from an API Resource, renaming one, or narrowing its type (making it non-nullable,
changing its shape) on an endpoint that isn't brand new.

## Steps
1. **An HTTP API has consumers you do not deploy.** Removing a field, renaming one, or narrowing a
   type is breaking even when every in-repo caller is updated.
2. **This goes through the additive-then-remove path**, not one commit that changes the shape
   directly — add the new field, let both exist for a deprecation window, remove the old one only
   after that window closes.
3. `skills/deprecation-migration` owns the mechanics of that path (Expand/Contract, the announcement,
   the removal date).

## Output / checkpoint
Any breaking field change on a shipped API endpoint lands as an addition first (new field alongside
the old), never as a single commit that removes or narrows the old field outright.

## Guardrails
- "Every in-repo caller is updated" is not the bar — an external consumer you don't control or can't
  see is exactly who this rule protects.
- This is the contract question; `skills/laravel-conventions` §10 holds the separate layer question of
  where the endpoint's logic itself lives.

## Origin
No external source: this is `skills/laravel-conventions` §6.14 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
