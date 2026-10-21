# file-upload-ui-pitfalls §3 — Accessibility, security and tests

Sources: own craft, except the points credited in place: WCAG 2.2 Understanding SC 2.5.7 and SC 4.1.3, RFC 6266 and the Fetch Standard nosniff section (all read 2026-10-20, facts only, own words; see origin.md). Other accessibility points are public practice, recalled and not re-read in this pass.

## 3.1 Accessibility
1. **Symptom: the drop zone cannot be reached or used without a pointer.** Drag and drop is never the only route (`accessibility` §1); every operation needs a keyboard equivalent. WCAG 2.2 SC 2.5.7 asks that any function using a dragging movement also work with a single pointer without dragging (a click-to-browse button does); keyboard access is judged separately and does not satisfy it. The page does not name file upload, so applying it to a drop zone is our reading.
2. **The primary control is a real button or a file input with a visible label** ("Choose files"), focusable and activated with Enter and Space. The drop zone is an extra, not a replacement.
3. **Do not hide the native input with `display: none` and rely on a click proxy that is not focusable.** Visually hide it in a way that keeps it in the accessibility tree, or use a button that opens the picker; keep a visible focus ring (`a11y-hiding-and-tables-pitfalls`). Check by search: a file input with the hidden attribute (or display none) inside a label or behind a styled element that has no tab stop; the picker is then unreachable by Tab and cannot be opened with Enter or Space. Fix: a real button that calls the picker, or an input hidden by visually-hidden styles that keeps focus and shows the focus ring on its label.
4. **Label the control and state the constraints in text associated with it** (types, size, count), through an accessible description, not only a tooltip or an icon.
5. **Announce changes in a status region** (WCAG 4.1.3: results and progress messages must be exposed without moving focus; a progress message can use a log or status role): "3 files added", "report.pdf uploaded", "scan.png failed: file too large". Do not announce every percentage tick.
6. **Progress uses a progress element or an equivalent role with name, value and range,** updated at a calm rate; the text beside it carries the status.
7. **Each file row is a list item with its name, size, status, and buttons named for the file** ("Remove report.pdf", "Retry scan.png"), not "Remove" repeated.
8. **After removing a file, move focus to a sensible place** (the next row, or the add button), not the document start.
9. **Status is not colour only:** failed and done rows carry an icon and text, with sufficient contrast in light and dark themes (`accessibility` §3).
10. **The drag-over highlight is not the only cue;** the instruction text says "or drop files here", and reduced motion disables any pulsing (`accessibility` §7).
11. **Paste support** helps image workflows and keyboard users; announce it in the instruction text.
12. **A camera or mobile picker is a different permission path;** explain why access is requested at the moment of use and handle refusal with text.

