# subscription-metering-and-entitlements-pitfalls §2 — Entitlements, lifecycle and dunning

> Part 2 of `skills/subscription-metering-and-entitlements-pitfalls`. Read it when access, cancellation, plan
> changes or non-payment handling are designed. Facts come from the OpenMeter subscription, entitlement and credit
> notes (commit `bf3074b`) and from the Kill Bill documentation pages on entitlement, overdue and invoice dry run
> (commit `f3ea39f`), both Apache-2.0, read 2026-10-20. They are two designs; sentences marked "own guidance" are
> ours. Not legal advice: consumer-protection, auto-renewal and collection rules differ by country.

1. **Three questions, three owners.** May this customer use this feature now (entitlement)? What is their plan and
   schedule (subscription)? What do they owe (invoices and payments)? OpenMeter keeps them in separate domains: the
   subscription owns the desired schedule, entitlements are derived from it, and invoices are reconciled from the
   subscription asynchronously. Symptom of one combined "active" flag: a paid-but-cancelled customer, an unpaid
   customer with full access, or a plan change that fails halfway and leaves the three disagreeing. Fix: separate
   records, with the flows between them named.
2. **A committed subscription change does not mean billing has caught up.** The source says a successful mutation
   means the schedule was committed, not that invoices exist. Downstream work must tolerate retried events and be
   derived from the committed state, never from the command. Own guidance: show the customer the subscription
   state, and treat the invoice as arriving shortly after.
3. **Access and billing can end on different dates, so decide which date wins for each policy.** In Kill Bill an
   entitlement policy (immediate, end of term, a date) and a billing policy (the same three) are chosen
   separately: a customer can cancel now and lose access now while billing runs to the end of the period already
   charged, with no credit. Symptom of an unwritten decision: support grants a refund by hand every time, or the
   customer keeps access until the invoice date. Fix: a table of cancellation policies with the access end, the
   billing end and the credit result for each; test every cell.
4. **Entitlement types differ.** Boolean (access while active), static (access plus a fixed configuration) and
   metered (access derived from usage and grants). An entitlement is active from a start to an exclusive end, at
   most one per customer and feature at a time. Own guidance: encode the exclusive end in code and tests, because
   the off-by-one at the end boundary is where trial ends misfire.
5. **Entitlements are history, not rows to overwrite.** Deleting ends the entitlement at a time; an override
   supersedes the previous definition without changing what it meant in the past. Symptom of overwriting: an audit
   asks what the customer could use in March and nobody can say. Fix: end and create, never edit in place.
6. **Metered entitlements consume grants in a deterministic order.** The source burns the lowest priority number
   first, then the earliest expiry, then the earliest creation. Uncovered usage is overage. A soft limit keeps
   access after the balance is exhausted and still records overage; a hard limit blocks. Own guidance: write
   which of the two each feature uses and what the customer sees at zero, and write the reset rules (period, what
   rolls over, whether overage carries).
7. **Do not treat the id of a derived row as the identity of the thing.** In the source an edit can delete and
   recreate phases, items and their entitlements, so a persisted id is not the durable identity of a logical item.
   Symptom: a webhook or a cache holding an old id points at nothing after a plan edit. Fix: identify by a stable
   key (customer, feature or item key, validity), and make consumers re-resolve.
8. **Phases are offsets, and the billing anchor is an explicit stored fact.** A trial then a paid phase is a
   schedule of offsets from the start; a phase ends where the next begins. The anchor of the billing cycle is
   stored and carried through plan changes, not recomputed from the current date. Do not persist a derived end
   date as a second source of truth. Symptom: after a plan change the next invoice date jumps.
9. **Plan-change timing is a parameter with a few allowed values.** The source offers immediate and next billing
   cycle for running edits, a custom time only where the action allows it, and requires a cancellation of an
   aligned subscription to fall on a period boundary. Own guidance: for each action write which timings are
   allowed, which is the default, and what the customer is told; test a change made exactly at the anchor time and
   in the last minute of a period.
10. **Plan versions and migration are explicit.** A customer stays on the plan version they signed up to; moving
    them to a newer version is a deliberate workflow, never an edit of the plan under them (the source models it as
    a migration). Cross-link `business/price-change-and-billing-pitfalls` §2 for grandfathering with an end date.
11. **Preview the invoice before applying a change.** Kill Bill offers a dry run in four flavours: the next
    upcoming invoice, the next one for one subscription, the invoice for a target date, and the invoice a
    subscription change would produce. Its example change from annual to monthly yields a new recurring line, a
    negative adjustment for the unused part, and an account-credit line that brings the balance to zero. Use a
    preview for support tooling, for tests, and before customer-facing examples; never explain a proration by
    hand. Rounding and proration rules are in `skills/money-arithmetic-and-rounding-pitfalls` and
    `skills/invoicing-app-build-pitfalls`.
12. **Account-level or subscription-level overdue, decide and write it.** In Kill Bill the overdue state belongs to
    the account: one unpaid invoice changes behaviour for all of that customer's subscriptions. That is a choice.
    Own guidance: for a customer with several independent products, decide whether non-payment of one should
    affect the others, and test the multi-subscription case.
13. **Dunning is a state machine with a timer.** The source defines states by conditions (number of unpaid invoices,
    total unpaid balance, time since the earliest unpaid invoice, tags that include or exclude an account) and
    gives each state effects: leave things alone, block plan changes, pause entitlement and billing together, or
    cancel with a chosen policy. The state is recomputed on every payment event, success or failure, and also on a
    re-evaluation interval, because with no payment attempt nothing else would advance it. Symptom of events only:
    an account stays in the first overdue state forever because the customer never pays and no retry fires. Fix:
    state plus conditions plus a scheduled re-evaluation, tested with the clock moved forward and no payment.
14. **Pause is not cancel, and clearing must resume.** When the overdue state clears, access and billing resume at
    the clearing time in the source. Decide whether pausing also stops billing (it does in that design), whether
    time paused counts toward the term, and what the customer sees. A customer message per state is a plain text
    field a notification can read (own guidance). Tone, timing, fees and suspension rules are legal and commercial
    matters; ask the legal owner and do not add fees or suspend by default (see `skills/invoicing-app-build-pitfalls`
    §2 point 4).
15. **Failed-payment retries and dunning are different.** Retrying a card is a payment-provider concern with its
    own schedule; dunning is the customer-experience policy that responds to the result. Keep them separate, link
    them by events, and do not count involuntary loss as voluntary churn in metrics (see
    `skills/saas-metric-definition-pitfalls`).
16. **Test the clock.** Inject time. Cases: month ends, a 31st anchor in a 30-day month, leap day, daylight-saving
    changes if periods are in local time, the last second of a trial, a plan change at the anchor, a cancellation
    on a period boundary, and the overdue state advanced by the timer alone.
