# combobox-autocomplete-ui-pitfalls: origin and source stamps

> Provenance of `skills/combobox-autocomplete-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No field was built, run or tested while writing it. Read date: 2026-10-20.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: select-only variant section (keys, active option, Tab, empty options, Escape in a dialog), skip-when line.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| W3C ARIA Authoring Practices, combobox pattern (https://www.w3.org/WAI/ARIA/apg/patterns/combobox/) | W3C document licence (liability, trademark, permissive-software terms), not MIT/Apache/CC BY; the page was read only for facts | Focus and keys, `aria-activedescendant`, `aria-expanded`, `aria-controls` (needed only while visible), `aria-haspopup`, `aria-selected`, `aria-autocomplete` none/list/both. Read 2026-10-20 through a summarising fetcher |
| W3C WAI-ARIA 1.2 Recommendation, roles section (https://www.w3.org/TR/wai-aria-1.2/) | W3C document licence, facts only, own words | listbox must own option or group elements. Read 2026-10-20 through a summarising fetcher, first 100000 characters only |
| W3C ARIA Authoring Practices, select-only combobox example (https://www.w3.org/WAI/ARIA/apg/patterns/combobox/examples/combobox-select-only/) | same W3C terms | Select-only keys, Tab commits, Escape. Read 2026-10-20 through a summarising fetcher |
| W3C ARIA Authoring Practices, combobox list-autocomplete example and listbox pattern, read 2026-10-20 | W3C document licence, facts only | `aria-selected` only on the highlighted option, one selection attribute convention, set size and position for partial lists, option naming, wrap behaviour, no result-count announcement |
| W3C WCAG 2.2 Understanding SC 4.1.3, 3.3.2, 1.4.11, read 2026-10-20 | W3C document licence, facts only | Status messages without focus move, labels presented to all users, 3:1 contrast for state indicators |
| WHATWG DOM Standard (abort section) and HTML Standard (datalist element), read 2026-10-20 | CC BY 4.0 (WHATWG, as recorded for the HTML Standard above) | Default abort reason is an AbortError; datalist is a suggestion list linked through the list attribute |
| adobe/react-spectrum `LICENSE` | Apache-2.0, Copyright 2019 Adobe (read 2026-10-20) | Licence only: the combobox documentation path tried returned 404, so no library behaviour was taken |

Credit: WHATWG, DOM Standard and HTML Standard, https://spec.whatwg.org/ (CC BY 4.0).

No permissive source found for the debounce, minimum-length, stable-list, creation and multi-select chip points, searched: the pages above and the React Aria repository (documentation path not found).

## Own craft, not from a source
Debounce and minimum length, race handling and cancellation, stable list while loading, the typed query against the committed value, stored values outside the loaded page, key behaviour, announcements, state list, multi-select and chip behaviour, creating options, tests, framework pointers.

## Removed
Library-specific option names and install steps; styling of the popup; virtual-list implementation detail.

## Not verified
1. **Verified 2026-10-20 (APG pages, facts only)**: focus stays on the input, `aria-activedescendant`, `aria-expanded` and `aria-controls` semantics, `aria-autocomplete` values none/list/both, Down, Up, Enter, Escape, Alt+Down behaviour, select-only keys and Tab commit. **Corrected**: §2.2.1 (Down goes to the first option), §2.3.1 (`aria-controls` only needed while visible, `aria-haspopup`), §2.3.3 (value meanings), §2.6.3 and §2.6.4 (Up opens at the first option, Tab commits and the native select differs). **Second pass 2026-10-20**: Home and End in the editable variant corrected (§2.2.4: optional popup keys per the combobox page); listbox owning options or groups confirmed (§2.3.4). **Third pass 2026-10-20**: corrected §2.3.2 (aria-selected goes on the highlighted option only, one convention, not on the saved value), §2.2.1 and §2.2.3 (list example wraps and clears on Escape), §2.4.2 (the example announces no count; WCAG status messages cited instead); added §1.4.5 (option names), §2.1.2 highlight contrast and scroll note, abort name in §1.2.3, datalist facts in the framework pointers of section 3. **Still unverified**: option required context, `aria-hidden` on the popup (the page does not mention it), live-region announcements, grouping (no guidance on the page), the inline-only `aria-autocomplete` value. Deleted: none.
2. **The 16 CSS pixel zoom behaviour on iOS** is remembered browser behaviour, not re-checked.
3. **The select-only keyboard model** was checked against the authoring practices example; what each assistive technology exposes was not tested.
4. **Framework pointers** (headless libraries, Vuetify, htmx, Livewire) name features from memory; no version was checked.
5. **No performance number** is stated; none was measured.
