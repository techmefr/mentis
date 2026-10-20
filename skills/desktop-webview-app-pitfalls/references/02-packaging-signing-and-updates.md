# desktop-webview-app-pitfalls §2 — Packaging, signing and updates

Sources: the Electron fuses, ASAR integrity, code signing and updates tutorials (efd4495) and the Tauri updater plugin page (b9dd703), read 2026-10-20. Points marked "own guidance" are not from a source.

## 2.1 Package-time switches (Electron)
1. **Fuses are switches inside the Electron binary, flipped when you package and before you sign,** so that the operating system's signature check stops anyone flipping them back. Disable what you do not use.
2. **The run-as-Node switch is on by default;** an app that never needs the environment variable that triggers it should turn it off, and use utility processes for separate Node work. With it off, forking a child process the old way throws.
3. **Cookie encryption is off by default and one-way:** once on, turning it off corrupts the store. On macOS it needs a signed app to reach the keychain.
4. **Integrity validation of the packed app archive and "only load the app from the archive" are separate switches** that work together; enabling them needs the header hash to be provided by your build (re-read the current requirements and supported versions).
5. **Order matters: package, flip fuses, then sign.** Signing first and flipping later breaks the signature or loses the protection (own guidance, consequence of the point above).

## 2.2 Where data and secrets live
1. **A desktop app ships its code to the user; nothing inside is secret.** An API key in the bundle is public, as for any client (own guidance). Use a server that holds the key, or a per-user token.
2. **Store user secrets with the system's secure storage facility,** not in plain files or the web layer's storage (own guidance).
3. **The webview's own profile folder holds cookies and tokens;** deny the web layer's file access to it (§1.2.5) and do not log its contents.

## 2.3 Code signing
1. **macOS apps are signed and notarized,** a separate process where the platform's automated systems check the build. The Electron docs point to the packaging tools that do both; some operating system features only work for signed apps.
2. **Windows builds are signed with a certificate or with the vendor's signing service;** the docs describe both. Unsigned installers trigger warnings and may be blocked by policy.
3. **Sign in CI with credentials stored as secrets,** from a clean checkout, and fail the build if signing does not happen (own guidance). A release that was "signed on someone's laptop" cannot be reproduced when that person is away.
4. **Verify the output, not the log** (own guidance): run the platform's signature check on the artifact before publishing.

## 2.4 Updates
1. **An update channel is a remote-code-execution channel.** Whatever feeds it must be authenticated, so sign every update and verify before install.
2. **Tauri's updater requires a signature and it cannot be switched off.** The public key goes in the configuration (the key content, not a path); the private key signs the artifacts and must never be shared. Losing the private key means installed copies cannot be updated, so back it up in a secret store.
3. **The signing key must be an environment variable of the build;** a dotenv file is not read for this. Never print it in a log.
4. **Update endpoints are secure-scheme only in production,** and the insecure-transport switch exists for tests. Leave it off in a release.
5. **The static update file and the dynamic response differ:** the dynamic server answers "no content" when there is no update; both need a version in a semantic-versioning form, per-platform URLs and the signature text (the content of the signature file, not its path).
6. **Electron's built-in updater has different server formats for macOS and Windows,** and its helper module or hosted service covers the common case. Roll your own update server only when you must, and follow the platform format to the letter.
7. **Windows installers force the app to quit before install.** Save state in the before-exit hook, and tell the user.
8. **Downgrades are refused by default;** allowing them is a deliberate comparison override. A rollback plan therefore needs a higher version number with older code (own guidance).
9. **Staged rollouts and channels are the server's job** (the Tauri page shows channel in the endpoint); decide the channel names before the first public release.

## 2.5 Checks (own guidance)
1. The build log, the repository and the artifact contain no private key and no secret.
2. The signature of each platform artifact verifies with the platform tool, and the update signature verifies with the public key in the shipped configuration.
3. An update from the previous release to the new one was run on a clean machine for each platform, including the quit-and-install path.
4. Fuses and security switches read back from the final binary match the intended list.
