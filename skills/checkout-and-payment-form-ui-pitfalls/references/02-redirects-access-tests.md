# checkout-and-payment-form-ui-pitfalls §2 — Redirects, accessibility, performance and tests

Source: own craft knowledge, except the points marked with a citation (third pass 2026-10-20 added Stripe's 3-D Secure overview and WCAG 2.2 Understanding SC 1.3.5 and SC 3.3.7, facts only), checked on 2026-10-20 (see origin.md). Unmarked points have no source.

## 2.1 3-D Secure and other redirects, and the return
1. **Why it exists**: for many card payments the issuer may require the cardholder to authenticate, in a frame, a challenge window or a full redirect to the bank, after which the user comes back. Your UI must treat that as a normal branch, not an error. Which payments require it is decided by the issuer, the processor and the rules that apply; do not assume it will not happen. Stripe's overview says the issuer may ask the cardholder to identify (password, one-time code, biometrics), that strong customer authentication rules in the European area, the United Kingdom, India, Japan and Australia can make it mandatory for cards, and that elsewhere it is optional (Stripe, 3-D Secure).
2. **Use the processor's confirm-and-handle-action call** so the library opens the challenge and resumes, rather than building the redirect by hand, unless a redirect payment method needs it.
3. **The return URL is a hint, not proof.** Symptom: the user lands on the success page because the URL contains "success", or on "failed" because they closed the bank tab. On return, read the order or intent state from your server, which got it from the processor, and render by that state (§1.5). Stripe's documentation likewise has the page retrieve the intent status after the return and treats a still-pending authentication as an unfinished payment (Stripe, verifying payment status).
4. **Return pages must work without the original page state**: a new tab, a different browser, a mobile app switching back, a cleared session. Identify the order by a signed, unguessable reference, and require sign-in or a verified link before showing personal details.
5. **Make the return idempotent**: reloading it, or arriving twice, must not repeat any action; the page reads state and shows it.
6. **Cancel and back from the bank page** return to a page that says nothing was charged only if the server knows that; otherwise show the pending or unknown path. Offer to retry or choose another method.
7. **Timeouts at the bank**: the user may wait on the issuer page for minutes. The checkout page that spawned it shows the "action required" state and a way back, and the server expires the attempt cleanly.
8. **Keep the amount and order locked across the redirect**, and recheck on return that cart and order still match (§1.2).
9. **Frame or window blockers**: popup blockers and in-app browsers can break the challenge. Prefer the processor's recommended mode, test in the browsers and in-app webviews your users use, and show a plain instruction when the window did not open.
10. **Mobile apps**: return to the app by a verified link or the processor's documented mechanism, and re-read state on resume; the app may have been killed while the user was at the bank (`flutter-monetization-pitfalls` for store-billing differences).
11. **Wallet and redirect methods** (bank-redirect, wallet buttons) share these rules: state from the server, return page by reference, pending by design where settlement is delayed.
12. **Do not log the return query string in full**; it can carry tokens or payment references that should not reach analytics (`telemetry-sensitive-data-pitfalls`).

## 2.2 Page structure
1. **Keep checkout short and linear**: contact, delivery, payment, review, or one page with those sections, with a visible summary at all times and no unrelated navigation (`long-and-multistep-form-pitfalls`).
2. **Guest checkout is allowed unless the product needs an account**; ask for an account after payment, not before.
3. **Autofill works** (WCAG 1.3.5 asks that the purpose of a field collecting information about the user be exposed programmatically, with the autocomplete attribute as the sufficient technique; browser guessing is not enough, and a field not about the user, such as an amount, is outside it): correct autocomplete attributes on name, email, address and phone fields, and no tricks that defeat the browser's helpers (`international-input-pitfalls`). The standard tokens include street-address, postal-code and country (a two-letter code; country-name for the name), prefixed shipping or billing, with an optional section-name prefix when a form holds two addresses (HTML Standard, autofill). Card tokens (cc-number, cc-exp, cc-csc) exist, but with hosted fields the processor owns them.
3a. **Do not ask twice for what the user already gave in the same process** (WCAG 3.3.7: previously entered information must be auto-filled or selectable, and a checkout that includes a third-party payment step is in scope). A "billing address same as delivery" choice satisfies it; re-typing a newly created password is allowed. The browser's own autofill does not count, the site must supply the data.
4. **Payment method choice is stated and defaults sensibly**: show the methods available for this country and currency only.
5. **The final button states the action and the amount** ("Pay 49.99 EUR"), and for subscriptions the recurrence, so the click is informed.
6. **Terms and consent** are links the user can open without losing the form; the wording of required consents and withdrawal rights is a legal matter for your adviser, not this block, and not legal advice.
7. **Trust cues are factual**: the processor's name, the accepted methods, the refund contact. Do not fake badges or urgency counters.

## 2.3 Accessibility
1. **Hosted fields need accessible names**: a visible label tied to each field, and for frames a title that says what the field is; test that a screen reader reads the label and error for each, since the field lives in another document (`accessibility`, `04-forms`).
2. **Errors are announced and linked**: an error summary at the top that takes focus on a failed submit, links to each field, and each field error is tied to its input; a decline message is announced in a live region without losing the typed values. The GOV.UK Design System places the summary at the top of the main area, above the page heading, moves focus to it on load and links each item to its field (GOV.UK, error summary). Status text that does not take focus is exposed by role (WCAG 2.2 SC 4.1.3).
3. **The busy state is communicated**: the button announces "Paying", a status region announces processing and the result, and focus does not jump (`in-app-notifications-pitfalls` §2.3 for the live-region pattern).
4. **The 3-D Secure frame or window is reachable and escapable**: focus moves into the challenge, returns on close, and a keyboard user can cancel; verify the processor's component, do not assume.
5. **Do not rely on timeouts shorter than a person needs**: a session expiring mid-form warns first, extends easily, and preserves the cart. WCAG 2.2 SC 2.2.1 (level A) lets a user turn off, adjust, or extend a content time limit (warning before expiry with at least 20 seconds to extend), with an exception for real-time events such as an auction; a stock hold needs the same warning.
6. **Totals are text, not images**, with a clear structure for the summary (a description list or table) and the changed total announced after a coupon or a country change.
7. **Target size and spacing** (at least 24 by 24 CSS pixels or spaced so, WCAG 2.2 SC 2.5.8, level AA) keep the pay button from being hit by accident or hard to hit on touch, with the destructive "cancel order" apart from it (`responsive-layout`).
8. **Contrast and focus visibility** are checked in the processor's themed fields too; pass your theme tokens to them where the processor allows it.
9. **Language and format**: amounts, dates and addresses follow the locale and the language attribute is set (`locale-value-formatting-pitfalls`, `i18n-message-format-pitfalls`).

## 2.4 Performance
1. **Decide where the processor script loads, per the processor's documentation, and load it without blocking.** Corrected on 2026-10-20: Stripe documents the opposite of checkout-only for its script, recommending it on every page so its fraud detection sees browsing behaviour (Stripe, including Stripe.js), and describes async or defer loading so it does not block rendering. Loading it site-wide widens the CSP surface and your privacy notice, so weigh that against the fraud benefit and write the choice down; another processor may differ.
2. **Create the intent or session early but not wastefully**: before the user pays, not for every cart view; reuse it while the cart is unchanged, and update it instead of recreating.
3. **Do not block the first paint on the payment script**; render the summary and form skeleton, and enable the button only when the hosted fields report ready.
4. **Handle the slow processor**: show the busy state, set a client timeout that moves to the pending state, not to failure (§1.5).
5. **Avoid layout shift** when the payment frame mounts: reserve its height (`webperf`).
6. **Measure the funnel and the failures by kind** (`event-tracking-plan-pitfalls`), without card data or full return URLs, and with consent where required.

## 2.5 Privacy
1. **Collect only what the payment and delivery need.** Extra fields cost conversion and create data to protect (`dsar-handling-pitfalls` for what you must later find and delete).
2. **Order records keep the payment reference and brand and last four digits**, never the card number or security code.
3. **Customer-facing receipts and emails contain no full card data**, and the support tools show the same masked view (`field-and-row-permission-ui-api-pitfalls`).
4. **Logs hold the support reference and the processor's event id, not the payload** with personal data (`telemetry-sensitive-data-pitfalls`).

## 2.6 Tests
1. **Totals parity**: for a cart with discount, tax and shipping, assert the summary, the intent amount, the confirmation and the invoice are the same integer.
2. **Cart changed mid-checkout**: change a price or expire a coupon before submit, assert the user sees the new total and no silent charge.
3. **Double submit**: double click, press Enter twice and replay the request with the same key, assert one order and one charge in the processor's test mode.
4. **Back and reload**: after success, go back and reload, assert no resubmission and the result page shows the stored order.
5. **Decline kinds**: use the processor's published test values for declines, authentication required and processing errors; assert each message, that typed fields survive and focus lands on the right place.
6. **Redirect return**: complete, fail, cancel and abandon the challenge; assert the return page reads server state in each, and that a forged success query string shows nothing paid.
7. **Unknown outcome**: simulate a timeout, assert the pending screen, no second submit, and the update when the notification arrives (`unknown-payment-outcome-pitfalls`).
8. **Two tabs**: pay in one, open the other, assert it shows the paid order.
9. **No card data leak**: assert no request, log line or analytics event of your own contains the test card number or security code.
10. **Accessibility**: assert names for hosted fields, the error summary with focus, the status announcement and a keyboard-only pass including the challenge; run an automated check (`playwright-e2e-pitfalls`).
11. **Locale**: run the flow with a comma-decimal currency and a right-to-left locale (`rtl-and-bidi-layout-pitfalls`).
12. **Return from a payment that needs more**: retrieve an intent that is still waiting for an authentication action, assert the page says the payment is not complete and offers the way back, not success (Stripe, verifying payment status).

## 2.7 Framework pointers (reference only)
1. **Processor libraries** provide hosted-field components and a confirm call that handles authentication actions; read the current documentation for your processor and version before relying on any behaviour named here.
2. **Laravel**: the server creates the order and the processor intent, exposes an order status endpoint, and handles the processor's signed notifications as the source of truth (`laravel-http-client`, `laravel-idempotent-jobs`, `laravel-post-may-run-twice`, `laravel-dispatch-after-commit`).
3. **React or Nuxt**: the checkout is a state machine (editing, submitting, action required, processing, paid, failed, unknown) rather than a set of booleans, with the order query keyed by reference and polled while pending (`data-fetching-state-conventions`, `react-nextjs-conventions`).
4. **Vuetify or similar kits**: their text fields are not hosted fields; use them for contact and address only, and check dialog and focus behaviour around the challenge (`vue-nuxt-vuetify-conventions`).
5. **Mobile stores** have their own billing rules for digital goods; see `flutter-monetization-pitfalls` before adding a card form to an app.
