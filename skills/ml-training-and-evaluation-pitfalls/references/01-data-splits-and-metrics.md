# ml-training-and-evaluation-pitfalls §1 — Data, splits and metrics

Sources: the troubleshooting reference and the dataset notes of the sentence-transformer training skill, and the `huggingface-llm-trainer` skill, of huggingface/skills at c3ff942, read 2026-10-20. Points marked "own guidance" are not from a source.

## 1.1 The data must match what the objective expects
1. **Each training method expects its own columns:** supervised tuning wants conversation or text columns, preference methods want a chosen and a rejected answer, online reinforcement methods want prompts only. The source also notes that for some objectives the number and order of columns matter and their names do not.
2. **Validate an unfamiliar dataset on a handful of rows before any paid run.** Print a few rows, count columns, and look for empty strings, missing labels and mismatched column counts. A format failure on the first step of a GPU job is the most avoidable cost.
3. **Check the label convention against the loss.** One example from the source: a ranking head with a single output goes with a binary objective, two or more outputs with a multi-class one; the mismatch is raised late and cryptically.
4. **Do not take a task-specific fine-tune as a base for a different task.** A checkpoint tuned for question answering carries a head that is not a pooling layer, and encoding with it returns constant or garbage vectors.
5. **Pin the dataset and the base model to a revision** (own guidance). A hub name alone can change under you, and then two runs of the same script are not the same experiment. Record the revision, the licence of the data and the licence of the base model next to the result.

## 1.2 Splits and leakage
1. **A metric that is perfect at the first evaluation means the evaluation set overlaps the training set.** The source's fix is to confirm the split call was done correctly and that the hub dataset's training and development splits really are disjoint. Look for duplicates across splits, not only for the same index.
2. **Split before fitting anything** (own guidance): scalers, vocabularies, feature selectors and deduplication statistics are fitted on the training part only. Fitting them on everything is leakage that no later check shows.
3. **Split by the unit that must generalize** (own guidance): by user, document, patient or time window, not by row, when rows of one unit are alike. A random row split on time-ordered data tests on the past of its own training set.
4. **Keep a test set that nobody tunes against.** Choose hyperparameters on the evaluation split and report once on the test split (own guidance).
5. **An evaluation set drawn from the training distribution tells you about that distribution only.** Say which one it is when reporting.

## 1.3 Baselines and metrics that do not move
1. **Measure the untouched base model and a trivial baseline with the same evaluation first.** Without them, a number has no meaning, and "after training the metric equals the metric before" cannot be seen.
2. **When metrics stay at the baseline, check in this order:** column order and label detection; whether the negatives or the task are too easy; whether the key that selects the best checkpoint matches the key the evaluator writes (§2.2); whether the base model fits the task; whether the learning rate is far too low for this kind of model; whether the dataset is too small for the chosen loss.
3. **Learning rates are not portable across model families.** The source gives different typical ranges for encoders, adapter-based tuning and static embeddings (re-read the current guidance); a rate from another recipe is the usual cause of both flat and diverging runs.
4. **A training loss on its own can mislead.** For some ranking losses the printed value is tiny by construction; judge by the evaluation metric, not the loss magnitude.
5. **Metrics that read the raw output need the right output transform.** The source describes a ranking model whose default squashing function saturated and destroyed the ordering after distillation-style training; use the identity there and the squashing function only with the binary objective.
6. **Report spread, not one run** (own guidance): several seeds for any claim of a small improvement, and say that the seeds were fixed or not.

## 1.4 Checks (own guidance)
1. Count rows shared between train and evaluation (exact and near duplicates). The count is zero or explained.
2. List what was fitted before the split. The list is empty.
3. The baseline number, the trained number, the evaluation split and the revisions are in one table.
4. A first-step score near the maximum, or a score identical before and after training, is investigated before it is reported.
