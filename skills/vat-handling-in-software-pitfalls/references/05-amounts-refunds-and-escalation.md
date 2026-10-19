# vat-handling-in-software-pitfalls §5 — Amounts, refunds and escalation

> Part 5 of `skills/vat-handling-in-software-pitfalls`. Read it when an amount is computed, a refund flow built,
> or a case is unclear. Source: Council Directive 2006/112/EC, consolidated version of 01.01.2025, Articles 73,
> 73a, 78, 79, 90, 219 and 226, https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02006L0112-20250101
> , read 2026-10-19. Re-read before relying. Sentences marked "own guidance" are ours. The articles read say nothing
> on how a total is rounded: that is national, and it is why point 3 is a question, not a rule.

1. **The taxable amount is the consideration.** Article 73 says that, for ordinary supplies, the taxable amount
   includes everything that constitutes consideration obtained or to be obtained by the supplier from the customer
   or a third party, including subsidies directly linked to the price. Own guidance: the base is what the buyer and
   any third party pay for the supply, so bundles, third-party payments and subsidies are modelled, not ignored.
2. **What is in and out of the base.** Article 78 includes taxes, duties, levies and charges other than the VAT
   itself, and incidental expenses such as commission, packing, transport and insurance charged to the customer.
   Article 79 excludes early-payment discounts, discounts and rebates granted at the time of the supply, and
   repayments of expenditure incurred in the customer's name and on his behalf. Own guidance: shipping and fees are
   lines with their own tax class and treatment, discounts are stored as lines with a type, and whether a given
   voucher, coupon or fee is in or out is a case for the adviser, together with Article 73a on multi-purpose
   vouchers.
3. **Rounding is a decision, not a default.** Own guidance: per line or on the total, banker's or half-up, give
   different results on the same basket; the Directive text read gives no rule, so the rule is the national one,
   obtained from the adviser, written as data, and applied by the single decision function (part 1). The mechanics
   of exact decimal arithmetic, rounding modes and allocating a remainder are in
   `skills/money-arithmetic-and-rounding-pitfalls` §1; never use binary floating point for an amount.
4. **Make the rounding visible and consistent.** Own guidance: the invoice shows the taxable amount per rate
   (Article 226(8)) and the tax amount (Article 226(10)); the totals must be the sums of what is printed, so the
   rounding level chosen is the one the printed figures reproduce. A test recomputes every stored invoice from its
   printed lines and fails on any cent of difference.
5. **Cancellation, refusal, non-payment and price reductions reduce the taxable amount.** Article 90(1) says so,
   under conditions the Member States determine, and Article 90(2) lets Member States derogate for non-payment.
   Own guidance: a refund flow carries a reason (cancellation, return, goodwill price reduction, bad debt), and the
   tax consequence of each reason is the adviser's rule per country, not one universal subtraction.
6. **Never edit an issued invoice.** Article 219 treats a document that amends and refers specifically and
   unambiguously to the initial invoice as an invoice. Own guidance: a refund is a credit note with its own number
   (part 4), referencing the original, reusing the original treatment snapshot (part 3, point 7), with amounts
   negative or marked as credit, never a rewrite and never a hard delete.
7. **Partial refunds and several rates.** Own guidance: a partial refund names the lines and quantities it
   reverses, so base and tax are computed per rate from the original lines; the remainder after rounding is
   allocated by the rule of point 3 so the sum of all credit notes never exceeds the original.
8. **Foreign-currency orders.** Own guidance: the invoice shows what the national rule requires for the tax
   amount in the Member State's currency (part 1, point 9); store the original-currency amounts, the rate and its
   date.
9. **Escalate to the tax adviser, with a file.** Own guidance, the list: a new country, product class or customer
   type; any classification of a product as goods, service or electronically supplied service; any marketplace or
   resale model; reverse-charge cases; customers outside the Union; thresholds and special schemes; the rounding
   and currency rules; simplified invoices; invoice timing and storage; refunds and bad debt; a notice from an
   authority. The file holds the product description, an example order with its stored inputs (dummy data), the
   current code decision, and the question. The adviser's answer is stored with its date and referenced from the
   tax tables.
10. **Say what you did not know.** Own guidance: the final message of any change in this area lists the rules
    taken from a source with their date, the rules assumed from the adviser's decision with its date, and the
    cases not covered, and ends with: not tax advice, escalate to the tax adviser.
