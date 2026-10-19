# vat-handling-in-software-pitfalls §3 — The record per transaction

> Part 3 of `skills/vat-handling-in-software-pitfalls`. Read it when an order or payment model is designed or
> audited. Source: Council Directive 2006/112/EC, consolidated version of 01.01.2025, Articles 44, 45, 58, 63,
> 226, 233 and 247, https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02006L0112-20250101 , read
> 2026-10-19. Re-read before relying. Sentences marked "own guidance" are ours. The Directive articles read do not
> list what evidence of country or status must be kept; that is national and adviser territory.

1. **The decision depends on facts, so the facts are stored.** Articles 44, 45 and 58 make the place of supply
   depend on where the customer or the supplier is established, resides or has a permanent address. Own guidance:
   store, on every transaction, the inputs the decision used, not only its output: customer status, the country
   evidence, the product class, the supply date, the result. A tax amount with no recorded inputs cannot be
   defended or recomputed.
2. **Customer status carries its proof.** Article 226(4) requires the customer's VAT identification number on
   an invoice in the cases it names. Own guidance: a business status is stored with the number given, the result of
   the validation (checked by whom or by what service, when, outcome, the response kept), and the name and address
   it matched. A number that was never checked is recorded as "unchecked", and the order is treated as a consumer
   sale or held, as the adviser decided. How a number is validated and what check satisfies the authority is for
   the adviser, not read here.
3. **Re-check at the right moments.** Own guidance: validate at order time and at each renewal of a subscription,
   because a status can change; keep each check as a row, never overwrite the previous one.
4. **Country evidence is plural.** Own guidance: the Directive speaks of establishment, permanent address and usual
   residence, which are legal notions; the signals you hold are different things (billing address, delivery
   address, payment-method country, network location, the customer's own declaration). Store each signal with its
   source and time, store which one the decision used, and never let a single editable form field be the only
   evidence. Which signals the authority accepts, and how many are needed, is for the adviser.
5. **Conflicting signals are a state, not an error.** Own guidance: when signals disagree, the order records the
   conflict and follows the rule the adviser set, and never picks silently; a periodic count of conflicts is a
   quality measure for the tax design.
6. **Date is the supply date.** Article 63 ties chargeability to the supply of the goods or services, and Article
   226(7) asks the invoice to show the supply date when it can be determined and differs from the issue date. Own
   guidance: keep the issue date, the supply date and the payment date as three fields, and compute with the
   supply date.
7. **Freeze the treatment at the time.** Own guidance: the stored result (rate, treatment code, reason, legal
   mention) is a snapshot on the transaction. Later changes to tables never rewrite it; a correction is a new
   document (part 5).
8. **Keep the audit trail.** Article 233(1) says authenticity of origin, integrity of content and legibility of
   an invoice are ensured from issue to the end of the storage period, and that business controls creating a
   reliable audit trail between an invoice and a supply may do it. Own guidance: the link order, payment, invoice,
   credit note is a stored chain, with append-only history on the fields above.
9. **Retention is national.** Article 247(1) says each Member State determines the storage period for invoices
   concerning supplies in its territory. Own guidance: store the country and the retention rule per record, never
   one global value, and delete only on the adviser's rule; personal data duties run in parallel, see
   `business/data-protection`.
10. **Dummy data in tests.** Own guidance: fixtures use fake tax numbers and fake customers; a test number that
    looks valid is labelled as such so it is never sent to a real validation service.
