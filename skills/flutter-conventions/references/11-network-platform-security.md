# flutter-conventions §11 — Network, platform and build security

> Section 11 of `skills/flutter-conventions`. Read it when an HTTP client is configured, a link or an intent
> enters the app, a web view is embedded, a platform manifest or property list is touched, or a release is
> built. Storage of tokens and permissions are §8; the background (what each class of attack is) is in
> `skills/security-hardening`. The other sections and the guardrails stay in `SKILL.md`.

1. **Traffic is encrypted, and the platform is told so.** Every endpoint is reached over TLS. On Android
   the network security configuration refuses cleartext traffic (the default for recent target versions,
   stated explicitly so it survives a change of target); on iOS the transport security settings are left at
   their default and never set to allow arbitrary loads. A cleartext exception exists for one reason and one
   host (a local development server), lives in the debug variant of the manifest or the debug build
   configuration only, and is absent from the release artefact. The check is on the built release, not on the
   source tree.
2. **Certificate validation is never disabled, in any build.** A callback that accepts every certificate
   "for the dev backend" is the most common way a development shortcut ships: it reaches the release by a
   merge, a flag left on or a copy-paste. Give the development server a certificate from a local authority
   installed on the test device, or use the platform's debug-only trust configuration. A grep for a
   permissive bad-certificate callback in the repository is a gate item.
3. **Every client has a connect timeout and a response timeout, set deliberately.** The defaults are either
   unbounded or the operating system's, and an unbounded request holds a spinner, a connection and a
   cancellable operation forever on a bad network. The values are chosen per operation class (a quick read, a
   large upload) and a timeout surfaces as its own error state (§4), not as a generic failure.
4. **Pin a certificate only where the data justifies the operational cost.** Pinning protects against a
   rogue authority; it also turns a certificate rotation into an outage for every installed version that
   cannot be updated at once. If it is adopted, pin the public key rather than the leaf certificate, carry at
   least one backup pin, ship the rotation plan with the pin, and give the pin failure its own error. For
   most applications correct validation (point 2) is the right level.
5. **Nothing compiled into the app is a secret.** A value passed at build time as a definition, or read from
   an asset, is in the binary and extractable with a string search. It is configuration (an endpoint, a
   public identifier), and it comes from a file outside version control selected per environment. A real
   credential lives on the server, and the app calls a backend that holds it; an obfuscated key is still a
   key in the package.
6. **Obfuscation raises the cost of reading the app, it does not protect a secret.** Release builds are
   obfuscated, with the debug symbols split out and kept outside version control but stored per release so
   crash reports can be symbolicated (§9). On Android, the shrinker's rules are tested on the release build:
   a rule that strips a serialised class passes in debug and fails in production on the first response that
   needs it.
7. **Deep links, intents and notification payloads are untrusted input.** Parse the incoming URI with the
   tolerant parser and treat a failure as "ignore"; compare scheme and host with an allow-list; map the path
   onto the route table rather than navigating to the path verbatim; validate every parameter's type and
   range before it reaches a query or a screen; and never trigger a destructive or paid action from the link
   alone, only open the screen that asks for confirmation. Prefer verified domain links over a custom scheme,
   since any installed app can register the same custom scheme and receive its links.
8. **A web view is a browser inside the app, and is configured as one.** Script execution is off unless the
   page needs it. Navigation is restricted to an allow-list of hosts through the navigation delegate, which
   sees redirects and sub-frame loads too, so the allow-list is checked on every request and not only on the
   first. A URL taken from a link, a push payload or user input is never loaded as is. A channel that lets
   page script call native code is a public API: it validates the message as untrusted, exposes the smallest
   capability, and is absent when no feature needs it. Credentials never travel in a URL query. The web view's
   cookies and cache are cleared at logout.
9. **Android components are private unless they have a reason.** Declare the exported attribute on every
   component (it is mandatory for components with an intent filter on recent targets), export only the
   launcher entry and the deliberate deep-link receivers, and review each intent filter, since an exported
   component with a broad filter accepts input from any app. Request only the permissions a feature uses
   (§8). Decide the backup policy explicitly: sensitive files are excluded from backup rather than inherited
   into a cloud copy.
10. **A screen showing sensitive data hides itself from capture and from the app switcher.** On Android
    the secure-window flag blocks screenshots, screen recording and the recents thumbnail; on iOS, the
    snapshot taken when the app goes inactive is replaced by a neutral overlay for those screens. Apply it
    per screen, not application-wide, so the rest of the app stays testable and shareable.
11. **Password and secret fields turn off the keyboard's learning.** A field for a password, a code or a
    token sets obscured entry and disables suggestions and autocorrection, so the keyboard does not store the
    value in its dictionary. Autofill hints are set where the platform's password manager should fill the
    field, and are absent where it should not.
12. **A biometric prompt unlocks a key, it does not return a boolean.** Code that branches on "the prompt
    succeeded" can be bypassed on a compromised device by a hook returning the boolean. Where the operation is
    sensitive, the platform keystore holds a key that is released only after the biometric check, and the
    operation needs the key. A rooted or jailbroken check is advisory and never the security boundary.
13. **Keychain entries outlive the app on iOS.** An uninstall removes the app's files and leaves its
    keychain items, so a reinstall can find a previous user's tokens. Detect the first launch after install
    (a flag in ordinary preferences, which is removed on uninstall) and clear the secure storage then.
14. **Local queries are parameterised, and a dynamic column name comes from an allow-list.** The local
    database accepts bind arguments for every value; an identifier (a sort column, a table) cannot be bound
    and is chosen from a closed set in code, never interpolated from input.
15. **Logs in a release build carry no token, no personal data and no request body.** Print statements are
    removed or routed through a logger with levels, the release level is warning or above, and the crash
    reporter's scrubbing (§9) covers what the logger would have printed. Assertions are removed in release, so
    validation never lives in an `assert`.
16. **Debug switches are compile-time constants.** Anything that bypasses authentication, shows a debug
    menu, points at a staging server or skips a check is guarded by the build mode constant (or a flavour),
    which the compiler removes from release code. A runtime flag read from storage is a switch an attacker
    can set.
17. **A package is a dependency with the app's privileges, and platform plugins run native code.** The lock
    file is committed; a new package gets a look at its maintainer, its release history, its open
    advisories and the permissions its native side declares, before it is added (`skills/security-hardening`
    §4); an abandoned plugin is replaced rather than forked in place.
18. **The release build is the artefact that is checked.** The analyser is clean, the debug banner is off,
    the manifest and property list contain the permissions, the exported components and the transport
    settings the review expects, and the symbols are archived. A security review of the source tree misses
    what a build step added.
