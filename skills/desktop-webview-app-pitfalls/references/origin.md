# desktop-webview-app-pitfalls: origin and source stamps

> Provenance of `skills/desktop-webview-app-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from official documentation, never run by us: no app was built, signed, packaged or
updated while writing it.

## Sources (read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| electron/electron at commit efd4495: `docs/tutorial/security.md` (checklist and the first seven items in full), `fuses.md`, `asar-integrity.md` (headings), `code-signing.md` (headings), `updates.md` | MIT, Copyright (c) Electron contributors and GitHub Inc. (`LICENSE` read 2026-10-20) | Process-model defaults and their versions, bridge and sender checks, permission handler default, CSP, navigation and opener items, fuses and their order relative to signing, signing and notarization existence, update formats |
| tauri-apps/tauri-docs at commit b9dd703: `src/content/docs/security/` (capabilities, scope, runtime-authority, csp), `plugin/updater.mdx` | MIT, Copyright (c) 2020-2023 Tauri Programme within the Commons Conservancy (`LICENSE` read 2026-10-20) | Capability files and merging, default command exposure, scopes and deny-wins, remote capability caveat, CSP behaviour, updater signature, key custody, endpoint rules, Windows quit |
| tauri-apps/tauri-docs at b9dd703: `security/index.mdx`, `security/permissions.mdx`, `develop/calling-rust.mdx` (opened to locate a claim, none found there), and the live capabilities and release-notes pages (v2.tauri.app, 2.11.1 entry) | MIT (same file); release notes are product documentation, facts only | Default command exposure and manifest restriction and the "does not protect against" list are in `security/capabilities.mdx` (read again at the commit); remote-origin permission-check fix in 2.11.1 |
| electron/electron at efd4495: `docs/tutorial/code-signing.md` (read in full 2026-10-20) | MIT (same file) | Signing and notarization prerequisites, Windows certificate kinds and key custody |
| Electron documentation pages: security checklist, ASAR integrity | product documentation, facts only, rewritten, read 2026-10-20 | Items 8-20 summary, integrity platform versions and header hash |

## Removed (stated in the sources, not carried)
- Every configuration sample, command line and code sample, and the full key and file naming of update bundles.
- Checklist items 8 to 20 of the Electron security page beyond what its headings state (webview options, experimental features, ASAR specifics, file protocol detail): headings only were used; the list was not re-derived from the full text.
- Mobile capability examples, plugin authoring, the pages on lifecycle, ecosystem and future of the Tauri security section.
- Store-specific signing (Mac App Store, Windows Store) and the Windows certificate vendor steps.

## Not verified
1. **Electron checklist** re-opened 2026-10-20 at the commit, source file read in full: 20 items confirmed, including web view, navigation, sender validation, experimental features, current version, file addresses and fuses. Added: header-versus-meta policy delivery, null sender frame.
2. **Version numbers** re-confirmed in the file: Node integration off since 5.0.0, context isolation default since 12.0.0, sandbox default since 20.0.0 (and disabling context isolation disables the sandbox); ASAR integrity needs Electron 16 on macOS and 30 on Windows, and the packaging tools set the hash up automatically from named minimum versions (not carried). Fuse file (order before signing, run-as-Node, cookie encryption one-way, two ASAR fuses) and updates file (two server formats, 204 on macOS) re-read and confirmed.
3. **Tauri major version.** The pages read describe the capability model and link to 2.0.0 API docs without stating a major version; a version-1 project uses an allowlist model that this block does not cover. Corrected: the "does not protect against native code" statement and the all-windows default come from the capabilities page, not the runtime-authority page; downgrades need a custom comparator; the Tauri page has no release-channel setting. The Electron updates page says nothing on downgrades or Windows quit.
4. **Own guidance, labelled in the text:** argument validation, secure storage, signing in CI, artifact verification, rollback by higher version, every "Checks" section.
5. **No command, key or configuration was executed.**

## Related blocks
`csp-and-sanitiser-pitfalls`, `security-hardening`, `rust-async-unsafe-pitfalls`, `package-manager-supply-chain-pitfalls`,
`mobile-release`, `source-freshness`.

Independent verification 2026-10-21: 30 checked, 30 matched, 0 corrected, 0 unverified
