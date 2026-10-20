# survey-form-builder-app-build-pitfalls §2 — Public endpoint, roles, exports and v2

> Part 2 of `skills/survey-form-builder-app-build-pitfalls`. Read it when a share link, an export, a webhook or
> the first release are planned. Mostly craft knowledge; point 1 carries facts from the SurveyJS documentation in `references/origin.md` (source 1), read 2026-10-20. Everything not marked as sourced is our own guidance.

1. **The public endpoint is untrusted input.** Symptom: a crafted request submits an answer to a hidden
   question, a value outside the options, a ten-megabyte text, or an answer to a closed form. Fix: validate the
   whole submission server-side against the version's schema (types, option ids, lengths, required after
   recomputing visibility), reject unknown question ids, check the form is open and within its dates, and
   never trust a value computed in the browser, such as a quiz score. Return field-level errors by question id. The SurveyJS documentation recommends the same stance for its Node backend: rebuild the form model from the stored definition on the server, load the posted data into it and clear values that do not fit, instead of storing what the browser sent, and its server validation hook returns errors keyed by question name (source 1).
2. **Spam and duplicates are handled in layers.** A rate limit per address and per form, a honeypot field, a
   challenge on forms that need it, a submission time lower bound, a duplicate check per mechanism from §1
   point 9. Symptom: results skewed by a script. Fix: store a flag per submission instead of silently
   dropping, so the owner can review and exclude; do not use a fingerprint on an anonymous form.
3. **Roles and visibility are a rule on the query.** Typical shape: owner and editors change the form, analysts
   read responses, a viewer reads aggregates only, a collaborator sees only their own forms. Symptom: the
   response list is guarded but the export, the webhook payload, the notification email and a shared results
   link still expose rows. Fix: one scoping function for every read path and abilities (edit-form, publish,
   view-responses, view-identity, export, delete-responses) rather than role names (see
   `skills/laravel-permissions-not-roles`); a shared results link is read-only, aggregate-only and revocable.
4. **Exports are stable and safe.** Columns keyed by question id with the label as header at export time, one
   column per option for multi-select or a defined joined format, the version and submission time in the file,
   and one file layout across versions with empty cells where a question did not exist. Neutralise cells that
   start with a formula character; large exports are an async job with an expiring link and an audit entry of
   who exported what. See `skills/csv-xlsx-import-export-pitfalls`.
5. **Analysis reads a defined number.** A response rate names its denominator (invited, started, or reached);
   an average of a scale says whether skipped answers count; results across versions say how a changed
   question is combined or not. Symptom: a headline figure that moves when someone edits a form. Fix: one
   query per metric reused by the screen and the export. See `skills/reporting-analytics-app-build-pitfalls`.
6. **Integrations are idempotent and versioned.** An outbound webhook carries an event id, the form id, the
   version and the submission id so a receiver can ignore replays; failures retry with a cap and a visible
   status. Treat tokens as secrets in a vault. Inbound embeds run in an isolated frame and cannot read the host
   page.
7. **Uploads and rich text inside a form are riskier than text.** A file question needs a type and size policy
   and storage outside the web root (see `skills/file-upload-ui-pitfalls`); a rich-text answer is sanitised
   on output (see `skills/rich-text-editor-pitfalls`).
8. **Accessibility and language belong to the schema.** Labels, help and error text per language on the
   version, not on the question forever; every question has a programmatic label; errors name the question.
   See `skills/i18n-catalog-workflow-pitfalls`.
9. **What to split first.** Form, version and question types with server validation; submissions and partial
   resume; logic with publish checks; anonymity modes and group minimums; exports; then webhooks, templates
   and analytics. Ship the first three before any integration.
10. **What is regretted at v2.** Answers keyed by label or position; edits in place; logic validated only in the
    browser; "anonymous" with a user id stored; no resume; export columns that shift between runs; no tenant
    column; a response count that nobody can define; hard-deleted forms. Each is cheap at the first migration
    and expensive once responses exist.
11. **Laravel and Nuxt pointers, short.** In Laravel: a form request built from the version's schema, a JSON
    column or typed answer table with a unique key on form version and submission and question id, a policy per
    ability, a queued export job, a unique single-use token column. In Nuxt: render the form from the schema
    document, share the logic engine through a package used by both sides, and never compute scores or
    visibility only on the client.
