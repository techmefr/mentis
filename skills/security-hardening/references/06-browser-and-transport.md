# § 6 — Browser and transport protections

> Section 6 of `skills/security-hardening`. Read it when a diff sets response headers, serves a page,
> embeds or links a third-party resource, opens a window, sets a cookie, or sends a request over a
> network the user does not control. These are the protections a browser enforces on your behalf **only
> if you ask for them**: the application code is not the last line of defence, the client is.

The specifications behind each point are named at the end of the section. The exact syntax of a header
changes more slowly than anyone remembers and faster than a copy of it in this file should be trusted:
read the current specification before writing a value you are not sure of (`skills/source-freshness`).

1. **Response headers are configuration owned by the code, not by whoever deploys it.** A header set only
   in a proxy or a CDN disappears when the app moves behind another one, and nothing in the repo says it
   was ever there. Set them in one place the application controls, test that they are present on the
   routes that matter, and keep the list short enough to be reviewed in one reading.
2. **A content security policy is an allow-list of where code may come from, and its value is what it
   forbids.** Start from a default that allows nothing but your own origin, then add the origins each
   directive needs, one by one, with a reason. A policy that allows inline scripts, or puts a bare
   wildcard in a script source, stops no injected script: it has the cost of a policy and none of the
   effect.
3. **Roll a policy out in report-only mode first.** The browser then reports violations without
   blocking, and the reports show which legitimate resources the policy would have broken. Switch to
   enforcing when the reports from real traffic are quiet, and keep a reporting endpoint afterwards,
   because the next violation is either a regression or an injection and you want to know which.
4. **A strict policy is why inline handlers and inline styles stop being acceptable.** `onclick="..."`,
   `javascript:` URLs and `style="..."` attributes are exactly what the policy refuses, so a codebase
   that wants the policy has to keep that behaviour in files. Where an inline script is unavoidable,
   authorise it by a per-response nonce or a hash of its content, never by re-allowing all inline code.
   Writing without inline code from the start is far cheaper than removing it later.
5. **Forbid the browser from guessing a content type.** The no-sniff header makes it honour the type you
   declared, which is what stops an uploaded file served as text from being run as script. It only helps
   if the declared type is correct, which is the §4.4 rule applied at the header.
6. **Decide who may frame the page, and say it.** The frame-ancestors directive of the content security
   policy is the current control and the older frame-options header is its legacy equivalent. An
   application with no reason to be embedded declares that, because a page that can be framed can be
   overlaid with an invisible frame and clicked on the victim's behalf. A page that must be embedded
   names the exact origins that may embed it.
7. **Choose a referrer policy instead of inheriting the browser default.** The referrer carries the
   address of the page the user came from to the next site, so a path containing an identifier, a
   search term or a token (which §2.9 already forbids) leaks on every outbound navigation. A policy that
   sends only the origin cross-site, or nothing, closes the leak for pages that were not written with it
   in mind.
8. **Switch off the browser features the page does not use.** The permissions policy disables powerful
   features (camera, microphone, geolocation, payment, and others) for the page and for every frame in
   it, so a compromised third-party script or an embedded widget cannot request them either. Disable by
   default, enable the one the product needs.
9. **Cross-origin isolation is a trade you make for a feature, not a hardening you apply for free.** The
   opener and embedder policies isolate the page from other origins, which some powerful APIs require,
   and they break cross-origin embeds that do not opt in. Adopt them when a feature demands it, and
   expect to audit every third-party resource the page loads.
10. **A third-party script or stylesheet is code you run with your page's authority.** Load it from your
    own origin when the licence allows. When it must come from elsewhere, pin it with a
    subresource-integrity hash of the exact bytes you reviewed, plus the cross-origin attribute the
    integrity check requires, so that a changed file on the third party's server fails to load instead
    of running. A tag with no integrity value on a mutable URL means the third party's next release
    ships to your users unreviewed.
11. **An integrity hash pins a version, so it needs a versioned URL.** A hash on an address that serves
    "the latest" turns every upstream release into a broken page, and the cheap fix is to delete the
    hash. Reference an immutable, versioned file, or host it yourself.
