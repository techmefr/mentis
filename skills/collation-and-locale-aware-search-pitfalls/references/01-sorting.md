# collation-and-locale-aware-search-pitfalls §1 — Sorting

Facts about collation come from UTS #35 part 5 (CLDR collation), restated in our own words; runtime behaviour
(the Intl collator and its options) is marked "re-read before relying" where it was not re-read.

## 1.1 Use the locale's collator, once
1. **Symptom:** a list shows Zebra before Älg, every capitalised word before every lowercase one, or an accented
   name at the very end. **Cause:** the sort compares code units or bytes, which orders by encoding, not by what
   a reader expects. **Fix:** sort with the locale-aware comparison of the platform (the `Intl.Collator`
   comparison, a locale-aware `localeCompare`, an ICU collator) and the user's locale.
2. **Build the collator once and reuse it.** Constructing one per comparison costs far more than comparing, and a
   sort calls the comparison many times (re-read before relying). Keep it with the locale in a cache.
3. **A locale-aware comparison is still not a total order of your keys.** Two different strings can compare
   equal at the chosen strength. Add a final tie-breaker (an identifier) so a sort is repeatable and a page
   never repeats or drops a row.
4. **CLDR describes collation as language- and application-dependent**: some languages have special phonebook
   sorting and other criteria, such as phonetic versus visual, so "alphabetical" is a statement about a
   language and a use, not a universal.

## 1.2 Type, locale and settings
1. **One locale can have several sort orders, called types.** The data names a default type per locale (for
   Chinese, the default differs between the simplified and the traditional variant: one orders by pinyin, the
   other by stroke) and a requested type that does not exist falls back first to the locale's default, then to
   the standard type, then to the root collation. A requested "phonebook" for a locale without one silently
   gives the default. **Check:** read back which collation was actually used, as in the spec's table of requested
   and actual types.
2. **Choose the type through the locale tag, not through a country list.** The `-u-co-` extension carries the type;
   do not map country to ordering with a table of your own.
3. **Strength is the first setting to read.** At the primary level only base letters differ, secondary adds
   accents, tertiary (the default) adds case, and a higher level is rarely needed. The spec's common
   combinations: "ignore accents" is primary strength, "ignore case" is secondary strength, accents ignored but
   case kept is primary strength with a case level on.
4. **Case order is a setting.** Where the same letter in two cases compares at the tertiary level, an upper-first
   or lower-first option decides which sorts first; leave it to the locale unless a product rule says otherwise.
5. **Punctuation and spaces are not ignored by default in CLDR.** The standard algorithm ignores them with the
   "shifted" variable handling, while CLDR defaults to non-ignorable, so spaces and punctuation sort as ordinary
   characters, ahead of digits and letters. **Symptom:** "de la Cruz" and "Delaware" order differently in two
   engines. **Fix:** choose the handling, and the extent of what counts as variable (spaces only, up to
   punctuation, up to currency symbols), on purpose.
6. **Numbers inside strings sort digit by digit unless asked.** "item 12" comes before "item 2" unless numeric
   ordering is on, which compares each run of decimal digits by value (the spec's example puts A-21 before
   A-123). Turn it on for file names and codes people read as numbers, and keep it off for identifiers that
   merely contain digits. Long digit runs and leading zeros are an edge to test (re-read before relying).
7. **Scripts sort in a default group order, and it can be changed.** A list mixing Latin, Greek, Cyrillic and
   Han letters follows the root order of script groups; a reorder setting moves a script or the digits and
   punctuation groups. A product with a primary language usually wants that script first.

## 1.3 Index headers and A-Z bars
1. **Symptom:** a jump bar has an "Ö" under O although the language files it after Z, a Czech "CH" is split
   across C and H, accented letters have no bucket. **Cause:** the bucket is the uppercased first code point.
   **Fix:** use the language's index characters from the locale data; each bucket holds the strings whose
   primary weight lies between its character and the next.
2. **An index character can be a sequence.** The spec's examples include a two-letter unit and entries that
   split a bucket for a prefix. Build the list from locale data, not from the alphabet of one language.
3. **The index only works with the matching collation.** The list of buckets and the order of the target list must
   come from the same locale and type, or an item lands in the wrong bucket.
4. **Mixed scripts need boundary buckets.** The data places special buckets before the first character, between
   scripts and after the last; an item in an unlisted script goes in an overflow bucket, not nowhere.

## 1.4 Stored order and its version
1. **Symptom:** after an upgrade of the database, the ICU library or the runtime, rows appear out of order, a
   lookup in an index misses a row that exists, or a unique index admits a duplicate. **Cause:** the
   collation's rules changed with the Unicode or library version, and a stored index still follows the old ones.
   **Fix:** record the collation name and version next to any persisted order (an index, a materialised sort),
   compare it at start-up or in a migration, and rebuild when it differs (re-read before relying: the engines
   that warn about a version mismatch differ).
2. **The spec has a version setting for this reason.** When identical results are needed on different systems,
   the collation version is stated explicitly; otherwise it follows the Unicode version of the system.
3. **Two systems with two versions order differently.** If a browser and a server must agree (a merge of two
   sorted lists, a cursor), pin the collation on one side and send the order, not the strings.

## 1.5 The database's order against the application's
1. **Symptom:** page 2 repeats or skips rows, an alphabetical list differs between the admin and the export.
   **Cause:** the query sorts with the column's collation and the application re-sorts with another, or the
   cursor compares in the application what the database ordered in its own way. **Fix:** sort in one place.
   When the database owns the order, page in the database with a key made of the column and the identifier; when
   the application owns it, load the full set or keep a sort-key column.
2. **A database collation is a column property.** The default of a server, a database and a column can all
   differ, and a comparison in a query takes the column's. Read `mysql-pitfalls` §1.3 for the MySQL names and
   `mongodb-conventions` §2.2 for the index-and-query match rule, instead of copying them.
3. **A case- or accent-insensitive collation changes a unique constraint** (§2.3).
4. **A binary collation is for identifiers, not for names.** Use it for keys, tokens and anything compared
   exactly; use a language collation for what a person reads in order.
