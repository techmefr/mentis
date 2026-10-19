# vat-handling-in-software-pitfalls §4 — Invoice content

> Part 4 of `skills/vat-handling-in-software-pitfalls`. Read it when an invoice or credit note template changes.
> Source: Council Directive 2006/112/EC, consolidated version of 01.01.2025, Articles 217 to 222, 226, 226b,
> 232, 233 and 247, https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02006L0112-20250101 , read
> 2026-10-19. Re-read before relying. Sentences marked "own guidance" are ours. The national rules for the invoice
> of your supply may add or relax details within the options of the Directive.

1. **Article 226 lists the details and says only these are required for VAT purposes.** Without prejudice to
   particular provisions, an invoice issued under Articles 220 and 221 carries: the date of issue; a sequential
   number, based on one or more series, that uniquely identifies the invoice; the supplier's VAT identification
   number; the customer's VAT identification number where the customer is liable for the tax or receives certain
   goods supplies; the full name and address of both; the quantity and nature of the goods or the extent and
   nature of the services; the supply date or the date of payment on account when it differs from the issue date;
   the taxable amount per rate or exemption, the unit price exclusive of VAT and discounts or rebates not included
   in it; the VAT rate applied; the VAT amount payable except under a special arrangement that excludes it. Own
   guidance: each is a field in the invoice model, filled from the stored transaction (part 3), not typed.
2. **Some mentions depend on the case.** Article 226 also requires, in the situations it names: a reference to
   the exemption provision, or another indication that the supply is exempt; the words "Reverse charge" when the
   customer is liable for the tax; "Self-billing" when the customer issues the invoice; "Cash accounting" under the
   corresponding arrangement; the margin scheme mentions; and the tax representative's identification when the
   representative is liable. Own guidance: the legal mention is a field of the tax treatment (part 1), so the
   template cannot forget it. The wording on a Member State's invoice may follow its own transposition.
3. **Numbering is a uniqueness guarantee.** Article 226(2) asks for a sequence uniquely identifying the invoice,
   in one or more series. Own guidance: numbers come from a transactional counter per series, issued at the time
   the invoice is finalised; a gap is investigated, not renumbered; a draft has no number.
4. **A document that amends an invoice is an invoice.** Article 219 says any document or message that amends and
   refers specifically and unambiguously to the initial invoice is treated as an invoice. Own guidance: a credit
   note carries the same required details and a reference to the original (part 5).
5. **When an invoice is required.** Article 220(1) obliges the taxable person to ensure an invoice is issued for
   supplies to another taxable person or to a non-taxable legal person, for certain distance sales of goods, and
   for payments on account. Article 221(1) lets Member States require one for other supplies. Own guidance: do not
   assume a consumer sale needs none; the national rule decides, and the template exists for every case.
6. **Timing.** Article 222 sets a latest day for invoices on certain supplies, expressed relative to the month of
   the chargeable event, and lets Member States set time limits for others. Own guidance: store the deadline per
   case and alert on invoices not yet issued; the exact deadline is re-read in the text and confirmed by the
   adviser.
7. **Simplified invoices are an option, not a default.** Article 220a lets Member States allow a simplified
   invoice in listed cases and Article 226b lists the minimum details; Article 220a(2) excludes certain supplies.
   Own guidance: ship the full invoice by default; a simplified one is a configuration the adviser approves per
   country, and the amount limits are re-read from the text, not remembered.
8. **Which country's invoice rules apply.** Article 219a(1) says invoicing is subject to the rules of the Member
   State where the supply is deemed to be made, with exceptions in Article 219a(2). Own guidance: the invoice
   template is selected by the tax decision, not by the supplier's home country.
9. **Electronic invoices need the recipient's acceptance.** Article 217 defines an electronic invoice as one that
   contains the required information and was issued and received in any electronic format; Article 232 says use of
   an electronic invoice is subject to acceptance by the recipient. Own guidance: store the acceptance or the
   agreement with the date. Structured electronic invoicing duties imposed by Member States are another subject.
10. **Authenticity, integrity, legibility.** Article 233 requires all three until the end of the storage period,
    and says each taxable person determines how, for example by business controls forming an audit trail.
    Own guidance: hash and archive the issued document; never regenerate a past invoice from current templates or
    current tables, always serve the stored original.
11. **Storage may be constrained.** Article 247(2) and (3) allow Member States to require storage in the original
    form and to restrict storage in certain countries. Own guidance: the archive's region is a data point checked
    against the retention rule per country (part 3, point 9).
