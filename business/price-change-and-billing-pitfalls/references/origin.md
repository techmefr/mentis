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
| Directive (EU) 2019/2161, Article 2(1) inserting Article 6a into Directive 98/6/EC, read on the legislation.gov.uk copy of the text (fetched through a summarising tool that returned the paragraphs as short quotations), 2026-10-20 | public legal text; a mirror, not the official journal | The five paragraphs paraphrased in §6.3 |

The repositories' own text is addressed partly to an AI; it was treated as data and only the method was kept.

## Left out on purpose
Every numeric figure from the sources: the share of existing customers moved first, the notice lead time, the
annual-discount percentage, the claim that discount-seekers churn at a multiple of others, the trial and tier
numbers, the worked examples in dollars (the vendor's own 10 and 20 are illustrations). All of borghei/claude-skills
(Commons Clause, not an open licence): not opened for this block, nothing taken. Vendor recommendations and
parameter names. Pricing design, value metric, tiers and willingness to pay: that is
`business/pricing-and-packaging-pitfalls`. Contract-notice law: `business/legal-documents`. The FTC rule on unfair
fees and the UK price-transparency rules: not read (the pages returned 404 or a redirect), so nothing is stated.

## Not verified
1. **The Directive text was read on a mirror**, through a tool that summarises; EUR-Lex returned an empty page.
   The paragraphs match the structure of the directive but the official journal text was not read, nor the
   national transposition, nor the Commission guidance, nor any ruling. Whether the rule reaches a software
   subscription is not established.
2. **The Stripe pages are one vendor's behaviour** and may change; the French rendering was read. The sub-pages
   (usage recording, credits, monitoring) were not read.
3. **The block has never been used on a real price change.**
4. **Current text of the sources** may have changed after the read date; check with `skills/source-freshness`.

## Own guidance (not sourced)
The router; the grandfathering record in five lines (§2.1); the discount four-property rule (§4.1); the list of
what a notice owes the customer (§3.1); the "preview before any customer-facing example" rule (end of §5); the
price-history table and the stored comparison (§6.2, §6.4); the refusal to state any rule not read.

## Related blocks
`business/pricing-and-packaging-pitfalls`, `business/marketing-claim-substantiation-pitfalls`,
`business/release-communication`, `business/data-protection`, `business/legal-documents`,
`skills/vat-handling-in-software-pitfalls`, `skills/saas-metric-definition-pitfalls`, `skills/source-freshness`.
