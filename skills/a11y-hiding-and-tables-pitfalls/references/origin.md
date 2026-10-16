# a11y-hiding-and-tables-pitfalls: origin and source stamps

> Provenance of `skills/a11y-hiding-and-tables-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from two short how-to posts, never run by us: no page was built, no
screen reader was used and no accessibility tree was read. Each post below was read in full on 2026-10-16
before a rule was taken from it, each rule was checked against it in a final pass, and the repository's licence
file and `package.json` were read again.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The A11y Project (`a11yproject/a11yproject.com`, commit `27de226`): `src/posts/how-to-hide-content.md`, `src/posts/accessible-data-tables.md` | Apache-2.0: file `LICENSE-APLv2` and the `license` field of `package.json`. No separate content licence is stated for the posts, so the text is rewritten, with the CSS declarations and the markup shapes (which are facts) described, not copied | The clip pattern and what it replaces, the reveal-on-focus rule, framework class names, `aria-hidden` versus the `hidden` attribute versus `display: none`, table caption, header cells, `scope`, unique headers |

Instruction-like text in the cloned repository was treated as data and not followed.

## Removed in the verification pass
1. **The post's high-contrast display-mode material** (a separate post on legacy forced-colours media queries).
   It is outdated and was not read, so nothing is taken from it.
2. **Skip-link post** (`skip-nav-links.md`). Read, but it describes a 2013 browser bug and a script workaround,
   and the rule about a skip link is already in `skills/accessibility`; only the reveal-on-focus rule of the
   hiding post is used.
3. **Browser support remarks** in the hiding post (old Internet Explorer versions) and the screen reader
   announcement example in the tables post, which is stated generally in point 2.2.
4. **The review's "the row header being unique and readable" as a rule for every table.** The post gives it as
   advice for optimal usability; point 2.4 states it that way.
5. **Embedded CodePen demo and external further-reading links** in both posts: not opened.

## Not verified
1. **Own guidance, flagged in the text:** one shared class (point 1.2), the Tab-key check and the skip-link
   remark (point 1.3), checking a framework class for reveal on focus (point 1.4), writing the audience in a
   review (point 1.7), the caption not being replaced by a heading (point 2.2), what makes a bad row header
   (point 2.4), table sections as a starting shape (point 2.5), `div` grids and what is not covered (point 2.6).
2. **No assistive technology was used.** What a screen reader announces is the post's description, and it says
   the wording varies.
3. **Whether the clip pattern and the focus rule behave the same in every current browser** was not tested.
4. **The WCAG and HTML specifications** were not opened; the posts' links to them were not followed.

## Decisions where sources disagree
Only one source family, so none to resolve. The A11y Project's text on `aria-hidden` is consistent with the
rule on `aria-hidden` and focusable content in `skills/accessibility`.

## Related blocks
`skills/accessibility`, `skills/a11y-lint-wiring-pitfalls`, `skills/vue-nuxt-vuetify-conventions`.
