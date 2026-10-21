# web-components-forms-a11y-pitfalls: origin and source stamps

> Provenance of `skills/web-components-forms-a11y-pitfalls`. Read it when a rule has to be traced to its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No element was built or run in a browser while writing it. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| whatwg/html, custom-elements chapter, scripting chapter (template element) at the live standard | CC BY 4.0 for the text, BSD-3-Clause for code in it (`LICENSE` read 2026-10-20) | Form-associated elements (`formAssociated`, `attachInternals`, `setFormValue`, validity flags, the four form callbacks and their arguments), default semantics through the internals, custom states and the state pseudo-class, the need for tab stop plus role plus label on an autonomous button, declarative shadow root attributes (mode, delegated focus, serialisable, clonable) |
| whatwg/dom, event interface and retargeting (live standard) | CC BY 4.0 (`LICENSE` read 2026-10-20) | The composed flag, the composed path and closed roots, the retargeting algorithm |
| WHATWG HTML standard, custom-elements chapter (ElementInternals interface, `shadowRoot` getter, readonly, restore reasons), forms chapter (label `for`), parsing and dynamic-markup-insertion chapters (declarative shadow root, unsafe fragment parsing modes), second read 2026-10-20 | CC BY 4.0 (same repository licence) | Internals member list, shadow root access limited to declarative roots, readonly effect, restore reasons, same-tree rule for `for`, legacy `innerHTML` mode disabling declarative roots (§1.1.4, §1.3.3, §1.3.5, §2.1.4, §2.1.5, §3.3.3, §3.3.4) |
| W3C CSS Shadow Module Level 1 (editor's draft) and CSS Shadow Parts Level 1, read 2026-10-20 | W3C document licence, facts only, own words | `part` and `exportparts`, no chained `::part()`, slotted selector reaches only assigned elements, `:host` specificity (§3.1.1, §3.1.5, §3.2.1) |
| W3C CSS Cascade Level 5, encapsulation contexts, read 2026-10-20 | W3C document licence, facts only | Outer context wins for normal declarations, inner for important ones (§3.1.3) |

## Own craft, not from a source
Attribute against property policy and property upgrade, id references across roots, focus delegation consequences, styling hooks (custom properties, parts, host against `:host`, slotted content), hydration of declarative roots, the checks and the checkpoint.

## Removed
Constructor, callbacks, registration (`skills/web-components-lifecycle-pitfalls`); Lit specifics (`skills/web-components-conventions`); the lit.dev documentation (not in the Lit repository, so not read for this block); web.dev articles (the repository licence is CC BY 3.0 with moved paths, nothing was found to read).

## Verified on the second pass, 2026-10-20
10 verified (form members on the internals, restore reasons and state argument, same-tree rule for the label `for` attribute, `:state()` and `states` as the custom-state mechanism, parts and forwarding, outer-wins cascade, slotted reach, internals `shadowRoot` getter limits, declarative roots only through unsafe parse entry points, `readonly` effect), 1 corrected (`readonly`: the standard bars the element from constraint validation and says nothing about submission), 0 deleted.

## Not verified
1. **Nothing was run.** Every symptom is reasoned from the standards, not reproduced.
2. **Adopted style sheets** (§3.1.7) are recalled from memory; parts, cascade order and slotted reach were re-read in the CSS specifications on the second pass.
3. **`aria-labelledby` and `aria-describedby` across shadow roots, and the focus, label and screen-reader behaviour** are recalled public practice, not re-read (the label `for` rule was).
4. **Browser support** (custom-state pseudo-class, declarative shadow DOM parsing entry points, internals aria properties) is not checked; no table is given.
5. **Custom-state pseudo-class support** (§2.3.3): the mechanism was re-read, browser support was not checked.
6. **Written by us:** the checks lists and the output/checkpoint of `SKILL.md`.

## Related blocks
`web-components-lifecycle-pitfalls`, `web-components-conventions`, `accessibility`, `nuxt-no-hydration-nondeterminism`, `csp-and-sanitiser-pitfalls`.
