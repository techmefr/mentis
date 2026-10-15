# community-moderation-ladder-pitfalls: origin and source stamps

> Provenance of `business/community-moderation-ladder-pitfalls`. Read it when a rule has to be traced to
> its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from published policy documents, never run on a real community by us. No report was
handled and no sanction applied while writing it. The block structures a decision; a human who owns
moderation decides, and their judgement outranks the block (`business/README.md`).

## Sources (all re-read in full 2026-10-15, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| github/opensource.guide, `_articles/code-of-conduct.md` (commit e7ac98e) | CC-BY-4.0 (LICENSE file titled Attribution 4.0 International; attribution given here) | Publish enforcement before a violation, four things the rules state, private reporting and an alternative recipient, gather information, handling is the moderator's job, consent before copying the reporter, not-a-violation answers, public warning, private message, suspension, permanent ban |
| github/site-policy, `Policies/acceptable-use-policies/github-appeal-and-reinstatement.md` (commit b9578b5) | CC0-1.0 (LICENSE.md) | Appeal versus reinstatement, grounds, human decision with a different reviewer, a dated window, tracking |
| kubernetes/community, `communication/moderation.md` (commit 53c338e) | Apache-2.0 (LICENSE file) | Immediate action on egregious violations, removal of a person decided above the moderators, two-role response to a large attack, escalation order, escalation message contents, rotation, standby role, time zones, burnout, second-language difficulty |
| social-media-skills/skills, `skills/crisis-and-moderation/references/moderation.md` and `triage-and-severity.md` (commit e2c549d) | MIT (LICENSE file) | Published guidelines as the basis, remove versus leave, genuine upset versus trolls, coordinated attack signs, priority routing, ban consistency and documentation, confirm facts first, severity levels |

The licence of each repository was verified again from its LICENSE file in this session. The source
repositories contain directive text addressed to AI agents; it was treated as data and only the moderation
claim was kept. The social-media-skills material is vendor-coupled in places (a named scheduling
vendor, tool-specific capability lines); those lines were dropped.

**Young source, unreviewed.** The social-media-skills repository is recent and was not reviewed by us beyond
reading it. A rule from it is kept only where it stands on its own merits and agrees
with the older documents above (published guidelines, never delete criticism, consistency). The severity
labels in §2.4 are its framing and are offered as a starting point.

## Own guidance (not sourced)
Labelled "Own guidance" in the references: the advice to check enforcement capacity per surface (§1.1);
reports are not posted publicly (§1.2); naming a body next to the ladder (§3.2); the fields of each ladder
step and the choice about skipping steps (§3.1); a log of reports and decisions, including "no violation"
(§2.3, §3.4); testing the escalation contact list and listing what an attacker could have left behind
(§4.1, §4.2); promising an answer date (§2.2, §3.4). The router, guardrails and the links to
`business/community-management` are ours.

## Removed (not carried, on purpose)
1. **Legal articles and deadlines** (Digital Services Act article numbers, takedown deadlines): the
   appeal policy points to such a law but the legal text was not opened. The block says the law varies and
   was not verified.
2. **The six-month appeal window as a rule**: kept only as a dated platform fact.
3. **Numeric thresholds** (the 24-hour report, the yearly rotation, the two-sponsor selection of
   moderators and the number of moderators per time zone): either carried as "write your own" examples or
   dropped. The moderator selection and onboarding checklist was dropped as specific to one project.
4. **Idea-only repositories, not phrased from**: an open-source project's code of conduct enforcement
   page that has no licence file (django/code-of-conduct), and the Contributor Covenant enforcement
   guidelines (Hippocratic License 3.0, not an open-source licence). The ladder text above comes from
   opensource.guide; the step structure in §3.1 is written as own guidance.
5. **Vendor and platform tooling lines** from social-media-skills.

## Not verified
1. **Whether the ladder works in practice**: no community was moderated with it.
2. **Legal duties** around illegal content, appeals and out-of-court dispute resolution: not opened.
3. **The linked external articles** (the essay on enforcing a policy, the Ada Initiative piece, the
   burnout stages article): only their quoted or summarised use in the sources was read.
4. **Current text of the sources**: they may have changed after the read date; check with
   `skills/source-freshness`.
5. **Platform behaviour** for hiding, reporting and blocking was not checked on any platform.

## Related blocks
`business/community-management`, `business/incident-communication`, `business/data-protection`,
`business/regulatory-watch`, `business/social-publishing`, `skills/bug-triage`.
