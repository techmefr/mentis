# assumption-validation-pitfalls §1 — Criteria, budget and the smallest test

A hypothesis is a structured statement with criteria and a time budget, not a hunch with a test attached.
Everything below is fixed before the test starts, because a test with no stated way to fail will confirm.

## 1.1 What is written before testing
1. **Five things** (shinpr hypothesis-discipline):
   - what we believe;
   - how we will know we are right, as a measurable observation;
   - how we will know we are wrong, as a measurable observation;
   - the validation method (prototype, data analysis, interview, code spike, market research);
   - the time budget, the maximum spent before a forced decision.
2. **One hypothesis, one test.** Each validation yields an interpretable result for one hypothesis.
3. **Separate creating from judging.** Generate candidate hypotheses first, then evaluate them (same source).
4. **A template** (fields from the source, layout ours):

   ```
   We believe that:          one statement
   We will know we are right when:   measurable, observable
   We will know we are wrong when:   measurable, observable
   Method / time budget / deadline:  type | maximum effort | date
   Status:   draft | testing | validated | invalidated | inconclusive | adopted | rejected | timeout
   ```

## 1.2 Time budget and the forced decision
1. **Every hypothesis has a time budget and a deadline** (the source's examples are a day, a week, two weeks).
   A validation without them does not end by decision.
2. **A passed deadline without a conclusion is a timeout**, and a timeout forces a choice: extend with a
   written justification, pivot, or abandon (shinpr hypothesis-discipline and recipe-validate).
3. **Pivot means changing the hypothesis on the partial evidence**; abandon means stopping and recording what
   the partial evidence taught (recipe-validate).
4. **Extending needs a reason in writing**, not a default; the extension gets its own deadline (own guidance,
   built on point 2).

## 1.3 Break the hypothesis down and aim at the weakest part
1. **A hypothesis bundles assumptions.** Decompose it into individual testable ones and classify each by risk
   type: value, usability, feasibility, viability (shinpr hypothesis-verifier).
2. **Rank by risk**, from the uncertainty of the evidence, the decision a wrong assumption would change and
   how reversible that decision is. Test the highest first.
3. **Ask for the smallest test that could disprove it**, and pick the assumption whose disproof can change the
   current decision. Leave the others as unresolved inputs, noted with the decision that would need them.
4. **Methods by what they measure** (same source):

   | Method | Fits | Shows |
   |---|---|---|
   | Prototype test | usability or value | whether users can and will do the target actions |
   | One-question survey | value or viability | whether the assumed behaviour or preference exists, at scale |
   | Data mining | any, if data exists | whether existing data supports or contradicts it |
   | Research spike | feasibility | whether the technical approach is viable within constraints |

## 1.4 Keep the test honest
1. **Define the criteria independently of the author.** The verifier's rule: success and failure criteria set
   apart from whoever wrote the hypothesis, in a separate context, to avoid anchoring (shinpr).
2. **Seek disconfirming evidence.** Look actively for reasons the hypothesis might be wrong.
3. **Check interpretation risk only where it can flip the verdict**: confirmation, selection, anchoring,
   survivorship, an alternative explanation that produces the same "success". Record the evidence, the verdict
   it could flip and the smallest control that settles it. An empty list is valid.
4. **Say how to tell a real result from coincidence**, and name the extra evidence that would strengthen it
   (shinpr hypothesis-verifier).
5. **Define "inconclusive" in advance.** A designed test has a path to disproof and permits an inconclusive
   result (same source).
6. **For online controlled experiments use `experiment-design-pitfalls`**; this section covers discovery-stage
   tests (prototypes, interviews, data mining, spikes).
