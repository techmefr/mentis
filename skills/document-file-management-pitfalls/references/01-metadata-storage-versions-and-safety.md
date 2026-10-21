# document-file-management-pitfalls §1 — Metadata, storage, versions and safety

> Part 1 of `skills/document-file-management-pitfalls`. Read it when a schema, a storage layout or an upload
> path is designed. Mostly craft knowledge; points 9, 10, 11 and 13 and the new point 15 carry facts from an open-source upload protocol (MIT), two pages of a storage vendor's documentation, the Fetch and MIME Sniffing standards (CC BY 4.0), IETF standards, the HTML Standard, a W3C note on capability URLs and the ZIP format specification, read 2026-10-20 and restated in our words (`references/origin.md`, sources 1 to 9). Everything not marked as sourced is our own guidance. Each point gives the symptom, the check and the
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
   for how many versions or how long they are kept (policy, set by the owner). Give every version a fresh key: the storage vendor documents that an upload through a presigned link replaces any object already stored under the key named in the link (source 2), so a link that names an existing key overwrites the old bytes.
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
   storage key. A link to a folder does not extend to files added later unless the owner chose that. The W3C note on capability URLs (source 6) lists how such links leak: address bars, logs and history, the Referer header sent to another site, and third-party scripts on the page; its advice is https only, expiry (including one-time links), no third-party links or scripts on the page opened through the link (or rel noreferrer on them), several links per resource so one can be revoked alone, 410 or 404 once expired, and an unguessable identifier instead of a counter. It is a 2014 working draft, so treat it as guidance.
8. **Ownership survives departures.** Symptom: a user leaves and their files vanish or stay stuck. Fix:
   ownership belongs to the workspace or a transferable owner; deactivate users rather than delete them; a
   transfer action with an audit row.
9. **Serve files through an authorised path.** Symptom: a public bucket or a long-lived URL leaks files, or
   the app streams large downloads and exhausts workers. Fix: keep storage private; for each download check
   authorisation, then redirect to a short-lived signed URL or stream via the web server's offload feature;
   set cache headers so a private file is never stored by a shared cache; log the download. The storage vendor's documentation confirms that a presigned link works for whoever holds it until it expires, and can be used any number of times before then; the vendor checks the expiry when the request arrives, so a download that began in time finishes even if the expiry passes, while a resumed download after expiry fails (source 2). That is why the authorisation check comes before the redirect and the link is short-lived, and why a strictly one-time download needs an application-side token, not a presigned link. Cache headers: in HTTP caching a shared cache may not reuse a response to a request carrying an Authorization header unless the response allows it, and the private directive bars shared caches from storing a response at all (RFC 9111 sections 3.5 and 5.2.2.7, source 7).
10. **Do not trust the type, serve safely.** Symptom: an upload named `.jpg` is HTML, opens inline and runs
    script on the application's origin. Check: upload an HTML file renamed to an image and a script inside an
    SVG, then open them. Fix: detect the type from content (magic bytes), compare with an allow-list per
    feature, store the detected type, serve with a fixed content type from that list, a no-sniff header, a
    forced-download disposition for anything not meant to render, a content-security policy on the download
    host, and ideally a separate cookieless domain for user content. The Fetch Standard defines the no-sniff header as a request filter: with it, a script-like request is blocked when the declared type is not a JavaScript type and a style request is blocked unless the type is text/css; the standard leaves out images because blocking them was not compatible with deployed content, so the header does not stop a wrongly typed image or document by itself. The MIME Sniffing Standard adds that when sniffing is switched off the computed type is the declared type, and when the declared type is missing or unknown the sniffing rules run with scriptable types disabled (source 3). The HTML Standard's own sandboxed-frame example says user content should be served from a separate domain, so that a visit straight to the page does not run in the site's origin (source 5). Treat SVG, HTML and office files with
    macros as active content. See `skills/security-hardening`.
11. **Upload limits are layered and consistent.** Symptom: the front accepts 200 MB, the proxy cuts at 1 MB and
    the user sees a generic error; or an unbounded body fills the disk. Fix: size and count limits set at the
    proxy, the application and the storage policy with the same numbers (chosen by policy), a per-user and
    per-tenant quota (§2, point 7), chunked or direct-to-storage uploads for large files with a server-issued
    permission and a completion call that verifies size and checksum, and cleanup of abandoned partial
    uploads by a scheduled job. The resumable upload protocol shows the pieces: the client asks the server for the current byte offset and continues from it; a chunk whose offset differs from the server's is refused with a conflict status and nothing is changed; the server may announce a maximum size, may verify a checksum per chunk, may let unfinished uploads expire after which they cannot be resumed, and may let the client terminate an upload to free its resources (source 1). The storage vendor recommends a lifecycle rule that aborts incomplete multipart uploads to keep their storage cost down (source 2).
12. **Scan on a quarantine path and gate release.** Symptom: an infected file is shared before the scanner
    finishes, or the scanner is down and files pass. Check: upload a harmless standard antivirus test file and
    stop the scanner. Fix: new uploads land in a quarantine location with state `pending`; a queued job scans
    and sets `clean` or `infected` with the engine name and signature version; only `clean` is downloadable,
    previewable or shareable; `infected` is isolated, the owner is told, an audit row is written; a scanner
    outage leaves files `pending` and retries, never flips to clean; large or archive files get a bounded scan
    with a stated outcome for "too big to scan" decided by policy. Re-scan on signature updates only if the
    policy asks for it. Scanning reduces risk; it does not prove safety.
13. **Filenames on download are safe.** Strip control characters and quotes from the suggested name, encode
    non-ASCII correctly in the disposition header, and never reflect the name unescaped in a page. The header standard says to put the UTF-8 encoded name in the extended `filename*` parameter, with a plain `filename` before it as a fallback for old clients (its own example puts the fallback first, because clients that do not know the extended form ignore it when it comes after), and to treat the name as advisory: clients should keep only the last path segment, with both slash kinds as separators, strip or replace control characters and leading and trailing whitespace, and ignore names with special meaning such as `.`, `..`, `~`, `|` and device names, and a recipient that picks the media type from the file extension must use a safe one (source 4). It warns that many clients mishandle a backslash escape in the quoted form and may unescape percent sequences, so a name containing a percent sign followed by two hex digits can be misread. That duty is the client's; the server still strips separators (point 2) and chooses the extension itself. The extended-parameter encoding is now defined in RFC 8187, which obsoletes RFC 5987 (the one RFC 6266 points to) and requires UTF-8 from producers (source 8).
14. **Every record belongs to a tenant from the first migration.** Tenant column on files, versions, folders,
    shares and scan rows, one default scope (see `skills/laravel-tenant-context-by-default`), storage prefix
    from the tenant, and a test per path.
15. **A signed link cannot outlive the credentials that signed it.** Symptom: a link meant to last a day stops working after
    an hour, or a link believed to be short lives as long as the signer's credentials. Check: create a link with the
    longest lifetime your policy allows using the same credentials the application really runs with, and measure when it
    stops. Fix: choose the lifetime knowing that the vendor's presigned link expires when the temporary role session that
    signed it expires, even if a longer lifetime was requested (source 2); refresh the link on demand from an authorised
    request instead of storing it.
