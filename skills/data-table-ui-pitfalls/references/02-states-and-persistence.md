# data-table-ui-pitfalls §2 — States and persistence

Sources: own craft, with the state-keeping facts from the TanStack Table state guide (MIT, read 2026-10-20).

## 2.1 The states a table has
1. **Seven distinct renderings, not three**: first load (skeleton with the real column layout), empty because nothing exists yet, empty because filters match nothing, refreshing (old rows kept, a small busy mark), failed (message with a retry), partial (some rows or columns failed or are hidden by permission), and stale-offline (shown data may be old, with its age).
2. **Empty-because-none and empty-because-filtered are different messages.** The first says what a row is and offers the creating action; the second names the active filters and offers "clear filters". Symptom: a user with a typo in a filter thinks the product has no data.
3. **Never render an empty state from a failed or not-yet-run request.** Test the error and loading flags before the empty branch. Symptom: a flash of "No results" before the data arrives, or a permanent one after a 500.
4. **Keep the previous rows while refetching on sort or page change**, dim them and mark busy; blanking the table moves the scroll and the layout. Keep the header and the toolbar in place.
5. **A failed refetch after a success keeps the old rows and says the refresh failed**; do not replace data with an error card unless there are no rows to keep.
6. **A permission-hidden column or row set is not an empty set.** Say "some columns are hidden for your role" or not at all, but never show wrong totals computed on hidden rows without noting it.
7. **Row-level states exist too**: saving, saved, failed with the reason; an inline edit that fails restores the old value and says why.
8. **Loading skeletons keep the final column widths** to avoid layout shift when data arrives.

## 2.2 Column state persistence
1. **Persist what the user chose**: column order, width, visibility, pinning, sort, page size. Not the current page or the selection.
2. **Store it per user and per table id, on the server for work tools and in local storage for conveniences.** A layout that matters ("my invoice view") deserves the server so it follows the user across devices.
3. **Version the stored layout.** After a release adds, renames or removes a column, an old layout refers to ids that do not exist or hides the new column forever; on load, drop unknown ids and append new columns with their default state.
4. **Validate on read.** Storage can hold garbage, an old schema or another user's data; fall back to defaults on any error and never crash the page.
5. **Offer "reset to default"** next to every persisted layout; a user cannot recover from a hidden-column mistake otherwise.
6. **Role-restricted columns are removed from a stored layout at load**, not just hidden by CSS.
7. **The library keeps this state itself** (sorting, filters, pagination, visibility, order, sizing, pinning, selection); you can own a slice and persist it. Persist the serialisable part only; functions and row objects do not survive a reload.

## 2.3 What belongs in the URL
1. **Sort, filters, search and page belong in the URL** so a refresh, a shared link and the back button work; the details are in `filters-search-and-saved-views-pitfalls` §1.
2. **Column layout and density do not**: they are preferences, not part of what is being looked at.
3. **Selection does not**: never put 500 ids in a link.

## Checks
- Throttle the network and force a 500: are loading, error and empty all different on screen?
- Open the table with a filter that matches nothing and with an empty account: are the messages different?
- Reload with a stored layout from before a column was renamed: does the table render and keep the rest?
- Resize a column, reload, log in on another device: is the behaviour what the layout scope promised?
