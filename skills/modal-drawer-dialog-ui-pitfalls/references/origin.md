# modal-drawer-dialog-ui-pitfalls: origin and source stamps

> Provenance of `skills/modal-drawer-dialog-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No dialog was built, run or tested while writing it. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| W3C WAI-ARIA Authoring Practices (dialog pattern) and the HTML specification (dialog element) | W3C Software and Document License / WHATWG terms, not MIT/Apache/CC BY | Public facts only (dialog and alertdialog roles, `aria-modal`, `aria-labelledby`, native dialog modal behaviour and Escape); the pages were not opened for this pass |

No MIT, Apache-2.0 or CC BY source was read for this block.

## Own craft, not from a source
Dialog against page, focus return and fallback, Escape on the top layer, press-and-release backdrop rule, scroll lock counting and gutter, layer scale, dirty-state guard, destructive confirmation wording, drawer rules, mobile viewport and keyboard handling, URL-addressable dialog and history rules, tests, framework pointers.

## Removed
Library-specific code and option names; animation recipes; z-index numeric values.

## Not verified
1. **Native dialog element behaviour and browser support** were recalled, not re-read. Re-read before relying.
2. **ARIA role and attribute facts** were recalled from the public specification. Re-read before relying.
3. **Mobile viewport behaviour** (dynamic viewport units, keyboard resizing) varies by browser and was not tested.
4. **Framework pointers** (headless libraries, Vuetify, Livewire, Inertia, htmx) name features from memory; no version was checked.
