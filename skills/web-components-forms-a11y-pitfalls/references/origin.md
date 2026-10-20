# web-components-forms-a11y-pitfalls: origin and source stamps

> Provenance of `skills/web-components-forms-a11y-pitfalls`. Read it when a rule has to be traced to its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No element was built or run in a browser while writing it. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| whatwg/html, custom-elements chapter, scripting chapter (template element) at the live standard | CC BY 4.0 for the text, BSD-3-Clause for code in it (`LICENSE` read 2026-10-20) | Form-associated elements (`formAssociated`, `attachInternals`, `setFormValue`, validity flags, the four form callbacks and their arguments), default semantics through the internals, custom states and the state pseudo-class, the need for tab stop plus role plus label on an autonomous button, declarative shadow root attributes (mode, delegated focus, serialisable, clonable) |
| whatwg/dom, event interface and retargeting (live standard) | CC BY 4.0 (`LICENSE` read 2026-10-20) | The composed flag, the composed path and closed roots, the retargeting algorithm |

## Own craft, not from a source
Attribute against property policy and property upgrade, id references across roots, focus delegation consequences, styling hooks (custom properties, parts, host against `:host`, slotted content), hydration of declarative roots, the checks and the checkpoint.

## Removed
Constructor, callbacks, registration (`skills/web-components-lifecycle-pitfalls`); Lit specifics (`skills/web-components-conventions`); the lit.dev documentation (not in the Lit repository, so not read for this block); web.dev articles (the repository licence is CC BY 3.0 with moved paths, nothing was found to read).

## Not verified
1. **Nothing was run.** Every symptom is reasoned from the standards, not reproduced.
2. **Styling hooks** (parts, inheritance, `:host` precedence, adopted style sheets) are recalled from memory; the CSS shadow-parts and scoping specifications were not read. Re-read before relying.
3. **Id references across shadow roots and the focus, label and screen-reader behaviour** are recalled public practice, not re-read.
4. **Browser support** (custom-state pseudo-class, declarative shadow DOM parsing entry points, internals aria properties) is not checked; no table is given.
5. **Reading an existing root from the internals in the upgrade case** (§3.3.3) is named but its exact API was not re-read.
6. **Written by us:** the checks lists and the output/checkpoint of `SKILL.md`.

## Related blocks
`web-components-lifecycle-pitfalls`, `web-components-conventions`, `accessibility`, `nuxt-no-hydration-nondeterminism`, `csp-and-sanitiser-pitfalls`.
