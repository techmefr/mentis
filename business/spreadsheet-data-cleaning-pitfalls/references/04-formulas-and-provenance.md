# spreadsheet-data-cleaning-pitfalls §4 — Formulas and provenance

A workbook is a program with no tests and no history. The errors that matter are the ones that survive a
glance: a range that stopped one row short, a number typed inside a formula, a cleaning step nobody wrote down.

## 4.1 Formula drift
1. **Check that every range reaches the last row**, including after rows were added. Symptom: a total that stays
   put when data is appended. Fix: use a bounded table or a range written to include the data, and add a check
   cell counting rows against the range.
2. **Copy a formula down and compare a few rows** by hand; mixed absolute and relative references break at the
   row you did not look at.
3. **Look for formulas replaced by values** in the middle of a column (one typed number among formulas). Check:
   a column's formulas should be all one pattern; scan for the exception.
4. **Hidden rows, columns and filters change totals.** Check whether a total counts what is shown or what is
   stored, and unhide before auditing.
5. **Errors hidden by a catch-all** (a formula that returns zero or blank on any failure) turn a real fault into
   a clean-looking cell. Let errors show during cleaning.

## 4.2 Constants and structure
1. **Put every rate, threshold and date in a labelled cell** that formulas point to. Symptom: a tax rate changed
   in one formula and not in forty others. Check: search for numeric literals inside formulas.
2. **One table, one header row, one fact per column.** Merged cells, subtotals in the middle of the data and
   notes in the margin break sorting, filtering and import.
3. **Separate inputs, calculations and outputs** on different sheets or areas, and say which is which.
4. **Do not rely on cell colour for meaning**; a colour does not export and cannot be filtered reliably. Put the
   status in a column.

## 4.3 Provenance and the change log
1. **Keep the raw file unchanged and clean a copy.** Name files so the order is obvious and never overwrite the
   source.
2. **Write the change log as you go**: the rule applied, the columns, the number of rows touched, the date, who
   did it, and the source and date of any lookup or rate table.
3. **Record the unresolved rows** (unreadable date, missing key, conflicting values) in a list for the data
   owner. Never fill a gap with a value you invented to make the table complete.
4. **Prefer a scripted or recorded sequence** for a clean you will repeat, so the next file gets the same
   treatment and the steps can be read.

## 4.4 Reconcile before handing on
1. **Rows in, rows out, rows removed (with reasons)** must add up. Write the three numbers.
2. **A control total before and after** on a column that should not change by cleaning (an amount, a count of
   distinct customers); a difference needs an explanation.
3. **Spot-check a handful of rows against the source system**, chosen at random plus the odd ones (the largest,
   the oldest, the ones with blanks).
4. **Say what the file is not**: the date it was cleaned, what was left unresolved, who owns the figures.
5. **Personal data in a spreadsheet travels with the file.** Remove columns the reader does not need before
   sharing (`business/data-protection`).
