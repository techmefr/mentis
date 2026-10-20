# locale-value-formatting-pitfalls §1 — Dates, times, calendars

Facts about locale data come from UTS #35 part 4 (Dates), restated in our own words; the Intl behaviour named
below is the ECMAScript formatter, listed as "re-read before relying" where marked.

## 1.1 Format with the locale, never with a pattern you wrote
1. **Symptom:** a date reads `03/04/2026` to someone who expects 3 April and to someone who expects 4 March;
   a month name is English on a French page; a weekday precedes the day where the locale puts it after.
   **Check:** search for date patterns in strings (`dd/MM`, `MM-dd`) outside code that talks to an API.
   **Fix:** ask the formatter for fields or a style and let the locale arrange them. Fields (year, month, day)
   give the locale freedom to order and punctuate; a length style (short, medium, long, full) gives a complete
   date. Never mix a style with individual fields in one call: the standard formatter rejects the mix (re-read
   before relying).
2. **Pass the locale explicitly.** A formatter called with no locale uses the runtime default, which on a server
   is the machine, not the visitor. The locale comes from negotiation (`locale-negotiation-and-switcher-pitfalls`). Check by search: a date or number formatter constructed with an undefined locale, and the locale-default convenience methods on dates and numbers called with no argument; each ignores a language the user picked inside the application whenever it differs from the device's.
3. **The locale data describes a whole pattern per length, not words.** UTS #35 holds date, time and
   date-plus-time patterns per length and a set of available skeleton patterns; the formatter picks the
   closest. A requested combination that has no good pattern is assembled with a joining pattern, which can
   read stiffly: render the combinations you ship, in the locales you ship.

## 1.2 Store an instant or a plain date; format at the edge
1. **Three different things:** an instant (a point on the timeline, stored as UTC or with an offset), a local
   date-time with a named zone (a meeting at 09:00 in a city, whose offset changes with the season), and a plain
   calendar date (a birthday, an invoice date) that has no zone at all. Name which one a field is.
2. **Symptom:** a birthday shows the day before for users west of the server. **Cause:** a plain date was parsed
   as midnight UTC and shown in a zone behind it. **Fix:** keep a plain date as year-month-day values or a
   date-only string and format it with the zone set to UTC, or use a plain-date type where the platform has
   one. A date-only ISO string is read as UTC while a date-time string without an offset is read as local
   time in the standard `Date` parser (re-read before relying; the two differ and surprise).
3. **Grouping and "today" by the UTC day is the same defect in another form.** Symptom: events are bucketed by cutting the first ten characters of an ISO instant (the UTC date), then the bucket's date string is formatted in the viewer's zone and "today" and "yesterday" are computed from UTC; west of UTC the heading shows the day before, east of UTC a late-evening event lands under the wrong day. Fix: derive the day in the chosen zone (format the instant with that zone to get year, month and day) and use that value for the bucket, the heading and the today test. Grep recipe: the idiom that converts a date to an ISO string and slices ten characters is almost always a UTC day taken for a local one.
4. **A form's "today" limit (a maximum birth date, a minimum start date) built from the UTC date** rejects a valid local date shortly after local midnight east of UTC and accepts tomorrow in the evening west of it. Build it from the local calendar date in the user's zone.
5. **Store the offset or the zone, not the display.** A future local time ("every Monday at 09:00 in Berlin")
   is a zone name plus a wall time; converting it to a UTC instant at creation time breaks it across a change
   of daylight saving. The zone choice between server and client is `locale-negotiation-and-switcher-pitfalls` §3.3.
6. **Show the zone when the reader may be elsewhere.** An event shown in the viewer's zone says so, or shows
   the event's own zone name; ask the formatter for the short or long zone name instead of writing "CET".

## 1.3 Date ranges and intervals
1. **Format a range as a range.** The locale data holds interval patterns that drop repeated parts (one month
   name for two days of the same month). Joining two formatted dates with a dash repeats the month and the
   year and misses the locale's own separator. Use the range formatter of the platform (re-read before relying
   for support) or the interval patterns of the library.

## 1.4 Clock: 12 or 24 hours
1. **The hour cycle is regional data.** UTS #35 gives, per region, one preferred cycle and a list of allowed
   ones (24-hour from 0 to 23, 12-hour from 1 to 12, and two rarer variants). Leave it to the locale; offer a
   user setting only when the product needs it, and pass it as the hour-cycle option.
2. **Symptom:** a 24-hour locale shows "AM/PM", or midnight shows as 24:00. **Cause:** a forced 12-hour flag, or
   a locale whose cycle runs 1 to 24. **Fix:** do not set the flag; if a setting exists, set the cycle (not a
   boolean) and test midnight and noon.
3. **Do not detect AM or PM by string search.** The markers are localized and can be several words; compare
   hours as numbers.

## 1.5 Weeks, weekends and calendars
1. **The first day of the week, the weekend days and the rule that numbers week 1 differ by territory.**
   UTS #35 keeps them as week data keyed by territory, with a minimum number of days for the first week.
   **Symptom:** a calendar grid starts on Sunday in a country that starts on Monday; "week 1" differs between
   the front end and the report. **Fix:** read the first day and minimal days from the locale or the library;
   never hard-code Sunday or Monday, and never compute week numbers with a formula copied from another country.
2. **A calendar is a locale extension, not a country list.** UTS #35 gives per territory the calendars in
   common use in preference order (Gregorian only by default; for example Buddhist before Gregorian for
   Thailand, Gregorian before Japanese for Japan). A calendar is requested with the `-u-ca-` extension on the
   locale tag, and the numbering system with `-u-nu-` (re-read before relying). Show the common calendars
   where a user can choose one and keep the stored value Gregorian or an instant.
3. **A year in another calendar is not the Gregorian year.** Never mix a calendar year shown to the user with a
   year used in arithmetic or an API call; do arithmetic on the canonical value and format last.
4. **Era and year display.** In locales with eras the formatted year includes the era name; a test that
   compares a formatted year with a number fails there. Compare canonical values.

## 1.6 Tests that survive a time zone
1. **Fix the zone and the locale in every test that formats a date.** A test that passes in the author's zone and
   fails in CI formats with the machine zone. Set both explicitly and pick a date near a daylight-saving change
   and one near midnight. The rule for server-rendered Vue pages is `nuxt-no-hydration-nondeterminism`.
