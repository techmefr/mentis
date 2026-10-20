# ecommerce-store-quality-pitfalls: origin and source stamps

> Provenance of `business/ecommerce-store-quality-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from general e-commerce practice, never run on a real store by us. The block
structures a check; it certifies nothing, and the store owner decides what changes (`business/README.md`).

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| Google Merchant Center product data specification and a policy page on listing disapproval | Product documentation, no licence granted on the text; facts only, rewritten, no limit figure reused | Identifier stability, GTIN validity, variant group identifier, availability values and matching rule, price format and tax by market, title rules, disapproval consequences (§1.1, §1.2, §1.3, §3.1.1) |
| Your Europe (European Union) pages on pricing and payments and on returns | EU official portal; licence notice not read, facts only, EU scope only, not legal advice | Total price before purchase, no late delivery cost, pre-ticked extras not consent, card surcharge rule, withdrawal period and return cost (§2.1.1, §2.2.6, §3.2.1) |
| An MIT marketing skills repository named by the gap review | not opened | Nothing; no permissive source for checkout or measurement practice was read |

## Verified
Feed identity, availability and price-matching points and the EU price-display, pre-ticked extras and return-cost points
listed above. Where a point cites a page it is a confirmation of the existing point, not a legal opinion.

## Left out on purpose
Channel-specific feed attribute names, limits and approval rules (each platform's own, changing). Benchmark
conversion, cart-abandonment and return rates. Price-comparison and tax rates by country. Platform and plugin
recommendations. Payment-provider integration detail. Legal texts on withdrawal rights, price statements, consent
and retention: method only, not legal advice. Any source with no open licence: not opened.

## Not verified
1. **Only the feed and EU consumer points listed above were read**; checkout form practice, payment failure handling,
   returns process, measurement and reference-price rules are one author's practice. The EU pages did not cover
   reference ("was") prices or refund deadlines. Searched: one shopping-feed spec and the EU portal.
2. **Consumer, tax and consent rules** mentioned are pointers to check with a qualified person, and were not
   checked against any law for this block.
3. **Channel behaviours** were read for one channel only (feed refresh timing and diagnostics were not on the pages
   read); other platforms differ.
4. **Never run by us** on a real store.
5. Re-read before relying; add an open-licence source when one is found.

## Own guidance (not sourced)
Attribute filling and image practice (§1.2.2, §1.4), guest checkout and form practice (§2.2), payment failure handling
(§2.3), reference price log (§3.1.3), return process and policy consistency (§3.2), confirmation (§3.3) and the
whole-week, margin-aware test rule (§3.4).

## Related blocks
`skills/vat-handling-in-software-pitfalls`, `business/price-change-and-billing-pitfalls`,
`business/pricing-and-packaging-pitfalls`, `business/marketing-claim-substantiation-pitfalls`, `skills/seo`,
`skills/experiment-design-pitfalls`, `skills/funnel-and-cohort-definition-pitfalls`, `business/data-protection`, `skills/source-freshness`.
