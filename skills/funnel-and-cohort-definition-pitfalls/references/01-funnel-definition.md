# funnel-and-cohort-definition-pitfalls §1 — Funnel definition

A funnel is a claim that users pass through ordered steps. Most disagreements between two funnels are
differences in these definitions, not in the product.

## 1.1 What a step is
1. **Sequential.** A user cannot reach step N without passing through step N minus one (nimrodfisher). Steps
   that can be completed in any order break the funnel assumption.
2. **Counted once.** Each user is counted once per step at a given point in time, so a user who repeats a step
   is not counted twice (source: mutually exclusive and de-duplicated per step).
3. **Complete enough.** No meaningful step is omitted that could explain the drop-off (source: exhaustive within
   scope).
4. **An intentional action, not a page view.** Defining steps by page views inflates the early steps, because a
   page can be loaded with no intent (source). Pick an action the user chose to take.
5. **One counting unit across all steps.** Mixing session-level counts with user-level counts across steps
   produces rates that mean nothing (source).

## 1.2 The denominator
1. **The first step defines the universe.** Every conversion rate is relative to it, so it must be defined
   clearly and be appropriate to the question (source).
2. **Two rates, two questions.** Step-over-step conversion (users at step N over users at step N minus one)
   answers where the biggest drop is. Overall conversion (users at step N over users at step one) is what to
   report to stakeholders on the health of the funnel (source). Say which one a chart shows.

## 1.3 The time window
Pick the type deliberately; the same behaviour gives different numbers under each.
1. **Open-ended**: later steps may be completed at any time. The source says it fits purchases, where users shop
   over days.
2. **Time-bounded**: all steps must be completed within a fixed window, for example seven days. The source says
   it fits onboarding, where a late completion is not a real conversion.
3. **Cohort-based**: group users by start date and follow them over a fixed observation window. The source
   says it is required for a fair comparison between periods.
4. **State the window and apply it to every step** (source checklist). Comparing a funnel with one window to a
   funnel with another is a definition difference, not a change in behaviour.

## 1.4 Split before concluding
1. **Break the funnel by the most relevant segments before drawing conclusions** (source). Its examples:
   acquisition channel (paid traffic may carry lower intent than organic), device type (mobile often drops
   sharply at form steps), new versus returning users (returning users are familiar with the product, and mixing
   them in inflates averages) and plan or price point (paying users convert differently from free ones).
2. **An aggregate can hide the segment that moved.** The mix of segments across the two periods being compared is
   part of the definition (own guidance); see `analysis-validation-pitfalls` for Simpson's paradox.

## 1.5 Prioritising a drop-off
1. **Weigh the drop-off by what flows through it.** The source's impact score is the absolute drop-off times
   the value per user at that step: a 40 percent drop at a step with ten times the traffic matters more than a
   40 percent drop later on.
2. **Recovery value is an upper bound**, not a forecast. The source computes it as users lost at the step times
   the conversion rate of the remaining steps times the revenue per conversion, and it assumes the drop-off
   could be eliminated entirely.
3. **Every drop-off that is acted on has at least one hypothesis and an owner** (source checklist), so the
   chart ends in a decision.
