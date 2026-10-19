# skill-trigger-evals: origin and source stamps

> Provenance of `skills/skill-trigger-evals`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us. Each file below was re-read in full in this session
(2026-10-19) before any rule was written; the wording is ours, no text or script copied.

## Sources

| Source | Licence | What it gave |
|---|---|---|
| agentskills/agentskills `docs/skill-creation/optimizing-descriptions.mdx` (commit 69ef37e), read in full | `docs/` is CC BY 4.0 (`docs/LICENSE`); repository code is Apache-2.0. Credit given | Query set (about 20, 8 to 10 per label, axes, near-misses, realism), runs and trigger rate (3 runs, 0.5 threshold), 60/40 split, the loop, best iteration by validation, fresh-query check, the one-step-task nuance |
| `docs/skill-creation/evaluating-skills.mdx`, read in full | CC BY 4.0 | Output evals: cases, with/without or previous-version baseline, clean context, timing, assertions, grading with evidence, aggregation, pattern analysis, human review, the iteration loop |
| `docs/specification.mdx`, read in full | CC BY 4.0 | The 1024-character description limit |

## Decisions
- **Overlap with an existing block.** `skill-trigger-eval-pitfalls` (2026-10-16) already restates the
  description-optimisation guide as pitfalls in two sections. This block is the run-it-end-to-end procedure and
  adds the output-eval method; it points to the pitfalls block for the failure modes and does not restate them.
  Folding the two into one block is a maintainer decision (`maintaining-blocks` §4: one source per rule).
- The guide's example shell script is not carried over; only its idea (count trigger runs per query) is, with
  the client-specific detection left to an adaptation note.
- Numbers (20 queries, 3 runs, 0.5, 60/40, about five iterations, 5 to 10 fresh queries, 2 or 3 starting
  output cases) are the guide's starting points, labelled so in the block.

## Not verified
1. No client was run: nothing here says how any client decides to load a skill, or that a rate of 0.5 is the
   right bar.
2. The `skill-creator` skill the guides mention was not read and is not used.
3. The guide's `benchmark.json`, `grading.json` and `timing.json` shapes were read but not adopted as a mentis
   file format; the block names the data to keep, not a schema.
4. The block has never been run on a real description.

## Related blocks
`skill-trigger-eval-pitfalls`, `llm-eval-regression-pitfalls`, `writing-skills`, `testing-blocks`,
`distributing-blocks`, `source-freshness`.
