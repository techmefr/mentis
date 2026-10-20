# ml-training-and-evaluation-pitfalls §3 — Training data hygiene

All points in this file are own guidance; no source was read for them.

## 3.1 Duplicates and contamination
1. **Duplicates inside the training set inflate memorisation.** Symptom: the tuned model repeats a rare
   passage verbatim, or a template dominates outputs. Check: count exact duplicates, then near duplicates (same
   text after lowercasing and whitespace collapse). Fix: deduplicate, keeping one per cluster.
2. **Duplicates across train and evaluation are leakage** (see §1.2). For instruction data, the same task
   phrased differently counts: compare normalised prompts, not only the answers.
3. **Public benchmark items inside scraped data** make a benchmark score meaningless. Check: search the
   training text for the evaluation questions and answers before reporting. Fix: remove the items, or report the
   score as contaminated.
4. **Model-generated data carries its generator's habits and errors.** Symptom: the tuned model copies a
   phrase tic or a repeated wrong fact. Fix: sample and read generated rows, filter by an independent check, and
   record which model produced them and under which terms of use.

## 3.2 Personal and confidential content
1. **A tuned model can reproduce training text.** Symptom: an email address or a name appears in a completion
   for a neutral prompt. Check: prompt with the first words of rows that hold personal data and see whether the
   rest comes back. Fix: remove or replace personal data before tuning; deletion after tuning means retuning.
2. **Minimise before collecting** (`llm-pii-and-data-handling-pitfalls` §1): fields that do not teach the target
   behaviour stay out, and detection is a second layer with known misses.
3. **Confidential customer data is not tuning data by default.** Check the contract and consent for that use
   before including it; per-customer data in a shared model can surface to another customer.

## 3.3 Labels and licences
1. **Audit a random sample of labels by hand, per class.** Symptom: a ceiling on the metric that no change
   moves. Check: two readers label the same sample; low agreement means the task or the guideline is unclear,
   not that the model is weak. Fix: rewrite the guideline, relabel, and keep the disagreement cases.
2. **Label noise is not uniform.** Look at the rare classes and at examples the current model gets "wrong" with high
   confidence; they are often labelling mistakes.
3. **Record the licence and provenance of every data source** next to the revision (§1.1.5): scraped text, a
   hub dataset, vendor-labelled rows, generated rows. A source with no stated licence is not cleared by being
   public. The decision belongs to the owner, not to the data engineer; not legal advice.
4. **A dataset card in the repository** lists sources, collection dates, cleaning steps, exclusions and known
   gaps, so a later run can be compared with this one.

## 3.4 Checks
1. Exact and near-duplicate counts within train and between train and evaluation are written down; the second is zero.
2. Evaluation and benchmark items were searched for in the training text.
3. A personal-data scan and a regurgitation probe were run on the tuned model.
4. Per-class label agreement on a hand-checked sample is reported.
5. Every source row has a licence, a provenance and a collection date, or it is excluded.
