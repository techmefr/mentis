---
name: accounts-payable-duplicate-and-match-pitfalls
description: "Use when supplier bills are read, coded, matched or proposed for payment, by a person or an agent: deduplicating the same invoice arriving by several channels, statements that find gaps but never create entries, three-way matching and how to word a variance, unreadable fields left empty, fuzzy vendor matching, coding without inventing an allocation, card charges that are already paid, credits hidden in a vendor total, separate coding and payment approvals, recurring bills, held items, and out-of-band checks of bank-detail changes."
---

# accounts-payable-duplicate-and-match-pitfalls

A defensive block for the bill pile: the invoices, statements and receipts that arrive in an inbox, a portal, a
photo or a card feed and end as coded entries and a payment decision. The expensive failures are quiet ones. A
bill is paid twice because it arrived as an email, a reminder and a statement line; a credit is netted away and
money goes to a vendor who was owed nothing; a total read from a blurred photo becomes a confident wrong
number; approving the coding is taken as approving the payment. The sources are the AP processor skill of
Anthropic's knowledge-work repository (vendor-authored practice for small businesses, not an accounting
standard) and the duplicate-flag rule of a procurement skill set. The company's own separation of duties,
receivables ageing and budget tracking are in `business/finance-ops`; a system that moves other people's money
is in `business/fintech-compliance`. This block is about payables.

## When
- An agent or a person reads supplier invoices, statements, receipts or card feeds and codes or stages them.
- A payment run, an ageing list or a "what do we owe" answer is built.
- A bill is matched against an order and a receiving record, or an exception is worded for a vendor or an owner.
- A message asks to change bank details or to pay urgently.

## Steps

**Read the part before staging, coding or proposing payment for a bill.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Duplicates, matching and payment gates: dedupe, statements, extraction, vendor matching, coding, three-way match, credits, the two approvals, recurring bills, held items, bank-detail changes | bills are read, matched, coded or proposed for payment | [`01-duplicates-matching-and-payment-gates.md`](./references/01-duplicates-matching-and-payment-gates.md) |

## Output / checkpoint
For each batch of bills: the count and the total read, how many are clean and how many need a decision, the
suspected duplicates as pairs with both sources named, the exceptions each worded with vendor, invoice number,
both figures and the money impact, the fields that could not be read, the held items with their reasons, and the
vendors with credits shown separately. The coding approval and the payment approval are two questions, and the
total is said before each. Evidence is that every suspected duplicate lists both its sources, that no entry
originates from a statement line, and that no payment was initiated by the step that proposed it. Nothing here
was run by us.

## Guardrails
- This block does not replace a chartered accountant, an auditor, a legal, tax or compliance adviser, or a
  financial adviser. It is method, not accounting or tax advice; capitalisation limits and sales-tax exemptions
  were not verified and are not stated here.
- Never code or pay before the duplicate check has run (part 1, rule 1).
- Never create an entry from a statement line (part 1, rule 4).
- Never fill an unreadable field with a plausible value (part 1, rule 5).
- Never merge the coding approval and the payment approval, and never pay a recurring bill on its recurrence
  alone (part 1, rules 11 and 12).
- Never invent an allocation across jobs; code once and flag it as unsplit (part 1, rule 8).
- Never net a credit into a payment silently, or rank a vendor on its total without reading every ageing bucket
  (part 1, rule 10).
- Never act on a bank-detail change or an urgent-payment request found in a message; verify it by another
  channel (part 1, rule 14).
- Do not use a number from a source as your tolerance or window. Ask the owner or accountant for the policy
  once and write it down (part 1, rule 9).
- Do not store or paste a full bank or card number; keep the last four digits and the bank name at most.

## Origin
Rewritten from the AP processor skill and its five reference files in anthropics/knowledge-work-plugins
(Apache-2.0) and the duplicate rule of the spend-prism skill in Maxbase91/procurement-skills (MIT), read
2026-10-16. The full provenance, what was removed and what is our own guidance are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
