# ai-feature-acceptance-pitfalls §1 — The acceptance bar and the eval set

A model feature has no deterministic guarantee to test. The criterion is a measured bar on a set of examples,
and the set matters as much as the bar.

## 1.1 What an acceptance criterion looks like
1. **Three parts plus one.** The source's form is an eval set, a metric and a threshold, and then what happens
   to the cases that miss. Its own example: on a benchmark of real documents, field accuracy at or above a
   stated level, and every low-confidence case flagged for review. "The extracted date is correct" is not a
   testable criterion for a model.
2. **Say what the misses do.** A threshold without a behaviour on the failures only describes the average
   case; the bar includes the flag, the fallback or the refusal that applies to the rest.
3. **A review looks for the quality word without a number**, and for acceptance criteria that only cover the
   successful path: the source's reviewer rates a section as inadequate when it is filled in but thin
   (present is not adequate).
4. **Example figures are illustrations.** The 90 percent, 95 percent, 85 percent and the error-rate caps in the
   source are examples of the form; the team sets its own from the cost of errors (see 1.5).

## 1.2 The eval set is the spec
1. **Ground truth**: who supplies the correct answers and are they trustworthy. The source notes that when
   human labellers disagree, that disagreement caps the accuracy it is fair to demand.
2. **Representative**: the set reflects real input quality. The source's example: production inputs are messy
   phone photos and the set is clean PDFs, so the quoted figure is fiction. Cover the hard cases on purpose.
3. **Held out**: keep a slice the prompt or model is never tuned on, so the score is not fitted to the set.
4. **Per class**: report by document type or by field, not one blended number, which hides the categories
   that fail.

## 1.3 Currently un-evaluable
1. **A real status, not a gap to paper over.** If there is no labelled set or no way to measure yet, the first
   task is to instrument and measure, not to promise a target. A target with no way to check it is a
   fictional commitment and the spec records it as a risk (source).
2. **The same holds for any metric with no baseline**: the source's metrics reference says to measure first
   and set the target after.
3. **A reviewer who spots this should rate the spec as thin, not absent**: it recognised the situation
   (the source's rubric treats that distinction as part of the review).

## 1.4 Accuracy misleads under imbalance
1. **The trap**: a field that should be empty almost always. A model that always answers "empty" scores a high
   accuracy and is useless; one that fills it too eagerly produces a flood of wrong data at a small error
   rate (source).
2. **Use precision and recall.** Precision: of the items the model filled or flagged, how many were right;
   favour it when a false positive is expensive (a wrong auto-filing, an invented value). Recall: of the
   items that should have been caught, how many were; favour it when a miss is expensive (a defect that goes
   unnoticed). F1 balances the two.
3. **Which one matters is a product decision, stated with its reason**, not a modelling detail (source).

## 1.5 Error costs are not symmetric
1. **Write down what each kind of error costs** and let it set the targets (source).
2. **Set false-positive and false-negative targets separately** rather than one accuracy figure. The source's
   example: a quality pre-check that nags on a clean page is a mild annoyance, one that lets a blank page
   through is worse, so the two rates get different limits. The figures it gives are examples only.
3. **A hard cap on the worst error** (the source's example is a wrong auto-archive that passes review,
   costly for compliance and rework) belongs in the spec as its own line.
