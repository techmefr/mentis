# booking-and-scheduling-app-pitfalls §2 — Policies, sync and v2

> Part 2 of `skills/booking-and-scheduling-app-pitfalls`. Read it when policies, integrations or the first
> release are planned. Craft knowledge, no external source read. No fee or refund rule is stated.

1. **Cancellation is a state, not a delete.** Booking states: held, confirmed, cancelled by customer, cancelled
   by provider, completed, no-show. Symptom: a deleted booking leaves a paid invoice with nothing behind it.
   Fix: keep the row with its state, reason, actor and time; a cancel frees the slot in the same transaction;
   the cancellation window and any fee are policy values that the business owns and that the confirmation
   screen and email repeat in plain words. The policy in force at booking time is stored on the booking, so a
   later change does not rewrite old bookings. Not legal advice.
2. **Rescheduling is atomic.** Symptom: the old slot is freed, the new one is taken by someone else, and the
   customer ends with nothing. Fix: reserve the new slot first, then release the old one, in one
   transaction, keeping the booking id and a link to the previous time in its history; rescheduling by the
   provider notifies the customer and offers alternatives rather than moving silently.
3. **No-shows and waitlists.** A no-show is marked by staff after a grace period, never by a timer alone,
   and its consequences (fee, flag, deposit kept) follow the business policy. A waitlist is an ordered list per
   slot or day; on a release, offer the freed slot to the first entry with an expiring hold, and move on if
   it lapses. Symptom: a freed slot sold twice, to the waitlist and to the public. Fix: the offer is a hold.
4. **Calendar sync has a source of truth.** Symptom: duplicates, or an external edit silently deleting a
   booking. Fix: decide whether the application or the external calendar owns each booking; store the
   external event id and a sync token or etag; import external busy time as blocks without details;
   push changes through a queued job with an idempotency key; handle the external system's own zone
   representation on the way in; show a failed push to a person. Invitations carry a stable event id so an
   update replaces rather than duplicates, and a cancel sends a cancel.
5. **Reminders are scheduled from the stored time.** Symptom: reminders at the wrong hour after a clock change
   or after a reschedule. Fix: compute the send instant from the booking's instant at schedule time, store the
   reminder rows with their own state, recompute them on reschedule, cancel them on cancel, and send in the
   recipient's zone and language. A reminder job is idempotent (see `skills/laravel-idempotent-jobs`) and goes
   out through notifications (see `skills/laravel-mail-via-notifications`). Consent for channels such as text
   messages is checked before sending.
6. **Roles and visibility.** Customer (own bookings), provider (own calendar), front desk (all bookings for a
   location), manager (policies, reports), admin. Abilities: create on behalf of a customer, override a rule
   such as lead time, cancel others' bookings, see customer contact data, export. Symptom: a provider sees
   another provider's customers. Fix: scope every query by tenant, location and resource (see
   `skills/laravel-tenant-context-by-default`), name abilities as permissions (see
   `skills/laravel-permissions-not-roles`), and log every override.
7. **Payments sit at the boundary.** A deposit or full payment is a separate record linked to the booking; the
   booking is confirmed only when the payment provider's confirmed event arrives, handled idempotently;
   an expired hold with a pending payment is reconciled, not ignored. Amounts follow
   `skills/money-arithmetic-and-rounding-pitfalls`; refunds follow the business policy, not this block.
8. **What to split first.** Order: resource, service and zone model; availability rules and exceptions; the
   slot function and the conflict-safe reservation with its parallel test; holds with expiry; cancel and
   reschedule with states; reminders; roles; calendar sync; waitlists; payments; recurrence editing. Ship the
   zone, clock-change and double-booking tests before any integration.
9. **What is regretted at v2.** Local times stored as UTC only, or UTC offsets stored as zones; slots generated
   in the browser; availability checked then inserted; holds with no expiry; cancel as delete; one global
   time zone for the whole product; recurrence stored as copies instead of a rule; no policy snapshot on the
   booking; calendar sync with no external id; capacity hard-coded to one. Each is cheap in the first
   migration and costly after bookings exist.
10. **Laravel and Nuxt pointers, short.** In Laravel: a range type or a unique constraint with a transactional
    insert for conflicts, row locks on resources, a scheduled command to release expired holds (see
    `skills/laravel-scheduling`), queued sync and reminder jobs with idempotency keys, dates cast to the
    application zone only at the edge (see `skills/laravel-date-via-localised-accessors`), and fixed test
    dates. In Nuxt: format with the zone the server returned, show the zone name next to every time, treat the
    slot list as stale and handle "no longer available" on confirm, and never compute availability in the client.
