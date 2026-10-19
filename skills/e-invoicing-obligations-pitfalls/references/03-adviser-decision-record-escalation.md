# e-invoicing-obligations-pitfalls §3 — Adviser questions, decision record, escalation

> Part 3 of `skills/e-invoicing-obligations-pitfalls`. Read it when a format or platform is chosen, tested or
> changed, or a question must go to the adviser. Own guidance throughout, built on the reading in parts 1 and 2
> (Directive (EU) 2025/516 and one national authority page, read 2026-10-19). Not tax or legal advice.

1. **Name the owners first.** Own guidance: a finance or compliance owner for the duty, an engineering owner for the
   systems, the accounting adviser for the interpretation. Without a named owner the question stays open.
2. **Questions for the accounting adviser, per flow.** Own guidance: (a) are we in scope for this flow, from which
   date; (b) does our current format qualify; (c) which format or syntaxes are accepted; (d) is a platform
   mandatory, which kinds; (e) do we issue, receive or both on it; (f) is acceptance by the recipient required;
   (g) what data must be reported and when; (h) how long and where must invoices be archived; (i) what applies to
   corrections, credit notes and self-billing; (j) what applies to foreign customers and suppliers. Record each
   answer with date and person.
3. **Ask for the source, not the answer alone.** Own guidance: the adviser's statement is useful; the sentence from
   the authority's page or the text it rests on is what goes in the record, with its date.
4. **Keep a decision record per flow.** Own guidance, one entry: flow, options considered (own tool, ERP module,
   third-party platform, authority portal if the national text allows one), choice, reasons, who decided, date,
   sources and their read dates, and the review date.
5. **A test before go-live, with evidence.** Own guidance: with invented customers and amounts, produce each invoice
   type (standard, credit note, corrective, reverse-charge), validate the output with the vendor's or authority's
   validation tool if one exists, send it, receive a test invoice, and keep the results. A test that was not
   written down did not happen.
6. **Test the failure paths.** Own guidance: rejected invoice, missing identifier on the recipient, platform
   outage, duplicate submission, a corrected invoice after an issue. Record what the system does and who is alerted.
7. **Know where the vendor stops and the company starts.** Own guidance: a vendor says its product is "compliant";
   the record notes what exactly it covers (format, transmission, reporting, archiving) and what stays with the
   company (master data, content, retention). Ask the vendor for its statement in writing and date it.
8. **Check the data the invoice needs exists.** Own guidance: the content list changes (part 1, point 11), so
   audit the master data for customer identifiers, supplier bank identifiers and the sequential number of corrected
   invoices before choosing the platform.
9. **Escalate immediately when:** an authority notice or a customer demand arrives with a date; two sources
   disagree on a date; a flow has no owner; the adviser cannot say whether a format qualifies; a platform or format
   change would stop invoices leaving; an invoice was rejected and not corrected in time. Own guidance.
10. **Re-read on a schedule.** Own guidance: when the national page's "modified" date changes, when a new law is
    announced, and at the review date in the decision record; follow `skills/source-freshness` and the
    retrieval method in `business/regulatory-watch` §5.
11. **Keep the record light and private.** Own guidance: no real invoices, tax identifiers or customer data in the
    record; link to where the adviser's documents sit instead.
