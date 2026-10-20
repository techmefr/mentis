# project-management-artefact-pitfalls §2 — Estimates and dependencies

> Part 2 of `business/project-management-artefact-pitfalls`. Read it when a date or an effort is given or accepted.

An estimate is a statement about uncertainty. Once it is copied into a plan without its range it turns into a
commitment, and the dependency chain behind it turns one late task into a late project.

## 2.1 Say what the number is
1. **Give a range and the assumptions that bound it.** Symptom: "six weeks" is quoted in a meeting and read as a
   promise. Fix: write "four to nine weeks, assuming the data arrives by the first of the month and one review
   cycle"; the assumptions go into the log (§1.1).
2. **State what is included.** Symptom: the figure covers build and not testing, review, deployment or the
   waiting time between handoffs. Check: list the activities from first touch to done and mark which are in the
   number. Fix: add the missing ones or say they are out.
3. **Separate effort from elapsed time.** Ten days of work can be six calendar weeks once availability, meetings
   and waits are counted. Fix: give both, or state the availability you assumed.
4. **Do not let the person who wants it set it.** Symptom: an estimate that matches the deadline exactly. Fix: the
   people doing the work estimate, the requester sets the priority, and a mismatch is a scope or date decision
   (§3.3), not a negotiation on the estimate.
5. **Use evidence from past work, and label guesses.** Own guidance: compare with a similar finished task and say
   so; where there is nothing to compare with, write "guess" next to the figure. Never quote a benchmark ratio or
   an industry overrun figure you have not re-read; re-read before relying.
6. **Re-estimate when the facts change, and show the old figure.** A silent change of the figure is a silent
   change of the date.

## 2.2 Dependencies
1. **List what you wait for and what waits for you.** Symptom: a milestone slips and a team learns about it from
   a missed handoff. Fix: for each dependency, the supplier, the item, the date needed, the date promised and the
   person who promised it.
2. **A promise from someone who is not the owner of the work is a hope.** Check: did the person doing the work
   agree to the date? Fix: confirm with them or mark the date unconfirmed.
3. **Slip travels downstream.** When an upstream task moves, compute what moves after it, and tell the owners the
   same day. Symptom: the plan still shows the old end date because only the late task was edited.
4. **Find the longest chain.** The tasks that, if late, move the end date are the ones to watch; a late task off
   that chain may be harmless. Fix: mark the chain, and watch float (the slack) on the rest.
5. **Check external dependencies first.** A vendor, a regulator, a customer or another company's release has its
   own calendar. Fix: ask for the date early and put a decision date in the plan for the fallback.
6. **Wait states are tasks.** Approval, procurement and review queues take elapsed time that no one is working
   in; schedule them as activities with an owner.
