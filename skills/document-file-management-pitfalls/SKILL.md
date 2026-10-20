---
name: document-file-management-pitfalls
description: "Use when a document or file management application is designed or built: file metadata separate from stored bytes, content-addressed or opaque storage keys and layout, versions that never overwrite, folder and per-file permissions with inheritance, sharing links that expire, retention and legal hold as method, antivirus scanning on a quarantine path, previews and thumbnails as derived and disposable, upload limits and content-type checks, safe downloads, and what to split first and what gets regretted at v2. Method only; retention and records law is not legal advice. Upload and viewer screens are separate blocks."
---

# document-file-management-pitfalls

A defensive block for building the application that stores, versions and shares files, not for organising a
company's documents. A file store built in a hurry fails in familiar ways: the filename is the storage key so
two uploads collide, a new version overwrites the old one, a shared folder exposes a file its owner meant to
keep private, an uploaded file is served with a type that lets a browser run it, a "deleted" document is still
on disk for years, and previews are generated inline until a large file takes the server down. The content is
craft knowledge with no external source read (see `references/origin.md`). The upload and viewer screens are UI
components covered by their own blocks; this block covers the data, storage and rules behind them. Tenant
boundaries are in `skills/laravel-tenant-context-by-default`, role design in `skills/laravel-permissions-not-roles`,
visibility in `skills/field-and-row-permission-ui-api-pitfalls`, background work in `skills/background-jobs-conventions`
and `skills/laravel-idempotent-jobs`, web hardening in `skills/security-hardening`, erasure handling in
`skills/dsar-handling-pitfalls`, personal data duties in `business/data-protection`, staff audit in
`skills/admin-back-office-pitfalls`.

## When
- A new document manager, file vault, attachment feature or shared drive is specified or its schema is drafted.
- An existing app grows versions, folder sharing, previews, retention or antivirus scanning.
- A feature touches upload, download, deletion or access to stored files.

## Steps

**Read the part you need before the schema, the bucket layout or the upload endpoint is written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Metadata and bytes, storage layout, versions, permissions, sharing, upload and download safety, scanning | a schema, a storage layout or an upload path is designed | [`01-metadata-storage-versions-and-safety.md`](./references/01-metadata-storage-versions-and-safety.md) |
| 2 | Retention and holds, deletion and erasure, previews, search, quotas, integrations, split order, v2 regrets, framework pointers | retention, previews, quotas or the first release are planned | [`02-retention-previews-and-v2.md`](./references/02-retention-previews-and-v2.md) |

## Output / checkpoint
Before building: the entity list (file, version, folder, share, scan result), the storage key scheme, the
version and restore rules, the permission model with inheritance and the sharing rules, the retention and
deletion behaviour written down, and the upload and download contract (limits, accepted types, response
headers). Evidence is a test that two uploads with the same name both survive, a test that a new version leaves
the old one retrievable, a test that a user without access gets the same response as for a missing file through
the list, the search, the direct link and the preview, and a test that an infected or unscanned file is not
downloadable. Nothing here was run by us.

## Guardrails
- This block is not legal advice. Retention periods, records duties and erasure obligations depend on the
  jurisdiction and the document type; ask the data-protection owner and see `business/data-protection`.
- Never use the user's filename as the storage key or path; use an opaque key and keep the name as metadata
  (§1, point 2).
- Never overwrite stored bytes; a change is a new version (§1, point 4).
- Never make the storage bucket or folder public to serve files; serve through an authorised endpoint or a
  short-lived signed link (§1, point 9).
- Never trust the declared content type or extension; check the content and serve with a fixed type, a
  forced-download disposition where needed and a no-sniff header (§1, point 10).
- Never release an upload to users before the scan result is clean (§1, point 12).
- Never enforce permission in the screen only, nor on the folder only when a file can be reached directly (§1,
  point 6).
- Never delete with a database cascade; remove bytes in an audited job (§2, point 4).

## Origin
Written from craft knowledge of building document and file-management applications; no open-source document
system documentation was read, so no source is credited and no text was taken. See
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
