# csv-xlsx-import-export-pitfalls §2 — Preview, validation and idempotency

## 2.1 Preview and dry run
1. **Two-phase import: parse and validate into a staging area, then commit.** Symptom: a validation error in row
   9,000 after 8,999 rows were written. Fix: stage rows (a staging table or a stored result set) with a status
   per row, show the summary, then commit on an explicit action.
2. **The preview shows what will happen, not just what was read.** Counts of rows to create, update, skip and
   reject; the first rows as they will be stored (after trimming and type conversion); detected encoding,
   delimiter and column mapping. A raw echo of the file hides the conversions that cause the surprises.
3. **The dry run runs the same code as the real run** with writes turned off, or writes inside a transaction
   that is rolled back. A separate "validation" implementation drifts from the real one.
4. **The commit applies what was previewed.** Symptom: data changed between preview and commit and the numbers
   no longer match. Fix: commit from the staged rows, re-check the preconditions that can change (existence,
   version, permissions), and report rows that no longer apply.
5. **Staging data expires and is access-controlled.** It holds the same sensitive values as the file; delete
   it after the retention you state.

## 2.2 Row-level errors
1. **Each error carries row number, column, the offending value and a reason in plain language.** Symptom:
   "Invalid data". Fix: errors are data (a list), not a string.
2. **Count rows as the person sees them** (the W3C tabular data model notes that skipping rows changes the source row numbers, so keep the source line, not the post-header index, as the identity of a row). Row 1 is the header in their spreadsheet; an off-by-one error
   sends them to the wrong row. Number rows by spreadsheet line, and say so.
3. **Report all errors up to a cap, not the first one.** Fixing one error per upload is the slowest loop. Cap
   at a number you state ("showing the first 200 of 1,340") and offer the full list as a file.
4. **Return the error report as a downloadable file in the input's shape**: the original columns plus an error
   column, containing only the rejected rows. The person fixes and re-uploads that file. It must be importable
   as is, with the error column ignored.
5. **Distinguish blocking errors from warnings.** A missing optional value, a value that will be normalised, a
   probable duplicate: warnings go in the preview, the person may proceed.
6. **Decide the policy and show it: all-or-nothing, or valid rows now.** All-or-nothing is simpler to reason
   about for small files and for linked records; partial import suits large files if the report and the
   re-upload loop (point 4) work. Symptom of an unstated policy: half the file imported and nobody knows which.
7. **Validate relations in the file against the database in one pass** (existing parents, codes in a reference
   list), loading references once rather than querying per row; both for speed and to report all missing
   references together.
8. **Do not leak other tenants' data through errors.** "Customer 123 already exists" for a record the person
   cannot see is a disclosure; say "identifier already used" or scope the check.

## 2.3 Identity, idempotency and re-import
1. **Name the identity key of an imported record**: an external reference supplied in the file, or a
   natural key. Without one, every re-import duplicates. Symptom: doubled customers after a retry. Fix: a unique
   constraint on the key in the database, not only a check in code.
2. **Choose the re-import behaviour per import type:** create only, update existing, upsert, or skip existing.
   State it on the screen. "Upsert" needs a rule for blanks: an empty cell either leaves the field alone or
   clears it, and the person must know which.
3. **The same file twice must give the same state.** Test by importing it twice and diffing. Store a checksum of
   each processed file per scope and warn on a repeat (a warning, not a refusal: a corrected file differs
   anyway).
4. **Upserts are race-prone.** Two workers with overlapping rows insert the same key. Use the database's
   atomic upsert on the unique key, or serialise per key, and handle the unique-violation as "update".
5. **Child rows and order.** Parent before child, or resolve references in a second pass. Duplicated keys inside
   the same file are an error, reported on both rows.
6. **Side effects of import are the dangerous part:** emails, webhooks, audit entries, derived counters,
   search indexing. Decide whether imported records fire them. A first import that mails ten thousand people is
   the classic incident. Default to off or to a batch that is reviewed, and log what was suppressed.
7. **Record the import as an object:** who, when, file checksum, mode, counts, status, and the list of record ids
   created or changed. It is the audit trail, and the basis for an undo where you offer one.

## 2.4 Background processing
1. **Anything beyond a few seconds runs in a worker**, started from the commit action; the request returns an
   import identifier at once. Symptom: timeouts at the proxy, duplicated runs from browser retries.
2. **Progress and status are read from the import object**, not from the worker's memory: queued, validating,
   importing, done, done with errors, failed, cancelled; counts so far. A progress bar that lies is worse than a
   spinner.
3. **Workers die.** The import must be resumable or restartable: process in batches, record the last committed
   batch, and make each batch idempotent (§2.3). A restart then continues rather than duplicates. Queue delivery
   guarantees are in `skills/background-jobs-conventions`.
4. **Batch size trades speed against lock time and memory.** Measure with your data; do not copy a number.
   Commit per batch so a failure loses one batch, not the file.
5. **Concurrent imports into the same scope** can deadlock or race. Allow one running import per scope and type,
   or lock per key, and say "an import is already running" with a link.
6. **Notify on completion**, with the result and the error report link; the person left the page long ago.
7. **Cancelling** stops after the current batch and keeps what was committed; say so. Offer undo only if the
   import object lists exactly what it changed.
