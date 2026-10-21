---
name: onboarding-and-empty-state-pitfalls
description: "Use when a first-run experience or an empty state is designed, written or reviewed in a business application, whatever the framework: first-run routing, setup checklists and progress that persists across devices, skip and resume, tours and tooltips, sample data that must be clearly removable, empty, filtered-empty and error-empty states, plus accessibility, performance and the tests that catch them."
---

# onboarding-and-empty-state-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the first ten minutes of a new account and the screens that have nothing
to show yet. The premise: **onboarding is state, not decoration, and an empty state is a fork in the road, not a
blank**: a checklist that resets on another device, a tour that fires again after every release, sample data that
leaks into real reports, an empty table that is really a failed request, a "skip" that cannot be undone. Multi-step
forms and wizards (validation, drafts) are in `long-and-multistep-form-pitfalls`; list and table states follow
`data-table-ui-pitfalls`; saved preferences and per-user storage are in `settings-and-preferences-page-pitfalls`;
the inbox side of nudges is in `in-app-notifications-pitfalls`; usability replay of a journey is `persona-ux-audit`;
widget accessibility is in `accessibility`.

## When
- A signup, invitation-accept, first-login, setup checklist, product tour or sample-data feature is built or changed.
- A page has no data yet, or filters return nothing, and its empty state is written.
- A user reports "it asks me again", "I cannot get the checklist back", "demo data is in my numbers", "the page is just blank".

**Skip when** a part does not exist in the project: no checklist (§1.2), no sample data (§1.6), no tour (§1.5), no invitations (§1.7), no analytics (§2.5). Say "not applicable: none exists" in one line per part rather than spend effort confirming absence or inventing a finding. The empty-state rules (§2.1) apply to any screen that lists data.

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | First-run routing, checklist model, progress persistence, skip and resume, invitations, tours, sample data | the onboarding flow, its state or its data is written | [`01-flow-progress-sample-data.md`](./references/01-flow-progress-sample-data.md) |
| 2 | Empty states, accessibility, performance, measurement, tests, framework pointers | an empty state, the UI of the flow or its tests are written | [`02-empty-states-access-tests.md`](./references/02-empty-states-access-tests.md) |

## Output / checkpoint
A change is done when: first-run of an account is decided from stored state, not a client flag (pre-account intro screens may use a local flag, §1.1.8); each checklist step is derived from
real data or stored once per user with an explicit rule; progress survives devices and reloads; every step can be
skipped and resumed; sample data is flagged, excluded from real totals and removable in one action; each empty state
names its cause and offers one next action; and the tests in §2.6 exist. No checkpoint is written: a craft block, 🟡,
nothing here was run in an application.

## Guardrails
- Decide first-run from server state and re-check on every entry once an account exists (§1.1). Never trust a local flag alone for state that belongs to a signed-in user; the one exception is a screen shown before any account exists (§1.1.8).
- Derive a checklist step from the data it describes where possible (§1.2). Never let a step stay ticked after the data was deleted.
- Make skip a first-class, reversible action (§1.4). Never trap the user in a flow with no way out or back.
- Flag sample data on the record and keep it out of real aggregates (§1.6). Never mix it with real rows without a marker.
- Separate empty, filtered-empty, loading and error (§2.1). Never show "nothing here" for a failed request.
- Facts about a library are for the date stamped in `references/origin.md`; re-read before relying.

## Origin
Own craft knowledge, with the accessibility points of §2.3 and one storage fact of §1.1 checked on 2026-10-20 against the W3C ARIA Authoring Practices modal dialog pattern, WCAG 2.2 and the HTML Standard (facts only, credited). Every other point stays unsourced. Details in
[`references/origin.md`](./references/origin.md).
