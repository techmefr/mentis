# calendar-and-scheduling-view-pitfalls: origin and source stamps

> Provenance of `skills/calendar-and-scheduling-view-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No calendar was built, run or tested while writing it. Read date: 2026-10-20.

## Sources

| Source | Licence | What it gave |
|---|---|---|
| None | n/a | FullCalendar's `LICENSE.md` (MIT, Copyright (c) 2026 Adam Shaw) was read on 2026-10-20 and its documentation was not opened in this pass, so nothing is credited to it. No MIT, Apache-2.0 or CC BY source on calendar interface design was found and read. The content is craft knowledge. |

## Own craft, not from a source
Instant against wall-clock storage, zone display rules, all-day dates with exclusive end, daylight saving gap and repeat handling, half-open range queries, series master with exceptions and splits, snapping and drag rules, lane layout, server-side conflict checks, accessibility and state lists, test matrix.

## Removed
Resource, availability-rule and booking data models (a sibling lot); notifications and reminders; rich text on events; vendor API option names.

## Not verified
1. **Everything is own knowledge**: no external claim was checked against a source.
2. **Recurrence rule semantics** (iCalendar, RFC 5545, exclusive all-day end) are recalled public facts, not re-read in this pass. Re-read before relying.
3. **Accessibility points** (grid keys, live regions, reduced motion) are recalled public practice, not re-read in this pass.
4. **Library names in the framework pointers** are from memory; their zone, all-day and keyboard behaviour was not checked.
5. **Daylight saving rules for invalid and ambiguous local times** differ between date libraries; check the one in use.
6. **No number** (slot length, caps) is stated; none was measured.
