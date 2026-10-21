# filters-search-and-saved-views-pitfalls §2 — Search, facets, semantics and tests

Sources: own craft, with the faceting and filtering facts from the TanStack Table guides (MIT, read 2026-10-20) and the accessibility facts from WCAG 2.2, WAI-ARIA 1.2, the ARIA Authoring Practices and the HTML Standard (read 2026-10-20, see `origin.md`).

## 2.1 Server against client filtering
1. **Filter over the same dataset as sorting and paging.** Client-side filtering is right when the browser holds the complete set; with a paged server response it filters only the loaded rows, which the library documentation also states. Symptom: a search that finds nothing for a record that exists on page 9.
2. **When filtering is server-side, say so in the interface** ("search all invoices") and send the filter model, not the matched ids.
3. **A client-side quick filter over loaded rows is a different control** and carries a different label ("filter this page").
4. **Case and accent folding live in one place.** Client-side comparators default to case-insensitive or case-sensitive depending on which one you pick; the server may differ. Align them or users see different results from the same typing.
5. **Do not search on formatted values** (a date shown as 20/10/2026, a currency string) unless the search text is parsed the same way; filter on the stored value.

## 2.2 Debounce, races and cancellation
1. **Debounce text input before querying**, with a delay long enough to avoid a request per keystroke and short enough to feel immediate; measure on the real data rather than copying a number. Run non-text controls (checkbox, select) at once.
2. **Cancel or ignore superseded requests.** Symptom: type "inv", then "invoice"; the "inv" answer arrives last and overwrites the screen. Tag each request with its filter key and render only the one that matches the current key (`data-fetching-state-conventions` §2).
3. **Minimum length is a product choice, not a default**: searching on one character may be expensive on the server; if you wait for more characters, show a hint.
4. **Keep the previous results visible while the new ones load**, with a busy mark; flashing an empty list per keystroke reads as a failure.
5. **Server limits are the real protection**: rate-limit and cap query cost and length on the server; the debounce is only politeness.
6. **IME composition**: do not fire a search in the middle of composing characters (languages entered through composition); wait for the composition to end. UI Events defines a composition session as one start, one or more updates and one end, and marks key and input events inside it with an isComposing flag, which is the check to use (W3C UI Events, read 2026-10-20).
7. **Escape clears and returns focus**; the clear button is a real, named button. The combobox pattern lists clearing on Escape only as optional, and only once the popup is already closed, so do not make it the single way to clear.

## 2.3 Facets
1. **A facet shows the values present and their counts for the other active filters.** Symptom: a facet says "Paid (12)" and clicking it shows 9 rows. Cause: the count ignored another filter, or counts rows the user cannot see. Compute the count with the same filter and permissions as the list.
2. **Decide per facet whether it excludes its own condition when counting** (a multi-select usually does, so users can add values; a single-select may not). Document it.
3. **Counts cost queries.** Compute them on the server in one grouped query, cap the number of values (top N plus "more"), and skip or approximate on very large sets with a label.
4. **Facet value order is a choice**: by count, alphabetical or a fixed business order; keep it stable while the user clicks, or values jump under the pointer.
5. **Nulls and empties are a value** ("None", "Unassigned"); omitting them makes the counts not add up.
6. **Range facets (amount, date) need sensible buckets or min and max from the filtered rows**, and must not offer ranges that give zero rows without saying so.
7. **Counts may be slightly stale on live data**; mark them approximate if they are cached.

