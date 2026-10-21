# booking-and-scheduling-app-pitfalls: origin and source stamps

> Provenance of `skills/booking-and-scheduling-app-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against the iCalendar standard and the IANA time zone database notes. Never run by us: no application was built and no test was executed.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: applicability gate for rule-only schedules, concrete clock-change test set per zone, offline device-clock evaluation check.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | RFC 5545, "Internet Calendaring and Scheduling Core Object Specification (iCalendar)" (IETF, 2009): DATE-TIME forms (section 3.3.5), recurrence rule handling of nonexistent and repeated local times (section 3.3.10), recurrence identifier and range (section 3.8.4.4), exception dates, sequence number (section 3.8.7.4), unique identifier | IETF standard text, read for facts only and restated; no sentence copied | Floating, UTC and zone-referenced times, the default for gaps and repeats, instance identity, this-and-future range, versioning of an invitation |
| 2 | IANA time zone database, "Theory and pragmatics of the tz code and data" (`data.iana.org/time-zones/theory.html`) | Documentation of a standards body, no licence file read: facts only, rewritten | Region-based zone names, recorded transitions and predicted future, ambiguity of abbreviations |
| 3 | PostgreSQL manual, pages "Range Types" (`postgresql.org/docs/current/rangetypes.html`) and "CREATE TABLE" (`sql-createtable.html`), 18 series | Documentation of an open-source project under the PostgreSQL licence (licence text not read here): facts only, rewritten | Exclusion constraint with overlap operator and GiST prevents overlapping ranges, btree_gist for equality on a scalar column, unique unsuitable for ranges, deferrable constraints cannot arbitrate a conflict clause |

Neighbouring blocks of this repository were read to avoid duplication: `skills/python-patching-and-time-pitfalls`
and `skills/dotnet-testcontainers-and-time-seam-pitfalls` (time in tests), `skills/laravel-date-via-localised-accessors`
(date display), `skills/laravel-scheduling`, `skills/laravel-idempotent-jobs`, `skills/inventory-stock-app-pitfalls`
(concurrent decrements). None covers designing a booking application, so a new block was justified.

## Verified
1. §1 points 1 to 4, §2 point 4: backed by the sources above, as the points now say.
2. §1 point 6, the database constraint for overlapping ranges (PostgreSQL exclusion constraint): source 3 (second pass).
3. The "state what happens in a gap" rule of §1 point 3 now cites the standard's default (offset before the gap).

## Added
1. §1 point 12, calendar export with a bare local time, shown by source 1.

## Removed
1. **Cancellation fees, refund rules and no-show penalties:** not read; flagged as business policy, not legal advice.
2. **Every numeric value** (hold lifetime, lead time, grace period, buffers): set by policy.
3. **Named calendar and booking products and their APIs:** not used.

## Not verified
1. **Still our own guidance:** the conflict-safe reservation and holds (§1 points 5 to 9; the range-constraint remark in point 6 is sourced, the rest of the point is not), rule-only schedules and offline
   evaluation (points 10 and 11, from a dogfood read, not from a source), the spring and autumn dates quoted in point 3
   (the block already says to re-check them), and in §2 cancellation, rescheduling, no-show and waitlist, reminders, roles,
   payments, build order and v2 regrets.
2. **Current zone database release and any recent rule change** were not re-read; rules change by decree.
3. **Nothing was run.** The zone, clock-change, double-booking and hold-expiry tests named in the checkpoint
   were not written or executed.
4. **Framework pointers and row locks** were not checked against a current release; the DST dates of point 3 (EU and US) could not be re-read, the official EU text returned no content;
   re-read before relying.

## Second pass, strict re-read (2026-10-21)

Re-opened: RFC 5545 full text (sections 3.3.5, 3.3.10, 3.8.2.2, 3.8.4.4, 3.8.5.1, 3.8.7.4, 3.8.4.7), IANA tz
"Theory and pragmatics" page, PostgreSQL "Range Types" and "CREATE TABLE" pages, PostgreSQL "Sequence Manipulation
Functions", 15 U.S.C. section 260a (Cornell LII).
- Confirmed: floating, UTC and TZID forms with "floating time SHOULD only be used where that is reasonable" (3.3.5); a
  repeated local time is the first occurrence and a nonexistent one uses the offset before the gap, with the 02:30 to 03:30
  New York example (3.3.5); recurrence start times that do not exist or repeat are read that way (3.3.10); RECURRENCE-ID
  names the instance by its original start and THISANDFUTURE reschedules later instances by the same difference
  (3.8.4.4); SEQUENCE starts at 0 and the organiser increments it on a significant revision (3.8.7.4, descriptive, no
  keyword); UID must be globally unique (3.8.4.7); exclusion constraint with GiST on a range, UNIQUE usually unsuitable,
  btree_gist for scalar equality, deferrable constraints cannot arbitrate ON CONFLICT; IANA region names and ambiguous
  abbreviations (CST for Central and for China); US change at 2 a.m. second Sunday of March to first Sunday of November.
- Corrected: section 3.3.10 also says instances generated by a rule with a nonexistent local time MUST be ignored and not
  counted, so the standard is not uniform for a series that crosses the gap; the block now says to choose, document and
  test one behaviour, and carries section numbers.
- Still unverified: the European change dates (the official text could not be retrieved); the rest of the block.
Counts: 14 claims re-checked, 1 corrected.

## Related blocks
`skills/helpdesk-ticketing-app-build-pitfalls`, `skills/hr-leave-and-time-tracking-app-pitfalls`,
`skills/inventory-stock-app-pitfalls`, `skills/python-patching-and-time-pitfalls`,
`skills/laravel-date-via-localised-accessors`, `skills/laravel-scheduling`.
