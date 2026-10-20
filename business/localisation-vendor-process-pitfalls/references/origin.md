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
1. **Only the scoring section was checked**; brief, kit, glossary, memory hygiene and change handling are one author's
   practice. Searched: MQM Council pages; no permissive source for vendor briefs or translation memory hygiene found
   (translation memory exchange standards were not opened).
2. **The framework chosen** is the parties' decision; MQM is one catalogue, and ISO 5060 is mentioned on its pages but was
   not read.
3. **Contract points** (ownership of memory, reuse pricing, data handling) are listed as questions to settle, not
   as legal facts.
4. **Never run by us** on a real job.
5. Re-read before relying; add an open-licence source when one is found.

## Own guidance (not sourced)
Brief and context kit (§1.1, §1.2), source freeze (§1.3), glossary and do-not-translate list (§2.1), memory hygiene
(§2.2), reviewer role, sampling and reviewer calibration (§3.1, §3.2.4, §3.2.5), feedback loop (§3.3) and change
handling (§3.4).

## Related blocks
`skills/i18n-message-format-pitfalls`, `skills/i18n-catalog-workflow-pitfalls`, `skills/locale-value-formatting-pitfalls`,
`skills/rtl-and-bidi-layout-pitfalls`, `business/vendor-management`, `skills/vendor-claims-and-scoring-pitfalls`,
`business/data-protection`, `business/ux-writing`, `skills/source-freshness`.
