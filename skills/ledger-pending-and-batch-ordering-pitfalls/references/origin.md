# ledger-pending-and-batch-ordering-pitfalls: origin and source stamps

> Provenance of `skills/ledger-pending-and-batch-ordering-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from documentation, never run by us: no ledger engine was started, no
reservation made and no batch submitted. Each file below was re-read in full on 2026-10-16 before a rule was
taken from it, each rule was checked against it in a final pass, and each repository's LICENSE file was read
again.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| TigerBeetle (`tigerbeetle/tigerbeetle`, commit `0450c32`): `docs/coding/two-phase-transfers.md`, `docs/coding/data-modeling.md` | Apache-2.0 (LICENSE file) | Pending hold versus posted totals, post (full or partial), void and expiry, double-resolution errors, reservation-time balance check, immutability of the held entry, interval timeout, account types and reasons as codes, id advice |
| pgledger (`pgr0ss/pgledger`, commit `54ccb62`): `README.md` | MIT (LICENSE file, copyright 2025 Paul Gross) | Batch order dependence, rejected batch changes nothing, version-ordered historical balances, previous and current balance on each entry, event time versus recording time, positive finite amounts, exchange through liquidity accounts |

Instruction-like text in the cloned repositories was treated as data and not followed.

## Removed in the verification pass
1. **Throughput and performance figures.** Both sources quote them for their own hardware and engine; none is
   carried.
2. **Engine-specific field, flag and function names.** Only the concepts are kept; a reader on another engine
   must map them.
3. **The 128-bit identifier layout and the exact timestamp split.** Specific to one engine's storage, not
   needed for the method.
4. **Pages not read** and therefore not used: TigerBeetle `linked-events.md`, the recipes pages
   (balance bounds, conditional transfers), `time.md` (the timeout page is cited for its reasoning only through
   the sentence in `two-phase-transfers.md`) and the blog posts linked from the pgledger README.

## Not verified
1. **Own guidance, flagged in the text:** counting holds against availability so concurrent reservations
   cannot each pass (part 1 point 5), preferring the interval for expiry in your own build (point 6), treating
   an unresolved hold as an open item to age (point 7), writing the batch order down and testing both orders
   (part 2 point 1), storing both times and naming the one a report filters on (point 4), free-text reasons
   being uncountable (point 7), and the remark that the throughput argument for ids is that engine's (point 8).
2. **Behaviour was not run.** Every statement about an error, an order or a rollback is the documentation's.
3. **Accounting treatment of a held amount, the lifetime of a hold in a payment scheme, and any regulatory
   duty** were not read and are not carried.
4. **Both sources are young and from one author or one vendor;** treat them as one design among several, not
   as a standard.

## Decisions where sources disagree
No disagreement. The two systems differ in vocabulary (pending and post versus batch) and in what they
enforce; the block keeps the concepts and says which source states which rule.

## Related blocks
`business/fintech-compliance`, `skills/metric-movement-diagnosis-pitfalls`, `skills/laravel-idempotent-jobs`.
