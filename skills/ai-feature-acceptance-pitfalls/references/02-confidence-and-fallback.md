# ai-feature-acceptance-pitfalls §2 — Confidence, human review and dependencies

Once the bar is set, the spec must say what the system does with uncertain output, what it never does, and
what it needs from the business before it can reach the bar.

## 2.1 The confidence threshold is a dial
1. **Split traffic by confidence instead of trusting everything**: above the threshold the output is applied
   or suggested, below it goes to a person (source).
2. **The threshold trades the automation rate against the error rate.** Raising it means fewer automatic
   errors and more manual review. Tune it on the eval set against the cost of each error, not by taste
   (source: do not pick a round number by feel).
3. **Design the review step**: the model proposes with a reason, a person confirms, the system executes;
   highlight the fields that need review and show the reason (source).
4. **Recommendation versus action**: the source's pattern for risky automation is that the smart component
   only proposes and a deterministic layer performs the side effects, so the risky part stays reversible and
   auditable. The spec states which side owns the write.

## 2.2 The needs-review ratio is a guardrail at both ends
1. **Too high** and the model is not saving work.
2. **Too low** and it may be confidently wrong in silence.
3. **Watch both ends** (source).

## 2.3 Never fabricate
1. **When the value cannot be decided, return null and a reason**, not a confident guess. Put "do not strain to
   produce an answer" into the spec for low-confidence cases (source).
2. **On model failure or low confidence, fall back to manual entry**, not to a crash (source).
3. **Track the AI-specific failures**: invented fields, and wrong answers delivered with high confidence
   (source calls them silent errors).

## 2.4 Drift
1. **Accuracy decays when the world changes under the model**: templates, procedures and rules get updated
   (source).
2. **Plan re-evaluation**, not a one-time launch, and state what triggers it. The trigger list itself
   (a schedule, a rule-table change, a drop in the review ratio) is own guidance.

## 2.5 Data and rules are a schedule gate
1. **The model runs on material it does not invent**: labelled eval sets, mapping and rule tables, reference
   taxonomies, ground-truth examples. A missing table or label set blocks the build and caps the accuracy
   (source).
2. **Treat each as a top-priority dependency with an owner and a date**, and gate the phase on it
   (source).
3. **The source's observation is that this, more than the model, is what makes such projects slip**: the
   business material never arrives. State it as the source's claim, not as measured fact.
