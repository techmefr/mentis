---
name: laravel-precognitive-request-scoping
description: "Use when a FormRequest's validation rule has a side effect the caller doesn't expect on every keystroke: scope it to skip during a precognitive request, since HandlePrecognitiveRequests runs the real FormRequest before the controller."
---

# laravel-precognitive-request-scoping

Narrow trigger extracted from `skills/laravel-conventions` §6.17, so a FormRequest validation rule
with a side effect routes here directly instead of only through the whole Laravel block.

## When
Writing or reviewing a validation rule used on a route with `HandlePrecognitiveRequests` (as-you-type
validation) — specifically a rule that checks against a row the request itself is about to create or
modify (a uniqueness check, a "does this already exist" lookup).

## Steps
1. **`HandlePrecognitiveRequests` runs the same FormRequest the real submission runs**, stopped
   before the controller — so every keystroke re-runs the full validation.
2. **A rule checking against a row the precognitive request itself is about to create** — a
   uniqueness check against data that doesn't exist yet — reports a false positive on every keystroke.
3. **Scope those rules to skip during a precognitive request** rather than letting them fire on data
   that isn't final yet.

## Output / checkpoint
Any validation rule that depends on the row the current request is about to create/modify is
conditioned to skip (or behave correctly) when `$request->isPrecognitive()` is true.

## Guardrails
- This only applies to rules that check against the request's own not-yet-created data — a rule
  validating unrelated, already-existing state is meant to fire on every keystroke and needs no
  scoping.
- The full FormRequest section lives in `skills/laravel-conventions` §6 — read it for the neighbouring
  validation rules this one sits beside.

## Origin
No external source: this is `skills/laravel-conventions` §6.17 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
