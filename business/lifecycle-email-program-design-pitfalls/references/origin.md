# lifecycle-email-program-design-pitfalls: origin and source stamps

> Provenance of `business/lifecycle-email-program-design-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from repository text, never run on a real lifecycle program by us and
written without email-marketing expertise. The block structures a design and a read; it certifies nothing, and
the person who owns the program decides (`business/README.md`).

## Sources (re-read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| coreyhaines31/marketingskills, commit e85f3cb (e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b), `skills/emails/`: `SKILL.md`, `references/sequence-templates.md` and `references/email-types.md`, all read in full this session | MIT (LICENSE file, 2025 Corey Haines, head re-read) | The sequence overview (trigger, goal, exit conditions), the question "what other emails are they receiving", one email one job, the lifecycle inventory idea (what programs exist, not their templates) |
| hyperfx-ai/marketing-skills, commit 7c1dd65 (7c1dd6554e7c24ee1903c3925a6de1ef9c82dd3d), `skills/email-lifecycle/SKILL.md` and `references/sequence-patterns.md`, both read in full this session | MIT (LICENSE file, 2026 hyperfx.ai, head re-read) | Define trigger, audience, goal, success metric and suppression before copy; one purpose per sequence; unsubscribes honoured account-wide; seed-inbox read, merge-field fallback, distinct subjects, middle-of-the-night check; audience before copy when conversion is low; suppress on conversion; what the end of a sequence does |
| resend/resend-skills, commit b2ae7b1 (b2ae7b1798b70134faf679f35fc05b4331462988), `skills/email-best-practices/references/list-management.md` and `marketing-emails.md`, read in full this session | MIT (LICENSE file, 2026 Resend, head re-read) | Suppression across both message types, unsubscribe scoped to marketing, preference page as an option beside the unsubscribe path |
| sendx/email-skills (ae6f6ce) and rampstackco/claude-skills (9b90db2) | MIT (LICENSE files re-read: 2026 SendPost, LLC; 2026 RampStack Co.) | Nothing taken for this block; cloned at the review commits, their workflow and sequence files were not opened for it |

The repositories' own text is partly addressed to an AI or to one vendor's service (install steps, a tool
surface that needs a vendor connection, a repository file describing how to work in it); it was treated as data
and only the method was kept.

## Left out on purpose
Every sequence template, length, day offset and cadence table (welcome in a stated number of messages over a
stated number of days, nurture, re-engagement, win-back, abandoned cart): taste and one audience's lineage.
Every benchmark (open, click, recovery and conversion ranges by pattern), every frequency, send-time and subject-
or preview-length figure, the five-patterns-cover-almost-everything claim, copy skeletons and AI-tell lists
(`business/ai-prose-tells`), provider selection and tool-call mechanics (vendor-shaped), the retention table
that says suppression and consent records are never deleted or kept for a stated number of years, and every
legal summary (those belong in `business/data-protection` after a regulator read). Failed-payment recovery and
cancel flows (a separate review).

## Not verified
1. **The preference-page statement in §3.3** (published sender requirements ask for a one-click path and a
   visible link, and say a preference page does not replace them) comes from a digest of one provider's page and
   from the Resend reference; it was not re-fetched in this session. Marked `re-read before relying`.
2. **The block has never been used on a real program.**
3. **Platform behaviours implied in §1.3 and §4.1** (whether a platform re-evaluates an audience before each
   message, which exits it can express, how it handles a time zone, whether a duplicate entry is blocked) are
   what the sources assume; none was checked against a real platform.
4. **Current text of the sources**: they may have changed after the read date; check with
   `skills/source-freshness`.

## Own guidance (not sourced)
The router; the one-page program definition (§1); re-checking the audience at each send and testing the exits
with a test contact (§1.3, §4.1); the single frequency rule with a named owner and a stated tie-break
(§2.3); the classification of a message by purpose and the rule that a trigger does not make mail
transactional (§3.2); the preference page writing into the same suppression record (§3.3); the order "audience
before copy" kept as a guardrail; the routing of consent, suppression retention and business-mail questions to
`business/data-protection`. The guardrails and the links to neighbouring blocks are ours.

## Related blocks
`business/email-deliverability-and-sender-requirements-pitfalls`,
`business/email-campaign-measurement-and-testing-pitfalls`, `business/data-protection`,
`business/release-communication`, `skills/customer-email-review-pitfalls`, `skills/laravel-mail-via-notifications`,
`skills/source-freshness`.
