# spreadsheet-data-cleaning-pitfalls §1 — Types and identifiers

A spreadsheet decides what a cell is the moment a file opens. A value that looks like a number is turned into
one, and the original text is gone as soon as the file is saved.

## 1.1 Identifiers are text
1. **Treat any value you would never add up as text**: postal codes, account and order numbers, phone numbers,
   product codes, national identifiers. Symptom: leading zeros disappear, a "+" is dropped, a code starting with
   a letter-digit mix is read as a date. Fix: import the column as text and keep it as text.
2. **Long digit strings lose digits.** Programs keep a limited number of significant digits and display the rest as
   a power of ten. Symptom: two different card or tracking numbers look identical, or end in zeros. Check: compare
   the length of the cleaned value with the original. Fix: text, from the import step, never repaired after the
   fact (the lost digits cannot be recovered from the cell).
3. **Gene-style names and short codes can be read as dates** by some programs (a letter-and-digit code turned into a
   month and day). Check a sample of such codes after opening.

## 1.2 Open a CSV without a guess
1. **Use the import dialog, not a double click**, so each column's type is chosen by you. Symptom: a file that
   looks fine and differs from the source in cells you did not look at.
2. **Check the delimiter, the quote character and the encoding.** Symptom: accented characters turned into
   symbols, or an entire row in one cell. Fix: re-import with the correct encoding rather than retyping.
3. **Compare row and column counts with the source** (a line count of the raw file against the table).
4. **Beware a text-looking number with spaces or a non-breaking space**; it will not sum. Check with a count of
   numeric cells against a count of non-empty cells.

## 1.3 Saving without damage
1. **Saving a CSV from a spreadsheet writes what is displayed in some cases and what is stored in others**, and
   rewrites separators with the locale. Open the saved file in a plain text view before sending it on.
2. **Keep a typed format for the final deliverable** (a workbook or a documented CSV) and say which columns are
   text in a short readme or header row.
3. **Do not reformat a cell to "fix" a lost value**; the original is lost, go back to the source.

## 1.4 Quick type audit
1. **For each column write its intended type** (text, whole number, decimal, date, category, boolean) before
   cleaning.
2. **Count the values that do not fit** (text in a number column, number in a date column) and list them; do not
   coerce them quietly.
3. **Mixed types in one column are a finding**, reported to whoever owns the data.
