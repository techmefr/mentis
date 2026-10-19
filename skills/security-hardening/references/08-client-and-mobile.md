# § 8 — Client-side templates and mobile apps

> Section 8 of `skills/security-hardening`. Read it when a diff binds data into a front-end template
> in a way the framework does not escape, ships code to a browser bundle or a mobile app, or embeds a
> web view. §2 is the generic output rule; this section is where it breaks on the client, and where the
> trust boundary is a device you do not control.

## Browser templates

A component framework escapes text and ordinary attribute values for you. The vectors below are the
ones it does not, which is why a template that looks safe line by line can still be an injection.

1. **A bound URL is not escaped as a URL.** Escaping makes `javascript:...` safe as *text*; as the target
   of a link, a form action or a frame source it still runs. Any `href`, `src` or `action` fed from data
   a user influenced passes a scheme check against an allow-list first (`https`, `http`, `mailto`, `tel`
   as the product needs) and is refused otherwise; a relative path is checked to start with a single
   slash, not two. Do the check when the value is stored and again where it is bound.
2. **A dynamic component name from data is code selection.** Resolving which component to render from a
   string a user can influence lets them pick any registered component, including ones that were never
   meant to be reachable from that route. Map the value through a fixed table of permitted components and
   fall back to nothing for a key not in it.
3. **Never compile a template from data.** A runtime template compiler given a string a user influenced
   evaluates expressions in it. The template is source code; the data is a value inside it.
4. **A bound style string is an injection surface.** A raw user-supplied style can load remote resources
   and read attribute values through selectors, which exfiltrates data without a script. Bind a single
   property to a value validated against a short list or a pattern, never a free-form string.
5. **No event attribute takes data.** Binding user input into an `on*` attribute is code execution by
   another name, and under the strict policy of §6.2 it does not even work. Attach handlers in code.
6. **Raw-HTML rendering takes sanitised input, from a maintained sanitiser, with an allow-list.** Every
   framework has such a facility (§2.12). Sanitise at the point of render with a library whose job is
   exactly this, configured with an allow-list of elements and attributes, and sanitise again on the
   server before storing when you can. A render function that writes `innerHTML` is the same facility
   under a different name.
7. **A value placed in a script block or a data attribute is output for a different parser.** Embedding
   server data in the page as JSON inside a script element must escape the characters that end the
   element, and must not assemble the script by string concatenation (§2.5).
8. **Everything in the client bundle is public.** A build-time variable that the tool inlines into the
   bundle (the usual prefix convention marks which ones) is readable by anyone who loads the page, along
   with source maps if you ship them. Only values that are public by design belong there; a key that
   must stay secret stays on a server the page calls, and a source map is published deliberately or not
   at all.
9. **Tokens live where scripts cannot read them when they can.** A session identifier in an
   HTTP-only cookie survives an injected script; the same value in local storage does not. A token the
   page must hold in memory is short-lived (`auth-session-conventions`).
10. **The front end is not the enforcement point.** A hidden button, a disabled field and a client-side
    validation are experience, not control; each rule they express is enforced again on the server (§1,
    §3). A review that finds a restriction only in a component has found a missing control.

## Mobile applications

The device belongs to the user, who may be hostile, and the binary can be unpacked. The network crosses
hotspots and proxies. Both change what has to be written down.

11. **All traffic is encrypted, and the platform is told so.** The application uses secure transport for
    every endpoint, and both platforms are configured to refuse clear text rather than merely not use it:
    the Android network security configuration with cleartext disabled, the iOS transport-security
    setting with arbitrary loads off. A single development exception left in a release build is a
    downgrade path. Exceptions for local development live in debug-only configuration.
12. **Every network client sets a timeout, and a limit on what it will read.** The defaults of most
    clients wait indefinitely, which turns a slow or hostile server into a frozen application and a
    drained battery. Set connect and receive deadlines explicitly, and cap response size for anything
    that is parsed in memory (§2.11).
13. **Pin the certificate only where the data justifies the cost.** Pinning rejects a certificate issued
    by a compromised or coerced authority, and also breaks every user the day the certificate rotates
    unless a backup pin and an update path exist. Apply it to the endpoints that carry credentials or
    regulated data, pin the public key rather than the leaf certificate, ship a second pin, and have a
    way to update pins that does not require a store release.
14. **A web view is a browser you embedded, with your app's powers.** Keep script execution off unless
    the page needs it; load only URLs that pass an allow-list of hosts, decided in the navigation
    callback, never a URL that arrived from a deep link, a push payload or a server field unchecked; do
    not expose native functions to the page unless the page is yours, loaded from a pinned origin, and
    the exposed function can do nothing a hostile page should not ask for; disable file access from the
    page unless required; and treat what the page sends back as untrusted input (§1).
15. **A deep link is an input.** The scheme, host and path are validated against what the app can
    handle, a navigation target is chosen from a list and not built from the link, and any action the
    link triggers (sign in, pay, delete) asks the user to confirm, because anything on the device can
    fire the link.
16. **An exported component is an entry point.** On Android, an activity, service, receiver or content
    provider is reachable by other applications when it is exported or declares an intent filter. Export
    only the launcher entry, mark everything else as not exported explicitly, and treat each intent
    payload as input from an untrusted process (§3.10). On iOS, the same discipline applies to URL
    schemes and universal links.
17. **Keep secrets out of the binary.** A key compiled in is a key published: values supplied at build
    time are configuration, not protection. A secret the server needs stays on the server and the
    app calls an endpoint of yours; per-user credentials live in the platform's secure store (Keychain,
    Keystore-backed storage), never in plain preferences or files, and are cleared at sign-out together
    with cached personal data.
18. **Hide sensitive screens from the system.** A screen showing credentials, payment data or personal
    records is excluded from screenshots and the app-switcher snapshot (the secure-window flag on
    Android, a cover view on iOS) and leaves the clipboard alone.
19. **Obfuscation raises the cost; it is not a control.** Shrink and obfuscate release builds, keep the
    mapping and debug-symbol files out of the repository and in private storage next to the release they
    belong to (they are what makes crash reports readable and what an attacker would love to have), and
    check that the shrinker's keep rules do not retain the classes you are trying to hide. Then design as
    though the binary were readable, because it is.
20. **Ask for the permissions the feature needs, when it needs them.** Declare only what the app uses,
    request each at the moment of use with a reason the user can read, and degrade gracefully when it is
    refused (`skills/accessibility` covers the refusal path being usable).
21. **Sensitive operations re-authenticate on the device.** A biometric or passcode prompt before showing a
    stored secret or confirming a payment is checked against the platform's key store, not against a
    boolean the app keeps, since a boolean can be flipped on a compromised device.

**Checks, by command:** search templates for the raw-HTML facility, for bound `href`/`src`/`:is`/`style`
values and for `on*` bindings, and read each hit's data source; list every build-time public variable and
confirm none is a secret; in the mobile project, search the manifests for exported components and
`usesCleartextTraffic`, the transport-security settings for arbitrary loads, the code for web-view
controllers and for client constructors without a timeout.

**Sources:** the framework security guides for the front-end frameworks in use; OWASP Cheat Sheets (XSS
Prevention, DOM-based XSS, Content Security Policy, HTML5 Security, Mobile Application Security);
OWASP MASVS and MASTG (network, storage, platform, resilience); Android developer documentation (network
security configuration, exported components, secure window flag); Apple developer documentation
(App Transport Security, Keychain, URL schemes and universal links).
