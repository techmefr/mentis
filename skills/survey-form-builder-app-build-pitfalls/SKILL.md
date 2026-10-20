---
name: survey-form-builder-app-build-pitfalls
description: "Use when a survey, questionnaire or form-builder application is designed or built: the minimal model of form, version, question, logic rule, submission and answer, schema versioning so edits never corrupt collected responses, conditional logic as data with cycle and orphan checks, response storage that survives question changes, partial and resumed responses, anonymity versus pseudonymity and small-group disclosure, spam and duplicate control, exports and analysis, and what gets regretted at v2. Method only; consent and privacy law is not legal advice."
---

# survey-form-builder-app-build-pitfalls

A defensive block for building the tool that lets other people make forms, not for writing good questions or for
building one form screen. A builder made in a hurry fails in familiar ways: someone renames a question after 400
answers and the export columns shift, a logic rule points at a question that was deleted, "anonymous" results
identify a respondent in a group of three, a respondent who reloads loses everything, and a bot fills the form
a thousand times. The content is mostly craft knowledge; some points are checked against the SurveyJS form library documentation (see `references/origin.md`).
Wording and sampling of a survey are in `business/customer-interview-synthesis-pitfalls` and
`business/learning-development`; a single long form screen is in `skills/long-and-multistep-form-pitfalls`;
file questions in `skills/file-upload-ui-pitfalls`; exports in `skills/csv-xlsx-import-export-pitfalls`;
personal data duties in `business/data-protection`.

## When
- A survey tool, feedback collector, quiz maker, intake form builder or internal poll feature is specified or
  its schema is drafted.
- An existing app grows custom fields, conditional questions, shareable public forms or response exports.
- A feature touches editing a form that already has responses, branching, anonymity or export.

## Steps

**Read the part you need before the schema or the migration is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Minimal model and its pitfalls: form versions, question identity, logic as data, response storage, partial responses, anonymity | a schema or a write path is designed | [`01-model-and-pitfalls.md`](./references/01-model-and-pitfalls.md) |
| 2 | Public endpoint abuse, roles and visibility, exports and analysis, integrations, what to split first, v2 regrets, framework pointers | a share link, an export, a webhook or the first release are planned | [`02-roles-integrations-and-v2.md`](./references/02-roles-integrations-and-v2.md) |

## Output / checkpoint
Before building: the form schema shape with a stable id per question, the version policy for forms that have
responses, the allowed question types with how each answer is stored, the logic rule grammar with its
validations, the anonymity mode per form written as a sentence, and the minimum group size for any breakdown.
Evidence is a test that renaming and reordering a question leaves old answers attached to it, a test that a
cyclic or dangling logic rule is refused at publish, a test that a respondent can resume, and a test that the
export of an anonymous form carries no identifying column. Nothing here was run by us.

## Guardrails
- This block is not legal advice. Consent wording, retention, special-category questions and the standing of
  "anonymous" depend on the jurisdiction and the use; ask the data-protection owner.
- Never key an answer by the question's label or position: use a stable question id (§1, point 2).
- Never edit the schema of a form that has responses in place: publish a new version (§1, point 1).
- Never accept logic that can loop or point at a missing question: validate at publish (§1, point 4).
- Never promise anonymity you cannot keep: define the mode, and block breakdowns under a minimum group (§1,
  points 7 and 8).
- Never trust the public endpoint: validate the answer against the version's schema on the server (§2, point 1).
- Never write an export cell that starts with a formula character unquoted (§2, point 4).

## Origin
Written from craft knowledge of building form and survey tools, then checked on 2026-10-20 against the SurveyJS
documentation (MIT), credited in the origin file; no text was taken. See [`references/origin.md`](./references/origin.md). 🟡:
never run by us.
