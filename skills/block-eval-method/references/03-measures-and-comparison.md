# block-eval-method §3 — Measures and the per-task comparison

> Section 3 of `skills/block-eval-method`. Read it when results have to become a claim. For baselines and
> assertions in general see `skills/llm-eval-regression-pitfalls` §1; for the arms and the matrix see
> `skills/testing-blocks` §8.

## What is measured
1. **Delivered size is what the run added, not what a chat reply contains.** On a task inside a seeded
   repository, count the lines added in code files by a diff against the seeded base, tests excluded, lockfiles
   and generated files skipped. On a task that writes a fresh file, count the code files delivered. When the
   agent answered in chat and wrote nothing, count the fenced code of the reply so an answer is not scored as
   zero.
2. **Add a second size proxy that packing lines does not defeat:** the compressed size of the delivered code.
   Repeated names and boilerplate compress well, so fusing statements onto one line gains much less on it than
   on a line count. Read it next to lines, not instead.
3. **Cost, time and turns come from the harness's own output,** never from a clock you started. Reply length is
   reported and never scored (§4.12).
4. **A run killed at the timeout is its own category.** It delivered nothing: count it apart, do not score it
   as a zero in a size average, and do not judge it for completeness.

## One task, one pair
5. **For each task and arm, take the median of the repeated runs** (the rate, for a pass/fail measure). Run
   each cell several times: one run measures luck (`skills/testing-blocks` §8.6).
6. **Compare arms task by task,** B against A on the same task, not pooled over tasks. A pooled mean lets one
   large task decide the result.
7. **Report the median of the per-task ratios B over A,** so a task of 300 lines and a task of 12 lines weigh
   the same.

## The sign test
8. **For each measure, count the tasks B wins, the tasks B loses and the ties,** with ties dropped. Whether
   "lower" or "higher" is better is fixed per measure beforehand (fewer lines, lower cost, higher pass rate).
9. **Two-sided sign test over the tasks that were not ties:** the probability of a split at least this uneven
   if B and A were equally likely to win a task. It is coarse and it is honest: it assumes nothing about the
   distribution, which a handful of runs per cell cannot support.
10. **Say "better on X of Y tasks"** with that probability. Never say "X% better" from a mean the test does
   not back.

## Iterating cheaply
11. **Re-run only the candidate arm on a short hand-picked task list** (one task per failure mode the full run
   showed), and pair its cells with the reference arms of an earlier full run in the comparison. Iterating on a
   rule set then costs only the candidate's cells.
12. **Re-pick the short list from the full run when the failure modes move,** and say in the report that it is
   a hand-picked subset.

## Quality, size and cost together
13. **Read size next to completeness (§4.1).** An arm with fewer lines whose completeness also fell is doing
   less, not less building.
14. **Read cost next to the pass rate on the checked tasks.** A cheaper arm that fails more is not cheaper.

## Limits to write down every time
15. One model, or the listed models, and one harness.
16. The tools that were off, and therefore what the run did not measure.
17. Which tasks had a hidden check, and that those checks are a floor and not a proof: passing them does not
   make the code secure or correct in general.
18. How many runs per cell, and that the comparison can only disprove a block's value as well as confirm it:
   if the arms converge, say they converged.