12. **A link that opens a new browsing context must not hand it the opener.** Current browsers treat
    `target="_blank"` links as no-opener by default, but older ones and some embedded views do not, and
    a window opened by script never did. State `rel="noopener"` on external targets so the new page
    cannot reach back through `window.opener` and navigate yours, and add `noreferrer` when the
    destination should not learn where the click came from (§6.7).
13. **Every `postMessage` listener checks who sent it.** The message event carries the sender's origin,
    and a handler that acts on the data without comparing that origin to an exact expected value takes
    commands from any page that can get a reference to the window. Compare against a literal, never
    against a substring or a pattern; when sending, name the target origin instead of the wildcard.
14. **Never serve a secure page that loads an insecure sub-resource.** A script, stylesheet, frame or
    request fetched over plain HTTP from a secure page is mixed content. Browsers block the active kinds
    and may upgrade or warn on the passive ones (image, audio, video), and either way the page loses the
    guarantee it was served with. Reference everything by a secure scheme or a relative path, and treat a
    mixed-content warning in a build as a failure.
15. **A form posts to a secure address, and a downgrade is a bug.** A page served securely whose form
    action, API endpoint or redirect points at plain HTTP sends the submitted data in the clear and
    gives an on-path attacker the chance to rewrite it. Check the action and every redirect hop, and
    make the secure-to-insecure redirect something a test would catch.
16. **A cookie states its own limits, every time.** The secure attribute keeps it off plain connections;
    the HTTP-only attribute keeps scripts from reading it; the same-site attribute decides whether it
    rides along on cross-site requests, and is a baseline CSRF defence rather than a replacement for
    tokens on state-changing requests; a host-prefixed name binds it to the exact origin and path. A
    session cookie missing any of these is a decision nobody made (`auth-session-conventions` owns the
    session itself, this is the transport half).
17. **CORS is an exception you grant, so grant the smallest one.** Name the origins that may read a
    response; never reflect the request's origin back as the allowed one; never combine a wildcard with
    credentials, which browsers refuse for a reason. A permissive policy on an authenticated endpoint
    lets any page a logged-in user visits read that user's data.
18. **A password field says what it is.** Typing it as a password hides it on screen, and the right
    autocomplete token (current or new password) lets a password manager do its job instead of the user
    reusing one memorable password. Do not block paste into it, which removes the manager too.
19. **A public form that creates records needs a cost for the abuser and an alternative for everyone
    else.** A challenge, a proof of work or a rate limit (§7.4) keeps bots from filling it. Whichever is
    chosen must stay usable by people who cannot solve a visual puzzle (`skills/accessibility`), or the
    control excludes the users it was meant to protect.
20. **Prefer fewer browser-side secrets over better-hidden ones.** Anything delivered to the page is
    readable by whoever loads it and by every script running in it. A token the front end needs is
    short-lived and scoped; the one that must never be exposed stays on a server the page calls.

**Checks, by command** (presence, never the exact value, which belongs to the specification): fetch the
headers of a representative page and look for the content security, no-sniff, framing, referrer and
permissions headers, and for the strict-transport header on the secure origin. Search the source for
`target="_blank"` without a `rel`, for `<script`/`<link` pointing at an absolute URL with no `integrity`,
for `http://` in `src`/`href`/`action` and in fetch calls, for `addEventListener("message"` (then read the
next lines for an origin comparison), and for inline `on*=` handlers and `style=` attributes that a
strict policy would refuse. Load the page in a headless browser and list the requests it made over plain
HTTP.

**Sources:** W3C Content Security Policy Level 3; W3C Referrer Policy; W3C Subresource Integrity; W3C
Permissions Policy; W3C Mixed Content; WHATWG HTML Living Standard (link types `noopener` and
`noreferrer`, cross-document messaging, cross-origin opener and embedder policies); WHATWG Fetch (CORS,
credentials, the no-sniff header); RFC 6265bis (cookies); OWASP Secure Headers, Content Security Policy
and CORS cheat sheets.
