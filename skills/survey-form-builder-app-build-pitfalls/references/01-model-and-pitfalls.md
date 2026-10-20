# survey-form-builder-app-build-pitfalls §1 — Minimal model and its pitfalls

> Part 1 of `skills/survey-form-builder-app-build-pitfalls`. Read it when a schema or a write path is designed.
> Mostly craft knowledge; points 2, 4 and 5 carry facts from the SurveyJS form library documentation (MIT), read 2026-10-20 and restated in our words (`references/origin.md`, source 1). Everything not marked as sourced is our own guidance. Each point gives the symptom, the check and the fix.

1. **A form with responses is versioned, never edited in place.** Symptom: the owner removes a question or
   changes a scale from five to seven points after answers exist, and the old answers become meaningless or
   crash the export. Check: collect answers, edit the form, export. Fix: the form is a stable identity, its
   schema lives in an immutable version row once published or first answered; every submission stores the
   version it was answered against. Allow safe edits (help text, typo) to apply across versions and make
   structural edits create a new version, with a visible warning that results will be split by version.
2. **A question has a stable id, separate from label and position.** Symptom: renaming "Team" to "Squad"
   splits one column in two, or reordering changes which answer belongs to which question. Fix: generate an
   opaque id at creation, never reuse it, key answers by it, and treat the label and the order as display
   fields. For a choice question give each option its own id too, so relabelling an option keeps its answers. The SurveyJS documentation draws the same line: a question's name must be unique across the form and is the key under which the answer is stored, while the title is only what the respondent reads, and a choice item has a unique value apart from its display text (source 1).
3. **Minimal model.** Form, form version (schema document plus settings), question (inside the version, with an
   id, a type, a required flag and constraints), submission (version, started, submitted, status, respondent
   reference if allowed), answer (submission, question id, typed value). Keep the schema as one validated
   document in the version row and answers as rows or a typed document; decide once and keep the type of each
   question's stored value explicit (text, number, date, one option id, list of option ids, file reference).
4. **Conditional logic is data with validation.** Symptom: a rule shows a question depending on one that sits
   later in the form, two rules depend on each other, or a rule references a deleted question or option and the
   form silently shows everything. Fix: a small rule grammar (source question id, operator, value, action show
   or skip to), evaluated by one engine shared by browser and server, and a publish-time check that every
   reference exists, points earlier in the flow, and that the dependency graph has no cycle. Test with a table
   of answers and expected visible questions. The SurveyJS documentation shows why the publish-time check is needed: loading a form definition does not report a visibility expression that names a missing question, and a separate static linter finds misspelled references, conditions that can never be true, and cycles among calculated values and triggers (source 1).
5. **Hidden means not required and not stored.** Symptom: a respondent answers a branch, goes back, changes
   the branch, and the stale hidden answers remain and enter the results; or a required question that is hidden
   blocks submission. Fix: on submit, recompute visibility on the server, drop answers to hidden questions,
   skip required checks for them, and keep the visibility result with the submission for audit. The SurveyJS documentation exposes the same choice as a setting with four modes: keep hidden values, clear them when the question is hidden, clear them when its page or panel is hidden, or clear them only on completion, which is its default (source 1). Only the last two leave stale values in place until the end, so decide the mode and still recompute on the server.
6. **Partial responses are first-class.** Symptom: a long form lost on reload or a session timeout. Fix: a
   submission row in a draft status created on first answer, saved on each section or on blur, resumable by an
   unguessable token or the logged-in user, with an expiry and a clear rule on whether partials are counted in
   results. Distinguish started, in progress, submitted and abandoned in reports. See
   `skills/long-and-multistep-form-pitfalls`.
7. **Anonymous, confidential and pseudonymous are different promises.** Anonymous: nothing stored can lead to
   the person, which also rules out IP address, device fingerprint, a login reference and free text that names
   someone. Confidential: the owner can see identity, others cannot. Pseudonymous: a stable code allows
   linking waves without a name. Symptom: a form labelled anonymous stores a user id on the submission. Fix:
   one explicit mode per form shown to respondents, enforced in what is written, and the mode cannot be
   weakened after responses exist.
8. **Small groups re-identify.** Symptom: a breakdown by team and role shows one respondent's answers. Fix: a
   minimum group size setting; any filter or breakdown below it is suppressed or merged, including combinations
   of filters and differences between two overlapping views. Free-text answers to an anonymous form are shown
   to the owner with a warning, since they can identify. The threshold is a policy choice; none is stated here.
9. **One response per respondent is a rule with a mechanism.** Options: a single-use invitation token, a
   logged-in user, a cookie (weak), none. Symptom: a promise of one response with no mechanism, or a token that
   can be reused after submit. Fix: choose the mechanism per form, mark the token consumed in the same
   transaction as the submission, and say plainly in the settings what the mechanism does not stop.
10. **Archive, never cascade.** Deleting a form must not silently delete its responses; offer archive, then a
    deliberate purge with a retention rule, and handle a respondent's erasure request by deleting or
    anonymising that submission while the form stays (see `skills/laravel-no-cascade-delete`).
