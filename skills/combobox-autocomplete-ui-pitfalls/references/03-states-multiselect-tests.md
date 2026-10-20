# combobox-autocomplete-ui-pitfalls §3 — States, multi-select, creation and tests

Own craft knowledge; no source read for this section.

## 3.1 States
1. **Six states, each visibly different: idle (closed), loading with nothing to show, results, no match, error, and disabled or read-only.** Symptom: a blank panel that could mean any of them.
2. **Loading with nothing yet shows a short placeholder row** ("searching"); loading with a previous list keeps it (§1.3).
3. **No match says what was searched** ("no result for 'xyz'") and, where it applies, offers the way forward: broaden, or create (§3.5).
4. **Error says the search failed and offers a retry in the panel**, keeps the typed text and never looks like "no match". An aborted request is neither (§1.2).
5. **A disabled field keeps its value visible and explains why** when the reason is not obvious; a read-only field is still focusable and copyable.
6. **A required field reports its error on blur or submit, not while the list is open**, and the message names the problem ("choose an option from the list") when free text is not accepted.

## 3.2 Free text against a required choice
1. **Symptom: the user typed a full name, never picked it, and the form saved nothing or the typed text.** Decide whether the field accepts only options or free text, and enforce it.
2. **Only options**: commit nothing on blur unless one option matches exactly; show an error on submit if the text is not a chosen option.
3. **Free text allowed**: the value is the text, and no hidden id exists. Do not mix both in one field.
4. **Never validate only in the browser**: the server checks the id exists and the user may use it (`security-hardening` §3).

## 3.3 Multi-select
1. **Selected values show as chips next to or inside the input; each has its own remove control with a name** ("remove Paris") and is reachable by keyboard. Symptom: a row of chips with unlabeled "x" buttons.
2. **Backspace on an empty input removes the last chip, or first moves focus onto it**; pick one and make it announce the removal.
3. **Selecting keeps the list open and clears the query** (or keeps it, as a documented choice) so several picks are fast; already chosen options are marked, or hidden, never silently duplicated.
4. **Many chips wrap or collapse to "+3" with a way to expand**, never scroll sideways inside the field.
5. **A maximum count is stated before it is reached** and blocks the extra pick with a message.
6. **Store ids, not labels**, and load labels for the saved ones together with the form (§1); a saved set of 200 needs a paged reading, not 200 lookups.
7. **"Select all" in an async list means the loaded options only**, unless the server can take a filter; say which (the same rule as `data-table-ui-pitfalls` §1.5).

## 3.4 Removing, clearing and announcing
1. **A clear button is a real button with a name**, reachable by Tab and not shown by hover only.
2. **Clearing returns focus to the input** and empties both the text and the committed value.
3. **Announce add and remove** in the live region (§2.4), once per action.

## 3.5 Creating a new option
1. **Offer "Create 'xyz'" as the last row only when the text matches nothing exactly** (case and accent aware) and the user may create. Symptom: duplicates ("Acme" and "acme") created because the row was always shown.
2. **Creation is a normal request with the same states as a search**: pending, failed (keep the text, show why), and done (the new option is selected and in the cache).
3. **Do not let a double Enter create it twice**: the row is inert while the request runs, and the server rejects a duplicate key (`security-hardening` §3).
4. **When creation needs more than a name**, open a dialog (`modal-drawer-dialog-ui-pitfalls`) and return the new option to the field; the field keeps the typed text meanwhile.
5. **Permissions apply**: hide or disable the create row for a user who may not create, and let the server refuse anyway.

## 3.6 Performance
1. **Symptom: the field lags on an option list of a few hundred rows with rich rows.** Fix first at the server (smaller pages, §1.4); render only visible rows (virtual list) when a long list is genuinely needed, and keep keyboard scrolling and `aria-activedescendant` correct with a virtualised list (set the position and total on each option when the full set is not in the page).
2. **Do not re-render the whole list for a hover.** Highlight state belongs to one index, not to each option.
3. **Measure before optimising** and keep the budget as a number your team set, not one from a library page.

## 3.7 Tests
1. **Fake timers and a controllable fake network**, so a test can answer request two before request one.
2. **Race test**: type "pa", then "par"; resolve the second first, then the first; the list shows the second's results.
3. **Stored value test**: render with a value whose option is not in the first page; the label shows.
4. **Keyboard test**: open, move, choose with Enter, assert no form submission and the value set; Escape closes without clearing the value.
5. **State tests**: loading, no match, error with retry and aborted request each render their own message.
6. **Multi-select test**: add, remove with the keyboard, maximum reached, duplicate refused.
7. **Accessibility test**: roles, `aria-expanded`, `aria-controls` and `aria-activedescendant` point at existing elements; run the project's checker on the open state, not only the closed one (`a11y-lint-wiring-pitfalls`).

## 3.8 Framework pointers
Facts to re-read in the version you use; none was checked here.
1. **Headless libraries** for React and Vue ship the pattern with keyboard and ARIA done; prefer one over a hand-built field, and check that it supports async options and a value outside the loaded list.
2. **Vuetify and similar kits** offer an autocomplete and a combobox component; check the options-load hook, the "selected not in items" behaviour and chip slots before relying on defaults.
3. **Server-rendered stacks** (Livewire, htmx) debounce with an attribute and cancel previous requests differently; confirm the older response cannot replace the newer (`htmx-protocol-pitfalls`).
4. **The native `datalist`** is cheap and accessible for short static lists and weak for async data, rich rows and styling.
