---
name: event-tracking-plan-pitfalls
description: "Use when an analytics event plan or tracking spec is designed, reviewed or verified before it ships: the questions the data must answer, unique event names, not redefining auto-collected events such as page view and scroll, naming and length limits, locale-aware and subdomain-aware page scopes, text selectors that are discovery hints and not final triggers, precise trigger definitions (a click is not a successful submit), typed properties, never auto-picking the account, container or workspace, preview no-hit versus a broken configuration, a verification gate before publish, personal data handling, the QA checklist, and traces of model inputs and outputs."
---

# event-tracking-plan-pitfalls

Not a step of the pipeline: a craft block for the plan that decides which user actions become analytics data, from
the first list of events to the check after release. The two sections share one premise: **an event plan is a
contract between the people who read the data and the people who ship the page, so every ambiguity in it (a name
used twice, a trigger that fires on the wrong moment, a selector that matches too much, a property whose type
nobody wrote down) becomes a wrong number later that nobody can trace**. The definition of the funnels and cohorts
built on these events is in `funnel-and-cohort-definition-pitfalls`; checking a number already computed is in
`analysis-validation-pitfalls`. The source tool is specific to one tag manager and one analytics product; items
that hold only there are marked as vendor items.

## When
- Writing or reviewing the list of events, properties and triggers for a feature or a whole site.
- A plan reuses a name, redefines something the analytics product already collects, or relies on a text match
  to find a button.
- A preview shows an event that "did not fire" and someone wants to rewrite the configuration.
- Anything the model sees or produces (prompts, retrieved text, tool calls, outputs) is about to be captured.

## Steps

**Read only the section the task meets.** They are independent.

| Ref | Covers | Read it when | File |
|---|---|---|---|
| 01 | The plan itself: goals first, unique and valid names, auto-collected events, page scopes, selectors, trigger precision, typed properties | a plan is being written or reviewed | [`01-names-scopes-and-triggers.md`](./references/01-names-scopes-and-triggers.md) |
| 02 | Approval, verification and privacy: no automatic choices, the approval and publish gates, reading a failed preview, the QA checklist, personal data, model traces | a plan is about to be approved, verified, published or to capture sensitive data | [`02-verification-and-privacy.md`](./references/02-verification-and-privacy.md) |

## Output / checkpoint
A plan is done when a reader who was not in the discussion can say, for every event, which question it answers,
the exact moment it fires, the type and an example of each property, which properties are personal data and what
is done about them, and how QA will see it fire once and only once. A verification is done when each missed
event is classified (selector problem, runtime problem or preview limitation) before anything is rewritten, and
when nothing was selected or published on the reader's behalf. Read the plan once looking for a name that
appears twice, a selector that depends on visible text, and a trigger worded as a click when the analysis needs
the outcome. Nothing here was verified on a live site: the check is a read of the text.

## Guardrails
- Never let two events share a name; merge them or rename them to their distinct intent (reference 01).
- Never redefine an event the analytics product already collects automatically (reference 01).
- Never approve a selector that works only through visible text; text is a hint to find the element, not the
  trigger (reference 01).
- Never word a trigger loosely: "when the button is clicked" and "when the form is submitted successfully" are
  different events (reference 01).
- Never pick an account, a container or a workspace on the person's behalf because one looks right; show the
  options and wait for the answer (reference 02).
- Never publish on a missing or blocked verification, and never treat a broad request as approval of the plan
  (reference 02).
- Never read a preview that saw nothing as a broken configuration before the three known false negatives are
  excluded (reference 02).
- Never capture model inputs or outputs without deciding the data classes, minimisation before the data leaves
  the process and before storage, access and read logging, retention, consent and sampling (reference 02).
- The 40 character name limit and the reserved names are the source's statement for one analytics product and
  were not checked against its documentation (reference 01).

## Origin
Rewritten from jtrackingai's analytics-tracking-automation (Apache-2.0), the skills `tracking-schema`,
`tracking-verify` and `tracking-discover` and its references, and from product-on-purpose's pm-skills, the
`measure-instrumentation-spec` skill (Apache-2.0), read 2026-10-16. Young 2026 repositories, one author's
practice and not consensus. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
