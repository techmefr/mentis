# spreadsheet-data-cleaning-pitfalls: origin and source stamps

> Provenance of `business/spreadsheet-data-cleaning-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from general spreadsheet and data-cleaning practice, never run on a real
file by us, with no external source. The block structures a check; it certifies nothing, and the person who owns
the data decides what counts as an error (`business/README.md`).

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None. The gap review (2026-10-20) found no licence-verified source for tabular hygiene. The two MIT repositories named in it were not used: nothing found there was about spreadsheet cleaning. | n/a | Nothing; the method is written from own practice |

## Left out on purpose
Every program-specific claim stated as fact: the number of significant digits a given program keeps, the epoch of
date serials, which short codes a given version turns into dates, default separator and encoding behaviour,
function names and menu paths. Each is written as "check on the file in front of you". Any numeric threshold.
Statistical cleaning (outlier rules, imputation): `skills/analysis-validation-pitfalls`. Tool recommendations and
scripting recipes. Any source with no open licence: not opened.

## Not verified
1. **No source was read**; the block is one author's practice and may miss pitfalls specific to a program or
   locale.
2. **Program behaviours** (digit limits, date epochs, import defaults, save-as-CSV behaviour) differ by product and
   version and were not checked against documentation for this block.
3. **Never run by us** on a real file.
4. **A block with no outside check**: re-read before relying, and add a documentation or open-licence source when
   one is found.

## Own guidance (not sourced)
All of it: the identifier-as-text rule (§1.1), the type audit (§1.4), the date and number audits (§2), key testing
and survivor rules (§3), row-count and unmatched checks after a join (§3.4), formula drift checks (§4.1), the
change log and the reconciliation line (§4.3, §4.4).

## Related blocks
`skills/analysis-validation-pitfalls`, `skills/saas-metric-definition-pitfalls`, `business/data-analytics`,
`skills/data-contract-quality-rules-pitfalls`, `business/data-protection`, `skills/source-freshness`.
