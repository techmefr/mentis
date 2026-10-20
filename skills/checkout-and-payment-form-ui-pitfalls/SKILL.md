---
name: checkout-and-payment-form-ui-pitfalls
description: "Use when the user-interface side of a checkout or payment form is designed, written or reviewed, whatever the framework or processor: order summary and totals consistency, error and decline states, double submit and back-button replays, 3-D Secure and other redirects with the return page, pending and unknown outcomes shown honestly, hosted fields so raw card data never touches your code, plus accessibility, performance and the tests that catch them. UI side only; not legal advice."
---

# checkout-and-payment-form-ui-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the screen where a user decides to pay. The premise: **the checkout UI
is a view of server-side truth, and every defect shows a number or a state the server does not hold**: a total that
differs between summary and charge, a button pressed twice and charged twice, a bank redirect that returns to a
page that says "failed" for a payment that succeeded, a decline message that blames the wrong thing, a card field a
screen reader cannot name. The server side of an ambiguous outcome (timeout as unknown, idempotency, resolving by
evidence) is `unknown-payment-outcome-pitfalls`; amounts and rounding are `money-arithmetic-and-rounding-pitfalls`;
tax is `vat-handling-in-software-pitfalls`; billing changes are `price-change-and-billing-pitfalls`; invoices are
`invoicing-app-build-pitfalls`; compliance scoping is `fintech-compliance`; address and name fields are
`international-input-pitfalls`; form timing and drafts are `long-and-multistep-form-pitfalls`; accessibility is
`accessibility`. This block never collects, stores, logs or transmits raw card numbers: it uses the processor's hosted
fields or redirect.

## When
- A cart summary, checkout, payment form, subscription signup or update-card screen is built or changed.
- A user reports "charged twice", "it said failed but I was charged", "the total changed", "the bank page led nowhere".
- A new payment method, redirect flow, coupon or tax display is added.

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Card data boundary, totals consistency, submit lifecycle, double submit, errors and declines, pending outcomes | the form, the submit button or the messages are written | [`01-boundary-totals-submit-errors.md`](./references/01-boundary-totals-submit-errors.md) |
| 2 | 3-D Secure and redirects with return, accessibility, performance, privacy, tests, framework pointers | an authentication or redirect step, the accessibility pass or the tests are written | [`02-redirects-access-tests.md`](./references/02-redirects-access-tests.md) |

## Output / checkpoint
A change is done when: card data enters only the processor's hosted fields or page; the summary and the charge are
read from one server-computed total; the submit action is guarded and idempotent per attempt; every return from a
redirect is resolved from server state; pending and unknown outcomes have their own screen; messages separate user
fixable declines from system faults; and the tests in §2.6 exist. No checkpoint is written: a craft block, 🟡,
nothing here was run against a processor.

## Guardrails
- Let the processor's hosted fields or page take the card data (§1.1). Never let a card number, expiry or security code reach your server, logs, analytics or client state.
- Compute totals once on the server and display that value (§1.2). Never recompute the amount in the browser and charge a different one.
- Disable submit on first press and attach an idempotency key per attempt (§1.3). Never rely on the disabled button alone.
- Decide the result of a redirect from server state, not from the query string (§2.1). Never show success because the return URL says so.
- Show unknown and pending as such (§1.5). Never show "failed" when the outcome is not known, or invite a second charge.
- Facts about a processor or library are for the date stamped in `references/origin.md`; re-read before relying.

## Origin
Own craft knowledge, with points checked on 2026-10-20 against the payment processor Stripe's public documentation (idempotency, payment status lifecycle; facts only, credited), the HTML autofill field names, the GOV.UK Design System error summary and WCAG 2.2 Understanding 4.1.3. Every other point stays unsourced. Details in
[`references/origin.md`](./references/origin.md).
