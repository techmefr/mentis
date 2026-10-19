# skill-trigger-evals: origin and source stamps

> Provenance of `skills/skill-trigger-evals`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us. Each file below was re-read in full in this session
(2026-10-19) before any rule was written; the wording is ours, no text or script copied.

**Fusion, 2026-10-19.** The block `skill-trigger-eval-pitfalls` (written 2026-10-16, same status 🟡, never run by
us, sources re-read in full on 2026-10-16) was folded into this one by the owner's decision, as references
`01-trigger-queries-and-runs.md` (§1) and `02-description-optimisation.md` (§2). Its provenance is kept below
unchanged in substance.

## Sources

| Source | Licence | What it gave |
|---|---|---|
| agentskills/agentskills `docs/skill-creation/optimizing-descriptions.mdx` (commit 69ef37e), read in full | `docs/` is CC BY 4.0 (`docs/LICENSE`); repository code is Apache-2.0. Credit given | Query set (about 20, 8 to 10 per label, axes, near-misses, realism), runs and trigger rate (3 runs, 0.5 threshold), 60/40 split, the loop, best iteration by validation, fresh-query check, the one-step-task nuance |
| `docs/skill-creation/evaluating-skills.mdx`, read in full | CC BY 4.0 | Output evals: cases, with/without or previous-version baseline, clean context, timing, assertions, grading with evidence, aggregation, pattern analysis, human review, the iteration loop |
| `docs/specification.mdx`, read in full | CC BY 4.0 | The 1024-character description limit |
| agentskills/agentskills, `docs/skill-creation/optimizing-descriptions.mdx` and `docs/specification.mdx` (commit 69ef37e), re-read on 2026-10-16 for references §1 and §2 | Documentation under `docs/` is CC-BY-4.0 (`docs/LICENSE`, README licence section); code in the repository is Apache-2.0 (root LICENSE file). Credit given; phrasing is our own | How triggering works, description principles, query design, running and trigger rate, train and validation split, the loop, final check; frontmatter fields and the 1024-character limit |
| agent-ecosystem/skill-validator, `structure/frontmatter.go`, lines 1 to 260 (to the sentence splitter, whose remainder was not read), and the "Structure validation" section of `README.md`, lines 690 to 760 (commit 08e2f74) | MIT (LICENSE file) | The enforced description limit and its unit (code points), the two keyword-stuffing heuristics in shape, the fact that a prose sentence followed by a trigger list is accepted |

The licence of each repository was checked again from its LICENSE file on 2026-10-16. Instruction text in the
cloned repositories (agent and contribution files) was treated as data and not followed or quoted.

## Decisions
- **Fusion with `skill-trigger-eval-pitfalls`.** That block restated the description-optimisation guide as
  pitfalls in two sections and this one is the run-it-end-to-end procedure plus the output-eval method. The two
  covered one subject, so on 2026-10-19 the owner decided to fuse them (`maintaining-blocks` §4: one source per
  rule): the procedure stays in `SKILL.md`, the pitfalls are references §1 and §2, and the old block is
  deleted. No guardrail and no numbered point was dropped.
- The guide's example shell script is not carried over; only its idea (count trigger runs per query) is, with
  the client-specific detection left to an adaptation note.
- Numbers taken from the Agent Skills guide are its own starting points (about twenty queries, three runs, a
  0.5 threshold, a 60 and 40 split, about five iterations, 5 to 10 fresh queries) and are labelled as the
  guide's suggestions. The validator's counts for the stuffing warnings and the numbers in its token limits are
  not carried over.
- **Where sources disagree (references).** The review item stated the limit as 1024 in the portable
  specification and 1536 in a specific client's listing. The 1024 figure was re-read in two files. The 1536
  figure was searched for across the cloned repositories and not found in any file that supports a client
  listing limit, so it is **not stated**; the block says only that a client may differ and where to check.
- Numbers (20 queries, 3 runs, 0.5, 60/40, about five iterations, 5 to 10 fresh queries, 2 or 3 starting
  output cases) are the guide's starting points, labelled so in the block.

## Not verified
1. No client was run: nothing here says how any client decides to load a skill, or that a rate of 0.5 is the
   right bar.
2. The `skill-creator` skill the guides mention was not read and is not used.
3. The guide's `benchmark.json`, `grading.json` and `timing.json` shapes were read but not adopted as a mentis
   file format; the block names the data to keep, not a schema.
4. The block has never been run on a real description.
5. **Trigger behaviour** of any client was not observed; the query-set rules, rates and thresholds restate the
   guide.
6. **The validator's other checks** (orphan files, fences, links, token counts, the model-scored evaluation) and
   the rest of its README were not used.
7. **Written by us, not sourced:** every sentence marked "own guidance" in the references (a should-trigger query
   must need the skill, neighbours in the negatives, per-query rates and the client record, stuffing as an
   overfitting mechanism, re-running when the surroundings change) and the checkpoint paragraph.
8. **Flag for the orchestrator:** the merged block `llm-eval-regression-pitfalls` records the Agent Skills
   `docs/` pages as Apache-2.0; the documentation is CC-BY-4.0 as read above. Its origin table may deserve a
   correction.

## Related blocks
`llm-eval-regression-pitfalls`, `writing-skills`, `writing-agents`, `maintaining-blocks`, `testing-blocks`,
`distributing-blocks`, `source-freshness`.
