# pricing-and-packaging-pitfalls: origin and source stamps

> Provenance of `business/pricing-and-packaging-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from repository text and two method pages, never run on a real pricing
decision by us and written without pricing expertise. The block structures a discussion; it certifies nothing,
and the person who owns the pricing decision decides (`business/README.md`).

## Sources (re-read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| coreyhaines31/marketingskills, commit e85f3cb (e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b), `skills/pricing/SKILL.md` (v2.1.4) and `references/` `research-methods.md`, `pricing-models.md`, `tier-structure.md`, `pricing-page-teardown.md`, all read in full this session | MIT (LICENSE file, 2025 Corey Haines, head re-read) | Three axes (packaging, metric, price), value-metric test, per-model fit notes (seats, usage and meter, credits, outcome, hybrid), do not gate the core, personas, free plan and trial trade-offs, first price as a learning bet, competitor and cost as inputs, the corrected reading of the four-question survey curves (cheap curves fall, expensive curves rise), exclusions recorded, "perception, not demand" |
| alirezarezvani/claude-skills, commit 19392f7 (19392f7a08264ed00486a251f5b2098321771f94), `commercial/skills/pricing-strategist/SKILL.md`, `references/packaging_anti_patterns.md` and `references/van_westendorp_methodology.md`, all read in full this session | MIT (LICENSE file, 2025 Alireza Rezvani, head re-read) | The packaging anti-pattern questions (restated, cutoffs dropped), one upgrade trigger per tier, a range never a number, value-based pricing needs a measurable driver, segment before reading, validate with a real purchase test |
| guia-matthieu/clawfu-skills, commit 4108f5c (4108f5c010ccaa8b5707fa05ca1d888ae167e548), `skills/validation/pricing-validation/SKILL.md` lines 1 to 90 | MIT (LICENSE file, 2026 Guia, head re-read) | Method-follows-the-question idea only; nothing else taken |
| Sawtooth Software blog, "Van Westendorp pricing sensitivity meter" (WebFetch, 2026-10-20, page read through a summarising fetch, not word for word) | vendor blog, no open licence, facts only | The four questions, the named crossings and that their names lack strong theory, limits (no competition, no cost or margin, no demand prediction, weak economic grounding, best for new products), the purchase-intent extension and its discount factors for overstated intent |
| Wikipedia, "Van Westendorp's Price Sensitivity Meter" and "Gabor-Granger method" (WebFetch, 2026-10-20, summarising fetch) | CC BY-SA, facts only, no text used | Original 1976 method, two curves inverted by convention, the base method sets prices without estimating demand; Gabor-Granger: five price points, one random starting price, move up after interest and down after none, demand and revenue curve, results confined to the chosen prices, respondents with no interest at the lowest price coded as zero or dropped. Both articles carry a maintenance tag saying they lack inline citations |

Not used: borghei/claude-skills (Commons Clause plus MIT, which removes the right to sell, so not an open
licence under `CONVENTIONS.md`): idea-only, nothing taken, not re-cloned. fradser/dotclaude and
davila7/claude-code-templates: copies, not used.

The repositories' own text is addressed partly to an AI; it was treated as data and only the method was kept.

## Gabor-Granger and vendor facts: how far they were reached
No academic or open primary text on either survey method was read. For the four-question method the nearest
reach is a vendor method page (Sawtooth) and an encyclopedia article. For the stepped-price method the only
fetch was the encyclopedia article. Two other vendor guides (a conjoint vendor's pages for both methods)
returned 404. The statements in §5.3 on anchoring on a fixed first price, uneven price gaps, overstated intent
and one offer at a time are partly from the encyclopedia article (random start, chosen price points, zero
coding) and partly own method guidance or the overstated-intent point made on the vendor page; they are
labelled as practice, not as the method's literature. The earlier review's search summaries for this method
were not relied on.

## Left out on purpose
Every numeric benchmark in the sources: trial conversion with and without a card upfront, trial lengths, the
10 to 1 value-to-price ratio, the order-of-magnitude price buckets and the "just charge fifty" story, the
discount-asker churn multiple, the annual-discount percentage, raise-price signal thresholds, tier multiples,
tier-mix priors, the packaging detection cutoffs, survey sample sizes (they disagree and have no derivation),
the sourced-looking statistics attributed to named authors and reports, the "each percent of price is worth
eleven percent of profit" claim (margin arithmetic true only for given margins), the feature-importance decile
rules for packaging, charm and decoy pricing psychology (no citation). Price changes, grandfathering, discounts
and billing mechanics: `business/price-change-and-billing-pitfalls`. The pricing-page readability rubric for
automated agents (read, but rests on one source and a heuristic, so left out until corroborated). Calculators
and scripts in the repositories.

## Not verified
1. **Credit-based and outcome-based models** (§2.4) rest on the marketing skills only. They need checking
   against two independent practitioner or academic references.
2. **The survey-method statements** rest on a vendor page and encyclopedia articles through summarising
   fetches, not on the original papers.
3. **The block has never been used on a real product**, and its guardrails were not tested against a real
   pricing discussion.
4. **Current text of the sources**: they may have changed after the read date; check with
   `skills/source-freshness`.

## Own guidance (not sourced)
The router and the order of sections; the four-part metric test wording (§2.1); the edge checks on seats and
the "unit the customer controls" check (§2.2, §2.3); the "a tier nobody should rationally pick" question
(§3.3); the non-conversion budget and time-to-value questions (§4.1); the page checklist as a list (§4.2); the
tie-counting and exclusion-count habits (§5.2); the randomise, even gaps and coding habits (§5.3); the
guardrails and links to neighbouring blocks.

## Related blocks
`business/price-change-and-billing-pitfalls`, `business/product-marketing`,
`business/marketing-claim-substantiation-pitfalls`, `skills/saas-metric-definition-pitfalls`,
`skills/vat-handling-in-software-pitfalls`, `skills/experiment-design-pitfalls`, `skills/source-freshness`.
