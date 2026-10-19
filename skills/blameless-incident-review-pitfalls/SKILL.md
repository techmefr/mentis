---
name: blameless-incident-review-pitfalls
description: "Use when an incident, degradation or near-miss review (postmortem, incident analysis) is written, reviewed or facilitated: contributing factors instead of a single root cause or human error, the second story, no counterfactual wording, timelines with evidence, precise failure vocabulary, honest customer-facing words (outage versus degradation), action items that are scoped and followed through, and the review process (owner, status, draft review before the meeting, review checklist, meeting agenda)."
---

# blameless-incident-review-pitfalls

Not a step of the pipeline: a craft block for the document written after an incident. The four sections
share one premise: **the review is a learning tool, and each way of writing it that protects a person or
makes the story neat also removes the learning**. Real-time incident communication and roles are not
covered here. For the record format of an architectural decision see `documentation-adr`.

## When
- Writing, reviewing or facilitating the review of an incident, a service degradation or a near-miss.
- A draft says "human error", names one root cause, or says what "would have" prevented the failure.
- A review produced a long list of tickets nobody will do, or the same kind of incident keeps coming back.
- Choosing the owner, the status values, the review timing or the meeting agenda for incident reviews.

## Steps

**Read only the section the task meets.** They are independent, except that §4 uses the vocabulary of §1.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Frame and language: contributing factors, second story, wording, interviews | a draft blames a person or one cause, or the wording is vague | [`01-frame-and-language.md`](./references/01-frame-and-language.md) |
| 2 | Writing the review: timeline and evidence, no counterfactuals, impact, tags | the timeline or description is being written | [`02-writing-the-review.md`](./references/02-writing-the-review.md) |
| 3 | Action items: selection, format, follow-through, sharing | the follow-up list is being written or has stalled | [`03-action-items.md`](./references/03-action-items.md) |
| 4 | Process: owner, status values, timing example, review checklist, meeting | a review process is set up or a draft is checked before the meeting | [`04-process-and-review.md`](./references/04-process-and-review.md) |

## Output / checkpoint
A review is done when someone who was not in the incident can answer from the page alone: what happened and
when (each timeline entry has its evidence), what the customer experienced, which conditions combined, why
the responders' actions made sense to them at the time, and who owns each action and by when. Read it once
searching only for a person's name used as a cause, the words "root cause" and "human error", and a sentence
containing "had" or "would have"; none should survive without a reason. Nothing was verified by running an
incident process: the check is a read of the text.

## Guardrails
- Never write "human error" or one person's action as a cause; ask what about the system made it reasonable (§1.1).
- Never carry a single root cause as the conclusion; sources differ on this and this block takes the
  contributing-factors stance (§1.1).
- Never use "outage" unless service was fully unavailable (§1.2).
- Never mix a hypothetical fix into the timeline or description (§2.2).
- Never change a detail to make the story look better (§2.1).
- Never let a timeline entry stand without the metric, search or message it came from (§2.1).
- Never open a ticket for every idea; every action has an owner, a date and the factor it addresses (§3).
- Deadlines, cadences and severity names in this block are one organisation's choices, shown as examples
  (§4.2); nothing here is an HR, employment or legal rule.

## Origin
Rewritten from PagerDuty's incident response documentation (Apache-2.0) and Adrian Hornsby's operational
excellence incident review template (MIT), read 2026-10-15. The template's attributions of ideas to Allspaw,
Cook, Woods, Dekker, Argyris, Schön and Hollnagel are its author's claims and were not checked here. 🟡:
never run by us; open points are in [`references/origin.md`](./references/origin.md).
