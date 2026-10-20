# combobox-autocomplete-ui-pitfalls §1 — Async options and races

Own craft knowledge; no source read for this section.

## 1.1 Debounce and minimum length
1. **Symptom: one request per keystroke, a flickering list and a rate-limited backend.** Check: type a six-letter word and count requests in the network panel. Fix: debounce the query so a request leaves only after a short pause in typing.
2. **Debounce the request, never the input.** The text field updates on every keystroke; only the call is delayed. A debounced field value feels broken and drops characters on a slow device.
3. **Set a minimum length only when an empty or one-letter query is costly or meaningless.** Below it, show a hint ("type two letters to search"), not an empty panel. Where the useful behaviour is "show recent or popular options on focus", send the empty query on purpose and say so.
4. **Trim and normalise before comparing.** A query that differs only by trailing space or case must not trigger a second request or a second cache entry.
5. **Skip a request that cannot change the answer.** The same normalised query as the last one in flight or in cache reuses it.

## 1.2 Out-of-order and cancelled responses
1. **Symptom: the list shows results for "pa" while the field says "paris".** Cause: two requests in flight, the older one answered last and overwrote the state.
2. **Tag every request with its query (or a counter) and apply a response only if it is still the latest.** The simple form: compare the response's query with the current normalised query before setting state.
3. **Abort what is no longer wanted.** Cancel the in-flight request when the query changes, the list closes or the component unmounts; an aborted request is not an error and must not show the error state (§3.1).
4. **Cache by query for the life of the open list**, so deleting a letter returns the earlier answer at once instead of a spinner.
5. **A library that keys data by query does 2 to 4 for you** (`data-fetching-state-conventions` §2). Check that it also keeps the previous list visible while the next loads (§1.3).

## 1.3 Keep the list stable while loading
1. **Symptom: the panel collapses to a spinner and the highlighted option jumps on every keystroke.** Fix: keep the previous options on screen, dimmed or with a small progress hint, until the new ones arrive.
2. **Reset the highlight to the first option when the options change**, never keep an index that now points at another row.
3. **Do not move the pointer target under the mouse**: replacing the list while the user is about to click causes a click on the wrong option. A short settle (apply the new list only after the response, not mid-click) avoids it.
4. **Announce the new count once per settled list**, not once per keystroke (§2.4).

## 1.4 Fetch size and ranking
1. **Return a bounded page of options** and say when more exist ("20 shown, keep typing to narrow"); never ship ten thousand rows into a dropdown.
2. **The server ranks; the client does not re-sort it.** Exact and prefix matches first is a server decision; client re-sorting hides the ranking the backend computed.
3. **Match on what users type**: accents, case, word order and spaces in names. Decide the rule once (§1.1) and test it with an accented name.
4. **Highlight the matched part of each option with a visible, non-colour-only cue**, and keep the full label readable (`accessibility` §3).

## 1.5 Two sources of truth
1. **Symptom: the input shows the typed text after the user picked an option, or the chosen label after they started editing.** Separate three things: the typed query, the selected option, and the committed value.
2. **Choosing an option sets the input text to its label and closes the list**; typing again clears the committed selection until another option is chosen (single select).
3. **Leaving the field without a choice** either restores the last committed label or clears the query, never leaves free text that looks committed. Decide which and keep it the same across the product.

## 1.6 A selected value that is not in the loaded options
1. **Symptom: an edit form opens with a blank combobox, or with a raw id.** Cause: the label is looked up in the options list, and the first page of options does not contain the saved one.
2. **Store the option id, and render the label from the record that was loaded with the form** (an included relation, or one lookup by id). Never rely on the search results to describe the current value.
3. **When the label is missing or the record was deleted**, show a clear state ("unavailable option") and let the user replace it; do not silently drop the value on save.
4. **Pre-load nothing beyond that one record.** The list is fetched when the field opens.

## Checks
```
Throttle the network to slow, type a word, delete two letters, retype: the list matches the field every time.
Open an edit form whose saved option is not on the first page of results: the label shows.
Type, then close the list: the request is cancelled and no error appears.
```
