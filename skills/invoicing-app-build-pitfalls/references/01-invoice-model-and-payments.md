# invoicing-app-build-pitfalls §1 — Invoice model and payments

> Part 1 of `skills/invoicing-app-build-pitfalls`. Read it when a schema, an issue step or a payment flow is
> designed. Mostly craft knowledge; points 1, 3, 4, 5 and 8 carry facts from open-source billing sources and one vendor page, read 2026-10-20 and restated in our words (`references/origin.md`, sources 1 to 3). Everything not marked as sourced is our own guidance. No legal or tax rule is stated; ask the accountant.

1. **Minimal model.** Customer (with billing identity and tax identifiers as the accountant requires), invoice
   (header: status, number, issue date, due date, currency, totals, seller and buyer snapshots, link to a
   source order or contract), invoice line (description, quantity, unit, unit price, discount, tax code and the
   rate applied, amounts), payment, payment allocation (payment to invoice, with an amount), credit note
   (an invoice document of negative effect linked to the original), and for recurring billing a subscription
   and its plan with a billing period. Keep payments and invoices separate: a payment is a fact about money
   received, an allocation says what it settled. The reference data model separates the payment from the application of a payment to an invoice, with an amount applied on each application row (source 2); the billing engine's docs go the other way and map one payment to one invoice, with several partial payments allowed and one payment over several invoices unsupported (source 1). Allocation rows are therefore a design choice, not a universal one.
2. **Draft has no number; the number is given when issuing.** Symptom: a deleted draft leaves a hole, two
   concurrent issues share a number. Fix: draft gets an internal id; issuing runs in one transaction that locks
   a counter per tenant, seller entity and series, assigns the next number, freezes the content, sets the issue
   date and writes the status change. Whether gaps are tolerated, whether a series restarts each year and what
   a void must record are rules to obtain from the accountant, not to guess; write the answer in the spec
   with its date.
3. **An issued invoice carries snapshots.** Symptom: changing a customer address or a product price alters old
   invoices, or a tax-rate edit rewrites history. Fix: copy seller and buyer identity, line descriptions, unit
   prices, tax codes and applied rates, and the exchange rate and its date if converted, onto the invoice at
   issue. Keep the template version and a hash of the stored PDF or structured file; reprints serve the stored
   file, never a fresh render. The reference model's invoice lines hold their own description, quantity and amount, and carry the tax authority rate used, with an override-account field whose comment explains it protects against configuration changes after posting (source 2).
4. **Issued means immutable; correction is a credit note.** Symptom: a changed amount no longer matches what the
   customer holds. Fix: after issue, no update path to amounts, lines, parties or dates, enforced in the model
   and, where the database allows, by a trigger or by revoking update on those columns. A mistake is fixed by a
   credit note referencing the original (full or partial) and, if needed, a new invoice. Allocation and
   payment status remain mutable since they are not the invoice content. Whether a given correction needs a
   credit note or may be reissued is a legal question. The payment vendor's page agrees on the shape: once an invoice is finalised most details cannot change, only a few such as the memo or metadata, a substantive change means a new invoice and voiding the old one, and only a draft can be deleted (source 3). The billing engine's docs correct with negative adjustment and credit items and call invoices mostly static (source 1).
5. **Statuses.** Draft, issued, partly paid, paid, overdue, void, written off. Fix: store only draft, issued,
   void as the document status and derive the settlement state (paid, partly paid, overdue) from allocations
   and the due date at read time, so it cannot drift. Define void: allowed only when nothing is paid and the
   customer has not been sent it, otherwise use a credit note. The billing engine computes the balance from charges, credits, adjustments and the paid amount, and treats a written-off invoice as zero balance through a tag (source 1), which supports deriving the settlement state. The vendor page instead stores paid, void and uncollectible as statuses and allows a paid invoice to go back to open by unapplying payments (source 3); storing paid is a valid alternative if every transition is recorded as a row.
6. **Money and rounding.** Integer minor units or exact decimals with a currency code on the invoice and every
   amount (see `skills/money-arithmetic-and-rounding-pitfalls`). Pick one rounding rule: per line then sum, or
   sum then round the tax per rate, as the accountant instructs; write it, test it, and make the screen, the
   PDF and every export read the same stored totals rather than recomputing. Symptom: the PDF total differs
   by a cent from the dashboard. A foreign-currency invoice stores the rate used for the base-currency figure
   and the date of that rate; rate source and conversion rules are policy.
7. **Tax is a code, not a rate in a column.** Store a tax code on the line and the rate and rule version
   applied at issue; the table of codes is dated and archived, never overwritten (see
   `skills/vat-handling-in-software-pitfalls`). Do not hard-code a rate or an exemption in code; every one
   must come from a source read and dated by the accountant. Reverse-charge, exempt and zero-rated lines need
   their own codes and a mention field, whose wording is a legal matter.
8. **Payments allocate explicitly.** Symptom: a part payment settles the newest invoice, or a customer pays
   without a reference and nobody knows what was settled. Fix: a payment can be unallocated, partly allocated
   or over-allocated to a credit balance; allocation is a row with an amount, made by the customer reference,
   by an operator, or by a stated rule (oldest first); reallocation is a new row, never an edit; a refund is a
   negative payment tied to the original. The billing engine records a refund and a chargeback as signed rows on the invoice's payment mapping, beside the original payment attempt, and adds a credit balance item when an invoice would go negative (source 1). Reconcile with the bank or processor on event date (see
   `skills/gl-subledger-reconciliation-pitfalls`).
9. **Archive, never delete.** An issued invoice is never deleted; a customer with invoices is archived, not
   removed, and foreign keys restrict (see `skills/laravel-no-cascade-delete`). An erasure request on a
   customer's personal data needs a routine that keeps the invoice as the law allows and minimises the rest;
   what must be kept and for how long is for the accountant and the data-protection owner. Soft delete hides
   rows, it does not erase them.
10. **Audit trail.** Insert-only log of who issued, voided, credited, changed bank details, allocated or
    reallocated payment, exported, with time and origin (screen, API, job). Retention is a legal question.
11. **Tenant and entity boundary.** Every table carries tenant and, where one tenant has several legal
    entities, entity id; counters, series and tax setup are per entity; scope once by default (see
    `skills/laravel-tenant-context-by-default`). Symptom of missing: a guessed invoice id shows another
    company's invoice, or two entities share a series.
12. **Dates.** Store issue date, due date and service or delivery period as dates with their meaning, not
    timestamps in the viewer's zone; due date is computed from payment terms at issue and then stored.
    Symptom: an invoice becomes overdue a day early for someone in another time zone.
