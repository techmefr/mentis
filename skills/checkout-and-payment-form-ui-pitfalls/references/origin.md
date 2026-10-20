# checkout-and-payment-form-ui-pitfalls: origin and source stamps

> Provenance of `skills/checkout-and-payment-form-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No checkout was built, run or tested against a processor while writing it. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| None read | n/a | No MIT, Apache-2.0 or CC BY source on checkout interfaces was found and read with its LICENSE file; none was opened. Processor documentation was not consulted |

## Own craft, not from a source
Hosted-field boundary, totals consistency, submit lifecycle and double submit, error and decline kinds, pending and unknown states, redirect and challenge return handling, page structure, accessibility, performance, privacy, test list and framework pointers.

## Removed
Server-side ambiguous-outcome handling (`unknown-payment-outcome-pitfalls`), rounding (`money-arithmetic-and-rounding-pitfalls`), tax rules (`vat-handling-in-software-pitfalls`), processor-specific API calls, subscription billing engine design, anything touching raw card data.

## Not verified
1. **Everything is own knowledge**: no external claim was checked against a source or a processor's documentation.
2. **Authentication behaviour** (when a challenge is required, how the processor resumes, which methods are delayed) is recalled practice and varies by processor, issuer and region. Re-read the current processor documentation before relying.
3. **Compliance and consumer-law points** (card-data scope, consent wording, withdrawal rights) are method only, not legal advice.
4. **Accessibility points**, including hosted-field and challenge behaviour, are recalled public practice and were not run.
5. **Framework pointers** name features from memory; no version was checked.
6. **No number** (poll interval, timeouts, hold time) is stated; none was measured.
