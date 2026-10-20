# checkout-and-payment-form-ui-pitfalls §1 — Boundary, totals, submit and errors

Source: own craft knowledge, no external source (see origin.md). Processor facts are not stated here; check the processor's current documentation.

## 1.1 The card-data boundary
1. **Symptom: a card number shows up in a log, an error report, a session replay or a form-analytics tool.** Cause: card fields rendered by your own inputs. Use the processor's hosted fields, embedded frame or redirect page, so the values never exist in your page's memory or requests. The scope of your compliance duties depends on this choice; ask your adviser, this is not legal advice.
2. **Keep the surrounding page from observing the fields.** Exclude the payment area from session recording, heatmaps and form analytics, and from error-report breadcrumbs that capture input values (`telemetry-sensitive-data-pitfalls`).
3. **Send the processor's token or intent id, not card data, to your server.** The server charges or confirms against that reference.
4. **Content security policy matters here**: the page allows only the processor's script and frame origins, from the processor's documentation, and nothing else injects into the payment page (`csp-and-sanitiser-pitfalls`).
5. **Load the processor script from the processor's own origin, as documented**, never copied or bundled, so fixes and fraud signals reach it.
6. **Never prefill or store card fields yourself.** Saved cards are processor-held payment methods referenced by id, shown as brand and last four digits only.
7. **Never put payment values in a URL**, a local storage key, or a query string; those end up in history, referrers and logs.
8. **Test with the processor's published test values** in its test mode, never real cards, and keep test and live keys apart (`credential-lifecycle-pitfalls`).

## 1.2 Totals consistency
1. **Symptom: the order summary says 49.99 and the charge is 52.30.** Cause: totals computed in several places (cart, summary, confirmation, processor call) with different rounding, tax or discount order. Compute once on the server from the cart, return the line items and the total, and display and charge exactly that.
2. **Amounts are integers in minor units with a currency**, formatted at display (`money-arithmetic-and-rounding-pitfalls`). Never parse a formatted string back into an amount.
3. **Recompute and compare before charging.** If the cart changed since the summary was shown (price, stock, coupon expiry), stop and show the new total for confirmation rather than charging a different amount silently.
4. **Show every component that changes the total**: items, discount, shipping, tax, fees, and what the tax depends on (country, business status) (`vat-handling-in-software-pitfalls`). A line that appears only at the last step is the classic abandonment and trust defect.
5. **Show the currency and the billing period** for subscriptions: what is charged now, what recurs, when, and how to cancel (`price-change-and-billing-pitfalls`). A trial states the date the first charge occurs.
6. **Coupons and credits have visible, reversible state**: applied, invalid with the reason, expired; removing one updates the total and the processor intent in the same step.
7. **Address and country changes recompute tax and shipping** and update the amount held by the processor; the intent amount is updated or recreated, never left stale.
8. **The confirmation page and the receipt read the stored order**, not the client's last computed values; the numbers match the invoice (`invoicing-app-build-pitfalls`).

## 1.3 Submit lifecycle and double submit
1. **Symptom: two orders, two charges.** Causes: a double click, Enter pressed twice, a retry after a slow response, the back button replaying the POST, two tabs. Guard at three levels.
2. **UI guard**: on first activation, disable the button, show a busy state and keep the label meaningful ("Paying..."), and ignore further submit events in code, not only visually.
3. **Idempotency key per attempt**: generate it when the checkout session or the attempt begins, send it with the request, reuse it on every retry of that same attempt, and issue a new one only for a deliberately new attempt (`unknown-payment-outcome-pitfalls` for the server rules).
4. **Server-side uniqueness**: one open order or intent per cart; a second submit for it returns the existing state. The server owns this guarantee, the UI only avoids provoking it.
5. **Make the submit a POST followed by a redirect to a GET result page** (post, redirect, get), so a reload or back does not resubmit.
6. **Re-enabling the button after a timeout is a defect when the outcome is unknown.** Move to the pending state (§1.5) instead of offering another try that can double charge.
7. **Prevent the page from changing under the attempt**: lock the cart and amounts while the payment runs; edits during it start a new attempt with a new key.
8. **Two tabs**: the second one detects an order already paid for this cart and shows it instead of a form.

## 1.4 Errors and declines
1. **Separate the kinds of failure** and word each for the action it needs: invalid input (fix the field), authentication required or failed (complete or retry the check), declined by the issuer (use another method or contact the bank), a temporary system fault (try again later, nothing was charged or we are checking), and a configuration or integration error (not the user's to fix; show a generic message, log the detail).
2. **Never show raw processor or bank messages or codes as the user's guide.** Map machine codes to your own copy through one table; keep the code in the logs and the support reference.
3. **Do not reveal more than useful about the reason of a decline**: the issuer's reason is often withheld on purpose; do not guess ("insufficient funds") when the code does not say it.
4. **Field errors attach to the field** with a message that says what to do ("Check the expiry date"), and focus moves to the first invalid field on submit (`long-and-multistep-form-pitfalls`, `accessibility` `04-forms`).
5. **Validate early where it is free**: the hosted fields validate format as the user types; your own fields (name, address, email) follow the validation timing of the form block.
6. **Keep what the user typed after an error**, except fields the processor clears; do not reset the whole form for a decline.
7. **Offer a way forward**: try another method, change the card, pay later, contact support with the reference.
8. **Do not lock the user out after a decline**, and do not retry automatically on a decline; automatic retries of a failed payment are a billing-engine policy with its own rules (`price-change-and-billing-pitfalls`).
9. **Fraud and rate limiting appear as a neutral message** and a support route, not as an accusation, and never leak how the check works.

## 1.5 Pending and unknown outcomes
1. **Three honest states beyond success and failure**: processing (we sent it, waiting), action required (the user must complete a step), and unknown (we cannot tell yet). Each has its own screen and copy.
2. **Symptom: the page says "payment failed" and an email later says "paid".** The UI showed failure for a timeout or a closed window. Show "We are checking your payment, do not pay again", and resolve through the server's evidence path (`unknown-payment-outcome-pitfalls`).
3. **Update the page when the state resolves**: poll the order status endpoint with a gentle backoff or listen for a push, and stop at a sensible limit with a message and an email promise rather than spinning forever.
4. **Never mark the order paid in the browser.** The paid state comes from the server after confirmation by the processor's signed notification or a lookup (`unknown-payment-outcome-pitfalls`, `laravel-http-client`).
5. **Send the confirmation by email and show it in the account**, so a user who left the page can still find the outcome (`laravel-mail-via-notifications`).
6. **A delayed method** (bank transfer, voucher, some wallets) is pending by design; show the instructions, the deadline and where to see the status, and do not call it success until settled.
7. **Keep a support reference on every non-success screen**, and make it copyable, so staff can find the attempt without asking for card details.
8. **Cart and stock during pending**: hold them for a stated time, release them on expiry, and tell the user what happens if payment arrives after release.
