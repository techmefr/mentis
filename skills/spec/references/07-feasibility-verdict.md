# spec §7 — The feasibility verdict

> Section 7 of `skills/spec`. Read it when the request has a real chance of being impossible, too costly or
> blocked by something outside the team's hands, before effort goes into a plan.

1. **State a verdict at the end of the spec, one of three**: `GO` (nothing found stands in the way), `CONDITIONAL`
   (feasible if named conditions hold), `NO-GO` (not feasible as asked, with the reason). A spec that ends without
   one has left the question to whoever discovers the answer during the build.
2. **A `CONDITIONAL` lists its conditions as checkable facts**: a dependency delivered by a date, a permission
   granted, a measurement under a limit, a decision by a named owner. Each has an owner and a way to find out.
3. **A `NO-GO` is a result, not a failure.** It states what was tried or read, what blocks, and the nearest thing
   that is feasible. It saves the build that would have found the same wall at a higher price.
4. **Base it on what you looked at**: the interfaces that actually exist, the limits of the platform or the
   vendor read from its documentation, a spike if the question is empirical (`skills/brainstorm` step 0). A
   verdict from intuition is labelled as one.
5. **Do not turn doubt into a silent assumption.** If feasibility depends on something you could not check, the
   verdict is `CONDITIONAL` with that as the condition, not a `GO` with the doubt left out.
