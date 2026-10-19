---
name: i18n-catalog-workflow-pitfalls
description: "Use when the translation catalog workflow is set up or reviewed in any framework: static extraction (why a message in a variable or a built key is missed, marking a dynamic key), a CI health check for missing and unused keys and inconsistent variables, normalisation churn, lint for descriptions and literal strings, generated versus explicit message IDs and what changes an ID, loading only the active locale, BCP 47 fallback chains, pseudo-localisation, and translator-side quality checks, length limits and glossaries."
---

# i18n-catalog-workflow-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for what happens between a message written in code and a translated
message shown on screen. The three sections share one premise: **a catalog is a build artifact with its own
failure modes, and most of them are silent until a user reads the wrong language**. The Vue and Nuxt rules for a
missing key (loud in development) and lazy-loaded locales are in `vue-nuxt-vuetify-conventions` §6.12 and
`vue-nuxt-vuetify-conventions` §6.16 and are linked, not restated. The message text itself is in
`i18n-message-format-pitfalls`; locale choice and the language switcher are in
`locale-negotiation-and-switcher-pitfalls`.

## When
- Setting up extraction, a translation vendor or a CI check for a project that has, or will have, a second language.
- A key shows up untranslated in production, a dead key sits in the catalog, or a catalog diff is far larger
  than the change.
- Choosing between generated and explicit message IDs, or a source sentence is edited and the translation vanishes.
- A locale falls back to the wrong language, or every locale ships in the main bundle.
- A layout breaks on long text and nobody saw it before translation.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Extraction and health: static extraction, dynamic keys, the CI health check, normalisation, lint | a key is missed, unused or inconsistent, or a check is added | [`01-extraction-and-health.md`](./references/01-extraction-and-health.md) |
| 2 | IDs, fallback and loading: generated versus explicit IDs, what changes an ID, active-locale chunk, fallback chains | an ID scheme is chosen, a source text is edited, a locale falls back oddly | [`02-ids-fallback-and-loading.md`](./references/02-ids-fallback-and-loading.md) |
| 3 | Pseudo-locale and translator QA: pseudo-localisation, blocking and bypassable checks, length limits, glossary | before translation starts, or when a vendor tool is chosen | [`03-pseudolocale-and-translator-qa.md`](./references/03-pseudolocale-and-translator-qa.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a key was added in code and the CI check was seen to fail for
it, a dynamic key was marked and then seen as used (§1), a source sentence was edited and the effect on the ID
and on the translation was read from the catalog diff (§2), and the application was started in the pseudo-locale
and the strings that stayed in plain source text were listed (§3). A configuration that was only read is not verified.

## Guardrails
- Never put a message in a variable or build a key by interpolation and expect extraction to find it (§1.1).
- Never rely on runtime to find a missing key: a CI check lists missing, unused and inconsistent keys (§1.2).
- Never commit a normalisation run mixed with a feature change (§1.3).
- Never edit a source text or add a context without reading the effect on the ID first (§2.1).
- Never assume a locale tag with an underscore falls back to its language (§2.3).
- Never start translation before the pseudo-locale has been looked at (§3.1).
- This block states the behaviour of the tools named in [`references/origin.md`](./references/origin.md) as of
  the repositories read on the date given there. Option names are version-bound. Nothing was run while writing it.

## Origin
Rewritten from the Lingui guides on extraction, pseudo-localisation, dynamic catalogs and IDs (MIT), the
i18n-tasks README (MIT), the vue-i18n fallback guide (MIT), Mozilla Pontoon's translation documentation
(BSD-style) and the formatjs lint rules (facts only), read 2026-10-15. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
