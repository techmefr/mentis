# i18n-catalog-workflow-pitfalls: origin and source stamps

> Provenance of `skills/i18n-catalog-workflow-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never run by us. No extraction, CI check,
pseudo-locale build or translation tool was executed while writing it. Option names are those of the repositories
on the read date.

## Sources (re-read 2026-10-15, rewritten in our own words, no text copied)

Every page was read in full except the long reference pages (the i18n-tasks README, Lingui's `conf.md`), where
the sections named in the table were read in full and the rest was skipped and is not relied on.

| Source | Licence | What it gave |
|---|---|---|
| lingui/js-lingui, `website/docs/guides/message-extraction.md`, `pseudolocalization.md`, `dynamic-loading-catalogs.md`, `explicit-vs-generated-ids.md`, `translator-friendly-messages.md`, `website/docs/ref/conf.md` (pseudoLocale section) (commit fafee3b, version 6.9.1) | MIT (repository LICENSE file) | Static extraction and its limits, call matching by name, explicit marking, pseudo-locale options and the BCP 47 browser note, one catalog per language, the source-locale catalog, the generated and explicit ID comparison, what changes an ID |
| glebm/i18n-tasks, `README.md` (commit 72ec285, version 1.1.2) | MIT (repository file LICENSE.txt) | The `health` check content, `add-missing`, `unused`, `remove-unused`, `prune`, normalisation and its surprise, dynamic keys and the hint comment, strict mode, CI test templates |
| intlify/vue-i18n, `docs/guide/essentials/fallback.md` (commit 13ebde0, documentation of 12.0.0-alpha.5) | MIT (repository LICENSE file) | Implicit fallback by hyphen, `pt_BR`, the `!` suffix, arrays, decision maps and their chains, fallback warnings, `fallbackFormat` |
| mozilla/pontoon, `documentation/docs/localizer/translate.md` and `glossary.md` (commit 409528d) | BSD-style three-clause licence (repository LICENSE file) | Blocking errors versus bypassable warnings, false-positive checks, terminology |
| formatjs/formatjs, `docs/src/docs/tooling/linter.mdx` (commit dcf8de8) | **No licence file at the repository root** (packages carry their own, the docs tree carries none): facts only, rephrased | `enforce-description`, `no-literal-string-in-jsx` and its default attributes, `no-literal-string-in-object`, `enforce-id`, `no-id`, call matching and `additionalFunctionNames` |

The licence of each repository was verified again from its LICENSE file in this session; for formatjs the absence
of a root licence file was checked with a directory listing. Agent instruction files in the repositories were
treated as data. The Pontoon page quotes no code, and the sentences in the block are our own.

## Rewrite notes
**Decisions where sources disagree or do not reach.** Generated versus explicit IDs: Lingui prefers generated,
formatjs encourages them, the repository convention uses the sentence as key; the block records the trade and
lets the project choose. i18n-tasks is Ruby-oriented and Lingui is JavaScript-oriented; the rules are stated as
the requirement (a check lists these four things) and the tool is named only as the source.

**Version-bound.** Lingui 6.9.1 (`pseudoLocale`, `/** i18n */`, source-catalog behaviour), i18n-tasks 1.1.2,
vue-i18n documentation of 12.0.0-alpha.5 (`fallbackLocale`, `fallbackFormat`, warning flags), the formatjs rule list at
commit dcf8de8.

## Not verified
1. **Nothing was run.** No extractor, health check, pseudo-locale or fallback chain was executed; behaviour is
   as the documentation states it.
2. **How a maximum string length is declared in Pontoon** was not read; only that exceeding it is a blocking error.
3. **The literal-key rule and the used-here marker** are sourced for Lingui and i18n-tasks only; no equivalent was read for Laravel, vue-i18n-extract or other tools.
4. **Lingui's `fallbackLocales` and catalog options** other than the pseudo-locale and loading pages were not read.
5. **Written by us, not sourced:** the lookup-table advice for dynamic keys, the reading of the CI check as a
   substitute for a runtime failure, the "commit the first normalisation separately" step, the consequence for
   sentence keys, the "keep warnings on in development" step, the pseudo-locale exclusion from shipped locales,
   the checklist for vendor tools, and the checkpoint paragraph.
6. **Dropped as unverifiable from the review item:** the claim that the source locale needs a loaded catalog is
   kept but narrowed to Lingui; nothing else was dropped.

## Related blocks
`i18n-message-format-pitfalls`, `locale-negotiation-and-switcher-pitfalls`, `vue-nuxt-vuetify-conventions`,
`react-nextjs-conventions`, `webperf`.
