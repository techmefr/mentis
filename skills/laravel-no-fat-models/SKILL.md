---
name: laravel-no-fat-models
description: "Use when a model gains a method beyond fillable/casts/relationships/trivial accessors: business logic goes to an action or query class, never a *Service/*Repository."
---

# laravel-no-fat-models

Narrow trigger extracted from `skills/laravel-conventions` §1.1, so "where does this method go"
routes here directly instead of only through the whole Laravel block.

## When
Adding a method to an Eloquent model, or reviewing one that does more than read the model's own
attributes — orchestration, a call reaching another aggregate, business logic.

## Steps
1. **Keep models thin.** A model holds `$fillable`, `$casts`, relationships, trivial computed
   accessors over its own attributes, and lifecycle traits. Business logic and orchestration go in
   an **action or query class**, never a generic `*Service`/`*Repository`.
2. **One class, one verb-plus-noun mission** (`RegisterUser`, `GetActiveSessionsForUser`), never a
   `UserManager`/`UserService` that accumulates unrelated methods over time.
3. **Separate the read from the write.** A query class answers a question and touches nothing; an
   action changes state. Merging them gives a method whose name cannot be honest
   (`getOrCreateAndNotify`).
4. **An action has one public method and returns a value** — domain data, never an HTTP response or a
   redirect, so it stays callable from a command, a job or a test without faking a request.

## Output / checkpoint
The model's class body holds only `$fillable`/`$casts`/relationships/trivial accessors/traits; the
new logic lives in a named action or query class with one public method.

## Guardrails
- A fat model is the class everything imports and nobody can change; a generic service is the same
  failure one layer up — moving logic out of the model into a `*Service` is not the fix.
- Per-concept scopes and accessors that do accumulate belong in a concern trait, not directly on the
  model — `skills/laravel-conventions` §1.4 covers when a trait earns its place.
- The full breakdown of action/query separation and the code-baseline no-bag-name rule live in
  `skills/laravel-conventions` §1 — read it before naming a new class `*Service`.

## Origin
No external source: this is `skills/laravel-conventions` §1.1 extracted to its own trigger. Written
2026-09-09, same pilot as `laravel-no-db-enums`.
