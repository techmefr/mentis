# csv-xlsx-import-export-pitfalls §1 — Upload and parsing

## 1.1 Accepting the file
1. **Set limits before parsing: bytes, rows, columns, cell length.** Symptom: a 2 GB upload or a ten-million
   row file takes a worker down. Check: upload a file just over each limit. Fix: refuse early with the limit
   named, at the proxy and in the application.
2. **Decide the type from content, not only the extension or the declared media type.** Symptom: a renamed
   file or a CSV saved as XLSX gets a parse error nobody understands. Fix: sniff the first bytes (an XLSX is a
   zip container, an old XLS is a different binary format), and refuse formats you do not support with a clear
   message.
3. **Store the original upload untouched** with who, when and a checksum, even if you delete it later. It is
   the only way to answer "what did I upload" and to replay a bug.
4. **Treat the file as hostile.** Zip bombs and huge XML in XLSX, macros in older workbook formats, XML entity
   expansion in a spreadsheet's XML parts, path tricks in archive entries. Use a maintained library with entity
   expansion off, limit decompressed size, never run macros, and parse in a worker with limited memory. Scan
   uploads if the rest of the application does.
5. **Authorise the upload as an action**, not only as a page: the person needs the right to import this kind of
   record into this scope (tenant, project). See `skills/field-and-row-permission-ui-api-pitfalls` §3.

## 1.2 Encoding, delimiter, quoting
1. **Do not assume UTF-8.** Symptom: accented letters turn into two odd characters, or into question marks.
   Check: import a file saved by a desktop spreadsheet program in a non-English locale. Fix: detect (byte-order
   mark first, then validate as UTF-8, then fall back to a configured legacy encoding), show the detected
   encoding in the preview and let the person change it.
2. **A byte-order mark at the start becomes part of the first header.** Symptom: the first column is never
   found though its name looks right. Fix: strip a leading mark before reading headers.
3. **The delimiter is a locale artefact.** Spreadsheet programs in locales that use a decimal comma write
   semicolons. Symptom: the whole row lands in one column. Fix: detect among comma, semicolon, tab and pipe by
   consistency of field counts over the first rows, and let the person override.
4. **Quoting follows the common CSV rules** (RFC 4180 §2 items 5 to 7; real files deviate, and the RFC itself notes that some programs do not quote at all): fields with the
   delimiter, quote or line break are quoted, quotes are doubled inside, and an unquoted field holds no quote. Symptom: a note with a line break splits
   into two rows. Fix: use a real parser, never split on newline, and test with embedded newlines and quotes.
5. **Line endings and trailing blank lines vary.** RFC 4180 §2 items 1 and 2 name CRLF as the record separator and make the final line break optional, while §3 admits other endings exist. Ignore fully empty trailing rows, report fully empty rows in
   the middle rather than silently dropping them.
6. **Number and date text follows the file's locale, not yours.** Parsing rules are in
   `skills/locale-value-formatting-pitfalls` and `business/spreadsheet-data-cleaning-pitfalls` §2. For imports:
   require an explicit date format or a documented one, and reject ambiguous values rather than guess a day-month
   order.

7. **Header presence and charset are not in the file.** RFC 4180 §3 carries them as optional media-type parameters (`header`, `charset`); a bare file has neither, and a reader that ignores them must decide for itself. Symptom: a header row imported as data, or a first data row swallowed as header. Fix: ask in the preview whether row 1 is a header, defaulting from the template. Expect rows whose field count differs from the header (the RFC wants equal counts; files break it) and report them as row errors.

## 1.3 Headers and mapping
1. **Match headers by normalised name** (trimmed, case-folded, accents and punctuation folded), with a synonym
   list per column, then offer a mapping screen for what did not match. Symptom: a trailing space in a header
   makes the whole column silently ignored. Fix: never ignore an unmatched column without telling the person.
2. **Reject duplicate headers or require the person to choose.** Two columns named the same make the last win
   in most parsers.
3. **Required columns missing is a file-level error, before any row work.** Say which ones.
4. **Extra columns are listed as ignored in the preview**, not discarded quietly.
5. **A template file helps more than a description.** Offer a downloadable template with the exact headers, one
   example row, and a sheet or section of allowed values for coded fields.
6. **Versioned templates.** When the template changes, accept the previous one for a period or fail with a
   message that names the change. An import that quietly maps by position breaks when someone inserts a column.

## 1.4 Workbook (XLSX) specifics
1. **Which sheet?** Default to the first visible sheet, show the choice in the preview, and let the person
   pick. Hidden sheets are a common source of "wrong data".
2. **Cell values come as stored, not as displayed.** Dates are numbers with a format, identifiers typed as
   numbers lose leading zeros before you ever see them, and a formula cell has a cached result that may be
   stale or absent. Fix: read cached values only, say that formulas are not evaluated, and for identifier columns
   require text format in the template.
3. **Merged cells, multi-row headers and notes above the table** break column mapping. State the expected
   layout in the template; let the person choose the header row in the preview.
4. **The date epoch differs between workbook modes** and the serial number alone does not carry it. Use the
   library's date handling and test with a file from each program you support (re-read the library
   documentation).
5. **Prefer CSV for machine-to-machine files** and XLSX for people. CSV has no types, so pin the contract: encoding,
   delimiter, decimal separator, date format, null representation.
