# plan references: origin of §17

> Provenance of `references/17-self-review-sizing-and-edges.md`. Read it to trace a rule to its source, never to apply one.
> The origin of steps 0 to 16 stays in `SKILL.md`.

**Status: 🟡.** Rewritten from two sources, re-read in full on 2026-10-19 (both clones at the commits of `maketime-16` review, MIT licence file read again): no text copied, own examples.

| Source | Licence | What it gave |
|---|---|---|
| `obra/superpowers`, `skills/writing-plans/SKILL.md` (whole file) | MIT, 2025 Jesse Vincent | Points 1 to 6 (the self-review checklist run by the planner, name and type consistency, the Interfaces note per task, proportion last), points 7 to 9 (task right-sizing, step granularity, structure before tasks) |
| `mattpocock/skills`, `skills/engineering/to-tickets/SKILL.md` (whole file) | MIT, 2026 Matt Pocock | Points 10 to 15 (blocking edges, frontier, prefactor, one fresh context, expand-migrate-contract for a wide change) and the vertical-slice option of point 16 |

Already in `SKILL.md` before this pass and therefore not restated: step 4 (what a step contains), 5 (review focus), 6 (proportion), 8 (file map and header), 9 (no placeholders), 10 (self-review, coverage), 14 (traceability). Point 3 and point 6 sharpen steps 9 and 6 rather than repeat them. The review that proposed this extension (`maketime-16`, P1.1) described the block as 1 KB; it is no longer, and CATALOG row `writing-plans` (owned by `plan`) is accurate for steps 4 to 6 and 8 to 10.

## Not taken

1. The default save path of the source's plan files, its plan header with an execution-skill banner, the execution handoff and its choice between two execution modes: Rule E puts the plan in the spec-kit artefacts, and `skills/execute-plan` owns execution.
2. The ticket publication step of `to-tickets` (a tracker, `ready-for-agent` labels, sub-issues) and its advice to keep file paths and code snippets out of a ticket: a `tasks.md` task names its file and signature (steps 4 and 8), so the advice is for tracker tickets, not for this block.
3. The source's per-task commit steps and its frequent-commit instruction: commit policy belongs to the project.

## Not verified / open decision for the owner

1. **Horizontal against vertical slicing.** The `to-tickets` source states vertical tracer-bullet slices as the rule, and the `tdd` skill of the same repository calls writing every test first a horizontal slice and treats it as the wrong shape (`skills/engineering/tdd/SKILL.md` of that repository, line 32, re-read 2026-10-19). mentis `tdd` writes all acceptance tests first, red, on purpose, and delegates the writing to a separate agent against test tampering. The two answer different questions (resistance to tampering against the quality of tests), and mentis tests are derived from the spec rather than imagined, which weakens the source's objection but does not settle it. **Not decided, so not adopted:** `tdd` is unchanged, and vertical slicing appears in the plan block (reference 17, point 16) only as an option, "one option, the owner has not decided". Decision needed: which governs, and why.
2. Nothing here was run on a real feature. The edge test of point 11 and the expand-migrate-contract sequence of point 15 are restated from the source, not observed.
3. The source's `to-tickets` examples and its tracker documentation (`docs/engineering/to-tickets.md`) were not read.
