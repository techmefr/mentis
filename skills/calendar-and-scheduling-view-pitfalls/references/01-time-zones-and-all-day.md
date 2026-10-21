# calendar-and-scheduling-view-pitfalls §1 — Time zones, all-day and ranges

Sources: own craft, plus facts from the iCalendar standard (RFC 5545, full text re-read 2026-10-20, own words), the tz database theory page (public domain, read 2026-10-20), RFC 9557 and Unicode UTS 35 (read 2026-10-20) where marked; no source text taken.

## 1.1 Two kinds of time
1. **Symptom: a weekly 09:00 meeting shows at 10:00 for half the year.** Cause: it was stored as a UTC instant computed once in winter; after the clock change the offset differs but the stored instant did not move.
2. **A moment that happened or must be simultaneous for everyone is an instant** (a call starting, a deadline set in UTC, a log entry). Store it as UTC and show it in the viewer's zone.
3. **A plan that follows a place's clock is wall-clock time plus a zone identifier** ("09:00 in Europe/Paris, every Monday"). Store the local date, the local time and the zone name, never a fixed offset, because offsets change with the rules. The tz database documentation uses exactly this case: a meeting set for 13:00 next October 1 in Dublin goes wrong if software keeps conversions made before Ireland changes its daylight saving rules. RFC 9557 adds that copying an offset into an offset-only zone makes a program add six months wrongly across a clock change (+01:00 is not Europe/Paris), and that an offset and a zone name kept side by side can become inconsistent when the zone definition changes; the zone name is the part to trust.
4. **A third kind exists: floating time**, a local date and time with no zone that means the same clock reading wherever the person is (iCalendar form 1, RFC 5545 section 3.3.5). The standard says to use it only where that is the reasonable behaviour (for example a daily reminder) and that two attendees in different zones will then take part at different actual times; never let it be the default for an event others attend.
5. **Pick the kind per event type, and write it in the model,** not in a comment: an appointment at a clinic is wall-clock in the clinic's zone; a webinar start can be an instant.
6. **Store zone identifiers, not abbreviations** ("CST" is several zones). The zone database is updated by governments; keep the runtime's data current (`locale-value-formatting-pitfalls`). The tz theory page confirms the ambiguity (CST in China and North America, IST in India, Ireland and Israel) and says its zone names are meant to identify a zone uniquely. It also says users are not expected to pick Region/City names unaided, so offer a picker with place names or a map, not a raw list of identifiers.
7. **Convert at the edges only:** parse to a zoned value on input, compute in one representation, format on output. Symptom of converting twice: events off by exactly the offset.

## 1.2 Which zone does the viewer see
1. **Decide and show the zone shown.** Options: the viewer's profile zone, the browser zone, or the event's own zone. State it in the header ("Times in Europe/Paris") and let the user change it.
2. **Show the event's own zone when it differs from the viewer's** ("09:00 Paris, 03:00 your time"). A clinic appointment must read in the clinic's zone first.
3. **The browser zone is not the user's real zone when travelling or on a VPN;** a profile setting wins for business data, the browser is a default.
4. **A resource has a zone** (a room, a person, a location), and availability is evaluated there, not in the viewer's.
5. **Server and database run in UTC;** the web server's local zone must never decide what a date is (`laravel-date-via-localised-accessors`).
6. **A local date-and-time form control carries no zone.** The HTML Standard describes the datetime-local input value as a date and time with no time zone, so the zone has to come from a separate, visible field (or the event's zone) and be saved with the value; otherwise the server guesses.

## 1.3 All-day and multi-day events
1. **Symptom: an all-day event shows on two days for users west of the author, or ends a day early.** Cause: it was saved as a midnight instant, and a different zone reads that instant as the previous or next local day.
2. **An all-day event is a date or a date range with no time and no zone,** shown on the same calendar days for everyone. RFC 5545 §3.2.19 says the zone parameter must not be applied to date values, and §3.8.2.2 says the end value type must match the start (a date start needs a date end) and must be later than the start. Re-read in the full text 2026-10-20; section 3.3.5 also forbids writing a UTC offset into a date-time value.
3. **Use an exclusive end date** for ranges (an event on the 5th ends on the 6th), the convention calendar standards use: RFC 5545 §3.6.1 (read 2026-10-20) calls the end of an event non-inclusive, and a date start with no end or duration lasts one day. Inclusive ends break at month boundaries and in sums of days. If the interface shows an inclusive end, convert at the edge and say so in the form.
4. **A timed event crossing midnight** is drawn as two segments in a day grid and as one bar in a month view; it keeps one identity for editing.
5. **Multi-day bars wrap at the week start** and show their title again on the new row, with a visible "continues" edge.
6. **Do not let an all-day toggle silently keep the old time:** switching to all-day drops the times, switching back asks for them.

## 1.4 Daylight saving edges
1. **The spring gap does not exist and the autumn hour happens twice.** A local time of 02:30 on the gap day is invalid; 01:30 on the repeat day is ambiguous.
2. **Decide the rule for each:** shift an invalid time forward, and pick the first or second occurrence of an ambiguous one, then apply it in one function and test it. RFC 5545 §3.3.5 (read 2026-10-20) fixes a default for zoned local times: a repeated time means the first occurrence, and a skipped time is read with the offset in force before the gap, so it lands after the gap. Use that default unless the product says otherwise.
3. **A recurring series on a gap day keeps its wall-clock rule** and moves to the nearest valid time that day; it does not shift all later occurrences. Interchange caution: RFC 5545 §3.3.10 says recurrence instances falling on an invalid date or a nonexistent local time must be ignored and not counted, which differs from moving them; if the series is exported to calendar clients, expect the skip and decide which behaviour you show.
4. **Duration arithmetic differs from calendar arithmetic.** "Plus 24 hours" and "plus one day" are different on a clock-change day; scheduling intent is almost always "one day". RFC 5545 §3.3.6 defines weeks and days as nominal (their length depends on the calendar) and hours, minutes and seconds as exact.
5. **Day grids on a clock-change day have 23 or 25 hour rows;** do not hard-code 24 rows.

## 1.5 Ranges, weeks and formatting
1. **Query by a half-open range** (start inclusive, end exclusive), in UTC for instants and dates for all-day events, and return events that overlap the range, not only those that start inside it.
2. **The first day of the week is a locale and user choice** (Sunday, Monday, Saturday); week numbering also differs by locale. Take both from the locale, not from a constant. Unicode UTS 35 (CLDR) keeps per-territory first-day, weekend start and end, and minimum-days-in-first-week data, with a world default and overrides by territory, so the first day and the week-of-year rule are data, and the weekend is not always Saturday and Sunday.
3. **Month grids show leading and trailing days of adjacent months;** decide whether their events are shown and make the dimming not depend on colour alone.
4. **Format day and month names, time cycle (12 or 24 hour) and ordering through the locale** (`locale-value-formatting-pitfalls`); right-to-left layouts mirror the grid and the week order.
5. **Non-Gregorian calendars exist for some locales;** if you must support them, take the calendar from the locale and keep storage Gregorian. UTS 35 lists the calendars in common use per territory with a preferred order (Japan: Gregorian then Japanese; Thailand: Buddhist then Gregorian) and says an interface offering a choice should show those.

## Checks
- An event created in one zone and read in two others shows the correct local days and times, before and after a clock change.
- An all-day event shows on the same date for users in zones on both sides of UTC.
- A series crossing both clock changes keeps its wall-clock time.
- A range query returns an event that started before the range and ends inside it.
