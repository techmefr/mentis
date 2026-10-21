# locale-value-formatting-pitfalls §3 — Lists, relative time, parsing

## 3.1 Lists
1. **Symptom:** "Anna, Ben, and Chloe" in a locale that writes no comma before the last conjunction, or the
   word "and" hard-coded between two names. **Cause:** `join(", ")` plus a literal. **Fix:** use the list
   formatter (type values per ECMA-402: conjunction, disjunction, unit; re-read runtime support) with the type and the style
   (long, short, narrow); the locale provides the separator, the final word and the pair form.
2. **The conjunction word is part of the grammar, not a label.** "Or" lists, "and" lists and unit lists
   ("5 ft, 3 in") are different types; pick the type that matches the meaning.
3. **Items are formatted before they are listed**, each with its own locale rules (names, dates, amounts);
   pass the formatted items. Do not format the list with its items already joined.
4. **A long list is a layout problem too.** Truncate after a count and show the rest on demand ("Anna, Ben and
   3 others") with a plural-aware message (`i18n-message-format-pitfalls` §1), not by cutting a string.

## 3.2 Relative time and durations
1. **Use the relative-time formatter**, with the unit and a signed number: "in 3 days" and "3 days ago" are
   different words in most languages, and some have special words for 1 (such as yesterday or tomorrow),
   available through the "auto" numeric option (re-read before relying).
2. **Pick the unit by size yourself.** The formatter formats a number of a unit you choose; the rule that turns
   "73 seconds" into "a minute ago" is yours. Write it once, test its edges, and use the same reference "now"
   on the server and the client (`locale-negotiation-and-switcher-pitfalls` §3.3 point 4).
3. **A relative time goes stale.** A cached or server-rendered "2 minutes ago" is wrong when read; refresh it
   or give the absolute time as the title.
4. **Durations ("1 h 30 min", "01:30:00") are not relative times.** A duration formatter exists in newer
   runtimes (re-read before relying for support); without it, format each unit with the unit formatter (§2.5)
   and join with the list formatter set to the unit type, never with literal letters.
5. **Never mix "today" logic with zones you did not choose.** "Today" and "yesterday" depend on the viewer's
   zone and on a day boundary; compute the day difference in the chosen zone.
6. **Two formatters with one name and different input units.** Symptom: a duration shows as "83:20" because a shared helper takes seconds and some call sites pass milliseconds, or the reverse; a second, hand-built helper with the same name in a utility file shadows or duplicates the locale-aware one. Check: search for every definition of each shared formatter (duration, size, relative time) and list the unit its input takes; then check each call site passes that unit, and delete the duplicate or rename it to carry the unit. Name the unit in the parameter or the function.

## 3.3 Reading a typed value back
1. **There is no inverse of the formatter in the standard library.** A global number parser reads `1,5` as 1
   and `1.234` as 1.234 everywhere. **Symptom:** a German user types "1.234,50" and the order total is 1.234.
   **Fix:** read the separators of the user's locale (format a known number with the locale and read the group
   and decimal parts from the result's parts), strip the group separator, replace the decimal separator with a
   dot, then parse; or use a number input that returns a value, or a library that parses by locale.
2. **Accept more than one form in a forgiving way, and show what was understood.** UTS #35 recommends, for
   dates, trying the expected format of the locale first (it is the only way to tell 03/07 as a month and year
   from 03/07 as a day), matching loosely on case and normalization, and accepting the ASCII variants of AM and
   PM. After parsing, echo the result in the locale's format so the user sees what the system understood.
3. **For dates, prefer a structured control** (a date picker that returns a value, or three labelled fields in
   the locale's order) over free text. A text field that accepts a date makes the product responsible for every
   format of every locale it is opened in.
4. **Digits in another script and full-width digits** reach inputs through keyboards and paste; normalise them
   to canonical digits at the boundary and validate after.
5. **Validate canonical values, not display strings.** The server checks the canonical amount or date it
   receives; it never trusts a display string or tries to guess the locale it came from.
