# spreadsheet-data-cleaning-pitfalls §2 — Dates, numbers and locale

The same characters mean different things in different locales. A cleaned file is wrong in exactly the rows where
the guess failed, and the failures look valid.

## 2.1 Dates
1. **Write the date format of the source** (day-month-year, month-day-year, year-month-day) from the file's origin
   and from rows where one part is above twelve. Symptom: dates up to the twelfth parsed in one order and the rest
   left as text. Check: look for a mix of real dates and text in one column.
2. **Serial numbers are dates in disguise.** A column of five-digit numbers in a date field is an unformatted
   date counter; its origin (the epoch the program counts from) varies by program and file, so confirm it on a row
   whose real date you know before converting. One vendor documents a 1900 and a 1904 system a fixed 1,462 days apart,
   the first the default on Windows and recent Mac versions and the second the default on older Mac versions; dates
   copied between workbooks on different systems shift by that offset, and dates inside a chart are not converted
   (Microsoft Support, date systems in Excel).
3. **Two-digit years are ambiguous.** Decide the century rule with the owner of the data and apply it everywhere.
4. **A date with a time is a moment, and a moment needs a zone.** Record whether times are local, UTC or
   unlabelled before comparing across sources or computing durations. Symptom: events on the wrong day near
   midnight.
5. **Keep the original text beside the converted date** until the owner has accepted the result.

## 2.2 Numbers
1. **Decimal comma and thousand separator swap by locale.** "1.234" is one thousand two hundred thirty-four in
   one and about one in another. Symptom: totals that are off by a factor of a thousand. Check: compare a control
   total with the source system.
2. **Strip symbols into their own columns**: currency sign, unit, percent. A percent stored as 0.12 and as 12 in
   the same column is a unit error; decide one, convert, and say which.
3. **Negative numbers come in several forms** (a minus sign, brackets, a trailing minus). Check the minimum value
   and the count of negatives after conversion.
4. **Rounding is a display unless you round the value.** Summing displayed, rounded figures differs from the
   total of the stored ones; say which one is reported.

## 2.3 Mixed units and currencies
1. **A column with several currencies or units is not a number column.** Keep the unit in its own column and
   convert with a stated rate table and date, not a rate typed from memory.
2. **Record the rate source and date** in the change log (§4.3).

## 2.4 Text hygiene
1. **Trim leading and trailing spaces and replace non-breaking spaces** before comparing text; otherwise two
   equal-looking values never match (§3).
2. **Normalise case and accents for matching, not for display**: keep the original in its column.
3. **Do not change spelling variants into one value silently**; build a mapping table that a person can read and
   correct (§3.3).
