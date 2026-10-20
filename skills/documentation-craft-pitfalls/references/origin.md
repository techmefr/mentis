# documentation-craft-pitfalls: origin and source stamps

> Provenance of `skills/documentation-craft-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from a published style guide and own craft knowledge, never run on a real
documentation task by us.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| MicrosoftDocs/microsoft-style-guide, pages "Content planning", "Top 10 tips for Microsoft style and voice", "Headings", "Lists", "Writing step-by-step instructions", "Code examples", "Reference documentation", "Final publishing review" (LICENSE file read: Creative Commons Attribution 4.0 International, repository last pushed 2024-11-13) | CC BY 4.0 | Planning questions on audience, goal and success measure; fewer words and getting to the point; headings as an outline, specific and parallel; list forms and range; procedure rules and a short-procedure limit; example guidance (scenario, requirements, output, secure code); reference-page layout and review of generated text; the final-review techniques |

Credit as the licence requires: Microsoft Writing Style Guide, Microsoft, https://github.com/MicrosoftDocs/microsoft-style-guide, CC BY 4.0. The text was rewritten, not reproduced; no endorsement by the author is implied.

## Removed
1. **The brand voice, the word list, grammar and capitalisation rules, the global-communication and chatbot
   chapters**: product-specific or too wide for a page-structure block.
2. **The guide's examples and its "Replace this with this" pairs**: none restated; the examples in the block are
   ours.
3. **The four-way split of documentation by reader need** is not taken from any named framework; it is the
   craft's common distinction and is marked own guidance in §1. The documentation framework that popularised a
   fixed naming of it (CC BY-SA) was not opened.

## Not verified
1. The guide's figures (two to seven list items, about seven steps per procedure) are quoted from the version
   read on 2026-10-20 and may have changed; re-read before relying.
2. §3 is mostly own guidance. No source on documentation freshness or runbook rehearsal was read, and the claim
   that stale pages cost trust is observed craft knowledge, not measured.
3. The guide targets one company's product documentation; its fit for a small repository README is our
   judgement.
4. No docs tool, link checker or snippet runner was run or read; none is named.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: a skip-when line, reviewing existing pages allowed, a one-maintainer owner, the list-length figures scoped, points 15 and 16 added (a privacy or behaviour claim against the code and other pages; commands, addresses and pins across pages). The status stays 🟡.

## Related blocks
`skills/documentation-adr`, `skills/prose-lint-gate-pitfalls`, `skills/troubleshooting-kb-article-pitfalls`,
`skills/release-notes-writing-pitfalls`, `skills/blameless-incident-review-pitfalls`,
`skills/backup-restore-drill-pitfalls`, `skills/source-freshness`.
