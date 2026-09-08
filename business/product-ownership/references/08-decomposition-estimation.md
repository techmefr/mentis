# § 8 — Decomposition and estimation

> Section 8 of `business/product-ownership`. Read it when a ready story has to be broken into tasks, and
> whenever a number is about to be attached to work.

1. Decompose into tasks that each end in something verifiable, not into phases. "Analysis, development,
   testing" tells you nothing about progress: at the end of the first two you have no working behaviour
   and no way to tell whether the estimate was right. Three tasks that each end in something that works
   report their own progress.
2. **A story is sized to one merge request.** That is the sizing test, and it is mechanical enough to settle
   an argument: if the honest plan needs two branches merged separately, it is two stories, and splitting it
   now costs less than splitting a half-merged one later. What this buys is a review unit that matches the
   story a reviewer read, and a story whose "done" is a single observable event rather than a state spread
   across three MRs nobody can total up. A story that cannot be delivered in one MR because it genuinely
   spans two systems is a dependency (§6.1.4), declared as such, not a big story.
3. **Decomposition, confirmation, then writing — never collapsed.** The plan is the deliverable the person
   who will build it judges; creating the tasks in the tracker is a mechanical consequence of an approved
   plan, not an initiative. Four phases in order: read the story, decompose while asking only the questions
   you actually need, estimate and present the plan, and write it down **only after an explicit go**. A
   tracker filled with tasks nobody approved is worse than an empty one: it looks decided.
4. A task nobody can finish inside a normal working slice is still two tasks. The slice is the unit of
   honest reporting: a task longer than that spends most of its life at "in progress", which is
   indistinguishable from stuck, so nobody asks until it is late.
5. **Estimating without reading the code is a guess with a number on it.** Where the repository isn't
   accessible, say the estimate is unavailable rather than producing a figure that will be held against the
   team. The figure is remembered and the caveat is not — that asymmetry is the whole reason for the rule.
6. State the unit and keep it stable across the backlog; a re-scaled unit invalidates every past comparison.
   Which is the only thing an estimate is actually good for: comparing this work to work already done. A
   unit redefined mid-backlog means the historical data no longer says anything.
7. A bug in work you are currently delivering isn't estimated separately — it's part of that work. A
   pre-existing or third-party bug is estimated like anything else. The line is who introduced it and
   when: absorbing a pre-existing bug into current work hides both the cost of the bug and the cost of
   the feature.
8. **Estimate the whole of what "done" means, not the code.** The migration, the seed data, the
   permission, the documentation, the announcement (§5.7–§5.8) are part of delivery, and an estimate that
   covers only the implementation is short by the amount that surprises everyone at the end of every
   story.
9. **A wide estimate is information; a single number that hides the width is not.** "Two days if the
   export format is what we think, a week if it isn't" is an honest answer and it names the thing to
   check first. Collapsing it to "four days" throws away the useful half and commits to the average of
   two futures.
10. **The person who will do the work estimates it.** An estimate produced by someone else is a target
    with a number on it, and it is defended rather than revised — which is how a plan survives contact
    with reality by getting quieter rather than by getting corrected.
11. **Re-estimate when the plan changes, and say so.** An estimate silently exceeded teaches everyone
    that estimates are theatre; an estimate revised with a reason keeps them useful. The revision is
    cheap on the day it becomes clear and impossible the day before the deadline.
12. **A decomposition is checked against the story, not against the code you plan to write.** Every task
    should trace to a criterion or an explicit part of the scope; a task that traces to nothing is either
    a discovered dependency worth surfacing (§6.11) or work nobody asked for.
