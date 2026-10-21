# data-table-ui-pitfalls §3 — Access, scale, tests and pointers

Sources: own craft; W3C ARIA Authoring Practices table pattern, grid pattern, sortable table example and grid-and-table properties practice (facts only, read 2026-10-20) for §3.1 items 1 to 4; WCAG 2.2 Understanding SC 4.1.3 and SC 2.5.8 (facts only, read 2026-10-20) for items 5 and 3.3.4; the virtualization facts are from the TanStack Table guide (MIT, read 2026-10-20).

## 3.1 Accessibility
1. **Use a real table (`table`, `th`, `td`) for read-mostly data.** The grid role is for interactive cell-by-cell navigation like a spreadsheet and brings a keyboard model you must implement fully (one tab stop, arrow keys between cells, Home and End, Enter or F2 to edit and Escape to leave editing); a half-built grid is worse than a table. A table's cells are not focusable, and every control inside it is its own tab stop: a table full of widgets is the case where a grid shortens the tab sequence.
2. **Give the table a name** (caption, or a label or labelled-by reference on the table) and keep header cells as `th` with a scope (`a11y-hiding-and-tables-pitfalls` §2).
3. **Expose the sort state on the header** (`aria-sort` with ascending, descending, none) on the header cell (the th, not the button) of one column at a time (the attribute cannot express multi-key priority, so setting it on several columns says little; remove it from the old column when the sort moves), and make the sort control a real button inside the header cell with an accessible name that states the column and the action.
4. **When rows are loaded in parts, tell assistive technology the total** (`aria-rowcount`, `aria-rowindex`) so a page of 25 is not read as the whole. The count includes header rows, each row index starts at 1, increases and never exceeds the count (missing or inconsistent indices can make a screen reader skip rows); use -1 as the count when more rows exist but the total is unknown.
5. **Announce changes politely**: after sort, filter or page change put a short message ("12 results, sorted by date, newest first") in a status region (WCAG 4.1.3: a result message must be exposed without moving focus; the sortable table example in the authoring practices does not announce, so this is an addition, not a requirement); do not move focus to the table body unprompted.
6. **Row actions need names that include the row** ("Edit invoice 2041"), not N identical "Edit" buttons. A kebab menu follows the menu-button keyboard rules.
7. **Selection checkboxes are labelled with the row** and the header checkbox with what it selects; show the selected count in text, not only highlight colour.
8. **Do not make the whole row a click target with nothing keyboard-reachable inside it.** One real link or button per row, and let the row click be an extra.
9. **Sticky headers and columns must not hide the focused cell** when the keyboard scrolls; scroll the focus into the visible area.
10. **Horizontal scroll regions are focusable** and named so keyboard users can scroll them; narrow screens need a deliberate pattern (priority columns, a stacked card view), not a squeezed table (`responsive-layout`).
11. **Colour is never the only status**: a badge has a word or icon (`accessibility`).

## 3.2 Large data
1. **Rendering and loading are separate problems.** Virtualization (mount only visible rows) cuts DOM cost but the data still lives in the browser; the library documentation says it does not replace server-side paging when the dataset is too large to load.
2. **Page on the server when the full set is too heavy to query, send or hold.** Row count alone does not decide it; row width, column count and device class do.
3. **Virtualization breaks things that need the whole DOM**: find-in-page, print, "select all visible" and focus restoration; for virtualized tables keep row heights predictable (or measure), keep keyboard navigation working by row index and keep `aria-rowcount` honest.
4. **Infinite scroll suits feeds, not work tables**: no footer, no stable place, no "go to row 400". Offer paging or a load-more button with a count when users need to return to a spot.
5. **Cap the page size** at the server; never trust a client-sent size. A maximum protects the database and memory.
6. **Debounce text filters and cancel superseded requests** (`filters-search-and-saved-views-pitfalls` §2).
7. **Export is not "what is on screen".** Run it on the server from the filter, as a job for large sets, with the same permission rules, and say which filter and columns it used. Spreadsheet formula injection: prefix cell values that start with `=`, `+`, `-` or `@` when exporting to a format that evaluates them.
8. **Heavy cell renderers (avatars, charts per row) are the usual cost, not the row count**: render placeholders, lazy-load images, avoid per-row subscriptions.

## 3.3 Mistakes of interaction
1. **Do not change row order under the pointer** when data refreshes (live updates): queue new rows with a "3 new rows" control.
2. **Inline edit saves explicitly or on blur with feedback**, keeps the typed value on failure, and does not reorder rows mid-edit.
3. **Do not trap focus in a cell editor**; Escape cancels and returns focus to the cell.
4. **Keep sort controls and filter controls reachable on touch**: WCAG 2.2 asks for pointer targets of at least 24 by 24 CSS pixels, or enough spacing around smaller ones that a 24 pixel circle on each does not touch another target.

## 3.4 Tests
1. **Pagination and sort against the real order**: create enough rows (more than two pages, with duplicate sort values) and assert page 1 plus page 2 equals the ordered whole, with no duplicate id.
2. **Selection**: tick on page 1, move to page 2 and back; assert the count text and the ids sent by the bulk action; assert "all matching" sends the filter.
3. **State rendering**: stub loading, empty-none, empty-filtered, error and refetching responses; assert a different, named element for each.
4. **Layout persistence**: store an old-schema layout and assert the table opens with defaults for the unknown columns.
5. **Accessibility**: assert sort state on the header, a name on the table, labelled row actions and the live-region message; run an automated check and one keyboard-only pass (Tab to header, activate sort, reach a row action).
6. **Authorization**: a user without the permission cannot execute the bulk action by sending ids directly.
7. **Large data**: a performance test with the maximum page size and the heaviest renderer, measuring interaction responsiveness; do not assert a hard number copied from elsewhere.

## 3.5 Framework pointers (reference only)
1. **Headless engines** (a table core that owns state and leaves markup to you) separate model from rendering; start from one rather than hand-writing sort and selection logic. Declare which operations are manual (server-side) in the one place the engine offers.
2. **Vuetify** data tables expose a server-side mode with an items length, sort-by and page options; the rules above (same place for sort and page, row key, states) still apply. See `vue-nuxt-vuetify-conventions`.
3. **Laravel** back end: paginate with a cursor for keyset and the standard paginator for offset, always order by a column plus the primary key (the Laravel documentation, source 2: cursor paging needs an order by on at least one unique column or a unique combination, does not support columns holding null, and offers only next and previous links), and apply the same filter to the count and to the bulk action (`laravel-lomkit-rest-api`, `laravel-aggregate-in-database`).
4. **React or Nuxt query layers**: include page, size, sort and filters in the query key and keep previous data while fetching the next key (`data-fetching-state-conventions` §2).
