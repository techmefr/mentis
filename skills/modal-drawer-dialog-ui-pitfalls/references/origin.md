# modal-drawer-dialog-ui-pitfalls: origin and source stamps

> Provenance of `skills/modal-drawer-dialog-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No dialog was built, run or tested while writing it. Read date: 2026-10-20.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: press-and-release backdrop fix, webview target check for the native element, native-shell back handler, shared-component check, skip-when line.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| W3C ARIA Authoring Practices, modal dialog pattern (https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) | W3C document licence (liability, trademark, permissive-software terms), not MIT/Apache/CC BY; facts only | Keys, initial focus, focus return, `aria-modal`, labelling. Read 2026-10-20 through a summarising fetcher |
| W3C ARIA Authoring Practices, alert dialog pattern (https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/) | same W3C terms; facts only | Role purpose and required labelling. Read 2026-10-20 through a summarising fetcher |
| HTML Standard, the dialog element (https://html.spec.whatwg.org/multipage/interactive-elements.html#the-dialog-element) | CC BY 4.0 for the text, confirmed in the repository LICENSE file on 2026-10-20 (code snippets BSD-3-Clause) | Modal and non-modal methods, top layer, inert document, close request and cancel event, `closedby`, focus restoration. Read through a summarising fetcher, excerpt only |

Credit: WHATWG, HTML Standard, https://html.spec.whatwg.org/ (CC BY 4.0).

No permissive source found for scroll lock, stacking, dirty-state confirmation, mobile and URL-addressable dialog points, searched: W3C authoring practices, HTML Standard; React Aria (Apache-2.0) and Radix (MIT) licences confirmed but their modal documentation could not be fetched, so no library documentation was read.

## Own craft, not from a source
Dialog against page, focus return and fallback, Escape on the top layer, press-and-release backdrop rule, scroll lock counting and gutter, layer scale, dirty-state guard, destructive confirmation wording, drawer rules, mobile viewport and keyboard handling, URL-addressable dialog and history rules, tests, framework pointers.

## Removed
Library-specific code and option names; animation recipes; z-index numeric values.

## Not verified
1. **Verified 2026-10-20**: modal inert document, top layer, cancel event, `closedby`, focus restoration, show against modal methods, role and labelling, Tab wrap, Escape, initial focus, alertdialog role. **Corrected**: §1.2.1 (description optional on a dialog, required on an alert dialog), §1.4.2 (backdrop is a pseudo-element; outside click closes only with the attribute set), §1.4.3 (`aria-modal` only when truly blocking), §2.4.2 (the alert dialog page gives no focus rule). **Added**: §1.4.7, §1.4.8, §2.3.8. Deleted: none.
2. **Still unverified**: browser support of the dialog element and `closedby` (no support table read), the press-and-release rule, scroll lock, layer scale, dirty-state, mobile and URL points, `form method=dialog` (the excerpt did not cover it).
3. **Mobile viewport behaviour** (dynamic viewport units, keyboard resizing) varies by browser and was not tested.
4. **Framework pointers** (headless libraries, Vuetify, Livewire, Inertia, htmx) name features from memory; no version was checked.
