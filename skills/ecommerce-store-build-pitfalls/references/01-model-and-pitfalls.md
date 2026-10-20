# ecommerce-store-build-pitfalls §1 — Model and pitfalls

> Part 1 of `skills/ecommerce-store-build-pitfalls`. Read it when a schema or the checkout flow is designed.
> Craft knowledge, no external source read. Each point gives the symptom, the check and the fix. Not legal advice.

1. **Product, variant and stock keeping unit are different things.** Symptom: a size or colour is a separate
   product, or stock is kept on the product so one size sells out the whole line. Fix: a product (title,
   description, brand), variants under it (the option values), a unique sellable unit with its own code, price,
   weight and stock state, and option definitions with stable ids so renaming "Red" does not rewrite history.
   Check: sell out one variant and confirm the others stay available. Bundles and kits are their own entity
   that expands to units at order time.
2. **A price is a record with a currency, not a column.** Symptom: a sale price overwrites the base, a second
   currency needs a rewrite, a total moves by cents. Fix: integer minor units plus a currency code on every
   amount (see `skills/money-arithmetic-and-rounding-pitfalls`), prices as rows with a currency, an optional
   customer group and a validity period, the displayed price chosen by a single function, and whether a price
   includes tax stored as a field, never assumed. Converting at a rate is a display or a payment decision that
   names the rate and its time.
3. **The server owns every total.** Symptom: a buyer edits a request and pays less, or the cart shows a stale
   price after a catalogue change. Check: change the price while an item is in a cart, then check out. Fix:
   the cart stores references and quantities, not prices; the checkout recomputes lines, discounts, shipping,
   tax and total on the server from current data; if the total differs from what the buyer last saw, show the
   difference and ask again before taking payment. Discount codes are rules with limits (per customer, total
   uses, dates, stacking) evaluated in one place and recorded on the order with the amount they gave.
4. **Cart and checkout are states, and a cart is not an order.** Typical states: open cart, checkout started
   (address and shipping chosen), payment pending, paid, abandoned, converted. Symptom: a refreshed page or two
   tabs create two orders, or an abandoned cart holds stock for ever. Fix: allowed transitions checked in one
   place (see `skills/laravel-recognise-state-machine-or-pipeline`), a version or token on the checkout so a
   stale tab is rejected, an expiry on abandoned checkouts, and a merge rule when a guest cart meets a logged-in
   cart. Merge adds quantities up to availability and tells the buyer what changed.
5. **Payment and order stay consistent through one idempotent step.** Symptom: money is taken and there is no
   order, or one payment creates two orders, because the browser closed or a webhook came twice. Check: kill
   the request after the provider confirms, and replay the event. Fix: create the order record before asking
   for payment in a pending state or keep a checkout record that holds everything needed; confirm from the
   provider's signed event, not the redirect; a unique key on the provider payment id so a replay is a no-op;
   and a reconciliation job that finds paid checkouts with no order and orders pending with no payment (see
   `skills/unknown-payment-outcome-pitfalls` and `skills/laravel-idempotent-jobs`). Never store card data; keep
   only the provider's reference and display fields.
6. **An order line is a snapshot.** Symptom: renaming a product, changing a price or deleting a variant alters
   past orders and invoices. Fix: copy onto the line the name, option values, unit code, unit price, currency,
   discount amount, tax rate applied, tax amount and the product id as a reference only; copy the shipping and
   billing address onto the order, not a link to the address book; and keep the invoice or receipt tied to
   these values (see `skills/invoicing-app-build-pitfalls`). Check: edit the product after a sale and reopen
   the order.
7. **Stock is reserved at a defined step and released on a defined event.** Symptom: two buyers pay for the
   last unit, or reserved stock never returns. Fix: choose the reservation point (add to cart, checkout start
   or payment) and write it down; reserve with a conditional update or a lock so the decrement cannot go below
   zero; give reservations an expiry and a release on cancellation, payment failure and refund; and keep
   available, reserved and on-hand as separate figures (see `skills/inventory-stock-app-pitfalls`). Overselling
   policy (backorder allowed or not) is a per-unit setting, not a code path.
8. **Tax is a computed and stored result.** Symptom: a rate change or a buyer moving country re-prices old
   orders, or a total is rounded differently on the screen and the invoice. Fix: determine tax from data you
   store (product tax class, ship-to and bill-to country, buyer type, whether the price is tax-inclusive),
   compute per line or per order by one documented method, store rate, base and amount on the line, and keep
   the computation in one module used by cart, checkout, invoice and refund (see
   `skills/vat-handling-in-software-pitfalls`). Which rates, thresholds and place-of-supply rules apply is a tax
   question for a qualified person; no rule is stated here.
9. **Fulfilment, returns and refunds are records.** Symptom: a refund is a negative order, a partial return
   cannot be expressed, or a refund exceeds what was paid. Fix: shipments (lines and quantities, carrier,
   tracking, status) separate from the order so partial shipping works; a return request with lines, reason and
   states (requested, approved, received, inspected, closed); refund records against the order or payment with
   an amount, a currency, a reason and a provider refund id; a check that cumulative refunds do not exceed the
   amount paid; a decision on whether returned stock goes back on sale; and a credit document when the
   business issues invoices. The return window and rights are legal and policy questions; the checkout and the
   confirmation must state the same policy (see `business/ecommerce-store-quality-pitfalls`).
10. **Order status is derived from facts where possible.** Symptom: "shipped" is set by hand while no shipment
    exists, or status disagrees with payment. Fix: keep separate dimensions (payment status, fulfilment status,
    return status) rather than one overloaded field, derive the displayed summary from them, and write every
    change to a history table with actor and time.
11. **Addresses and contact data are validated and stored precisely.** Country as a code, postal code and phone
    stored as text, an address copy per order, and a normalised email for guest lookup. Symptom: a leading
    zero lost, a country mismatch between shipping and tax. Validate for deliverability by the carrier's rules
    where available, not by a single regular expression for the world.
12. **Delete and erase differently.** Symptom: deleting a customer or a product cascades to orders and
    totals change. Fix: archive products and customers, restrict foreign keys (see
    `skills/laravel-no-cascade-delete`), keep orders and financial records for the period the business must
    retain them, and run an audited routine that anonymises personal fields when an erasure request is
    accepted (see `business/data-protection`). The retention period is a legal question.
13. **Time is stored precisely.** UTC timestamps, the store's time zone for cut-offs and promotion windows, the
    buyer's zone for display. Symptom: a sale ends hours early for some buyers, or a daily report splits orders
    differently from finance.
