# auth-gateway-proxy-pitfalls §2 — Routes, flags and cookies

> Section 2 of `skills/auth-gateway-proxy-pitfalls`. Read it when an authentication exemption, a redirect
> allow-list, a provider flag, the cookie secret or a refresh interval changes. Flag names are
> oauth2-proxy's, at the commit in `references/origin.md`.

1. **An exemption matches the decoded path, and ambiguous paths get none.** `--skip-auth-route` (and the
   deprecated `--skip-auth-regex`) match the percent-decoded path without the query string, after a single
   decoding pass; there is no recursive decoding. Before any pattern or negated pattern is evaluated, the
   documentation says exemptions are declined for malformed escapes, `.` or `..` segments, repeated slashes
   (including a leading `//`), semicolons, backslashes, fragment-like `#` content, decoded `?`, and control
   characters. That covers valid-looking paths such as `/public/file;version=1` and `/public//file`, which
   now need normal authentication. A declined exemption falls back to normal authentication; it is not an
   unconditional refusal. Write exemptions for plain paths and expect the odd ones to be challenged.
2. **Trailing slashes are significant.** The documentation says `/public` and `/public/` are distinct
   matching paths. Anchor patterns (`^/public/`) and state the form you mean; an unanchored pattern
   exempts more than it reads like. The documented rule format takes an optional method, so add one (`GET=^/health$`) so a write
   to an exempt path still needs a session.
3. **Weakening flags stay off.** The ones the documentation marks insecure or that turn verification off:
   `--insecure-oidc-allow-unverified-email`, `--insecure-oidc-skip-issuer-verification`,
   `--insecure-oidc-skip-nonce` (listed with default true, so set it deliberately), `--ssl-insecure-skip-verify`
   for provider TLS, `--ssl-upstream-insecure-skip-verify` for upstream TLS and `--redis-insecure-skip-tls-verify`
   for the session store. Where a provider forces one, the reason, the scope and the date to revisit
   go next to the setting. The generic client-side reasoning is `skills/oauth-oidc-client-pitfalls` §2.7.
4. **Pin the signing algorithms and the audience.** `--oidc-enabled-signing-alg` limits the accepted JWT
   algorithms (with discovery, the effective set is the intersection with what the provider advertises) and
   `--oidc-extra-audience` widens the accepted audiences, so every entry in it is a client you trust.
   `skills/jwt-verification` explains why both are pinned.
5. **A bearer-token bypass is also an exemption.** `--skip-jwt-bearer-tokens` lets a request with a verified
   JWT skip the login redirect; the token needs an audience matching the client ID or one of the extra
   issuer-audience pairs in `--extra-jwt-issuers`. By default an invalid token falls back to a login
   redirect, and `--bearer-token-login-fallback=false` answers 403 instead. For routes that are APIs,
   `--api-route` answers 401 rather than redirecting. Choose the answer on purpose, and keep the extra
   issuers list to issuers you control.
6. **A leading dot in the redirect allow-list opens every subdomain.** For `--whitelist-domain`, the
   documentation says a domain prefixed with `.` or `*.` allows any subdomain as a post-login redirect
   target, and that only an empty port (the protocol's default) is allowed unless you add a port or `*`
   (`example.com:*`). List exact hosts. A subdomain that any customer can create or take over is an open
   redirect with your login behind it.
7. **The cookie secret is mandatory and random.** With the cookie session store, the documentation says it
   is mandatory to set `--cookie-secret`, which ensures the session data is encrypted in the cookie. The
   secret file must be raw bytes of exactly 16, 24 or 32 bytes and the documented commands generate one
   from a cryptographically secure source; generate it, do not type it, and keep it out of the repository
   (`skills/security-hardening` §4.2). Cookie defaults worth checking, not assuming: `Secure` and
   `HttpOnly` are true, expiry 168 hours, `SameSite` empty. With `Secure` set, use a `__Host-` or
   `__Secure-` cookie name.
8. **A cookie store puts the session in every request, and cannot lock.** The documentation notes that
   concurrent requests can conflict while a session is refreshed and force a new login, and that the
   Redis store sends only a ticket, with each session encrypted under its own secret. Pick the store for
   those properties; for Redis, the connection and TLS verification are part of the session's security.
9. **Set the refresh interval from the token lifetimes.** The documentation recommends `cookie_refresh`
   equal to the access-token lifespan minus one minute, and `cookie_expire` equal to the refresh-token
   lifespan. With refresh at 0 an access token is never refreshed even when a valid refresh token exists,
   and a refresh interval equal to the lifespan lets a token that expires in transit reach the upstream.
   This is the server-side form of `skills/auth-session-conventions` §1.4.
10. **Keep debug pages and logs out of production.** `--show-debug-on-error` shows detailed error
    information that, in the documentation's words, may contain sensitive information and must not be used
    in production. The documentation says the callback diagnostics for a missing or invalid CSRF cookie
    include cookie names but not values, and are controlled by `--auth-logging`; leave it on. Own guidance:
    do not add a request-logging format that prints the `Authorization` or cookie headers.
11. **Validate the configuration in CI.** `--config-test` runs the same validation as startup (required
    fields, syntax, provider configuration, upstream definitions, and a session-store connectivity check
    when configured), exits 1 on error and cannot be combined with `--convert-config-to-alpha`. Run it
    on every change to the gateway's configuration, with test secrets, not production ones.
12. **Behind an `auth_request` front proxy, copy the refreshed cookie back.** The documented nginx setup says
    that, when cookie refresh is on, the front proxy must copy the `Set-Cookie` the gateway returns to its
    own response, or the refresh never reaches the browser and the person is logged out at the next expiry.
    Symptom: sessions that die at exactly the access-token lifetime while the gateway logs successful
    refreshes. Check: after a refresh, the browser response carries a new session cookie. Source: the nginx
    integration page, read 2026-10-20.
13. **Large tokens split the session cookie, and a proxy may forward only the first part.** The same page
    explains that a big identity token can push the session cookie past the 4 KB cookie limit, so the gateway
    splits it into numbered parts, and nginx by default copies only the first `Set-Cookie` header from the
    auth subrequest. Symptom: login works for people with small tokens and loops for people in many groups.
    Fix: forward every part as the page shows, or move the session to the Redis store (§2.8). Check: log in
    with an account that has the most groups you have.
14. **Sign-out ends only the gateway's session.** The endpoints page says the sign-out endpoint removes the
    gateway's own cookies; the person stays signed in at the identity provider and may be signed straight back
    in. To end both, send the person on to the provider's sign-out page through the redirect parameter, and
    add that host to the redirect allow-list or the redirect is ignored (§2.6). Check: sign out, reload a
    protected page, expect the login prompt rather than the application.
