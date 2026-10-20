# booking-and-scheduling-app-pitfalls §1 — Time, availability and conflicts

> Part 1 of `skills/booking-and-scheduling-app-pitfalls`. Read it when a schema or the reservation write path is
> designed. Craft knowledge, no external source read.

1. **Instant or wall time: decide per field.** Symptom: a weekly 09:00 appointment moves to 10:00 after the
   clocks change, or a flight-like event shifts when the viewer travels. Fix: a booking that happened or will
   happen at a fixed physical moment (a call across zones, a delivery slot) stores the instant in UTC; a
   booking meant as "9 o'clock where the venue is" stores the local date, local time and the venue's zone name,
   and derives the instant when needed. Store the zone with the venue or resource, not with the browser. Both
   forms are shown with their zone to the person booking.
2. **Zone names, never offsets.** Symptom: "+01:00" saved, then summer comes. Fix: store a zone name from the
   standard zone database, keep the database updated (rules change by decree), and re-derive instants from the
   local time when the rules for a future date change. Check: list the zones your users sit in and test two
   with different clock-change dates, plus one with a half-hour offset and one with no clock change.
3. **Clock changes create gaps and repeats.** Symptom: a slot at a local time that does not exist on the spring
   date, or two slots at the same local time on the autumn date. Fix: generate slots in local time, drop
   non-existent local times, label the repeated hour with its offset or generate by instant for that day,
   and treat a day as 23 or 25 hours long in duration maths. Never add 24 hours to get "tomorrow": add one
   calendar day in the zone. Test dates are fixed in the test, not read from the real clock.
4. **Availability is rules plus exceptions.** Model weekly working hours per resource (several intervals per
   day), date exceptions (holiday, leave, one-off opening), and existing bookings as the last subtraction.
   Symptom: rules overwritten by an exception edit and lost. Fix: exceptions are separate rows that override a
   date or a range, rules are versioned with a valid-from date, and an edit never rewrites past dates.
   Recurrence (every week, every second Monday, the last Friday) is stored as a rule with an anchor and a zone
   and expanded to occurrences for a window; a series edit asks "this one, this and following, all" and
   changes the rule only for the chosen range.
5. **Slots are computed on the server, from one function.** Inputs: resource, service duration, window, zone of
   the viewer, now. Rules applied in a stated order: working hours, exceptions, existing bookings and holds,
   buffer before and after, minimum lead time, maximum horizon, slot step. Symptom: the list shows a slot
   that the booking call then refuses, or the browser and the server disagree. Fix: the same function backs
   the list and the confirmation check; the browser only displays; the response states the zone it used.
6. **Double booking is prevented where the data lives.** Symptom: two customers confirm the same slot a
   second apart. Check: fire N parallel requests for one slot and assert one wins. Fix: a database constraint
   that rejects overlapping ranges for one resource where the database supports it, otherwise a unique
   constraint on (resource, slot start) for fixed slots, or a row lock on the resource inside the
   transaction; never "select free, then insert" in application code. The losing request gets a clear
   "no longer available" with alternatives, not a server error. Capacity above one (a class of twelve) is a
   conditional counter update, as in `skills/inventory-stock-app-pitfalls`, with the same parallel test.
7. **Holds expire.** Symptom: slots blocked forever by people who left the checkout. Fix: a hold is a booking
   in state held with an expiry time; availability treats unexpired holds as taken; a scheduled job and a
   lazy check on read release expired ones; confirming after expiry re-checks availability and may fail
   politely; the hold lifetime is a policy value. Extending a hold is allowed once, not indefinitely.
8. **Duration, buffers and multi-resource.** A service has a duration, optional buffers (cleaning, travel), and
   may need several resources at once (a person and a room). Symptom: back-to-back bookings with no travel, or a
   room free but the person busy. Fix: a booking claims every needed resource for its padded interval in one
   transaction (lock in a fixed order to avoid deadlock), and the buffer is shown to staff but not always to
   the customer.
9. **Past, now and lead time.** Reject bookings in the past using the server clock, apply a minimum lead time so
   nobody books the next minute, and show a "now" computed in the viewer's zone only for display. Edits to a
   past booking are corrections with an audit trail, not silent changes.
