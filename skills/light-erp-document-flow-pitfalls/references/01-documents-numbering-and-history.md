# light-erp-document-flow-pitfalls §1 — Documents, numbering and history

> Part 1 of `skills/light-erp-document-flow-pitfalls`. Read it when a schema, a status or a numbering rule is
> designed. Craft knowledge, no external source read. No accounting or tax rule is stated; ask the accountant.

1. **One header, many lines, one shared shape.** A document has a header (type, series, number, status, party,
   dates, currency, totals, owner) and lines (product or free text, quantity, unit, unit price, discount, tax
   code, line total, link to the source line). Using one generic document table with a type column keeps
   conversion and reporting simple; give each type its own rules in code, not its own copy of the schema.
   Symptom of one table per type: five almost-identical models and conversion code that drifts.
2. **Statuses are a table with transitions.** Draft, confirmed or sent, partly fulfilled, fulfilled, cancelled,
   and for invoices posted or paid. Symptom: a document stuck "pending" that nobody can define. Fix: per type,
   list each status, who may move it, the condition, and what becomes read-only; enforce in one place (see
   `skills/laravel-recognise-state-machine-or-pipeline`); store status changes as rows with actor and time.
   Derive "paid" or "fulfilled" from linked payments or deliveries rather than a hand-edited flag.
3. **Numbers are allocated at posting, in the same transaction, from a counter.** Symptoms: two documents with
   one number, or a hole after a rollback. Check: post fifty documents in parallel and compare. Fix: a
   counter row per tenant, series and year or period, locked while the number is taken, taken only when the
   document leaves draft, and written in the same transaction as the status change. Drafts carry a temporary
   id, not a number. A database sequence is not transactional on rollback and leaves holes; whether holes are
   acceptable, and how a void is recorded, is a legal and accounting policy you must obtain, not guess. State
   the policy in the spec: gapless with a voided-number record, or gaps allowed and explained.
4. **Conversion tracks remaining quantity per line.** Quote to order to delivery to invoice, often in parts.
   Symptom: an order delivered twice, or invoiced for more than shipped. Fix: each target line stores the
   source line id and quantity; remaining equals source quantity minus the sum of converted quantities in
   non-cancelled targets; the conversion locks the source line, rejects an over-conversion, and updating or
   cancelling a target restores the remaining quantity. Allow only the conversions your table lists.
5. **Lines snapshot price, tax and text.** Symptom: raising a product price changes last year's quotes, or a
   changed tax code rewrites old invoices. Fix: copy description, unit, unit price, discount, tax code and the
   tax rate or rule reference onto the line at the time it is added; keep the product id only as a link for
   reporting. The party's name and address are snapshotted on the header too, since a customer can move.
6. **Posted documents are immutable; correct by reversal.** Symptom: an edited confirmed document no longer
   matches the PDF the customer holds or the ledger. Fix: once past draft, the content is read-only at the
   database level where possible (trigger or revoked update on posted rows) as well as in the app; a
   correction is a new document (credit note, reversal, adjustment) referencing the original, and the
   original keeps its link to it. A cancelled document keeps its row, number and PDF.
7. **Keep the issued PDF.** Store the rendered file or the data and template version that produced it, with a
   hash, at issue time. Symptom of regenerating from live data: a reprint differs from what was sent.
8. **Archive or void, never delete a numbered document.** Drafts with no number may be deleted; anything
   numbered is voided or cancelled with a reason and stays listable. For master data (parties, products,
   tax codes) use an archived flag, hidden from pickers but resolvable from old documents; restrict foreign
   keys rather than cascading (see `skills/laravel-no-cascade-delete`). Soft delete hides, it does not erase
   personal data; an erasure request on a party needs a routine that anonymises personal fields and keeps
   the document with the snapshot minimised as the law allows; ask the data-protection owner.
9. **Money: currency per document, exact arithmetic, one rounding policy.** Integer minor units or exact
   decimals, the currency on the header, a rounding rule (per line or on the total) chosen once and written
   down, and a foreign-currency document storing the rate and its date used for any base-currency figure (see
   `skills/money-arithmetic-and-rounding-pitfalls`). Symptom: lines sum to a total that differs by a cent
   from the displayed one.
10. **Tenant and entity boundaries on every table.** A tenant is a customer of your product; an entity is one
    legal company inside it with its own series, books and tax setup. Put both ids on documents and lines,
    scope every query once by default (see `skills/laravel-tenant-context-by-default` and
    `skills/laravel-scope-dont-check-after-fetch`), make series and unique numbers unique within tenant and
    entity, and partition files and search the same way. Symptom of missing: an id guessed in a URL opens
    another customer's invoice.
11. **Audit trail is separate from status history.** Record who changed what field of which document, with old
    and new value, time and origin (screen, import, API, job), insert-only. Sensitive actions (post, void,
    price override, approval, export) are always logged. Retention of these records is a legal question;
    ask the accountant rather than assuming.
12. **Parties are one master with roles.** A customer and a supplier may be the same company; keep one party
    record with role flags and separate payment terms, bank details and tax identifiers per role, and a
    duplicate check as in `skills/crm-app-build-pitfalls` §1. Bank details change is an audited, approved
    action because it is a fraud vector.
