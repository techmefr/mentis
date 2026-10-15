---
name: skill-trigger-eval-pitfalls
description: "Use when it has to be measured whether a skill description makes an agent load the skill at the right moments and not at the wrong ones: the query set (should-trigger queries that hide the domain, near-miss negatives, realistic wording), repeated runs and trigger rates, why a one-step request may never trigger, and optimising the description without overfitting (train and validation split, selecting the iteration by validation, fresh queries at the end, character limit, keyword stuffing)."
---

# skill-trigger-eval-pitfalls

A block for the moment a skill description is rewritten to "trigger better". The two sections share one
premise: **a description is tuned against a sample of phrasings, and a description tuned on all of the sample
only remembers it**. Whether the skill, once loaded, produces good output is a different measurement and is in
`llm-eval-regression-pitfalls` (baseline, assertions, judges, errors and retries); this block does not repeat it.
Writing the skill itself is in `writing-skills`.

## When
- A skill never loads when it should, or loads on tasks it has nothing to do with.
- A description is being rewritten and the only evidence is "it worked on my prompt".
- A skill is added to a set that already has neighbours with overlapping vocabulary.
- A description is long, full of quoted phrases, or close to the character limit.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Trigger queries and runs: what triggers, should-trigger and near-miss queries, realism, repeated runs, trigger rate, observability | a trigger eval set is written or its results look noisy | [`01-trigger-queries-and-runs.md`](./references/01-trigger-queries-and-runs.md) |
| 2 | Description optimisation: writing principles, character limit and keyword stuffing, train and validation split, the loop, picking the iteration, final check | a description is being changed after an eval | [`02-description-optimisation.md`](./references/02-description-optimisation.md) |

## Output / checkpoint
The query set has near-miss negatives and positives that do not name the domain, every query was run several
times and has a rate, not a single verdict (§1). The description was changed from train failures only, the
chosen iteration is the one with the best validation pass rate, and a few fresh queries that never took part
confirmed it (§2). A description that was tuned until every query passed and never checked on unseen queries
is not verified.

## Guardrails
- Never use obviously irrelevant negatives; they test nothing (§1).
- Never judge a query from one run; triggering varies between runs (§1).
- Never feed validation results into the changes you make to the description (§2).
- Never add keywords copied from failed queries; address the category they stand for (§2).
- Never treat a clean lint result as a trigger result; a lint checks the shape of a description, not whether
  an agent acts on it (§2).
- Restates the documentation of two projects as of the commits in [`references/origin.md`](./references/origin.md).
  No trigger eval was run while writing it. The character limit stated is the portable specification's; the
  limit of a specific client was not found in a file read and is not stated.

## Origin
Rewritten from the Agent Skills documentation site's guides on optimising descriptions and the format
specification (CC-BY-4.0, credited) and from the frontmatter checks and documentation of an independent skill
validator (MIT), read 2026-10-16. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
