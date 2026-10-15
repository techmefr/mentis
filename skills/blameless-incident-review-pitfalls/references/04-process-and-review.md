# blameless-incident-review-pitfalls §4 — Process and review

How the review is organised: who writes it, in which states it moves, what is checked before the meeting.
Everything with a number in this section is one organisation's choice, shown as an example.

## 4.1 Owner and states
1. **Name one owner.** In PagerDuty's process the incident commander designates the owner at the end of the
   major incident call or very shortly after, and tells that person directly. Adhorn's template also lists a
   peer-review group that verifies the analysis before publication and everyone who took part in the
   response.
2. **What the owner does** (PagerDuty's list): schedule the review meeting and invite the right people,
   investigate and pull in help from other teams, fill in the page, create the follow-up tickets, review the
   content with the right people before the meeting, walk through the topics at the meeting, and send the
   results around.
3. **A status field**, as PagerDuty uses it:

   | Status | Meaning |
   |---|---|
   | Draft | content still being worked on |
   | In Review | content complete, ready for the meeting |
   | Reviewed | meeting over, content reviewed and agreed |
   | Closed | no further action needed on the review, open items live in the tracker |

   PagerDuty adds a step for a customer-facing message (its support team posts it, then closes the review);
   keep it only if you have such a message.
4. **Start early**: adhorn says to begin right after the incident, while details are fresh, and to involve
   everyone who took part.

## 4.2 Timing, as one company's example
1. **Meeting deadline**: PagerDuty schedules the review meeting within 3 calendar days for its most severe
   incidents and within 5 business days for the next level. It also calls the review mandatory for those
   two levels. Your severity levels and deadlines are yours to set.
2. **Schedule the meeting first**, before filling the page, so it is on the calendar (PagerDuty).
3. **Draft first, then the meeting**: PagerDuty posts the link for written review by experienced reviewers
   about 24 hours before the meeting, to avoid wasting meeting time. Start with the timeline.

## 4.3 Review checklist before the meeting
1. **PagerDuty's reviewer questions**:
   1. Does it give enough detail?
   2. Does it drill down to underlying causes rather than only pointing at what went wrong?
   3. Does it separate "what happened" from "how to fix it"?
   4. Do the proposed actions make sense and are they well scoped?
   5. Is it well written and understandable to a newcomer?
   6. Would the customer-facing message resonate or cause outrage?
2. **Adhorn's quality checklist adds**: second stories captured, contributing factors beyond the immediate
   technical cause, a timeline with supporting evidence, what worked well captured, customer impact
   quantified, patterns across incidents considered, owners and realistic dates on every action.
3. **Review the substance, not the typos.** PagerDuty: the point is constructive feedback on valuable
   changes; it still checks that the external message is free of spelling errors.

## 4.4 The meeting
1. **Aim**: PagerDuty runs a short meeting (15 to 30 minutes in its process) as a wrap-up whose goal is to
   find any disagreement about the facts, the analysis or the proposed actions and to spread awareness of
   what is hurting reliability.
2. **Invite** the incident lead, the service owners involved, the key responders, and the engineering and
   product managers of the affected systems; add a customer liaison for the most severe incidents
   (PagerDuty).
3. **Agenda, as PagerDuty's example**:
   1. Recap the timeline until everyone agrees.
   2. Recap the important and unusual points.
   3. How could the problem have been caught (a canary release, tests, a load-test environment)?
   4. Customer impact and any customer comments.
   5. Review the actions, whether they are right and whether more are needed.
4. **Do not skip the review.** PagerDuty's warning: without one, the team cannot see what it does right,
   where to improve, or how to avoid repeating the mistake. The scope (which incidents get one) is the
   team's decision, written down.
