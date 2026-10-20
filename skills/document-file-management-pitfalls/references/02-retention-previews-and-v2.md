# document-file-management-pitfalls §2 — Retention, previews, quotas and v2 regrets

> Part 2 of `skills/document-file-management-pitfalls`. Read it when retention, previews, quotas, an integration
> or the first release are planned. Craft knowledge, no external source read. Retention and records law is not
> legal advice.

1. **Retention is a rule attached to a class of document, not a global setting.** Symptom: everything is kept
   forever, or a cleanup job removed records that had to be kept. Fix: a retention class (name, trigger event
   such as created, closed or contract end, period, action at expiry: delete, anonymise or review) assigned to
   each file or folder, a default class per document type, a visible expiry date, and a job that lists what is
   due for the owner before acting. Which periods apply is for the data-protection owner and legal counsel; the
   application only enforces what they define. Mark any statement of a legal period as "re-read before relying".
2. **Legal hold overrides expiry.** Symptom: a file under dispute is deleted by schedule. Fix: a hold record
   (resource, reason, who, since) checked by the retention job and by every delete path; a held file cannot be
   purged or erased until released, and the audit log records hold and release. How an erasure request interacts
   with a hold is a legal question; see `skills/dsar-handling-pitfalls` and `business/data-protection`.
3. **Trash is a state with a timer.** Symptom: users delete by mistake and ask engineering to recover bytes.
   Fix: delete moves the file to trash (state, deleted time, deleted by), hidden from lists and search,
   restorable until the timer ends, then purged by a job. Trash still counts for quota unless stated.
4. **Purge removes bytes in an audited job, not by cascade.** Symptom: a database cascade deletes rows while the
   objects stay, or a failed storage call leaves rows pointing at nothing. Fix: restrict foreign keys (see
   `skills/laravel-no-cascade-delete`), mark rows `purging`, delete bytes first in a queued idempotent job
   (see `skills/laravel-idempotent-jobs`), then remove the row, keep a minimal tombstone (id, checksum, purge
   time, reason) for audit, and report failures instead of swallowing them. Mind that bulk pruning may skip
   delete events (see `skills/laravel-pruning-fires-delete-events`). Backups and replicas hold copies; state
   how long, as part of the erasure answer.
5. **Erasure of personal data inside documents is a procedure.** Symptom: a person's erasure request deletes
   their account but their name stays in thousands of PDFs. Fix: a way to find files by author, subject or
   extracted text, a decision per file (delete, redact, keep under hold), a record of what was done, and an
   honest limit for content that cannot be searched. Method only; the duty is for the data-protection owner.
6. **Previews and thumbnails are derived, disposable and sandboxed.** Symptom: a malformed file crashes the
   converter, or a huge document ties up the web server, or a stale preview shows an old version. Fix: generate
   in a queued job with a time and memory limit, in a sandbox with no network and no access to other files, keyed
   by version id so a new version makes a new preview, stored in the derived area, regenerable at any time and
   dropped by lifecycle rules, with a fallback icon and a clear "preview unavailable" state. Never render
   untrusted office or HTML content in the app's own origin. Preview only `clean` files (§1, point 12).
7. **Quotas count what costs.** Symptom: a tenant uploads past its plan, or versions and trash eat storage
   unseen. Fix: a size counter per tenant maintained transactionally (not recomputed on each request), counting
   versions, trash and derived files according to a stated rule, a soft warning and a hard stop that refuses new
   uploads with a clear message, and a reconcile job. Limits come from policy.
8. **Search covers metadata first, content second.** Symptom: users cannot find a file by name, or search shows
   titles they may not open. Fix: a metadata index (name, tags, folder, owner, dates), optional extracted text
   indexed asynchronously from `clean` files only, access filters applied inside the query, not after, and an
   index entry removed on purge (see `skills/search-index-sync-pitfalls` and
   `skills/filters-search-and-saved-views-pitfalls`).
9. **Tags and metadata fields are typed and bounded.** Same rule as custom fields in other apps: a choice list
   with stable ids, a cap per file type, and no logic hidden in a free-text tag.
10. **Check-out and edit conflicts are decided.** Symptom: two people edit a downloaded copy and the later
    upload hides the earlier one. Fix: choose between a lock (check-out with an owner and an expiry) and a
    version-compare on upload (reject when the base version is stale and offer a new version beside it); never
    silently accept the later upload as current.
11. **Integrations are idempotent and bounded.** Mail attachment capture, sync from another drive and e-signature
    return files; each import uses an external id and checksum to stay idempotent, passes through quarantine and
    scanning like any upload, stores the source reference and keeps provider tokens in a vault. Signed
    documents are stored as new, locked versions with the signature evidence, and their retention follows the
    class of the document (see `skills/light-erp-document-flow-pitfalls`).
12. **Exports and bulk downloads are jobs.** A folder download is a queued job producing an archive with a
    signed expiring link, respects the requester's permissions per file, caps total size by policy, avoids zip
    path traversal by generating entry names itself, and logs who exported what.
13. **What to split first.** Build in this order and keep each independent: file and version records with
    opaque keys and tenancy; upload and download through an authorised path with type checks; permissions and
    sharing; scanning on quarantine; trash and purge; retention classes and holds; previews; search; quotas;
    then integrations. Ship the first four before any viewer or editor, because every later feature trusts them.
14. **What is regretted at v2.** The filename as key; overwritten versions; a public bucket; permissions checked
    only on folders; a preview inline with the web worker; inferred content type; scanner flipping to clean on
    error; cascade deletes leaving bytes; one global retention setting; no tombstone for audit; no tenant
    prefix so one tenant's export was a project. Each is cheap at the first migration and expensive after the
    bytes exist.
15. **Laravel and Nuxt pointers, short.** In Laravel: a private disk with generated keys, a file and a version
    model, a policy used by controllers and by the signed-URL endpoint, queued jobs for scan, preview and
    purge with retries and a failed-job alert, a scheduled retention command that only reports in dry-run
    mode first, and validation rules that check content, not only extension. In Nuxt: upload directly to
    storage with a server-issued permission or through the API with progress, show the file state (pending,
    clean, infected) explicitly, never construct download URLs on the client from a key, and keep viewers
    behind a sandboxed frame.
