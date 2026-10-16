# ledger-pending-and-batch-ordering-pitfalls §2 — Batches, history and identifiers

> Section 2 of `skills/ledger-pending-and-batch-ordering-pitfalls`. Read it when movements are batched,
> balances are read back in time, or the schema is being designed. Sourced from the pgledger README (commit
> `54ccb62`, sections on batch ordering, historical balances, event timestamp and IDs) and the TigerBeetle
> page `docs/coding/data-modeling.md` (commit `0450c32`), read 2026-10-16. Sentences marked "own guidance" are
> ours.

1. **Inside a batch, order matters.** The pgledger README says its batch call applies the requests in array
   order and checks each account's balance constraints after each request, not at the end. Its example: an
   account that may not go negative accepts "money in, then money out" and rejects the reverse order of the
   same two requests. Own guidance: write the order down, test both orders, and never let a caller assume the
   set is evaluated as a whole.
2. **A rejected batch changes nothing.** The same README states that a rejected call leaves the ledger
   unchanged, so none of its movements or entries are recorded. This is the all-or-nothing unit from the main
   ledger block, applied to a batch.
3. **Read a past balance by version, not by creation time.** Each entry stores the account's previous and
   current balance. To find the balance at a past moment, take the latest entry before it, ordered by the
   account's own version number, because every entry written by one batch call shares one creation time and
   an account touched twice in the batch would otherwise be ambiguous.
4. **Keep the event time apart from the recording time.** The README says a movement can carry the time the
   real-world event happened, defaulting to the recording time. Its example: a bank webhook received just after
   midnight about money that arrived shortly before midnight belongs to the earlier month on the bank
   statement, so matching the statement means filtering on the event time. Own guidance: store both, and say in
   every report which one it filters on.
5. **Reject degenerate amounts; direction comes from the accounts.** A movement amount must be positive and
   finite: zero, negative, null, not-a-number and infinite values are rejected, and the direction is given by
   which account is debited and which is credited, not by the sign.
6. **One currency per account; exchange through a liquidity account per currency.** The README says an
   exchange between two currencies uses four accounts, including one system account for each currency, as two
   movements created together, so each currency still nets to zero.
7. **Fix account types and entry reasons as codes up front.** The TigerBeetle page suggests listing every
   known account type and every kind of movement and giving each a code (or range) before building. Own
   guidance: a reason that exists only as free text cannot be counted, reconciled or reported on.
8. **Generate identifiers without a central counter, ordered by time.** The same page advises against needing
   a central source for each new id (a counter becomes a bottleneck), against random ids for throughput
   reasons, and for time-ordered ids that sort lexicographically and collide with negligible probability; an
   id is also the idempotency key for a retried write. Own guidance: that throughput argument is that
   engine's; for a SQL ledger the lasting reasons are no counter on the hot path and ids that sort by time.