## 2.4 Semantics that bite
1. **Within one field, multiple values mean OR; across fields they mean AND.** Show it in the interface ("Status is Open or Pending, and Owner is Me") and keep the rule the same on the server.
2. **"Not" operators and nulls**: "status is not Closed" must say whether rows with no status match; SQL three-valued logic drops them silently.
3. **Dates and time zones**: a "date" filter on a timestamp column needs a day boundary in a named time zone (the user's, or the business one) and an inclusive end of day; "today" computed in the server zone shifts the rows at night. Say which zone the range uses.
4. **Text search**: define whether it is contains, prefix or full text, which columns it covers, and whether it matches across words; show the covered fields ("searching name, reference, email").
5. **Numbers**: filter on stored numeric values with a unit and currency shown; do not compare formatted strings.
6. **Free-text values go through parameters or the query builder, never string concatenation**; for wildcard characters in a contains search, escape them.

## 2.5 Empty results
1. **Name the filters** ("No invoices match: Status Open, Owner Me, Date this month") with a clear-all and per-chip remove.
2. **Offer the cheapest widening first**: remove the last added condition, show "close matches" only if they are really computed.
3. **Distinguish empty because nothing exists from empty because of filters** (`data-table-ui-pitfalls` §2.1); never show "no results" while loading or after an error.
4. **A zero count in a facet is still clickable only if it makes sense**; otherwise disable it with the reason.

## 2.6 Accessibility
1. **Every filter control has a visible label**, not only a placeholder; the placeholder disappears and often fails contrast (`accessibility`). WCAG 2.2 SC 3.3.2 requires labels or instructions where input is needed, and the HTML Standard says the placeholder attribute should not stand in for a label.
2. **Search is a form with a search landmark and a named input**; Enter submits, and the button is real. The HTML search element (or role search) creates the landmark; with more than one on a page, each needs a unique label (ARIA Authoring Practices, search landmark example). The element is for the controls, not for the results list, which belongs in the main content (HTML Standard, the search element).
3. **Announce result changes in a polite live region** ("12 results"), once per settled query, not per keystroke. WCAG 2.2 SC 4.1.3 asks that status messages be exposed by role or property without taking focus; in WAI-ARIA 1.2 the status role is implicitly polite and atomic, while alert is assertive and meant for urgent news.
4. **Applied filters are listed as text** (chips with a remove button named "Remove filter Status: Open"); colour alone is not the state (WCAG 2.2 SC 1.4.1). Keep the visible chip text at the start of the button name so the spoken name contains it (SC 2.5.3 Label in Name).
5. **Filter panels and popovers are keyboard-operable** with focus returning to the trigger when they close; a drawer filter on small screens traps focus only while it is modal. The modal dialog pattern moves focus in on open, keeps Tab inside, closes on Escape, and returns focus to the invoking element unless that element is gone.
6. **Date pickers allow typing**; a calendar-only control is hard for keyboard and assistive technology. The date picker dialog example keeps a text input with a stated format (tied by aria-describedby) next to the calendar button, and the calendar fills that input.

## 2.7 Tests
1. **Round trip**: build a filter, serialise to the URL, load the URL in a fresh session, assert the same controls and the same request.
2. **Parameter hygiene**: unknown field, bad value, duplicate key, an over-long value; assert a notice and a sane default, no server error.
3. **One model, many consumers**: for a seeded set, assert the table count, the displayed count and the export size are equal.
4. **Race**: delay the first response and answer the second first; assert the screen shows the second.
5. **Facets**: assert a facet count equals the rows after clicking it, with another filter active and as a restricted user.
6. **Semantics**: rows with null values, timestamps near midnight in two time zones, wildcard characters in the text, OR within a field and AND across.
7. **Saved views**: migrate after a field rename, shared view for a user with fewer permissions, deleted view link.
8. **Accessibility**: labels, live-region message, chip remove names, keyboard-only pass through the filter panel.

## 2.8 Framework pointers (reference only)
1. **Headless table engines** keep column filters and a global filter as state you can own and sync to the URL; mark filtering manual when the server filters (`data-table-ui-pitfalls` §3.5).
2. **Nuxt and Vue router**: read and write filters through the router query with replace for typing and push for commits; validate with a schema at read time (`vue-router-pitfalls`, `vue-nuxt-vuetify-conventions`).
3. **Laravel**: translate the filter model to the query in one place with an allow-list of fields and operators; the REST resource packages offer such filters (`laravel-lomkit-rest-api`); reuse the same query for count and export.
4. **Search engines**: facet counts are aggregations over the filtered set; mind analysers and collation (`search-engine-index-settings-pitfalls`, `collation-and-locale-aware-search-pitfalls`).
