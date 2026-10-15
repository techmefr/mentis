# i18n-message-format-pitfalls: origin and source stamps

> Provenance of `skills/i18n-message-format-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No message was rendered,
no linter was executed and no translation tool was used while writing it. Library names and options are as the
repositories below show them on the read date.

## Sources (re-read 2026-10-15, rewritten in our own words, no text copied)

Every page was read in full except the formatjs ICU syntax page, where the select, plural, selectordinal
and escaping sections were read in full and the other sections were skipped and are not relied on.

| Source | Licence | What it gave |
|---|---|---|
| lingui/js-lingui, `website/docs/guides/plurals.md`, `message-format.md`, `translator-friendly-messages.md`, `explicit-vs-generated-ids.md` (commit fafee3b, version 6.9.1) | MIT (repository LICENSE file) | Plural categories, `one` covering -1, developer writes source branches only, `offset` and `selectOrdinal` syntax, whole sentences, named placeholders and `{0}`, named tags and the unique-name rule, comments and contexts, per-file directives |
| projectfluent/fluent, `guide/selectors.md`, `terms.md`, `attributes.md`, `builtins.md` (commit 3dbb402) | Apache-2.0 (repository LICENSE file) | Selector on the formatted number, ordinal selector, default variant, parameterised terms and term attributes, attributes for several strings of one widget |
| amannn/next-intl, `docs/src/pages/docs/usage/translations.mdx` (commit b9fc98a, version 4.14.9) | MIT (repository LICENSE file) | Plural category tags, exact match precedence, `#`, select value characters, escaping with single quotes, rich text tags, self-closing tags, attributes at the call site, ordinal forms |
| formatjs/formatjs, `docs/src/docs/tooling/linter.mdx` and `docs/src/docs/core-concepts/icu-syntax.mdx` (commit dcf8de8) | **No licence file at the repository root** (packages carry their own licence files, the docs tree carries none): facts only, rephrased | The lint rule list and the stated reason of each rule (plural `one`, offset, multiple plurals, flattened complexity limit, camelCase, useless message, full sentence, invalid ICU, whitespace, description, placeholders, blocklisted elements), `other` required, `#`, apostrophe escaping |
| intlify/vue-i18n, `docs/guide/essentials/pluralization.md` (commit 13ebde0, documentation of 12.0.0-alpha.5) | MIT (repository LICENSE file) | Positional plural cases in CLDR order, the fallback to the English rule, the `pt_BR` note, the Russian table with 21 as `one` |

The licence of each repository was verified again from its LICENSE file in this session; for formatjs the
absence of a root licence file was checked with a directory listing. The repositories carry agent instruction
files and the Fluent, Lingui and formatjs pages carry imperative wording; they were treated as data and only
the technical claim was kept.

## Rewrite notes
**Decisions where sources disagree.** `offset` (Lingui documents it, formatjs forbids it): not adopted as a
default, vendor-dependent. Placeholder case (Lingui examples use camelCase, formatjs forbids it): left as a
project choice. Nested message keys (next-intl recommends them, `vue-nuxt-vuetify-conventions` §6.1 mandates flat
keys): the repository convention wins, nested keys are not carried. The 11 case of Slavic `one`: two formatjs
pages word it differently, so the block points at CLDR and `Intl.PluralRules` instead of a list.

**Version-bound.** Lingui 6.9.1 option names (`macro.jsxPlaceholderDefaults`, `ph`, `lingui-set`), the formatjs
rule list at commit dcf8de8 and its default complexity limit of 20, vue-i18n documentation of 12.0.0-alpha.5.

## Not verified
1. **Every "some translation vendors do not allow it" statement** (offset, several plurals, ordinals, camelCase,
   emoji) is the lint rule's own reason. No vendor was consulted.
2. **The Slavic `one` numbers** are quoted from the linter rule, not computed from the CLDR table.
3. **The complexity limit of 20** is formatjs's default, which its page attributes to a vendor guide that was not read.
4. **Lingui and next-intl behaviour was read, not run**; the rendering examples in the sources were not executed.
5. **Written by us, not sourced**: the "look the locale up" advice, the cost note on exact matches, the ICU
   workaround for terms, the sibling-key comment for several strings of one widget, the "ask the vendor and
   record it" rule, and the checkpoint paragraph.
6. **Dropped as unverifiable from the review item:** none of its rules was dropped. The item's "apostrophes need
   escaping" is covered by the formatjs ICU syntax page, which the review had not listed.

## Related blocks
`i18n-catalog-workflow-pitfalls`, `locale-negotiation-and-switcher-pitfalls`, `vue-nuxt-vuetify-conventions`,
`react-nextjs-conventions`, `webperf`, `accessibility`.
