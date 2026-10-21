---
name: agent-data-gap-honesty-pitfalls
description: "Use when an agent or an analyst reads data through connectors and reports figures, lists, schedules or times to someone who will act on them: a top-N or paginated call reported as a total, a summary object that contradicts its rows, a missing value read as zero or as fresh, a future date ranked as the newest, an empty result that was really a failed query, a ratio whose denominator comes from a wider universe, a promised recurrence with no scheduler behind it, a time whose offset contradicts its label, and a connected drive, mailbox or CRM that belongs to someone else: what to check before a number leaves, how to name a gap, and whose account a connector is signed into."
---

# agent-data-gap-honesty-pitfalls

A defensive block for the moment an agent turns what a connector returned into a sentence a person will act on.
Premise: **a hole in the data reads as good news unless the reader is told otherwise, and a figure that is true in
one place is carried into another where it is false**. Test fixtures are complete by construction, so these
failures appear only against real accounts. Null handling inside an analysis is `skills/analysis-validation-pitfalls`
(calculation traps); untrusted content and tool trust are `skills/agent-mcp-trust-pitfalls`; booking and calendar features in an
app are `skills/booking-and-scheduling-app-pitfalls`; this block is the agent-side rule set for reading and
reporting.

## When
- An agent summarises a ledger, a CRM, a mailbox, a store or a calendar for a person who will decide from it.
- A command chains several steps and one step's number feeds the next.
- An agent offers to repeat something weekly, or prints a time for an invitation, a brief or a booking.
- A connector the agent did not choose (a drive, a mailbox, a CRM) is about to be read.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Absent is not zero: slice versus total, summary versus rows, zero versus unknown, empty is not fresh, future dates, empty versus failed, disagreeing counts, naming a gap | a figure, a list or a "nothing found" is about to be reported | [`01-absent-is-not-zero.md`](./references/01-absent-is-not-zero.md) |
| 2 | Chain seams: the right denominator, recurrence with no scheduler, offsets against labels, a free-slot suggestion | a number crosses from one step to another, or a time or a schedule is promised | [`02-chain-seams.md`](./references/02-chain-seams.md) |
| 3 | Whose account this is: ownership of a connected store, search by name, no fallback to a document store, discarding a mismatched read, one record system, probing before calling an outage | a connector the user did not name is about to be read | [`03-whose-account-is-this.md`](./references/03-whose-account-is-this.md) |

## Output / checkpoint
Each reported figure says what it measured: the whole, a slice, or a sum of rows. Each "none", "zero" or "up to
date" has a second check beside it or is labelled unknown. Each rate names its numerator and denominator and the
universe of each. Each promised schedule names the thing that will run it, or is withdrawn. Each printed time
carries its zone. Before the first read of a connected store, the account it belongs to was compared with the
business the user named. Nothing here was run against a live connector by us.

## Guardrails
- Say that a number is a slice, and give the total from an unconstrained source or label the figure partial.
  Never present a top-N or one page as the whole (§1).
- Total the rows when a payload offers both a summary and its rows. Never trust a summary that was not
  reconciled with them (§1).
- Say "unknown" when zero is implausible. Never write a zero the data did not state (§1).
- Rank a missing date as the worst case and drop a future date to missing. Never let empty or impossible dates
  look fresh (§1).
- Cross-check an empty result with a second count before saying there is nothing. Never report a failed query as
  an empty business (§1).
- Compute each ratio against the base its numerator could reach, and name both. Never divide by a figure from a
  wider universe (§2).
- Say what runs and when, or offer a reminder the person controls. Never say "saved, runs every Monday" with no
  scheduler (§2).
- Trust the offset in a timestamp over a contradicting label, print the zone, and read the real events before
  offering a slot. Never infer the zone from a calendar default (§2).
- Confirm that a connected store belongs to the user before the first read and search by name. Never browse
  recent files or fall back to a document store when a data connector is missing (§3).
- This block is craft guidance from one small-business plugin set, never run by us; examples with figures are
  from that source's own test runs and are not independently checkable (see
  [`references/origin.md`](./references/origin.md)).

## Origin
Rewritten in our own words from the shared rules of a small-business assistant plugin set (Apache-2.0), read
2026-10-20. 🟡: never dogfooded; open points are in [`references/origin.md`](./references/origin.md).
