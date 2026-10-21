---
name: data-table-ui-pitfalls
description: "Use when a data table, data grid or admin list is written or reviewed in a business application, whatever the framework: sorting that only reorders the loaded page, offset pagination against keyset (cursor) pagination, selection that is lost or wrong across pages, bulk actions on 'select all', the empty, loading, error and refreshing states, persisting column order, width and visibility, table accessibility (names, sort state, keyboard, row actions) and large data (virtualization against paging, export), plus the tests that catch them."
---

# data-table-ui-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the one component every business application has. The premise: **a table
looks right on the twenty rows the developer loaded and is wrong on the rest**: it sorts only what it holds, selects
only what it shows, shows "no results" while the request failed, and loses the user's layout on reload. The same
table must also stay usable for a keyboard and a screen reader. Filters and saved views are in
`filters-search-and-saved-views-pitfalls`; the state-ownership rules (server state, URL state) are in
`data-fetching-state-conventions`; plain table markup (caption, `th` and `scope`) is in `a11y-hiding-and-tables-pitfalls`.

## When
- A list, grid or table with sorting, paging, selection or row actions is built or reviewed.
- A user reports "the sort is wrong", "select all missed some", "it says empty but there is data", "my columns reset".
- The row count is expected to grow beyond what one response or one screen holds.

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Where sort, filter and page run, offset against keyset, stable order, selection and bulk actions | a table gets server data, selection or a bulk action | [`01-data-paging-selection.md`](./references/01-data-paging-selection.md) |
| 2 | Empty, loading, refreshing, error and partial states, column state persistence, URL state | any table state or saved layout is written | [`02-states-and-persistence.md`](./references/02-states-and-persistence.md) |
| 3 | Accessibility, large data and virtualization, export, tests, framework pointers | a table ships, or is reviewed for access, speed or tests | [`03-access-scale-tests.md`](./references/03-access-scale-tests.md) |

## Output / checkpoint
A change is done when: sort, filter and page run in the same place; row identity is the business key; selection says
what it covers; every state in §2.1 has a visible, distinct rendering; layout survives reload; and the tests in §3.4
exist. No checkpoint is written: a craft block, 🟡, nothing here was run in an application.

## Guardrails
- Run sort, filter and pagination over the same dataset (§1.1). Never sort a page client-side and call it a sort.
- Key rows and selection by a stable business id (§1.4). Never key by array index.
- Say what "select all" covers and send the bulk action the filter, not a guess (§1.5). Never act on rows the user cannot see without telling them.
- Render loading, empty and error differently (§2.1). Never show an empty state for a failed request.
- Facts about a library are for the commit stamped in `references/origin.md`; re-read before relying.

## Origin
Own craft knowledge, with the paging and state facts re-read in the TanStack Table documentation (MIT, read
2026-10-20); the ARIA table, grid and sort facts and the status-message and target-size facts were re-read on a third pass in W3C pages (facts only, credited). Details in [`references/origin.md`](./references/origin.md).
