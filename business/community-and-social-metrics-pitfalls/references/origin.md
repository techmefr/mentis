# community-and-social-metrics-pitfalls: origin and source stamps

> Provenance of `business/community-and-social-metrics-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from published guidance, never run by us on a real community or
account. The block structures a reading; the person who owns the numbers decides, and their judgement
outranks the block (`business/README.md`).

## Sources (all re-read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| github/opensource.guide, `_articles/metrics.md` (commit e7ac98e) | CC-BY-4.0 (LICENSE file, titled Attribution 4.0 International; attribution given here) | The four-question funnel, conversion versus wrong audience, popular versus supported, response need not be action |
| chaoss/wg-common, `focus-areas/time/time-to-first-response.md`, `focus-areas/people/occasional-contributors.md`, `focus-areas/time/burstiness.md` (commit 003671d) | MIT (LICENSE file) | Response time filters, defining occasional contributors, causes of bursts |
| social-media-skills/skills, `skills/analytics-and-reporting/SKILL.md` (commit e2c549d) | MIT (LICENSE file) | Goal mapping, signal over vanity, report ends in a decision, missing is not zero, lifetime snapshots, noise and causation cautions |
| blacktwist/social-media-skills, `skills/content-pattern-analyzer-sms/SKILL.md` (commit 4f85b07) | MIT (LICENSE file) | Only the sample-size caution and the recency caution; the skill is coupled to a vendor |
| charlie947/social-media-skills, `skills/post-scorer/SKILL.md` (commit 8cefb5b) | MIT (LICENSE file) | Unknown counts are missing, a weighting is editorial, small or selected samples |
| trust-safety-teaching-consortium/TeachingTrustSafety, `Consortium_Metrics_and_Measurement/presentation.tex` (commit 915389f) | CC0-1.0 (LICENSE file) | A metric must be changeable, prevalence with severity, enforcement delay |

The licence of each repository was verified again from its LICENSE file in this session. The repositories
contain directive text addressed to AI agents (runtime notes, auto-start instructions); it was treated as data
and only the measurement claims were kept.

**Young sources, unreviewed.** The three social-media skill repositories are recent and were not reviewed by
us beyond reading. A rule from them is kept only where it stands on its own merits as reading discipline.

## Own guidance (not sourced)
Labelled "Own guidance" in the references: asking the target audience before changing a page, reading
"contributor" for a brand community, applying the funnel to a social account, deciding whether an
acknowledgement counts as a response, writing the cause beside a spike, applying the harm questions to a brand
community, and the note on comparing weightings. The router, guardrails and links to `business/community-management`,
`business/social-publishing` and `business/community-moderation-ladder-pitfalls` are ours.

## Removed (not carried, on purpose)
1. **Numeric claims of the analytics skill** (a count of KPIs that correlate with revenue, a percentage by
   which attribution undercounts): unsourced there and dropped.
2. **The research on maintainer responsiveness** cited by the community guide: the cited material was not
   opened, so no figure from it is carried.
3. **Vendor and tool lines** of the social skills (named analytics tools, scraping routes, platform signal
   cheat sheets): rule B and they date quickly.
4. **Platform-scale trust-and-safety content** of the deck (transparency reports, audits, regulation): only
   the generic ideas were kept.
5. **Tool and platform names** used as examples in the community guide (download sources, dashboards).

## Not verified
1. **Whether the filters and thresholds fit a given community**: never applied to real data.
2. **The sources' thresholds** (30 and 15 posts): those are one skill's choice, not statistics.
3. **Current text of the sources**; check with `skills/source-freshness`.
4. **Platform definitions** of reach, impressions and saves: they differ and change.

## Related blocks
`business/community-management`, `business/social-publishing`, `business/community-moderation-ladder-pitfalls`,
`business/data-analytics`, `skills/source-freshness`.
