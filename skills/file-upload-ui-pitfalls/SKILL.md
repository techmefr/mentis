---
name: file-upload-ui-pitfalls
description: "Use when a file upload control, drop zone, avatar or attachment uploader, or large-file upload is written or reviewed in a business application, whatever the framework: size and type checks on the client against the server, chunked and resumable uploads (offset, resume after a lost connection, expiry, integrity), direct-to-storage against through-the-server, previews and object URL cleanup, progress and cancel, multiple files and concurrency, error and retry states, accessibility of the picker and drop zone, and the security rules for what is accepted and served back, plus the tests that catch them."
---

# file-upload-ui-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the control where the browser, the network and untrusted bytes all meet. The
premise: **an upload that works on a small file on office wifi is the demo; the real cases are the 2 GB file on a train, the
file renamed to look like an image, the second click, and the user who cannot drag anything**. The client checks are for
speed and kindness, the server checks are for safety, and they must not be confused. The deeper server-side rules for what
is accepted and served back are in `security-hardening` §4; spreadsheet imports are in `csv-xlsx-import-export-pitfalls`;
job handling after the upload is in `background-jobs-conventions`; semantics are in `accessibility`.

## When
- A picker, drop zone, avatar, attachment list or document uploader is built or reviewed.
- Files can be large, many at once, or uploaded over unreliable networks.
- A user reports "it stuck at 99 percent", "it restarted from zero", "it accepted a wrong file", "I cannot attach with a keyboard".

**Skip when** a part does not exist: if the project has no file upload, say "not applicable: no upload"; if it only sends small images from the client in one request, §1.3 to §1.5 (chunking, resume, integrity) are "not applicable: single small request", while §1.1, §2.1, §3.1 and §3.2 still apply, because the served-content and keyboard checks matter most for the simplest uploader. Say "not applicable: reason" rather than invent a finding.

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Client and server checks, direct-to-storage, chunking, resumable protocols, integrity, expiry and cleanup | uploads are validated, large, or must survive bad networks | [`01-checks-chunking-resume.md`](./references/01-checks-chunking-resume.md) |
| 2 | Previews, progress, cancel, multiple files, concurrency, error and retry states | any upload state or preview is written | [`02-previews-progress-states.md`](./references/02-previews-progress-states.md) |
| 3 | Accessibility, security of accepted and served files, tests, framework pointers | an uploader ships or is reviewed | [`03-access-security-tests.md`](./references/03-access-security-tests.md) |

## Output / checkpoint
A change is done when: the server validates everything the client pre-checks; large files are chunked or sent directly
with a resume path; every upload has progress, cancel and a distinct failure state; the picker is keyboard operable with
a name and a status announcement; served files cannot run in the site's origin; and the tests in §3.4 exist. No
checkpoint is written: a craft block, 🟡, nothing here was run in an application.

## Guardrails
- Validate size, type and content on the server (§1.1). Never rely on the `accept` attribute or the file extension.
- Resume from the offset the server reports (§1.4). Never restart a failed large upload from byte zero.
- Revoke every object URL and release every preview (§2.1). Never leak a blob per selected file.
- Give every file its own status and cancel (§2.3). Never show one blended progress bar that hides a failure.
- Make the picker a real button with a status message (§3.1). Never ship a drop zone that only a pointer can use.
- Serve uploads from a separate origin or as attachments (§3.2). Never serve user files from the application origin with a guessed type.
- Facts about a protocol or library are for the commit stamped in `references/origin.md`; re-read before relying.

## Origin
Own craft knowledge, with the resumable upload facts re-read in the tus protocol specification (MIT, read 2026-10-20), and on a third pass the drag, status-message, filename-header and nosniff facts re-read in WCAG 2.2, RFC 6266 and the Fetch Standard (credited in origin.md).
Details in [`references/origin.md`](./references/origin.md).
