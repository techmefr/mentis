---
name: desktop-webview-app-pitfalls
description: "Use when writing or reviewing a desktop app that shows web content in a native shell (Tauri or Electron): what the web layer may ask the native layer to do, command and window permissions, loading local versus remote content, content security policy, navigation and external links, packaging switches, code signing, and signed automatic updates."
---

# desktop-webview-app-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for apps where HTML and JavaScript run inside a native shell. The premise:
**the web page is now a client of your operating system, so every web bug is a potential local bug**: a script
injected into a page can call a native command, read a file, open a program. The shell's job is to make that
channel small and checked. Web-only hardening is in `csp-and-sanitiser-pitfalls`; Rust language traps are in
`rust-async-unsafe-pitfalls`; mobile release is in `mobile-release`.

## When
- A project has a Tauri configuration or an Electron main process, or the request names either.
- A native command, a preload bridge or a message channel between the web layer and the native layer is added or changed.
- A window loads a remote address, or a link opens something outside the app.
- A build is signed, packaged or made to update itself.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Trust boundary, permission and capability files, scopes, bridge design, sender checks, remote content, content security policy, navigation | a native command, permission or window is added or reviewed | [`01-trust-boundary-and-permissions.md`](./references/01-trust-boundary-and-permissions.md) |
| 2 | Packaging switches, storage of data, code signing and notarization, signed updates, key custody | a build is packaged, signed, released or made to update | [`02-packaging-signing-and-updates.md`](./references/02-packaging-signing-and-updates.md) |

## Output / checkpoint
Each section ends with its own checks. For a change touching this block: the list of what the web layer can call
was written down and each item justified, no window with remote content can reach file or process access, a
restrictive content policy is set, update artifacts are signed and the signing key is outside the repository and the
build log.

## Guardrails
- Give each window only the permissions it needs, and scope file and network access (§1.2). Never grant a broad permission set to every window to save time.
- Never run remote content with direct system access; load remote pages in an isolated view with the bridge reduced to a few named functions (§1.4).
- Validate the arguments of every native command as if they came from an attacker (§1.1).
- Set a content security policy and keep it restrictive (§1.5). Never load scripts from a CDN into a privileged window.
- Never open an address from untrusted content with the system handler without checking its scheme (§1.6).
- Never commit or print the update signing key, and never disable signature checks (§2.4).
- Defaults changed across major versions; facts here carry the version they were stated for, re-read before relying on one (🟡, nothing here was built or run).

## Origin
Rewritten from the Electron documentation in `electron/electron` (MIT, commit efd4495) and the `tauri-apps/tauri-docs`
repository (MIT, commit b9dd703), read 2026-10-20. Own guidance is labelled in the text. See
[`references/origin.md`](./references/origin.md).
