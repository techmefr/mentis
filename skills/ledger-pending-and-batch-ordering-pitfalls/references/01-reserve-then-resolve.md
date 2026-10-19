# ledger-pending-and-batch-ordering-pitfalls §1 — Reserve, then resolve

> Section 1 of `skills/ledger-pending-and-batch-ordering-pitfalls`. Read it when funds are held before they
> move. Sourced from the TigerBeetle documentation (commit `0450c32`), page `docs/coding/two-phase-transfers.md`,
> read 2026-10-16. Field and error names belong to that engine and are not used here. Sentences marked "own
> guidance" are ours.

1. **A pending entry holds funds without posting them.** The source describes a reservation that is recorded
   in separate "pending" totals on both accounts and leaves the posted totals untouched. Model it the same
   way: a hold is its own state, visible to the availability check and invisible to the posted balance.
2. **Resolve it exactly once, by one of three outcomes.** The reservation is posted, voided, or expires. A
   post may move all of the held amount or only part of it; when only part is posted, the remainder returns to
   the original accounts. Posting more than was held is an error, not a silent cap.
3. **A second resolution is an error, not a no-op.** The source returns a distinct error for "already
   posted", "already voided" and "expired", and says a reservation can be resolved once: not twice, and not
   void-then-post. Own guidance: keep the three outcomes distinguishable in your own model so a retry can tell
   a duplicate from a conflict.
4. **Resolving never edits the held entry.** The source says completing a two-step movement creates a new
   movement that points at the first one by its id; the first stays as written and the second has its own id.
   This is the append-only rule of the main ledger block applied to holds.
5. **Check the balance rule when the hold is made.** The documentation says the second step can never break
   an account's balance rule, whether it is a post or a void, because the amount was reserved up front. Its
   worked case: an account that may not go below zero fails the reservation itself when the pending amounts
   would push it under, without waiting for the post. Own guidance: count holds against what is available, or
   two concurrent reservations can each pass a check that their sum would fail.
6. **Expiry is an interval, not a clock time.** The source gives a reservation an optional timeout expressed
   as a number of seconds from creation, not as an absolute timestamp, and points to its page on time for the
   reasoning. Own guidance: when you build your own, prefer the interval for the same reason (a clock that
   disagrees between nodes should not change which holds are alive), and say who releases an expired hold.
7. **A hold is not a payment outcome.** Own guidance: a reservation that was never resolved is an open item
   to age and chase, not a final state; the payment-operations rules for unknown outcomes are in
   `business/fintech-compliance` part 4.
8. **What not to carry.** Which accounting treatment a held amount receives, and how long a hold may last in
   a given payment scheme, are not in this source and were not read; send both to an accountant or to the
   scheme's own rules.
