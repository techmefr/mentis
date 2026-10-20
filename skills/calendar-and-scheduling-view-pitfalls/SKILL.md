---
name: calendar-and-scheduling-view-pitfalls
description: "Use when a calendar view, day or week grid, agenda, booking or scheduling interface is written or reviewed in a business application, whatever the framework: storing an event as an instant or as a wall-clock time, time zones and daylight saving gaps, all-day and multi-day events and their end dates, showing recurring events and editing one occurrence against the series, overlapping events layout, drag to move and resize with snapping and conflict checks, the empty, loading, failed-save and busy states, and accessibility of a grid (keyboard, names, focus, a list alternative), plus the tests that catch them."
---

# calendar-and-scheduling-view-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the view where a date bug becomes a missed appointment. The premise: **a calendar
displays two different kinds of time as if they were one** (an instant that happened, and a wall-clock plan that follows
local rules), and then lets people drag them. It looks right in the developer's zone in March; it breaks for another zone,
on the clock change, on a recurring series and for a keyboard user. Locale formatting is in `locale-value-formatting-pitfalls`,
date input in `international-input-pitfalls`, back-end date accessors in `laravel-date-via-localised-accessors`, the
resource model behind bookings (rooms, people, availability rules) is a sibling lot, and widget semantics are in
`accessibility`.

## When
- A month, week, day or agenda view, a scheduling grid, a booking picker or a drag-to-reschedule interaction is built or reviewed.
- A user reports "the meeting moved an hour", "my all-day event spans two days", "I edited one occurrence and the whole series changed", "I cannot use it without a mouse".
- Users or resources live in different time zones, or events repeat.

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Instant against wall-clock storage, zones, daylight saving, all-day, multi-day, ranges, week start | an event is stored, shown or compared across zones | [`01-time-zones-and-all-day.md`](./references/01-time-zones-and-all-day.md) |
| 2 | Showing recurrence, editing one or all, exceptions, drag to move and resize, snapping, conflicts, overlap layout | events repeat or can be dragged | [`02-recurrence-and-direct-edit.md`](./references/02-recurrence-and-direct-edit.md) |
| 3 | Accessibility of a grid, states, load by range and scale, tests, framework pointers | a view ships, scales or is tested | [`03-access-states-scale-tests.md`](./references/03-access-states-scale-tests.md) |

## Output / checkpoint
A change is done when: each event stores what its kind needs (instant plus zone, or wall-clock plus rule); all-day events
use dates, not midnight instants; recurrence is expanded in one place; every drag has a keyboard route; the view loads by
visible range; and the tests in §3.4 exist. No checkpoint is written: a craft block, 🟡, nothing here was run in an
application.

## Guardrails
- Store a plan that must stay at 09:00 local as wall-clock time plus a zone, and a happened-at moment as an instant (§1.1). Never store everything as a bare UTC instant and add an offset in the browser.
- Keep all-day events as dates with an exclusive end (§1.3). Never model them as 00:00 to 23:59.
- Expand a series on the server for the requested range and keep exceptions separate (§2.2). Never edit the series copy when the user changed one occurrence.
- Give every drag a keyboard route and announce the result (§3.1). Never ship a grid that works with a pointer only.
- Check conflicts on the server, in the resource's own zone (§2.5). Never trust the client's overlap test.
- Facts about a library are for the commit stamped in `references/origin.md`; re-read before relying.

## Origin
Own craft knowledge, with the recurrence, daylight-saving and keyboard points checked on 2026-10-20 against the iCalendar standard and a W3C keyboard-pattern example (facts only); no permissive source on calendar interface design was found and read. Details in
[`references/origin.md`](./references/origin.md).
