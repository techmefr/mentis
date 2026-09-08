# react-nextjs-conventions §9 — Security, never negotiable

> Section 9 of `skills/react-nextjs-conventions`. Read it when always, on any diff. The other sections and the guardrails stay in `SKILL.md`.

1. No secret committed. If one is, it's removed **and rotated** — dropping it from the next commit leaves it
   in the history. It also leaves it in every clone, every fork, and every CI log that echoed it, none of
   which a later commit can reach. Rotation is the only step that actually ends the exposure; the removal
   only stops it getting worse.
2. No hard-coded literal fallback on a secret env variable: fail closed, loudly, at boot. A
   `?? 'dev-secret'` is worse than a crash, because the application starts, signs tokens with a value that
   is in the repository, and looks healthy while doing it. The missing variable is a deployment problem for
   ten seconds; the fallback is a forgery problem for as long as nobody notices.
3. **A `NEXT_PUBLIC_` variable is not configuration, it is published content.** The value is inlined into
   the client bundle at build time, so it ships to every browser and lives in every cached asset; prefixing
   a key to "make it work in the component" hands it out permanently. Anything the browser must not have
   stays unprefixed and is read on the server — which is also the reason a server-only secret must never be
   referenced from a file that a Client Component imports, since the import graph decides what gets bundled.
4. `eval()`/`new Function()` on an untrusted string is forbidden: `JSON.parse` for data. The reason to state
   it as an absolute is that the untrusted input is rarely obvious at the call site — it arrives through a
   config field, a URL parameter or a saved template, three frames away from the evaluation, and the
   reviewer reading the evaluation cannot see it.
5. **`dangerouslySetInnerHTML` is the XSS surface, and it does not care where the string came from.** Any
   value on that prop is sanitised with a real library and an allowlist, on the server, before it reaches
   the component — not with a regex, and not by trusting that the field is "only ever written by an admin".
   Stored XSS is the version that hurts: the payload is saved once and executes in every future reader's
   session, with their cookies and their permissions.
6. **A URL from data can be a scheme.** `href={item.url}` accepts `javascript:` and `data:` as readily as
   `https:`, so a link whose target is user-supplied is a click away from executing script in the origin.
   Validate the scheme against an allowlist before rendering, and treat the same rule as applying to
   `src`, `action`, and anything the browser will dereference.
7. JWT: pin the expected algorithm (`{ algorithms: ['RS256'] }`), never accept `none`. Verification that
   trusts the token's own header lets the attacker choose how their token is checked, which is not
   verification.
8. **Never read identity or entitlement from anything the client can set** — a header, a query parameter, a
   field in the request body, a value in `localStorage`. The user id comes from the verified session on the
   server. This is the single most common authorisation hole in a React codebase, because the client already
   has the id in hand and passing it along feels like plumbing rather than a decision.
9. **A client-side check hides a control; it does not protect anything.** Conditioning a button on a role is
   good UX and no defence: the request can be replayed by hand, and the bundle containing the condition is
   readable. Every gate exists on the server too, in the route handler or the Server Action (§7.13), and the
   client version is a convenience layered on top of it.
10. **Everything a Server Component returns to a Client Component is serialised into the HTML payload.**
    Passing a whole model row down as a prop ships every column it has — password hash, internal notes,
    another tenant's identifier — to the browser, visible in view-source even though no UI renders it.
    Select the fields the component needs, at the query, not at the JSX.
11. **A route handler authenticated only by a cookie needs an origin check.** Server Actions carry that
    protection; a hand-written `POST` in `route.ts` does not get it for free, so a form on another site can
    submit to it with the user's session attached. Verify the `Origin` header against an allowlist, or use
    the framework's own action mechanism instead of rebuilding it.
12. **A redirect target taken from `searchParams` is an open redirect.** `?next=` sent to a domain that
    isn't yours turns your login flow into a credible phishing page, and any token in the URL or the
    referrer goes with it. Allowlist the destination, or accept only a path and reject anything with a
    scheme or a host.
13. **What comes back on the error path is part of the attack surface.** A returned stack trace, an ORM
    message with a table name, or a distinguishable "no such user" versus "wrong password" each hand over
    structure for free. The user gets one sentence they can act on; the detail goes to the log.
14. A shell command: never string interpolation, arguments as an array, a strict allowlist. Interpolation is
    what turns a filename field into a command, and the array form removes the shell from the path
    entirely rather than trying to escape it.
15. Never an auth token in `localStorage`/`sessionStorage`: an `HttpOnly`, `Secure`, `SameSite` cookie set
    server-side is the only sane option. Storage is readable by any script running on the origin, so a
    single XSS — or a single compromised dependency (point 16) — exfiltrates a long-lived credential rather
    than being confined to what it can do while the page is open.
16. **A dependency is code running with your privileges.** Adding a package for one helper function also
    adds its transitive tree, its install scripts and whoever now maintains it. Prefer the platform, pin the
    lockfile, and treat an unexplained dependency in a diff as a question rather than a detail.
