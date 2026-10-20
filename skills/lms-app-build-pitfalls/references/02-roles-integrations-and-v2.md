# lms-app-build-pitfalls §2 — Roles, integrations and v2

> Part 2 of `skills/lms-app-build-pitfalls`. Read it when permissions, an integration or the first release are
> planned. Mostly craft knowledge; point 3 carries facts from the xAPI specification in `references/origin.md` (source 1), read 2026-10-20. Everything not marked as sourced is our own guidance.

1. **Visibility is a rule on the query, by role.** Typical shape: an admin sees all, an instructor sees their
   courses and learners, a manager sees their team's progress but not free-text answers, a learner sees their
   own record. Symptom: the list hides results but the export, the leaderboard, the certificate page and the
   notification still expose them. Check: log in as a learner and compare counts and fields across list,
   export and public pages. Fix: one scoping function used by every read path, permissions named as abilities
   (view-progress, grade, export, issue-certificate, revoke) rather than role names (see
   `skills/laravel-permissions-not-roles`), and a test per ability and per path. A leaderboard is opt-in.
2. **Enrolment sources are explicit.** Self-enrol, manager assignment, cohort import, rule by group, payment.
   Symptom: removing a learner from a group leaves access, or an unenrol deletes results. Fix: an enrolment
   records its source; revoking the source suspends access and keeps the history.
3. **Standards are a decision, not a default.** Packaged content (SCORM, xAPI, cmi5) and learning-tool
   launch protocols bring player quirks, a runtime to host and a reporting format. Decide whether the product
   plays third-party packages at all; if yes, isolate the player in a sandboxed frame, store the raw statements
   it sends, and map them to your own events rather than letting them become your model. The xAPI specification was read for the points above (§1 points 3, 5 and 6: statements are immutable, voided by a later statement, and keep their own ids); SCORM, cmi5 and learning-tool launch protocols were not read, so re-read those specs before relying.
4. **Video and files are served through the platform.** Use storage with signed, expiring links and a
   transcoding step you do not block the request on (see `skills/document-file-management-pitfalls`,
   `skills/file-upload-ui-pitfalls`). Symptom: a course video reachable by a copied link after the learner is
   unenrolled. Check: open a link after revoking access.
5. **Imports and exports are staged and idempotent.** Learners and enrolments arrive by file or directory sync:
   key on an external id, show counts of create, update, skip and conflict before commit, store the import id
   on each row for undo. Exports of results carry the same visibility as the list and neutralise cells that
   start with a formula character (see `skills/csv-xlsx-import-export-pitfalls`).
6. **Accessibility and language are model concerns.** Captions and transcripts as attached assets on a lesson,
   a language per course version, not a column of translated strings on the lesson; a learner can resume in a
   screen-reader flow. See `skills/i18n-catalog-workflow-pitfalls`.
7. **Reports read a defined, dated number.** A completion rate names the version set, the enrolment statuses
   counted, whether dropped learners are in the denominator and the date field. Symptom: two screens disagree.
   Fix: one query per metric reused by screen and export; see `skills/reporting-analytics-app-build-pitfalls`.
8. **What to split first.** Course, version and lesson with publish; enrolment and progress events with the
   completion function; quizzes and attempts; certificates; cohorts and deadlines; reminders; then packaged
   content and integrations. Ship the first three before any integration.
9. **What is regretted at v2.** Courses edited in place; progress as a counter; completion computed in several
   screens; no enrolment record; certificates as loose files; naive local-time deadlines; roles checked by
   name in views; hard-deleted courses; no tenant column; no import undo. Each is cheap at the first migration
   and expensive after learners have history.
10. **Laravel and Nuxt pointers, short.** In Laravel: an immutable version table with a published-at guard, an
    action class for completion, a unique key on idempotent submit, policies for abilities, a scheduled command
    with a sent-record table for reminders, signed storage URLs. In Nuxt: keep the course outline and resume
    point from the API, never compute completion in the client, and render times from UTC with the zone shown.
