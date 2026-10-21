# data-table-ui-pitfalls §1 — Data, paging and selection

Sources: TanStack Table guides for sorting, pagination, row selection (MIT, commit stamped in origin.md, read 2026-10-20) for the facts marked as such; the rest is own craft.

## 1.1 Sort, filter and page over the same dataset
1. **Symptom: a sort that "does not work": the first page is sorted, page two starts again from the top.** Cause: the server pages the data and the client sorts only the loaded rows. The library documentation states the same limit: sorting a page sorts only the loaded rows.
2. **Pick one place for all three operations.** All client-side only when the browser holds the complete dataset; otherwise all server-side, with the sort and the filter sent as request parameters.
3. **Mixing is allowed only on purpose**, for example a client-side quick filter over the current page, and then the label must say so ("filter this page").
4. **Reset to the first page when sort, filter or page size changes.** Symptom: an empty page 7 after narrowing a filter. The library resets it for client-side models and expects you to do it yourself in manual mode.
5. **Put the page, the page size, the sort and the filters into one request key**, so a stale answer for an older key cannot overwrite a newer one (`data-fetching-state-conventions` §2).

## 1.2 Offset against keyset pagination
1. **Offset paging (page number plus size) is simple and supports "go to page 40".** Its costs: the database still walks the skipped rows, so deep pages slow down, and rows inserted or deleted between two requests make a row appear twice or never.
2. **Keyset (cursor) paging asks for "rows after this key".** It stays fast on deep data and is stable under inserts, but gives no page number, no jump to the end and no cheap total.
3. **Choose by what users do.** Search-and-jump interfaces on a few thousand rows: offset. Feeds, logs, audit trails, imports, anything append-heavy or deep: keyset.
4. **A keyset needs a total order.** Sort on the chosen column plus a unique tiebreaker (the primary key); without it, rows with equal values are skipped or repeated at the page boundary.
   The Laravel documentation (source 2) confirms both sides: offset paging can skip or repeat rows when data is written between requests, and a cursor needs a unique order and does not support null in the ordering columns.
5. **Changing the sort invalidates the cursor.** Drop it and start again; never reuse a cursor from another sort order.
6. **Show a total only if it is cheap or labelled.** Counting a large filtered set on every request is often the slowest query on the page; show "more than N" or "next / previous" instead, or count lazily.
7. **An unknown last page needs a "next" button that knows the end.** The library documents this: with an unknown page count the "last page" action does not exist and the next button follows a "has next" flag from the server.

## 1.3 Stable order
1. **Symptom: rows jump or duplicate when sorting by a column with ties (status, date without time).** Always add a deterministic tiebreaker to the sort on the server.
2. **Sort text with the locale and collation rules the users expect**, not byte order (`collation-and-locale-aware-search-pitfalls`); nulls sort first or last on purpose and the same way on every page.
3. **Sort numbers and dates as values, not as the formatted strings shown**, and say in the header what the unit is.

## 1.4 Row identity
1. **Use the business key as row id** (a uuid or database key). By default some libraries key rows by position; the documentation warns that selection state is keyed by row id, so an index id makes the selection follow positions, not rows.
2. **Symptom: after sort or refresh, the wrong rows stay ticked or a row expansion jumps to another row.** The fix is the row id.
3. **A row that disappears from the data (filtered out, deleted, edited out of the filter) keeps its selection entry unless you clear it**; decide and clear on purpose.

## 1.5 Selection and bulk actions
1. **Selection across pages must be a defined thing.** Per-page selection is simplest; selection that survives paging needs a set of ids kept outside the page data. The library notes that the selected-rows helper only returns rows of the current page in server mode while the state can hold ids from other pages.
2. **"Select all" has two meanings: this page, or everything that matches the filter.** Offer both, and say the count: "50 selected on this page. Select all 12,480 matching rows". The header checkbox is tri-state (none, some, all).
3. **For "all matching", send the filter and the exclusions, not 12,480 ids.** The server re-evaluates the filter at action time; an id list in the request body is large and already stale.
4. **Warn when the target set can change between selection and execution** (rows edited by others) and report the result per row: done, skipped with a reason, failed.
5. **A bulk action states its object and count in the confirmation** ("Delete 37 invoices"), and destructive ones offer undo or a reviewable result (`frontend-ux-antipattern-review-pitfalls` §1).
6. **Disable a bulk action with a reason when it does not apply to part of the selection** (a status that cannot be archived), and say how many rows it would skip.
7. **Long bulk work is a job, not a request**: return at once, show progress and the final report; the table refreshes when it ends (`background-jobs-conventions`).
8. **Authorization is checked per row on the server** for every id or filter match; the hidden-button case is not a control.

## Checks
- Take 3 pages of a sorted table, concatenate them: is the order the same as one request with a page size of 3 pages?
- Insert a row during paging: is any row duplicated or lost (offset) or neither (keyset)?
- Select on page 1, go to page 2, sort, come back: does the selection say what it holds?
- Select all matching, edit one row so it no longer matches, run the action: does the server agree on the set?
