# filters-search-and-saved-views-pitfalls: origin and source stamps

> Provenance of `skills/filters-search-and-saved-views-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No filter bar was built, run or tested while writing it. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| TanStack/table at commit 95c4768 (Vue guides: column-filtering, global-filtering, column-faceting, pagination) | MIT, Copyright (c) 2016 Tanner Linsley (`LICENSE` read 2026-10-20) | Client against server filtering on the same dataset, auto-removal of empty values, case-sensitive and insensitive comparators, faceting as data for filter interfaces, page reset on filter change |

## Own craft, not from a source
URL state rules, saved-view ownership and versioning, request races and debounce, facet count agreement, filter semantics (OR within a field, nulls, time zones), empty-result design, accessibility and test lists, framework pointers.

## Removed
Library option names and code, fuzzy matching, nested-row filtering, framework install steps.

## Not verified
1. **Library facts** are the documentation's claims at the commit; none was run. Re-read before relying.
2. **Platform behaviour** (history API, composition events, router query handling, SQL null logic) is general knowledge, not re-read for this pass.
3. **Framework pointers** name features from memory; no version was checked.
4. **No debounce delay or length threshold** is stated; none was measured.
