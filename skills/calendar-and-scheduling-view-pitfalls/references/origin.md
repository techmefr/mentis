# calendar-and-scheduling-view-pitfalls: origin and source stamps

> Provenance of `skills/calendar-and-scheduling-view-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No calendar was built, run or tested while writing it. Read date: 2026-10-20.

## Sources

| Source | Licence | What it gave |
|---|---|---|
| RFC 5545 iCalendar (rfc-editor.org page, partial reading, read 2026-10-20) | IETF standard, facts only, own words | date values without zone (§3.2.19), end later than start and same type (§3.8.2.2), daylight-saving default for repeated and skipped times (§3.3.5), nominal and exact durations (§3.3.6), end-of-rule type and invalid dates ignored (§3.3.10), range parameter (§3.2.13), exclusion and recurrence id (§3.8.5.1, §3.8.4.4), non-inclusive event end and one-day default for a date start (§3.6.1, re-read 2026-10-20 through a summarising fetcher) |
| W3C ARIA Authoring Practices, date-picker dialog example (read 2026-10-20) | W3C licence notice on the page, facts only, own words | keyboard keys, roving tab stop, live heading, grid role |
| RFC 5545, full text, <https://www.rfc-editor.org/rfc/rfc5545>, re-read 2026-10-20 (raw text, not a summary) | IETF Trust document; facts only, own words | Every section number cited in the block re-checked: 3.2.13, 3.2.19, 3.3.5 (three forms, first occurrence, offset before the gap, floating time), 3.3.6, 3.3.10 (UNTIL type, COUNT, invalid instances ignored and not counted), 3.6.1, 3.8.2.2, 3.8.4.4, 3.8.5.1, 3.8.5.3 |
| IANA time zone database, theory and pragmatics page, <https://data.iana.org/time-zones/theory.html>, read 2026-10-20 | Public domain (the page states it) | Future-meeting example, ambiguity of abbreviations, picker advice (§1.1.3, §1.1.6) |
| RFC 9557, Date and Time on the Internet: Timestamps with Additional Information, sections 1.2 and 3.4, <https://www.rfc-editor.org/rfc/rfc9557>, read 2026-10-20 | IETF Trust document; facts only | Offset-only zone pitfall, offset and zone name inconsistency (§1.1.3) |
| Unicode UTS 35 (LDML), dates chapter, week data and calendar preference, <https://unicode.org/reports/tr35/tr35-dates.html>, read 2026-10-20 | Unicode terms of use (copying needs the notices); facts only, own words | First day, weekend and minimum days as territory data; calendar preference (§1.5.2, §1.5.5) |
| W3C WCAG 2.2 (full page), W3C ARIA Authoring Practices date picker dialog example (re-read in full), HTML Standard datetime-local description, all 2026-10-20 | W3C Document License; CC BY 4.0 (WHATWG); facts only | SC 1.4.10 and 2.5.7 (§3.1.6, §3.1.10); date grid keys re-verified one by one |
| None else | n/a | FullCalendar's `LICENSE.md` (MIT, Copyright (c) 2026 Adam Shaw) was read on 2026-10-20 and its documentation was not opened in this pass, so nothing is credited to it. No MIT, Apache-2.0 or CC BY source on calendar interface design was found and read. The content is craft knowledge. |

## Own craft, not from a source
Instant against wall-clock storage, zone display rules, all-day dates with exclusive end, daylight saving gap and repeat handling, half-open range queries, series master with exceptions and splits, snapping and drag rules, lane layout, server-side conflict checks, accessibility and state lists, test matrix.

## Removed
Resource, availability-rule and booking data models (a sibling lot); notifications and reminders; rich text on events; vendor API option names.

## Not verified
1. **Most of the block is still own knowledge**: points not credited in the table above were not checked against a source. Second pass 2026-10-20: 14 points verified or added from the full RFC 5545 text, the tz theory page, RFC 9557, UTS 35, WCAG 2.2 and the date picker example (the §3.1.4 key list matches the example exactly); 0 corrected, 0 deleted; added: floating time (§1.1.4), count against end date (§2.1.7). Snapping, lane layout, conflict checks, load by range, states and tests are craft, no source found.
2. **Exclusive all-day end: verified 2026-10-20** (RFC 5545 §3.6.1: end is non-inclusive; a date start alone lasts one day), read through a summarising fetcher.
3. **Accessibility points:** the keyboard keys and live heading come from the one W3C example; reduced motion, names of events, agenda alternative and colour rules are recalled practice. A date-picker pattern is not an event-grid pattern.
   No permissive source found for drag, lane layout, conflict checks or load by range, searched: the standard and W3C pages above, FullCalendar's licence file only.
4. **Library names in the framework pointers** are from memory; their zone, all-day and keyboard behaviour was not checked.
5. **Daylight saving rules for invalid and ambiguous local times** differ between date libraries; check the one in use.
6. **No number** (slot length, caps) is stated; none was measured.

Independent verification 2026-10-21: 26 checked, 26 matched, 0 corrected, 0 unverified
