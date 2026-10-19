---
name: vat-handling-in-software-pitfalls
description: "Use when building, changing or reviewing billing, checkout, subscriptions or invoicing code that computes, stores or prints VAT: deciding what must be data rather than constants, how the customer's status and country feed the tax decision, what is recorded per transaction, what an invoice must carry, how rounding and credit notes interact with the tax, and which questions go to the tax adviser."
---

# vat-handling-in-software-pitfalls

A defensive block for the engineers who build the money path of a product sold in the European Union: where VAT
logic lives in code, what it depends on, what is kept as evidence, and who decides what the code cannot. The
failures are mechanical: a rate written as a constant, a country read from a billing form and trusted, a business
customer treated as a consumer because the tax number was never checked, an invoice missing a mandatory mention,
a rounding rule chosen by the first developer, a refund that rewrites the original instead of amending it, a rule
guessed for a case nobody asked the adviser about.
The legal text read for this block is Council Directive 2006/112/EC on the common system of value added tax, in the
consolidated version of 01.01.2025 as shown by EUR-Lex, read 2026-10-19. It is the Union framework: national law
transposes it with options, and the national rule is what applies. Every statement of law below is marked "re-read
before relying", and no rate or threshold is given from memory. Whether a supply is taxable, where, at what rate,
who accounts for the tax and which scheme applies are decisions for the tax adviser and the national tax authority,
never for this block or for an engineer alone. For the rounding mechanics see
`skills/money-arithmetic-and-rounding-pitfalls`; for the finance function and compliance around payments see
`business/finance-ops` and `business/fintech-compliance`; for checking that a source is still current see
`skills/source-freshness`. This block is a working method, not tax advice.

## When
- A product starts selling to customers in more than one country, or a new country, product type or customer type
  appears.
- Code computes a tax amount, stores a rate, validates a tax number or generates an invoice or credit note.
- A checkout, a subscription renewal or a marketplace flow is designed or reviewed.
- An invoice template, a numbering scheme or a refund flow changes.

## Steps

**Read only the part the task meets.** Part 2 first for a new market; part 4 first for an invoice change.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | What must be data, not constants: rate per country, per product class, per date, and the tax decision as a function | a rate, a tax code or a product class appears in code | [`01-data-not-constants.md`](./references/01-data-not-constants.md) |
| 2 | Place of supply and customer status: business or not, goods or services, digital services, the questions to ask | a new market, a new product type, a B2B feature | [`02-place-of-supply-and-customer-status.md`](./references/02-place-of-supply-and-customer-status.md) |
| 3 | The record per transaction: status, tax number check, country evidence, rate, date | the order or payment model is designed or audited | [`03-record-per-transaction.md`](./references/03-record-per-transaction.md) |
| 4 | Invoice content: the mandatory details, simplified invoices, numbering, storage, electronic form | an invoice or credit note template changes | [`04-invoice-content.md`](./references/04-invoice-content.md) |
| 5 | Amounts, rounding, refunds and credit notes, and the escalation list | an amount is computed, a refund flow built, or a case is unclear | [`05-amounts-refunds-and-escalation.md`](./references/05-amounts-refunds-and-escalation.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). For each change under review: the tax decision inputs (customer status,
country evidence, product class, date), where each value lives in the data model, the open questions with a named
owner, and the adviser's answer with its date. For a process: one dummy order traced from checkout to invoice to
credit note, each tax value shown with its source. Every output ends with: not tax advice, escalate to the tax
adviser.

## Guardrails
- Not tax advice. This block does not replace the tax adviser or the national tax authority; escalate before a
  sale in a new country, a new product class or a new customer type goes live.
- No rate, threshold, exemption or scheme detail from memory: read it in the source and date it, or ask (part 1).
- Never hard-code a rate, a country list or a product classification in code (part 1).
- Never trust a country or a business status entered by the customer without a recorded check (parts 2 and 3).
- Never edit an issued invoice: amend by a referencing document (part 5).
- Never paste real customer or tax data into a prompt, a ticket or a fixture; use dummy data.
- National law, the special schemes, rates, thresholds, guidance and case law were not read: say so and ask the
  adviser.

## Origin
Text of Council Directive 2006/112/EC (CELEX 32006L0112), consolidated version of 01.01.2025, on EUR-Lex, read
2026-10-19, restated in our words. The engineering method is our own guidance. Full provenance, what was removed
and what was not verified: [`references/origin.md`](./references/origin.md). 🟡: never run by us.
