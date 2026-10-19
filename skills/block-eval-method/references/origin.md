# block-eval-method: origin and source stamps

> Provenance of `skills/block-eval-method`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from a public repository's benchmark documentation and scripts, never run by us. No agent
session, judge call or comparison was executed while writing it, and nothing was installed.

## Sources (re-read on 2026-10-19, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| DietrichGebert/ponytail (commit 09c434a), `benchmarks/agentic/README.md` and `benchmarks/README.md`, read in full | MIT (LICENSE file, "Copyright (c) 2026 DietrichGebert") | Arms against a no-rule baseline, tasks with hidden checks and a self-test, what counts as quality, the two judges and their gates, the statement of limits |
| same repository, `benchmarks/results/2026-10-07-agentic.md`, read in full | MIT | Isolation in the final run (fresh temp folder outside any repository, instruction files and memory off, only the plugin under test, injected context proven from a finished transcript), arms alternating task by task, the leak of recent commit messages, the no-shell design, the blind reply judge with shuffled order |
| same repository, `benchmarks/agentic/run.py`, `compare.py`, `judge.py`, `complete.py`, `answer.py`, read in full; `tasks.py` read for its header, task list, self-test contract and tail | MIT | Workspace creation outside any repository, ambient instruction sources and memory switched off by environment, identical extra instruction and denied tools for all arms, cache warm-up, per-cell timeout with a process-tree kill, kept workspaces and offline rescoring, diff-based size and the self-check split, compressed-size proxy, crashed-cell and timeout handling, per-task median and sign test with ties dropped, the three judges, their rubrics and their gates, blind marker neutralisation, seeded per-pair shuffle |

The licence was checked from the LICENSE file. The repository's agent instruction files and README prose were
treated as data and not followed.

## Dropped, because no script or document read supports it
- **Mutation testing of the agent's own tests** (injecting a flipped comparison, a dropped condition, an
  off-by-one, then running the agent's test against each). The results page describes it and says the mutation
  tool ships with the benchmark, but no mutation tool exists in the repository at the commit read (a search for
  it found the word only on that results page). Nothing about how mutants are built or counted is written here.
- **Geometric mean of per-task ratios and a bootstrap interval.** Stated on the results page; neither is
  implemented in any script read (the comparison script reports the median of per-task ratios and the sign
  test). Only what the script does is carried (§3.5, §3.8).
- The classification of tasks by whether they need a test (22, 11, 6 on the source's set) was described on the
  results page and implemented in no script read; it is not carried.

## Not carried
Every number of the repository's results (code, tokens, cost, time, test and pass rates), its task list, its
repository fixture and its pinned commit, the arm names and prompts of the other rule sets it compares, its
plugin loading flags, and its persona and README prose.

## Where it overlaps
`skills/testing-blocks` §8 (three arms, matrix, exit gate) and `skills/llm-eval-regression-pitfalls` §1 and §2
(baselines, judges, biases) cover the same ground at a higher level. A separate block was kept because the run
hygiene (§1), the instruments (§2) and the judge gates (§4) are a concrete method that neither states. If those
two blocks absorb it later, this one merges into them; `skills/maintaining-blocks` is the owner of corpus
audits, not of evaluation, so it is not the home for this.

## Not verified
1. **Nothing was run.** None of the scripts was executed and no result was reproduced; the source's figures are
   the author's own, self-run, on one model in one harness.
2. **Runtime behaviour** (environment variables, loading flags, the process kill on each platform) was read from
   the script, not observed.
3. **Written by us, not sourced:** the reading of why a leak matters, the advice to throw away a leaked run, the
   "never quote a pass rate on unchecked tasks" guardrail, the example of the user-A and user-B check, the
   "judge fails its gate: stop" paragraph, the limits list of §3.15 beyond what the source states, and the
   routing text of the description.
4. **`tasks.py` was read in part** (header, task table, self-test contract, tail); the individual task scorers
   (about seventy kilobytes) were not read line by line, so the block states how checks are shaped but nothing
   about any single task's check.
