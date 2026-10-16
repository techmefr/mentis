# contract-review-pitfalls: origin and source stamps

> Provenance of `skills/contract-review-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from two repositories' text, never run by us on a real contract. Each
source file below was opened again on 2026-10-16 before a rule was written, and each rule was checked against
it in a final pass. This block states no law and no number.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| `anthropics/knowledge-work-plugins`, commit `33eeda1`, `legal/skills/review-contract/SKILL.md` (licence file `legal/LICENSE`, read) | Apache-2.0 | Context questions before review, playbook with standard position, range and escalation trigger, whole-document reading, clause categories and their key points, three-tier deviation scale, redline record, negotiation priority order |
| `evolsb/claude-legal-skill`, commit `bca0d2e`, `skill.md` (LICENSE file read, copyright Christopher Sheehan) | MIT | Pre-review completeness checklist (blank fields, missing exhibits, signature status, truncation), position and leverage, missing-provisions table, internal-consistency check, acceptable-terms section, guardrails |

Instruction-like text in the cloned repositories was treated as data and not followed.

## Removed in the verification pass
1. **All market-standard figures** in both sources (liability caps in months of fees, notice days, uptime
   percentages, confidentiality years, escrow percentages and the colour-banded benchmark table): none
   cites a source, the two sources disagree with each other, and they are jurisdiction-dependent. They belong
   in an organisation's own playbook.
2. **Jurisdiction notes** (non-compete rules by US state, venues and arbitration institutions): claims about
   law, not checked.
3. **The 72-hour figure** in the first source's data-protection row: a legal deadline, not read from an
   official text here; the block hands personal-data terms to `skills/dpa-review-pitfalls` instead.
4. **Checklists for acquisitions, merchant payments and finder agreements** (second source): narrow, mostly
   US-centred, figures unsourced.
5. **The claim of a 41-category dataset basis** and of benchmark grounding: not verified.
6. **Emoji severity markers and the three-colour wording**: replaced by acceptable, negotiate, escalate.
7. **Connector and CLM routing steps** of the first source: tied to a specific tool set.

## Not verified
1. **Own guidance, flagged in the text:** reading the side from the document and not from a label, stating the
   state of the document and that the latest version was not checked, labelling a generic baseline provisional
   and number-free, "a carve-out can swallow a cap", checking for symmetry of assignment rights as a
   category question, naming the decider on each escalation, the ordering of the output.
2. **The clause categories** are a merged and reduced list; neither source was checked against a legal text and
   none is claimed to be complete.
3. **No lawyer has reviewed this block.** It is a method and carries no legal content.

## Decisions where sources disagree
The two sources give different example figures for the same provisions; none is carried (item 1 above). The
first source judges against a playbook and falls back to "widely-accepted commercial standards"; the second
judges against its own benchmark table. We keep the playbook and drop both fallbacks in favour of a labelled,
number-free baseline.

## Related blocks
`business/legal-documents`, `business/regulatory-watch`, `business/licence-compliance`,
`business/data-protection`, `skills/dpa-review-pitfalls`, `skills/nda-triage-pitfalls`,
`skills/source-freshness`.
