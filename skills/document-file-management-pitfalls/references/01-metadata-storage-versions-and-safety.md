# document-file-management-pitfalls §1 — Metadata, storage, versions and safety

> Part 1 of `skills/document-file-management-pitfalls`. Read it when a schema, a storage layout or an upload
> path is designed. Craft knowledge, no external source read. Each point gives the symptom, the check and the
> fix.

1. **Metadata and bytes are two things.** Symptom: moving or renaming a file rewrites the stored object, or a
   lost database row orphans bytes nobody can find. Fix: a file record (id, tenant, owner, display name,
   size, declared and detected type, checksum, state, created time) in the database, and bytes in object or
   disk storage addressed by a key. Renaming and moving change the record only. A periodic job compares the two
   sides and reports orphan objects and missing bytes before either is deleted.
2. **The storage key is opaque.** Symptom: two users upload `report.pdf` and one replaces the other, or a name
   such as `../x` writes outside the folder, or a name with a personal name leaks into a log or a URL. Check:
   upload two files with the same name, one with path characters, one with a very long Unicode name. Fix: a
   generated key (a random id, or a content hash plus tenant prefix), never the user's name; keep the display
   name as metadata, normalise and length-limit it, and strip path separators and control characters.
3. **Storage layout is chosen for operations, not looks.** Symptom: one flat folder with millions of objects,
   or a layout that mixes tenants so one backup or export cannot be scoped. Fix: a tenant prefix first, then a
   short fan-out derived from the key, separate buckets or prefixes for originals, derived files (previews)
   and quarantine, and lifecycle rules that apply to each differently. Decide the backup and restore unit
   before the first upload, and keep the layout independent of the folder tree the user sees.
4. **Versions never overwrite.** Symptom: a new upload replaces the old bytes and a mistaken save cannot be
   undone. Check: upload twice and fetch the first. Fix: a version record (file id, number, key, size,
   checksum, author, time, comment) per upload, a pointer from the file to its current version, restore as
   "make an old version current by creating a new version that points at the same bytes", and a per-file rule
   for how many versions or how long they are kept (policy, set by the owner).
5. **Duplicates are a storage matter, not a user-facing merge.** Same checksum in one tenant may share bytes
   by reference with a reference count; never share bytes across tenants where a deletion or a leak in one
   would touch another. Detect duplicates by checksum, warn the user, but let them keep two records.
6. **Permissions: folder inheritance plus file override, checked on the file.** Symptom: moving a file into a
   shared folder silently exposes it, or a file inside a private folder is readable through its direct id.
   Check: read each file through list, search, direct id, preview, download and share link as a user without
   access. Fix: an access record (subject, resource, ability) with inheritance from the folder, an explicit
   override that can restrict as well as grant, a stated rule for what a move does to inherited access (show
   the effect before confirming), and one authorisation function called by every path, including the preview
   and the search index. An unauthorised read returns the same response as a missing file. See
   `skills/field-and-row-permission-ui-api-pitfalls` and `skills/laravel-permissions-not-roles`.
7. **Sharing links are credentials.** Symptom: a link posted once works forever for anyone. Fix: a random,
   unguessable token stored hashed, an expiry by default, optional password, an ability limited to view or
   download, a revoke button, a per-link access log, and an owner view of active links. Links never carry the
   storage key. A link to a folder does not extend to files added later unless the owner chose that.
8. **Ownership survives departures.** Symptom: a user leaves and their files vanish or stay stuck. Fix:
   ownership belongs to the workspace or a transferable owner; deactivate users rather than delete them; a
   transfer action with an audit row.
9. **Serve files through an authorised path.** Symptom: a public bucket or a long-lived URL leaks files, or
   the app streams large downloads and exhausts workers. Fix: keep storage private; for each download check
   authorisation, then redirect to a short-lived signed URL or stream via the web server's offload feature;
   set cache headers so a private file is never stored by a shared cache; log the download.
10. **Do not trust the type, serve safely.** Symptom: an upload named `.jpg` is HTML, opens inline and runs
    script on the application's origin. Check: upload an HTML file renamed to an image and a script inside an
    SVG, then open them. Fix: detect the type from content (magic bytes), compare with an allow-list per
    feature, store the detected type, serve with a fixed content type from that list, a no-sniff header, a
    forced-download disposition for anything not meant to render, a content-security policy on the download
    host, and ideally a separate cookieless domain for user content. Treat SVG, HTML and office files with
    macros as active content. See `skills/security-hardening`.
11. **Upload limits are layered and consistent.** Symptom: the front accepts 200 MB, the proxy cuts at 1 MB and
    the user sees a generic error; or an unbounded body fills the disk. Fix: size and count limits set at the
    proxy, the application and the storage policy with the same numbers (chosen by policy), a per-user and
    per-tenant quota (§2, point 7), chunked or direct-to-storage uploads for large files with a server-issued
    permission and a completion call that verifies size and checksum, and cleanup of abandoned partial
    uploads by a scheduled job.
12. **Scan on a quarantine path and gate release.** Symptom: an infected file is shared before the scanner
    finishes, or the scanner is down and files pass. Check: upload a harmless standard antivirus test file and
    stop the scanner. Fix: new uploads land in a quarantine location with state `pending`; a queued job scans
    and sets `clean` or `infected` with the engine name and signature version; only `clean` is downloadable,
    previewable or shareable; `infected` is isolated, the owner is told, an audit row is written; a scanner
    outage leaves files `pending` and retries, never flips to clean; large or archive files get a bounded scan
    with a stated outcome for "too big to scan" decided by policy. Re-scan on signature updates only if the
    policy asks for it. Scanning reduces risk; it does not prove safety.
13. **Filenames on download are safe.** Strip control characters and quotes from the suggested name, encode
    non-ASCII correctly in the disposition header, and never reflect the name unescaped in a page.
14. **Every record belongs to a tenant from the first migration.** Tenant column on files, versions, folders,
    shares and scan rows, one default scope (see `skills/laravel-tenant-context-by-default`), storage prefix
    from the tenant, and a test per path.
