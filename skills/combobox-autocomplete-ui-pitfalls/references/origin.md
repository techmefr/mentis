# combobox-autocomplete-ui-pitfalls: origin and source stamps

> Provenance of `skills/combobox-autocomplete-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No field was built, run or tested while writing it. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| W3C WAI-ARIA Authoring Practices (combobox, listbox patterns) and the WAI-ARIA specification | W3C Software and Document License, not MIT/Apache/CC BY | Public facts only (focus stays on the input, `aria-activedescendant`, `aria-expanded`, `aria-controls`, `aria-autocomplete`); the pages were not opened for this pass |

No MIT, Apache-2.0 or CC BY source was read for this block.

## Own craft, not from a source
Debounce and minimum length, race handling and cancellation, stable list while loading, the typed query against the committed value, stored values outside the loaded page, key behaviour, announcements, state list, multi-select and chip behaviour, creating options, tests, framework pointers.

## Removed
Library-specific option names and install steps; styling of the popup; virtual-list implementation detail.

## Not verified
1. **ARIA attributes and the keyboard model** were recalled from the public specification, not re-read. Re-read before relying.
2. **The 16 CSS pixel zoom behaviour on iOS** is remembered browser behaviour, not re-checked.
3. **Framework pointers** (headless libraries, Vuetify, htmx, Livewire) name features from memory; no version was checked.
4. **No performance number** is stated; none was measured.
