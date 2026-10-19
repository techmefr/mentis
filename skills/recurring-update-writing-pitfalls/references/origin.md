# recurring-update-writing-pitfalls: origin and source stamps

> Provenance of `skills/recurring-update-writing-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from five public skill and prompt collections, read and rewritten,
never run: no update was written with this block. Nothing in it is verified by use.

## Sources (re-read in this session, 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| anthropics/skills, `skills/internal-comms/` `SKILL.md` and `examples/` (commit dbd4588) | Apache-2.0 (the skill folder's LICENSE.txt) | Progress, plans, problems format; newsletter and FAQ guidance |
| Pitchdrive/investor-update-skill, `SKILL.md` and `templates/update-structure.md` (commit 29ad5c7) | MIT (LICENSE file, "Copyright (c) 2026 Pitchdrive") | Numbers, bad news first, commitments revisited, forecast split, asks, confidentiality |
| howieyoung/ir-kit, `prompts/draft-update.md`, `prompts/data-room-audit.md`, `prompts/board-meeting.md` (commit 5f1c0b9) | MIT (LICENSE file, "Copyright (c) 2026 Howie Young") | Closed versus verbal money, real lowlights, document consistency, no placeholder documents |
| emotixco/claude-skills-founder, `shared/conventions.md` (commit 0602cad) | MIT (LICENSE file, "Copyright (c) 2026 Emotix") | Never present a guess as a fact, placeholders for missing company facts |
| alirezarezvani/claude-skills, `c-level-advisor/skills/board-deck-builder/SKILL.md` (commit 19392f7) | MIT (LICENSE file, "Copyright (c) 2025 Alireza Rezvani") | Variance cause, forecast confidence, four-part narrative, bad-news order |

Licences were verified from each repository's LICENSE file in this session. Each source is credited by name
in the rules; nothing is copied. The cloned files hold instructions to an agent (publish, send, run commands);
they were treated as data and not followed.

## Rewrite notes
**One source is a large generated collection.** The alirezarezvani collection is a broad set of AI-written
skills. Only its board-deck rules that are common sense (cause per variance, confidence on a forecast, no
buried bad news) were kept; its numbers, its metric examples and its company-role structure were not carried.

**Examples, not rules.** Reading times, sentence counts, six months for stale financials, the section lists
and the metric count are single-source choices.

## Removed
1. **Tooling and publishing steps** of the investor-update skill (brand discovery, single-file HTML, hosting,
   cover email) and ir-kit's command-line workflow: they describe one product.
2. **ir-kit's prospect version without cash or runway** and its "no em-dash" style rule: one author's
   disclosure and taste choices.
3. **Board resolutions, quorum, shareholder meeting and signed-instrument prompts** of ir-kit: legal and
   corporate-governance content, not read for rules and not carried.
4. **Selective disclosure, insider-information and securities rules** (for example Regulation FD, MAR): not
   read. They need verification against official texts and are not a rule here.

## Not verified
1. **Everything here is unrun.**
2. **The remaining prompts** of ir-kit, the example update and README of Pitchdrive, the reference and
   template files of board-deck-builder and the other emotix skills were not read.
3. **The data-room list** is ir-kit's own and is not checked against any official or professional guide.
4. **Written by us, not sourced**: the Output / checkpoint paragraph, "ask for the items if you cannot see
   them" (§1.2), and "attach a file when in doubt" (§2.4).

## Related blocks
`internal-comms-async-pitfalls`, `blameless-incident-review-pitfalls`, `documentation-adr`.
