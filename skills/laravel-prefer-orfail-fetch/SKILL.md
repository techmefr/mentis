---
name: laravel-prefer-orfail-fetch
description: "Use when fetching one Eloquent record that must exist: prefer findOrFail/firstOrFail over a fetch plus a null check that aborts 404."
---

# laravel-prefer-orfail-fetch

Narrow trigger extracted from `skills/laravel-conventions` §4.3, so a single-record fetch routes here
directly instead of only through the whole Laravel block.

## When
Writing or reviewing a fetch of exactly one record where "not found" means the request itself
aborts 404 — a controller action, a job, a console command.

## Steps
1. **Prefer the `OrFail` fetch** (`findOrFail`, `firstOrFail`) over `find`/`first` plus a manual null
   check that aborts — one line, and the not-found path can't be forgotten.
2. **Distrust a null case handled *sometimes*.** A fetch whose result is checked in one caller and not
   in another is where the null-pointer error lands — the second caller.
3. Reach for `findOrFail`/`firstOrFail` even when the current caller "knows" the record exists — the
   assumption is what breaks first when the caller changes.

## Output / checkpoint
Every single-record fetch that should 404 on absence uses `findOrFail`/`firstOrFail` (or the
Eloquent-query equivalent), not a manual `if (!$model) abort(404)`.

## Guardrails
- This is about fetch shape, not about authorisation — an `OrFail` fetch still needs the scoping from
  `laravel-scope-dont-check-after-fetch` when the id comes from the request.
- The full section on pushing filtering/sorting/pagination into the query lives in
  `skills/laravel-conventions` §4 — read it before generalising this to collection fetches.

## Origin
No external source: this is `skills/laravel-conventions` §4.3 extracted to its own trigger. Written
2026-09-09, same pilot as `laravel-no-db-enums`.
