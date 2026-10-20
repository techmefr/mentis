# spreadsheet-data-cleaning-pitfalls: origin and source stamps

> Provenance of `business/spreadsheet-data-cleaning-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from general spreadsheet and data-cleaning practice, never run on a real
file by us, with no external source. The block structures a check; it certifies nothing, and the person who owns
the data decides what counts as an error (`business/README.md`).

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| Microsoft Support pages: Excel specifications and limits, stop automatically changing numbers to dates, date systems in Excel | Vendor documentation, no licence granted on the text; facts only, rewritten | Fifteen-digit precision, automatic date conversion with no off switch, text format and apostrophe workaround, scientific notation, 1900 and 1904 date systems and offset, size limits (§1.1.1, §1.1.2, §1.2.5, §2.1.2) |
| Google Docs Editors Help: Sheets size limits | Vendor documentation, facts only | Cell cap per spreadsheet (§1.2.5) |
| RFC 4180 (CSV) | IETF RFC, informational; facts only | Field, quote and line rules, no mandated charset, implementations deviate (§1.2.2) |
| An Excel support page on the two-digit year rule | not obtained (a page returned not found; a search result was not read) | Nothing |

The two MIT repositories named by the gap review were not used: nothing found there was about spreadsheet cleaning.

## Verified
Program facts in the table were checked against vendor pages and each confirms an existing point in kind. The figures differ
by version; they are given as read and the text tells the reader to check the current page.

## Left out on purpose
Every program-specific claim stated as fact: the number of significant digits a given program keeps, the epoch of
date serials, which short codes a given version turns into dates, default separator and encoding behaviour,
function names and menu paths. Each is written as "check on the file in front of you". Any numeric threshold.
Statistical cleaning (outlier rules, imputation): `skills/analysis-validation-pitfalls`. Tool recommendations and
scripting recipes. Any source with no open licence: not opened.

## Not verified
1. **Only the facts in the table were read**; identifiers beyond the examples, locale and time zone handling, key testing,
   joins, formula drift, provenance and the change log are one author's practice. Searched: vendor support pages and the
   CSV RFC; the two-digit year rule and gene-name conversion were not found.
2. **Program behaviours** were read for two products only; save-as-CSV behaviour, import defaults and locale separators
   were not found in the pages read.
3. **Never run by us** on a real file.
4. **A block with no outside check**: re-read before relying, and add a documentation or open-licence source when
   one is found.

## Own guidance (not sourced)
The type audit (§1.4), the locale, time zone and number audits (§2.1 points 1 and 3 to 5, §2.2 to §2.4), key testing and
survivor rules (§3), row-count and unmatched checks after a join (§3.4), formula drift checks (§4.1), the change log and
the reconciliation line (§4.3, §4.4). Gene-style names read as dates (§1.1.3) is not confirmed by the pages read.

## Related blocks
`skills/analysis-validation-pitfalls`, `skills/saas-metric-definition-pitfalls`, `business/data-analytics`,
`skills/data-contract-quality-rules-pitfalls`, `business/data-protection`, `skills/source-freshness`.
