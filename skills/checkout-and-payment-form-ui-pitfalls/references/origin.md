# checkout-and-payment-form-ui-pitfalls: origin and source stamps

> Provenance of `skills/checkout-and-payment-form-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No checkout was built, run or tested against a processor while writing it. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Stripe docs, Idempotent requests (docs.stripe.com/api/idempotent_requests), read 2026-10-20 | Vendor documentation, no licence stated; facts only, own words | key behaviour, 255 characters, 24-hour pruning in API v1, parameter mismatch, POST only (§1.3.3, §1.3.9, §1.3.10) |
| Stripe docs, Payment Intents lifecycle (French page), read 2026-10-20 | same | statuses, asynchronous processing up to days, failure returns to first state (§1.5.6, §1.5.9) |
| Stripe docs, Payment status updates (French page), read 2026-10-20 | same | retrieve after return, webhooks for fulfilment, polling caveat (§1.5.3, §1.5.4, §2.1.3, §2.6.12) |
| HTML Standard, form control infrastructure, autofill (html.spec.whatwg.org), read 2026-10-20, first 100000 characters of the page text | licence notice not seen on the page read (the copyright page URL tried returned 404); facts only | autofill tokens (§2.2.3) |
| GOV.UK Design System, Error summary, read 2026-10-20 | page states Open Government Licence v3.0 for content (MIT for code not confirmed); facts only | focus, links, placement (§2.3.2) |
| W3C WCAG 2.2 Understanding SC 4.1.3, read 2026-10-20 | W3C document licence, facts only | status messages (§2.3.2) |
| Stripe docs, Including Stripe.js (docs.stripe.com/js/including), read 2026-10-20 through WebFetch (page text), exact passage | Vendor documentation, no licence stated; facts only, own words | Load from the vendor host, no bundling or self-hosting, on every page for fraud detection, async or defer (§1.1.5, §2.4.1) |
| W3C WCAG 2.2 Understanding SC 2.2.1 and SC 2.5.8, read 2026-10-20 | W3C document licence, facts only | Time-limit options, minimum target size (§2.3.5, §2.3.7) |

No permissive source found for the checkout page-structure, privacy and performance points, searched: no other page opened. The Stripe pages contained text addressed to coding agents recommending a particular API; it was ignored, only the facts above were used.

## Own craft, not from a source
Hosted-field boundary, totals consistency, submit lifecycle and double submit, error and decline kinds, pending and unknown states, redirect and challenge return handling, page structure, accessibility, performance, privacy, test list and framework pointers.

## Removed
Server-side ambiguous-outcome handling (`unknown-payment-outcome-pitfalls`), rounding (`money-arithmetic-and-rounding-pitfalls`), tax rules (`vat-handling-in-software-pitfalls`), processor-specific API calls, subscription billing engine design, anything touching raw card data.

## Verified on 2026-10-20
Idempotency behaviour, status model, webhook-first fulfilment, return handling and autofill tokens, against one processor (Stripe) only. One correction (§1.5.3 polling). Four points added (§1.3.9, §1.3.10, §1.5.9, §2.6.12).

## Verified on the second pass, 2026-10-20
4 verified (script loading origin, time-limit options, target size, plus the Stripe.js fraud-detection note), 1 corrected (§2.4.1 said load the script on the checkout page only as the processor documents; Stripe documents every page), 0 deleted. Content security policy origins were not re-read (the page fetched listed only checkout origins in a French rendering).

## Not verified
1. **Everything not cited above is own knowledge**: sections 1.1, 1.2, 1.4, 2.2 (except 2.2.3), 2.4, 2.5 and 2.7 were not checked.
2. **Authentication behaviour** (when a challenge is required, how the processor resumes) varies by processor, issuer and region; only one processor was read, and its 3-D Secure page was not opened. Re-read your processor's documentation before relying.
3. **Compliance and consumer-law points** (card-data scope, consent wording, withdrawal rights) are method only, not legal advice.
4. **Accessibility points**, including hosted-field and challenge behaviour, are recalled public practice and were not run.
5. **Framework pointers** name features from memory; no version was checked.
6. **No number** (poll interval, timeouts, hold time) is stated; none was measured.
