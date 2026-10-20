# file-upload-ui-pitfalls §2 — Previews, progress and states

Sources: own craft; no source text taken.

## 2.1 Previews
1. **Symptom: the page gets slower with every file picked, and memory climbs.** Cause: an object URL created for each preview and never released.
2. **Create a preview with an object URL and revoke it** when the item is removed, replaced or the component is destroyed, and after the image has loaded when the preview is transient.
3. **Do not read the whole file as a data URL for a preview;** it doubles memory and blocks the thread for large files.
4. **Downscale before showing a large image** (a thumbnail through a canvas or a bitmap), or generate thumbnails on the server after upload; a 40 MB photo in a 64 px preview is waste.
5. **Previews apply the image's orientation metadata,** or photos from phones appear rotated; modern browsers handle it for display, canvas paths may not. Test with a phone photo.
6. **A preview is not proof of a valid file.** A file can preview and still fail server checks; the status comes from the server (§2.3).
7. **For non-images show an icon, name and size,** not a blank box; for documents, a server-generated first-page thumbnail if useful.
8. **Strip or warn about metadata when privacy matters** (location in photos); the server may re-encode avatars to drop it and to normalize format.
9. **An avatar needs a crop or a fixed ratio,** done client-side for feedback and finalized on the server.

## 2.2 Progress
1. **Symptom: a bar that jumps to 100 percent and then waits.** Cause: the bar measures bytes sent from the browser, while the server still stores, scans and processes. Show two phases: "Uploading" and "Processing".
2. **Upload progress events measure bytes sent, not bytes stored.** The authoritative end is the server's reply.
3. **Show text with the bar:** percentage or "12 MB of 80 MB", and, for long uploads, time left with a modest claim (an estimate smoothed over several seconds, not a flickering number).
4. **An indeterminate state is honest when the size is unknown,** a spinner with text, never a fake bar.
5. **Progress is a labelled element with current value and range** for assistive technology (§3.1), not an image of a bar.
6. **Do not block the whole page on one upload;** let the user continue and keep a visible tray of uploads in progress, which survives route changes in a single-page app.
7. **Warn before leaving with uploads running** (a page-unload prompt) when resume is not persisted (§1.4.4).

## 2.3 Multiple files and concurrency
1. **Symptom: one failure hides among twenty successes.** Cause: a single aggregate bar. Give every file its row: name, size, status, progress, cancel, retry.
2. **Limit concurrency** (a small number of parallel uploads) so a slow network does not stall every file at once; a queue shows "waiting".
3. **Order and identity:** key rows by a client-generated id, not by name (two files may share a name) and not by index (removal shifts them).
4. **Each file has independent outcome:** done, failed with a reason, cancelled. The summary says "18 uploaded, 2 failed" and offers "Retry failed".
5. **Cancelling aborts the request and, for resumable uploads, deletes the partial upload** (§1.4.8); the row shows cancelled, not a silent removal.
6. **A form with an uploader submits only when uploads are ready,** or submits references to completed uploads; never the raw files twice. If the form is long, the uploader state persists across steps (`long-and-multistep-form-pitfalls`).
7. **Total and per-file limits both exist:** state both ("up to 10 files, 25 MB each") before selection.
8. **Replace, add and remove are different actions** in a single-file field (avatar): replacing keeps the old file until the new one is ready.
9. **A batch must not lose its finished files on one failure.** Symptom: files are uploaded one after another inside one try block, so the first failure aborts the rest and the already-uploaded files are dropped. Check where the error handler sits: it belongs per file, with the batch continuing and the outcome of each reported (item 4).

## 2.4 Error and retry states
1. **Render each failure differently:** rejected before upload (type, size), network lost (retrying, paused), server refused (permission, quota, scan failed), server error (try again), expired (start over), cancelled by the user.
2. **A message says what happened and what to do,** per file and in plain words; never a raw status code or a generic "Upload failed".
3. **Retry is a button on the failed row and resumes when possible;** it does not re-add the file or duplicate it.
4. **Automatic retry for transient network errors only,** with backoff and a cap; permission and validation errors are not retried.
5. **Offline is a state:** pause, show "waiting for connection", resume on reconnect.
6. **A partial success is reported honestly:** the record can be saved with the files that succeeded, with the failures listed, if the product allows it; otherwise block with a count.
7. **The error message is announced** (§3.1) and focus moves to the first error when a submit is blocked (`long-and-multistep-form-pitfalls`).
8. **A server restart or deploy mid-upload** returns a retryable error; resumable uploads continue, plain ones restart, and the interface says which.

## Checks
- Selecting 50 images and removing them leaves no object URLs behind.
- A file that fails shows its own error while others finish; "Retry failed" retries only that file.
- The bar shows a processing phase after upload bytes finish.
- Cancel on a resumable upload leaves no partial object after the cleanup job.
