# document-file-management-pitfalls: origin and source stamps

> Provenance of `skills/document-file-management-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against an open-source upload protocol and two vendor documentation pages. Never run by us: no application was built and no test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | tus resumable upload protocol (`tus/tus-resumable-upload-protocol`, commit `c6a11fa`): `protocol.md`, core protocol and the expiration, checksum and termination extensions | MIT: file `LICENSE.txt` read | Offset-based resume, conflict on a mismatched offset, maximum size, per-chunk checksum, expiry of unfinished uploads, termination to free resources |
| 2 | Amazon S3 User Guide, pages "Configuring a bucket lifecycle configuration to delete incomplete multipart uploads" and "Download and upload objects with presigned URLs" (`docs.aws.amazon.com`) | Vendor documentation, no open licence stated: facts only, rewritten, no sentence copied | Abort-incomplete-upload lifecycle rule as a cost measure, presigned link validity bounded by the signing credentials |
| 3 | WHATWG Fetch Standard (the X-Content-Type-Options and nosniff sections) and WHATWG MIME Sniffing Standard (no-sniff flag, computed type), <https://fetch.spec.whatwg.org/>, <https://mimesniff.spec.whatwg.org/>, read 2026-10-20 | CC BY 4.0 (the `LICENSE` file of each repository was read 2026-10-20) | No-sniff blocks script-like and style requests with a wrong type, leaves images out; computed type with sniffing off. Replaces the MDN page credited in the first pass (a CC BY-SA documentation site, no longer used) |
| 4 | RFC 6266, Use of the Content-Disposition Header Field in HTTP (IETF, 2011), the filename parameter sections and examples, re-read in full 2026-10-20 | IETF standard text, read for facts only and restated | `filename*`, `filename` fallback and its order, filename advisory, last path segment, characters and names to strip, extension safety, escape and percent quirks |
| 5 | WHATWG HTML Standard, the iframe sandbox section and its examples, single-page standard fetched 2026-10-20 | CC BY 4.0 (WHATWG; `LICENSE` read 2026-10-20) | Separate domain for user content, allow-scripts with allow-same-origin removes the sandbox (§1 point 10, §2 point 6) |
| 6 | W3C TAG, Good Practices for Capability URLs, First Public Working Draft 18 February 2014, <https://www.w3.org/TR/capability-urls/>, read 2026-10-20 | W3C Document License; facts only, own words | Leak routes, https, expiry, revoke, unguessable identifiers (§1 point 7) |
| 7 | RFC 9111, HTTP Caching, sections 3.5 and 5.2.2.7, <https://www.rfc-editor.org/rfc/rfc9111>, read 2026-10-20 | IETF Trust document; facts only | Shared caches and Authorization, the private directive (§1 point 9) |
| 8 | RFC 8187, Indicating Character Encoding and Language for HTTP Header Field Parameters, <https://www.rfc-editor.org/rfc/rfc8187>, read 2026-10-20 | IETF Trust document; facts only | Obsoletes RFC 5987; producers use UTF-8 (§1 point 13) |
| 9 | PKWARE, ZIP File Format Specification (APPNOTE) version 6.3.10, sections 4.3.9.2 and 4.4.17.1, <https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT>, read 2026-10-20 | Vendor specification, no open licence stated; facts only, own words | Entry names without drive letter or leading slash, ZIP64 above 0xFFFFFFFF (§2 point 12) |

Neighbouring blocks of this repository were read to avoid duplication: `skills/security-hardening` (web
hardening), `skills/dsar-handling-pitfalls`, `skills/light-erp-document-flow-pitfalls` (document numbering and
history), `skills/field-and-row-permission-ui-api-pitfalls`, `skills/laravel-no-cascade-delete`,
`skills/laravel-pruning-fires-delete-events`, `skills/search-index-sync-pitfalls` and `business/data-protection`.
The overlap check found no block that covers building a document or file store (versions, storage layout,
sharing, retention, scanning). Upload and viewer screens are written by a sibling lot as UI-component blocks,
so this block covers data, storage and rules only.

## Verified
1. §1 point 10 (no-sniff header, source 3, now the Fetch and MIME Sniffing standards, with the MDN credit dropped) and point 13 (disposition filename encoding, source 4, re-read in full and extended with the RFC 6266 filename rules and RFC 8187); the rest of those points stays our own guidance. Second pass 2026-10-20: the tus claims (offset, 409 on a mismatched offset, Tus-Max-Size, per-chunk checksum, Upload-Expires, termination) and the two S3 pages re-read against the raw protocol file and the live vendor pages, all confirmed; 0 corrected, 0 deleted; sourced additions: S3 presigned upload replaces an existing key (§1 point 4), presigned link multi-use and expiry check at request time (§1 point 9), capability URL practices (§1 point 7), cache directives (§1 point 9), HTML sandbox and separate domain (§1 point 10, §2 point 6), RFC 6266 name rules (§1 point 13), ZIP names and ZIP64 (§2 point 12).
2. §1 point 11 (layered limits, chunked uploads, abandoned partial uploads) and point 9 (signed short-lived links): sources 1 and 2.

## Added
1. §1 point 15, signed link lifetime bounded by the signing credentials: source 2.

## Removed
1. **Every numeric threshold, size limit, retention period, quota and timer.** None is stated; set them by policy.
2. **Any statement of retention, records or erasure law.** Not read; method only.
3. **Named storage services, scanners and converters:** not used.

## Not verified
1. **Still our own guidance:** opaque keys and layout (§1 points 1 to 3), versions and duplicates (points 4 and 5), permission
   inheritance and sharing links (points 6 to 8), content-type detection and safe serving (point 10, beyond the no-sniff header), quarantine scanning
   (point 12), filenames (point 13, beyond the header encoding), tenants (point 14), and the whole of §2: retention classes, holds, trash, purge,
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
Independent verification 2026-10-21: 16 checked, 15 matched, 1 corrected, 0 unverified
