# csv-xlsx-import-export-pitfalls: origin and source stamps

> Provenance of `skills/csv-xlsx-import-export-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from craft knowledge; no file was parsed, no export run and no library
exercised while writing it.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read. No source with a LICENSE file read and verified as MIT, Apache-2.0 or CC BY was used. | n/a | n/a |
| CSV format description (RFC 4180): facts only, recalled and not re-opened | IETF standard, facts only | Quoting rules, that real files deviate |

## Rewrite notes
Every rule is own guidance from general practice in business import and export features. No text, example or
number was copied. No batch size, limit or timing is given.

## Removed
- Batch sizes, row limits and file size limits: no verified source, so none given.
- Library names and calls: not exercised.

## Not verified
1. **Formula injection** guidance (which leading characters, which mitigation works in which program) was
   recalled from vendor and security documentation and not re-read; check before relying.
2. **Spreadsheet program behaviour** (byte-order mark handling, delimiter by locale, text-cell handling of
   identifiers, row and column limits per sheet, date epochs) differs by program and version; test with the
   programs your users have.
3. **Archive and XML hardening** points (zip bombs, entity expansion) are standard practice, not checked against a
   library's current defaults.
4. **Own guidance, not sourced:** the two-phase import, error report shape, idempotency and re-import rules,
   background processing, streaming and export access rules.

## Related blocks
`spreadsheet-data-cleaning-pitfalls`, `international-input-pitfalls`, `locale-value-formatting-pitfalls`,
`laravel-idempotent-jobs`, `laravel-idempotent-data-commands`, `background-jobs-conventions`,
`queue-worker-runtime-pitfalls`, `field-and-row-permission-ui-api-pitfalls`, `data-protection`.
