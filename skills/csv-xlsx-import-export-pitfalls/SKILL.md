---
name: csv-xlsx-import-export-pitfalls
description: "Use when a business application imports or exports tabular files (CSV, XLSX) or such a feature is reviewed: upload limits and parsing, encoding and delimiter detection, header mapping, a preview and dry run before anything is written, row-level errors the person can fix and re-upload, idempotent re-imports and partial failure, background processing with progress, large exports that stream instead of loading everything, spreadsheet formula injection on export, and what an export must say about itself. Framework-independent."
---

# csv-xlsx-import-export-pitfalls

A defensive block for the file in and file out of a business application. Premise: **a file is untrusted,
ambiguous input that someone will upload again after fixing it, and an export is a copy that leaves your access
controls; design both for the second attempt and for the wrong reader**. Cleaning a spreadsheet by hand is in
`business/spreadsheet-data-cleaning-pitfalls`; locale, names and dates as input are in
`skills/international-input-pitfalls` and `skills/locale-value-formatting-pitfalls`; idempotent jobs and data
commands are in `skills/laravel-idempotent-jobs` and `skills/laravel-idempotent-data-commands`, queue behaviour in
`skills/background-jobs-conventions` and `skills/queue-worker-runtime-pitfalls`; which rows and columns a person
may export is `skills/field-and-row-permission-ui-api-pitfalls`; personal data in files is `business/data-protection`.

## When
- An import screen is designed or a bulk-upload bug is reported (garbled accents, shifted columns, half-imported
  files, duplicates after a retry, a timeout on a big file).
- An export is built or reviewed (timeouts, memory errors, wrong characters in the spreadsheet program, numbers
  and dates mangled, a cell executing a formula).
- A file import becomes a recurring integration between systems.

## Steps

**Read only the section the task meets.** §2 is the entry point for any "import did something wrong" report.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Upload and parsing: limits, format sniffing, encoding, delimiter, quoting, headers and column mapping, XLSX specifics | a file is accepted and read | [`01-upload-and-parsing.md`](./references/01-upload-and-parsing.md) |
| 2 | Preview, dry run, row-level errors, idempotency, partial failure, background jobs and progress | rows are validated and written | [`02-preview-validation-and-idempotency.md`](./references/02-preview-validation-and-idempotency.md) |
| 3 | Exports: streaming, background generation, formula injection, encoding for spreadsheet programs, typed values, self-description, access | an export is built or is slow or leaks | [`03-exports.md`](./references/03-exports.md) |

## Output / checkpoint
No pipeline checkpoint. A reviewed feature owes: the accepted formats, limits and encoding rules (§1), a preview
and dry-run path that writes nothing (§2), an error report downloadable in the same shape as the input with a
reason per row (§2), the identity key and re-import behaviour (§2), the background and progress design (§2), and an
export spec naming columns, types, encoding, row scope and the injection guard (§3).

## Guardrails
- Parse in a streaming reader with size and row limits, in a worker for anything long. Never read a whole upload
  into memory in the request (§1).
- Show a preview with the detected encoding, delimiter and column mapping and let the person correct them. Never
  commit a guess (§1, §2).
- Validate every row before writing any, or write in recorded batches that can be rolled forward. Never leave a
  file half-imported with no record of where it stopped (§2).
- Return row-level errors with row number, column and reason, in a file that can be fixed and re-uploaded. Never
  answer "import failed" alone (§2).
- Define the identity key and make a re-import update or skip, not duplicate. Never rely on the person not
  clicking twice (§2).
- Neutralise cells that start with a formula character, and stream large exports from a worker. Never write user
  text into a spreadsheet cell as is, nor build a big export in the request (§3).
- Apply the same row and column permissions to exports as to the screen. Never let an export reach what the
  list cannot (§3).
- CSV format points are checked against RFC 4180 and sheet limits against the spreadsheet vendor's limits page; the rest is craft knowledge. Status and unverified points are in
  [`references/origin.md`](./references/origin.md). No file was parsed and no program was run.

## Origin
Written from general practice in business import and export features and from the CSV format description (RFC 4180) and one vendor limits page, both read 2026-10-20, facts only and credited, plus on a third pass the W3C tabular data model and the Papa Parse documentation (MIT); no text was copied. 🟡: never run by us. Details in
[`references/origin.md`](./references/origin.md).
