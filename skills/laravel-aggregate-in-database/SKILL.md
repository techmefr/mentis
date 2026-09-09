---
name: laravel-aggregate-in-database
description: "Use when counting, summing or averaging an Eloquent relation or collection: do it in the database (withCount, ->count(), ->sum()), never by looping/hydrating a collection in PHP — and never over an already-paginated set."
---

# laravel-aggregate-in-database

Narrow trigger extracted from `skills/laravel-conventions` §4.5, so a count/sum/average over a
relation or collection routes here directly instead of only through the whole Laravel block.

## When
Writing or reviewing code that counts, sums, averages, or otherwise aggregates over an Eloquent
relation or a loaded collection.

## Steps
1. **Count and aggregate in the database.** `withCount()` and a relation's own `->count()`/`->sum()`
   issue a database aggregate; `count($model->relation)` or looping a collection to sum/average
   hydrates every row just to reach a number — and the two read almost identically at the call site.
2. **An aggregate is not a filter.** Computing totals in PHP over an already-paginated set gives the
   total of the page, not the total of the set — the bug that looks like a rounding error.

## Output / checkpoint
Every count/sum/average in the diff resolves to a database-level aggregate (`withCount`, a relation's
own `->count()`/`->sum()`/`->avg()`, or an aggregate query) — nothing loops a hydrated collection to
compute a number that could have come from the database.

## Guardrails
- This is the aggregate-specific case of `laravel-no-queries-in-loops`'s broader N+1 concern — the
  failure mode here is specifically a wrong total, not (only) a slow request.
- The full queries section, including the filter-on-the-key-you-have rule right after this one, lives
  in `skills/laravel-conventions` §4.

## Origin
No external source: this is `skills/laravel-conventions` §4.5 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
