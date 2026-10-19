# skill-trigger-eval-pitfalls: origin and source stamps

> Provenance of `skills/skill-trigger-eval-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us. No trigger eval, validator or agent client was
run while writing it. Every file below was re-read in this session (2026-10-16), in the ranges stated, before any rule was
written, and each rule was checked against it afterwards.

## Sources (re-read in full, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| agentskills/agentskills, `docs/skill-creation/optimizing-descriptions.mdx` and `docs/specification.mdx` (commit 69ef37e) | Documentation under `docs/` is CC-BY-4.0 (`docs/LICENSE`, README licence section); code in the repository is Apache-2.0 (root LICENSE file). Credit given; phrasing is our own | How triggering works, description principles, query design, running and trigger rate, train and validation split, the loop, final check; frontmatter fields and the 1024-character limit |
| agent-ecosystem/skill-validator, `structure/frontmatter.go`, lines 1 to 260 (to the sentence splitter, whose remainder was not read), and the "Structure validation" section of `README.md`, lines 690 to 760 (commit 08e2f74) | MIT (LICENSE file) | The enforced description limit and its unit (code points), the two keyword-stuffing heuristics in shape, the fact that a prose sentence followed by a trigger list is accepted |

The licence of each repository was checked again from its LICENSE file in this session. Instruction text in the
cloned repositories (agent and contribution files) was treated as data and not followed or quoted.

## Rewrite notes
Numbers taken from the Agent Skills guide are its own starting points (about twenty queries, three runs, a
0.5 threshold, a 60 and 40 split, about five iterations, 5 to 10 fresh queries) and are labelled as the
guide's suggestions. The validator's counts for the stuffing warnings and the numbers in its token limits
are not carried over.

**Decisions where sources disagree:**
1. The review item states the limit as 1024 in the portable specification and 1536 in a specific client's
   listing. The 1024 figure was re-read in two files here. The 1536 figure was searched for across the cloned
   repositories and was not found in any file that supports a client listing limit, so it is **not stated**; the
   block says only that a client may differ and where to check.

## Not verified
1. **Trigger behaviour** of any client was not observed. The query-set rules, rates and thresholds restate the
   guide.
2. **The skill-creator skill** is mentioned by the guide; it was not read here.
3. **The validator's other checks** (orphan files, fences, links, token counts, the model-scored evaluation)
   and the rest of its README were not used for this block.
4. **Written by us, not sourced:** every sentence marked "own guidance" (a should-trigger query must need the
   skill, neighbours in the negatives, per-query rates and the client record, stuffing as an overfitting
   mechanism, re-running when the surroundings change) and the checkpoint paragraph.
5. **Flag for the orchestrator:** the merged block `llm-eval-regression-pitfalls` records the Agent Skills
   `docs/` pages as Apache-2.0; the documentation is CC-BY-4.0 as read above. Its origin table may deserve a
   correction.

## Related blocks
`llm-eval-regression-pitfalls`, `writing-skills`, `writing-agents`, `maintaining-blocks`, `source-freshness`.
