# invoicing-app-build-pitfalls §2 — Runs, integrations and v2

> Part 2 of `skills/invoicing-app-build-pitfalls`. Read it when a recurring run, an integration or the first
> release are planned. Craft knowledge, no external source read.

1. **A billing run is idempotent per customer and period.** Symptom: a crash and a rerun bill some customers
   twice, or skip some. Fix: a run record with a period and a status, a unique key of subscription plus
   billing period on the generated invoice, work done per customer in its own transaction, a rerun that
   skips what exists and completes what is missing, and a report of created, skipped and failed. Test it by
   killing the run halfway (see `skills/laravel-idempotent-jobs`).
2. **Proration and usage are computed from stored inputs.** Symptom: mid-period plan change or metered usage
   produces an amount nobody can explain. Fix: store the period boundaries, the quantity and the unit price
   as invoice lines with a description of the period, use the same calendar rule everywhere (days in the
   period or a fixed month; the choice is a commercial policy), round once under the rule from §1 point 6,
   and keep raw usage events with ids so a dispute can be recomputed. Late usage goes on the next invoice or
   a credit, never into an issued one.
3. **Payment-provider webhooks are verified, deduplicated and replayable.** Symptom: a replayed event pays an
   invoice twice or a forged call marks it paid. Fix: check the signature with the provider's documented
   method, store the event id and ignore a seen one, return quickly and process in a queue, handle events
   arriving out of order by reading the object's current state from the provider, and log the raw event for a
   limited time. Keys and secrets live in a vault and are rotated.
4. **Dunning is a schedule with state, not a loop.** Reminders are driven by due date, settlement state and a
   per-customer pause flag; each reminder is a row so it is not sent twice; a payment or dispute stops the
   sequence; tone and timing are commercial choices and some jurisdictions restrict collection practice, so
   ask the legal owner. Do not suspend service or add fees by default.
5. **Refunds and disputes are documents, not edits.** A refund is a negative payment and, where the invoice
   was wrong, a credit note; a chargeback is a recorded event that reopens the receivable. Keep the link
   between the original payment, the refund and the credit note.
6. **Roles and abilities.** Create draft, issue, void, credit, apply payment, reallocate, refund, change
   bank details, change tax codes, export, see cost. Separate whoever changes customer bank details from whoever
   approves payments out. Name abilities as permissions (see `skills/laravel-permissions-not-roles`) and test
   each. Support staff can read and send, not issue or credit, unless the business says so.
7. **Imports.** Customers, opening balances and historic invoices come in through staging with a preview,
   duplicate control on the customer key, counts of create, update and skip, and an import id for undo.
   Historic invoices import as already issued with their original numbers, dates and totals, bypassing the
   issue step on purpose and flagged as imported; never renumber them. Spreadsheet traps are in
   `business/spreadsheet-data-cleaning-pitfalls`.
8. **Exports and structured formats.** An accountant export is a read of stored totals, with the same
   scoping, an audit entry and quoted formula-starting cells. A structured e-invoice or a tax-portal file is
   produced from the issued invoice's stored data, validated against the current specification you read and
   dated, and its transmission state stored on the invoice (see `skills/e-invoicing-obligations-pitfalls`).
   Do not invent mandatory fields; take them from the current specification.
9. **What to split first.** Order: customer master with duplicate control; invoice with draft, issue,
   numbering, snapshots, immutability, stored PDF and audit; credit notes; payments and allocation; roles;
   exports to the accountant; then recurring runs, usage, dunning, webhooks and structured formats. Ship the
   first four before any recurring billing, because every later feature depends on a sound issued invoice.
10. **What is regretted at v2.** Numbering at draft or by `max()+1`; editable issued invoices; totals
    recomputed on read; a single paid boolean; tax rate in a column with no code or date; payments attached
    to one invoice only; a billing run with no idempotency key; webhooks trusted without a signature or event
    id; deleted customers; no stored PDF; no entity id on series; one rounding rule per screen.
11. **Laravel and Nuxt pointers, short.** In Laravel: a counter row lock inside the issue action, a unique
    index on subscription and period, queued jobs with idempotency keys, a webhook controller that verifies
    the signature before dispatching, model attributes cast to integer minor units, and policies for
    abilities. In Nuxt: show amounts from the server's stored totals, never compute them as truth in the
    browser, disable editing from the status field the API returns, and download the stored PDF.
