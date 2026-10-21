# localisation-vendor-process-pitfalls: origin and source stamps

> Provenance of `business/localisation-vendor-process-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from general localisation-management practice, never run on a real
translation job by us. The block structures a check; it certifies nothing, and the content owner with a native
reviewer decides acceptance (`business/README.md`).

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| MQM Council website pages: home, full typology, error-types typology, scoring models, concrete example with formulas | CC BY 4.0 (footer line read on each page; a separate licence page returned not found) | Seven top-level categories, catalogue use, optional weights, four severity levels and how severity is judged, critical error fails, per-project thresholds per content type, source word count normalisation, neutral severity (§3.2.1, §3.2.2, §3.2.3, §3.2.5, §3.2.6) |

Credit: Multidimensional Quality Metrics (MQM), MQM Council, CC BY 4.0. Facts rewritten; no figure, multiplier or example reused.

Second pass, 2026-10-20:

| Source | Licence | What it gave |
|---|---|---|
| mozilla-l10n/documentation, commit 4fdc163 (4fdc1631ef354e2ffc8c0757477bed028468c9ac), `src/localization/dev_best_practices.md`, `making_string_changes.md`, `src/products/iOS_products/screenshots.md` | CC BY 4.0 (LICENSE file read, head). Credit: Mozilla localization documentation, CC BY 4.0, facts rewritten | Notes for ambiguous strings and variables, screenshots and design links for untested screens, whole messages and placeholders, no reuse of one string in two contexts, plurals and inflection, at least 30 percent room for expansion, no temporary strings, new identifier when meaning changes (§1.2, §1.3, §3.4) |
| Google developer documentation style guide, "Write for a global audience" (developers.google.com/style/translation), read raw | Creative Commons Attribution 4.0 (page footer read), code samples Apache 2.0. Credit: Google Developers, CC BY 4.0 | Source text for translation: short unambiguous sentences, consistent terminology, no idioms, humour or seasons. Nothing copied; used only to confirm that a clear source is part of the brief |
| Crowdin documentation: Glossary and Translation Memory pages (support.crowdin.com), read raw | Vendor documentation under its site terms, no open licence; facts only, own words | Glossary concept and term fields (definition, translatable, part of speech, status, gender), TM units with dates and contributor, separate memories per project, match priority and penalties, TMX download and upload (§2.1, §2.2) |
| OASIS XLIFF 2.1 (docs.oasis-open.org/xliff/xliff-core/v2.1), fetched | OASIS standard; licence text not read | Existence of the exchange format only; no detail relied on |

## Verified
The MQM points above confirm §3.2 headings, severity use, per-type thresholds, neutral preferences. The category list in
the previous version (accuracy, fluency, terminology, style, locale conventions, omission) was corrected: omission is an
accuracy subtype and two top-level categories were missing.

## Left out on purpose
Severity multipliers and any pass threshold (the MQM pages give examples; they are project choices). Industry standards for translation services and
their terms. Price models and per-word rates. Tool and platform recommendations. Machine-translation engine
comparisons. The code-side catalogue workflow (`skills/i18n-catalog-workflow-pitfalls`). Any source with no open
licence: not opened.

## Not verified
1. **Checked beyond scoring in the second pass**: the brief's context and note rules, whole messages and expansion room
   (Mozilla), glossary fields and memory handling (Crowdin docs as one tool's example), source freeze for temporary strings
   (Mozilla). **Still unsourced**: that the review should be done by a second native linguist who did not translate it
   (§3.1), calibration of reviewers (§3.2.5), the feedback loop and praise (§3.3), vendor availability for the next round, the
   advice to plan for the slowest language, and that a new language is a new project. Searched: MQM Council, Mozilla l10n docs,
   Google style guide, Crowdin docs, OASIS XLIFF; no open source on vendor review practice found. TMX and XLIFF
   specifications were not read.
2. **The framework chosen** is the parties' decision; MQM is one catalogue, and ISO 5060 is mentioned on its pages but was
   not read.
3. **Contract points** (ownership of memory, reuse pricing, data handling) are listed as questions to settle, not
   as legal facts.
4. **Never run by us** on a real job.
5. Re-read before relying; add an open-licence source when one is found.

## Own guidance (not sourced)
Market and tone in the brief (§1.1), the source freeze dates and ownership questions (§1.3), glossary ownership and
native review of the first version (§2.1.5, §2.1.6), memory hygiene beyond the fields named above (§2.2), reviewer role,
sampling and reviewer calibration (§3.1, §3.2.4, §3.2.5), feedback loop (§3.3) and release planning (§3.4). Context notes,
screenshots, whole messages, expansion room, glossary fields and the new-identifier rule moved from own guidance to
sourced in the 2026-10-20 pass.

## Related blocks
`skills/i18n-message-format-pitfalls`, `skills/i18n-catalog-workflow-pitfalls`, `skills/locale-value-formatting-pitfalls`,
`skills/rtl-and-bidi-layout-pitfalls`, `business/vendor-management`, `skills/vendor-claims-and-scoring-pitfalls`,
`business/data-protection`, `business/ux-writing`, `skills/source-freshness`.
