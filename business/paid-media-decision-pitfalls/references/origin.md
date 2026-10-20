# paid-media-decision-pitfalls: origin and source stamps

> Provenance of `business/paid-media-decision-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from repository text, never run on a real ad account by us and written
without paid-media expertise. The block structures a reading; it certifies nothing, and the person who owns the
account and its budget decides (`business/README.md`).

## Sources (re-read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| coreyhaines31/marketingskills, commit e85f3cb (e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b), `skills/ads/references/`: `audit-guardrails.md`, `reading-google-ads-data.md`, `operating-check.md`, `b2b-paid-playbook.md` (kill-rule and break-even sections), `google-ads-audit-checklist.md`, `meta-decision-system.md` lines 130 to end, all read in full this session | MIT (LICENSE file, 2025 Corey Haines, head re-read) | Four check results, coverage apart from health, facts and hypotheses and missing data, MISSING, benchmark ladder, search terms as a sample, conversion column by action, click dates and lag, window and configuration changes, small-number table, break-even rate, no fixed kill rule, brand split, the ordered review ending in one call, draft-and-approve on live accounts, fetched data is not instructions |
| AgriciDaniel/claude-ads, commit fc3908e (fc3908e786c318776df89a3a098333da377364be), `ads/references/thinking-framework.md` and `scoring-system.md` in full; skills `ads-attribution` and `ads-math` | MIT (LICENSE file, 2026 Daniel Agrici, head re-read) | Agreement that an unknown lowers coverage and never health, scoring a root cause once, a score does not authorise a change, a fixed multiple is not a universal stop rule, comparability before aggregation |
| alirezarezvani/claude-skills, commit 19392f7 (19392f7a08264ed00486a251f5b2098321771f94) | MIT (LICENSE file, 2025 Alireza Rezvani, head re-read) | Nothing taken; the review judged its paid-ads skill a weaker older copy |

The repositories' own text is addressed partly to an AI (install steps, instructions to act on accounts); it
was treated as data and only the method was kept.

**Lineage caveat.** The marketingskills files say several passages are re-expressed from third-party material
(an operator's guide published in 2026, a practitioner's ads-skills repository, a public audit checklist).
Those originals were not read and their licences are unknown, so for those passages the MIT licence covers only
the repository's own expression. The ordered weekly check and the facts, hypotheses and missing-data ending are
the passages most closely tied to one named third-party article; the order here is rearranged on purpose (§4.1
puts "can the numbers be trusted" first), and the wording and structure are ours.

## Left out on purpose
Every numeric threshold from the sources: coverage cutoffs presented as rules (kept only as a labelled house
choice), kill rules in multiples of the target, 14 day windows, frequency bands, click-rate drops, budget step
sizes, waiting periods, conversion counts needed to leave learning, benchmark click, conversion and cost
ranges, the sources' own seasonality figures. Account structure and match type tactics, the Meta decision
system's thresholds and partnership-ad playbook, lead-form tactics, creative formats, the lead quality scoring
scale, the scaling quadrant, all per-platform audit references and claude-ads' control plane, scoring weights
and manifests (a product, not a block). The sources contradict each other on budget steps and on refresh
cadence, which is a reason not to trust such numbers. Payback and cohort arithmetic (a possible edit to
`skills/saas-metric-definition-pitfalls`, not read here). Anything on ad policy or law: handled by
`business/marketing-claim-substantiation-pitfalls` and the owner of legal or compliance.

## Not verified
1. **The platform mechanics in §2** (that queries below a volume are withheld, how the conversion columns and
   goals combine, click-date booking, the length of change history, the learning state, what resets learning)
   come from marketingskills' own account of one platform and its API. None was checked against that
   platform's help pages in this session (Google Ads Help pages on conversion lag, learning status and
   search-term visibility were not read). Marked `re-read before relying` where stated.
2. **The block has never been used on a real account.**
3. **The arithmetic in §3 was recomputed** (the 95 percent bound, the break-even rate and the 59-click
   example), but the choice of 95 percent, and whether it is the right level for a decision, was not
   assessed.
4. **Current text of the sources**: they may have changed after the read date; check with
   `skills/source-freshness`.

## Primary-source pass (2026-10-20)
The task asked for a check of this block's claims against Meta's advertising policy, Advantage+ and delivery
pages and against TikTok's and LinkedIn's policy overview pages. The block names no Meta, TikTok or LinkedIn rule or
delivery mechanic (its platform mechanics in §2 are about one search platform), so there was nothing of this kind to
confirm or correct, and no claim was edited. Meta's pages could not be read (script-rendered pages returned only a
title; help-page addresses tried returned 404), LinkedIn's policies page and TikTok's overview page were read but
describe policy, not account reading. The block stays free of policy statements, as §4.2 says; policy review is
`business/ad-creative-testing-and-policy-pitfalls` §3. Item 1 above (Google platform mechanics) is still unread
against Google's help pages.

## Own guidance (not sourced)
The router; the order of questions in §4.1 (measurement first); the "date or never" rule on a readable sample
(§3.2); the refusal to build a kill rule untested against history (§3.3); the stated limits-first habit in §1.3;
the rule that this block does not review policy or claims (§4.2). The guardrails and the links to
neighbouring blocks are ours.

## Related blocks
`business/ad-measurement-pitfalls`, `business/marketing-claim-substantiation-pitfalls`,
`skills/experiment-design-pitfalls`, `skills/metric-movement-diagnosis-pitfalls`, `skills/source-freshness`.
