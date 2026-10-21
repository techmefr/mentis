---
name: filters-search-and-saved-views-pitfalls
description: "Use when filters, a search box, facets or saved views are written or reviewed on a list, table or report in a business application, whatever the framework: filter state kept in the URL, saved and shared views, server-side against client-side filtering, debounce and cancelled requests, facet counts that disagree with results, the empty-results state, filter semantics (AND, OR, empty, null, dates and time zones), accessibility of filter controls, and the tests that catch them."
---

# filters-search-and-saved-views-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the controls that decide which rows a user is looking at. The premise:
**a filter is a query, so its state must be explicit, shareable and identical on screen, in the request, in the
count, in the export and in a saved view**; every defect below is two of those disagreeing. The table that shows
the result is in `data-table-ui-pitfalls`; where state lives in general is in `data-fetching-state-conventions`;
index-side search behaviour (analysers, collation) is in `collation-and-locale-aware-search-pitfalls` and
`search-engine-index-settings-pitfalls`.

## When
- A filter bar, search box, facet panel or "saved views" feature is built or reviewed.
- A user reports "the link shows something else", "the count says 40 but I see 38", "my saved view broke", "search is slow while typing".
- Filter state is added to a list that is also exported, counted or shown on a dashboard.

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | One filter model, URL state, saved views, who may share them, versioning | filter state is stored, linked or saved | [`01-filter-state-urls-saved-views.md`](./references/01-filter-state-urls-saved-views.md) |
| 2 | Server against client, debounce and races, facets, semantics, empty results, accessibility, tests, framework pointers | a filter runs, is counted or tested | [`02-search-facets-semantics-tests.md`](./references/02-search-facets-semantics-tests.md) |

## Output / checkpoint
A change is done when: one serialisable filter object feeds the controls, the URL, the request, the count, the
export and the saved view; an unknown or invalid parameter degrades to a message, not an error; empty results say
which filters caused them; and the tests in §2.7 exist. No checkpoint: a craft block, 🟡, nothing here was run.

## Guardrails
- Keep one filter model for every consumer (§1.1). Never rebuild the filter separately for the count or the export.
- Put shareable state in the URL and validate it on read (§1.2). Never trust or execute a parameter as given.
- Check saved-view access on the server (§1.5). Never rely on hiding another user's view in the interface.
- Debounce input and ignore stale responses (§2.2). Never let a slow old answer replace a newer one.
- Name the filters behind an empty result (§2.5). Never show a bare "no results" with filters active.
- Library and platform facts are stamped in `references/origin.md`; re-read before relying.

## Origin
Own craft knowledge, with filter and facet facts re-read in the TanStack Table documentation (MIT), history and composition facts in the HTML Standard and UI Events, and the accessibility points of §2.2 and §2.6 checked against WCAG 2.2, WAI-ARIA 1.2 and the ARIA Authoring Practices (facts only), all read 2026-10-20.
Details in [`references/origin.md`](./references/origin.md).
