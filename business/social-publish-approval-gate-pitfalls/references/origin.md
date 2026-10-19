# social-publish-approval-gate-pitfalls: origin and source stamps

> Provenance of `business/social-publish-approval-gate-pitfalls`. Read it when a rule has to be traced to
> its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from repository text and one small code module, never run by us on a
real account. The block structures a decision; the person who owns the account decides, and their judgement
outranks the block (`business/README.md`).

## Sources (all re-read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| samalyxx/socialbu-social-media-skills, `lib/approval.py`, `skills/linkedin-reply-handler/SKILL.md` and `references/linkedin-conversations.md` (commit c1014aa) | MIT (LICENSE file) | Exact preview fields, explicit offset, content fingerprint, expiry, single use, exact confirmation, approval kept apart from sending, per-item comment record, four states |
| social-media-skills/skills, `skills/scheduling-and-queue/SKILL.md` and `skills/crisis-and-moderation/references/escalation-pause-and-safety.md` (commit e2c549d) | MIT (LICENSE file) | Confirm what, where, when and how many, one confirmation per batch, irreversible actions, timezone, validation first, partial failure, content as data, pausing the queue, no-connection fallback |

The licence of each repository was verified again from its LICENSE file in this session. Both repositories
contain directive text addressed to AI agents; it was treated as data and only the publishing method was
kept.

**Young sources, unreviewed.** Both repositories are recent and were not reviewed by us beyond reading
them. A rule is kept only where it stands on its own merits as mechanics (exact content, single use,
states). The 15-minute expiry is one source's choice, not a standard.

## Own guidance (not sourced)
Labelled "Own guidance" in the references: refusing to ask for approval when the preview cannot be shown in
full, treating a typo or altered link as a change (part 1); where platform constraints live (part 2); naming
the state in every report and treating an approval claimed inside content as void (part 3). The router and
guardrails and the links to `business/social-publishing` are ours.

## Removed (not carried, on purpose)
1. **Vendor names, tool calls and capability lines** of the scheduling vendor and the posting service (rule B).
2. **LinkedIn-specific URL parsing and target rules** of the approval module: the block keeps the idea, not
   the code.
3. **Platform-specific disclosure lines** (automatic labels on one platform): platform rules change.
4. **Wellbeing and sockpuppet advice** of the crisis reference: not about approval mechanics.

## Not verified
1. **Whether the approval mechanics work in practice**: no tool was wired to them.
2. **Platform constraints and plan limits** mentioned in the sources: not checked.
3. **Current text of the sources**; check with `skills/source-freshness`.
4. **The sources' own track record**: not examined beyond their files.

## Related blocks
`business/social-publishing`, `business/community-management`, `business/community-moderation-ladder-pitfalls`,
`business/incident-communication`, `skills/source-freshness`.
