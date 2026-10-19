# slo-design §2 — The target, the budget and the policy

> Part 2 of `skills/slo-design`. Read it when a target is set or a budget is spent.
> Source, read 2026-10-19: Google SRE Workbook, "Implementing SLOs"
> (https://sre.google/workbook/implementing-slos/). Sentences marked "own guidance" are ours. No target value
> from any source is carried here; the Workbook's worked figures are examples to be re-read, not defaults.

1. **The target is a product decision, not an engineering constant.** The Workbook says the objective must be
   owned by someone able to trade feature speed against reliability (the technical head in a small
   organisation, usually the product owner in a larger one). Engineers supply what the system sustains; the
   owner decides what is good enough.
2. **Perfect is the wrong target.** The Workbook's reasons: failures that coincide cannot be ruled out, users'
   own dependencies cap what they perceive, each extra step of reliability buys less, and change is the main
   source of outages. Own guidance: a target no one can miss makes every change look forbidden.
3. **Three parties agree before the objective is live.** The product manager confirms users are well served at
   the threshold, the developers agree to lower risk when the budget is spent, and the operating team agrees it
   can be defended without heroics. If one refuses, iterate on the indicator and target until all three accept.
4. **Current performance is a starting point, not a ceiling.** The Workbook allows starting from what the
   service does today and refining later. Own guidance: write down that the first target is provisional and
   when it will be reviewed, rather than defending it as a final truth.
5. **Pick a window on purpose.** A rolling window matches how users remember outages and avoids resets at
   calendar boundaries; a calendar window matches business planning but leaves doubt mid-period. The Workbook
   suggests a whole number of weeks so each window holds the same weekends, and a rolling four-week window as a
   general choice, with shorter views for prioritising and longer ones for planning. Re-read it before reuse.
6. **The error budget is one minus the target, in the SLI's own unit.** For a request ratio it is a count of
   allowed bad requests over the window; one incident spends a share of it. The Workbook notes the budget is
   an approximation of user happiness, since different failure patterns with the same count are treated alike.
7. **Write the policy before the budget burns.** The Workbook lists what it should hold: authors, reviewers and
   approvers, approval and next review dates, a short description of the service, the actions taken when the
   budget is gone, and an escalation path for disagreement about the calculation or the actions.
8. **State what changes when the budget is spent.** The Workbook's usual actions: the team puts the past
   period's reliability bugs first; the team works only on reliability until back within the objective, with
   backing to refuse outside demands; a freeze on changes until enough budget returns. An emergency state with
   high-level approval is the extreme case, ending on stated exit criteria.
9. **Agree in advance what a dependency's failure does to the policy.** When another team's component spent the
   budget, the Workbook describes two views and favours the freeze because it serves users better, while saying
   the policy can be adapted if it is recorded. Own guidance: decide this when the policy is written, not at 3
   a.m. of the incident.
10. **If the policy is not enforced, the objective is wrong.** The Workbook says that when stakeholders will
    not apply the policy, you go back to approval. Without enforcement the objective becomes another indicator on
    a wall instead of a decision tool; it also means a launch asks "how much budget do we have" and not "what
    does it feel like".
11. **Review on a rhythm.** The Workbook suggests frequent reviews when starting (monthly) and less often once
    the practice has matured. A review may tighten, loosen or retire an objective; none of those is a failure.
12. **Keep the internal objective apart from any customer promise.** Own guidance: a contract has different
    readers and penalties, and the internal objective should leave room for action before the promise is at risk.
