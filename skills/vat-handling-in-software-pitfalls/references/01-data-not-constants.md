# vat-handling-in-software-pitfalls §1 — Data, not constants

> Part 1 of `skills/vat-handling-in-software-pitfalls`. Read it when a rate, a tax code or a product class appears
> in code. Source: Council Directive 2006/112/EC, consolidated version of 01.01.2025, Articles 63, 90, 91 and 96
> to 98, https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02006L0112-20250101 , read 2026-10-19.
> Re-read before relying. Sentences marked "own guidance" are ours.

1. **The Directive sets a frame, each Member State fixes its own numbers.** Article 96 says each Member State
   applies a standard rate that it fixes itself as a percentage of the taxable amount, the same for goods and for
   services. Article 98 allows a limited number of reduced rates, only for supplies listed in Annex III. Own
   guidance: the rates in your code are the Member States' values, they differ by country and change, so they are
   rows in a table, never literals.
2. **No figure in this block.** The Directive states minimum levels; they are a floor for the Member States, not
   the rate you apply. Own guidance: never seed a rate table from memory, from a blog or from the Directive's
   minimums. The source of each row is the national tax authority or the adviser, filed with its date.
3. **A rate has three keys.** Own guidance: the country whose tax applies (part 2), the product class, and the
   date on which tax becomes chargeable. Article 63 says the chargeable event occurs and VAT becomes chargeable
   when the goods or the services are supplied. Own guidance: look up the rate by the supply date, not by the day
   the code runs, so a past order recomputed after a rate change gives the original figure.
4. **Product class is a mapping the business owns.** Article 98 ties a reduced rate to Annex III supplies, so
   which of your products falls where is a classification decision. Own guidance: each product or plan carries
   a tax class, a data field with a named owner; the mapping from class and country to rate is separate data, and
   a product with no class fails the order instead of defaulting to the standard rate.
5. **Rates are effective-dated rows.** Own guidance: a table of country, class, rate, valid from, valid to,
   source reference, entered by, entered on. A change is a new row; no row is edited or deleted once an invoice
   used it.
6. **One function decides the tax.** Own guidance: a single pure function takes customer status, country evidence,
   product class, supply date and returns the treatment (rate, or not taxable here, or customer accounts for it)
   with the reason. Checkout, invoicing, refunds and reports all call it; a second copy of the logic in a
   template or a report is a defect.
7. **The treatment is more than a number.** Own guidance: the result carries the rate, the legal mention the
   invoice needs (part 4) and the reason code, because "zero percent" is not one case: it can mean exempt, not
   taxable in this country, or taxed by the customer. Never store a bare 0.
8. **Cancellation and price changes follow the original.** Article 90(1) says that on cancellation, refusal, total
   or partial non-payment, or a price reduction after the supply, the taxable amount is reduced accordingly under
   conditions determined by the Member States. Own guidance: a credit note reuses the treatment of the original
   transaction by reference, it does not look the rate up again (part 5).
9. **Currency conversion is a rule too.** Article 91(2) addresses amounts expressed in a currency other than the
   Member State's, and says the rate applicable is the latest selling rate recorded, at the time VAT becomes
   chargeable, on the most representative exchange market of the Member State, or one determined by reference to
   it, under that Member State's rules; a following subparagraph says Member States accept instead the latest
   rate published by the European Central Bank. Own guidance: store the rate used and its source on the
   transaction; which rule applies in your case is a question for the adviser.
