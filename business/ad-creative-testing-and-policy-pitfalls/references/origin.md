# ad-creative-testing-and-policy-pitfalls: origin and source stamps

> Provenance of `business/ad-creative-testing-and-policy-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from repository text and one policy overview, never run on a real ad
account by us and written without paid-media expertise. The block structures a check; it certifies nothing. The
person who owns the account decides, and legal decides what is lawful (`business/README.md`).

## Sources (read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| AgriciDaniel/claude-ads, commit fc3908e (fc3908e786c318776df89a3a098333da377364be): `skills/ads-creative/SKILL.md`, `skills/ads-test/SKILL.md`, `ads/references/compliance.md` (review order, finding contract, high-risk prompts, recommendations, boundaries), `ads/references/creative-source-registry.md`, the opening of `ads/references/compliance-requirements.md` (intake only) | MIT (LICENSE file, "Copyright (c) 2026 Daniel Agrici", head re-read 2026-10-20) | Inventory by concept with resizes not distinct, fatigue from a time series and not age, quality, format and performance kept apart, no universal cadence or count, the policy review order, unknown rather than pass, high-risk categories as a trigger, recommendations as untrusted proposals, approval is not clearance |
| coreyhaines31/marketingskills, commit e85f3cb (e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b): `skills/ad-creative/SKILL.md` (read in full), `references/creative-roadmap.md` (lines 1 to 118, to the end), `references/hook-system.md` (opening and ending), `skills/ads/SKILL.md` ("Landing Page Alignment" section), `skills/ads/references/meta-decision-system.md` (fatigue section, read only to see what was not carried) | MIT (LICENSE file, "Copyright (c) 2025 Corey Haines", head re-read 2026-10-20) | Falsifiable test hypotheses (metric, comparison, expected direction), concept as a testable unit and judging concepts rather than single ads, change one thing per test, the ad-headline result as a candidate and the fresh randomised page test |
| www.linkedin.com/legal/ads-policy (LinkedIn Advertising Policies), fetched 2026-10-20 through a summarising tool | LinkedIn site terms, no open licence; facts only, no wording kept | review before running and its aim, rejection reasons and resubmission, discretion to approve, reject or remove, suspension for repeated violations, the eight section groups, the landing page rules |
| ads.tiktok.com/help/article/tiktok-advertising-policies-ad-creatives-landing-page (TikTok advertising policies overview), fetched 2026-10-20 through a summarising tool | TikTok site terms, no open licence; facts only | the group structure of policies and supporting resources; no review or enforcement text on that page |
| support.google.com/adspolicy/answer/6008942 (Google Ads policies overview), fetched 2026-10-20 | Google help content under Google's site terms, no open licence; facts and structure only, no wording kept | Four areas of policy, enforcement by disapproval with fix or appeal, account suspension for repeated violations, location variation, English text controlling, financial-product guidance updated on an ongoing basis |
| developers.facebook.com/docs/marketing-api/guides/split-testing (Meta split tests), fetched 2026-10-20 through a summarising tool | Meta developer terms, no open licence; facts only | Audience groups are mutually exclusive, one variable per test, per-ad confidence values for creative tests, advice not to compare unevenly sized groups |
| developers.facebook.com/docs/marketing-api/advantage-campaigns, fetched 2026-10-20 through a summarising tool | Meta developer terms; facts only | Advantage+ campaign state depends on budget, audience and placement settings; nothing taken into the block |
| developers.facebook.com/docs/marketing-api/reference/adgroup, fetched 2026-10-20 through a summarising tool | Meta developer terms; facts only | A new ad stays pending until reviewed; status values include pending review and disapproved; a synchronous review result is not the final decision. Nothing taken into the block |

The repositories' own text is addressed partly to an AI; it was treated as data and only the method was kept.
Second pass 2026-10-20: the Google overview, LinkedIn's policies page, TikTok's overview page and Meta's split-test
guide (its markdown form, since the HTML page is script-rendered) were downloaded and read as raw page text, and
confirmed the points in the rows above: Google's four areas, English text enforcing, disapproval then fix or
appeal, suspension and a strike system for repeat or egregious violations; LinkedIn's review before running
(usually within 24 hours), rejection reasons, edit and resubmit, discretion to approve, reject or remove, suspension
or termination for repeat violation, link behaviour rules, policies changed without notice; TikTok's overview dated
August 2025 as a group index only; Meta's mutually exclusive groups, one variable, KPIs and confidence fixed in
advance, comparable sizes, 2 to 7 creative cells with confidence by ad. Everything stays `re-read before relying`.

**Lineage caveat.** Several marketingskills files state that passages are re-expressed from third-party
material (a published tier list of ad formats, practitioner courses). Those originals were not read and their
licences are unknown, so for those passages the MIT licence covers only the repository's own expression. The
structure and wording here are ours. claude-ads' third-party notice mentions a private research input that is
not redistributed; nothing taken here is traceable to it, but parts of that lineage are not auditable.

## Left out on purpose
Every platform format or creative specification (lengths, sizes, ratios, safe zones, durations), every
threshold and band for frequency, click-rate drops, refresh cadence, creative count, the number of impressions
before judging, format tier lists and their funnel-role ratings, hook-writing templates, the awareness-stage
headline library, generation tools and pipelines, the creative review page template, anything about producing
assets with generative tools, the claim that several split tests compound into a stated gain, and the source
registry's identifiers (they belong to that repository's runtime). Everything legal: the compliance
requirements table of claude-ads (a dated AI-labelling transition, a regional rule package, a health-tracking
guidance note, endorsement guides, a quoted regulation number) was not verified against a primary source and
none of it is copied. No statute, authority, date or state count is stated.

## Not verified
1. **No platform's individual policy was read.** Google's overview (re-read raw on 2026-10-20) carries structure
   only; no individual Google policy page was opened. Meta's Advertising Standards were **not read**: on
   2026-10-20 the Transparency Center page, its older address on facebook.com and a Business Help review page each
   returned only a page title (script-rendered; retried on 2026-10-20 by plain download with a browser user agent,
   which got HTTP 400, and through a page-to-text tool, which got the title only; no official PDF was found), so
   the block names no Meta policy rule and its Meta policy note stays "not read". Meta's developer documentation
   is readable in markdown form and was read for the split-test page (raw, second pass); the campaign-state and
   ad-review pages were read as digests and nothing is taken from them. LinkedIn's policies page and TikTok's overview page were re-read raw (§3.4a); TikTok's
   review-process article returned an error page. Every platform fact is `re-read before relying`.
2. **How a platform runs a randomised ad comparison** (§2.1 item 3): confirmed for one platform only, from its
   developer documentation (split tests, read raw in markdown form); no other platform's page was read, and the point
   rests on one repository's account for the rest.
3. **Partly read sources**: of marketingskills, the ad-creative references other than the roadmap and hook
   system (templates, platform specs, motion and video, iMessage, generative tools, meta formats, review page)
   were not read and nothing rests on them; of claude-ads, only the files listed above, not its other skills
   or per-platform creative specification files.
4. **The two sources disagree on fatigue.** One says no universal cadence applies; the other quotes bands and
   lifespans. The block follows the first and carries neither; the bands were not checked against any primary
   source.
5. **The block has never been used on a real account.**
6. **Current text of the sources**: they may have changed after the read date; check with
   `skills/source-freshness`.

## Verified in the primary-source pass (2026-10-20)
Confirmed against LinkedIn's page: that a rejected ad can be fixed and resubmitted, that repeated violations can put
an account at risk, and that the landing page is part of what is checked (§3.3 item 4, §3.2 item 5, now credited in
§3.4a for that platform). Randomised ad comparison point (§2.1 item 3): confirmed on one platform's developer split-test page (second pass,
same day); not confirmed for TikTok or LinkedIn, whose pages read did not describe one.

## Own guidance (not sourced)
The router; the three-judgements wording applied to format fit and the rule that emotional judgement stays with
a person (§1.4 items 3 and 4 in their framing); the "add a size only where a baseline exists" note (§1.2 item 2);
the reasons an ad result does not transfer, as stated in §2.1 items 1 to 4 beyond the source's own sentence;
the two-findings line format (§3.1 item 3); the questions list in §3.4 item 2 as worded; the guardrails and the
links to neighbouring blocks.

## Related blocks
`business/paid-media-decision-pitfalls`, `business/ad-measurement-pitfalls`,
`business/marketing-claim-substantiation-pitfalls`, `business/data-protection`,
`skills/experiment-design-pitfalls`, `skills/metric-movement-diagnosis-pitfalls`, `skills/source-freshness`.
