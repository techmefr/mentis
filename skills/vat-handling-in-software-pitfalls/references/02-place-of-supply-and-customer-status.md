# vat-handling-in-software-pitfalls §2 — Place of supply and customer status

> Part 2 of `skills/vat-handling-in-software-pitfalls`. Read it for a new market, a new product type or a B2B
> feature. Source: Council Directive 2006/112/EC, consolidated version of 01.01.2025, Articles 9, 14, 14a, 24, 33,
> 44, 45, 58, 59, 59a, 59c and 196, https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02006L0112-20250101
> , read 2026-10-19. Re-read before relying. Sentences marked "own guidance" are ours. Every case here is flagged
> for the tax adviser: the Directive sets general rules and many specific ones this block did not read.

1. **Taxable person is a legal status, not a company form.** Article 9(1) defines a taxable person as anyone who,
   independently, carries out an economic activity in any place, whatever the purpose or results. Own guidance:
   "business customer" in your data model is a status derived from checks (part 3), not a checkbox the buyer ticks.
2. **Goods and services are separate questions.** Article 14(1) defines a supply of goods as the transfer of the
   right to dispose of tangible property as owner; Article 24(1) defines a supply of services as any transaction
   that is not a supply of goods. Own guidance: each product carries that nature as data, and the place rules
   below differ for each. Software delivered as a download or a subscription is a classification question for the
   adviser, not a guess.
3. **Services to a business: where the customer is.** Article 44 says the place of supply of services to a
   taxable person acting as such is where that person has established his business; if the service is provided to
   a fixed establishment elsewhere, it is where that establishment is; failing both, where the person has a
   permanent address or usually resides. Own guidance: the country evidence for a business sale is the customer's
   establishment and the establishment that receives the service, so the data model needs both, not one billing
   country.
4. **Services to a non-business: where the supplier is, by default.** Article 45 says the place of supply to a
   non-taxable person is where the supplier has established its business, or the fixed establishment from which the
   service is provided. Own guidance: this default is overridden by specific rules, so it is not a safe
   fallback; an unknown case goes to the adviser.
5. **Digital services to a consumer follow the consumer.** Article 58(1) says the place of supply of
   telecommunications, radio and television broadcasting and electronically supplied services to a non-taxable
   person is where that person is established, has a permanent address or usually resides. Own guidance: for those
   products the consumer's country decides the rate, so the country evidence of part 3 is what the tax rests on.
   Whether your product is an electronically supplied service is the adviser's call; the Directive points to a
   list in Annex II, which this block did not read.
6. **Email contact does not make a service electronic.** Article 58(1) says that when supplier and customer
   communicate by email, that does not of itself make the service an electronically supplied one. Own guidance:
   do not classify a service as digital because it is delivered or ordered online.
7. **There is a small-supplier provision, and it is not yours to apply.** Article 59c(1) disapplies the Article 58
   rule for a supplier established in only one Member State when conditions on cross-border value to consumers are
   met, within a stated yearly amount; Article 59c(3) gives the right to opt for the Article 58 rule. Own guidance:
   the amount, the conditions and the option are in the text, re-read before relying; nothing in your code switches
   rules on this without the adviser's written decision, and the cumulative cross-border value is data you track.
8. **Customers outside the Union are another set of rules.** Article 59 lists services to a non-taxable person
   outside the Community whose place of supply is where that person is established or resides; Article 59a lets
   Member States adjust the place of supply where effective use and enjoyment is elsewhere. Own guidance: a
   non-Union customer is not "no VAT" by default; it is a case for the adviser.
9. **Distance sales of goods have their own place rule.** Article 14(4) defines intra-Community distance sales of
   goods by conditions on the dispatch, the buyer's status and the nature of the goods, and Article 33(a) says
   their place of supply is where the goods are when the transport ends. Own guidance: for goods shipped to
   consumers in other countries, the destination is the data the tax follows, and the dispatch address is
   captured and kept as evidence.
10. **Platforms can be deemed the supplier.** Article 14a says that a taxable person who facilitates, through an
    electronic interface such as a marketplace or platform, certain supplies of goods is deemed to have received
    and supplied those goods himself. Own guidance: if your product is a marketplace, who is the supplier for tax
    purposes is decided by the adviser, and the data model must be able to represent both roles.
11. **Reverse charge moves who accounts for the tax.** Article 196 says VAT is payable by the taxable person, or
    the non-taxable legal person identified for VAT, to whom the Article 44 services are supplied, if the supplier
    is not established in that Member State. Own guidance: a treatment of "customer accounts for the tax" is its
    own result of the decision function (part 1), it depends on the validated customer data of part 3, and it
    requires a mention on the invoice (part 4).
12. **Escalate by case, not by code path.** Own guidance: the adviser's answer is given per product class,
    customer type and country pair, recorded as a decision with its date, and referenced from the tax table; code
    that cannot name its decision refuses the order.
