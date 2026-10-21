# production-readiness-review §1 — Level and evidence

> Part 1 of `skills/production-readiness-review`. Read it when a review is scoped or a checklist is written.
> Source, read 2026-10-20: mercari/production-readiness-checklist, "Production Readiness Level", "Production
> Readiness Checklist" and "Check Production Readiness" (MIT). Sentences marked "own guidance" are ours.

1. **One bar does not fit everything.** The source defines three levels (critical, standard, experimental) and
   says there is no one-size-fits-all; the items required differ per level. Symptom: a checklist so heavy that
   teams skip it, or so light that a payment path passes it. Fix: scale the required items to the level.
2. **Derive the level from the service objective.** The source ties the level to the expected objective, and
   says the objective has to be defined before the level can be chosen. Check: no level without a written
   target from `skills/slo-design` §2; if none exists, writing it is the first task.
3. **Place a service in the top level for what failure costs, not for its size.** The source puts services that
   handle personal data, contribute directly to company goals or could cause significant damage when down in the
   top level, and experimental or small-audience features in the bottom one. Own guidance: add legal exposure
   and the effect on other services that depend on it.
4. **When unsure, start in the middle and move up on evidence.** The source advises starting at the standard
   level and improving toward the critical one if needed. Own guidance: write the reason for any later move so
   the level is not just drifting.
5. **Ask for the evidence, not the claim.** The source's process has the owning team verify each item and
   provide evidence such as tickets, screenshots, documents or test results, and says the review takes much
   longer without it. Rule: a check is passed when someone else can open the evidence and see it.
6. **Make "not applicable" a written decision.** The source has the team tick the item and explain why it does
   not apply, as the evidence. Symptom: an item missing from the record. Fix: keep every row, with the reason.
7. **Say what a pass means.** Own guidance: ready means the team can operate and recover the service with the
   people and tools it has, at the stated level; it is not a promise of no incidents. Write the sentence into the
   record so no one reads it as a guarantee.
8. **Keep the checklist short enough to be read.** Own guidance: every item must change a decision or prevent a
   named failure; an item nobody has ever failed or acted on is a candidate for removal. Review the list after
   each incident for the item that was missing.
9. **Date the evidence.** Own guidance: a screenshot of a green dashboard from the design phase proves nothing
   about the build released; require the evidence to come from the version going live, and the design
   documents to match the implementation.
10. **Separate what is required to launch from what is required soon after.** The source marks items not yet
    enforced but planned for the future. Own guidance: use the same device for items you accept late, with a date
    and an owner, rather than blocking launch on everything or forgetting the rest.
11. **A deploy command that exits 0 is not evidence that the change is live.** Source, read 2026-10-20: the
    deploy-with-verification agent of the operating-kit plugin of wshobson/agents (MIT, root licence). The check that
    counts is a request to the running service, the one users reach, that shows the new revision. It catches a
    platform that reports success while still serving the previous revision, a staged rollout that routes only
    part of the traffic to the new build, and an image that starts and then crashes on its first real request.
    Own guidance: record the endpoint and its answer as the evidence, and update the state of record only after it,
    never before.
