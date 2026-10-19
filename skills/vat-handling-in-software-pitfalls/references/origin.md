# vat-handling-in-software-pitfalls: origin and source stamps

> Provenance of `skills/vat-handling-in-software-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from a directive text only, never run by us: no billing flow was designed
or reviewed with it. This block is a working method, not tax advice, and it does not replace the tax adviser or
the national tax authority.

## Sources (all read 2026-10-19, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Council Directive 2006/112/EC, consolidated version of 01.01.2025 (document 02006L0112-20250101 on EUR-Lex, which states it has no legal effect and that the Official Journal texts are authentic), https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02006L0112-20250101 , Articles 2, 9, 14, 14a, 24 | Official text of the European Union, reused with mention of the source | Transactions subject to VAT, taxable person, supply of goods and of services, deemed supplier through an electronic interface |
| Same, Articles 33, 44, 45, 46, 58, 59, 59a, 59c, 196 | same | Place of supply: distance sales, services to taxable and non-taxable persons, intermediaries, digital services, services outside the Community, the small-supplier provision, reverse charge for Article 44 services |
| Same, Articles 63, 73, 73a, 78, 79, 90, 91 | same | Chargeable event, taxable amount and its inclusions and exclusions, reductions after supply, currency conversion |
| Same, Articles 96 to 98 | same | Standard rate, minimum, reduced rates tied to Annex III (no figure restated) |
| Same, Articles 217 to 222, 226, 226b, 232, 233, 247 | same | Invoice definition, issue, mandatory content, simplified invoices, electronic invoices, authenticity, storage |

The text was read in a real browser (EUR-Lex answers an empty HTTP 202 to curl and to the fetch tool). It is the
consolidated version of 01.01.2025, not the Official Journal original (OJ L 347, 11.12.2006) and not necessarily
the current text: a later consolidation or amendment may exist.

## Removed
1. **Every rate, threshold and amount limit.** None is stated as a rule. The Directive's minimum rate figures, the
   small-supplier amount of Article 59c and the invoice amount limits of Articles 220a and 238 were read but are
   not restated; the reader re-reads the text and the national value.
2. **The one-stop-shop and import schemes** (Title XII, Chapter 6): not read; the block only says to ask.
3. **Place-of-supply rules other than those listed** (immovable property, transport, events, supplies on board,
   other services to consumers): not read.
4. **Annexes** (II list of electronically supplied services, III reduced-rate list): not read.
5. **Right of deduction, exemptions, registration and returns:** not read; out of scope.

## Not verified
1. **Official Journal original and later amendments** were not compared with the consolidated text.
2. **Recitals** and the implementing regulation on the Directive were not read.
3. **National law** transposing the Directive: rates, rounding, invoice mentions, retention periods, validation
   rules, simplified-invoice limits and invoicing timing were not checked.
4. **Rounding rule:** the articles read give none; part 5 point 3 says so and routes it.
5. **Evidence of customer location and status checks:** not in the articles read; routed to the adviser.
6. **Own guidance, flagged in the text:** the data model for rates and classes, the single decision function,
   the stored inputs per transaction, the re-check and conflict states, the immutable snapshot, the credit note
   chain, the reconciliation test and the escalation file.
7. **Source quality:** a single directive text; no practitioner guide was used.

## Related blocks
`business/finance-ops`, `business/fintech-compliance`, `business/data-protection`,
`skills/money-arithmetic-and-rounding-pitfalls`, `skills/source-freshness`,
`skills/gdpr-international-transfers-pitfalls`.
