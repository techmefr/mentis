---
name: long-and-multistep-form-pitfalls
description: "Use when a long or multi-step form is built or reviewed in a business application (create or edit screens with many fields, wizards, onboarding, back-office records): when to validate (blur, change, submit, per step), how to map server errors to fields and steps, how to save drafts and warn about unsaved changes, what the dirty state really compares, how to keep two editors from overwriting each other (version token, conditional update, conflict screen), and the accessibility of errors and step changes. Framework-independent."
---

# long-and-multistep-form-pitfalls

A defensive block for forms a person spends minutes in, where losing the content, overwriting a colleague's
edit or showing an error on a hidden step costs real work. Premise: **the form is a conversation with a server
that can refuse, change its mind or be written to by someone else meanwhile; every piece of state the person
typed has to survive each of those**. Short single-purpose forms and their basic labelling are in
`skills/accessibility` (reference 04) and the generic review defects (duplicate submission, optimistic updates) in
`skills/frontend-ux-antipattern-review-pitfalls`; names, phones, addresses and dates as input are in
`skills/international-input-pitfalls`; layout and microinteractions are in `business/interface-design`;
tables and filters belong to the data-table blocks, not here.

## When
- A form has more than about ten fields, several steps, or conditional sections.
- A save can fail on the server for a reason the client did not check, or two people can edit the same record.
- A person reports a lost entry, an error they cannot find, or "someone else's change disappeared".
- A wizard is built, or a long form is split into steps after the fact.

**Skip when** the form is short and single-purpose (a handful of fields, one request, nothing to lose): then only §1.1 and §1.3.5 to §1.3.7 matter, and the draft, dirty-state, step and conflict parts are "not applicable: short single-request form". Say so rather than invent a finding.

## Steps

**Read only the section the task meets.** §3 is the entry point for any "my data disappeared" report.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Validation timing, per-step validation, server errors mapped to fields and steps, submit behaviour | rules or error display are designed or reviewed | [`01-validation-and-server-errors.md`](./references/01-validation-and-server-errors.md) |
| 2 | Draft saving, dirty state, leaving the page, step navigation and resume | content could be lost by navigation, crash, timeout or expiry | [`02-drafts-dirty-state-and-steps.md`](./references/02-drafts-dirty-state-and-steps.md) |
| 3 | Concurrency (version token, conditional update, conflict screen) and accessibility of errors and steps | a record can be edited by several people, or errors and steps are announced | [`03-concurrency-and-accessibility.md`](./references/03-concurrency-and-accessibility.md) |

## Output / checkpoint
No pipeline checkpoint. A reviewed form is done when the review states, in one line each: for every rule
class, when it is validated and where its error appears (§1); for every server error shape found in the code,
which field or step shows it, or that none does (§1); how many requests a submit makes and what exists after
each one fails (§1.3.8); what is persisted as a draft, where, and what discards it (§2); the version token the
edit form carries and the answer on mismatch, or "no shared editing" (§3); and whether a keyboard and
screen-reader pass was run or only read from code. A line that cannot be filled is reported as unverified, not
guessed.

## Guardrails
- Validate again on the server for every rule the client checks, and show the server's answer next to the field.
  Never treat client validation as the only gate (§1).
- Show an error after the person leaves the field or submits, not while they are still typing it. Never flag a
  half-typed value (§1).
- Map every server error to a field or a step, and keep a form-level message for the ones that map to none.
  Never swallow an error the person cannot see (§1).
- Compare the form to its last saved or loaded values to decide it is dirty. Never set dirty on any event alone
  (§2).
- Keep what was typed when a save fails or the session expires. Never clear the form on an error response (§2).
- Send the version the person loaded and handle the refusal with a screen that shows both versions. Never let the
  last writer silently win on a shared record (§3).
- Move focus to the first error or the new step heading and announce it. Never leave focus on a button that
  disappeared (§3).
- Points marked with a source in the references were checked on 2026-10-20 against standards and one design-system page (facts only);
  the rest is own craft, listed in [`references/origin.md`](./references/origin.md). No framework behaviour was run.

## Origin
Written from general practice in business-application forms; the problem-details, conditional-request, precondition-required, WCAG and
autofill facts, and the error-summary pattern, were re-read on 2026-10-20 (facts only, own words); no text was copied. 🟡: never run by us. Details in
[`references/origin.md`](./references/origin.md).
