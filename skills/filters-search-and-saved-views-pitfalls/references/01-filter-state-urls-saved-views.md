# filters-search-and-saved-views-pitfalls §1 — Filter state, URLs and saved views

Sources: own craft, with the filter-state facts from the TanStack Table filtering guides (MIT, read 2026-10-20).

## 1.1 One filter model
1. **Define the filter as one serialisable object** (field, operator, value per condition, plus the search text), not as the state of widgets. Controls render it; the URL, the request, the count, the export and the saved view all consume the same object.
2. **Symptom: the count says 40, the table shows 38, the export has 41.** Cause: three code paths rebuilt the filter from the controls. Fix: one function turns the object into the query, used by all three.
3. **Give each condition a stable id and an operator** (equals, in, contains, between, is empty); the default operator per field type is a product decision, written down once.
4. **An empty filter value means "no condition", not "match empty".** The library has an auto-remove hook for exactly this: a cleared input removes the condition. Provide an explicit "is empty" operator for the other meaning.
5. **Keep applied and draft filters apart when a panel has an Apply button**; the URL and the request carry the applied one only.
6. **Reset paging to the first page when any filter changes**, and clear selection that no longer matches (`data-table-ui-pitfalls` §1.1 and §1.5).

## 1.2 URL state
1. **Filters, search, sort and page belong in the query string** so reload, back, forward and a pasted link all show the same rows. A view the URL cannot reproduce is a bug report nobody can reproduce either.
2. **Use readable, stable parameter names and one encoding scheme** (repeat a key for a list, or a documented separator); a nested JSON blob in the URL is fragile and leaks structure.
3. **Validate on read.** A parameter can be missing, hand-edited, from an older release, or hostile: unknown fields are ignored with a visible notice, bad values fall back to the default, nothing is injected into a query as a raw string.
4. **Keep sensitive values out of the URL** (personal data, tokens, free text a user would not paste into a chat); URLs go to logs, referrers and history. Use an id and look the value up.
5. **Do not push a history entry per keystroke.** Replace the entry while typing and push on commit; otherwise Back walks through every letter. The HTML Standard defines the two history calls as one routine with a push or replace mode, both staying in the same document, the URL must be one the page may rewrite or a SecurityError is thrown, and browsers may cap the state entries a page adds, so a push per keystroke can also hit that cap (HTML Standard, history API, read 2026-10-20).
6. **Short URLs for long filters**: past a few hundred characters, store the filter as a saved view or a server-side object and put its id in the URL.
7. **A date in the URL is a date with a rule**: store an absolute ISO date, or a named relative range ("last 30 days") resolved at read time and say which; never a locale-formatted string.
8. **Default values stay out of the URL** so a link with no parameters stays the clean default view.

## 1.3 Saved views
1. **A saved view stores the filter object, sort, visible columns and grouping, with a name, an owner and a version**, not a screenshot of widget state.
2. **Distinguish private, shared with a team and shared with everyone**, and who may edit or delete a shared one. Ownership change when the owner leaves is a defined rule, not an orphan.
3. **A view that depends on "me" or "today" stores the token, not the resolved value** ("assigned to me", "this month"); otherwise a shared view shows its author's data.
4. **Shared views never widen access.** A view resolves under the viewer's permissions; a filter that names a value the viewer cannot see is dropped with a notice, and counts never reveal hidden rows.
5. **Versioning**: when a field is renamed, removed or changes type, migrate stored views or mark them "needs attention" with the offending condition; do not silently show everything.
6. **Show whether the current state differs from the saved view** (modified indicator) and offer save, save as new and revert.
7. **Default view per user and a global default**, with a way back to "all rows"; a persisted default the user forgot is the usual cause of "my data is missing".
8. **Counting and limits**: cap the number of views, conditions per view and length of names, validate on the server.

## 1.4 Sharing links and bookmarks
1. **A shared link opens the view as the recipient**, with their permissions, and says so when conditions were dropped.
2. **A link to a deleted saved view says it was deleted** and opens the default, not a blank page.

## 1.5 Authorization
1. **Check on the server, per request, that the caller may read the view and every field it filters on.** Filtering on a field the caller cannot see leaks it by presence or absence of rows.
2. **Reject disallowed filter fields and operators server-side** rather than trusting that the interface did not offer them; allow-list fields, operators and sort columns.

## Checks
- Copy the URL into a private window of another permitted user: same rows, or a notice for what changed?
- Edit the URL by hand with a wrong field, a wrong value, a repeated key: does the page degrade without an error?
- Rename a field after a view was saved: what does the old view show?
- Compare the table count, the header count and the export row count for one filter.
