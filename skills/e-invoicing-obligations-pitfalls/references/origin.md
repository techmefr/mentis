# e-invoicing-obligations-pitfalls: origin and source stamps

> Provenance of `skills/e-invoicing-obligations-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from a legal text and one authority page, never run by us: no company,
platform or invoice was handled. This block is a working method, not tax or legal advice, and it does not
replace the accountant, the tax adviser or the national authority.

## Sources (all read 2026-10-19, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Council Directive (EU) 2025/516 of 11 March 2025, https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32025L0516 : Article 1(2) and (3), Article 5 points (3), (4), (5), (6) to (12), (15) to (19), Articles 6 to 8 | Official text of the European Union, reused with mention of the source | Electronic invoice definition, default electronic invoicing, standard reference, national option to mandate, acceptance, new invoice content, reporting articles 262 to 264, 271a to 271c, dates and derogations |
| Tax administration page, https://www.impots.gouv.fr/professionnel/je-passe-la-facturation-electronique (page showed "published 16/10/2024, modified 01/09/2026") | Public administration website, statement paraphrased | The national-trap example: effective date stated, documents listed, questions listed |

The Directive was read in a real browser (EUR-Lex answers an empty HTTP 202 to curl and to the fetch tool), in the
English version of the original publication, not a consolidated text. Method for retrieving official text:
`business/regulatory-watch` §5.

## Removed
1. **Any national duty, date or threshold other than the single page statement in part 2, point 4.**
2. **The platform and standard details.** Neither EN 16931 nor the French guide, calendar and platform list were
   read; the block only names them.
3. **Article 1 and 2 provisions on other subjects** (platform economy, special schemes, one-stop shop), and
   the amendments of Articles 2 (from 2027) and 3 (from 2028), not read for this block.

## Not verified
1. **Consolidated Directive 2006/112/EC and amending acts** after 2025/516: not checked.
2. **Any national law** other than the one page, and whether any company is in scope or exempt.
3. **EN 16931 and its syntaxes**, Directive 2014/55/EU, Implementing Decision (EU) 2017/1870 beyond the footnotes.
4. **Archiving rules and authenticity technologies** beyond the list wording of Article 233(2).
5. **The French page's FAQ answers, practical guide, calendar, legal documentation and approved platform list.**
6. **Own guidance, flagged in the text:** inventory columns, adviser questions, decision record entry, test list,
   escalation triggers, glossary line.
7. **Cross-references to other blocks:** by name; only `business/regulatory-watch` §5 uses a section number.

## Related blocks
`business/finance-ops`, `business/regulatory-watch`, `business/fintech-compliance`, `skills/source-freshness`.
