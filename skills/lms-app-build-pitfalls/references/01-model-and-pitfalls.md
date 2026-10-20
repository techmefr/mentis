# lms-app-build-pitfalls §1 — Minimal model and its pitfalls

> Part 1 of `skills/lms-app-build-pitfalls`. Read it when a schema or a write path is designed. Mostly craft knowledge;
> points 3, 5 and 6 carry facts from the xAPI specification (Apache-2.0), read 2026-10-20 and restated in our words (`references/origin.md`, source 1). Everything not marked as sourced is our own guidance. Each point gives the symptom, the check and the fix.

1. **A published course is versioned, never edited in place.** Symptom: an instructor fixes a typo, removes a
   lesson and adds two, and learners who had finished see their progress drop or a finished course reopen.
   Check: publish, enrol a learner, finish half, then edit. Fix: separate the course (stable identity) from the
   course version (immutable once published); an enrolment points at the version it started on. State the
   policy per change: typo fixes may apply to everyone, structural changes apply to new enrolments only, and a
   forced migration of in-progress learners is an explicit action that maps old lessons to new ones and keeps
   the old results.
2. **Minimal model, each entity with one owner.** Course, course version, module, lesson (with a type: text,
   video, file, quiz, assignment), enrolment (learner and version, with a status and dates), progress event,
   attempt (for a quiz or assignment), certificate, cohort (a group with start and end), user, role. Give each
   record an owner and a creator. Symptom of skipping the enrolment record: access is checked by a flag on the
   user and nobody can say what a learner was entitled to last spring.
3. **Progress is events, state is derived.** Symptom: a counter overwritten by two tabs, a video resumed at
   zero, a percentage that cannot be explained. Fix: insert an event per meaningful action (lesson opened,
   lesson completed, quiz submitted) with learner, version, lesson and time; derive the percentage and the
   state from events by one query; keep a cached summary only as a rebuildable projection. Store a resume
   position separately, since it is a convenience and may be lost. The xAPI specification is built on the same idea: a learning record is an immutable statement of who did what to which activity, with a result and an optional registration that may stand for an attempt, a session or several activities, not necessarily ended by completing an activity (source 1). It also separates the time the experience occurred from the time the record was stored, because records can arrive late, so derive progress by event time, not by arrival order.
4. **Completion is a written rule with one owner.** Symptom: the dashboard says 100 percent, the certificate
   page says not yet, the export says something else. Fix: write the rule as a sentence per course (every
   required lesson completed and every required quiz passed, optional lessons ignored), implement it in one
   function used by the screen, the certificate trigger, the reminder job and the export, and test it with a
   table of cases including a lesson removed in a later version. Decide whether a lesson counts when it is
   merely opened or only when an end condition is met.
5. **Attempts are rows with a policy.** Symptom: a retake overwrites the first score, or a learner opens the
   quiz in two tabs and gets two passes. Check: submit twice, quickly. Fix: an attempt row with start, submit
   time, answers, score, and the version of the quiz; a policy for the maximum number, which attempt counts
   (best, last, first), a time limit enforced on the server clock, and an idempotency key on submit. The specification applies the same rule to its own records: a statement carries an id, and a second write with an id already stored must not modify the stored statement, and the server should compare the two and answer a conflict when they differ (source 1). Keep
   questions versioned like lessons so an old attempt stays gradable and explainable.
6. **Grading is separate from delivery.** Automatic scoring for closed questions; a manual queue for
   assignments with a grader, a rubric, a status (submitted, graded, returned) and a recorded grade history.
   Symptom: a regrade changes a certificate already issued. Fix: a regrade is a new grade row and triggers the
   certificate rule again, with the outcome recorded, never a silent edit. The specification handles an invalid record the same way: statements cannot be changed or deleted, and a later statement voids an earlier one, a voiding statement cannot itself be voided, and restoring a voided statement means issuing a new statement (source 1).
7. **A certificate is a record with an identifier and a state.** Symptom: a PDF that anyone can edit and no way
   to confirm it is genuine, or a revoked learner whose certificate still looks valid. Fix: store the
   certificate as a row (learner, course version, issue date, optional expiry, a random unguessable
   identifier, status issued or revoked with a reason); the file is rendered from the row; a public check page
   shows only name, course and validity for a given identifier and nothing else. Expiry and renewal are
   states, not date edits.
8. **Cohorts and deadlines carry a zone.** Symptom: a deadline set for the end of the day closes the previous
   evening for learners abroad, or moves by an hour after a clock change. Fix: store instants in UTC plus the
   zone that the deadline is meant in, show the learner's local time and the zone name, and decide whether a
   late submission is blocked, flagged or accepted with a penalty. A cohort is a first-class group with its
   own dates and its own copy of the schedule, not a tag on enrolments. See `skills/locale-value-formatting-pitfalls`.
9. **Archive, never cascade.** Symptom: deleting a retired course erases certificates and results that someone
   will need later. Fix: archive the course and its versions, keep enrolments, attempts and certificates, hide
   the course from the catalogue, and handle a learner's erasure request as a documented anonymisation of the
   personal fields while the aggregate results remain (see `skills/laravel-no-cascade-delete`).
10. **Reminders and drip release are jobs with state.** Symptom: a learner gets the same nudge every night, or
    a lesson unlocks for the wrong cohort. Fix: a scheduled job that selects by rule and writes a sent-record
    per learner and rule, so it is idempotent; unlock by date or prerequisite computed from the cohort, not
    from the server's day. See `skills/queue-worker-runtime-pitfalls`.
