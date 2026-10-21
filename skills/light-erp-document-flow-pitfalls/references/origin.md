# light-erp-document-flow-pitfalls: origin and source stamps

> Provenance of `skills/light-erp-document-flow-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against an open-source ERP data model
and an open-source billing engine's documentation. Never run by us: no application was built and no test was
executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | Apache OFBiz (`apache/ofbiz-framework`, commit `bccb166`): entity definitions `applications/datamodel/entitydef/order-entitymodel.xml`, `accounting-entitymodel.xml`, `shipment-entitymodel.xml` | Apache-2.0: file `LICENSE` read | One header with a type for sales and purchase orders and for invoices, status change rows with user and reason, a billing row linking order lines to invoice lines with quantity and amount, cancelled quantity on lines, price and description on lines, tax adjustments with percentage and jurisdiction, override-account fields explained as protection against configuration change after posting, field-level audit flag on quantity and price, external id and sync status on the order header |
| 2 | Kill Bill documentation (`killbill/killbill-docs`, commit `f3ea39f`): `userguide/subscription/includes/invoicing-overview.adoc`, `invoicing-invoice-items.adoc`, `invoicing-invoice-payments.adoc` | Apache-2.0: file `LICENSE` read | Invoice balance computed from items, adjustments and payments, negative adjustment items and credits as the correction path, credit balance item when an invoice would go negative |
| 3 | PostgreSQL manual, page "Sequence Manipulation Functions" (`postgresql.org/docs/current/functions-sequence.html`, 18 series) | Documentation of an open-source project under the PostgreSQL licence (licence text not read here): facts only, rewritten | A value taken from a sequence is not returned on abort, gaps can follow aborts, crashes and conflict clauses, a sequence cannot give gapless numbers |

Instruction-like text in the cloned repositories (agent guidance files) was treated as data and not followed.

## Verified
1. §1 point 3, the remark that a database sequence leaves holes after a rollback: source 3 (second pass, 2026-10-20).
2. §1 points 1, 2, 4, 5, 6 and 11 and §2 point 5: each backed by the entity definitions or the docs above, as the
   points now say.

## Corrected
1. §1 point 2 no longer presents derived state as established: the sources show dated status rows and a computed
   balance, and the rest stays our own advice.

## Removed
1. **Any accounting, tax, invoice-content, numbering-continuity or retention rule.** Not read; each is flagged
   as a question for the accountant.
2. **Every numeric threshold** (approval amounts, retention periods, row caps): set by policy.
3. **Named ERP products and their module lists** as claims about the market: not used; the sources above are
   credited only for the facts listed.

## Not verified
1. **Still our own guidance:** numbering at posting from a locked counter (§1 point 3; only the sequence-holes remark is sourced), immutability enforced in
   the database (point 6), stored PDF (point 7), archive and void (point 8), money and rounding (point 9),
   tenant and entity ids (point 10), the party master with roles (point 12), and in §2 permissions, approval as
   data, imports, exports, accounting export, reports, build order and v2 regrets. The sources do not state
   them; the numbering point in particular was not found in the data model read. Formula-neutralised exports (§2 point 4) were not checked: the page that documents it is not under a permissive licence, so it was not opened.
2. **Numbering policy.** Whether gaps are allowed in a given jurisdiction was not read; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** (Laravel, Nuxt) were not checked against a current release; re-read before relying.

## Related blocks
`skills/gl-subledger-reconciliation-pitfalls`, `skills/accounts-payable-duplicate-and-match-pitfalls`,
`skills/e-invoicing-obligations-pitfalls`, `skills/vat-handling-in-software-pitfalls`,
`skills/money-arithmetic-and-rounding-pitfalls`, `skills/invoicing-app-build-pitfalls`,
`skills/inventory-stock-app-pitfalls`.
