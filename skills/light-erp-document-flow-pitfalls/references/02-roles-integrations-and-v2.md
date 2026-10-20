# light-erp-document-flow-pitfalls §2 — Roles, integrations and v2

> Part 2 of `skills/light-erp-document-flow-pitfalls`. Read it when permissions, an integration or the first
> release are planned. Craft knowledge, no external source read.

1. **Permissions are abilities per document type and action.** Create, edit draft, confirm, post, void, approve,
   see prices, see costs, export, change bank details. Symptom: everyone who can create can also post and
   approve their own document. Fix: separate roles for preparing, approving and posting where the business
   needs it, a rule that the approver differs from the creator above an amount set by policy, abilities
   named as permissions rather than role names (see `skills/laravel-permissions-not-roles`), and a test per
   ability. Cost and margin fields get their own ability since sales staff rarely need them.
2. **Approval is data, not a flag.** Store a request, the approver, the decision, the time and the version of
   the document approved; any content change after approval invalidates it. Symptom: a purchase order edited
   after sign-off.
3. **Imports go through staging and the same validation as the screen.** Products, parties and opening
   balances arrive from files. Fix: a staging table, a mapped preview, per-row errors, create-update-skip
   counts, the import id kept on each row so it can be reversed, and no import path that writes a numbered
   or posted document unless it follows the posting rule. Opening stock and balances go in as dated opening
   documents, not as edits. Spreadsheet traps are in `business/spreadsheet-data-cleaning-pitfalls`.
4. **Exports are scoped and logged; formulas are neutralised.** Same visibility as the list, async for large
   sets, signed expiring links, an audit entry, and cells starting with a formula character are quoted.
5. **Integrations carry ids and run twice safely.** Payment, bank, shipping, e-commerce, accounting export and
   e-invoicing platforms each have their own ids; store the external id and a sync state on the document,
   make inbound webhooks idempotent by event id, queue outbound calls and retry with backoff, and show failed
   syncs to a person instead of looping. Structured e-invoicing obligations are in
   `skills/e-invoicing-obligations-pitfalls`; do not hard-code a format.
6. **Accounting export is an interface, not a second ledger.** Decide whether the app only exports
   documents to the accountant's tool or posts journal entries itself; the second needs a chart of accounts,
   double entry and period locks, which is a different and larger product. Symptom of drifting into it by
   accident: ad hoc "accounting" columns on documents. Period lock, if present, blocks posting and edits in
   closed periods; the closing rules come from the accountant.
7. **Reports use documents, with defined dates and statuses.** A sales figure names the document type, the
   date (issue, delivery, payment), the status set (drafts and voids excluded) and the currency. Symptom:
   dashboard and export disagree. One query per metric, reused.
8. **What to split first.** Order: parties and products master with archive and duplicate control; one
   document type end to end (usually invoice or order) with numbering, statuses, snapshots, immutability and
   audit; the conversion chain with remaining quantity; roles and approvals; imports and exports; then
   purchase side, stock integration and accounting export. A later type reuses the shared document code.
9. **What is regretted at v2.** Numbering by `max()+1`; editable posted documents; no price and tax snapshot;
   no tenant or entity id; delete buttons on numbered rows; one rounding rule per screen; stock and invoicing
   coupled by direct table writes; statuses as strings scattered in conditions; generated PDFs not stored;
   approval as a boolean. Each is cheap at the first migration and costly once customers hold numbers.
10. **Laravel and Nuxt pointers, short.** In Laravel: a counter table locked with a row lock inside the
    posting transaction, an action class per status transition, policies for abilities, model events replaced
    by explicit actions where the team forbids observers, a global tenant scope, queued exports, and
    database triggers or constraints for the immutability of posted rows. In Nuxt: show read-only state from
    the server's status, never compute totals as the source of truth in the browser, keep forms of draft
    documents autosaved but numbers server-assigned, and download PDFs from the stored file.
