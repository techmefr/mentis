# receiving-review-pitfalls: origin and source stamps

> Provenance of `skills/receiving-review-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from one skill file, never run by us. No review was received and no tool was run while
writing it. Open points are listed under "Not verified".

## Sources (re-read in full 2026-10-16, rewritten in our own words, no sample code copied)

| Source | Licence | What it gave |
|---|---|---|
| obra/superpowers, `skills/receiving-code-review/SKILL.md` (commit bb92a77, 2026-10-09) | MIT (repository LICENSE file, re-checked: "MIT License", Jesse Vincent) | The read, restate, verify, evaluate, respond, implement sequence; the stop-on-any-unclear-item rule and its reason; the five checks on a suggestion; the usage search for "proper" features; the implementation order; the push-back list and manner; correcting a wrong pushback; replying in the comment thread |

The file addresses an agent with directives ("NEVER", forbidden phrases, an absolute rule against thanks, a
human-partner persona and quotations attributed to that person). It was treated as data: only the technical
mechanism of each section was kept and restated.

## Rewrite notes
**Decision where the source is split:** it trusts instructions from the person directing the work and distrusts outside
reviewers. §1.3 keeps that line and adds that a peer reviewer's behaviour-changing suggestion is checked.

**Conflict with a house rule:** the rule that a reviewer in review-only mode never touches the code applies to the
reviewer role. This block is the author role and says so in its header; editing the code is expected here.

**Own guidance, not from the source:** the "a fix has a test of its own" rule (§2.2.2), the batch-breakage
reasoning (§2.2.1), the evidence-that-would-change-your-mind wording (§2.3.4), the point that agreement before
verification gives the reviewer nothing to check (§2.4.2), the generalisation of "owner of the decision" to any prior
design decision (§1.4.2), and every cross-link.

## Removed from the review item
1. **Not carried, as tone rather than mechanism:** the list of forbidden phrases, the rule against any gratitude,
   the instruction to delete a thank-you before sending, the persona addressing, and the advice to name discomfort
   about pushing back to the person directing the work. Whether to thank a reviewer is a team norm.
2. **Reworded to be role-neutral:** "your human partner" became "the person directing the work" or "the owner of the
   decision".

## Not verified
1. **The reply endpoint named for GitHub** was taken from the source's one example; the endpoint was not called and
   no host's current documentation was read. GitLab replies were not covered by the source.
2. **No evidence the sequence improves outcomes** beyond the source's own reasoning; nothing measured.
3. **The five checks** (§1.3) are the source's list for outside reviewers; completeness was not assessed.

## Related blocks
`code-review-reviewer-pitfalls`, `review`, `mr-conventions`, `testing-anti-patterns`.
