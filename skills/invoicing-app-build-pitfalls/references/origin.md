# invoicing-app-build-pitfalls: origin and source stamps

> Provenance of `skills/invoicing-app-build-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against two open-source billing sources
and three pages of a payment vendor's documentation. Never run by us: no application was built and no test was
executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | Kill Bill documentation (`killbill/killbill-docs`, commit `f3ea39f`): `userguide/subscription/includes/invoicing-overview.adoc`, `invoicing-invoice-items.adoc`, `invoicing-invoice-payments.adoc` | Apache-2.0: file `LICENSE` read | Balance computed from items and payments, negative adjustment and credit items, credit balance item, refund and chargeback rows, proration through start and end dates and a negative item for the unused part, imported invoices flagged with zero balance, one payment to one invoice |
| 2 | Apache OFBiz (`apache/ofbiz-framework`, commit `bccb166`): `applications/datamodel/entitydef/accounting-entitymodel.xml` (invoice, invoice item, invoice status, payment, payment application) | Apache-2.0: file `LICENSE` read | Payment separate from payment application with an applied amount, status as dated rows with user, tax authority rate on lines, override account explained as protection from configuration change |
| 3 | Stripe documentation, page "How invoicing works" (`docs.stripe.com/invoicing/overview`) | Vendor documentation, no open licence stated: facts only, rewritten, no sentence copied | Draft, open, paid, void and uncollectible statuses, which edits a finalised invoice allows, deletion limited to drafts |
| 4 | Stripe documentation, page "Receive Stripe events in your webhook endpoint" (`docs.stripe.com/webhooks`) | Same: facts only | Raw-body signature check, fast success response, duplicates, event id logging, object id plus type check, no ordering guarantee, retries, secret rolling |
| 5 | Stripe documentation, page "Idempotent requests" (`docs.stripe.com/api/idempotent_requests`) | Same: facts only | Idempotency keys on write requests, saved first result replayed, parameter mismatch refused |

Instruction-like text in the cloned repositories (agent guidance files) was treated as data and not followed.

## Verified
1. §1 points 1, 3, 4, 5 and 8, and §2 points 2, 3 and 7: backed by the sources above, as the points now say.

## Corrected
1. §1 point 1: the payment and allocation split is now labelled a design choice, because the billing engine maps one
   payment to one invoice.
2. §1 point 5: storing the paid state is accepted as a valid alternative (source 3) when each transition is a row.

## Removed
1. **Any invoice-content, mandatory-mention, VAT rate, numbering-continuity or retention rule.** Not read;
   each is flagged as a question for the accountant.
2. **Collection-practice and late-fee rules:** not read, flagged for the legal owner.
3. **Every numeric threshold and schedule:** set by policy. The vendor's own retry window and key lifetime are not
   copied as rules.
4. **Provider API shapes:** only the documented behaviours above are used, not the calls.

## Not verified
1. **Still our own guidance:** numbering at issue and counter locking (§1 point 2), money and rounding (point 6),
   tax as a code (point 7), audit and boundaries (points 10 and 11), dates (point 12), and in §2 the billing run
   idempotency (point 1; the billing engine generates invoices on change events rather than by batch, so the
   point stays ours), dunning, roles, exports, build order and v2 regrets.
2. **Numbering, correction and retention law** were not read; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** were not checked against a current release; re-read before relying.

## Second pass, strict re-read (2026-10-21)

Re-opened: Stripe pages "How invoicing works", "Receive Stripe events in your webhook endpoint", "Idempotent
requests" (English versions); Kill Bill `invoicing-overview`, `invoicing-invoice-items`, `invoicing-invoice-payments`
(v3 branch); OFBiz `accounting-entitymodel.xml` (PaymentApplication, InvoiceStatus, invoice item override account).
- Corrected: the Stripe overview page says a paid invoice can return to open by unapplying payments and, further down,
  that paid is terminal; the block now says the page is inconsistent instead of relying on the reversal.
- Made exact: webhook retries are up to three days with exponential backoff in live mode (the block said "for days"); a
  rolled signing secret stays valid for a delay chosen by the operator, up to 24 hours on that page; idempotent results
  include 500 errors but are saved only after execution begins (validation failures and concurrent conflicts are not
  saved and can be retried), and keys can be pruned after 24 hours.
- Confirmed: finalised invoice edits limited to a few fields such as memo or metadata, substantive change means a new
  invoice and voiding the old one, only drafts deletable, raw-body signature check, 2xx before slow work, duplicate event
  ids and object id plus event type, no ordering guarantee and do not order by creation time; one payment to one invoice in
  the billing engine; refund and chargeback as signed payment rows; credit balance item; written-off and imported
  invoices count as zero balance; fixed items never prorated, plan change as a repair adjustment plus a new recurring item.
- Still unsourced: numbering and counter locking, money and rounding, tax as a code, audit, dates, billing run
  idempotency, dunning, roles, exports.
Counts: 14 claims re-checked, 3 corrected or made exact.

## Related blocks
`skills/light-erp-document-flow-pitfalls`, `skills/e-invoicing-obligations-pitfalls`,
`skills/vat-handling-in-software-pitfalls`, `skills/money-arithmetic-and-rounding-pitfalls`,
`skills/inventory-stock-app-pitfalls`.
