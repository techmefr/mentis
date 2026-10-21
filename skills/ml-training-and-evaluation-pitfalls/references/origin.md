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

## Extension 2026-10-20
§3 (training data hygiene) is own guidance from craft knowledge; no source was read for it and no source text was taken.

## Removed (stated in the sources, not carried)
- Every loss, evaluator, trainer-argument, hardware-tier and base-model recommendation and every numeric threshold or rate range (kept as the qualitative point only, marked re-read).
- Tool-call syntax of the job runner, example scripts, cost tables and plan requirements.
- Model-card generation, quantization and local-runtime conversion, the Space, paper and browser-inference skills: other subjects.

## Not verified
1. **Version-bound facts.** Option names, defaults, the conflict between checkpointing and cached losses, and the saturating-default remark are the source's claims at the commit; none was checked against the libraries. Re-read before relying on them.
2. **Own guidance, labelled in the text:** all of §1.2 beyond the overlap fix (fit after split, split by unit, held-out test), pinned revisions, seeds and spread, interval checkpointing, load test, weight formats, every "Checks" section.
3. **Other frameworks.** The sources are one hub's tooling; nothing about other training stacks was read. The generic points hold, the names do not transfer.
4. **The Orchestra-Research and K-Dense scientific skills** listed in the review file were not opened.
5. **No command, option or script was executed.**
6. **Checked 2026-10-20:** the 30-minute default job timeout and pickle code execution. The torch weights-only loader default page redirected and was not read.

## Related blocks
`llm-eval-regression-pitfalls`, `rag-retrieval-quality-pitfalls`, `analysis-validation-pitfalls`,
`experiment-design-pitfalls`, `cloud-iam-network-and-cost-pitfalls`, `source-freshness`.
