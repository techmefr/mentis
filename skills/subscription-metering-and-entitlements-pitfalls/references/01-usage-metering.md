# subscription-metering-and-entitlements-pitfalls §1 — Usage metering

> Part 1 of `skills/subscription-metering-and-entitlements-pitfalls`. Read it when a usage pipeline or a
> usage-based price is designed or debugged. Facts come from the OpenMeter repository's event-ingestion,
> credit and entitlement notes (commit `bf3074b`) and from the Kill Bill documentation page on usage invoice items
> (commit `f3ea39f`), both Apache-2.0, read 2026-10-20. They are two designs; sentences marked "own guidance" are
> ours. Retention periods, window sizes and tier figures in the sources are their settings, not rules.

1. **Every usage event has an identity, and a producer may send it twice.** The metering platform follows the
   CloudEvents convention that the pair of source and id is unique per distinct event and that a re-sent event may
   carry the same id; its pipeline ignores a repeat of a known pair. Symptom of missing identity: a network retry
   or a replayed queue bills the customer twice. Fix: the producer creates the id once, before the first send, and
   reuses it on every retry (see `skills/laravel-idempotent-jobs`).
2. **Remember identities longer than any producer retries or replays.** The platform's duplicate memory is a fixed
   window by default (re-read the figure before relying on it). A replay of last month's events after the window
   has passed is not a duplicate any more. Own guidance: set the window from the longest backfill or retry you
   allow, write it next to the producer contract, and alert when an event older than the window arrives.
3. **Meter on event time, not ingest time.** The event carries the time it happened; windows are cut on that time.
   Symptom of cutting on arrival: a delayed batch lands in the wrong month and a customer is billed for usage that
   belongs to the previous period.
4. **Late usage needs a written policy, because the invoice for the period may already exist.** Kill Bill
   recomputes a bounded number of previous periods each time it invoices and bills the difference as an extra item;
   usage older than that is ignored, and deleting usage inside the bounded range is an error that blocks
   invoicing. Both rules are the engine's choices. Own guidance: pick one explicit policy (bill a delta on the next
   invoice, credit it, or drop it with a counted and alerted record), never put it into an issued invoice (see
   `skills/invoicing-app-build-pitfalls` §2 point 2), and never delete raw usage inside a billed period.
5. **Attribution is a mapping with dates, not a field on the event.** The event names a subject; the platform
   resolves which customer that subject belongs to when it queries. Symptom of a hard link: a subject moves to
   another customer and the history moves with it. Own guidance: store the subject-to-customer mapping with a start
   and an end, resolve with the event time, and do not rewrite the past when the mapping changes.
6. **The meter is the price metric made executable.** A meter names the event type, the path to the value, the
   aggregation (sum, count, maximum, latest, unique count) and the grouping dimensions. The aggregation must match
   what the price says: a "peak concurrent jobs" price needs a maximum, not a sum; "active users" needs a unique
   count; "storage used" needs a latest or time-weighted value. Symptom of the wrong one: invoices that are
   internally consistent and commercially wrong. Fix: write the price metric in a sentence, derive the aggregation
   from it, and test with a small event set by hand.
7. **Bound the grouping dimensions.** Each combination of subject and dimension values is a row to store and a
   line to explain. Own guidance: group only by what the price or the customer's report needs, and refuse
   free-text values.
8. **Validate at ingest, and make rejection visible.** The value is often delivered as text; a non-numeric,
   negative or out-of-range value must be rejected with a stored reason, not dropped or coerced to zero. Own
   guidance: a counter of rejected events per producer, shown to whoever owns the producer.
9. **Balances and credit are derived state, not money.** The platform computes a balance from grants and usage and
   keeps snapshots only as a cache: removing snapshots, or adding an earlier one, must not change the answer, and
   any change to a grant, a reset or a usage input must invalidate the snapshots it affects and all later ones.
   Late events matter here too, so snapshots are kept behind a grace window. Treat feature credit as an access
   measure, never as currency (the engine says the same). Fix for a stale balance: delete the cache and recompute
   from the inputs; if that changes the answer, the invalidation was wrong.
10. **Resolution is a promise.** The platform's metering and credit run on one-minute windows, so nothing may rely
    on ordering or on a balance change inside the same minute, and a read at a sub-minute time rounds up. Own
    guidance: state the resolution of your meters in the product, and do not promise instant cut-off at a quota
    unless the pipeline can deliver it.
11. **Tier names mean two different things; test the boundaries.** In Kill Bill, with an all-tier policy each tier's
    quantity is charged at that tier's price; with a top-tier policy all quantity is charged at the highest tier
    reached. A capacity type charges a fixed price for the highest tier reached. Other vendors call these
    graduated and volume. Symptom: the invoice disagrees with the pricing page at exactly the tier edge. Fix: write
    the tier rule with a worked example on the pricing page, then unit-test the quantities just below, at and just
    above each boundary, and a quantity of zero.
12. **Usage is billed after the period and fixed fees before it.** An invoice mixing both has two rhythms; the
    customer needs both explained (see `business/price-change-and-billing-pitfalls` §5.3). Do not prorate usage.
13. **Do not meter in the request path.** Own guidance: emit the event through a queue or an outbox and keep the
    user-facing call independent of the metering pipeline. Decide on purpose whether a metering outage lets users
    continue (fail open, reconcile later) or blocks them (fail closed); the choice is commercial and goes in the
    contract.
14. **Reconcile the three counts.** Events accepted, rows aggregated per window, quantity on the invoice line.
    Raw events are kept with their ids so a dispute can be recomputed. When a bug was found in a producer, replay
    the corrected events under the same ids where possible and issue adjustments (credit notes) for invoices
    already sent, never edits.
