# cms-app-build-pitfalls §1 — Minimal model and its pitfalls

> Part 1 of `skills/cms-app-build-pitfalls`. Read it when a schema or a write path is designed. Mostly craft knowledge;
> points 2, 4, 5 and 6 carry facts from the Payload documentation (MIT), read 2026-10-20 and restated in our words (`references/origin.md`, source 1). Everything not marked as sourced is our own guidance. Each point gives the symptom, the check and the fix.

1. **Content model changes are migrations, in three steps.** Symptom: an editor-facing "delete field" or "change
   type" on a content type with entries wipes data or makes old entries fail validation and break the site.
   Check: create entries, change the type, load an old entry and the delivery API. Fix: expand (add the new
   field, optional), migrate (a job converts or fills existing entries, reported with counts and errors), then
   contract (remove the old field only when nothing reads it, after a delay and a backup). Never change a field
   type in place; add a new field. Treat required-ness added later as a backfill task, not an instant rule.
2. **Draft, published and archived are separate states of one entry.** Symptom: an editor fixes a sentence
   and the live page changes mid-edit, or an unfinished paragraph goes live. Fix: the published version is
   an immutable snapshot; editing happens on a draft; publish copies the draft to the live pointer in one
   transaction; "unpublish" moves the live pointer to none and keeps the draft. Keep the status as a small
   enumeration with defined transitions (see `skills/laravel-recognise-state-machine-or-pipeline`). The Payload documentation uses the same split: with drafts on, each entry gets a status field, the admin shows three states (draft, published, and changed when a newer draft exists), a draft save skips the required-field checks unless draft validation is turned on, and unpublishing is setting the status back to draft (source 1).
3. **Minimal model.** Content type, field definition (type, constraints, localised or not), entry (stable id,
   type, status, live revision pointer, created by), revision (entry, number, field values, author, time, note),
   media asset, asset usage, taxonomy term, entry-to-term link, locale, user, role. Give each entry a stable
   id separate from its slug.
4. **Scheduling is a job with state, not a date on a row.** Symptom: a scheduled post goes live an hour off
   after a clock change, appears twice, or never appears because the worker was down. Fix: store the instant
   in UTC with the editor's zone, a scheduled-action row (publish or unpublish, entry, revision, run-at,
   status), a worker that picks due rows idempotently and also catches up on missed ones, and an audit entry.
   Publishing a revision that was later changed publishes the revision chosen, not the latest draft. See
   `skills/laravel-scheduling`. The Payload documentation warns about the failure named here: its scheduled publish works by creating a background job, and without a worker that processes jobs the scheduled action is never executed (source 1).
5. **Concurrent editing needs a version check.** Symptom: two editors open the same entry, the second save
   silently erases the first. Check: open in two tabs, save both. Fix: each save carries the revision number
   or an updated-at token it started from; a mismatch returns a conflict with a diff or a "reload and merge"
   path; optionally a soft lock showing who is editing, with a timeout, as a courtesy and never as the protection. The Payload documentation describes such a lock: opening an entry locks it for that user, others can view read-only or take over, the lock expires after inactivity, and it can be switched off per collection (source 1). It is a lock, not a version check, so keep the check above as the protection.
6. **Revisions record who, when, what and why.** Symptom: nobody can say who changed a price on the page or
   restore the version before. Fix: a revision row per save or per meaningful change (autosave kept short-lived
   and collapsed), with author, time, an optional note, and a field-level diff; restore creates a new revision
   from the old one rather than rewriting history. Decide the retention for old revisions, since they grow
   without bound; the period is policy. The Payload documentation keeps versions in a separate collection with the user who made each change, and caps them per entry with an option to keep all (source 1).
7. **Media is an asset record, not a file path in the text.** Symptom: an image replaced in the library does
   not update pages, a deleted asset leaves broken images, an uploaded file is executed, or originals of 40
   megapixels are served to phones. Fix: store the original once, generate derivatives (sizes, formats) on
   demand or by a job, reference assets by id from fields, track usage so deletion warns or blocks, store alt
   text and focal point on the asset with a per-entry override, validate type by content, strip risky metadata
   per policy, and serve from storage that cannot execute files. See `skills/file-upload-ui-pitfalls`,
   `skills/document-file-management-pitfalls`.
8. **Slugs are unique, editable and redirected.** Symptom: a title change moves the URL and every inbound link
   404s, or two entries share a slug. Fix: a slug unique within its scope (type, locale, parent), generated
   from the title once and then independent, a history table of past slugs with a permanent redirect to the
   current one, a reserved list for system paths, and a check that a redirect never forms a chain or a loop.
9. **Locales are linked variants, with a fallback rule.** Symptom: a translated page points at a deleted
   original, the fallback shows the wrong language silently, or changing the source leaves translations marked
   current. Fix: a translation group id linking the variants, a status per locale (missing, draft, published,
   out of date), a source revision recorded on each translation so staleness is computed, a documented fallback
   order, locale-aware slugs, and language tags on delivered content. Decide per field whether it is localised
   (a price is often not). See `skills/i18n-catalog-workflow-pitfalls`.
10. **Archive, never cascade.** Deleting a content type, a taxonomy term or a user must not delete entries or
    revisions: reassign or archive, keep authorship as a record that survives a user's removal, and handle a
    personal-data erasure request as a documented edit of the content and its revisions (see
    `skills/laravel-no-cascade-delete`).
