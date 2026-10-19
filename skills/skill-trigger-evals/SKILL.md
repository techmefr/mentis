---
name: skill-trigger-evals
description: "Use when a skill's description has to be tested for whether it makes an agent load the skill at the right moments: about twenty labelled prompts (should-trigger and near-miss should-not-trigger), a train and validation split, repeated runs and a trigger rate, reading the result, and picking the best iteration. Also covers the separate with-versus-without eval of the skill's output once it has loaded."
---

# skill-trigger-evals

Cross-cutting (`WORKFLOW.md` §2), the method for measuring a description. A description is the only thing an
agent reads before deciding to load a skill, so "it worked on my prompt" is not evidence either way. The
pitfalls that spoil such a measurement (easy negatives, single runs, overfitting, keyword stuffing) are in
`skill-trigger-eval-pitfalls`; whether a loaded skill produces good output is in `llm-eval-regression-pitfalls`;
writing the description in the first place is `writing-skills` points 25 to 30.

## When
- A skill never loads when it should, or loads on tasks it has nothing to do with.
- A description is about to be rewritten, or a skill is added next to neighbours with overlapping vocabulary.
- A block is about to be shared (`distributing-blocks`) and its routing has never been run.

## Steps

1. **Check the frozen limits first.** The description is within the specification's 1024 characters and the
   skill is registered where the agent client discovers skills. `python3 bin/test_frontmatter.py` covers the
   first; the second is client-specific, so check it before blaming the wording.
2. **Write about twenty labelled prompts**: 8 to 10 that should trigger and 8 to 10 that should not. Store them
   as a list of `{query, should_trigger}`. Starting size from the Agent Skills guide, not a law.
   - Should-trigger: vary phrasing (formal, casual, typos), explicitness (names the domain or only describes the
     need), detail (terse or context-heavy) and complexity (one step, or buried in a longer chain). The useful
     ones are those where the link to the skill is not obvious from the prompt.
   - Should-not-trigger: **near-misses** that share keywords or concepts with the skill but need something
     else, including the territory of an installed neighbour. An unrelated prompt tests nothing.
   - Write them as users type: file paths, personal context, column or company names, abbreviations.
   Query-set detail and its failure modes: `skill-trigger-eval-pitfalls` §1.
3. **Split once, and keep the split.** About 60% train, 40% validation, each holding a proportional mix of
   positives and negatives, shuffled at random and fixed across iterations.
4. **Run every query several times and record a rate.** Three runs is the guide's starting point. Trigger rate =
   runs in which the skill was loaded over runs. The skill counts as triggered when the agent loaded its
   `SKILL.md`, as seen in whatever log, tool-call history or verbose output the client offers. A should-trigger
   query passes at a rate above a threshold (0.5 is the default); a should-not-trigger query passes below it.
   Twenty queries at three runs is sixty runs: script it. If the client allows it, stop a run as soon as the
   outcome is clear (the skill was consulted, or work started without it).
5. **Read the result before touching the description.** Evaluate on train and validation, but let only train
   failures drive the edits: which should-trigger queries missed, which should-not-trigger queries fired.
   - Misses suggest the scope is too narrow: broaden it or say more about when the skill helps.
   - False triggers suggest it is too broad: state what the skill does not do, or the boundary with the
     adjacent capability.
   - Address the category a failed query stands for, never its keywords; that is overfitting.
   - Stuck after several rounds: change the structure of the description, not the wording.
   - Re-check the length cap each round; descriptions grow while being optimised.
6. **Repeat to about five iterations**, then **choose by validation pass rate**, which may be an earlier
   iteration than the last. If nothing improves, suspect the queries (too easy, too hard, mislabelled) before the
   description.
7. **Apply and confirm on fresh prompts.** Write the chosen description into the frontmatter, re-run
   `python3 bin/test_frontmatter.py`, then run 5 to 10 new queries that never took part, a mix of both labels.
   Only that result says whether it generalises.
8. **Output quality is a second, separate eval**, run once the skill triggers:
   - Cases hold a realistic prompt, a plain-language expected output and optional input files; start with two or
     three, with varied phrasing and at least one boundary case.
   - Run each case twice from a clean context, with the skill and without it (or with a snapshot of the previous
     version of the skill as baseline), saving outputs and the tokens and duration of each run.
   - Write assertions after the first outputs exist: objectively checkable, specific, not brittle on wording;
     use a script for mechanical checks and a judge for the rest. A pass needs quoted or referenced evidence.
   - Aggregate pass rate, time and tokens per configuration and read the delta, then look at patterns:
     assertions that pass in both configurations or fail in both carry no information; those that pass only
     with the skill show what it adds; inconsistent results across runs point to ambiguous instructions.
   - A human reviews the outputs next to the grades and records specific feedback per case.
   - Feed failed assertions, the feedback and the run transcripts to a reviser together with the current skill,
     with the advice to generalise, keep the skill lean and explain the why; rerun in a new iteration; stop when
     feedback is empty or gains flatten.
   Assertion design, judges and flaky cases in depth: `llm-eval-regression-pitfalls`.

## Output / checkpoint
The query file with its split, the per-query trigger rates for train and validation, the description chosen and
the iteration it came from with its validation pass rate, and the fresh-query result. A business-layer or
cross-cutting block has no pipeline checkpoint; this block writes none.

## Guardrails
- Never call a description tuned until every query passes "verified": without validation and fresh prompts it
  only remembers the sample.
- Never feed validation results into the edits.
- Never judge from one run; triggering varies between runs.
- A hosted or automated eval service is not a dependency of this block (rule B); the method is the run
  count, the split and the rates, and a script of our own does the counting.
- Not run by us: no client was observed while writing this block, the numbers are the guide's starting points.
  What was not read or verified is in [`references/origin.md`](./references/origin.md).

## Origin
Rewritten from the Agent Skills guides on optimising descriptions and on evaluating skill output quality, and
the specification's description limit (CC BY 4.0, credited), agentskills/agentskills commit 69ef37e, read
2026-10-19. 🟡 never dogfooded: details in [`references/origin.md`](./references/origin.md).

**Adaptation note (Claude Code).** The guide's example script detects a trigger from the JSON output of a
non-interactive Claude Code run by looking for a Skill tool call naming the skill. Other clients need their own
detection; the method above does not depend on it.
