# gate §11 — Two independent evaluators

> Section 11 of `skills/gate`. Read it only for a change that ships without a human reading it, or whose failure
> is expensive and hard to reverse (a production deploy, a public publication, a compliance-bound text, a
> migration of live data). It doubles the cost of step 3, so it is opt-in and the operator chooses it.

1. **The idea.** One evaluator shares the blind spots of the process that produced the work if it is the same
   model reading it the same way. Two evaluators with no shared context, applying the same rubric, are unlikely to
   miss the same thing, and the work ships only when both pass.
2. **Write the rubric first, and make every item decidable.** Each criterion is a pass or a fail with a severity,
   and each is answered by evidence in the artefact. A rubric of adjectives ("clean", "good") gives two evaluators
   two different standards.
3. **Brief each evaluator alone.** The same rubric and the same artefact, nothing else: not the producer's
   reasoning, not the other evaluator's output, not the conversation. Contexts that overlap defeat the purpose.
   Where it is affordable, use different models or different tools for the two seats.
4. **Both must pass.** One pass and one fail is a fail. There is no averaging and no tiebreak by the producer.
5. **Collect every flag from both, fix them all, then re-run both.** Fixing only the flags of the evaluator that
   failed lets the other's concern ride into the next round unaddressed. A flag you disagree with is answered
   with evidence in the next round, not deleted.
6. **Cap the loop and name the cap.** Three rounds is a usual bound. When both evaluators still do not pass at
   the cap, stop and hand the artefact, both verdicts and the remaining flags to the operator; a fourth round
   by the same producer is the loop that is not converging.
7. **Deterministic checks run before either seat.** Build, tests and linters go first (§9); an evaluator is
   a reading of what a tool cannot decide, not a replacement for what a tool can.
8. **Report the two verdicts side by side**, per criterion, so that disagreement is visible. Agreement on every
   item is information; disagreement on one item is the most useful line of the report.
9. **Not for**: drafts, exploration, and anything a deterministic pipeline fully verifies. Using two evaluators on
   a typo fix is paying double for the privilege of nothing.
