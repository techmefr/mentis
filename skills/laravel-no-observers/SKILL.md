---
name: laravel-no-observers
description: "Use when a model needs to react to its own lifecycle (created, updated, deleted): never a model Observer or a boot() closure, always an explicit event listener."
---

# laravel-no-observers

Narrow trigger extracted from `skills/laravel-conventions` §1.2, so "make this fire when the row is
saved" routes here directly instead of only through the whole Laravel block.

## When
A model needs a side effect on save/update/delete — send a notification, denormalise a counter,
invalidate a cache, sync to a search index. Also fires on a review comment proposing
`php artisan make:observer` or a `static::creating(...)` closure inside a model's `boot()`.

## Steps
1. **Events plus listeners, never a model Observer.** An observer is invisible at the call site:
   something saves a row and unrelated code runs, with no trace in the code being read.
2. **`boot()` is the same problem wearing the framework's own clothes.** A static `boot()` override
   registering a lifecycle closure is not a safer alternative to an Observer — the fix is the same
   listener, registered explicitly in the `EventServiceProvider`, never a closure moved into the
   model.
3. **Register the listener explicitly**, so a reader following "what happens when this model is
   created" finds it in one searchable place rather than inferring it from a class that happens to
   exist.

## Output / checkpoint
The reaction lives in a listener class, registered in `EventServiceProvider` (or the equivalent
explicit registration), and grep for the model event name finds it — no `Observer` class, no
`static::creating`/`static::updating`/`static::deleting` in the model.

## Guardrails
- Heavy or slow reactions (an outbound call, a recalculation) are queued from the listener, not run
  inline in `boot()` where nothing controls their cost.
- The full argument for why explicit beats implicit here is `skills/laravel-conventions` §1.2 — read
  it before treating this as a style preference rather than a traceability one.

## Origin
No external source: this is `skills/laravel-conventions` §1.2 extracted to its own trigger. Written
2026-09-09, same pilot as `laravel-no-db-enums`.
