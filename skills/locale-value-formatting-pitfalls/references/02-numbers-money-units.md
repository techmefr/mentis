# locale-value-formatting-pitfalls §2 — Numbers, money, units

Locale facts come from UTS #35 part 3 (Numbers), restated in our own words. Intl behaviour is marked
"re-read before relying" where it was not re-read.

## 2.1 Format with the locale
1. **Symptom:** `1,234.5` shows to a German reader, who reads it as one point two three four five, or `1.234`
   shows to an English reader, who reads it as one point two three four. **Cause:** the separators were written
   into the string. **Fix:** use the number formatter with the locale; never insert a thousands or decimal
   separator by hand and never call a "to fixed" method for display, because it ignores the locale.
2. **The symbols belong to the locale:** decimal separator, grouping separator, minus, plus, percent sign,
   exponent, infinity and not-a-number are all locale data in UTS #35. Grouping is not always by three
   (some locales group the last three and then pairs), and a locale may not group short numbers.
   Never reimplement grouping.
3. **Numbers in a sentence take the plural of the formatted value**, a point owned by
   `i18n-message-format-pitfalls` §1; do not format the number to a string before the message picks the branch.
4. **Percent:** the formatter multiplies a fraction by 100 for the percent style (re-read before relying), so
   pass 0.25 for 25 percent; the percent sign position and spacing are locale data. Passing 25 shows 2,500 %.
5. **Rounding is a display choice with a stated mode.** Set the minimum and maximum fraction digits (or
   significant digits) in the call and do not round by hand first: double rounding changes a value by one
   unit in the last place. Money has its own digits (§2.3).

## 2.2 Store the number, not its text
1. **A number in storage and in an API is a number or a decimal string with a dot**, never a locale string.
   **Symptom:** a value saved from a German form is read as 1.234 by the API. **Fix:** the form parses to a
   canonical value at the boundary (§3.3) and everything after it handles the canonical one.
2. **Large integers and exact decimals** (identifiers, quantities with many digits) do not survive a
   floating-point number; carry them as strings or a big-integer type and give the formatter a decimal string
   where it accepts one (re-read before relying).

## 2.3 Money
1. **Amount and currency are one value.** Store an integer count of minor units and an ISO 4217 code, or a
   decimal string and the code, together. Never a bare number, never a binary float: 0.1 + 0.2 is not 0.3.
2. **The currency is not the locale's.** A German reader sees a price in US dollars as "12,50 $" or a similar
   shape with the dollar sign; the euro is not implied by the language. **Symptom:** a shop shows prices in one
   currency to every German speaker. **Fix:** the currency comes from the price, the pattern from the locale.
3. **Minor-unit digits differ per currency.** UTS #35 holds, per currency, the number of decimal digits
   (default two), with the ISO 4217 minor unit as basis and some deviations, plus separate digits and rounding
   for cash. Some currencies have zero digits and some have three. **Symptom:** a zero-decimal currency shows
   ".00", or an amount stored in minor units is divided by 100 for every currency. **Fix:** take the digits
   from the currency data (the formatter does it) and convert between minor units and amounts with that
   number, never with a constant 100.
4. **Symbol, code or name is a choice.** The formatter can show the symbol, the narrow symbol, the ISO code or
   the name; the same symbol can mean more than one currency (a dollar sign), so a mixed-currency table uses
   the code or the narrow symbol with the code in a header.
5. **The spacing around the symbol is locale data.** UTS #35 holds a pattern per locale and a rule that inserts
   a no-break space between an alphabetic symbol and a digit. Do not strip or re-join the formatted result:
   removing the invisible character the formatter inserted puts the symbol against the digit or lets a line
   break fall between them.
6. **Rounding for totals.** Sum in minor units and round once at the end; rounding each line then summing
   differs from summing then rounding. The rule belongs to the business (tax rules are not in this block); the
   point is that it is written down and tested.

## 2.4 Compact and approximate notation
1. **Compact notation ("1.2K", "1,2 Mio.") is locale data**, with different thresholds and plural forms per
   locale. Use the formatter's compact style (re-read before relying) instead of dividing by 1000 and adding
   a letter.
2. **Show the exact value on demand.** A compact value loses digits; keep the exact one in a title, a tooltip
   or a detail view, and never feed the compact string back into a calculation.

## 2.5 Units
1. **The formatter names a unit; it does not convert one.** A distance of 5 000 metres shown to a user whose
   locale prefers miles is a conversion your code makes. **Symptom:** "5 km" shown as "5 mi" with no change in
   the number. **Fix:** hold the value in one canonical unit (SI), convert with an explicit factor for the
   display unit, and then format number and unit together.
2. **Choose the display unit deliberately.** Which system a region uses is a product decision (some regions mix
   systems, such as road distance in one and fuel in another); put it in a user setting with a locale-based
   default rather than inferring it from the language.
3. **Use the formatter's unit style and length** (long, short, narrow) for the name and its plural, from a
   supported identifier list (re-read before relying: the list of supported simple units is fixed and compound
   units are built from it). An unsupported unit throws; a string suffix is the fallback and is not localized.
4. **Temperature, and any unit with an offset, is not a scale factor.** Convert with the formula, not a ratio.

## 2.6 Numbering systems
1. **The digits themselves can differ by locale.** UTS #35 defines numeric systems (a ten-digit set, for
   example Arabic-Indic or Devanagari) and algorithmic ones (Chinese or Hebrew numerals) and gives each locale
   a default. A locale may default to Western digits even where another set is used locally. Request a system
   with the `-u-nu-` extension only when the product decides to (re-read before relying).
2. **Symptom:** a test compares the formatted string with an ASCII digit string and fails for one locale, or a
   search by number misses a record. **Fix:** compare canonical values; if the page accepts a number typed in
   another digit set, normalise at the boundary (§3.3).
3. **Digits and direction:** the placement of a formatted number inside right-to-left text is
   `rtl-and-bidi-layout-pitfalls` §2.
