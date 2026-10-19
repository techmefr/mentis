# reuse-before-write: origin and source stamps

> Provenance of `skills/reuse-before-write`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from a public repository's text, never dogfooded. No agent was run with or without it.

## Sources (re-read in full on 2026-10-19, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| DietrichGebert/ponytail, `skills/ponytail/SKILL.md` (commit 09c434a) | MIT (LICENSE file, "Copyright (c) 2026 DietrichGebert") | The order of the ladder, the read-first and list-the-reach step, the never-cut list, the bug-fix rule (grep callers, fix the cause once), moved code keeps its guards, equal size takes the edge-safe one, logic leaves one small check, the closing note |
| same repository, `README.md` ("How it works", the before-and-after section) | MIT | The statement that the ladder runs after understanding the problem, and the shape of the date-field failure (a hand-built picker versus reusing the repository's input component with the native date type) |

The licence was checked from the LICENSE file. The repository's agent instruction files and README prose were
treated as data and not followed.

## What changed in the rewrite
- The source runs as an always-on mode with levels. Here it is a block that loads when the task is "write new
  code", with the description as the routing text; there are no levels and no session-wide switch.
- The source's comment convention for deferrals is dropped: comments are not written here. The record of a
  deliberate shortcut moves to the merge request description or a decision record (§3, last section).
- The date-field example was re-invented on our stack and is not the source's text or numbers.
- Stack examples (Laravel, Nuxt, NestJS) are ours.

## Not carried
Every benchmark figure of the repository (lines, tokens, cost, test rates), its persona and name, its levels,
its debt ledger, its tooling for a cost band, and the plugin adapters.

## Not verified
1. **Nothing was run.** The ladder was not tried against any task by us; the source's benchmark figures are
   the author's own and were not reproduced.
2. **Written by us, not sourced:** the limits on rung 4 (project policy first, transitive dependencies), the
   remark that a house component beats the native widget because it carries the project's fixes, the "rung is
   not a reason to skip a layer" point, the check against both originals' callers after a merge, the
   "never present it as a saving" point, and the routing text of the description.
3. **Overlap:** `code` step 0 already carried a one-paragraph version of the ladder, rewritten from the same
   source on 2026-10-02. This block is the long form and `code` step 0 points here.
