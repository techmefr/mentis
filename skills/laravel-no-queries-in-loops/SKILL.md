---
name: laravel-no-queries-in-loops
description: "Use when writing or reviewing a foreach/loop over Eloquent models, or an accessor: no query, aggregate or lazy relation access per iteration (N+1)."
---

# laravel-no-queries-in-loops

Narrow trigger extracted from `skills/laravel-conventions` §4.1–§4.2, so an N+1 pattern routes here
directly instead of only through the whole Laravel block.

## When
A `foreach` (controller, job, console command, or a Blade/Inertia template) iterates Eloquent
models and reads a relation, an aggregate, or does a `find()`/`where()` per row. Also fires on
reviewing an accessor that reads a relation, counts something, or queries configuration.

## Steps
1. **No query inside a loop.** A lazy-loaded relation accessed per iteration, an aggregate per row,
   a `find()` in a `foreach` — all N+1. Eager-load or aggregate before iterating.
2. **This includes a loop inside a view.** The controller can look clean while the template pulls a
   relation per row — read the template, not only the controller, before clearing a review.
3. **This includes an accessor that loads something.** An N+1 can hide behind an attribute that
   reads like a plain field; the moment an accessor loads a relation, counts something, or reaches
   configuration, it is a query wearing the clothes of a field.
4. **Read the relation accessor**, never re-fetch a related model by hand from a foreign-key
   attribute — a hand-rolled `Model::find($row->model_id)` is invisible to eager loading and cannot
   be fixed later by adding a `with()`.

## Output / checkpoint
The query count for the page/job/command is constant regardless of how many rows it processes —
verified with `Model::shouldBeStrict()` in local/CI (`laravel-conventions` §4.14) or by reading the
query log, not by inspection alone.

## Guardrails
- Count and aggregate in the database (`withCount()`, a relation's own `->count()`), never by
  hydrating every row to count them in PHP.
- The chunking trap, the search-index-is-a-different-engine case, and `chaperone()`/`lazy()` vs
  `cursor()` all live in `skills/laravel-conventions` §4 — read it before reaching for a fix beyond
  eager-loading.

## Origin
No external source: this is `skills/laravel-conventions` §4.1–§4.2 extracted to its own trigger.
Written 2026-09-09, same pilot as `laravel-no-db-enums`.
