# assumption-validation-pitfalls §2 — Confidence, evidence and recording results

Confidence is a record of evidence, not a mood. It moves when evidence arrives, it can fall, and how much
is enough depends on what the decision costs and whether it can be undone.

## 2.1 Four risks, one confidence each
1. **Four risks** (shinpr product-principles): value (will they use or buy it), usability (can they work out
   how to use it), feasibility (can we build it) and viability (does it work as a business).
2. **Track confidence per risk**, not as one number: different risks differ (shinpr hypothesis-discipline).
   The source scores each from 0 to 10; that scale is one author's choice and this block does not require it.
3. **Evidence ladder** (product-principles, qualitative form): no evidence beyond a feeling, then a structured
   evaluation (expert review, competitive analysis), then data (analytics, surveys, interview patterns), then
   something tested and confirmed (prototype validation, an A/B test, a beta).
4. **Show current confidence and the remaining risks** next to each user story or scope item, so readers see
   what is still assumed.

## 2.2 How much is enough
1. **Validated enough follows cost, risk and reversibility** (shinpr). A cheap, reversible change (a feature
   flag, a gradual rollout) needs a structured evaluation; a medium-cost one needs data; a costly irreversible
   one (a platform or pricing change) needs tested results.
2. **The table calibrates judgment, it is not a numeric gate**: the evidence required follows the cost, the
   risk, the reversibility and the decision at stake (same source).
3. **Do not spend validation effort on a decision it cannot change.** The source ties further research to a
   current decision that it could change.

## 2.3 Updating confidence
1. **Update only when new evidence is gathered**, and record the evidence that justified each change
   (shinpr hypothesis-discipline).
2. **Confidence can go down**: negative evidence is evidence.
3. **Keep a before, after and evidence line per risk**:

   ```
   Risk        | Before | After | Evidence
   Value       |        |       |
   Usability   |        |       |
   Feasibility |        |       |
   Viability   |        |       |
   ```
4. **Link the evidence**: data, screenshots, prototype results, interview notes.

## 2.4 Recording a result
1. **Write the result with its evidence**, the final confidence values and the decision learning: conclusions
   and evidence that could change confidence, the parent opportunity or a later decision (shinpr).
2. **Leave out working narration and baseline knowledge nobody will use** (same source).
3. **Update the parent opportunity** if the result changes what is understood about it.
4. **Inconclusive is honest.** When evidence is insufficient say so instead of forcing a verdict, and name
   what would settle it.
5. **A rejected or invalidated hypothesis stays in its file** as a learning asset: it records what does not
   work and why (shinpr). Rejected is not worthless.
6. **The result is reviewed by a person** before the workflow moves on (recipe-validate): the outcome, the
   updated confidence, the learnings and the next actions are put in front of the decision-maker.
