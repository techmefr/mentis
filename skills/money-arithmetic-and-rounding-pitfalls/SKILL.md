---
name: money-arithmetic-and-rounding-pitfalls
description: "Use when code stores, adds, splits, converts or displays amounts of money: integer minor units or exact decimals with an explicit currency, the exponent coming from the maintained ISO 4217 list (zero-, two- and three-decimal currencies), choosing a ledger scale once, calculating on integers, rejecting invalid amounts, largest-remainder splitting, a named rounding policy, currency exchange through paired transfers, overflow and the wire format."
---

# money-arithmetic-and-rounding-pitfalls

A defensive block for the arithmetic under a financial feature. The mistakes it prevents are small and
expensive: one unit of drift in a sum, a lost cent in a split, two decimals assumed for a currency that has none
or three, a ledger whose scale cannot be changed. The rules come from one reference implementation, one
database's data-modelling page and one ledger library, plus the maintained ISO 4217 list for currency exponents.
The invariant "money is never a float and every amount carries its currency" is already in `business/fintech-compliance`
part 2, and the general value-object idea is in `skills/design-patterns`; this block adds the mechanics. What
happens when a payment call returns nothing is in `skills/unknown-payment-outcome-pitfalls`.

**Not covered, and not verified:** which rounding mode or rounding point the law requires for tax, VAT, invoice
or statutory amounts depends on the jurisdiction and the date and was not read. This block states no such rule
and no tax rate. That question goes to an accountant or tax adviser.

## When
- A diff adds a column, field or type for an amount, a price, a balance or a fee.
- Amounts are summed, multiplied by a rate, divided among parties, converted between currencies or formatted.
- A new currency is supported, or an amount crosses a boundary (an API, a file, another system).
- A figure is "off by a cent", or a reconciliation shows a fractional-unit difference.

## Steps

**Read the part before changing how amounts are represented or computed.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Representation and arithmetic: integer units and currency, exponent from the ISO list, scale choice, validation, splitting, rounding policy, exchange, overflow, wire format | an amount is stored, computed, split, converted or sent | [`01-representation-and-arithmetic.md`](./references/01-representation-and-arithmetic.md) |

## Output / checkpoint
For each place amounts are handled: the stored representation (units and currency, or exact decimal), where the
exponent comes from, the scale and why it will not need to change, the rounding policy and the single point
where it is applied, how a split keeps its parts summing to the whole, and what an unknown currency does.
Evidence is a property test that splits random amounts into random numbers of parts in currencies with zero,
two and three decimals and asserts the parts sum to the whole, and a test that an unlisted currency is refused.
Nothing here was run by us.

## Guardrails
- This block does not replace a chartered accountant, an auditor, a legal, tax or compliance adviser, or a
  financial adviser. It is engineering method, not accounting, tax or investment advice.
- Never state or code a legally required rounding rule, VAT rule or rate from this block: it has none, and the
  question is for an accountant (part 1, rule 9).
- Never hardcode "two decimals" or "cents"; take the exponent from the maintained ISO 4217 list and re-read it,
  do not freeze a copy (part 1, rules 2 and 3).
- Never guess an exponent for an unlisted currency; refuse it at validation (part 1, rule 3).
- Never use a binary float for an amount at any hop, including a JSON number and an analytics job (part 1,
  rules 1 and 13).
- Never divide money by plain division; allocate so the parts sum exactly (part 1, rule 7).
- Never add or compare amounts of different currencies without an explicit conversion step (part 1, rule 10).
- Do not paste a real account number or balance into a prompt, a fixture or a log.

## Origin
Rewritten from the payments-platform money package and amount decision record (Apache-2.0), the TigerBeetle
data-modelling page (Apache-2.0) and the pgledger README (MIT), plus the ISO 4217 list one published by SIX as
maintenance agency, all read 2026-10-16. The full provenance, what was removed and what is our own guidance are
in [`references/origin.md`](./references/origin.md). 🟡: never run by us.
