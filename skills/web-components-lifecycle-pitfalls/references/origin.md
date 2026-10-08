# web-components-lifecycle-pitfalls: origin and source stamps

> Provenance of `skills/web-components-lifecycle-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from standards text and reading, never run in a browser by us. No element was defined
or constructed while writing it.

**Merge intent.** A broader web-components conventions block (written around one template library) exists only
on the unmerged branch of the frontend sourcing pull request (118). This block was written standalone, with a
name that cannot collide, to hold the native-platform gaps found in a comparison against it. It is meant to be
merged into the same-named framework block when that pull request lands, section by section, and then removed.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The WHATWG HTML standard, custom-elements chapter | standard text, read 2026-10-08 | Constructor requirements, `NotSupportedError` on duplicate name or constructor, attribute callbacks on upgrade, customized built-in definition, valid-name restrictions |
| The MDN custom-elements guide | MDN content, read 2026-10-08 | `connectedCallback` runs on every insertion and before children are added, `observedAttributes`, shadow root in the constructor, Safari and customized built-ins |
| The eslint-plugin-wc rule documentation (the opening rationale of all 22 rule pages read) | MIT, read 2026-10-08 | Rationale for attach in constructor, no attributes or children in constructor, no child traversal in the two callbacks, listener teardown, define guard and ordering, global exposure, no closed roots, no self classes, `on` prefix collision, typos, guard on super calls |

## Rewrite notes
Rules are re-explained principle first. Where the lint plugin gives an opinion (global exposure, one element
per file, open roots) it is stated as a convention, not a platform fact. The plugin's "avoid constructors
altogether" rule was **not** adopted: it conflicts with the platform-supported practice of attaching the shadow
root in the constructor. The verification lists are ours.

## Not verified
1. **The MDN statements** came through a summarising fetch tool; the facts match the standard where both speak,
   but none was run.
2. **Callback order for cloned and imported nodes** was not read.
3. **Safari support for customized built-ins** is as stated by MDN and the lint plugin; not tested.
4. **Nothing here was run.**
5. **Dropped from the review's list:** form-associated elements and `ElementInternals`, adopted style sheets,
   `::part` and `exportparts`, and the custom-elements manifest (P3): no source was read, and the review itself
   said a source had still to be found.
6. **Written by us, not sourced:** the verification lists and the output/checkpoint paragraph of `SKILL.md`.

## Related blocks
`accessibility`, `testing-anti-patterns`, `typescript-patterns`.
