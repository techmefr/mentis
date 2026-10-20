# document-file-management-pitfalls: origin and source stamps

> Provenance of `skills/document-file-management-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against an open-source upload protocol and two vendor documentation pages. Never run by us: no application was built and no test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | tus resumable upload protocol (`tus/tus-resumable-upload-protocol`, commit `c6a11fa`): `protocol.md`, core protocol and the expiration, checksum and termination extensions | MIT: file `LICENSE.txt` read | Offset-based resume, conflict on a mismatched offset, maximum size, per-chunk checksum, expiry of unfinished uploads, termination to free resources |
| 2 | Amazon S3 User Guide, pages "Configuring a bucket lifecycle configuration to delete incomplete multipart uploads" and "Download and upload objects with presigned URLs" (`docs.aws.amazon.com`) | Vendor documentation, no open licence stated: facts only, rewritten, no sentence copied | Abort-incomplete-upload lifecycle rule as a cost measure, presigned link validity bounded by the signing credentials |

Neighbouring blocks of this repository were read to avoid duplication: `skills/security-hardening` (web
hardening), `skills/dsar-handling-pitfalls`, `skills/light-erp-document-flow-pitfalls` (document numbering and
history), `skills/field-and-row-permission-ui-api-pitfalls`, `skills/laravel-no-cascade-delete`,
`skills/laravel-pruning-fires-delete-events`, `skills/search-index-sync-pitfalls` and `business/data-protection`.
The overlap check found no block that covers building a document or file store (versions, storage layout,
sharing, retention, scanning). Upload and viewer screens are written by a sibling lot as UI-component blocks,
so this block covers data, storage and rules only.

## Verified
1. §1 point 11 (layered limits, chunked uploads, abandoned partial uploads) and point 9 (signed short-lived links): sources 1 and 2.

## Added
1. §1 point 15, signed link lifetime bounded by the signing credentials: source 2.

## Removed
1. **Every numeric threshold, size limit, retention period, quota and timer.** None is stated; set them by policy.
2. **Any statement of retention, records or erasure law.** Not read; method only.
3. **Named storage services, scanners and converters:** not used.

## Not verified
1. **Still our own guidance:** opaque keys and layout (§1 points 1 to 3), versions and duplicates (points 4 and 5), permission
   inheritance and sharing links (points 6 to 8), content-type detection and safe serving (point 10), quarantine scanning
   (point 12), filenames (point 13), tenants (point 14), and the whole of §2: retention classes, holds, trash, purge,
   erasure, previews, quotas, search, conflicts, integrations, exports, build order and v2 regrets. No permissive document
   system documentation was identified (searched: the upload protocol and the vendor pages above; no document-management
   project documentation was read).
2. **Legal questions** (retention periods, legal hold, erasure) belong to the data-protection owner and legal
   counsel; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** (Laravel, Nuxt) are short and were not checked against a current release; re-read
   before relying.

## Related blocks
`skills/security-hardening`, `skills/dsar-handling-pitfalls`, `skills/laravel-no-cascade-delete`,
`skills/laravel-idempotent-jobs`, `skills/admin-back-office-pitfalls`, `business/data-protection`.
