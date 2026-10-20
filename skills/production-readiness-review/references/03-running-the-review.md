# production-readiness-review §3 — Running the review

> Part 3 of `skills/production-readiness-review`. Read it when a review is organised, held or closed.
> Source, read 2026-10-20: mercari/production-readiness-checklist, "Check Production Readiness" and the design
> and pre-production checklists (MIT); the Kubernetes enhancement proposal 1194, "Production Readiness Review
> Process" (Apache-2.0), cited as "the cluster project's process". Sentences marked "own guidance" are ours.

1. **Review in two moments.** The source splits its checklist into a design checklist to meet before
   development starts and a pre-production checklist to meet before deployment, and says the items verified at
   design must still hold at release. Do the same: a short pass at design when changes are cheap, and a full pass
   before launch.
2. **Deploy to production without live users first, when it is safe.** The source recommends deploying to
   production before opening the review, provided no real user is affected, because some checks (capacity
   estimates, dashboards, alerts, profiling) can only be validated there with non-production traffic. Own
   guidance: this needs a way to keep users off; confirm it, and keep data from the test traffic out of real
   reports.
3. **Open a tracked request per service.** The source has the owners open an issue from a template. Own
   guidance: one record per service and release, in the place the team already uses, so history stays together
   and an auditor can find it. (The cluster project's process records, per change and stage, a file naming the
   approving reviewer, next to the change's own metadata.)
4. **Have the owning team verify its own items first.** The source has the team check each item and attach
   evidence before the reviewer looks. Own guidance: the first pass is a rehearsal; if the team cannot show an
   item, they find out before the reviewer does.
5. **Use a reviewer outside the team, from a group that owns reliability.** The source names an architecture or
   site reliability team as reviewer. Own guidance: in a small company a peer from another team or a senior
   engineer outside the project will do; independence matters more than title. The cluster project's process gives
   the reason in its own words: authors and approvers are mostly developers, so operators' views can be missing
   and leave operational gaps; the page does not call its reviewers independent, that word is ours.
6. **Give the reviewer the right to hold the launch.** Own guidance: a review that cannot say no is a ceremony. (In the cluster project's process the right is mechanical: a continuous-integration check and a label are meant to block promotion of a change that lacks the review, and a reviewers-and-approvers file lists who may approve.)
   Say in advance who decides when the reviewer and the owner disagree, and write their decision down.
7. **Review the evidence in order of risk.** Own guidance: start with recovery, security, alerting and rollback;
   a missing item there changes the date, a missing description does not.
8. **Sort every open item into three.** Own guidance: fix before launch; accept with a named risk owner, a date
   and a mitigation; or reject the launch. Nothing stays in a fourth bucket of "later" without a name.
9. **Rehearse before the day.** Own guidance: run a rollback and one runbook in a rehearsal, with the people who
   will be on call. Rehearsal shows what documents hide (`skills/chaos-experiment` §2).
10. **Time the review before the date is promised.** Own guidance: a review requested the day before launch
    gets a rushed yes. Put it on the plan as a milestone with its own lead time, and tell the stakeholders it can
    move the date. (The cluster project ties the review to a deadline: the change's tracking issue must target a release milestone before the enhancement freeze.)
11. **Close with a record, then a trigger.** The source keeps the review on the service's record. Own guidance:
    store the final list, the accepted risks and the reviewer; set a trigger for the next review (a tier change,
    a major dependency or data change, an incident of a certain kind, or a long interval).
12. **Learn from incidents back into the list.** Own guidance: each incident review asks which readiness item
    would have caught it, and adds or sharpens that item; the checklist stays alive by losing items nobody acted
    on and gaining the ones that failed (`skills/blameless-incident-review-pitfalls`).
13. **Do not turn it into a gate that is routed around.** Own guidance: if teams skip the review by calling a
    launch a "pilot", define what a pilot may and may not do (audience, data, duration), and review again when
    it leaves that definition.
