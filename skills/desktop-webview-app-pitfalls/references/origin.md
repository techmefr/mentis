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

## Removed (stated in the sources, not carried)
- Every configuration sample, command line and code sample, and the full key and file naming of update bundles.
- Checklist items 8 to 20 of the Electron security page beyond what its headings state (webview options, experimental features, ASAR specifics, file protocol detail): headings only were used; the list was not re-derived from the full text.
- Mobile capability examples, plugin authoring, the pages on lifecycle, ecosystem and future of the Tauri security section.
- Store-specific signing (Mac App Store, Windows Store) and the Windows certificate vendor steps.

## Not verified
1. **Electron items 8 to 20** are cited from the checklist headings and the author's own knowledge, labelled where so; their sections were not read in full.
2. **Version numbers** for defaults (Node integration off since 5, context isolation since 12, sandbox since 20) are the page's statements at the commit.
3. **Tauri major version.** The pages read describe the version-2 capability model; a version-1 project uses an allowlist model that this block does not cover.
4. **Own guidance, labelled in the text:** argument validation, secure storage, signing in CI, artifact verification, rollback by higher version, every "Checks" section.
5. **No command, key or configuration was executed.**

## Related blocks
`csp-and-sanitiser-pitfalls`, `security-hardening`, `rust-async-unsafe-pitfalls`, `package-manager-supply-chain-pitfalls`,
`mobile-release`, `source-freshness`.
