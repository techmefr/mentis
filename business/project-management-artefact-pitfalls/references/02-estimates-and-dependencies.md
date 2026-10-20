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
   people doing the work estimate (the GAO guide names the activity owners and the most experienced team members as
   the best source, and asks owners to be able to explain the logic of their figures), the requester sets the priority, and a mismatch is a scope or date decision
   (§3.3), not a negotiation on the estimate.
5. **Use evidence from past work, and label guesses.** Own guidance: compare with a similar finished task and say
   so; where there is nothing to compare with, write "guess" next to the figure. Never quote a benchmark ratio or
   an industry overrun figure you have not re-read; re-read before relying.
6. **Re-estimate when the facts change, and show the old figure.** A silent change of the figure is a silent
   change of the date.
7. **A date with no uncertainty data conveys false accuracy.** The GAO guide describes a schedule risk analysis that
   feeds three-point durations or risk drivers into a statistical simulation to give a confidence level for the
   finish date, the time reserve needed for a chosen confidence, and the highest-priority risks. Symptom: a single end
   date asked to carry a promise. Fix: for a project that matters, ask for the range with its confidence, or at least
   a low, likely and high duration for the long activities. The formal analysis is heavy; the range is the minimum.
   Source: GAO Schedule Assessment Guide, practice 8.

## 2.2 Dependencies
1. **List what you wait for and what waits for you.** Symptom: a milestone slips and a team learns about it from
   a missed handoff. Fix: for each dependency, the supplier, the item, the date needed, the date promised and the
   person who promised it.
2. **A promise from someone who is not the owner of the work is a hope.** Check: did the person doing the work
   agree to the date? Fix: confirm with them or mark the date unconfirmed.
3. **Slip travels downstream.** When an upstream task moves, compute what moves after it, and tell the owners the
   same day. Symptom: the plan still shows the old end date because only the late task was edited.
4. **Find the longest chain.** The tasks that, if late, move the end date are the ones to watch; a late task off
   that chain may be harmless. Fix: mark the chain, and watch float (the slack) on the rest. The GAO guide defines the
   critical path as the longest path, calls tasks with float close to it near-critical because a small delay makes
   them critical, and says float is shared along a sequence of tasks, so it is not a private reserve and is not
   contingency. Nonworking periods in a calendar are not float either.
5. **Check external dependencies first.** A vendor, a regulator, a customer or another company's release has its
   own calendar. Fix: ask for the date early and put a decision date in the plan for the fallback.
6. **Wait states are tasks.** Approval, procurement and review queues take elapsed time that no one is working
   in; schedule them as activities with an owner.
7. **A task with no predecessor or no successor is a plan error.** Symptom: an activity can slip without moving
   anything because nothing is linked to its finish, so the end date looks safe. Check: list tasks with a missing
   predecessor or successor. Fix: link each to what it feeds, or mark it deliberately as a start or an end.
   The GAO guide calls this dangling logic and asks for it to be corrected. Source: GAO guide, practice 2.
8. **Very high float and hard date constraints are warnings.** The GAO guide says unreasonably high float suggests
   missing or invalid logic; a hard date constraint fixes a task and makes it critical regardless of the logic, and
   should be absent from the baseline and from official status updates unless justified by an outside event
   written down; lags should be few and justified. Check: count constraints and lags, and review the highest float.
   Source: GAO guide, practices 2 and 7.
