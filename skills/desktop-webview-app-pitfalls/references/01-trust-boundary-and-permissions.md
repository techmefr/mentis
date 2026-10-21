# desktop-webview-app-pitfalls §1 — Trust boundary and permissions

Sources: the Electron security tutorial (docs/tutorial/security.md, efd4495) and the Tauri security pages (capabilities, scopes, runtime authority, content security policy; tauri-docs b9dd703), read 2026-10-20. Points marked "own guidance" are not from a source. Version numbers are those the sources state for defaults.

## 1.1 The web layer is a client of the system
1. **List everything the web layer can invoke natively, and justify each item.** The sources agree that the web layer must be treated as able to run attacker-chosen script (a cross-site-scripting bug, a compromised dependency, a hijacked remote page), so the native side is the real security boundary.
2. **Validate arguments in the native code of every command** (own guidance): paths, URLs, program names and sizes. A command that takes a path and reads it is a file-read endpoint for the attacker.
3. **A permission system does not protect against bugs in your own native code.** Tauri's pages say capabilities limit what the frontend can reach, not what malicious or insecure native code does once reached.
4. **Electron is not a browser:** its pages hold much greater power than a website's, and the source says showing arbitrary untrusted content is a risk the framework is not designed to handle.

## 1.2 Tauri: capabilities, permissions and scopes
1. **Capabilities bind permissions to named windows and webviews,** in files under the capabilities folder. Every file in that folder is enabled by default; once capabilities are listed explicitly in the configuration, only those are used. Know which of the two modes the project is in.
2. **A window that belongs to several capabilities gets the union of their permissions.** Adding a window to one more capability can widen it silently.
3. **Commands you register are callable from all windows by default.** Restrict them in the application manifest when some windows must not reach them.
4. **Permissions can be limited by platform.** Put desktop-only and mobile-only permissions in separate capability files.
5. **Scopes allow or deny paths, addresses or other values per command, and deny always wins.** The enforcement is inside each command: whoever writes a scoped command must make sure it cannot be bypassed (path tricks, links) and have it reviewed. Deny the webview's own data folder where it can hold sensitive values.
6. **Allowing a remote address to call commands is a deliberate exception,** by listing its URLs in a capability. On Linux and Android the framework cannot tell a request from an embedded frame from one of the window itself, so the exception is wider there than it looks.

## 1.3 Electron: process model and defaults
1. **Never run remote content with Node integration on.** An XSS then becomes remote code execution. This is the default since Electron 5; verify nobody turned it back on.
2. **Keep context isolation on in every renderer** (default since 12) and the process sandbox on (default since 20). Turning context isolation off also turns the sandbox off for that renderer, whatever else is set.
3. **Expose a small, named bridge from the preload script instead of the raw module or the channel object.** One function per action, with its own argument check, never a generic "send any message" function.
4. **Validate the sender of every message the main process receives** from a renderer: which frame and which address. A subframe or a navigated window can send from a different origin.
5. **Never disable web security or allow insecure content** in a production window; the first disables the same-origin policy and implies the second.

## 1.4 Local versus remote content
1. **Prefer local, packaged pages for anything privileged.** Use a custom protocol for them rather than file addresses, since the file scheme gives the page access patterns a custom scheme does not (Electron lists this as a recommendation).
2. **Remote pages go in an isolated view with no Node access,** and any capability you grant is per address, never "all remote pages".
3. **Load remote resources over the secure scheme only** (secure web sockets likewise).
4. **Electron approves every permission request from a page by default** (camera, notifications, and so on) unless you install a handler. Install one, deny by default, allow by exact address and permission.

## 1.5 Content security policy
1. **Set one in both frameworks, and make it restrictive:** scripts from the app itself only. In Tauri the policy is applied only when set in the configuration, and the framework adds its own hashes and nonces to bundled code.
2. **A wildcard policy is no policy.** Avoid scripts from a CDN in a privileged window: each external host is an extra way in.
3. **Frontends that use WebAssembly need the policy to allow it explicitly** (Tauri's page notes the Rust-frontend case); a blocked module looks like a build bug.

## 1.6 Navigation and external links
1. **Limit navigation and new-window creation** in Electron: handle both events, allow a list of addresses, deny the rest.
2. **Never pass untrusted text to the system opener** (`shell.openExternal` in Electron, the opener plugin in Tauri) without checking the scheme and the host. A custom scheme or a file address can start a program.
3. **Do not leave debugging switches in production:** developer tools, the Node options variable, experimental web features and the Chromium feature-enabling switch (Electron security checklist, read 2026-10-20: do not enable either without a known reason).
4. **Embedded web views (`<webview>`):** do not allow popups on them unless needed, and in the main process strip preload scripts, force Node integration off and refuse unapproved sources when one attaches. Parse addresses with the URL parser when allow-listing navigation, not with string matching. Keep Electron current and move one major version at a time, reading the breaking-changes list (same checklist).

## 1.7 Checks (own guidance)
1. Produce the table: window or webview, content origin (local or remote), permissions or bridge functions, scope. Any remote origin with a file, process or shell entry is a finding.
2. In a test window, open the developer console and try to call a native command that window should not reach; it must be refused.
3. Search the sources for node integration enabled, context isolation disabled, sandbox disabled, a wildcard policy, and a generic message-forwarding function.
