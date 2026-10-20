---
name: event-operations-pitfalls
description: "Use when a company hosts, sponsors, speaks at or attends an event: a conference chosen because everyone goes, a booth with no meetings booked, badge scans counted as leads, a follow-up sent three weeks late, a venue contract signed with no cancellation terms, a sign-up with no accessibility or consent plan. Event selection and role, before-during-after arc, logistics and vendor checks, follow-up and measurement. Method only; contract terms and insurance are for the owner who signs, not legal advice."
---

# event-operations-pitfalls

Business layer (`business/README.md`), marketing. Most of what an event produces is decided before and after it,
not on the day. This block is the check on an event plan. Choosing and contracting suppliers (venue, caterer,
agency) is `business/vendor-management` §3; the shape of a product launch is `business/b2b-go-to-market-pitfalls`;
registrations that hold personal data are `business/data-protection`; consent and opt-out in follow-up emails are
`business/email-deliverability-and-sender-requirements-pitfalls`; accessible slides and handouts are
`business/accessible-documents-pitfalls`; community meetups as a programme are `business/community-management`.

It states method only. Insurance, liability, venue contracts, local permits and tax on events are decided by the
owner who signs. Not legal advice.

## When
- An event is being chosen, sponsored, hosted or attended, or a speaking slot is offered.
- A plan, budget or supplier contract for an event is reviewed.
- An event is over and its results are reported.

## Steps

**Read only the section the task meets.** §1 when choosing; §2 when planning the run; §3 afterwards.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Selection and role: goal, who must be in the room, host, sponsor, speak or attend, cost per useful conversation, saying no | an event is proposed or compared | [`01-selection-and-role.md`](./references/01-selection-and-role.md) |
| 2 | Plan and logistics: before, during, supplier and venue checks, accessibility, consent, budget and a run sheet | an event is being organised or attended | [`02-plan-and-logistics.md`](./references/02-plan-and-logistics.md) |
| 3 | Follow-up and measurement: tiers, timing, source tagging, results that name conditions, debrief | an event has happened | [`03-follow-up-and-measurement.md`](./references/03-follow-up-and-measurement.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: per event, a one-line goal and its measure, the named
audience and where it will be found, a budget with a cancellation view, a run sheet with owners, a follow-up plan
with tiers, and a debrief with the cost per useful conversation and the decision to repeat or drop.

## Guardrails
- State one primary goal per event and who must be in the room. Never attend because the sector does (§1).
- Judge an event on its own results. Never write off all events on one bad one, or repeat one on habit (§1).
- Book meetings and brief the people on the stand before the day. Never rely on foot traffic (§2).
- Check cancellation, deposits, insurance and dates before signing. Never sign a supplier contract on price alone
  (§2).
- Plan accessibility, consent and data handling for sign-ups. Never collect badge or registration data with no
  stated use (§2).
- Record the context of each conversation, not only the contact. Never log a lead with no note of what was said
  (§3).
- Follow up within days with what was discussed. Never send the same message to everyone scanned (§3).
- Report the cost per useful conversation and what is not measured. Never count scans or attendance as results
  (§3).
- This block is partly built from an MIT source and partly from general practice, and never run by us on a real
  event. Status and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Rewritten in our own words from the event-marketing notes of an MIT marketing skills repository (read
2026-10-20), plus general event-operations practice. 🟡: never run by us. Details in
[`references/origin.md`](./references/origin.md).
