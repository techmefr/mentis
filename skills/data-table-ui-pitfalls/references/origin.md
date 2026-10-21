# data-table-ui-pitfalls: origin and source stamps

> Provenance of `skills/data-table-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No table was built, run or tested while writing it. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| TanStack/table at commit 95c4768 (Vue framework guides: pagination, sorting, column-filtering, row-selection, column-visibility, virtualization, table-state, column-faceting) | MIT, Copyright (c) 2016 Tanner Linsley (`LICENSE` read 2026-10-20) | Client against server operations on the same dataset, page reset, unknown page count and cursor paging, row id and selection state, virtualization against paging, state that can be persisted |
| Laravel documentation, Pagination page (12.x), read 2026-10-20 | Vendor documentation, no open licence stated: facts only, rewritten | Cursor paging needs a unique ordering and does not support null columns, next and previous only, offset paging can skip or repeat rows under writes |
| W3C ARIA Authoring Practices: table pattern, grid pattern, sortable table example, grid and table properties practice (w3.org/WAI/ARIA/apg/), read 2026-10-20 | W3C document licence, not MIT/Apache/CC BY; facts only, own words | Table against grid, keyboard model, aria-sort on the th and its value set, aria-rowcount and aria-rowindex rules, -1 for an unknown total |
| W3C WCAG 2.2 Understanding SC 4.1.3 and SC 2.5.8, read 2026-10-20 | W3C document licence, facts only | Status messages without focus move; 24 by 24 CSS pixel target size and its spacing exception |
| W3C WAI-ARIA 1.2 Recommendation, property summaries (read 2026-10-20, through a summarising fetcher, page truncated before the detailed definitions) | W3C document licence, facts only | Roles on which row count and index apply; details taken from the practice page above |

## Own craft, not from a source
Offset against keyset trade-offs and tiebreakers, the seven table states, layout versioning, "select all matching" semantics, export injection, interaction and test lists, the framework pointers.

## Removed
Library-specific code and option names beyond the few cited as facts; column pinning, grouping, expanding and fuzzy matching; framework install steps.

## Not verified
1. **Library facts** (page reset, selection helper on a manual page, no last page on unknown count) are the documentation's claims at the commit; none was run. Re-read before relying.
2. **Verified 2026-10-20 (third pass)**: aria-sort values and one-column advice, aria-rowcount and aria-rowindex rules, -1 for unknown, table against grid and the grid keyboard model, table naming, target size, status message without focus move (§3.1 items 1 to 5, §3.3.4). **Corrected**: §3.1.1 (cells of a table are not focusable, controls inside are separate tab stops), §3.1.5 (the sortable table example does not announce the change, so the live message is our addition). **Still unverified**: the polite politeness wording, the sticky-header and scroll-region points, and spreadsheet formula injection characters (the usual reference is licensed share-alike, not opened; no permissive source found, searched: W3C pages above). Re-read before relying.
3. **Vuetify pointer** names features from memory; a fetch of its server-side table page returned no usable content, so it stays unverified. The Laravel pointer is now checked for cursor paging (see the table); the standard paginator name was not.
4. **No performance number** is stated; none was measured.

Independent verification 2026-10-21: 20 checked, 20 matched, 0 corrected, 0 unverified
