# calendar-and-scheduling-view-pitfalls: origin and source stamps

> Provenance of `skills/calendar-and-scheduling-view-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No calendar was built, run or tested while writing it. Read date: 2026-10-20.

## Sources

| Source | Licence | What it gave |
|---|---|---|
| RFC 5545 iCalendar (rfc-editor.org page, partial reading, read 2026-10-20) | IETF standard, facts only, own words | date values without zone (§3.2.19), end later than start and same type (§3.8.2.2), daylight-saving default for repeated and skipped times (§3.3.5), nominal and exact durations (§3.3.6), end-of-rule type and invalid dates ignored (§3.3.10), range parameter (§3.2.13), exclusion and recurrence id (§3.8.5.1, §3.8.4.4) |
| W3C ARIA Authoring Practices, date-picker dialog example (read 2026-10-20) | W3C licence notice on the page, facts only, own words | keyboard keys, roving tab stop, live heading, grid role |
| None else | n/a | FullCalendar's `LICENSE.md` (MIT, Copyright (c) 2026 Adam Shaw) was read on 2026-10-20 and its documentation was not opened in this pass, so nothing is credited to it. No MIT, Apache-2.0 or CC BY source on calendar interface design was found and read. The content is craft knowledge. |

## Own craft, not from a source
Instant against wall-clock storage, zone display rules, all-day dates with exclusive end, daylight saving gap and repeat handling, half-open range queries, series master with exceptions and splits, snapping and drag rules, lane layout, server-side conflict checks, accessibility and state lists, test matrix.

## Removed
Resource, availability-rule and booking data models (a sibling lot); notifications and reminders; rich text on events; vendor API option names.

## Not verified
1. **Most of the block is own knowledge**: points not credited in the table above were not checked against a source.
2. **Exclusive all-day end:** the standard pages read confirm that an end must be later than the start and of the same type, but did not state the exclusive rule in words (the section describing the event component was not reached). Re-read before relying.
3. **Accessibility points:** the keyboard keys and live heading come from the one W3C example; reduced motion, names of events, agenda alternative and colour rules are recalled practice. A date-picker pattern is not an event-grid pattern.
   No permissive source found for drag, lane layout, conflict checks or load by range, searched: the standard and W3C pages above, FullCalendar's licence file only.
4. **Library names in the framework pointers** are from memory; their zone, all-day and keyboard behaviour was not checked.
5. **Daylight saving rules for invalid and ambiguous local times** differ between date libraries; check the one in use.
6. **No number** (slot length, caps) is stated; none was measured.
