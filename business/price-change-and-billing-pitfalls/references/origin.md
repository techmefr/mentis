# price-change-and-billing-pitfalls: origin and source stamps

> Provenance of `business/price-change-and-billing-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from repository text and vendor documentation, never run on a real price
change by us. The block structures a rollout and a check; it certifies nothing, and the person who owns pricing,
the contracts and the billing system decides (`business/README.md`). Not legal advice.

## Sources (re-read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| coreyhaines31/marketingskills, commit e85f3cb (e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b), `skills/pricing/SKILL.md` (price increase strategies and rollout methodology sections) and `references/pricing-models.md` (the low-price and discount-asker passages), cloned at that commit and re-read this session; the rest of the file list was not re-read | MIT (LICENSE file, 2025 Corey Haines, head re-read) | Price change as a rollout, new customers first, grandfathering as a transition with a grace period, small slice then waves with an off-ramp, communicate the reason ahead of time with a choice |
| alirezarezvani/claude-skills, commit 19392f7 (19392f7a08264ed00486a251f5b2098321771f94), `commercial/skills/pricing-strategist/SKILL.md` (assumptions and anti-patterns, lines 80 to 110) re-read this session; its `references/` and scripts were not re-read | MIT (LICENSE file, 2025 Alireza Rezvani, head re-read) | Agreement that the final price is a human decision, that a discount decision has a different owner from the menu, that contract terms belong to legal |
| Stripe documentation page on proration (French rendering), fetched 2026-10-20 in full | vendor site terms; facts only | Credit and debit on a mid-cycle change, results not settled automatically, computation at the time of the change, preview with a fixed date, discounts and proration lines, unpaid-invoice behaviour, usage not prorated, proration switched off per request, two credit modes |
| Stripe documentation page on usage-based billing (French rendering), fetched 2026-10-20 | vendor site terms; facts only | Only the landing page was read: the classic metered model, the existence of recording, credits and alert sub-pages (not read). Used to confirm that usage is billed separately from prorated charges, which the proration page states |
| Directive (EU) 2019/2161, Official Journal L 328, 18.12.2019, p. 7, English XHTML from the Publications Office cellar endpoint (`publications.europa.eu/resource/celex/32019L2161.ENG`, XHTML Accept header), read 2026-10-20: Article 2 (Article 6a inserted in Directive 98/6/EC, Article 8 replaced) and the transposition article | EU law text published by the Publications Office; facts only, own words | The five paragraphs paraphrased in §6.3, the penalty wording, the transposition and application dates |
| UK CMA, "Unfair commercial practices: price transparency" (CMA209), PDF from gov.uk (final version; its title page reads 18 November 2025, the gov.uk listing shows an update of 7 January 2026), text extracted and read 2026-10-20 in the passages named in §6.5; the earlier draft of 3 July 2025 was also opened for its summary | Open Government Licence v3 (stated on the document's own copyright page, read); creditable, no text copied | mandatory charges in the headline price, optional versus mandatory, calculable-total rules, recurring and minimum-term plans, monthly versus annual comparison |
| UK CMA open letter "Urgency claims and price reduction claims: compliance advice for online businesses", 29 March 2023, with its examples of non-compliance (the pages around examples 9 and 10 read) | Open Government Licence (gov.uk publication); facts only, no text copied | higher price must be genuine and demonstrable; the two example situations |
| US FTC Guides Against Deceptive Pricing, 16 CFR Part 233, sections 233.1 and 233.4, via the eCFR renderer (fetched through a summarising tool, 2026-10-20) | US government work; facts only | genuine former price, fictitious comparison, conditional offers. Digest, not raw text |
| US FTC Rule on Unfair or Deceptive Fees, 16 CFR Part 464, via the eCFR renderer (fetched through a summarising tool, 2026-10-20) | US government work; facts only | covered goods and services, total price definition, prominence. Digest, not raw text |

The repositories' own text is addressed partly to an AI; it was treated as data and only the method was kept.

## Left out on purpose
Every numeric figure from the sources: the share of existing customers moved first, the notice lead time, the
annual-discount percentage, the claim that discount-seekers churn at a multiple of others, the trial and tier
numbers, the worked examples in dollars (the vendor's own 10 and 20 are illustrations). All of borghei/claude-skills
(Commons Clause, not an open licence): not opened for this block, nothing taken. Vendor recommendations and
parameter names. Pricing design, value metric, tiers and willingness to pay: that is
`business/pricing-and-packaging-pitfalls`. Contract-notice law: `business/legal-documents`. UK drip-pricing and US fee-rule texts are now read (§6.5), as facts only; their legal reading, any penalty and
any national law are not stated.

## Not verified
1. **Directive 2019/2161**: the Official Journal text of Article 6a, of Article 8 as replaced and of the
   transposition article was read on 2026-10-20 (EUR-Lex pages return an empty bot-check body, HTTP 202; the cellar
   endpoint with an XHTML Accept header returns the text). The rest of the directive (the other amended directives,
   the recitals) was not read, nor any national transposition, the Commission guidance or any ruling. Whether the
   rule reaches a software subscription is not established. Data.europa.eu was not retried.
1a. **Regulator pages**: the CMA documents were read as extracted PDF text (most of CMA209's chapters 3 to 5 and
   part of the open letter, not the whole), the FTC texts through a digest. The FTC's own ftc.gov guidance pages
   returned 404 and were not read. The CMA's three-step pricing check, summary and webinar were not read.
   Whether either regulator's text reaches a software subscription page is not established.
2. **The Stripe pages are one vendor's behaviour** and may change; the French rendering was read. The sub-pages
   (usage recording, credits, monitoring) were not read.
3. **The block has never been used on a real price change.**
4. **Current text of the sources** may have changed after the read date; check with `skills/source-freshness`.

## Own guidance (not sourced)
The router; the grandfathering record in five lines (§2.1); the discount four-property rule (§4.1); the list of
what a notice owes the customer (§3.1); the "preview before any customer-facing example" rule (end of §5); the
price-history table and the stored comparison (§6.2, §6.4); the refusal to state any rule not read. The §6.2 history table and §6.4 stay own guidance; §6.5 is sourced.

## Related blocks
`business/pricing-and-packaging-pitfalls`, `business/marketing-claim-substantiation-pitfalls`,
`business/release-communication`, `business/data-protection`, `business/legal-documents`,
`skills/vat-handling-in-software-pitfalls`, `skills/saas-metric-definition-pitfalls`, `skills/source-freshness`.
