# file-upload-ui-pitfalls: origin and source stamps

> Provenance of `skills/file-upload-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No uploader was built, run or tested while writing it. Read date: 2026-10-20.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: type-prefix allow-list and served-type replay checks, search recipe for a hidden input behind a label, silent truncation and batch-failure checks, database-stored files, skip-when line.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| tus/tus-resumable-upload-protocol at commit c6a11fa (protocol 1.0.0, 2016-03-25) | MIT, Copyright (c) 2013-2016 Transloadit Ltd and Contributors (`LICENSE.txt` read 2026-10-20) | Offset-based resume with HEAD and PATCH, creation extension and the upload URL, expiration header, checksum extension and its mismatch status, termination, concatenation, size limit and version negotiation |
| transloadit/uppy at commit a16a4be | MIT, Copyright (c) 2019 Transloadit (`LICENSE` read 2026-10-20) | Only that a modular client with S3 multipart and tus plugins exists (README opened, one line used as a pointer); no behaviour was taken |
| IETF RFC 6266, Content-Disposition in HTTP (rfc-editor.org/rfc/rfc6266), read 2026-10-20 | IETF Trust document, facts only | Attachment against inline, advisory filename, last segment, reserved names, `filename*` precedence (§3.2.2) |
| WHATWG Fetch Standard, X-Content-Type-Options section, and HTML Standard file input value (fake path), read 2026-10-20 through a summarising fetcher (page slices) | CC BY 4.0 (WHATWG) | nosniff blocks wrongly typed scripts and styles only; file input value is a fake path (§3.2.2, §3.2.3, §1.1.8) |
| W3C WCAG 2.2 Understanding SC 2.5.7 Dragging Movements and SC 4.1.3 Status Messages, read 2026-10-20 | W3C document licence, facts only | Single-pointer alternative to dragging; status messages without focus move (§3.1.1, §3.1.5) |
| WHATWG HTML standard, input element `accept` attribute and the prompt to unload steps, read 2026-10-20 | CC BY 4.0 (repository licence) | `accept` is a hint; unload prompt text not customisable, conditions for showing it (§1.1.6, §2.2.7) |
| W3C File API, blob URL section, read 2026-10-20 | W3C document licence, facts only | Object URL mapping keeps the blob alive until revoked or the page goes away (§2.1.2) |
| WHATWG XMLHttpRequest standard, ProgressEvent interface, read 2026-10-20 | CC BY 4.0 (WHATWG standards, repository licence) | `loaded`, `total`, `lengthComputable` (§2.2.2) |

## Own craft, not from a source
Client against server checks, direct-to-storage grants and completion verification, chunk idempotence, previews and object URL cleanup, two-phase progress, per-file states, accessibility of the picker and drop zone, served-file isolation, test and framework-pointer lists.

## Removed
Server-side scanning products and the detail of storage vendors' multipart rules; document and spreadsheet import flows (`csv-xlsx-import-export-pitfalls`); the document-management data model, versions and folders (a sibling lot); notifications on upload completion.

## Verified on the second pass, 2026-10-20
4 verified (`accept` is a hint, object URL lifetime, progress event fields, unload prompt behaviour), 2 corrected in wording (unload prompt is not reliable and not customisable; progress total may be unknown), 0 deleted. The protocol facts were read on the first pass and not re-read. Chunking, storage and security points are design practice and stay own craft.

## Verified on the third pass, 2026-10-20
4 verified or sourced (drag alternative, status messages, Content-Disposition filename advice, fake path), 1 corrected (§3.2.3: nosniff covers script and style destinations only, so it cannot be named as the protection against a stored HTML or SVG file), 0 deleted. The File API slice, the HTML `accept` parsing text and the HTTP 413 and 415 definitions were tried and not reached (the fetched slices ended early), so those stay as before. No permissive source found for direct-to-storage grants, antivirus scanning or image-processing limits, searched: the pages above.

## Not verified
1. **Protocol facts** are the specification's claims at the commit; none was run, and the protocol has a newer draft line for resumable uploads over plain HTTP that was not read. Re-read before relying.
2. **Browser behaviour** for image orientation handling in canvas paths and thumbnail memory cost is recalled, not re-read; object URLs, progress events and the unload prompt were re-read on the second pass.
3. **Accessibility and security points** are recalled public practice, not re-read in this pass; re-read the security block for the server rules.
4. **Storage vendor limits and framework pointers** name features from memory; no version was checked.
5. **No number** (chunk size, concurrency, limits) is stated; none was measured.

Independent verification 2026-10-21: 20 checked, 20 matched, 0 corrected, 0 unverified
