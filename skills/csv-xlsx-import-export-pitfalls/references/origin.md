# csv-xlsx-import-export-pitfalls: origin and source stamps

> Provenance of `skills/csv-xlsx-import-export-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from craft knowledge; no file was parsed, no export run and no library
exercised while writing it.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| RFC 4180, Common Format and MIME Type for CSV Files, <https://www.rfc-editor.org/rfc/rfc4180>, read 2026-10-20 | IETF Trust document, Informational; facts only, restated in own words | Record separator, optional final break, quoting rules, header and charset as optional media-type parameters, field-count expectation |
| Excel specifications and limits, Microsoft Support, <https://support.microsoft.com/en-us/office/excel-specifications-and-limits-1672b34d-7043-467e-8e27-269d656771c3>, read 2026-10-20 (page carries no date) | Vendor documentation; facts only | Rows, columns and cell-length limits of a worksheet |
| Import or export text (.txt or .csv) files, Microsoft Support, <https://support.microsoft.com/en-us/office/import-or-export-text-txt-or-csv-files-5250ac4c-663c-47ce-937b-339e391393ba>, read 2026-10-20 | Vendor documentation; facts only | List separator and decimal separator taken from regional settings, default column formats on open, text column to keep leading zeros |
| Formula injection sources (OWASP page, vendor pages) | n/a | No permissive source found, searched: OWASP and vendor documentation known to the author; OWASP content is CC BY-SA and was not opened, vendor pages not read. |

## Rewrite notes
Every rule is own guidance from general practice in business import and export features. No text, example or
number was copied. No batch size, limit or timing is given.

## Removed
- Batch sizes, row limits and file size limits: no verified source, so none given.
- Library names and calls: not exercised.

## Not verified
1. **Formula injection** guidance (which leading characters, which mitigation works in which program) was
   recalled from vendor and security documentation and not re-read; still unverified.
2. **Verified 2026-10-20:** quoting, line endings, header and charset parameters (RFC 4180); Excel row, column and cell limits. Also verified 2026-10-20: delimiter follows regional separators, leading zeros lost without a text column. **Still unverified spreadsheet program behaviour** (byte-order mark handling, other programs' limits, date epochs) differs by program and version; test with the
   programs your users have.
3. **Archive and XML hardening** points (zip bombs, entity expansion) are standard practice, not checked against a
   library's current defaults.
4. **Own guidance, not sourced:** the two-phase import, error report shape, idempotency and re-import rules,
   background processing, streaming and export access rules.

## Related blocks
`spreadsheet-data-cleaning-pitfalls`, `international-input-pitfalls`, `locale-value-formatting-pitfalls`,
`laravel-idempotent-jobs`, `laravel-idempotent-data-commands`, `background-jobs-conventions`,
`queue-worker-runtime-pitfalls`, `field-and-row-permission-ui-api-pitfalls`, `data-protection`.
