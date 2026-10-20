# csv-xlsx-import-export-pitfalls §3 — Exports

## 3.1 Size and time
1. **Stream rows; never build the whole file in memory.** Symptom: memory errors or a timeout on a large
   export, fine in testing. Fix: read in keyset-paged or cursor-based chunks and write each to the output as it
   comes. Check: export ten times the production row count in a test and watch memory.
2. **Offset paging is slow and unstable on big tables.** Rows shift between pages when data changes, and deep
   offsets cost more each time. Use a stable order and a keyset ("after this id"), and know that a live table can
   still change during the export.
3. **Long exports run in a worker and produce a file you download**, not a response held open. The request
   returns an export identifier; the person gets a notification and a link. Symptom of the synchronous design:
   proxy timeouts at an unpredictable row count.
4. **Consistent snapshot or declared inconsistency.** A long export can mix states. Either read in one
   consistent transaction snapshot where the database allows it, or stamp the file with its start time and say
   rows may reflect changes during the run.
5. **Cap and warn on size.** XLSX has hard limits on rows and columns per sheet (re-read the current limits for
   your library and program); beyond them, split into sheets or offer CSV. Say so before generating.
6. **Compress and expire the file.** Large files are zipped; the download link expires and is bound to the
   requester (§3.4).
7. **Do not export what the list does not show without saying so.** Exporting "the current filter" must match
   what the screen counts; show "Exporting 12,408 rows" before starting, from the same query.

## 3.2 Content that goes wrong in spreadsheet programs
1. **Formula injection.** A cell whose text starts with an equals sign, plus, minus, at sign (and, in some
   programs, tab or carriage return) can be executed as a formula or link when the file is opened. Symptom: a
   user-supplied name that becomes a command or a data-leaking link in a colleague's spreadsheet. Fix: on export
   of user-controlled text, prefix such cells with a single quote or tab, or write them as typed text cells in
   XLSX; keep the original in the database. Apply it to every free-text column, not just the ones that look
   risky. The guidance is documented by OWASP and by spreadsheet vendors; re-read before relying, as program
   behaviour and mitigations change.
2. **Do not neutralise numbers that are numbers.** A negative amount starts with a minus sign. Apply the guard
   to text columns only, by column type, so figures stay numeric.
3. **Identifiers must stay text.** Leading zeros and long digit strings are changed by the program on open.
   In XLSX write them as text cells; in CSV the program decides on open, so offer XLSX where the file is
   for people, and document the import-dialog route otherwise.
4. **Encoding for the program that opens it.** Some spreadsheet programs only read UTF-8 CSV correctly when a
   byte-order mark is present; others handle it badly. Choose by your audience, document it, and test by opening
   the file in each program you support. For machine consumers prefer UTF-8 without a mark, declared.
5. **Delimiter and decimal separator.** A file with decimal points opens in a decimal-comma locale as text or
   as wrong numbers. For people, offer a locale option or XLSX with real numeric cells; for machines, a fixed,
   documented format.
6. **Dates and times as ISO text or real date cells with a stated time zone.** Never as display strings in a
   locale, never as local time with no zone label.
7. **Line breaks inside cells** are legal when quoted but confuse naive consumers and some tools; keep or
   replace deliberately, and say which.
8. **Null, empty and zero are different.** Pick a representation and document it (empty cell for unknown, zero
   for zero).

## 3.3 What an export says about itself
1. **Stable, documented column names and order**, in a machine-friendly header row, with a human label option.
   Renaming a column silently breaks every consumer's script.
2. **Include an export version and the generation time**, in the file name and, for XLSX, on a metadata sheet.
   For CSV keep the data table clean and put metadata in the file name, not in lines above the header.
3. **File names carry no personal data** and no characters that a file system rejects.
4. **Round-trip where it makes sense.** If an export is meant to be edited and re-imported, its columns, types
   and identity key (`§2.3`) must match the import template, with the internal identifier included.

## 3.4 Access and audit
1. **Row and column permissions apply to exports exactly as to screens**, and are applied in the query, not
   by filtering afterwards. Symptom: a hidden salary column is present in the CSV. See
   `skills/field-and-row-permission-ui-api-pitfalls`.
2. **An export is a bulk read: give it its own permission** and its own limits per person and per period. A
   person who can see rows one at a time should not automatically pull the full table.
3. **Log each export:** who, when, filter, row count, columns, and the file's expiry. Bulk reads are the
   pattern of data leaving, and the log is what answers "who took this".
4. **The download link is a credential.** Make it expire, bind it to the requester's session or require
   sign-in at download, and do not put it in a URL that gets indexed or forwarded. Delete the file after expiry.
5. **Personal data minimisation.** Offer only the columns the purpose needs, and mark in the interface that the
   file contains personal data (rules in `business/data-protection`).