## 3.2 Security of accepted and served files
1. **The detailed rules are in `security-hardening` §4;** this section lists the interface-side items that people forget.
2. **Generate the storage name on the server** and keep the original name only as display metadata, escaped on output and cleaned in the `Content-Disposition` header. Never join a client name into a path. RFC 6266 calls the disposition filename advisory only: the receiver should keep the last path segment, strip control characters and edges of whitespace, and avoid reserved names such as dot, double dot or tilde; a `filename*` parameter carries non-Latin-1 characters and wins over a plain `filename` when both are sent. The HTML Standard adds that a file input's `value` shows a fake path prefix plus the first name, so never expect a real client path.
3. **Serve user files from a separate origin or with `Content-Disposition: attachment`** and a content type fixed by the server after inspection, plus `X-Content-Type-Options: nosniff` as a second layer only: the Fetch Standard applies it to script and style destinations (a response with a wrong type is blocked there), and allows other destinations, so it does not stop a stored HTML or SVG file being opened as a page; the attachment disposition, the isolated origin and the server-fixed type do that. An uploaded HTML or SVG file on the application origin is a stored script. Check by search, in this order: the content type the download route sends (is it the stored client-declared value replayed as is?), whether a nosniff header and a content-security policy are set anywhere, whether a download disposition is set, and whether the storage origin differs from the application origin. A route that replays a declared type with a long immutable cache lifetime and no disposition serves a stored script to every reader. Re-encoding images on the client is not a control, since the server receives whatever a script sends.
4. **SVG, HTML and PDF are active formats:** refuse them for avatars, re-encode, or serve only as downloads from the isolated origin.
5. **Image processing is an attack surface:** limit decoded dimensions and memory before decoding, process in an isolated worker, and re-encode to drop embedded payloads and metadata.
6. **Archives can be bombs and path traversals:** if you unpack, limit total size, entry count and depth, and reject entries with absolute or parent paths.
7. **Authorize downloads per file and per user,** using the record's permissions; a guessable or permanent URL is a leak (`field-and-row-permission-ui-api-pitfalls`). Signed, expiring links for private files.
8. **Rate-limit and size-limit the upload endpoint,** and authenticate it; an anonymous endpoint with no limit is storage for strangers.
9. **Scan when files cross users** and keep unscanned files unreachable until the result.
10. **Do not trust the client for the chunk sequence:** a malicious client can send out of order, overlapping or oversized chunks; the server validates offsets and totals.
11. **Log the upload event, not the content,** and never log signed URLs.
12. **Personal data in files** (identity documents, medical files) follows the product's retention and encryption rules; say in the interface how long files are kept.

## 3.3 Where the logic lives
1. **Keep upload logic out of the page component:** one module owns the queue, concurrency, retry and resume, and the component renders its state, which keeps the states of §2 testable.
2. **The same module serves every uploader in the product,** so avatars, attachments and imports share limits, messages and accessibility behaviour.
3. **Surface the module's state as data** (a list of items with status and progress), not as callbacks that each screen reinterprets.

## 3.4 Tests
1. **Server validation tests:** an executable renamed to an image, an oversize body, a zero-byte file, a path-like name, an unknown type; each refused with a clear error.
2. **A limits contract test:** the client reads the server's limits; changing the server value changes the client message with no code change.
3. **Resume test:** interrupt a large upload, resume from the reported offset, and compare the final checksum with the source; also an expired upload.
4. **Idempotence test:** the same chunk sent twice leaves the file correct.
5. **Component tests for states:** each failure in §2.4, cancel, retry, partial success, the processing phase.
6. **Cleanup test:** abandoned and cancelled uploads leave nothing after the job.
7. **Keyboard test:** choose, remove and retry with the keyboard only; the live region text; focus after removal.
8. **Preview leak test:** adding and removing many files leaves no object URLs (spy on create and revoke).
9. **Serving test:** an uploaded HTML or SVG file downloads or renders inert, with the expected headers.
10. **Slow-network test in a real browser** with throttling, and a large-file test in the project's own environment; do not trust a number from another setup.

## 3.5 Framework pointers
1. **Uppy** (modular, with resumable and multipart storage plugins) and **tus-js-client** are client libraries for the flows above; the tus protocol has server implementations in several languages. Re-read their documentation for the version in use; none was run here.
2. **Laravel** can validate size and MIME type from content on the request, store to a disk (local or S3-compatible) and generate temporary signed URLs; large uploads need the web server and PHP limits raised together, and a chunked or direct path for the biggest files.
3. **Livewire's** temporary upload and **Vuetify's** file input handle the pick and the simple case; the states in §2 and the limits in §1 remain your work.
4. **Object storage** services expose multipart upload and signed policies with conditions (key prefix, maximum size, content type); use the conditions.
5. **Nuxt and similar** server routes can stream a body to storage without buffering; check the platform's request size and time limits.

## Checks
- Every item in §3.4 exists or is listed as a gap in the review.
- A keyboard-only user can attach, remove and retry, and a screen reader announces each outcome.
- An uploaded SVG cannot run script on the application origin.
