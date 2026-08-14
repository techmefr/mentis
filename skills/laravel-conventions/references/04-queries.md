# laravel-conventions §4 — Queries

> Section 4 of `skills/laravel-conventions`. Read it when an Eloquent query, a relation load, or anything inside a loop. The other sections and the guardrails stay in `SKILL.md`.

1. **No query inside a loop.** A lazy-loaded relation accessed per iteration, an aggregate per row, a
   `find()` in a `foreach` — all N+1. Eager-load or aggregate before iterating. This includes a loop inside a
   view.
2. **Read the relation accessor**, never re-fetch a related model by hand from a foreign-key attribute: the
   accessor uses the loaded relation when it's there and is the thing eager-loading can optimise.
3. **Prefer the `OrFail` fetch** (`findOrFail`, `firstOrFail`) over a fetch plus a null check that aborts
   404: one line, and the not-found path can't be forgotten.
4. Push filtering, sorting and pagination into the query, not into a collection loaded whole and filtered in
   PHP.
