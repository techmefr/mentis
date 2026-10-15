# oauth-oidc-client-pitfalls §3 — The session and CSRF after login

> Section 3 of `skills/oauth-oidc-client-pitfalls`. Read it when a session is created from a login result,
> or when a cookie-based session gains a form, an API route or a CORS configuration. It states the
> server-set-cookie shape; the token lifecycle and the client-set-cookie pattern some of our frontends use
> are `skills/auth-session-conventions`.

1. **Create a new session at every sign-in; never reuse the one the request arrived with.** Applications
   that keep sessions for anonymous and signed-in users and promote the current one at login are open to
   session fixation, per the Copenhagen Book: an attacker plants a known session ID (a link with the ID in
   the query is the textbook case), the victim signs in, and the attacker now holds a signed-in session.
   Accept session IDs only from cookies and request headers, never from a URL or a form.
2. **The session ID is long and random, and may be stored hashed.** The source asks for a session ID that is
   sufficiently long and random to defeat guessing and says it can be hashed before storage for extra
   safety. The generation rules are `skills/credential-lifecycle-pitfalls` §3.1.
3. **Session cookie attributes.** The source lists `HttpOnly`, `SameSite=Lax` (`Strict` for critical sites),
   `Secure`, `Max-Age` or `Expires` (needed for the cookie to persist) and `Path=/`. It prefers `Lax` over
   `Strict` because a `Strict` cookie is not sent when the user arrives from an external link, which would
   show a signed-out page to a signed-in user. The maximum cookie lifetime is 400 days, so a long session
   re-sets the cookie as it is used. oauth2-proxy's documentation adds a naming point: with `Secure` set,
   use a cookie name with the `__Host-` or `__Secure-` prefix.
4. **A cookie session needs CSRF protection, and `SameSite` is not it.** The browser attaches the cookie to
   a cross-origin form post or `fetch` automatically, so an attacker's page can act as the user without
   ever reading the cookie. The source is explicit that the `SameSite` flag covers cross-site and not
   cross-origin requests (two subdomains are cross-origin but not cross-site) and should not be the only
   layer. It also warns that cookies do not by themselves protect against XSS, since authenticated
   requests can still be made from injected script.
5. **Check `Origin` on every request that is not a GET, and never mutate on a GET.** The source's simplest
   defence is comparing `Origin` with your own origin for non-GET requests and refusing when it differs.
   When the header is missing, refuse; `Referer` is the fallback the source allows. The header can be
   forged by a custom client, but not by JavaScript in a victim's browser, and only browsers are
   vulnerable to CSRF. This only works if no GET changes state, which `SameSite=Lax` also depends on, since
   `Lax` cookies are sent on cross-site GET navigations. Use POST, PUT or DELETE for changes.
6. **If you use tokens, choose a shape that survives subdomains.** The source describes a per-session
   anti-CSRF token in a hidden field, and a signed double-submit cookie: a random token is HMAC-signed with
   a server secret, the HMAC is linked to the session, the token goes in a cookie (`Secure`, `HttpOnly`,
   `SameSite`) and the HMAC in the form. A plain double-submit cookie is not enough, because an attacker who
   controls a subdomain can set their own pair. A token must not be single-use per form render, since one
   use of the back button would break the page.
7. **Keep CORS strict wherever credentials ride on cookies.** The source says that a loose
   `Access-Control-Allow-Credentials` policy lets a hostile site fetch a page with a valid CSRF token in it.
   Own guidance: allow named origins only, never reflect the request's `Origin` back, and never combine a
   wildcard origin with credentials.
8. **Invalidate sessions on sign-out and on a change in who the user is.** Sign-out deletes the session from
   the server and the client. The source adds that all of a user's sessions are invalidated when they gain
   new permissions (email verification, a new role) or change the password; for security-critical
   applications, sign-out also ends every session. The lifecycle rules are `skills/auth-session-conventions`
   §1.5.
9. **Offer sudo mode for the sensitive actions.** Instead of short sessions, the source suggests long
   sessions plus re-authentication, with a password, a passkey or an OTP, before a sensitive action, tracked
   by when the user last used a credential in this session. It also notes that IP and header checks are weak
   because both can be spoofed, which is why sudo mode is the stronger recommendation.
