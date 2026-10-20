# data-table-ui-pitfalls: origin and source stamps

> Provenance of `skills/data-table-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No table was built, run or tested while writing it. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| TanStack/table at commit 95c4768 (Vue framework guides: pagination, sorting, column-filtering, row-selection, column-visibility, virtualization, table-state, column-faceting) | MIT, Copyright (c) 2016 Tanner Linsley (`LICENSE` read 2026-10-20) | Client against server operations on the same dataset, page reset, unknown page count and cursor paging, row id and selection state, virtualization against paging, state that can be persisted |
| W3C WAI-ARIA Authoring Practices (table and grid patterns) | W3C Software and Document License, not MIT/Apache/CC BY | Public facts only (sort state attribute, row count attributes, grid against table); the pages were not opened for wording |

## Own craft, not from a source
Offset against keyset trade-offs and tiebreakers, the seven table states, layout versioning, "select all matching" semantics, export injection, interaction and test lists, the framework pointers.

## Removed
Library-specific code and option names beyond the few cited as facts; column pinning, grouping, expanding and fuzzy matching; framework install steps.

## Not verified
1. **Library facts** (page reset, selection helper on a manual page, no last page on unknown count) are the documentation's claims at the commit; none was run. Re-read before relying.
2. **ARIA attributes** were recalled from the public specification, not re-read in this pass. Re-read before relying.
3. **Vuetify and Laravel pointers** name features from memory; no version was checked.
4. **No performance number** is stated; none was measured.
