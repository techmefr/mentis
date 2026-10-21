# ml-training-and-evaluation-pitfalls: origin and source stamps

> Provenance of `skills/ml-training-and-evaluation-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation-style skill files, never run by us on a GPU, a training job or a model
hub. No model was trained, downloaded or pushed while writing it.

## Sources (read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| huggingface/skills at commit c3ff942: `skills/train-sentence-transformers/references/troubleshooting.md` | Apache-2.0 (`LICENSE` read 2026-10-20) | Out-of-memory order, NaN causes, flat metrics causes, evaluation hangs, best-checkpoint key mismatch, cached-loss conflict, perfect-score overlap, saturating output transform, inline module loading failure, pooling and wrong-base symptoms, authorization and tracker checks |
| huggingface/skills at c3ff942: `skills/huggingface-llm-trainer/SKILL.md` | Apache-2.0 (same file) | Ephemeral machine and push requirement, timeout warning, dataset validation before paid runs, columns per method, secrets for tokens, asynchronous submission |
| Hugging Face Hub documentation: jobs guide, pickle security page | product documentation, facts only, rewritten, read 2026-10-20 | Default job timeout, secrets encrypted, pickle code execution |

| scikit-learn user guide: common pitfalls page and cross-validation page (the project is BSD-3-Clause, LICENSE read 2026-10-20 on the repository) | BSD-3-Clause; documentation facts only, rewritten | Fit after split with the 0.76 versus 0.5 example, inconsistent preprocessing example, grouped and time-series splitting, test-set leakage from tuning, seed effect on scores |
| Google Machine Learning Crash Course: dividing datasets, overfitting and interpreting loss curves pages | CC BY 4.0 for the page text (stated on the pages, read 2026-10-20); credit: Google for Developers | Duplicates between sets, repeated test use, representative data, loss-curve divergence |
| Hugging Face: transformers Trainer documentation, datasets loading guide, dataset-card pages, Hub jobs configuration page, Hub pickle page; PyTorch: `torch.load` page, automatic mixed precision examples; OpenAI supervised fine-tuning guide | Product documentation, facts only, rewritten, read 2026-10-20 | Best-model arguments, gradient checkpointing cost, warmup, revision argument, read-only mounts and bucket outputs, retries restart the command, weights-only default, unscale before clipping, held-out data and 50-example start |

## Extension 2026-10-20
§3 (training data hygiene) is own guidance from craft knowledge; only 3.1.2, 3.3.4 and the new 3.3.5 were checked against a source on 2026-10-20, and no source text was taken. Searched for a source on label audit, personal-data memorisation and licence clearing in the dataset-card, Crash Course and OpenAI fine-tuning pages: nothing specific found (the OpenAI page gives no personal-data guidance).

## Removed (stated in the sources, not carried)
- Every loss, evaluator, trainer-argument, hardware-tier and base-model recommendation and every numeric threshold or rate range (kept as the qualitative point only, marked re-read).
- Tool-call syntax of the job runner, example scripts, cost tables and plan requirements.
- Model-card generation, quantization and local-runtime conversion, the Space, paper and browser-inference skills: other subjects.

## Not verified
1. **Version-bound facts.** Option names, defaults, the conflict between checkpointing and cached losses, and the saturating-default remark are the source's claims at the commit; none was checked against the libraries. Re-read before relying on them.
2. **Own guidance, still labelled in the text:** the recording of licences next to revisions, the practice of reporting several seeds (the seed effect itself is sourced), interval checkpointing, the fresh-process load test, every "Checks" section, and the order of the memory recovery steps (no documentation page gives an order). Sourced and unmarked on 2026-10-20: fit after split, preprocessing consistency, split by unit, held-out test, pinned revision argument, weight formats and the weights-only default.
3. **Other frameworks.** The sources are one hub's tooling; nothing about other training stacks was read. The generic points hold, the names do not transfer.
4. **The Orchestra-Research and K-Dense scientific skills** listed in the review file were not opened.
5. **No command, option or script was executed.**
6. **Checked 2026-10-20:** the 30-minute default job timeout, encrypted secrets and pickle code execution on the Hub pages; the weights-only default on the PyTorch page (the page names no release). Corrected: the "silently keeps the last checkpoint" claim is attributed to the training skill only, because the Trainer documentation says nothing about silence; the pickle page lists several alternatives, not only a code-free format.
7. **Not sourced and left as the training skill's claims:** every option name of the sentence-transformers trainer, learning-rate ranges, the cached-loss conflict, the saturating output transform and pooling advice.

## Related blocks
`llm-eval-regression-pitfalls`, `rag-retrieval-quality-pitfalls`, `analysis-validation-pitfalls`,
`experiment-design-pitfalls`, `cloud-iam-network-and-cost-pitfalls`, `source-freshness`.

Independent verification 2026-10-21: 18 checked, 18 matched, 0 corrected, 0 unverified
