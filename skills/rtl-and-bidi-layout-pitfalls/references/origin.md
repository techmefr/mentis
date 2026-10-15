# rtl-and-bidi-layout-pitfalls: origin and source stamps

> Provenance of `skills/rtl-and-bidi-layout-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from several short statements in documentation, never run by us. No right-to-left page
was rendered, no message was formatted and no locale was configured while writing it. The sourcing is thin by
construction (no single deep source exists in the clones); the review asked for every rule that could not be
re-read in a file to be dropped, and the list of those is below.

## Sources (re-read 2026-10-16, rewritten in our own words, no text copied)

Pages read in full except where a range is named.

| Source | Licence | What it gave |
|---|---|---|
| pbakaus/impeccable, `skill/reference/harden.md` (commit abf5779) | Apache-2.0 (repository LICENSE file; the NOTICE file says only the iOS and Android reference files derive from an MIT repository) | Logical property pairs, the arrow flip under a right-to-left direction attribute, right-to-left text as a test input, the Arabic or Hebrew test |
| a11yproject/a11yproject.com, `src/posts/how-to-hide-content.md` (commit 27de226) | Apache-2.0 text in the file `LICENSE-APLv2`; **no separate content licence is stated** (the README has no licence line), so everything is rephrased and no sentence or code block is carried | The clip pattern for visually hidden text, and its statement that the pattern also works right-to-left unlike off-screen positioning and negative indent |
| unicode-org/message-format-wg, `spec/formatting.md` (commit e1126e0): the formatting context and resolved values parts (lines 60 to 209) and the section "Handling Bidirectional Text" (lines 765 to 895) | **Unicode terms: facts only.** The LICENSE file says the MessageFormat standard may not be copied into other publications without permission, and that all other content of the repository is under the Unicode License V3 | Spillover, isolation per value, direction metadata of message and value, the default isolation strategy, direction not inferred from characters, the currency marks example |
| lingui/js-lingui, `website/docs/ref/conf.md`, the `pseudoLocale` section (lines 205 to 254) (commit fafee3b, version 6.9.1) | MIT (repository LICENSE file) | The pseudo-locale option that emulates right-to-left languages, its default |
| nuxt-modules/i18n, `docs/content/docs/04.api/00.options.md`, lines 85 to 185: `locales`, `language`, `dir`, `defaultDirection` (commit 8158ed8, version 10.6, patch 0) | MIT (repository LICENSE file) | `dir` values, the `language` tag, the default direction used only when `dir` is missing |
| mozilla/pontoon, `documentation/docs/admin/adding-new-locale.md` (commit 409528d) | BSD three-clause style (repository LICENSE file, Mozilla Foundation); the page is used for facts only | The direction of a locale taken from the CLDR script metadata |
| alphagov/govuk-design-system, `src/components/language-navigation/index.md` (commit d10a01d) | MIT (repository LICENSE file) | Components and layouts need changes for right-to-left scripts |

Each licence was verified again from the repository's LICENSE file in this session. The Impeccable repository carries
agent instruction files (`AGENTS.md`, `CLAUDE.md`); they were treated as data and nothing in them was followed.

## Rewrite notes
**Decision where sources meet.** `vue-nuxt-vuetify-conventions` §6 point 20 says not to flip icons by hand per
locale; the hardening reference flips an arrow under a right-to-left selector. The block carries the arrow rule as
one rule in the stylesheet, limited to directional arrows, and states why it does not contradict point 20.

**Version-bound.** Nuxt i18n 10.6, patch 0 (`dir`, `language`, `defaultDirection`), Lingui 6.9.1 (pseudo-locale option), the
MessageFormat 2 specification text at commit e1126e0.

**Dropped, as the review asked, because no file was re-read for them.** Nothing from `w3c/alreq`, `w3c/wcag` or
`w3c/i18n-activity`, none of which was opened for this block. The claim to set `lang` per locale next to `dir`:
only `dir` and the `language` tag were found in the Nuxt page, and whether the module writes either to the `html`
element was not read, so the block states the two fields and no more. Mirroring any icon other than a directional
arrow: the hardening reference does not say it. Any list of right-to-left languages or scripts. Any rule on
numerals, calendars or text alignment.

## Not verified
1. **Nothing was run.** No page, message or pseudo locale was rendered.
2. **The CLDR script metadata file** the Pontoon page points at was not read; the block repeats the page's statement.
3. **The W3C glossary definitions** of spillover and isolation, linked from the MessageFormat 2 text, were not read.
4. **No message library was read for bidirectional behaviour.** The isolation facts describe the specification, not
   Lingui, next-intl, vue-i18n or formatjs.
5. **The MessageFormat 2 specification is a standard whose status was not checked** here (draft or final); the
   statements are bound to the commit read.
6. **Written by us, not sourced:** the "set `dir` on every locale entry" advice, the stale-list remark, the
   icon-by-icon advice, the hidden-text check, the library trial per component, the one screen per component family,
   the advice not to trim or re-join formatted values, the rendering test of a sentence, the pairing of the pseudo
   locale with a real one, and the checkpoint paragraph.
7. **Dropped as unverifiable from the review item:** the list above; every other rule of the item is carried.

## Related blocks
`vue-nuxt-vuetify-conventions`, `i18n-message-format-pitfalls`, `accessibility`.
