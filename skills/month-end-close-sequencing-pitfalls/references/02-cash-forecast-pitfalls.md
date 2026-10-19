# month-end-close-sequencing-pitfalls §2 — Cash forecast pitfalls

> Section 2 of `skills/month-end-close-sequencing-pitfalls`. Read it when a short-term cash forecast is built
> or checked. Sourced from the cash-flow-snapshot skill of anthropics' knowledge-work-plugins (commit
> `33eeda1`, `small-business/skills/cash-flow-snapshot/SKILL.md` and `reference/gotchas.md`), read 2026-10-16.
> Sentences marked "own guidance" are ours. A forecast is an estimate, not a promise.

1. **Never assume an opening balance.** The source's question "will I make payroll" is about the balance, not
   only the net movement. Take the balance from a source with its as-of date, or ask for it. If nobody knows
   it, head the output "no opening balance, net change only" and leave cash-on-hand out of the risks.
2. **Check where the balance comes from.** The source notes that one ledger product holds no bank or cash
   balances at all, so an opening balance must never be taken from it. Own guidance: for any ledger, confirm
   the balance field is a bank balance before using it.
3. **One source of record for totals.** If two ledgers are connected, ask which is the record and take the
   totals from that one only.
4. **Take receivables that are still owed.** The source warns that an ageing export can include invoices that
   are already collected and shows them as zero; keep only rows with a balance due.
5. **Use each payer's own payment lag.** Compute the delay between invoice and receipt for each customer from
   actual dates, and its spread across its recent payments, instead of one flat assumption for everyone. The
   source makes the same point for payment processors: settlement lag varies by transaction type, so take it
   from real transaction-to-settlement pairs.
6. **Build the range from observed spread.** Own guidance: express the low and high cases from the measured
   variation of each payer's lag, and say so. The source's own band formula (spread divided by average lag,
   capped, with a fixed fallback) was not checked and is not carried.
7. **Thin history is declared.** With too few payments from a payer, the source falls back to a population
   estimate and a default band and flags the thin data. Own guidance: label such a range as a default, not a
   measurement, and never present it with the same weight as one built from real history.
8. **Name the sources used.** The source says the sources behind the forecast affect how wide the range
   should be (for example a file upload with no live payables data gives less confidence). State them in the
   output.
9. **Fixed costs hide in one-off entries.** The source notes that rent and similar costs often appear as
   one-off vendor bills each month without a recurring tag; look for the same vendor and similar amount across
   consecutive months and ask the owner to confirm the list. Own guidance: confirm, do not assume.
10. **Confirm the data mapping before computing.** When a file's columns are ambiguous, show the header row
    and ask; one question beats a wrong forecast built silently.
11. **Name each risk.** A late payer with its invoice and the window it moves into; a payroll date with the
    low-case balance before it; thin data; a data source with limited visibility. The source limits the list to
    the largest few by impact; keep the list short enough to be read.
12. **State what the forecast is.** The source ends with a reminder that it is not a substitute for accounting
    advice. Own guidance: add that card spend not yet recorded is the most common reason a forecast is quietly
    optimistic (the source's own remark on one connector), and ask for it.
13. **Nothing here is financial advice.** A forecast informs a decision; a financing decision goes to a
    chartered accountant or financial adviser.
