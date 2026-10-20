# ml-training-and-evaluation-pitfalls §2 — Runs, failures and artifacts

Sources: the troubleshooting reference of the sentence-transformer training skill and the `huggingface-llm-trainer` skill of huggingface/skills at c3ff942, read 2026-10-20. Points marked "own guidance" are not from a source.

## 2.1 Out of memory and NaN: the order of recovery
1. **For out-of-memory, change in this order and one at a time:** smaller per-device batch (compensating where the loss allows with an inner mini-batch or gradient accumulation); half-precision of the type your GPU supports; gradient checkpointing; shorter maximum sequence length; adapter-based tuning for large decoder bases; then a bigger or several GPUs. Each step changes speed or quality, so note which one you took.
2. **Gradient checkpointing conflicts with the cached variants of some losses** and shows up as an autograd error ("does not require grad"). Turn it off for those, since they organize their own forward and backward passes.
3. **Shrinking the candidate list of a listwise loss is an experiment change, not a memory setting,** and is the last resort. Lower the loss's own mini-batch first; the memory of some pairwise weightings grows with the square of the list length and may not respond to it.
4. **For NaN or infinite loss, lower the learning rate first,** add a warmup (a fraction of the steps), prefer bfloat16 over float16 where available, clip the gradient norm for unusual setups, and inspect the data for empty or broken rows and for inputs that tokenize to nothing.
5. **A loss that is hugely larger after a step, with a healthy-looking data sample, is usually the rate.** Do not search the model code before trying a smaller rate and a warmup.

## 2.2 Hangs and silent selection
1. **A run that hangs at the first evaluation has an evaluation schedule but no evaluation data** (or an empty one). Give it data or turn the schedule off.
2. **A multi-GPU run that hangs at start:** check the dataset class reports a consistent length on every process, that a no-duplicates sampler has enough data for the number of processes, that the framework and CUDA versions match on every node, and raise the communication timeout.
3. **If the key used to pick the best checkpoint does not match a metric the evaluator writes, the trainer silently keeps the last checkpoint.** Print the metric names once and copy the key from the printed list.
4. **Check the tracker is the one you configured** when no metrics appear: the reporting option, its login or key, and, on a rented machine, that the key was passed as a secret.

## 2.3 Ephemeral machines and timeouts
1. **A rented training machine is thrown away at the end,** so results exist only if they were pushed to a hub or a bucket during the run. Enable the push, give the job write access, and verify the repository after a short test run, not after the long one.
2. **The job's timeout must exceed the expected duration with margin.** The source warns that its default is too short for most training and that exceeding it loses all progress. Estimate the duration and cost first, and set the timeout above it.
3. **Prefer checkpointing to the hub or bucket at intervals,** so a failure at hour three loses minutes (own guidance).
4. **Submit asynchronously and report the job identifier and monitoring link;** do not poll in a loop (the source advises checking on request). Logs may take a minute to appear.
5. **For a demo on a small card, drop the evaluation set and its schedule to save memory,** and say that you did (the source gives this tip; re-read before relying on the saving).

## 2.4 Tokens, saving and loading
1. **A hub push that fails with an authorization error is usually a token without write permission, a missing login on the machine, or a missing secret on the job.** Check who the machine thinks it is before regenerating anything.
2. **Pass tokens to a job as secrets by reference,** never inline in the script or the log. The same applies to tracker keys.
3. **A custom module defined inline in the training script is saved under the script's own entry-point name and cannot be loaded from any other script.** Put it in an importable module, or build the head from stock modules, or state that the model loads only from the same script.
4. **Test the load path from a fresh process** (a different script, with only the saved folder and the package) before announcing the model (own guidance).
5. **Prefer weight formats that cannot run code on load,** and treat a pickled checkpoint from a hub as code you are about to execute (own guidance, re-read the loader's current default before relying on it).
6. **Pooling must match the architecture:** mean pooling over causal attention is wrong for decoder models, which want last-token pooling. A model that "loads" but encodes garbage often has the wrong pooling or the wrong base.

## 2.5 Checks (own guidance)
1. A one-step smoke run on a few rows passes: data format, memory, evaluation, push and tracker.
2. The timeout, the expected duration and the checkpoint interval are written down together.
3. Nothing needed later exists only on the machine that ran the job.
4. The saved model was loaded and queried in a fresh process, and gave the metric the run reported on a small sample.
