# file-upload-ui-pitfalls §1 — Checks, chunking and resuming

Sources: tus resumable upload protocol 1.0.0 (MIT, commit stamped in origin.md, read 2026-10-20) for the facts marked as such; the rest is own craft.

## 1.1 Client checks against server checks
1. **Symptom: a user waits ten minutes for a 3 GB file and is then told it is too big.** Cause: no client check. The fix is a check at selection time.
2. **The client check is a courtesy: size, count, a type hint, image dimensions.** It saves time and gives a precise message before any byte moves.
3. **Symptom: a script file renamed `photo.jpg` is stored and served.** Cause: trusting the extension, the `accept` attribute or the client-supplied content type. All three are chosen by the sender.
4. **The server is the authority:** it enforces the maximum size while reading (not after buffering), inspects the content to decide the type, checks dimensions and decoded size for images and archives, and applies the same limits the client displayed (`security-hardening` §4).
5. **One source for the limits.** The server exposes allowed types and the size cap, and the client reads them; two hard-coded copies drift, and the client then rejects what the server accepts or the reverse.
6. **The `accept` attribute only filters the picker dialog.** A drop, a paste and a script bypass it; re-check on drop and paste.
7. **Reject early with a message per file:** which file, which rule, what is allowed ("report.exe: this type is not allowed, use PDF, DOCX or PNG"). Keep the other valid files.
8. **Zero-byte files, duplicate names and very long names are cases:** decide the rule, test it, and never use the client name as a storage path.
9. **An allow-list by type prefix is not an allow-list.** Symptom: the server accepts any type that starts with `image/`, which includes the vector format that can carry script, and the type is the one the client declared. Check: grep the upload handler for a prefix test on the declared type; replace it with an explicit list of types, decided after inspecting the bytes, and see §3.2.3 for how they are served.
10. **A limit that truncates silently is a defect.** Symptom: a picker keeps only the first N selected files and says nothing. Say the limit before selection and name the files that were dropped.
11. **Quota is a server rule too:** per user, per record and in total, refused with a clear message, and shown before upload where cheap.

## 1.2 Through the server or direct to storage
1. **Through the application server is simplest and keeps one control point,** but it ties up workers for the whole transfer and hits request size and timeout limits of proxies.
2. **Direct to object storage with a short-lived signed URL moves the bytes off your servers.** The server issues the grant: allowed key, maximum size, content type condition and a short expiry, scoped to one object and one user.
3. **A direct upload needs a completion step:** the client tells the application the object exists, and the server then verifies it (size, type by content, scan) before the record becomes visible. Symptom otherwise: records pointing at missing or unchecked objects.
4. **Never put storage credentials in the browser,** only signed, scoped, expiring grants; and never let the client pick the destination key.
5. **Configure storage cross-origin rules narrowly** (the application origin, the needed methods) and test the pre-flight, a common reason a direct upload works locally and fails in production.
6. **Files stored in the database** (a binary column, chunks reassembled by a query) need the same limits as any other store: a maximum size enforced while reading, memory bounded when assembling or serving, and a note on backup size; check that assembling a chunked upload does not hold the whole file in one string or buffer.
7. **Unreferenced objects accumulate:** upload then abandon leaves orphans. Use a pending state and a cleanup job (§1.6, `background-jobs-conventions`).

## 1.3 Chunking
1. **Symptom: uploads of large files fail with gateway timeouts or request-too-large errors.** Cause: one request for the whole file crossing a proxy or platform limit.
2. **Split the file into ranges with `Blob.slice` and send each as its own request,** with the index, the total size and the offset. Choose a size big enough to limit request overhead and small enough to retry cheaply; measure on real networks rather than copying a number.
3. **Many storage services have their own multipart rules** (minimum part size except the last, a maximum number of parts, a final "complete" call listing parts). Read the service's rules; do not assume your chunk size fits.
4. **Send chunks sequentially or with a small concurrency,** and make the server accept a chunk idempotently by offset, so a retried chunk does not corrupt the file.
5. **Do not hold the whole file in memory** in the client or the server; stream or slice.
6. **The final assemble step is atomic:** the file becomes visible only when all bytes are present and checked.
7. **A chunk request carries authentication and the CSRF protection the application uses,** like any other write.

## 1.4 Resumable uploads
1. **Symptom: a lost connection at 99 percent restarts from zero.** Cause: the client has no way to ask how much arrived.
2. **A resumable protocol asks the server for the current offset, then continues from it.** In the tus protocol a HEAD request on the upload URL returns an `Upload-Offset` header, and a PATCH with the same offset in `Upload-Offset` and a content type of `application/offset+octet-stream` sends the rest; the server answers with the new offset.
3. **Create the upload first:** the creation extension of that protocol is a POST declaring the total length (or deferring it) and returning the upload URL in a `Location` header; the client keeps that URL and resumes against it.
4. **Persist the upload URL on the client** (local storage or the record), so a reload or a new tab can resume. Without it resumption works only inside one page life.
5. **An unknown or expired upload answers 404 or 410,** so the client starts a new upload instead of looping. In tus the expiration extension adds an `Upload-Expires` header with an HTTP date; surface the deadline to the application and clean up after it.
6. **A server advertises its limits** (the protocol has a maximum size header and a version negotiation that answers 412 for an unsupported version); read them instead of guessing.
7. **Integrity:** a checksum extension lets a client send a digest with a chunk; the server answers a specific 460 status when it mismatches, and the client resends that chunk. Use a checksum for large or valuable files, and still verify the whole file at the end.
8. **Termination:** the client can delete an unfinished upload to free storage when the user cancels; offer it, and clean up server-side anyway.
9. **Concatenation** (partial uploads joined into one) allows parallel parts; it adds complexity, so use it only if sequential chunks are too slow.
10. **Reuse a protocol and an existing client library instead of writing your own;** the details (offset races, retries, expiry) are where hand-written ones fail. Pin the library and re-read its notes on upgrade.
11. **Retries use backoff and a cap:** network failures retry quietly a few times, then show an error with a retry button (§2.4).
12. **A paused upload is a state:** the user can pause, resume and see "waiting for connection" when offline, rather than an error.

## 1.5 Integrity and duplicates
1. **Compute the size on the client and compare it with the stored size** at completion; a mismatch is a failed upload, not a partial success.
2. **A content hash of the finished file lets the server detect duplicates** and avoid storing twice; decide whether a duplicate is refused, linked or kept, and say it.
3. **The same file chosen twice is a user error to handle:** a duplicate notice, not two silent copies.
4. **A file changed on disk during upload** can produce a corrupt result; compare size and modification time before each chunk when the platform exposes them, and fail with a clear message.

## 1.6 Lifetime and cleanup
1. **Every upload has a pending, ready, rejected and deleted state;** only ready files are linked and served.
2. **Abandoned uploads expire** (the expiry above) and a scheduled job removes the object and its record.
3. **Deleting a record deletes its files,** or queues it, with the same permission check as viewing.
4. **Scan before ready** when the files are shared with others (an antivirus or content scanner step), with the file held in a quarantined state until the result.

## Checks
- A client limit change is read from the server; no hard-coded duplicate exists.
- Renaming an executable to an image extension is refused by the server.
- Killing the network at 70 percent and restoring it resumes from the reported offset, and a reload resumes from the stored URL.
- An expired upload URL leads to a new upload, not a loop.
