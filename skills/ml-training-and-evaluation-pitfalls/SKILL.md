---
name: ml-training-and-evaluation-pitfalls
description: "Use when training, fine-tuning or evaluating a machine-learning model, or running a job on rented GPUs: dataset format and splits, leakage and trivially perfect scores, baselines, out-of-memory and NaN loss, checkpoints that are silently not the best, results lost with an ephemeral machine, pinned model and dataset revisions, and loading what you saved."
---

# ml-training-and-evaluation-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the traps of training and measuring a model that the application
blocks do not see. The premise: **a training run almost always finishes and prints numbers, so the failures are
the wrong numbers and the lost results**: a score that is perfect because the evaluation set overlaps the training
set, a "best" checkpoint that is just the last one, a job that timed out with nothing pushed, a model that saves
fine and cannot be loaded from another script. Prompt and agent evaluation is in `llm-eval-regression-pitfalls`;
retrieval is in `rag-retrieval-quality-pitfalls`; the account and cost side of a rented machine is in
`cloud-iam-network-and-cost-pitfalls`.

## When
- A model is trained or fine-tuned (supervised, preference, ranking or embedding objectives), locally or on rented GPUs.
- A dataset is chosen, split or reformatted for training.
- A run fails with out-of-memory, NaN loss or a hang, or finishes with metrics that do not move or look too good.
- A model or dataset is downloaded from a hub, saved, pushed or loaded elsewhere.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Dataset format, splits, leakage, baselines, trivially perfect and unmoving metrics, pinned revisions | a dataset is chosen or split, or a score is read | [`01-data-splits-and-metrics.md`](./references/01-data-splits-and-metrics.md) |
| 2 | Memory and NaN recovery order, hangs, best-checkpoint selection, ephemeral machines, timeouts, tokens, saving and loading | a run is configured, fails, or its output must survive | [`02-runs-failures-and-artifacts.md`](./references/02-runs-failures-and-artifacts.md) |

## Output / checkpoint
Each section ends with its own checks. For a change touching this block: the split is disjoint and was made before
any preprocessing was fitted, a baseline was measured with the same evaluation, the format was validated on a few
rows before a long run, the job's timeout exceeds its expected duration and its outputs leave the machine, and the
saved model was loaded from a fresh process.

## Guardrails
- Make the split before anything is fitted, and check that train and evaluation share no rows (§1.2). Never trust a first-step score of 100 percent.
- Measure a baseline with the same evaluation before claiming an improvement (§1.3).
- Validate the dataset format on a small sample before a paid run (§1.1).
- Change one thing at a time when recovering from memory errors, in the order of §2.1. Never shrink the experiment (list length, sequence length) as if it were a memory knob.
- Push outputs off the machine before the job ends and set a timeout longer than the run (§2.3). Never rely on an ephemeral disk.
- Never put a token in a script or a log; pass it as a secret (§2.4).
- Library names, option names and defaults move between versions; re-read the version in use before relying on one (🟡, nothing here was run).

## Origin
Rewritten from the `huggingface/skills` repository (Apache-2.0, commit c3ff942), read 2026-10-20. Leakage and
reproducibility points beyond the source are our own guidance and are labelled. See
[`references/origin.md`](./references/origin.md).
