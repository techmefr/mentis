# blameless-incident-review-pitfalls: origin and source stamps

> Provenance of `skills/blameless-incident-review-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from two repositories of documentation, read and rewritten, never run: no incident
review was written or facilitated with this block. Nothing in it is verified by use.

## Sources (all re-read in full 2026-10-15, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| PagerDuty/incident-response-docs, `docs/after/effective_post_mortems.md` and `docs/after/post_mortem_process.md` (commit 464fc9d) | Apache-2.0 (repository LICENSE file, "Copyright 2016 PagerDuty, Inc.") | Dos, don'ts and suggestions (outage wording, no shaming, no human error, no alternate reality), reviewer questions, owner duties, status values, timeline evidence, meeting deadlines and agenda, action selection |
| adhorn/operational-excellence, `IncidentReviewTemplate.md` (commit 7456c60) | MIT (repository LICENSE file, "Copyright (c) 2020 Adrian Hornsby") | Contributing factors over a single root cause, second stories, language list, precise vocabulary, interview approach, classification, action item fields, quality checklist, learning loops |

The licence of each repository was verified again from its LICENSE file in this session. Both sources carry
directives in the imperative; they were treated as practice descriptions and rewritten as mechanisms, with
the source named per rule.

## Rewrite notes
**Sources differ: a single root cause.** PagerDuty's process asks the owner to "identify the underlying
cause" while its guidance says a mistake is rarely rooted in one action and has several contributing
factors; adhorn rejects a single root cause and the "5 Whys" approach outright. The block carries adhorn's
stance and says so (§1.1).

**Examples, not rules.** The 3 calendar and 5 business day meeting deadlines, the 24 hour pre-review, the
15 to 30 minute meeting, the status names, the severity scale and the "top two priority levels" ticket
filter are PagerDuty's own choices and are labelled as examples (§3.1, §4). PagerDuty's customer-impact
examples and its customer-facing message step belong to its product and support organisation.

**Attributions are the author's.** Adhorn's template credits blameless postmortems to Allspaw, second
stories to Cook, Woods and Dekker, single and double-loop learning to Argyris and Schön, and
work-as-imagined versus work-as-done to Hollnagel. Those attributions are reported as the template's own
claims and were not checked; the block does not cite those authors.

## Removed
1. **"A false alarm that mobilised responders still gets a review."** Not found in either file; dropped.
2. **"A review is never skipped because the cause is known."** Not found as stated; the block keeps only
   PagerDuty's warning against neglecting the review and leaves the scope to the team (§4.4).
3. **Adhorn's work-as-imagined versus work-as-done sections, chaos engineering and game-day prompts** were
   read but not carried beyond one line (§3.3); they are one template's wider programme.
4. **Human and working-conditions question lists** (fatigue, stress, emotional climate) from the template:
   not carried as rules, they belong to an interviewer's judgement and risk becoming HR assessment.

## Not verified
1. **Everything here is unrun.** No review was written with these rules.
2. **The attributions** to Allspaw, Cook, Woods, Dekker, Argyris, Schön and Hollnagel (adhorn's claims).
3. **The PagerDuty videos and talks** it links were not watched; the links are not carried.
4. **PagerDuty's other pages** (roles, severity levels, crisis) were not read for this block.
5. **Written by us, not sourced**: the Output / checkpoint paragraph, the question "which assumption was
   wrong" as a prompt for each finding (§1.1, built from adhorn's single and double-loop remark), the point
   that a process must name who chases the tickets (§3.3), and the statement that no HR or legal claim is
   carried.

## Related blocks
`documentation-adr`, `handoff`, `internal-comms-async-pitfalls`.
