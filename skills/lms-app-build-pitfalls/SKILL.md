---
name: lms-app-build-pitfalls
description: "Use when a learning management or e-learning application is designed or built: the minimal model of course, module, lesson, enrolment, progress, attempt, certificate and cohort, content versioning so a published course can change under learners who are mid-way, completion rules defined once, progress as events rather than a counter, assessment attempts and grading, certificates that can be verified and revoked, cohorts and deadlines in time zones, instructor and learner visibility, and what gets regretted at v2. Method only; learner-data and records duties are not legal advice."
---

# lms-app-build-pitfalls

A defensive block for building the application, not for designing a good course. An LMS built in a hurry fails
in familiar ways: an instructor edits a lesson and the learners who finished it are silently back at 60 percent,
"completed" means video watched in one place and quiz passed in another, a certificate cannot be proven or
withdrawn, a cohort deadline lands a day early for half the group, and every learner can see the others' grades.
The content is craft knowledge with no external source read (see `references/origin.md`). Writing objectives
and checking learning are in `skills/training-objectives-and-formative-assessment-pitfalls` and
`business/learning-development`; file storage is in `skills/document-file-management-pitfalls`; upload screens in
`skills/file-upload-ui-pitfalls`; roles in `skills/laravel-permissions-not-roles`; tenants in
`skills/laravel-tenant-context-by-default`; personal data duties in `business/data-protection`.

## When
- A new LMS, course platform, onboarding academy or training tracker is specified or its schema is drafted.
- An internal tool grows courses, quizzes, certificates, cohorts or a completion dashboard.
- A feature touches editing published content, progress, grading, certificates or deadlines.

## Steps

**Read the part you need before the schema or the migration is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Minimal model and its pitfalls: content versions, progress events, completion rule, attempts, certificates, cohorts and time | a schema or a write path is designed | [`01-model-and-pitfalls.md`](./references/01-model-and-pitfalls.md) |
| 2 | Roles and visibility, integrations and standards, imports and exports, what to split first, v2 regrets, framework pointers | permissions, an integration or the first release are planned | [`02-roles-integrations-and-v2.md`](./references/02-roles-integrations-and-v2.md) |

## Output / checkpoint
Before building: the entity list with a key and an owner for each, the completion rule per course written as a
sentence, the version policy (what an edit does to learners already in progress), the certificate validity and
revocation rule, the cohort and deadline time-zone rule, and the visibility matrix by role. Evidence is a test
that editing a published lesson leaves an in-progress learner's progress intact, a test that completion is
derived by one function from the stored events, and a test that a learner cannot read another learner's result
through the list, the export and the certificate page. Nothing here was run by us.

## Guardrails
- This block is not legal advice. Retention of learner records, accessibility duties, and the standing of a
  certificate depend on the jurisdiction and the use; ask the data-protection owner.
- Never edit a published lesson in place: create a new version and decide explicitly what happens to learners
  in progress (§1, point 1).
- Never store progress as one overwritten number: store events and derive the state (§1, point 3).
- Never compute completion in two places: one function owns the rule (§1, point 4).
- Never issue a certificate without a verifiable identifier and a revocation state (§1, point 7).
- Never store a deadline as a local wall-clock string without its zone (§1, point 8).
- Never filter visibility in the screen only: enforce it in the query, the export and the certificate page
  (§2, point 1).
- Never cascade a delete from a course to learners' records (§1, point 9).

## Origin
Written from craft knowledge of building learning platforms; no open-source LMS documentation was read, so no
source is credited and no text was taken. See [`references/origin.md`](./references/origin.md). 🟡: never run
by us.
