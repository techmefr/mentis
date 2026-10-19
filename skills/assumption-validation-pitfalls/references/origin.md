# assumption-validation-pitfalls: origin and source stamps

> Provenance of `skills/assumption-validation-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from one repository of documentation, read and rewritten, never run: no assumption was
validated and no finding promoted with this block. Nothing in it is verified by use. The repository is young
(its LICENSE says 2026) and the rules are one author's practice, not consensus.

## Sources (all re-read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| shinpr/claude-code-discover, `skills/hypothesis-discipline/SKILL.md` and `references/hypothesis-template.md` (commit a414fc7) | MIT (repository LICENSE file, "Copyright (c) 2026 Shinsuke Kagawa") | Criteria before testing, lifecycle states, time budget and timeout, confidence update rules, result recording, key disciplines |
| shinpr/claude-code-discover, `skills/product-principles/SKILL.md` (same commit) | MIT (same LICENSE file) | Four risks, confidence as evidence ladder, cost, risk and reversibility, three tiers, promotion criteria, traceability |
| shinpr/claude-code-discover, `skills/recipe-validate/SKILL.md`, `agents/hypothesis-verifier.md` and `agents/knowledge-distiller.md` (same commit) | MIT (same LICENSE file) | Timeout options, independent design of the test, decomposition, test methods, interpretation risks, promotion and contradiction handling, review of results |

The licence was verified again from the LICENSE file in this session. The files are written as directives to
an agent harness (invoke this agent, stop and wait for approval, JSON output contracts); they were treated as
practice descriptions and rewritten as mechanisms, and no instruction was executed. The rest of the
repository (about 25 other skill files, other agents, the templates for opportunities and PRDs) was not read.

## Rewrite notes
**Boundary with the experiment block.** The source covers discovery-stage validation (prototype, survey, data
mining, spike). Online controlled experiments are in `experiment-design-pitfalls`, and the two cross-refer
without merging (§1.4).

**Numbers are the author's.** The 0 to 10 confidence scale, its bands and the table of thresholds by cost
are one author's calibration; the source itself says the table calibrates judgment and is not a gate. The
block carries the ladder and the cost, risk and reversibility principle, not the numeric bands (§2.1, §2.2).

**Harness mechanics are not carried.** The OST file layout, the document locations, the agent names, the JSON
shapes, the blocking approval gates and the "do not use model invocation" flags belong to the source's tool.

## Removed
1. **The numeric 0 to 10 bands and the threshold table by cost** (product-principles): one author's
   calibration; the qualitative ladder and principle are kept.
2. **OST hierarchy, Knowledge Pyramid file locations, MVP definition and state design** (product-principles):
   read, not carried; product-framework content outside this block.
3. **Prototype generation, worktree code spike and market-research procedures** (recipe-validate): tool
   orchestration, not carried.
4. **JSON output contracts** of the two agents: harness detail.
5. **The "Tier 1 learnings re-checked on freshness" mechanics** beyond the last-validated tag and the
   changed-conditions trigger: not carried.

## Not verified
1. **Everything here is unrun.** No hypothesis was validated and no learning promoted with these rules.
2. **No external citation was checked**: the source names the Opportunity Solution Tree and the four risks
   without a reference, and none is added here.
3. **The rest of the repository** was not read, as listed above.
4. **Written by us, not sourced**: the Output / checkpoint paragraph, the "extension gets its own deadline" and
   "written reason for an extension" advice in §1.2, and the cross-reference to the experiment block.

## Verification pass (2026-10-16)
Every rule in the three references was compared with the attributed shinpr files, read in full in the same
session; "Rejected is not worthless", the "calibrates judgment" statement and the timeout options were
re-searched and exist as stated.
- **Corrected:** none needed; no reversed or overstated rule found.
- **Own guidance, already labelled:** the written-reason and own-deadline advice for an extension.
- **Not re-verified:** that the method works, and the other files of the repository.

## Related blocks
`experiment-design-pitfalls`, `premortem-review-pitfalls`, `analysis-validation-pitfalls`.
