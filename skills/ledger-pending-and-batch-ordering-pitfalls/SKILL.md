---
name: ledger-pending-and-batch-ordering-pitfalls
description: "Use when code reserves money before it settles or writes several ledger movements in one batch: pending entries that hold funds without posting, post, void and expiry, resolving a reservation twice, order-dependent batch outcomes, historical balances read from the wrong ordering, event time versus recording time, previous and current balance stored on each entry, account types and entry reasons as codes, identifiers without a central counter."
---

# ledger-pending-and-batch-ordering-pitfalls

A defensive block for the part of a ledger that sits between "requested" and "settled". The basics of a
ledger (append-only, entries net to zero, never a float) are in `business/fintech-compliance` part 3 and are
not repeated; this block adds what goes wrong when funds are held first and moved later, when several
movements are written together, and when someone later asks "what was the balance on that day". It states
method only. It carries no currency amount, no time limit and no accounting treatment, and it does not
replace a chartered accountant, an auditor, or a legal, compliance or financial adviser.

## When
- A payment, order or transfer reserves funds first and settles them later (card authorisation, escrow,
  payout hold).
- Several ledger movements are submitted in one call or one transaction.
- A report, a statement match or a month-end figure needs the balance of an account at a past moment.
- Account types, entry reasons or identifiers are being designed for a new ledger.

## Steps

**Read only the part the diff touches.**

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Reserve, then resolve: pending entry, post, void, expiry, double resolution, reservation-time balance check | funds are held before they move | [`01-reserve-then-resolve.md`](./references/01-reserve-then-resolve.md) |
| 2 | Batches, history and identifiers: order dependence, all-or-nothing batches, version-ordered balances, event versus recording time, codes, ids | movements are batched, balances are read back in time, or the schema is being designed | [`02-batches-history-identifiers.md`](./references/02-batches-history-identifiers.md) |

## Output / checkpoint
For each reservation or batch in the diff: where the funds are held while pending, what resolves the
reservation and what happens to the part that is not posted, what a second resolution does, whether the
balance rule is checked when the hold is made, and, for a batch, which order the requests run in and what is
recorded when one is rejected. Evidence is a test that resolves one reservation twice and sees an error, a
test that runs the same batch in two orders and sees the difference, and a test that reads a historical
balance on a day with several movements. Nothing here was run against a real ledger: the check is a read of
the text and of your own tests.

## Guardrails
- Never let a pending hold change a posted balance, and never let the second step of a two-step movement be
  the place where the balance rule is first checked (part 1).
- Never treat resolving a reservation twice as a harmless repeat: it is an error to surface (part 1).
- Never assume a batch is order-independent, and never record half of a rejected batch (part 2).
- Never read a past balance by ordering on a timestamp that a whole batch shares (part 2).
- Never match a ledger against a bank statement on the recording date when the statement uses the event date
  (part 2).
- Never draw a unique id from a central counter on the hot path (part 2).
- This block does not replace a chartered accountant, an auditor, or a legal, compliance or financial
  adviser; how a held amount is reported in the books is theirs to decide.

## Origin
Rewritten from the TigerBeetle documentation (Apache-2.0) and the pgledger README (MIT), read 2026-10-16.
Both are one author's or one vendor's design, not a standard. 🟡: never run by us; the full provenance and
what was removed are in [`references/origin.md`](./references/origin.md).
