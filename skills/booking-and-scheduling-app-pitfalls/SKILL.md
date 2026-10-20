---
name: booking-and-scheduling-app-pitfalls
description: "Use when a booking, appointment or scheduling application is designed or built: resource, service and availability model, time zones and daylight-saving transitions, storing instants versus wall-clock times, recurring availability and exceptions, slot generation, double booking and concurrency, temporary holds with expiry, buffers and lead times, cancellation and rescheduling rules, no-shows, waitlists, calendar sync and invitations, reminders, roles, payments and deposits at the boundary, what to split first and what gets regretted at v2. Method only; no cancellation fee or refund rule is stated."
---

# booking-and-scheduling-app-pitfalls

A defensive block for building the application that lets people reserve time on a person, a room or a thing.
Booking tools fail in familiar ways: a slot appears at the wrong hour after a clock change, two customers get the
same slot, a held slot is never released, a recurring appointment drifts by an hour in winter, a cancellation
frees a slot that was already paid, and a calendar sync creates duplicates. The content is mostly craft knowledge; some points are checked against the iCalendar standard and the IANA time zone notes (see `references/origin.md`). Time handling in tests is in
`skills/python-patching-and-time-pitfalls` and `skills/dotnet-testcontainers-and-time-seam-pitfalls`; date display
is in `skills/laravel-date-via-localised-accessors`; scheduled jobs are in `skills/laravel-scheduling`; idempotent
writes are in `skills/laravel-idempotent-jobs`; money is in `skills/money-arithmetic-and-rounding-pitfalls`;
reminders by mail are in `skills/laravel-mail-via-notifications`; the list and filter screens are in
`skills/data-table-ui-pitfalls` and `skills/filters-search-and-saved-views-pitfalls`; the same clock rules serve
SLA windows in `skills/helpdesk-ticketing-app-build-pitfalls` and leave dates in
`skills/hr-leave-and-time-tracking-app-pitfalls`.

## When
- A tool lets customers or staff reserve a slot, a seat, a room or a person.
- Availability is computed from working hours, exceptions and existing bookings.
- Bookings are synchronised with an external calendar or taken from several channels.
- A hold, a deposit, a cancellation rule or a recurrence is added.

**Skip when** nothing in the application reserves time. If it only decides whether now falls inside a rule (open hours, an access window, a quiet period) and has no slots, holds or bookings, apply §1 points 1 to 4 and the rule that the server decides (point 5) only, and say "not applicable: no reservation" for points 5 to 9 and for §2.

## Steps

**Read the part you need before the time model or the reservation write path is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Instants versus wall time, zones and clock changes, availability and recurrence, slot generation, double booking, holds, buffers | a schema or the reservation write path is designed | [`01-time-availability-and-conflicts.md`](./references/01-time-availability-and-conflicts.md) |
| 2 | Cancellation and rescheduling, no-shows, waitlist, calendar sync, reminders, roles, payments at the boundary, what to split first, v2 regrets, framework pointers | policies, integrations or the first release are planned | [`02-policies-sync-and-v2.md`](./references/02-policies-sync-and-v2.md) |

## Output / checkpoint
Before building: for every stored time, whether it is an instant or a wall-clock time and which zone governs it;
the resource, service and availability entities; the conflict rule and where it is enforced; the hold lifetime;
the buffer and lead-time rules; the cancellation, reschedule and no-show policies (owned by the business); the
calendar source of truth; the reminder schedule. Evidence is a test across a spring-forward and a fall-back date
in two zones, a parallel test where N customers take one slot, a test that an expired hold frees the slot, and a
test that a recurring series keeps its local hour across a clock change; for a rule-only schedule, the same spring-forward and fall-back test on a window edge, and a statement of what the device clock may and may not decide offline. Nothing here was run by us.

## Guardrails
- This block states no cancellation fee, refund, deposit or no-show penalty; the business sets them and writes
  them with a date. It is not legal advice.
- Never store a future appointment only as a UTC instant when the person means a local hour; keep the local time
  and the zone name, and derive the instant (§1, point 1).
- Never use a fixed offset as a zone; store a zone name from the zone database (§1, point 2).
- Never check availability and insert in two steps; enforce the conflict in the database or under a lock
  (§1, point 6).
- Never hold a slot without an expiry and a job that releases it (§1, point 7).
- Never delete a booking on cancel; keep it with a state and a reason (§2, point 1).
- Never let a calendar sync overwrite the application's bookings without a source-of-truth rule and an external
  id (§2, point 4).
- Never compute availability only in the browser; the server decides (§1, point 5).

## Origin
Written from craft knowledge of building booking and scheduling applications, then checked on 2026-10-20 against the
iCalendar standard and the IANA time zone database notes, credited in the origin file; no text was taken. See
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
