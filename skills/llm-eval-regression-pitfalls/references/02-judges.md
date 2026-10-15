# llm-eval-regression-pitfalls §2 — Judges

## 2.1 Deterministic first
1. **Run mechanical checks before any model grades.** The context-engineering skill's pairwise procedure starts
   with deterministic pre-checks: both candidates must satisfy the same schema, evidence and scope constraints.
   The Agent Skills guide adds that scripts are more reliable than a model for mechanical checks. A judge's time
   is for what a script cannot decide.
2. **Direct scoring for criteria with a ground truth;** pairwise comparison for taste. The same skill
   makes this split, and notes that pairwise judgments tend to track human preference better for subjective
   tasks (a claim of that source, not tested here).
3. **One criterion per score.** A criterion that measures two things gives scores nobody can interpret.
4. **To compare two versions, try a blind comparison.** The Agent Skills guide suggests showing both outputs to a
   judge without saying which version made which, scoring holistic qualities on its own rubric, and says this
   complements assertions because two outputs can pass every assertion and still differ in quality.

## 2.2 Rubric and evidence
1. **Ask for evidence before the score,** so the number is anchored in features of the output and the
   judgment can be audited.
2. **Match the scale to the rubric.** A wide scale needs a description of each level; without one,
   calibration is poor.
3. **Write the edge cases into the rubric** with a rule for each, since ambiguous cases cause most of the
   variance.
4. **Version the judge prompt** and rerun the regression set when it changes; small wording changes can move
   scores.
5. **Re-anchor against fresh human-labelled examples now and then;** rubrics drift.

## 2.3 Biases to control
1. **Position:** a first slot is favoured in pairwise comparison. Judge in both orders and call a disagreement
   a tie, or use several shuffles.
2. **Length and verbosity:** longer answers score higher. Tell the judge to ignore length, make conciseness
   a separate criterion, and test with pairs that differ only in length.
3. **Self-enhancement:** a model rates its own family's output higher, so use a different model to judge
   than to generate, and remove model-identifying text before judging.
4. **Authority:** a confident tone scores higher. Require evidence for claims and consider a fact-check step.
5. **Measure the bias in your own data** (first-slot win rate, correlation of score with length) instead of
   assuming a source's figure holds for your task.

## 2.4 The judge reads text you do not control
1. **The submission can contain a fake grade or a fake delimiter.** Inspect's model-graded scorers take two
   precautions: the grade is taken from the last grade line, so an earlier injected one does not win, and
   the data delimiters inside the submission are rewritten so it cannot close the data block.
2. **If you write your own template and pattern, keep both properties** and test with a submission that
   contains a grade line and a delimiter.
3. **An unparseable verdict is unscored,** not a failure or a pass: Inspect records an unscored result with
   the grader's output kept, does not retry the verdict, and metrics skip it (§3).

## 2.5 Panels, fallback and reproducibility
1. **A panel of graders votes;** in Inspect a grade wins only with more than half the panel, and a grader
   that returns nothing parseable does not lower the bar, so a thin panel leaves a sample unscored rather
   than decided by list order. The previous plurality behaviour is available as an option.
2. **Name the grader explicitly.** Inspect picks the model argument first, then the model bound to a grader
   role, and otherwise the model under evaluation; a role marked required raises an error when it is not bound.
   Own guidance: mark it required so a missing grader fails loudly instead of the model grading itself.
3. **Fix the grader's settings** for reproducibility. The documentation says the grader otherwise runs on the
   provider's defaults, often a non-zero temperature and no seed, so borderline grades can change between
   runs and epochs. Set the lowest temperature and a seed where supported, then run several epochs and look
   at the variance, since this reduces but does not always remove disagreement.
4. **Check the judge against people.** Compare to human labels on a sample and watch for systematic
   disagreement on a criterion, which is worse than random noise.
