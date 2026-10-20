# ai-product-ux-pitfalls §1 — Trust and expectations

All points in this file are own guidance.

## 1.1 Showing how far to trust
1. **Fluent text reads as true.** Symptom: users act on a wrong answer because it looked finished. Check: ask
   five users to say, from the screen alone, which parts were looked up and which were generated. Fix: separate
   quoted or retrieved material from generated text visually, and label drafts as drafts.
2. **Show the basis, not a score.** A source link, the document date and the passage beat a percentage. A
   confidence number that was never compared with outcomes invites false precision (`ai-feature-acceptance-pitfalls`
   covers the threshold side). If a number is shown, it was calibrated on held-out data; otherwise use coarse
   labels tied to an action ("check before sending").
3. **Citations must open the cited passage.** A link to a whole document sends nobody to the claim;
   `rag-retrieval-quality-pitfalls` §3 covers checking them.
4. **Say when there is no answer.** A refusal, "not found" or "I need more information" is a result with its own
   screen. A guess dressed as an answer is the worst outcome, since nothing flags it.
5. **Match the stakes.** Low-stakes suggestions can be one click to accept; consequential ones (money, deletion,
   messages to third parties, medical or legal content) need a preview and a deliberate step.

## 1.2 Setting expectations
1. **State scope where the feature starts**: what it is for, what it does not do, what it cannot see (the
   documents it has no access to), and that it can be wrong. One line in the empty state, not a legal footer.
2. **The empty state teaches.** Three concrete example requests beat "ask me anything"; blank prompts yield vague
   questions and poor answers that get blamed on the feature.
3. **Do not anthropomorphise past what is useful.** A name and a face suggest judgement and memory the system lacks.
   Disclosure obligations are in `ai-content-disclosure-and-provenance-pitfalls`.
4. **Copy must not outrun the evaluation.** "Always accurate" or "understands your business" are claims the
   acceptance set cannot back; use what was measured.

## 1.3 Checks
1. A user can tell retrieved from generated content from the screen alone.
2. Every consequential action has a preview and a deliberate confirmation.
3. The no-answer path has a designed screen.
4. The scope line is on screen at first use.
